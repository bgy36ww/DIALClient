#!/usr/bin/env python

"""" This uses setuptools to build a package

Modeled after https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='dialclient',
  version='0.0.1',
  description='python DIAL protocol library',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Wei Wang',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.6',
  ],
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  install_requires=['', 'requests', 'untangle', 'lxml'],
  include_package_data=True,
)
