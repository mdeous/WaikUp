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
    pass


class RestrictedAdminIndexView(RestrictedViewMixin, AdminIndexView):
    pass


class ReadOnlyModelView(BaseModelView):
    can_create = False
    can_edit = False


class UserModelView(ReadOnlyModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['username', 'first_name', 'last_name', 'email']
    column_filters = ['admin', 'active']


class RoleModelView(BaseModelView):
    column_searchable_list = ['name', 'description']


class CategoryModelView(BaseModelView):
    column_searchable_list = ['name']


class LinkModelView(BaseModelView):
    column_searchable_list = ['url', 'title', 'description']
    column_filters = ['archived']
