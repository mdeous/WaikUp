# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for

from waikup.lib import globals as g
from waikup.models import Link
from waikup.forms import NewLinkForm


webui = Blueprint('webui', __name__)


@webui.route('/', methods=['GET', 'POST'])
@g.auth.login_required
def index():
    form = NewLinkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = g.auth.get_logged_in_user()
            link = Link.create(url=form.url.data, title=form.title.data, description=form.description.data, author=user)
            flash("New link added: %s" % form.url.data)
            return redirect(url_for('webui.index'))
        for field_name, field_errors in form.errors.iteritems():
            for field_error in field_errors:
                flash("%s - %s" % (field_name, field_error), category='danger')
        for field in ('url', 'title', 'description'):
            getattr(form, field).data = ''
    links = Link.select()
    return render_template(
        'index.html',
        page_name='index',
        links=links,
        new_link_form=form
    )
