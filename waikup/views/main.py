# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask.ext.security import login_required, current_user

from waikup.lib.helpers import Paginated
from waikup.models import Link, Category
from waikup.forms import NewLinkForm, ChangePasswordForm, EditLinkForm, SimpleLinkForm, flash_form_errors

main = Blueprint('main', __name__)


def list_links(page_name, links=None):
    """
    Used for both index and archives view, returns a page containing given (or all) links.
    :param page_name: 'index' or 'archives'
    :param links: list of links to return in the page, or None
    :return: rendered HTML page
    """
    toggle_link_id = request.form.get('link_id')
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
    links = Paginated(links, page_num, current_app.config['ITEMS_PER_PAGE'], links.count())
    return render_template(
        'links_list.html',
        page_name=page_name,
        links=links,
        toggle_form=toggle_form,
        delete_form=delete_form
    )


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Index page view.
    :return: rendered HTML page.
    """
    return list_links('index')


@main.route('/archives', methods=['GET', 'POST'])
@login_required
def archives():
    """
    Archives page view.
    :return: rendered HTML page.
    """
    return list_links('archives')


@main.route('/newlink', methods=['POST'])
@login_required
def new_link():
    """
    New link submission view.
    :return: redirects to page from where submission was made.
    """
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('main.'+redirect_to)
    form = NewLinkForm()
    form.set_category_choices()
    if form.validate_on_submit():
        category = Category.get(Category.name == form.category.data)
        Link.create(
            url=form.url.data,
            title=form.title.data,
            description=form.description.data,
            author=current_user.id,
            category=category
        )
        flash("New link added: %s" % form.url.data, category='success')
        return redirect(redirect_to)
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='error')
    return redirect(redirect_to)


@main.route('/chpasswd', methods=['POST'])
@login_required
def change_password():
    """
    Password changing view.
    :return: redirects to page from which password changing occured.
    """
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('main.'+redirect_to)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current.data):
            flash("Wrong password", category='error')
            return redirect(redirect_to)
        current_user.set_password(form.new.data)
        current_user.save()
        flash("Password changed", category='success')
        return redirect(redirect_to)
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='error')
    return redirect(redirect_to)


@main.route('/delete', methods=['POST'])
@login_required
def delete_link():
    """
    Link deletion view.
    :return: redirects to page from which link deletion occured.
    """
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('main.'+redirect_to)
    linkid = request.form.get('link_id')
    delete_form = SimpleLinkForm()
    if delete_form.validate_on_submit():
        if linkid is None:
            flash("No link specified", category='error')
            return redirect(redirect_to)
        try:
            link = Link.get(Link.id == linkid)
        except Link.DoesNotExist:
            flash("Link not found: %s" % linkid, category='error')
            return redirect(redirect_to)
        if (not current_user.is_admin) and (current_user.username != link.author.username):
            flash("You are not allowed to delete this link: %s" % linkid, category='error')
            return redirect(redirect_to)
        link.delete_instance()
        flash("Deleted link: %s" % linkid, category='success')
    else:
        flash_form_errors(delete_form)
    return redirect(redirect_to)


@main.route('/search', methods=['GET'])
@login_required
def search():
    """
    Link search view.
    :return: rendered HTML page with links matching search terms.
    """
    redirect_page = request.args.get('page', 'index')
    page_num = request.args.get('page')
    if (page_num is None) or (not page_num.isdigit()):
        page_num = 1
    else:
        page_num = int(page_num)
    pattern = request.args.get('pattern')
    if pattern is None:
        flash("No pattern given", category='error')
        return list_links(redirect_page)
    archived = redirect_page == 'archives'
    pattern = "%%%s%%" % pattern
    links = Link.select().where(Link.archived == archived).where(
        (Link.title ** pattern) | (Link.description ** pattern)
    )
    links = Paginated(links, page_num, current_app.config['ITEMS_PER_PAGE'], links.count())
    return render_template(
        'links_list.html',
        page_name=redirect_page,
        links=links,
        toggle_form=SimpleLinkForm(),
        delete_form=SimpleLinkForm()
    )


@main.route('/edit_link/<int:linkid>', methods=['GET', 'POST'])
@login_required
def edit_link(linkid):
    """
    Link edition view.
    :param linkid: id of link being edited.
    :return: rendered HTML for modal's content.
    """
    form = EditLinkForm()
    form.set_category_choices()
    redirect_page = request.args.get('redir', 'index')
    redirect_to = url_for('main.'+redirect_page)
    try:
        link = Link.get(Link.id == linkid)
    except Link.DoesNotExist:
        flash("Link not found: %d" % linkid, category='error')
        return redirect(redirect_to)
    if request.method == 'POST':
        if (not current_user.is_admin) and (current_user.username != link.author.username):
            flash("You are not allowed to edit this link: %d" % link.id, category='error')
            return redirect(redirect_to)
        if form.validate_on_submit():
            link.title = form.title.data
            link.url = form.url.data
            link.description = form.description.data
            category = Category.get(Category.name == form.category.data)
            link.category = category
            link.save()
            flash("Updated link: %d" % link.id, category='success')
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
