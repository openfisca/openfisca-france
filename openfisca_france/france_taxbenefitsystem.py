import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france.entities import entities
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from openfisca_france.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist
from openfisca_france.situation_examples import couple


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class FranceTaxBenefitSystem(TaxBenefitSystem):
    """French tax benefit system"""
    CURRENCY = "€"
    DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    preprocess_parameters = staticmethod(preprocessing.preprocess_parameters)

    REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)

        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_dir)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        self.cache_blacklist = conf_cache_blacklist

        self.open_api_config = {
            "variable_example": "rsa_montant",
            "parameter_example": "marche_travail.salaire_minimum.smic_h_b",
            "simulation_example": couple,
            }

    def prefill_cache(self):
        # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
        from .model.prestations import aides_logement
        aides_logement.preload_zone_apl()
        from .model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales import versement_transport
        versement_transport.preload_taux_versement_transport()
