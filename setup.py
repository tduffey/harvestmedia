# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
      name='harvestmedia',
      version='0.2',
      packages=find_packages('.'),
      author='Ryan Roemmich',
      author_email='ryan@roemmich.org',
      url='https://github.com/ralfonso/harvestmedia',
      description='An interface for the Harvest Media API (http://www.harvestmedia.net/)',
      install_requires=['httplib2', 'pytz', 'iso8601', ],
      keywords='Harvest HarvestMedia API Media Music',
)
