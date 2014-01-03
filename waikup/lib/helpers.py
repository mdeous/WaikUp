# -*- coding: utf-8 -*-

from functools import wraps

from flask import request

from waikup.lib.errors import ApiError


class Singleton(type):
    def __init__(cls, name, bases, attr_dict):
        super(Singleton, cls).__init__(name, bases, attr_dict)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class required_fields(object):
    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for field in self.fields:
                if field not in request.form:
                    raise ApiError("Missing field: %s" % field)
            return func(*args, **kwargs)
        return wrapper
