# -*- coding: utf-8 -*-

from flask import redirect, url_for, request
from flask.ext.admin import AdminIndexView
from flask.ext.admin.contrib.peewee import ModelView
from flask.ext.security import current_user


class RestrictedViewMixin:
    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, *args, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(RestrictedViewMixin, ModelView):
    create_modal = True
    edit_modal = True


class RestrictedAdminIndexView(RestrictedViewMixin, AdminIndexView):
    pass


class ReadOnlyModelView(BaseModelView):
    can_create = False
    can_edit = False


class UserModelView(ReadOnlyModelView):
    column_editable_list = ['first_name', 'last_name', 'email', 'admin', 'active']
    column_exclude_list = ['password']
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_filters = ['admin', 'active']


class CategoryModelView(BaseModelView):
    column_editable_list = ['name']
    column_searchable_list = ['name']


class LinkModelView(BaseModelView):
    column_editable_list = ['url', 'title', 'category', 'archived', 'author']
    column_searchable_list = ['url', 'title', 'description']
    column_filters = ['archived']


class EMailModelView(BaseModelView):
    column_editable_list = ['address', 'disabled']
    column_searchable_list = ['address']
    column_filters = ['disabled']
