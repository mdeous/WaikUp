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

try:
    from prod_settings import *
except ImportError:
    pass
