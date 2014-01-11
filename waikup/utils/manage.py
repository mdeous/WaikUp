#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from flask.ext.script import Manager

from waikup.app import app, db
from waikup.models import User, Token, Link

manager = Manager(app)


@manager.command
def setupdb():
    for table in (User, Token, Link):
        table.create_table(fail_silently=True)


@manager.command
def resetdb():
    for table in (Token, Link, User):
        db.database.drop_table(table)


@manager.command
def adduser(admin=False, inactive=False):
    username = raw_input("Username: ")
    first_name = raw_input("First name: ")
    last_name = raw_input("Last name: ")
    email = raw_input("Email: ")
    password1 = getpass()
    password2 = getpass('Confirm password: ')
    if password1 != password2:
        print "Passwords don't match!"
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


def main():
    manager.run()


if __name__ == '__main__':
    main()
