# -*- coding: utf-8 -*-

import os
import glob

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from .entities import entities
from . import decompositions, scenarios

from .model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from .conf.cache_blacklist import cache_blacklist as conf_cache_blacklist


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class FranceTaxBenefitSystem(TaxBenefitSystem):
    """French tax benefit system"""
    CURRENCY = u"€"
    DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    decomposition_file_path = os.path.join(
        os.path.dirname(os.path.abspath(decompositions.__file__)), 'decomp.xml')
    preprocess_legislation = staticmethod(preprocessing.preprocess_legislation)

    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
    REV_TYP = None  # utils.REV_TYP  # Not defined for France
    REVENUES_CATEGORIES = {
    'brut': ['salaire_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    'imposable': ['salaire_imposable', 'chomage_imposable', 'retraite_imposable', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
    'net': ['salaire_net', 'chomage_net', 'retraite_nette', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_net', 'fon'],
    'superbrut': ['salaire_super_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    }

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        self.Scenario = scenarios.Scenario

        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        self.add_legislation_params(param_dir)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        self.cache_blacklist = conf_cache_blacklist

    def prefill_cache(self):
        # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
        from .model.prestations import aides_logement
        aides_logement.preload_zone_apl()
        from .model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales import versement_transport
        versement_transport.preload_taux_versement_transport()
