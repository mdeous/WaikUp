#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read().strip()
DEPENDENCIES = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).readlines()

setup(
    name='waikup',
    version='0.1',
    description='Collaborative news sharing platform.',
    long_description=README,
    author='Mathieu D. (MatToufoutu)',
    packages=['waikup'],
    include_package_data=True,
    zip_safe=False,
    install_requires=DEPENDENCIES,
    entry_points={
        'console_scripts': ['waikup_manage = waikup.utils.manage:main']
    }
)
