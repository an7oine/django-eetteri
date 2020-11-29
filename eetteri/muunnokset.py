# -*- coding: utf-8 -*-

import datetime
import decimal
import uuid

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.models.expressions import Col
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time


class DatabaseOperations(BaseDatabaseOperations):
  compiler_module = 'eetteri.kaantaja'

  # Abstraktit metodit.
  def date_extract_sql(self, lookup_type, field_name):
    raise NotImplementedError
  def date_interval_sql(self, timedelta):
    raise NotImplementedError
  def date_trunc_sql(self, lookup_type, field_name):
    raise NotImplementedError
  def datetime_cast_date_sql(self, field_name, tzname):
    raise NotImplementedError
  def datetime_cast_time_sql(self, field_name, tzname):
    raise NotImplementedError
  def datetime_extract_sql(self, lookup_type, field_name, tzname):
    raise NotImplementedError
  def datetime_trunc_sql(self, lookup_type, field_name, tzname):
    raise NotImplementedError
  def time_trunc_sql(self, lookup_type, field_name):
    raise NotImplementedError
  def no_limit_value(self):
    raise NotImplementedError
  def regex_lookup(self, lookup_type):
    raise NotImplementedError
  def sql_flush(
    self, style, tables, *, reset_sequences=False, allow_cascade=False
  ):
    raise NotImplementedError

  # Ohitetaan turhat heittomerkit.
  def quote_name(self, name): return name

  # Ohitetaan turhat kenoviivat `LIKE`-kyselyjen yhteydessä.
  def prep_for_like_query(self, x): return x
  def prep_for_iexact_query(self, value): return value

  def get_db_converters(self, expression):
    ''' Vrt. django.db.backends.sqlite3.operations.DatabaseOperations '''
    converters = super().get_db_converters(expression)
    internal_type = expression.output_field.get_internal_type()
    if internal_type == 'DateTimeField':
      converters.append(self.convert_datetimefield_value)
    elif internal_type == 'DateField':
      converters.append(self.convert_datefield_value)
    elif internal_type == 'TimeField':
      converters.append(self.convert_timefield_value)
    elif internal_type == 'DecimalField':
      converters.append(self.get_decimalfield_converter(expression))
    elif internal_type == 'UUIDField':
      converters.append(self.convert_uuidfield_value)
    elif internal_type in ('NullBooleanField', 'BooleanField'):
      converters.append(self.convert_booleanfield_value)
    return converters

  def convert_datetimefield_value(self, value, expression, connection):
    # pylint: disable=unused-argument
    if value is not None:
      if not isinstance(value, datetime.datetime):
        value = parse_datetime(value)
      if settings.USE_TZ and not timezone.is_aware(value):
        value = timezone.make_aware(value, self.connection.timezone)
    return value

  def convert_datefield_value(self, value, expression, connection):
    # pylint: disable=unused-argument
    if value is not None:
      if not isinstance(value, datetime.date):
        value = parse_date(value)
    return value

  def convert_timefield_value(self, value, expression, connection):
    # pylint: disable=unused-argument
    if value is not None:
      if not isinstance(value, datetime.time):
        value = parse_time(value)
    return value

  def get_decimalfield_converter(self, expression):
    # pylint: disable=unused-argument, inconsistent-return-statements
    def converter(value, expression, connection):
      if value is not None:
        return decimal.Decimal(value)
    return converter

  def convert_uuidfield_value(self, value, expression, connection):
    # pylint: disable=unused-argument
    if value is not None:
      value = uuid.UUID(value)
    return value

  def convert_booleanfield_value(self, value, expression, connection):
    # pylint: disable=unused-argument
    return bool(value) if value in (1, 0) else value

  # class DatabaseOperations
