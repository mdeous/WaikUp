# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, required, optional, equal_to, ValidationError

from waikup.models import Category


def is_category(form, field):
    categories = [c.name for c in Category.select()]
    if field.data not in categories:
        raise ValidationError("Not a valid category")


class NewLinkForm(Form):
    name = 'new-link'
    endpoint = 'webui.new_link'
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
        validators=[required()]
    )
    category = SelectField(
        'Category:',
        validators=[optional(), is_category],
        default='Other'
    )

    def set_category_choices(self):
        self.category.choices = [(c.name, c.name) for c in Category.select()]


class ChangePasswordForm(Form):
    name = 'chpasswd'
    endpoint = 'webui.change_password'
    old = PasswordField(
        'Old password:',
        validators=[required()]
    )
    new = PasswordField(
        'New password:',
        validators=[required()]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[required(), equal_to('new', message="Passwords don't match")]
    )
