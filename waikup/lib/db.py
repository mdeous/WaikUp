# -*- coding: utf-8 -*-

from peewee import Database, Model
from playhouse.shortcuts import RetryOperationalError

from waikup.lib.helpers import load_class


class WaikupDB(object):
    def __init__(self, app):
        self.app = app
        self.db_cls = None
        self.database = None
        self.load_database()
        self.Model = self.get_model_class()
        self.database.connect()

    def load_database(self):
        db_base_cls = load_class(self.app.config['DATABASE'].pop('engine'))
        assert issubclass(db_base_cls, Database)
        self.db_cls = self.get_db_class(db_base_cls)
        self.database = self.db_cls(
            self.app.config['DATABASE'].pop('name'), **self.app.config['DATABASE']
        )

    def get_db_class(self, base_cls):
        class AutoReconnectDatabase(base_cls, RetryOperationalError):
            pass
        return AutoReconnectDatabase

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.database
        return BaseModel
