# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for

from waikup.lib import globals as g
from waikup.models import Link, Category, Paginated
from waikup.forms import NewLinkForm, ChangePasswordForm, EditLinkForm, SimpleLinkForm, flash_form_errors

ITEMS_PER_PAGE = 10


webui = Blueprint('webui', __name__)


def list_links(page_name, links=None):
    toggle_link_id = request.args.get('toggle')
    page_num = request.args.get('page')
    toggle_form = SimpleLinkForm()
    delete_form = SimpleLinkForm()
    if (page_num is None) or (not page_num.isdigit()):
        page_num = 1
    else:
        page_num = int(page_num)
    if toggle_form.validate_on_submit():
        result_ok = Link.toggle_archiving(toggle_link_id)
        if result_ok:
            flash("Toggled archiving for link %s" % toggle_link_id, category="success")
        else:
            flash("Link does not exist: %s" % toggle_link_id, category="danger")
    else:
        flash_form_errors(toggle_form)
    if links is None:
        links = Link.select().where(Link.archived == (page_name == 'archives')).order_by(Link.submitted.desc())
    links = Paginated(links, page_num, ITEMS_PER_PAGE, links.count())
    return render_template(
        'links_list.html',
        page_name=page_name,
        links=links,
        toggle_form=toggle_form,
        delete_form=delete_form
    )


@webui.route('/', methods=['GET', 'POST'])
@g.auth.login_required
def index():
    return list_links('index')


@webui.route('/archives', methods=['GET', 'POST'])
@g.auth.login_required
def archives():
    return list_links('archives')


@webui.route('/newlink', methods=['POST'])
@g.auth.login_required
def new_link():
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('webui.'+redirect_to)
    form = NewLinkForm()
    form.set_category_choices()
    if form.validate_on_submit():
        user = g.auth.get_logged_in_user()
        category = Category.get(Category.name == form.category.data)
        link = Link.create(
            url=form.url.data,
            title=form.title.data,
            description=form.description.data,
            author=user,
            category=category
        )
        flash("New link added: %s" % form.url.data)
        return redirect(redirect_to)
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='danger')
    return redirect(redirect_to)


@webui.route('/chpasswd', methods=['POST'])
@g.auth.login_required
def change_password():
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('webui.'+redirect_to)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = g.auth.get_logged_in_user()
        errors = False
        if not user.check_password(form.old.data):
            flash("Wrong password", category='danger')
            return redirect(redirect_to)
        user.set_password(form.new.data)
        user.save()
        flash("Password changed", category='success')
        return redirect(redirect_to)
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='danger')
    return redirect(redirect_to)


@webui.route('/delete', methods=['POST'])
@g.auth.login_required
def delete_link():
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('webui.'+redirect_to)
    linkid = request.args.get('linkid')
    delete_form = SimpleLinkForm()
    if delete_form.validate_on_submit():
        if linkid is None:
            flash("No link specified", category='danger')
            return redirect(redirect_to)
        link = Link.get(Link.id == linkid)
        if link is None:
            flash("Link not found: %s" % linkid)
            return redirect(redirect_to)
        user = g.auth.get_logged_in_user()
        if (not user.admin) and (user.username != link.author.username):
            flash("You are not allowed to delete this link: %s" % linkid, category='danger')
            return redirect(redirect_to)
        link.delete_instance()
        flash("Deleted link: %s" % linkid, category='success')
    else:
        flash_form_errors(delete_form)
    return redirect(redirect_to)


@webui.route('/email', methods=['GET', 'POST'])
@g.auth.admin_required
def email_mgmt():
    return render_template(
        'email_mgmt.html',
        page_name='email_mgmt'
    )


@webui.route('/genmail')
@g.auth.admin_required
def genmail():
    return render_template('emails/html.jinja2', links=Link.select().where(Link.archived == False))


@webui.route('/token')
@g.auth.login_required
def token():
    def generate_token(user):
        new_token = user.generate_token()
        flash('New token generated: %s' % new_token.token, category='success')

    def delete_token(user):
        if user.token.count() == 0:
            flash('No token to delete', category='danger')
            return
        user.delete_token()
        flash('Token deleted', category='success')

    token_actions = {
        'generate': generate_token,
        'delete': delete_token
    }
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('webui.' + redirect_to)
    action = request.args.get('action')
    if action is None:
        flash('No action specified', category='danger')
        return redirect(redirect_to)
    if action not in token_actions:
        flash('Unknown action: %s' % action, category='danger')
        return redirect(redirect_to)
    current_user = g.auth.get_logged_in_user()
    token_actions[action](current_user)
    return redirect(redirect_to)


@webui.route('/stats')
@g.auth.login_required
def stats():
    return render_template(
        'stats.html',
        page_name="stats"
    )


@webui.route('/search', methods=['POST'])
@g.auth.login_required
def search():
    redirect_page = request.args.get('redir', 'index')
    page_num = request.args.get('page')
    if (page_num is None) or (not page_num.isdigit()):
        page_num = 1
    else:
        page_num = int(page_num)
    redirect_to = url_for('webui.' + redirect_page)
    pattern = request.form.get('pattern')
    if pattern is None:
        flash("No pattern given", category='danger')
        return list_links(redirect_page)
    archived = redirect_page == 'archives'
    pattern = "%%%s%%" % pattern
    links = Link.select().where(Link.archived == archived).where(
        (Link.title ** pattern) | (Link.description ** pattern)
    )
    return list_links(redirect_page, links=links)


@webui.route('/edit_link/<int:linkid>', methods=['GET', 'POST'])
@g.auth.login_required
def edit_link(linkid):
    form = EditLinkForm()
    form.set_category_choices()
    link = Link.get(Link.id == linkid)
    redirect_page = request.args.get('redir', 'index')
    redirect_to = url_for('webui.'+redirect_page)
    if link is None:
        flash("Link not found: %d" % linkid, category='danger')
        return redirect(redirect_to)
    if request.method == 'POST':
        user = g.auth.get_logged_in_user()
        if (not user.admin) and (user.username != link.author.username):
            flash("You are not allowed to edit this link: %d" % link.id, category='danger')
            return redirect(redirect_to)
        if form.validate_on_submit():
            link.title = form.title.data
            link.url = form.url.data
            link.description = form.description.data
            category = Category.get(Category.name == form.category.data)
            link.category = category
            link.save()
            flash("Updated link: %d" % link.id)
        else:
            flash_form_errors(form)
        return redirect(redirect_to)
    form.title.data = link.title
    form.url.data = link.url
    form.description.data = link.description
    form.category.data = link.category.name
    return render_template(
        'edit_link_modal_content.html',
        edit_link_form=form,
        link=link,
        page_name=redirect_page
    )
