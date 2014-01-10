# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for
from peewee import DoesNotExist

from waikup.lib import globals as g
from waikup.models import Link
from waikup.forms import NewLinkForm


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
    links = Link.select().where(Link.archived == False)
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
    links = Link.select().where(Link.archived == True)
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
    if form.validate_on_submit():
        user = g.auth.get_logged_in_user()
        link = Link.create(url=form.url.data, title=form.title.data, description=form.description.data, author=user)
        flash("New link added: %s" % form.url.data)
        return redirect(redirect_to)
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='danger')
    for field in ('url', 'title', 'description'):
        getattr(form, field).data = ''
    return redirect(redirect_to)
