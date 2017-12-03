# -*- coding: utf-8 -*-
import os

#
# Application
#
DEBUG = False
REVERSE_PROXIED = False

#
# Security
#
SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGEME')
SECURITY_URL_PREFIX = '/user'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'CHANGEME')
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Auth'
SECURITY_RECOVERABLE = True

#
# Database
#
DATABASE = {
    'name': os.getenv('DATABASE_NAME', 'waikup'),
    'user': os.getenv('DATABASE_USER', 'waikup'),
    'password': os.getenv('DATABASE_PASSWORD', 'waikup'),
    'host': os.getenv('DATABASE_HOST', '127.0.0.1'),
    'port': int(os.getenv('DATABASE_PORT', 5432)),
    'engine': 'waikup.lib.models.AutoRetryPostgresql'
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
MAIL_SERVER = os.getenv('MAIL_SERVER', '127.0.0.1')
MAIL_PORT = int(os.getenv('MAIL_PORT', 25))
MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', False))
MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', False))
MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'username')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'password')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'waikup@example.com')
MAIL_TITLE = '[WaikUp] Latest selected links'
MAIL_RECIPIENTS = []

del os
try:
    from prod_settings import *
except ImportError:
    pass
