# -*- coding: utf-8 -*-

import sys
from functools import wraps
from math import ceil

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


class Paginated(object):
    def __init__(self, query, page, per_page, count):
        self.page = page
        self.per_page = per_page
        self.count = count
        self.items = query.paginate(page, per_page)

    def __iter__(self):
        for item in self.items:
            yield item

    @property
    def pages(self):
        return int(ceil(self.count / float(self.per_page)))

    @property
    def has_previous(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages


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


def load_class(cls):
    path, klass = cls.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)
