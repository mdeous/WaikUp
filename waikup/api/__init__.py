# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

from flask import request, abort
from peewee import DoesNotExist

from waikup.lib.errors import ApiError


class Resource(object):
    name = ''
    fields = ()
    fk_map = {}

    def __init__(self, obj):
        self.obj = obj

    @property
    def dict(self):
        result = {}
        for field in self.fields:
            value = getattr(self.obj, field)
            if field in self.fk_map:
                value = getattr(value, self.fk_map[field])
            result[field] = value
        return result

    @property
    def data(self):
        return {"success": True, self.name: self.dict}


class ResourceSet(object):
    def __init__(self, resource_cls, objs):
        self.name = resource_cls.name + 's'
        self.resources = []
        for obj in objs:
            self.resources.append(resource_cls(obj))

    @property
    def data(self):
        result = {"success": True, self.name: []}
        for resource in self.resources:
            result[self.name].append(resource.dict)
        return result


class login_required(object):
    def __init__(self, admin=False):
        self.admin = admin

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Auth')
            check_token_header(token)
            if self.admin:
                if not token.user.admin:
                    abort(403)
            return func(*args, **kwargs)
        return wrapper


def check_token_header(token):
    from waikup.models import Token
    token = request.headers.get('Auth')
    if token is None:
        abort(403)
    try:
        token = Token.get(Token.token == token)
    except DoesNotExist:
        abort(403)
    if token.expiry < datetime.now():
        token.delete_instance()
        abort(403)
    return token


def owner_required(func, obj_type):
    @wraps(func)
    def wrapper(objid):
        from waikup.models import Link
        token = request.headers.get('Auth')
        token = check_token_header(token)
        link = Link.get(Link.id == objid)
        if (link.author != token.user) or (not token.user.admin):
            abort(403)
        return func(objid)
    return wrapper
