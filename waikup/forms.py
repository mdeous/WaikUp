# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, required, optional, equal_to


class NewLinkForm(Form):
    name = 'newlink'
    endpoint = 'webui.new_link'
    fields = ('url', 'title', 'description')
    url = URLField(
        'URL:',
        validators=[url(), required()]
    )
    title = TextField(
        'Title:',
        validators=[required()]
    )
    description = TextAreaField(
        'Description:',
        validators=[optional()]
    )


class ChangePasswordForm(Form):
    name = 'chpasswd'
    endpoint = 'webui.change_password'
    fields = ('old', 'new', 'confirm')
    old = PasswordField(
        'Current password:',
        validators=[required()]
    )
    new = PasswordField(
        'New password:',
        validators=[required()]
    )
    confirm = PasswordField(
        'Confirm password:',
        validators=[required(), equal_to('new', message="Passwords don't match")]
    )
