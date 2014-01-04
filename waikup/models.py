# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from hashlib import md5
from flask.ext.peewee.auth import Auth

from peewee import *
from flask.ext.peewee.admin import ModelAdmin, Admin
from werkzeug.security import generate_password_hash, check_password_hash

from waikup import settings
from waikup.app import db, app


## MODELS


class BaseModel(db.Model):
    update_fields = ()
    id = PrimaryKeyField()

    def safe_update(self, data):
        for field in self.update_fields:
            if (field in data) and (data[field] is not None):
                setattr(self, field, data[field])
        return self.save()


class User(BaseModel):
    update_fields = (
        'username',
        'first_name',
        'last_name',
        'email'
    )
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


class Token(BaseModel):
    token = CharField(default=lambda: md5(os.urandom(128)).hexdigest())
    user = ForeignKeyField(User, related_name='tokens', unique=True)
    expiry = DateTimeField(default=lambda: datetime.now()+timedelta(weeks=1))

    def __unicode__(self):
        return u'%s' % self.token


class Link(BaseModel):
    update_fields = (
        'url',
        'title',
        'description'
    )
    url = CharField(unique=True)
    title = CharField()
    description = TextField(null=True)
    submitted = DateTimeField(default=datetime.now)
    author = ForeignKeyField(User, related_name='links')

    def __unicode__(self):
        return u'%s' % self.url


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


class CustomAuth(Auth):
    def get_user_model(self):
        return User

    def get_model_admin(self, model_admin=None):
        return UserAdmin


class CustomAdmin(Admin):
    def check_user_permission(self, user):
        return user.admin


auth = CustomAuth(app, db)
admin = CustomAdmin(app, auth)
admin.register(User, UserAdmin)
admin.register(Token, TokenAdmin)
admin.register(Link, LinkAdmin)
admin.setup()
