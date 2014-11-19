# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os


from openfisca_core.taxbenefitsystems import LegacyTaxBenefitSystem
from ..entities import entity_class_by_symbol
from ..scenarios import Scenario
from .. import COUNTRY_DIR

from .cotisations_sociales import preprocessing

def init_country():
    class TaxBenefitSystem(LegacyTaxBenefitSystem):
        entity_class_by_key_plural = {
            entity_class.key_plural: entity_class
            for entity_class in entity_class_by_symbol.itervalues()
            }

        legislation_xml_file_path = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        preprocess_compact_legislation = staticmethod(preprocessing.preprocess_compact_legislation)

    # Define class attributes after class declaration to avoid "name is not defined" exceptions.
    TaxBenefitSystem.Scenario = Scenario



    return TaxBenefitSystem

# Import new syntax-based output variables.
from . import (  # noqa
    input_variables,
    inversion_revenus,
#    lgtm_new,
    )

# Import model modules.
#from . import calage as cl
#from . import cmu as cmu
#from . import common as cm
#from .cotisations_sociales import capital as cs_capital
from .cotisations_sociales import travail_new  # noqa
#from .cotisations_sociales import remplacement as cs_remplac
#from . import irpp as ir
#from . import irpp_charges_deductibles as cd
#from . import irpp_credits_impots as ci
#from . import irpp_plus_values_immo as immo
#from . import irpp_reductions_impots as ri
#from . import isf as isf
#from . import lgtm as lg
## from .minima_sociaux import aah
#from .minima_sociaux import asi_aspa
#from .minima_sociaux import ass
#from .minima_sociaux import rsa
#from .prestations_familiales import aeeh
#from .prestations_familiales import af
#from .prestations_familiales import ars
#from .prestations_familiales import asf
#from .prestations_familiales import paje
#from .prestations_familiales import cf
#from . import pfam as pf
#from . import th as th


TaxBenefitSystem = init_country()
tax_benefit_system = TaxBenefitSystem()


def test_1():
    year = 2012
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(
            exposition_accident = 3,
#            localisation_entreprise = "75001",
            salbrut = 3000 * 12,
            taille_entreprise = 3,
            type_sal = 0,
            ),
#        menage = dict(
#            zone_apl = 1,
#            ),
        ).new_simulation(debug = True)
    print simulation.calculate("maladie_employe")
