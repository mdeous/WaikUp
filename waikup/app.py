# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.peewee.admin import Admin
from flask.ext.peewee.auth import Auth
from flask.ext.peewee.db import Database

from waikup import settings
from waikup.api.links import links
from waikup.api.users import users
from waikup.lib.errors import ApiError, http_error

# Setup application
app = Flask(__name__)
app.config.from_object(settings)

# Setup views
app.register_blueprint(links, url_prefix='/api/links')
app.register_blueprint(users, url_prefix='/api/users')

# Setup database and admin area
db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)


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


