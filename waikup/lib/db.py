# -*- coding: utf-8 -*-

from peewee import Database, Model
from playhouse.shortcuts import RetryOperationalError

from waikup.lib.helpers import load_class


class WaikupDB(object):
    """
    Abstraction class that mimicks flask-peewee's Database class
    """
    def __init__(self, app):
        self.app = app
        self.db_cls = None
        self.database = None
        self.load_database()
        self.Model = self.get_model_class()
        self.database.connect()

    def load_database(self):
        """
        Fetches database settings and connects to it.
        :return: None
        """
        db_base_cls = load_class(self.app.config['DATABASE'].pop('engine'))
        assert issubclass(db_base_cls, Database)
        self.db_cls = self.get_db_class(db_base_cls)
        self.database = self.db_cls(
            self.app.config['DATABASE'].pop('name'), **self.app.config['DATABASE']
        )

    def get_db_class(self, base_cls):
        """
        Factory method that returns an auto-reconnecting database class.
        :param base_cls: Database subclass that should use as the base class
        :return: an auto-reconnecting Database subclass
        """
        class AutoReconnectDatabase(base_cls, RetryOperationalError):
            pass
        return AutoReconnectDatabase

    def get_model_class(self):
        """
        Factory method that returns a Model subclass bound to the current database.
        :return: the class from which models should inherit.
        """
        class BaseModel(Model):
            class Meta:
                database = self.database
        return BaseModel
