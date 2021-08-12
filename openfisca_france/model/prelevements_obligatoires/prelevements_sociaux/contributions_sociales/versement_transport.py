import json


from numpy import logical_or as or_, fromiter

from openfisca_france.model.base import *
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR


class taux_versement_transport(Variable):
    value_type = float
    entity = Individu
    label = ""
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        depcom_entreprise = individu('depcom_entreprise', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        categorie_salarie = individu('categorie_salarie', period)

        seuil_effectif = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.versement_transport.bareme.seuil_effectif

        preload_taux_versement_transport()
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            + (categorie_salarie == TypesCategorieSalarie.non_pertinent)
            )
        taux_versement_transport = fromiter(
            (
                get_taux_versement_transport(code_commune, period)
                for code_commune in depcom_entreprise
                ),
            dtype = 'float',
            )
        # "L'entreprise emploie-t-elle plus de 9 ou 10 salariés dans le périmètre de l'Autorité organisatrice de transport
        # (AOT) suivante ou syndicat mixte de transport (SMT)"
        return taux_versement_transport * or_(effectif_entreprise >= seuil_effectif, public) / 100


class versement_transport(Variable):
    value_type = float
    entity = Individu
    label = "Versement transport"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        taux_versement_transport = individu('taux_versement_transport', period)
        cotisation = - taux_versement_transport * assiette_cotisations_sociales
        return cotisation


# File loading and parsing -> global table_versement_transport

def preload_taux_versement_transport():
    if 'table_versement_transport' not in globals():
        global table_versement_transport
        with open(COUNTRY_DIR + '/assets/versement_transport/taux.json') as data_file:
            table_versement_transport = json.load(data_file)


def get_taux_versement_transport(code_commune, period):
    if not isinstance(code_commune, str):  # In Python 3, code_commune is a bytes
        code_commune = code_commune.decode('utf-8')
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
