# -*- coding: utf-8 -*-

DEBUG = True
REVERSE_PROXIED = False

#
# Security
#
SECRET_KEY = "PLEASE CHANGE ME"
SECURITY_URL_PREFIX = '/user'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'PLEASE CHANGE ME'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Auth'
SECURITY_RECOVERABLE = True

#
# Database
#
DATABASE = {
    "name": "waikup",
    "user": "waikup",
    "password": "waikup",
    "engine": "peewee.PostgresqlDatabase"
}
DEFAULT_CATEGORIES = [
    'System',
    'Security',
    'Networking',
    'Development',
    'Tools',
    'News',
    'Fun',
    'Other'
]
DEFAULT_CATEGORY = 'Other'

#
# User interfaces (Web UI / API)
#
BUNDLE_ERRORS = True
ITEMS_PER_PAGE = 10
ATOM_LINKS_COUNT = 50
DATETIME_FORMAT = '%b %d %Y at %H:%M:%S'

#
# E-mails
#
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = 'sender@example.com'
MAIL_TITLE = "[WaikUp] Latest selected links"

try:
    from prod_settings import *
except ImportError:
    pass
