#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from getpass import getpass

from flask.ext.mail import Message
from flask.ext.script import Manager
from jinja2 import Environment, PackageLoader
from peewee import IntegrityError

from waikup.app import app, db, mail
from waikup.models import User, Token, Link, Category

try:
    import simplejson as json
except ImportError:
    import json

TABLES = [User, Token, Category, Link]
manager = Manager(app)


def create_categories():
    for cat in app.config['DEFAULT_CATEGORIES']:
        print "[+] Inserting category: %s" % cat
        Category.create(name=cat)


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
                # try to get item with given criteria from db
                query = fk_model_cls.select().where(
                    *[getattr(fk_model_cls, fk_field) == item[fk_name][fk_field] for fk_field in item[fk_name]]
                )
                fk_obj = query.first()
                # item does not exist in db, create it
                if fk_obj is None:
                    if not item[fk_name]:
                        print "[!] Only 'id' field provided for '%s', but wasn't found, skipping item" % fk_name
                        sys.exit(3)
                    fk_obj = fk_model_cls()
                    for fk_field in item[fk_name]:
                        setattr(fk_obj, fk_field, item[fk_name][fk_field])
                    try:
                        fk_obj.save()
                        print "[+] Created %s object" % fk_name
                    except IntegrityError:
                        print "[!] Duplicate %s object, skipping" % fk_name
                        db.database.rollback()
                        continue
                item[fk_name] = fk_obj
            # create a model object from the JSON item
            model_obj = model_class()
            for field in item:
                setattr(model_obj, field, item[field])
            try:
                model_obj.save()
                print "[+] Created %s object" % model_name
            except IntegrityError:
                print "[!] Duplicate %s object, skipping" % model_name
                db.database.rollback()
                continue
    print "[+] Done"


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
def sendmail():
    """Sends an email containing lastly submitted links."""
    links = Link.select().where(Link.archived == False)
    print "[+] Loading and populating email templates..."
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja').render(links=links)
    text = env.get_template('text.jinja').render(links=links)
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
