# coding: utf-8
from waikup.lib import globals as g


def create_cors():
    from flask_cors import CORS
    cors = CORS(
        resources={
            r'/api/*': {'origins': 'chrome-extension://*'}
        }
    )
    return cors


def create_security():
    from waikup.models import WaikUpAnonymousUser
    from flask_security import Security, PeeweeUserDatastore
    from waikup.models import User, Role, UserRole
    g.user_datastore = PeeweeUserDatastore(g.db, User, Role, UserRole)
    security = Security(anonymous_user=WaikUpAnonymousUser)
    return security


def create_admin():
    from flask_admin import Admin
    from waikup.models import User, Category, Link, EMail
    from waikup.views.admin import (
        RestrictedAdminIndexView, UserModelView, CategoryModelView, LinkModelView, EMailModelView
    )
    admin = Admin(
        name='WaikUp Admin',
        template_mode='bootstrap3',
        index_view=RestrictedAdminIndexView()
    )
    admin.add_view(UserModelView(User))
    admin.add_view(CategoryModelView(Category))
    admin.add_view(LinkModelView(Link))
    admin.add_view(EMailModelView(EMail))
    return admin


def create_api():
    from flask_restful import Api
    from waikup.views.api import LinkListResource, LinkResource, UserResource, CategoryListResource
    api = Api(prefix='/api')
    api.add_resource(LinkListResource, '/links')
    api.add_resource(LinkResource, '/links/<int:linkid>')
    api.add_resource(UserResource, '/profile')
    api.add_resource(CategoryListResource, '/categories')
    return api


def create_blueprints(app):
    pass


def create_app(settings):
    """
    Application factory.
    :param settings: Settings object from imported file.
    :return: a Flas application.
    """
    extensions = []

    # Main application
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(settings)

    # Database
    from waikup.lib.db import WaikupDB
    g.db = WaikupDB()
    g.db.init_app(app)

    # Flask-Security
    security = create_security()
    security.init_app(app, datastore=g.user_datastore)

    # Flask-DebugToolbar
    fdt = None
    if app.config['DEBUG'] and app.config.get('DEBUG_TB_ENABLED', False):
        from flask_debugtoolbar import DebugToolbarExtension
        fdt = DebugToolbarExtension()
    extensions.append(fdt)

    # Flask-Bootstrap
    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()
    extensions.append(bootstrap)

    # Flask-CORS
    cors = create_cors()
    extensions.append(cors)

    # Flask-Mail
    from flask_mail import Mail
    g.mail = Mail()
    extensions.append(g.mail)

    # Flask-Admin
    admin = create_admin()
    extensions.append(admin)

    # Flask-RESTful
    api = create_api()
    extensions.append(api)

    # Initialize extentions
    for extension in extensions:
        if extension is not None:
            extension.init_app(app)

    # Register blueprints
    from waikup.views.main import main
    app.register_blueprint(main)

    return app
