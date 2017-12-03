# -*- coding: utf-8 -*-

from math import ceil


class Paginated(object):
    """
    Helper class that implements pagination logic.
    """
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
        """
        Computes the amount of pages required to hold all items.
        :return: pages count
        """
        return int(ceil(self.count / float(self.per_page)))

    @property
    def has_previous(self):
        """
        Checks if there are pages before the current one.
        :return: True/False
        """
        return self.page > 1

    @property
    def has_next(self):
        """
        Checks if there are pages after the current one.
        :return: True/False
        """
        return self.page < self.pages
