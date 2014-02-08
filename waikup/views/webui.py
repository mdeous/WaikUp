# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for

from waikup.lib import globals as g
from waikup.models import Link, Category
from waikup.forms import NewLinkForm, ChangePasswordForm


webui = Blueprint('webui', __name__)


@webui.route('/')
@g.auth.login_required
def index():
    toggle_link_id = request.args.get('toggle')
    if toggle_link_id is not None:
        result_ok = Link.toggle_archiving(toggle_link_id)
        if result_ok:
            flash("Archived link %s" % toggle_link_id, category="success")
        else:
            flash("Link does not exist: %s" % toggle_link_id, category="danger")
    links = Link.select().where(Link.archived == False).order_by(Link.submitted.desc())
    return render_template(
        'links_list.html',
        page_name='index',
        links=links
    )


@webui.route('/archives')
@g.auth.login_required
def archives():
    toggle_link_id = request.args.get('toggle')
    if toggle_link_id is not None:
        result_ok = Link.toggle_archiving(toggle_link_id)
        if result_ok:
            flash("Marked link as active: %s" % toggle_link_id, category="success")
        else:
            flash("Link does not exist: %s" % toggle_link_id, category="danger")
    links = Link.select().where(Link.archived == True).order_by(Link.submitted.desc())
    return render_template(
        'links_list.html',
        page_name='archives',
        links=links
    )


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


@webui.route('/delete')
@g.auth.admin_required
def delete_link():
    redirect_to = request.args.get('redir', 'index')
    redirect_to = url_for('webui.'+redirect_to)
    linkid = request.args.get('linkid')
    if linkid is None:
        flash("No link specified", category='danger')
        return redirect(redirect_to)
    links = list(Link.select().where(Link.id == linkid))
    if not links:
        flash("Link does not exist: %s" % linkid, category='danger')
        return redirect(redirect_to)
    link = links[0]
    link.delete_instance()
    flash("Deleted link: %s" % linkid, category='success')
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
