# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from functools import wraps
from hashlib import md5

from flask import url_for, redirect, request, abort
from flask.ext.peewee.admin import ModelAdmin
from flask.ext.peewee.auth import Auth
from flask.ext.peewee.utils import get_next
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

from waikup import settings
from waikup.lib import globals as g
from waikup.lib.errors import ApiError


## MODELS


class ApiModel(g.db.Model):
    safe_fields = ()
    id = PrimaryKeyField()
    no_item_code = 404
    no_item_message = "Item does not exist"

    def safe_update(self, data):
        for field in self.safe_fields:
            if (field in data) and (data[field] is not None):
                setattr(self, field, data[field])
        try:
            result = self.save()
        except IntegrityError:
            raise ApiError("Item values overlap with an existing one")
        return result

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = super(ApiModel, cls).get(*args, **kwargs)
        except DoesNotExist:
            raise ApiError(cls.no_item_message, status_code=cls.no_item_code)
        return obj

    @classmethod
    def create(cls, *args, **kwargs):
        try:
            result = super(ApiModel, cls).create(*args, **kwargs)
        except IntegrityError:
            raise ApiError("Item already exists")
        return result

    @classmethod
    def safe_delete(cls, *args, **kwargs):
        try:
            delete_query = cls.delete().where(*args, **kwargs)
            result = delete_query.execute()
        except DoesNotExist:
            raise ApiError(cls.no_item_message, status_code=cls.no_item_code)
        return result


class User(ApiModel):
    safe_fields = (
        'first_name',
        'last_name',
        'email'
    )
    no_item_message = "User does not exist"
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    email = CharField()
    admin = BooleanField(default=False)
    active = BooleanField(default=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @classmethod
    def from_token(cls, token):
        token_obj = Token.get(Token.token == token)
        return token_obj.user

    def set_password(self, password):
        self.password = generate_password_hash(password, settings.HASH_METHOD, settings.HASH_SALT_LEN)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self):
        self.delete_token()
        return Token.create(user=self)

    def delete_token(self):
        delete_query = Token.delete().where(Token.user == self)
        return delete_query.execute()


class Token(ApiModel):
    no_item_code = 403
    no_item_message = "Forbidden"
    token = CharField(default=lambda: md5(os.urandom(128)).hexdigest())
    user = ForeignKeyField(User, related_name='tokens', unique=True)
    expiry = DateTimeField(default=lambda: datetime.now()+timedelta(weeks=1))

    def __unicode__(self):
        return u'%s' % self.token


class Link(ApiModel):
    class Meta(object):
        order_by = ('submitted',)

    safe_fields = (
        'url',
        'title',
        'description',
        'archived'
    )
    url = CharField(unique=True)
    title = CharField()
    description = TextField(null=True)
    submitted = DateTimeField(default=datetime.now)
    archived = BooleanField(default=False)
    author = ForeignKeyField(User, related_name='links')

    def __unicode__(self):
        return u'%s' % self.url

    @classmethod
    def toggle_archiving(cls, linkid):
        links = list(cls.select().where(cls.id == linkid))
        if not links:
            return False
        link = links[0]
        link.archived = not link.archived
        link.save()
        return True


class MailingProfile(ApiModel):
    name = CharField(unique=True)
    sender = CharField()
    reply_to = CharField()
    title = CharField()
    html_template = CharField()
    text_template = CharField()


class MailingAddress(ApiModel):
    address = CharField(unique=True)


class ProfileAddress(ApiModel):
    profile = ForeignKeyField(MailingProfile)
    address = ForeignKeyField(MailingAddress)


## ADMIN PANEL MODELS


class UserAdmin(ModelAdmin):
    columns = ('username', 'first_name', 'last_name', 'email')


class TokenAdmin(ModelAdmin):
    columns = ('token', 'user')
    foreign_key_lookups = {'user': 'username'}


class LinkAdmin(ModelAdmin):
    columns = ('url', 'title', 'author')
    foreign_key_lookups = {'author': 'username'}


## AUTHENTICATION SYSTEM


class HybridAuth(Auth):
    @staticmethod
    def check_token_header():
        token_str = request.headers.get('Auth')
        if token_str is None:
            abort(403)
        try:
            token = Token.get(Token.token == token_str)
            if token.expiry < datetime.now():
                token.delete_instance()
                abort(403)
            return token
        except DoesNotExist:
            abort(403)

    def owner_required(self, func):
        @wraps(func)
        def wrapper(linkid):
            token = self.check_token_header()
            link = Link.get(Link.id == linkid)
            if (link.author != token.user) or (not token.user.admin):
                abort(403)
            return func(linkid)
        return wrapper

    def get_user_model(self):
        return User

    def get_model_admin(self, model_admin=None):
        return UserAdmin

    def test_user(self, test_func):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                if request.blueprint in ('links', 'users'):
                    token = self.check_token_header()
                    if not test_func(token.user):
                        abort(403)
                else:
                    user = self.get_logged_in_user()
                    if not user or not test_func(user):
                        login_url = url_for('%s.login' % self.blueprint.name, next=get_next())
                        return redirect(login_url)
                return func(*args, **kwargs)
            return inner
        return decorator
