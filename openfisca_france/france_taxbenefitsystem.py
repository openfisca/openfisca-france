# -*- coding: utf-8 -*-

import os
import pickle

import checksumdir
import appdirs

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france.entities import entities
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from openfisca_france.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist
from openfisca_france.situation_examples import couple


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PARAMETER_TREE = True


class FranceTaxBenefitSystem(TaxBenefitSystem):
    """French tax benefit system"""
    CURRENCY = u"€"
    DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    preprocess_parameters = staticmethod(preprocessing.preprocess_parameters)

    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)

        self.load_parameters_from_cache()
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        self.cache_blacklist = conf_cache_blacklist

        self.open_api_config = {
            "variable_example": "rsa_montant",
            "parameter_example": "cotsoc.gen.smic_h_b",
            "simulation_example": couple,
            }

    def load_parameters_from_cache(self):
        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        if not CACHE_PARAMETER_TREE:
            return self.load_parameters(param_dir)
        dir_hash = checksumdir.dirhash(param_dir)
        cached_dir = appdirs.user_cache_dir(self.get_package_metadata()['name'])
        pickle_path = os.path.join(cached_dir, f'{dir_hash}.pickle')

        if os.path.isfile(pickle_path):
            # print("Found cached parameters")
            with open(pickle_path, "rb") as pickle_file:
                self.parameters = pickle.load(pickle_file)
        else:
            # print("No cached parameters")
            if not os.path.isdir(cached_dir):
                os.mkdir(cached_dir)
            self.load_parameters(param_dir)
            with open(pickle_path, "wb+") as pickle_file:
                pickle.dump(self.parameters, pickle_file)


    def prefill_cache(self):
        # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
        from .model.prestations import aides_logement
        aides_logement.preload_zone_apl()
        from .model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales import versement_transport
        versement_transport.preload_taux_versement_transport()
