# -*- coding: utf-8 -*-

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.validation import BaseDatabaseValidation

from .ominaisuudet import DatabaseFeatures
from .muunnokset import DatabaseOperations
from .yhteys import Yhteys


class DatabaseWrapper(BaseDatabaseWrapper):
  ''' Tietokantayhteys. '''

  def is_usable(self):
    return True

  client_class = BaseDatabaseClient
  creation_class = BaseDatabaseCreation
  introspection_class = BaseDatabaseIntrospection
  validation_class = BaseDatabaseValidation

  features_class = DatabaseFeatures
  ops_class = DatabaseOperations

  Database = Yhteys

  # Vrt. `django.db.backends.mysql.base.DatabaseWrapper`.
  operators = {
    'exact': '= %s',
    'iexact': 'LIKE %s',
    'contains': 'LIKE BINARY %s',
    'icontains': 'LIKE %s',
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': 'LIKE BINARY %s',
    'endswith': 'LIKE BINARY %s',
    'istartswith': 'LIKE %s',
    'iendswith': 'LIKE %s',
  }

  def get_connection_params(self):
    return self.settings_dict

  def get_new_connection(self, conn_params):
    return Yhteys(self, **conn_params)

  def init_connection_state(self):
    pass

  def _set_autocommit(self, autocommit):
    pass

  def create_cursor(self, name=None):
    return self.connection.Kursori(self.connection)

  # class DatabaseWrapper
