#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import click
from flask import current_app
from flask.cli import FlaskGroup
from flask_mail import Message
from jinja2 import Environment, PackageLoader
from peewee import IntegrityError

from waikup import settings
from waikup.lib.factory import create_app
from waikup.lib.models import Category, EMail, Link, User, db

# TODO: add user management commands (list, edit, delete)
# TODO: allow user management commands to take input from stdin
# TODO: implement database migration

TABLES = db.Model.__subclasses__()


@click.group(cls=FlaskGroup, create_app=lambda _: create_app(settings))
def cli():
    click.echo(click.style('\n[ WaikUp Management Tool ]\n', bold=True, fg='yellow'))


@cli.command()
def setupdb():
    """
    Creates the database schema.
    :return: None
    """
    click.echo(click.style('Setting up database:', fg='green'))
    for table in TABLES:
        click.echo(click.style('* creating table: {}'.format(table._meta.name), fg='blue'))
        table.create_table(fail_silently=True)
    for cat in current_app.config['DEFAULT_CATEGORIES']:
        if Category.select().where(Category.name == cat).count() == 0:
            click.echo(click.style('* creating category: {}'.format(cat), fg='blue'))
            Category.create(name=cat)


@cli.command()
def resetdb():
    """
    Resets database content.
    :return: None
    """
    click.echo(click.style('Resetting database:', fg='green'))
    for table in TABLES:
        click.echo(click.style('* deleting table: {}...'.format(table._meta.name), fg='blue'))
        table.delete().execute()
        db.database.execute_sql(*db.database.compiler().drop_table(table, cascade=True))
    setupdb()


@cli.command()
@click.option('--admin', default=False, is_flag=True)
@click.option(
    '--firstname',
    prompt=(click.style('Creating new user:', fg='green') + '\n' +
            click.style('* first name: ', fg='blue'))
)
@click.option('--lastname', prompt=click.style('* last name: ', fg='blue'))
@click.option('--email', prompt=click.style('* email address: ', fg='blue'))
@click.option(
    '--password',
    prompt=click.style('* password: ', fg='blue'),
    confirmation_prompt=True,
    hide_input=True
)
def adduser(admin, firstname, lastname, email, password):
    """
    Adds a new user.
    :return: None
    """
    try:
        current_app.extensions['security'].datastore.create_user(
            first_name=firstname,
            last_name=lastname,
            email=email,
            admin=admin,
            password=password
        )
    except IntegrityError:
        click.echo(click.style('ERROR: user already exists', bold=True, fg='red'))


@cli.command()
@click.argument('email')
@click.option(
    '--password',
    prompt=click.style('* new password: ', fg='blue'),
    confirmation_prompt=True,
    hide_input=True
)
def chpasswd(email, password):
    """
    Change given user's password.
    :return: None
    """
    click.echo(click.style("Changing {}'s password:".format(email), fg='green'))
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        click.echo(click.style('ERROR: unknown user'.format(email), bold=True, fg='red'))
        sys.exit(1)
    user.set_password(password)
    user.save()


@cli.command()
def sendmail():
    """
    Sends an email containing last submitted links.
    :return: None
    """
    click.echo(click.style('Sending new links list by e-mail:', fg='green'))
    links = Link.select().where(Link.archived == False)
    if not links:
        click.echo(click.style('* no new links', fg='blue'))
        return
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja2').render(links=links)
    text = env.get_template('text.jinja2').render(links=links)
    recipients = EMail.select().where(EMail.disabled == False)
    for recipient in recipients:
        click.echo(click.style('* sending email to {}'.format(recipient.address), fg='blue'))
        msg = Message(recipients=recipient.address)
        msg.subject = current_app.config['MAIL_TITLE']
        msg.body = text
        msg.html = html
        current_app.extensions['mail'].send(msg)
    for link in links:
        click.echo(click.style('* archiving link #{}'.format(link.id), fg='blue'))
        link.archived = True
        link.save()


if __name__ == '__main__':
    cli()
