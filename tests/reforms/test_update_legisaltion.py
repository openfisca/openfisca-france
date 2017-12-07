# -*- coding: utf-8 -*-

from __future__ import division


import datetime

#%%
import logging


from numpy import maximum as max_, minimum as min_, where


from openfisca_core import periods
from ..cache import tax_benefit_system
from openfisca_france.reforms.fusion_rsa_apl_progressive import create_fusion_rsa_apl_progressive

log = logging.getLogger(__name__)


def test():
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    reform = create_fusion_rsa_apl_progressive(socle = 600)
    reform_tax_benefit_system = reform(tax_benefit_system)
    year = 2012
    scenario = reform_tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_de_base',
                ),
            ],
        period = periods.period(year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(
            loyer = 1000,
            ),
        )
