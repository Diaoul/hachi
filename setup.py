#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='hachi',
    version='0.1',
    license=open('LICENSE').read(),
    description='XBee API',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    keywords='xbee api zigbee',
    url='https://github.com/Diaoul/hachi',
    author='Antoine Bertin',
    author_email='diaoulael@gmail.com',
    packages=find_packages(),
    classifiers=['Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite='hachi.tests.suite')
