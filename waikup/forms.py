# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, required, optional, equal_to


class NewLinkForm(Form):
    url = URLField(validators=[url(), required()])
    title = TextField(validators=[required()])
    description = TextAreaField(validators=[optional()])


class ChangePasswordForm(Form):
    old = PasswordField(validators=[required()])
    new = PasswordField(validators=[required()])
    confirm = PasswordField(validators=[required(), equal_to('new', message="Passwords don't match")])
