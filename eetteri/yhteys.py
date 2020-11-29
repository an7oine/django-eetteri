# -*- coding: utf-8 -*

import itertools


class Yhteys:

  from django.db.utils import (
    Error,
    DataError,
    DatabaseError,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
  )

  class Kursori:

    def __init__(self, yhteys):
      self.yhteys = yhteys
      # def __init__

    def close(self):
      pass


    def __enter__(self):
      return self

    def __exit__(self, *args, **kwargs):
      return False

    def execute(self, query, params):
      if query.tyyppi == 'INSERT':
        self.lastrowid = self.yhteys.insert(query)
      elif query.tyyppi == 'UPDATE':
        self.rowcount = self.yhteys.update(query)
      elif query.tyyppi == 'DELETE':
        self.yhteys.delete(query)
      elif query.query.annotation_select:
        # Hae erikseen lukumäärä.
        aggregate, = query.query.annotation_select.values()
        assert aggregate.function == 'COUNT'
        self.tulokset = iter(([self.yhteys.select_count(query)], ))
      else:
        self.tulokset = self.yhteys.select(query)
      # def execute

    def fetchone(self):
      return next(self.tulokset)

    def fetchmany(self, pituus):
      return list(itertools.islice(self.tulokset, pituus))

    def fetchall(self):
      return list(self.tulokset)

    # class Kursori

  def __new__(cls, kanta, **kwargs):
    if cls != __class__:
      return super().__new__(cls)
    # XXX valitaan toteutus parametrien mukaan.
    from .rest import RestYhteys
    return RestYhteys(kanta, **kwargs)
    # def __new__

  def __init__(self, kanta):
    self.kanta = kanta

  def select(self, kysely):
    raise NotImplementedError

  def select_count(self, kysely):
    raise NotImplementedError

  def insert(self, kysely):
    raise NotImplementedError

  def update(self, kysely):
    raise NotImplementedError

  def delete(self, kysely):
    raise NotImplementedError

  def commit(self):
    pass

  def rollback(self):
    raise self.NotSupportedError

  def close(self):
    pass

  # class Yhteys
