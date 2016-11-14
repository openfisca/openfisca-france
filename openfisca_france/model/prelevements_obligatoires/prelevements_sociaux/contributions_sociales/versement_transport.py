# -*- coding: utf-8 -*-

import json


from numpy import logical_or as or_, fromiter

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR

class taux_versement_transport(Variable):
    column = FloatCol
    entity = Individu
    label = u""

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        depcom_entreprise = simulation.calculate('depcom_entreprise', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        seuil_effectif = simulation.legislation_at(period.start).cotsoc.versement_transport.seuil_effectif

        preload_taux_versement_transport()
        public = (categorie_salarie >= 2)
        taux_versement_transport = fromiter(
            (
                get_taux_versement_transport(code_commune, period)
                for code_commune in depcom_entreprise
                ),
            dtype = 'float',
            )
        # "L'entreprise emploie-t-elle plus de 9 ou 10 salariés dans le périmètre de l'Autorité organisatrice de transport
        # (AOT) suivante ou syndicat mixte de transport (SMT)"
        return period, taux_versement_transport * or_(effectif_entreprise >= seuil_effectif, public) / 100


class versement_transport(Variable):
    column = FloatCol
    entity = Individu
    label = u"Versement transport"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)
        cotisation = - taux_versement_transport * assiette_cotisations_sociales
        return period, cotisation



# File loading and parsing -> global table_versement_transport

def preload_taux_versement_transport():
    if not 'table_versement_transport' in globals():
        global table_versement_transport
        with open(COUNTRY_DIR + '/assets/versement_transport/taux.json') as data_file:
            table_versement_transport = json.load(data_file)


def get_taux_versement_transport(code_commune, period):
    instant = period.start
    taux_commune = table_versement_transport.get(code_commune, None)
    if taux_commune is None:
        return 0.0 + 0.0
    else:
        aot = taux_commune.get('aot', None)
        smt = taux_commune.get('smt', None)
        return select_temporal_taux_versement_transport(aot, instant) + select_temporal_taux_versement_transport(smt, instant)


def select_temporal_taux_versement_transport(rates, instant):

        if rates is None:
            return 0.0

        taux = rates.get('taux')
        for date in sorted(taux, reverse=True):
            if str(instant) >= date:
                return float(taux[date])
        return 0.0


