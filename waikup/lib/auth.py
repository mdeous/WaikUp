# -*- coding: utf-8 -*-

from datetime import datetime
from flask import request, abort
from functools import wraps

from peewee import DoesNotExist
from flask.ext.peewee.auth import Auth

from waikup.models import Token, User, UserAdmin


class ApiAuth(object):
    @staticmethod
    def get_token_from_header():
        token_str = request.headers.get('Auth')
        if token_str is None:
            abort(403)
        try:
            token = Token.get(Token.token == token_str)
        except DoesNotExist:
            abort(403)
        else:
            if token.expiry < datetime.now():
                token.delete_instance()
                abort(403)
            return token

    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.get_token_from_header()
            return func(*args, **kwargs)
        return wrapper


class WebAuth(Auth):
    def get_user_model(self):
        return User

    def get_model_admin(self, model_admin=None):
        return UserAdmin
