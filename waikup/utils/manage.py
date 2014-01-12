#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from flask.ext.mail import Message
from flask.ext.script import Manager
from jinja2 import Environment, PackageLoader

from waikup.app import app, db, mail
from waikup.models import User, Token, Link

manager = Manager(app)


@manager.command
def setupdb():
    """Creates the database schema."""
    for table in (User, Token, Link):
        print "[+] Creating table: %s..." % table._meta.name
        table.create_table(fail_silently=True)
    print "[+] Done"


@manager.command
def resetdb():
    """Resets database content."""
    for table in (Token, Link, User):
        print "[+] Resetting table content: %s..." % table._meta.name
        db.database.drop_table(table)
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
    html = env.get_template('html.jinja').render(links=links, reply_to=app.config['MAIL_REPLY_TO'])
    text = env.get_template('text.jinja').render(links=links, reply_to=app.config['MAIL_REPLY_TO'])
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
