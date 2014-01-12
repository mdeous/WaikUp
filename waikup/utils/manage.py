#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from flask.ext.mail import Message
from flask.ext.script import Manager

from waikup.app import app, db, mail
from waikup.models import User, Token, Link

manager = Manager(app)


@manager.command
def setupdb():
    """Creates the database schema."""
    for table in (User, Token, Link):
        print "[+] Creating table: %s" % table._meta.name
        table.create_table(fail_silently=True)
    print "[+] Done"


@manager.command
def resetdb():
    """Resets database content."""
    for table in (Token, Link, User):
        print "[+] Resetting table content: %s" % table._meta.name
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
    def generate_txt(link_objects):
        links_txt = ""
        email_txt = app.config['MAIL_REPLY_TO']
        for link_obj in link_objects:
            links_subtxt = '* %(title)s - %(link)s\n'
            links_subtxt += '    %(description)s\n'
            links_txt += links_subtxt
            links_txt = links_txt % {
                'title': link_obj.title,
                'link': link_obj.url,
                'description': link_obj.description
            }
        full_txt = app.config['MAIL_BODY_TEMPLATE'] % {'links_list': links_txt, 'reply_to': email_txt}
        return full_txt

    def generate_html(link_objects):
        links_html = "<br><ul>"
        email_html = '<a href="mailto:%(address)s">%(address)s</a>' % {'address': app.config['MAIL_REPLY_TO']}
        for link_obj in link_objects:
            link_subhtml = '<li>%(title)s - <a href="%(link)s">%(link)s</a></li>'
            link_subhtml += '<ul><li>%(description)s</li></ul>'
            link_subhtml = link_subhtml % {
                'title': link_obj.title,
                'link': link_obj.url,
                'description': link_obj.description
            }
            links_html += link_subhtml
        links_html += '</ul>'
        full_html = app.config['MAIL_BODY_TEMPLATE'] % {'links_list': links_html, 'reply_to': email_html}
        return full_html

    links = Link.select().where(Link.archived == False)
    print "[+] Formatting TXT and HTML email templates"
    msg = Message(recipients=app.config['MAIL_RECIPIENTS'])
    msg.subject = app.config['MAIL_TITLE']
    msg.body = generate_txt(links)
    msg.html = generate_html(links)
    print "[+] Sending email"
    mail.send(msg)
    print "[+] Archiving links"
    for link in links:
        link.archived = True
        link.save()
    print "[+] Done"


def main():
    manager.run()


if __name__ == '__main__':
    main()
