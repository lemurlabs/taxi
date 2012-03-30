#!/usr/bin/env python
from distutils.core import setup
from taxi import __version__

setup(
    name='taxi',
    version=__version__,
    packages=['taxi'],
    description='Taxi is a Zebra frontend',
    author='Sylvain Fankhauser',
    author_email='sylvain.fankhauser@liip.ch',
    scripts = ['bin/taxi'],
    url='http://bitbucket.org/sephi/taxi',
)
