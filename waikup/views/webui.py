# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for

from waikup.lib import globals as g
from waikup.models import Link
from waikup.forms import NewLinkForm


webui = Blueprint('webui', __name__)


@webui.route('/', methods=['GET', 'POST'])
@g.auth.login_required
def index():
    links = Link.select().where(Link.archived == False)
    return render_template(
        'index.html',
        page_name='index',
        links=links
    )


@webui.route('/archives', methods=['GET', 'POST'])
@g.auth.login_required
def archives():
    links = Link.select().where(Link.archived == True)
    return render_template(
        'archives.html',
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
