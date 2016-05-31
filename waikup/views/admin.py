# -*- coding: utf-8 -*-

from flask import redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_security import current_user


class RestrictedViewMixin:
    """
    Mixin class that restricts access to admin views to admins.
    """
    def is_accessible(self):
        """
        Checks if user is allowed to access the view (i.e. is an admin).
        :return: True/False
        """
        return current_user.is_admin

    def inaccessible_callback(self, *args, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(RestrictedViewMixin, ModelView):
    """
    Base view.
    """
    create_modal = True
    edit_modal = True


class RestrictedAdminIndexView(RestrictedViewMixin, AdminIndexView):
    """
    Admin's index view.
    """
    pass


class ReadOnlyModelView(BaseModelView):
    """
    Base view for read-only models.
    """
    can_create = False
    can_edit = False


class UserModelView(ReadOnlyModelView):
    """
    User view.
    """
    column_editable_list = ['first_name', 'last_name', 'email', 'admin', 'active']
    column_exclude_list = ['password']
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_filters = ['admin', 'active']


class CategoryModelView(BaseModelView):
    """
    Category view.
    """
    column_editable_list = ['name']
    column_searchable_list = ['name']


class LinkModelView(BaseModelView):
    """
    Link view.
    """
    column_editable_list = ['url', 'title', 'category', 'archived', 'author']
    column_searchable_list = ['url', 'title', 'description']
    column_filters = ['archived']


class EMailModelView(BaseModelView):
    """
    Email view.
    """
    column_editable_list = ['address', 'disabled']
    column_searchable_list = ['address']
    column_filters = ['disabled']
