# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextAreaField, PasswordField, SelectField, StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, required, optional, equal_to, ValidationError

from waikup import settings
from waikup.models import Category


def is_category(form, field):
    categories = [c.name for c in Category.select()]
    if field.data not in categories:
        raise ValidationError("Not a valid category")


class FormWithCategory(Form):
    def set_category_choices(self):
        self.category.choices = [(c.name, c.name) for c in Category.select()]


class NewLinkForm(FormWithCategory):
    name = 'new-link'
    endpoint = 'webui.new_link'
    url = URLField(
        'URL:',
        validators=[url(), required()]
    )
    title = StringField(
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
        default=settings.DEFAULT_CATEGORY
    )


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


class EditLinkForm(FormWithCategory):
    name = 'edit-link'
    endpoint = 'webui.edit_link'
    url = URLField(
        'URL:',
        validators=[url(), required()]
    )
    title = StringField(
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
        default=settings.DEFAULT_CATEGORY
    )
