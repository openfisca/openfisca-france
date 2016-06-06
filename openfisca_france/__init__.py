# -*- coding: utf-8 -*-

import os, itertools, glob

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from . import entities
from . import decompositions, scenarios
from .model import datatrees
from .model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from .conf.cache_blacklist import cache_blacklist as conf_cache_blacklist


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))

class FranceTaxBenefitSystem(TaxBenefitSystem):
    """French tax benefit system"""
    CURRENCY = u"€"
    DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
    preprocess_legislation = staticmethod(preprocessing.preprocess_legislation)
    columns_name_tree_by_entity = datatrees.columns_name_tree_by_entity

    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
    REV_TYP = None  # utils.REV_TYP  # Not defined for France
    REVENUES_CATEGORIES = {
    'brut': ['salaire_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    'imposable': ['salaire_imposable', 'chomage_imposable', 'retraite_imposable', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
    'net': ['salaire_net', 'chomage_net', 'retraite_nette', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_net', 'fon'],
    'superbrut': ['salaire_super_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    }

    def prefill_cache(self):
        # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
        from .model.prestations import aides_logement
        aides_logement.preload_zone_apl()
        from .model.prelevements_obligatoires.prelevements_sociaux import taxes_salaires_main_oeuvre
        taxes_salaires_main_oeuvre.preload_taux_versement_transport()


def init_tax_benefit_system():
    tax_benefit_system = FranceTaxBenefitSystem(entities.entities)
    tax_benefit_system.Scenario = scenarios.Scenario

    param_file = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
    tax_benefit_system.add_legislation_params(param_file)
    tax_benefit_system.add_variables_from_directory(os.path.join(COUNTRY_DIR,'model'))

    tax_benefit_system.cache_blacklist = conf_cache_blacklist

    for extension_dir in EXTENSIONS_DIRECTORIES:
        tax_benefit_system.load_extension(extension_dir)

    return tax_benefit_system
