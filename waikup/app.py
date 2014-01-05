# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.peewee.db import Database

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


# Setup authentication and admin panel
from waikup.models import User, Token, Link, UserAdmin, TokenAdmin, LinkAdmin, CustomAuth, CustomAdmin

auth = CustomAuth(app, db)
g.auth = auth

admin = CustomAdmin(app, auth)
admin.register(User, UserAdmin)
admin.register(Token, TokenAdmin)
admin.register(Link, LinkAdmin)
admin.setup()
g.admin = admin


# Setup views
from waikup.views.api.links import links
from waikup.views.api.users import users
from waikup.views.webui import webui

app.register_blueprint(webui, url_prefix='/')
app.register_blueprint(links, url_prefix='/api/links')
app.register_blueprint(users, url_prefix='/api/users')


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


