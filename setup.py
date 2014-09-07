#!/usr/bin/env python
from distutils.core import setup

setup(
    name='IDNcheck',
    version='0.1.0',
    author='AJ Bowen',
    author_email='aj@gandi.net',
    packages=['idncheck', 'idncheck.tests'],
    scripts=['bin/nothing.py','bin/more_nothing.py'],
    url='http://example.com/',
    license='LICENSE.txt',
    description='Returns IDN restriction level of a string.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Nothing >= 1.1.1",
        "somepackage == 0.1.4",
    ],
)

