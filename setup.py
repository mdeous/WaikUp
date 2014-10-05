#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
README = open(os.path.join(CURRENT_DIR, 'README.md')).read().strip()
DEPENDENCIES = open(os.path.join(CURRENT_DIR, 'requirements.txt')).readlines()
VERSION = open(os.path.join(CURRENT_DIR, 'VERSION')).read().strip()


setup(
    name='waikup',
    version=VERSION,
    description='Collaborative news sharing platform.',
    long_description=README,
    author='Mathieu D. (MatToufoutu)',
    packages=[
        'waikup',
        'waikup.lib',
        'waikup.utils',
        'waikup.utils.migrations',
        'waikup.lib',
        'waikup.views',
    ],
    package_data={
        'waikup': [
            'static/css/*',
            'static/fonts/*',
            'static/img/*',
            'static/js/*',
            'templates/*.html',
            'templates/auth/*.html',
            'templates/emails/*.jinja2',
            'templates/macros/*.html'
        ]
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=DEPENDENCIES,
    entry_points={
        'console_scripts': ['waikup_manage = waikup.utils.manage:main']
    }
)
