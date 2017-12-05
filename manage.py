#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from getpass import getpass

import click
from flask import current_app
from flask.cli import FlaskGroup
from flask_mail import Message
from jinja2 import Environment, PackageLoader

from waikup import settings
from waikup.lib.factory import create_app
from waikup.lib.models import db, Category, User, Link, EMail
# TODO: add user management commands (list, edit, delete)
# TODO: allow user management commands to take input from stdin
# TODO: implement database migration

TABLES = db.Model.__subclasses__()


def create_cli_app(_):
    return create_app(settings)


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    click.echo('[ WaikUp Management Tool ]\n')


@cli.command()
def setupdb():
    """
    Creates the database schema.
    :return: None
    """
    for table in TABLES:
        click.echo("[+] Creating table: {}...".format(table._meta.name))
        table.create_table(fail_silently=True)
    for cat in current_app.config['DEFAULT_CATEGORIES']:
        if Category.select().where(Category.name == cat).count() == 0:
            click.echo("[+] Inserting category: {}".format(cat))
            Category.create(name=cat)
    click.echo("[+] Done")


@cli.command()
def resetdb():
    """
    Resets database content.
    :return: None
    """
    for table in TABLES:
        click.echo("[+] Deleting table: {}...".format(table._meta.name))
        table.delete().execute()
        db.database.execute_sql(*db.database.compiler().drop_table(table, cascade=True))
    setupdb()


@cli.command()
@click.option('--admin', default=False, is_flag=True)
def adduser(admin):
    """
    Adds a new user.
    :return: None
    """
    click.echo("[+] Creating new user (admin={})".format(admin))
    first_name = raw_input("[>] First name: ")
    last_name = raw_input("[>] Last name: ")
    email = raw_input("[>] Email: ")
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        click.echo("[!] Passwords don't match!")
        sys.exit(1)
    current_app.extensions['security'].datastore.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        admin=admin,
        password=password1
    )
    click.echo("[+] Done")


@cli.command()
@click.argument('email')
def chpasswd(email):
    """
    Change given user's password.
    :return: None
    """
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        click.echo("[!] Unknown user: {}".format(email))
        sys.exit(1)
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        click.echo("[!] Passwords don't match!")
        sys.exit(2)
    click.echo("[+] Changing {}'s password".format(email))
    user.set_password(password1)
    user.save()
    click.echo("[+] Done")


@cli.command()
def sendmail():
    """
    Sends an email containing last submitted links.
    :return: None
    """
    links = Link.select().where(Link.archived == False)
    if not links:
        click.echo("[+] No new links, nothing to do")
        return
    click.echo("[+] Loading and populating email templates...")
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja2').render(links=links)
    text = env.get_template('text.jinja2').render(links=links)
    recipients = EMail.select().where(EMail.disabled == False)
    for recipient in recipients:
        click.echo("[+] Sending email to {}...".format(recipient.address))
        msg = Message(recipients=recipient.address)
        msg.subject = current_app.config['MAIL_TITLE']
        msg.body = text
        msg.html = html
        current_app.extensions['mail'].send(msg)
    click.echo("[+] Archiving links...")
    for link in links:
        link.archived = True
        link.save()
    click.echo("[+] Done")


if __name__ == '__main__':
    cli()
