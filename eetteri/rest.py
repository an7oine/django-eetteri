# -*- coding: utf-8 -*-

import functools

from django.utils.functional import cached_property
import requests

from .yhteys import Yhteys


class RestYhteys(Yhteys):

  class Yhteysvirhe(Yhteys.InterfaceError): pass
  class Palvelinvirhe(Yhteys.InternalError): pass
  class Pyyntovirhe(Yhteys.ProgrammingError): pass
  class Sanomavirhe(Yhteys.OperationalError): pass
  class Sivutusvirhe(Yhteys.OperationalError): pass
  class Tunnistautumisvirhe(Yhteys.InterfaceError): pass
  class PuuttuvaRajapintavirhe(Yhteys.ProgrammingError): pass

  tunnistautuminen = 'Authorization'

  def __init__(self, kanta, *, PALVELIN, POLKU, AVAIN, **kwargs):
    super().__init__(kanta)
    self.api = f'{PALVELIN}{POLKU}'
    self.avain = AVAIN
    # def __init__

  @cached_property
  def _tunnistautuminen(self):
    if self.avain is not None:
      # REST-tunniste.
      return {self.tunnistautuminen: f'Token {self.avain}'}
    else:
      # Ei tunnistustietoja.
      return {}
    # def _tunnistautuminen

  @property
  def pyynnon_otsakkeet(self):
    return {
      **self._tunnistautuminen,
      'Content-Type': 'application/json',
    }
    # def pyynnon_otsakkeet

  # HTTP-virheiden nojalla nostettavat poikkeukset.
  virhe = {
    503: (Yhteysvirhe, 'Palvelin tilapäisesti poissa käytöstä'),
    500: (Yhteysvirhe, 'Järjestelmävirhe palvelimella'),
    429: (Yhteysvirhe, 'Liikaa samanaikaisia pyyntöjä'),
    404: (PuuttuvaRajapintavirhe, 'Rajapintaa ei löydy'),
    403: (Yhteysvirhe, 'Tarvittava käyttöoikeus puuttuu'),
    401: (Tunnistautumisvirhe, 'Tunnistautuminen epäonnistui'),
    400: (Pyyntovirhe, 'Pyynnön sisältö on virheellinen'),
  }

  # Luodaan `_get`-, `_post`- jne. metodit:
  # kutsutaan vastaavaa requests-funktiota kohdistuen `self.apiin`.
  def __pyynto(nimi):
    # pylint: disable=no-self-argument, no-member
    def _pyynto(self, polku, *args, lisaa_api=True, **kwargs):
      try:
        with getattr(requests, nimi)(
          self.api + polku if lisaa_api else polku,
          *args,
          headers=self.pyynnon_otsakkeet,
          stream=True,
          **kwargs
        ) as sanoma:
          if sanoma.status_code >= 400:
            poikkeus, viesti = self.virhe.get(
              sanoma.status_code, (self.Palvelinvirhe, 'Tuntematon virhe')
            )
            raise poikkeus(viesti + f': {nimi.upper()} {polku}')
          try:
            return sanoma.json()
          except ValueError:
            raise self.Sanomavirhe('Virheellinen paluusanoman muoto')
          # with getattr
      except IOError:
        raise self.Yhteysvirhe('Yhteyden muodostus epäonnistui')
      # def _pyynto
    _pyynto.__name__ = f'_{nimi}'
    return _pyynto
    # def __pyynto
  _get = __pyynto('get')
  _put = __pyynto('put')
  _post = __pyynto('post')
  _patch = __pyynto('patch')
  _delete = __pyynto('delete')
  del __pyynto

  def _sivutettu_get(self, polku, *args, **kwargs):
    polku = self.api + polku
    while True:
      sanoma = self._get(polku, *args, lisaa_api=False, **kwargs)
      if not 'results' in sanoma:
        raise self.Sivutusvirhe(sanoma)
      yield from sanoma['results']
      if not sanoma.get('next'):
        break
      polku = sanoma['next']
      # while True
    # def _sivutettu_get

  def select(self, kysely):
    polku = kysely.polku
    kentat = [kentta.attname for kentta in kysely.fields]
    if getattr(kysely, 'pk', None):
      try:
        yield list(map(self._get(
          polku + f'{kysely.pk}/', params={'kentta': kentat}
        ).get, kentat))
      except (self.PuuttuvaRajapintavirhe, StopIteration):
        pass
    else:
      for tulos in self._sivutettu_get(polku, params={'kentta': kentat}):
        yield list(map(tulos.get, kentat))
    # def select

  def select_count(self, kysely):
    return self._get(kysely.polku)['count']
    # def select_count

  def insert(self, kysely):
    sanoma = self._post(kysely.polku, json=kysely.data)
    if isinstance(sanoma, list):
      # Poimi viimeinen mahdollisista useista, lisätyistä riveistä.
      sanoma = sanoma[-1]
    # Poimi primääriavain.
    return sanoma.get(kysely.query.get_meta().pk.attname)
    # def insert

  def update(self, kysely):
    if getattr(kysely, 'pk', None):
      try:
        self._patch(kysely.polku + f'{kysely.pk}/', json=kysely.data)
      except self.PuuttuvaRajapintavirhe:
        return 0
      else:
        return 1
    else:
      lkm = self.select_count(kysely)
      self._patch(kysely.polku, json=kysely.data)
      return lkm
    # def update

  def delete(self, kysely):
    self._delete(kysely.polku + f'{kysely.pk}/')

  # class RestYhteys
