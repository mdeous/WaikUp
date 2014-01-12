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
ATOM_LINKS_COUNT = 50
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = 'sender@example.com'
MAIL_REPLY_TO = 'sender@example.com'
MAIL_TITLE = "Veille - en vrac"
MAIL_BODY_TEMPLATE = u"""
Bonjour,

Voici les liens sélectionnés par les consultants durant la semaine dernière:

%(links_list)s

Bonne lecture!

Veuillez contacter %(reply_to)s en cas de besoin.

"""
MAIL_RECIPIENTS = []


try:
    from prod_settings import *
except ImportError:
    pass
