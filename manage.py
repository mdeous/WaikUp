#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from getpass import getpass

from flask_mail import Message
from flask_security import PeeweeUserDatastore
from flask_script import Manager
from jinja2 import Environment, PackageLoader

from waikup.app import app, db, mail
from waikup.models import *

try:
    import simplejson as json
except ImportError:
    import json

TABLES = g.db.Model.__subclasses__()
manager = Manager(app)


def create_categories():
    """
    Inserts the default categories in the database.
    :return: None
    """
    for cat in app.config['DEFAULT_CATEGORIES']:
        if Category.select().where(Category.name == cat).count() == 0:
            print "[+] Inserting category: %s" % cat
            Category.create(name=cat)


@manager.command
def setupdb():
    """
    Creates the database schema.
    :return: None
    """
    for table in TABLES:
        print "[+] Creating table: %s..." % table._meta.name
        table.create_table(fail_silently=True)
    create_categories()
    print "[+] Done"


@manager.command
def resetdb():
    """
    Resets database content.
    :return: None
    """
    for table in TABLES:
        print "[+] Deleting table: %s..." % table._meta.name
        table.delete().execute()
        db.database.execute_sql(*db.database.compiler().drop_table(table, cascade=True))
    setupdb()


@manager.command
def adduser(admin=False, inactive=False):
    """
    Adds a new user.
    :return: None
    """
    user_datastore = PeeweeUserDatastore(db, User, Role, UserRole)
    print "[+] Creating new user (admin=%r, inactive=%r)" % (admin, inactive)
    first_name = raw_input("[>] First name: ")
    last_name = raw_input("[>] Last name: ")
    email = raw_input("[>] Email: ")
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        print "[!] Passwords don't match!"
        sys.exit(1)
    user_datastore.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        admin=admin,
        active=not inactive,
        password=password1
    )
    print "[+] Done"


@manager.command
def chpasswd(username):
    """
    Change given user's password.
    :return: None
    """
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
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
    """
    Sends an email containing last submitted links.
    :return: None
    """
    links = Link.select().where(Link.archived == False)
    if not links:
        print "[+] No new links, nothing to do"
        return
    print "[+] Loading and populating email templates..."
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja2').render(links=links)
    text = env.get_template('text.jinja2').render(links=links)
    recipients = EMail.select().where(EMail.disabled == False)
    for recipient in recipients:
        print "[+] Sending email to %s..." % recipient.address
        msg = Message(recipients=recipient.address)
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
