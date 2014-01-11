# -*- coding: utf-8 -*-

import os
import sys

waikup_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'waikup')
sys.path.insert(0, waikup_dir)

from waikup.app import app as application

