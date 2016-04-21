# -*- coding: utf-8 -*-

import sys
from math import ceil


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


def load_class(cls):
    path, klass = cls.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)
