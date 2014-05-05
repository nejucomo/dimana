#! /usr/bin/env python

VERSION = '0.1a0'

from setuptools import setup

setup(name='dimana',
      description='Dimensional Analysis - arithmetic with measurement units.',
      author='Nathan Wilcox',
      author_email='nejucomo@gmail.com',
      version=VERSION,
      url='https://github.org/nejucomo/dimana',
      license='TGPPLv1.0',
      py_modules=['dimana'],
      test_suite='test_dimana',
      )
