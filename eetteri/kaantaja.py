# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, function-redefined

from django.core.exceptions import FieldError
from django.db.models.aggregates import Count
from django.db.models.expressions import Col
from django.db.models.lookups import Exact
from django.db.models.sql.compiler import (
  SQLCompiler, SQLInsertCompiler, SQLUpdateCompiler, SQLDeleteCompiler,
)
from django.db.models.sql.constants import MULTI
from django.db.models.sql.datastructures import Join
from django.db.utils import DatabaseError, IntegrityError


class Kysely:

  def __init__(self, compiler):
    self.compiler = compiler
    self.connection = compiler.connection
    self.ops = compiler.connection.ops
    self.query = compiler.query  # sql.Query

    # Laadi luettelo mallin periyttämiseen liittyvistä JOIN-ehdoista.
    # Tällaiset liitostaulut sallitaan.
    def periytysketju():
      curr_opts = self.query.get_meta()
      for int_model, field in curr_opts.parents.items():
        yield field
        curr_opts = int_model._meta
    periytysketju = list(periytysketju())
    if any(
      True
      for alias, taulu in self.query.alias_map.items()
      if isinstance(taulu, Join) and taulu.join_field not in periytysketju
    ):
      pass #raise DatabaseError('JOIN-ehtoa ei voida toteuttaa.')
    if self.query.distinct:
      raise DatabaseError('DISTINCT-ehtoa ei voida toteuttaa.')
    if self.query.extra:
      raise DatabaseError('.extra()-lauseketta ei voida toteuttaa.')
    if getattr(self.query, 'having', False):
      raise DatabaseError('HAVING-ehtoa ei voida toteuttaa.')


    expressions, klass_info, annotations = self.compiler.get_select()
    def _kentat():
      # pylint: disable=unused-variable
      for kentta_ix in klass_info['select_fields']:
        yield expressions[kentta_ix][0].target
    self.fields = list(_kentat()) if klass_info else ['*']

    self.tyyppi = next((tyyppi for kaantaja, tyyppi in {
      SQLInsertCompiler: 'INSERT',
      SQLUpdateCompiler: 'UPDATE',
      SQLDeleteCompiler: 'DELETE',
    }.items() if isinstance(self.compiler, kaantaja)), 'SELECT')
    self.polku = '/'.join(self.query.model._meta.db_table.split('_') + [''])

    # def __init__

  # class Kysely


class SQLCompiler(SQLCompiler):

  def as_sql(self):
    self.pre_sql_setup()
    kysely = Kysely(self)
    try:
      ehto, = self.query.where.get_source_expressions()
      assert isinstance(ehto, Exact)
      assert isinstance(ehto.lhs, Col)
      assert ehto.lhs.field == self.query.get_meta().pk
      assert ehto.rhs_is_direct_value()
    except (ValueError, AssertionError):
      pass
    else:
      kysely.pk = ehto.rhs
    return kysely, ()
    # def as_sql

  # class SQLCompiler


class SQLInsertCompiler(SQLCompiler, SQLInsertCompiler):

  def as_sql(self):
    kysely, p = super().as_sql()
    kysely.data = rivit = []
    for obj in self.query.objs:
      rivi = {}
      rivit.append(rivi)
      for field in self.query.fields:
        value = field.get_db_prep_save(
          getattr(obj, field.attname)
          if self.query.raw
          else field.pre_save(obj, obj._state.adding),
          connection=self.connection
        )
        if not field.null and value is None and not field.primary_key:
          raise IntegrityError("You can't set %s (a non-nullable "
                     "field) to None!" % field.name)

        # Prepare value for database, note that query.values have
        # already passed through get_db_prep_save.
        value = self.connection.ops.value_for_db(value, field)
        rivi[field.attname] = value
        # for field in self.query.fields
    return [(kysely, p), ]
    # def as_sql

  # class SQLInsertCompiler


class SQLUpdateCompiler(SQLCompiler, SQLUpdateCompiler):

  def as_sql(self):
    kysely, p = super().as_sql()
    if not self.query.values:
      return None, ()
    kysely.data = {}

    qn = self.quote_name_unless_alias
    values, update_params = [], []
    for field, model, val in self.query.values:
      if hasattr(val, 'resolve_expression'):
        val = val.resolve_expression(
          self.query, allow_joins=False, for_save=True
        )
        if val.contains_aggregate:
          raise FieldError(
            'Aggregate functions are not allowed in this query '
            '(%s=%r).' % (field.name, val)
          )
        if val.contains_over_clause:
          raise FieldError(
            'Window expressions are not allowed in this query '
            '(%s=%r).' % (field.name, val)
          )
      elif hasattr(val, 'prepare_database_save'):
        if field.remote_field:
          val = field.get_db_prep_save(
            val.prepare_database_save(field),
            connection=self.connection,
          )
        else:
          raise TypeError(
            "Tried to update field %s with a model instance, %r. "
            "Use a value compatible with %s."
            % (field, val, field.__class__.__name__)
          )
      else:
        val = field.get_db_prep_save(val, connection=self.connection)

      if hasattr(val, 'as_sql'):
        raise FieldError
      kysely.data[field.column] = val

    return kysely, p
    # def as_sql

  # class SQLUpdateCompiler


class SQLDeleteCompiler(SQLCompiler, SQLDeleteCompiler):
  pass
