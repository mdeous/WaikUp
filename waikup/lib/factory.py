# coding: utf-8


def create_cors():
    from flask_cors import CORS
    cors = CORS(
        resources={
            r'/api/*': {'origins': 'chrome-extension://*'}
        }
    )
    return cors


def create_security():
    from flask_security import Security
    from .models import WaikUpAnonymousUser
    security = Security(anonymous_user=WaikUpAnonymousUser)
    return security


def create_security_datastore(db):
    from flask_security import PeeweeUserDatastore
    from .models import UserRole, User, Role
    datastore = PeeweeUserDatastore(db, User, Role, UserRole)
    return datastore


def create_admin():
    from flask_admin import Admin
    from .models import User, Category, Link, EMail
    from ..views.admin import (
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
    from ..views.api import LinkListResource, LinkResource, UserResource, CategoryListResource
    api = Api(prefix='/api')
    api.add_resource(LinkListResource, '/links')
    api.add_resource(LinkResource, '/links/<int:linkid>')
    api.add_resource(UserResource, '/profile')
    api.add_resource(CategoryListResource, '/categories')
    return api


def create_app(settings):
    """
    Application factory.
    :param settings: Settings object from imported file.
    :return: a Flas application.
    """
    extensions = []

    # Main application
    from flask import Flask
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings)

    # Database
    from .models import db
    db.init_app(app)

    # Flask-Reverse-Proxy
    if app.config['REVERSE_PROXIED']:
        from flask_reverse_proxy import FlaskReverseProxied
        rp = FlaskReverseProxied()
        extensions.append(rp)

    # Flask-Security
    security = create_security()
    security_datastore = create_security_datastore(db)
    security.init_app(app, datastore=security_datastore)

    # Flask-DebugToolbar
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
    mail = Mail()
    extensions.append(mail)

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
    from ..views.main import main
    app.register_blueprint(main)

    return app
