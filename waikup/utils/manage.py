#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import sys
from getpass import getpass
from random import choice

from flask.ext.mail import Message
from flask.ext.script import Manager
from jinja2 import Environment, PackageLoader
from peewee import IntegrityError, PeeweeException

from waikup.app import app, db, mail
from waikup.lib.errors import ApiError
from waikup.models import User, Token, Link, Category
from waikup.utils import migrations

try:
    import simplejson as json
except ImportError:
    import json

TABLES = [User, Token, Category, Link]
manager = Manager(app)


def create_categories():
    for cat in app.config['DEFAULT_CATEGORIES']:
        if Category.select.where(Category.name == cat).count() == 0:
            print "[+] Inserting category: %s" % cat
            Category.create(name=cat)


def read_db_version():
    version = 0
    if os.path.exists(app.config['DB_VERSION_FILE']):
        with open(app.config['DB_VERSION_FILE']) as inf:
            version = inf.read().strip() or '0'
            if not version.isdigit():
                print "[!] Unexpected version value: %s" % version
                sys.exit(2)
    return int(version)


def write_db_version(ver):
    with open(app.config['DB_VERSION_FILE'], 'w') as outf:
        outf.write(str(ver))


@manager.command
def setupdb():
    """Creates the database schema."""
    for table in TABLES:
        print "[+] Creating table: %s..." % table._meta.name
        table.create_table(fail_silently=True)
    create_categories()
    print "[+] Adding default credentials 'admin:admin'..."
    user = User(
        username='admin',
        first_name='WaikUp',
        last_name='Admin',
        email='admin@example.org',
        admin=True,
        active=True
    )
    user.set_password('admin')
    user.save()
    print "[+] Creating internal API user"
    api_user = User(
        username='waikupapi',
        first_name='WaikUp',
        last_name='API',
        email='api@example.org',
        admin=False,
        active=True
    )
    api_user.set_password(''.join(choice(string.printable) for _ in xrange(64)))
    api_user.save()
    print "[+] Assigning new API token to 'waikupapi' user"
    api_token = api_user.generate_token()
    print "[+] Done"


@manager.command
def resetdb():
    """Resets database content."""
    for table in reversed(TABLES):
        print "[+] Resetting table: %s..." % table._meta.name
        table.delete().execute()
        db.database.execute_sql(*db.database.compiler().drop_table(table, cascade=True))
    setupdb()


@manager.command
def importdb(model_name, data_file):
    """Imports a JSON file previously generated with admin interface export command."""
    # handle arguments errors
    print "[+] Importing %s data from %s" % (model_name, data_file)
    created_objects = 0
    table_names = [t._meta.name.lower() for t in TABLES]
    if model_name.lower() not in table_names:
        print "[!] Unknown model name: %s" % model_name
        sys.exit(1)
    model_class = TABLES[table_names.index(model_name.lower())]
    if not os.path.exists(data_file) and not os.path.isfile(data_file):
        print "[!] File not found: %s" % data_file
        sys.exit(2)
    with open(data_file) as inf:
        data = json.load(inf)
        for item in data:
            # remove the 'id' field (will be automatically generated)
            if 'id' in item:
                del item['id']
            # handle item's foreign keys
            fk_names = [f for f in item if isinstance(item[f], dict)]
            for fk_name in fk_names:
                if ('id' in item[fk_name]) and (len(item[fk_name].keys()) > 1):
                    del item[fk_name]['id']
                if fk_name not in model_class._meta.fields:
                    print "[!] Unexpected foreign key field: %s" % fk_name
                    sys.exit(3)
                fk_model_cls = model_class._meta.fields[fk_name].rel_model
                # get item with given criteria from db (or create it)
                item[fk_name] = fk_model_cls.get_or_create(**item[fk_name])
            # create a model object from the JSON item
            model_obj = model_class()
            for field in item:
                setattr(model_obj, field, item[field])
            try:
                model_obj.save()
                created_objects += 1
            except IntegrityError:
                db.database.rollback()
                continue
    print "[+] Created %d %s objects" % (created_objects, model_name)
    print "[+] Done"


@manager.command
@manager.option('-v', '--version', dest='version', default=None, help='Schema version to upgrade to')
def migratedb(version=None):
    """Applies database schema migrations."""
    current_version = read_db_version()
    max_version = version or len(migrations.modules)
    highest_version = len(migrations.modules)
    if max_version == current_version:
        print "[+] No schema migration to apply"
        sys.exit(0)
    elif max_version > highest_version:
        print "[!] Can't apply version %d, max version is %d" % (max_version, highest_version)
        sys.exit(1)
    for migration in migrations.modules[current_version:]:
        vernum = migrations.modules.index(migration)+1
        if vernum > max_version:
            break
        try:
            migration.migrate()
            print "[!] Applied schema migration: %d"
        except PeeweeException as err:
            print "[!] Error: %s" % err.message
            sys.exit(3)
        write_db_version(vernum)
    print "[+] Done"
    pass


@manager.command
def adduser(admin=False, inactive=False):
    """Adds a new user."""
    print "[+] Creating new user (admin=%r, inactive=%r)" % (admin, inactive)
    username = raw_input("[>] Username: ")
    first_name = raw_input("[>] First name: ")
    last_name = raw_input("[>] Last name: ")
    email = raw_input("[>] Email: ")
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        print "[!] Passwords don't match!"
        sys.exit(1)
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        admin=admin,
        active=not inactive
    )
    user.set_password(password1)
    user.save()
    print "[+] Done"


@manager.command
def chpasswd(username):
    """Change given user's password."""
    try:
        user = User.get(User.username == username)
    except ApiError:
        print "[!] Unknown user: %s" % username
        sys.exit(1)
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        print "[!] Passwords don't match!"
        sys.exit(2)
    print "[+] Changing %s's password" % username
    user.set_password(password1)
    user.save()
    print "[+] Done"


@manager.command
def sendmail():
    """Sends an email containing lastly submitted links."""
    links = Link.select().where(Link.archived == False)
    print "[+] Loading and populating email templates..."
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja2').render(links=links)
    text = env.get_template('text.jinja2').render(links=links)
    print "[+] Sending email..."
    msg = Message(recipients=app.config['MAIL_RECIPIENTS'])
    msg.subject = app.config['MAIL_TITLE']
    msg.body = text
    msg.html = html
    mail.send(msg)
    print "[+] Archiving links..."
    for link in links:
        link.archived = True
        link.save()
    print "[+] Done"


def main():
    manager.run()


if __name__ == '__main__':
    main()
