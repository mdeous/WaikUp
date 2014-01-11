# -*- coding: utf-8 -*-

import site

activate_this = '/var/www/waikup/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from waikup.app import app as application
