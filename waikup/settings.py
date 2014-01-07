# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = "PLEASE CHANGE ME"
DB_STRING = "dbname=waikup user=waikup password=waikup"
HASH_METHOD = 'pbkdf2:sha256:2000'
HASH_SALT_LEN = 16
DATABASE = {
    "name": "waikup",
    "user": "waikup",
    "password": "waikup",
    "engine": "peewee.PostgresqlDatabase"
}
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True

try:
    from prod_settings import *
except ImportError:
    pass
