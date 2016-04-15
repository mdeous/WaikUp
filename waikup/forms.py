# -*- coding: utf-8 -*-

from flask import flash
from flask.ext.wtf import Form
from wtforms import TextAreaField, PasswordField, SelectField, StringField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, required, optional, equal_to, ValidationError

from waikup import settings
from waikup.models import Category


def is_category(form, field):
    categories = [c.name for c in Category.select()]
    if field.data not in categories:
        raise ValidationError("Not a valid category")


def flash_form_errors(form):
    for field_name, field_errors in form.errors.iteritems():
        for field_error in field_errors:
            flash("%s (field: %s)" % (field_error, field_name), category='danger')


class FormWithCategory(Form):
    category = SelectField(
        'Category',
        validators=[optional(), is_category],
        default=settings.DEFAULT_CATEGORY
    )

    def set_category_choices(self):
        self.category.choices = [(c.name, c.name) for c in Category.select()]


class SimpleLinkForm(Form):
    link_id = IntegerField(validators=[required()])


class NewLinkForm(FormWithCategory):
    name = 'new-link'
    endpoint = 'main.new_link'
    url = URLField(
        'URL',
        validators=[url(), required()]
    )
    title = StringField(
        'Title',
        validators=[required()]
    )
    description = TextAreaField(
        'Description',
        validators=[required()]
    )



class ChangePasswordForm(Form):
    name = 'chpasswd'
    endpoint = 'main.change_password'
    current = PasswordField(
        'Current password',
        validators=[required()]
    )
    new = PasswordField(
        'New password',
        validators=[required()]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[required(), equal_to('new', message="Passwords don't match")]
    )


class EditLinkForm(FormWithCategory):
    name = 'edit-link'
    endpoint = 'main.edit_link'
    url = URLField(
        'URL',
        validators=[url(), required()]
    )
    title = StringField(
        'Title',
        validators=[required()]
    )
    description = TextAreaField(
        'Description',
        validators=[required()]
    )
