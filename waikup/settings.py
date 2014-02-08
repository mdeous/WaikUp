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
DB_VERSION_FILE = '~/.waikup-db-version'
DEFAULT_CATEGORIES = [
    'Web',
    'Forensics',
    'Reverse Engineering',
    'Cryptography',
    'Networking',
    'Development',
    'Malware',
    'News',
    'Fun',
    'Other'
]
DEFAULT_CATEGORY = 'Other'
ATOM_LINKS_COUNT = 50
DATETIME_FORMAT = '%b %d %Y at %H:%M:%S'
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = 'sender@example.com'
MAIL_TITLE = "Veille - en vrac"
MAIL_RECIPIENTS = []


try:
    from prod_settings import *
except ImportError:
    pass
