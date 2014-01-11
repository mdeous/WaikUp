#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read().strip()
DEPENDENCIES = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).readlines()

setup(
    name='waikup',
    version='0.1',
    description='Collaborative news sharing platform.',
    long_description=README,
    author='Mathieu D. (MatToufoutu)',
    packages=[
        'waikup',
        'waikup.lib',
        'waikup.utils',
        'waikup.lib',
        'waikup.views',
        'waikup.views.api'
    ],
    package_data={
        'waikup': [
            'static/css/*',
            'static/fonts/*',
            'static/js/*',
            'templates/*.html',
            'templates/auth/*.html',
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
