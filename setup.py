#!/usr/bin/env python
from distutils.core import setup

setup(
    name='IDNcheck',
    version='0.1.0',
    author='AJ Bowen',
    author_email='aj@gandi.net',
    packages=['idncheck', 'idncheck.tests'],
    license='LICENSE.txt',
    description='Returns IDN restriction level of a string.',
    long_description=open('README.md').read()
)

