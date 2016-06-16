# -*- coding: utf-8 -*-

import os, itertools


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"€"
REVENUES_CATEGORIES = {
    'brut': ['salaire_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    'imposable': ['salaire_imposable', 'chomage_imposable', 'retraite_imposable', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
    'net': ['salaire_net', 'chomage_net', 'retraite_nette', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_net', 'fon'],
    'superbrut': ['salaire_super_brut', 'chomage_brut', 'retraite_brute', 'pensions_alimentaires_percues', 'pensions_alimentaires_versees', 'rev_cap_brut', 'fon'],
    }


def init_country():  # drop_survey_only_variables = False, simulate_f6de = False, start_from = 'imposable'
    """Create a country-specific TaxBenefitSystem."""
    # from openfisca_core.columns import FloatCol
    from openfisca_core.taxbenefitsystems import MultipleXmlBasedTaxBenefitSystem
    from . import decompositions, entities, scenarios
    from .model import datatrees
    from .model import model  # Load output variables into entities. # noqa analysis:ignore
    from .model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
    from .conf.cache_blacklist import cache_blacklist as conf_cache_blacklist

    # if simulate_f6de:
    #     del column_by_name['f6de']
    #     csg_deduc_patrimoine_simulated = prestation_by_name.pop('csg_deduc_patrimoine_simulated')
    #     prestation_by_name['csg_deduc_patrimoine'] = FloatCol(
    #         csg_deduc_patrimoine_simulated._func,
    #         entity = csg_deduc_patrimoine_simulated.entity,
    #         label = csg_deduc_patrimoine_simulated.label,
    #         start = csg_deduc_patrimoine_simulated.start,
    #         end = csg_deduc_patrimoine_simulated.end,
    #         val_type = csg_deduc_patrimoine_simulated.val_type,
    #         freq = csg_deduc_patrimoine_simulated.freq,
    #         survey_only = False,
    #         )
    # else:
    #     prestation_by_name.pop('csg_deduc_patrimoine_simulated', None)

    class TaxBenefitSystem(MultipleXmlBasedTaxBenefitSystem):
        """French tax benefit system"""
        check_consistency = None  # staticmethod(utils.check_consistency)
        CURRENCY = CURRENCY
        DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
        DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
        DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
        entity_class_by_key_plural = dict(
            (entity_class.key_plural, entity_class)
            for entity_class in entities.entity_class_by_symbol.itervalues()
            )

        # Declared below to avoid "name is not defined" exception
        # column_by_name = None
        # prestation_by_name = None

        columns_name_tree_by_entity = datatrees.columns_name_tree_by_entity

        legislation_xml_info_list = [
            (
                os.path.join(COUNTRY_DIR, 'param', 'param.xml'),
                None,
                ),
            # (
            #     os.path.join(COUNTRY_DIR, 'assets', 'xxx', 'yyy.xml'),
            #     ('insert', 'into', 'existing', 'element'),
            #     ),
            ] + zip(model.extensions.extensions_parameters, itertools.repeat(None))

        preprocess_legislation = staticmethod(preprocessing.preprocess_legislation)

        REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
        REV_TYP = None  # utils.REV_TYP  # Not defined for France
        REVENUES_CATEGORIES = REVENUES_CATEGORIES
        Scenario = scenarios.Scenario
        cache_blacklist = conf_cache_blacklist

        def prefill_cache(self):
            # Compute one "zone APL" variable, to pre-load CSV of "code INSEE commune" to "Zone APL".
            from .model.prestations import aides_logement
            aides_logement.preload_zone_apl()
            from .model.prelevements_obligatoires.prelevements_sociaux import taxes_salaires_main_oeuvre
            taxes_salaires_main_oeuvre.preload_taux_versement_transport()

    return TaxBenefitSystem


def init_tax_benefit_system():
    """
    Helper function which suits most of the time.

    Use `init_country` if you need to get the `TaxBenefitSystem` class.
    """
    TaxBenefitSystem = init_country()
    tax_benefit_system = TaxBenefitSystem()
    return tax_benefit_system
