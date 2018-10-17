# -*- coding: utf-8 -*-

import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france.entities import entities
from openfisca_france import decompositions, scenarios
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from openfisca_france.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist
from openfisca_france.situation_examples import couple


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class FranceTaxBenefitSystem(TaxBenefitSystem):
    """French tax benefit system"""
    CURRENCY = u"€"
    DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    decomposition_file_path = os.path.join(
        os.path.dirname(os.path.abspath(decompositions.__file__)), 'decomp.xml')
    preprocess_parameters = staticmethod(preprocessing.preprocess_parameters)

    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
    REV_TYP = None  # utils.REV_TYP  # Not defined for France
    REVENUES_CATEGORIES = {
        'brut': ['salaire_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
        'imposable': ['salaire_imposable', 'chomage_imposable', 'retraite_imposable', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon', 'prelevements_sociaux_revenus_capital'],
        'net': ['salaire_net', 'chomage_net', 'retraite_nette', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_net', 'fon'],
        'superbrut': ['salaire_super_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
        }

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        self.Scenario = scenarios.Scenario

        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_dir)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        self.cache_blacklist = conf_cache_blacklist

        self.open_api_config = {
            "variable_example": "rsa_montant",
            "parameter_example": "cotsoc.gen.smic_h_b",
            "simulation_example": couple,
            }

    def prefill_cache(self):
        # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
        from .model.prestations import aides_logement
        aides_logement.preload_zone_apl()
        from .model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales import versement_transport
        versement_transport.preload_taux_versement_transport()
