# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.mail import Mail
from flask.ext.peewee.db import Database
from peewee import fn
from werkzeug.contrib.atom import AtomFeed

from waikup import settings
from waikup.lib import globals as g
from waikup.lib.errors import ApiError, http_error


# Setup application

app = Flask(__name__)
app.config.from_object(settings)
g.app = app


# Setup database

db = Database(app)
g.db = db


# Setup mailing

mail = Mail(app)
g.mail = mail


# Setup authentication and admin panel

from flask.ext.peewee.admin import Admin
from waikup.models import HybridAuth
from waikup.models import User, Token, Link, Category
from waikup.models import UserAdmin, TokenAdmin, LinkAdmin, CategoryAdmin

auth = HybridAuth(app, db)
g.auth = auth

admin = Admin(app, auth)
admin.register(User, UserAdmin)
admin.register(Token, TokenAdmin)
admin.register(Link, LinkAdmin)
admin.register(Category, CategoryAdmin)
admin.setup()
g.admin = admin


# Setup views

from waikup.views.api.links import links
from waikup.views.api.users import users
from waikup.views.webui import webui

app.register_blueprint(webui)
app.register_blueprint(links, url_prefix='/api/links')
app.register_blueprint(users, url_prefix='/api/users')


@app.route('/links.atom')
def links_feed():
    feed_title = 'Recently submitted links'
    cat = request.args.get('cat')
    if cat is not None:
        feed_title += (' - %s' % cat.title())
        category = Category.get(fn.lower(Category.name) == cat.lower())
        all_links = Link.select().where(Link.category == category).limit(settings.ATOM_LINKS_COUNT)
    else:
        all_links = Link.select().limit(settings.ATOM_LINKS_COUNT)
    feed = AtomFeed(
        feed_title,
        feed_url=request.url,
        url=request.base_url
    )
    for link in all_links:
        feed.add(
            link.title,
            unicode(link.description),
            content_type='text',
            author='%s %s' % (link.author.first_name, link.author.last_name),
            url=link.url,
            updated=link.submitted
        )
    return feed.get_response()


@app.context_processor
def global_forms():
    from waikup.forms import NewLinkForm, ChangePasswordForm
    newlink_form = NewLinkForm()
    newlink_form.set_category_choices()
    return {
        'new_link_form': newlink_form,
        'chpasswd_form': ChangePasswordForm()
    }


# Setup custom error handlers

@app.errorhandler(ApiError)
def api_error_handler(error):
    response = error.json
    response.status_code = error.status_code
    return response


@app.errorhandler(401)
def unauthorized_handler(error):
    return http_error(error)


@app.errorhandler(403)
def forbidden_error(error):
    return http_error(error)


@app.errorhandler(404)
def not_found_handler(error):
    return http_error(error)


@app.errorhandler(410)
def gone_handler(error):
    return http_error(error)


@app.errorhandler(500)
def server_error_handler(error):
    return http_error(error)
