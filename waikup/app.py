# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_mail import Mail
from flask_restful import Api
from flask_security import Security, PeeweeUserDatastore
from peewee import fn
from werkzeug.contrib.atom import AtomFeed

from waikup import settings
from waikup.lib import globals as g
from waikup.lib.db import WaikupDB
from waikup.views.admin import CategoryModelView, LinkModelView, UserModelView, \
    RestrictedAdminIndexView, EMailModelView


# Setup application

app = Flask(__name__)
app.config.from_object(settings)
if app.config['DEBUG'] and app.config.get('DEBUG_TB_ENABLED', False):
    from flask_debugtoolbar import DebugToolbarExtension
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    toolbar = DebugToolbarExtension(app)
Bootstrap(app)
CORS(
    app,
    resources={
        r'/api/*': {'origins': 'chrome-extension://*'}
    }
)

# Setup database

db = WaikupDB(app)
g.db = db


# Setup mailing

mail = Mail(app)
g.mail = mail


# Setup authentication

from waikup.models import Category, Link, User, Role, UserRole, WaikUpAnonymousUser, EMail
user_datastore = PeeweeUserDatastore(g.db, User, Role, UserRole)
g.user_datastore = user_datastore
login_manager = Security(
    app,
    user_datastore,
    anonymous_user=WaikUpAnonymousUser
)


# Setup admin panel

admin = Admin(
    app,
    name='WaikUp Admin',
    template_mode='bootstrap3',
    index_view=RestrictedAdminIndexView()
)
admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Category))
admin.add_view(LinkModelView(Link))
admin.add_view(EMailModelView(EMail))

# Setup views

from waikup.views.main import main

app.register_blueprint(main)


# Setup API

from waikup.views.api import api as api_bp, LinkListResource, LinkResource, UserResource, CategoryListResource

api = Api(api_bp)
api.add_resource(LinkListResource, '/links')
api.add_resource(LinkResource, '/links/<int:linkid>')
api.add_resource(UserResource, '/profile')
api.add_resource(CategoryListResource, '/categories')
app.register_blueprint(api_bp, url_prefix='/api')


# Atom feed

@app.route('/links.atom')
def links_feed():
    """
    Atom feed view.
    :return: Atom feed HTTP response.
    """
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


# Context processors

@app.context_processor
def global_forms():
    """
    Context processor that defines forms used in every view.
    :return: a {form_name: form_object} dict.
    """
    from waikup.forms import NewLinkForm, ChangePasswordForm
    newlink_form = NewLinkForm()
    newlink_form.set_category_choices()
    return {
        'new_link_form': newlink_form,
        'chpasswd_form': ChangePasswordForm()
    }
