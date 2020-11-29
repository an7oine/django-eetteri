# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  setup_requires='git-versiointi',
  name='django-eetteri',
  description='Django-ajuri rajapinnan käyttämiseen tietokantana',
  url='https://github.com/an7oine/django-eetteri.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@me.com',
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    'Django>=3.1',
    'requests>=2.3.0',
  ],
)
