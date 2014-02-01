#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from flask.ext.mail import Message
from flask.ext.script import Manager
from jinja2 import Environment, PackageLoader

from waikup.app import app, db, mail
from waikup.models import User, Token, Link, Category

manager = Manager(app)


def create_categories():
    for cat in app.config['DEFAULT_CATEGORIES']:
        print "[+] Inserting category: %s" % cat
        Category.create(name=cat)


@manager.command
def setupdb():
    """Creates the database schema."""
    for table in (User, Token, Link, Category):
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
    for table in (Token, Link, User, Category):
        print "[+] Resetting table content: %s..." % table._meta.name
        db.database.drop_table(table)
    create_categories()
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
