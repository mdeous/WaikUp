# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.peewee.db import Database
from werkzeug.contrib.atom import AtomFeed

from waikup import settings
from waikup.forms import NewLinkForm
from waikup.lib import globals as g
from waikup.lib.errors import ApiError, http_error


# Setup application

app = Flask(__name__)
app.config.from_object(settings)
g.app = app


# Setup database

db = Database(app)
g.db = db


# Setup authentication and admin panel

from flask.ext.peewee.admin import Admin
from waikup.models import User, Token, Link, UserAdmin, TokenAdmin, LinkAdmin, HybridAuth

auth = HybridAuth(app, db)
g.auth = auth

admin = Admin(app, auth)
admin.register(User, UserAdmin)
admin.register(Token, TokenAdmin)
admin.register(Link, LinkAdmin)
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
    feed = AtomFeed(
        'Recently submitted links',
        feed_url=request.url,
        url=request.base_url
    )
    all_links = Link.select().limit(settings.ATOM_LINKS_COUNT)
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
def new_link_form():
    return {'new_link_form': NewLinkForm()}


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


# Setup debug toolbar

if app.debug:
    from flask.ext.debugtoolbar import DebugToolbarExtension
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    app.config['DEBUG_TB_PANELS'] = (
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    )
    toolbar = DebugToolbarExtension(app)
