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


# TODO: actualiser la date des end (c'est souvent 2014 ou 2015)


from datetime import date
from functools import partial

from openfisca_core.columns import AgeCol, BoolCol, EnumCol, FloatCol, PeriodSizeIndependentIntCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import (
    build_alternative_formula,
    build_select_formula,
    )

from .. import entities
# Import new syntax-based output variables.
from . import (
    inversion_revenus,
    travailleurs_non_salaries,
    education,
    )

from .minima_sociaux import (
    asi_aspa,
    ass,
    cmu,
    rsa,
    )

from .cotisations_sociales import remplacement

# Import model modules.
from . import calage as cl
from . import common as cm

#from .cotisations_sociales import remplacement as cs_remplac

from . import irpp as ir
from . import irpp_charges_deductibles as cd
from . import irpp_credits_impots as ci
from . import irpp_plus_values_immo as immo
from . import irpp_reductions_impots as ri
from . import isf as isf

# from .minima_sociaux import aah

from .prestations_familiales import aeeh
from .prestations_familiales import af
from .prestations_familiales import ars
from .prestations_familiales import asf
from .prestations_familiales import paje
from .prestations_familiales import cf

from . import pfam as pf
from . import th as th
from . import lgtm

from .input_variables import travail_base  # noqa
from .cotisations_sociales import remuneration_prive
from .cotisations_sociales import travail_prive
from .cotisations_sociales import travail_verification

from .cotisations_sociales import travail_fonction_publique
from .cotisations_sociales import travail_totaux
from .cotisations_sociales import allegements

from .cotisations_sociales import capital as cs_capital


build_alternative_formula = partial(
    build_alternative_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


build_select_formula = partial(
    build_select_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


############################################################
# Impôt sur le revenu
#
###########################################################


build_alternative_formula(
    'agem',
    [
        ir._agem_from_birth,
        ir._agem_from_age,
        ],
    AgeCol(label = u"Âge (en mois)", val_type = "months"),
    )
