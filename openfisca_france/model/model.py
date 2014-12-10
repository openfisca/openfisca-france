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
    build_dated_formula,
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
build_dated_formula = partial(
    build_dated_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_select_formula = partial(
    build_select_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


############################################################
# Cotisations sociales
############################################################


# build_dated_formula('prelsoc_cap_bar',
#     [
#         dict(start = date(2002, 1, 1),
#           end = date(2005, 12, 31),
#           function = cs_capital._prelsoc_cap_bar__2005,
#          ),
#         dict(start = date(2006, 1, 1),
#           end = date(2008, 12, 31),
#           function = cs_capital._prelsoc_cap_bar_2006_2008,
#          ),
#         dict(start = date(2009, 1, 1),
#           end = date(2015, 12, 31),
#           function = cs_capital._prelsoc_cap_bar_2009_,
#          ),
#     ],
#     FloatCol(entity='ind',
#     label = u"Prélèvements sociaux sur les revenus du capital soumis au barème",
#     url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))

# Revenus fonciers (sur les foyers)
build_dated_formula('prelsoc_fon',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_fon__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_fon_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_fon_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les revenus fonciers",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS",
    ))

# Plus values de cessions de valeurs mobilières
build_dated_formula('prelsoc_pv_mo',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_pv_mo__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_pv_mo_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_pv_mo_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))
# Plus-values immobilières
build_dated_formula('prelsoc_pv_immo',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_pv_immo__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_pv_immo_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_pv_immo_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les plus-values immobilières",
    url = u"http://www.pap.fr/argent/impots/les-plus-values-immobilieres/a1314/l-imposition-de-la-plus-value-immobiliere",
    ))

############################################################
# Impôt sur le revenu
############################################################

build_alternative_formula(
    'agem',
    [
        ir._agem_from_birth,
        ir._agem_from_age,
        ],
    AgeCol(label = u"Âge (en mois)", val_type = "months"),
    )


# charges déductibles
build_dated_formula('cd_percap',
    [
        dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = cd._cd_percap_2002,
         ),
        dict(start = date(2003, 1, 1),
          end = date(2006, 12, 31),
          function = cd._cd_percap_2003_2006,
         ),
    ],
    FloatCol(entity='foy'))

build_dated_formula(
    'cd1',
    [dict(start = date(2002, 1, 1),
         end = date(2003, 12, 31),
         function = cd._cd1_2002_2003,
         ),
     dict(start = date(2004, 1, 1),
         end = date(2005, 12, 31),
         function = cd._cd1_2004_2005,
         ),
     dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = cd._cd1_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = cd._cd1_2007_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2013, 12, 31),
         function = cd._cd1_2009_2013,
         ),
     dict(start = date(2014, 1, 1),
         end = date(2014, 12, 31),
         function = cd._cd1_2014,
         ),
    ],
    FloatCol(entity = 'foy',
    label = u"Charges déductibles non plafonnées",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php"))

build_dated_formula(
    'cd2',
    [dict(start = date(2002, 1, 1),
         end = date(2005, 12, 31),
         function = cd._cd2_2002_2005,
         ),
     dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = cd._cd2_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = cd._cd2_2007_2008,
         ),
    ],
    FloatCol(entity = 'foy',
    label = u"Charges déductibles plafonnées",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php"))

build_dated_formula('rev_cat_rvcm',
    [
        dict(start = date(2002, 1, 1),
          end = date(2004, 12, 31),
          function = ir._rev_cat_rvcm__2004,
         ),
        dict(start = date(2005, 1, 1),
          end = date(2012, 12, 31),
          function = ir._rev_cat_rvcm_2005_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = ir._rev_cat_rvcm_2013_,
         ),
    ],
    FloatCol(entity='foy',
    label = u'Revenu catégoriel - Capitaux',
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"))

build_dated_formula('plus_values',
    [
        dict(start = date(2007, 1, 1),
          end = date(2007, 12, 31),
          function = ir._plus_values__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2011, 12, 31),
          function = ir._plus_values_2008_2011,
         ),
        dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ir._plus_values_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = ir._plus_values_2013_,
         ),
    ],
    FloatCol(entity='foy'))

# réductions d'impots
build_dated_formula(
    'donapd',
    [dict(start = date(2002, 1, 1),
         end = date(2010, 12, 31),
         function = ri._donapd_2002_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2013, 12, 31),
         function = ri._donapd_2011_2013,
         ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula(
    'dfppce',
    [dict(start = date(2002, 1, 1),
         end = date(2003, 12, 31),
         function = ri._dfppce_2002_2003,
         ),
     dict(start = date(2004, 1, 1),
             end = date(2004, 12, 31),
             function = ri._dfppce_2004,
             ),
     dict(start = date(2005, 1, 1),
             end = date(2005, 12, 31),
             function = ri._dfppce_2005,
             ),
     dict(start = date(2006, 1, 1),
             end = date(2006, 12, 31),
             function = ri._dfppce_2006,
             ),
     dict(start = date(2007, 1, 1),
             end = date(2007, 12, 31),
             function = ri._dfppce_2007,
             ),
     dict(start = date(2008, 1, 1),
             end = date(2010, 12, 31),
             function = ri._dfppce_2008_2010,
             ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._dfppce_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._dfppce_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._dfppce_2013,
         ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('resimm', [
     dict(start = date(2009, 1, 1),
         end = date(2010, 12, 31),
         function = ri._resimm_2009_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._resimm_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._resimm_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._resimm_2013,
         ),
],
FloatCol(entity = 'foy'))
build_dated_formula('patnat', [
     dict(start = date(2010, 1, 1),
         end = date(2010, 12, 31),
         function = ri._patnat_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._patnat_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._patnat_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._patnat_2013,
         ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('saldom',
    [
     dict(start = date(2002, 1, 1),
         end = date(2004, 12, 31),
         function = ri._saldom_2002_2004,
         ),
     dict(start = date(2005, 1, 1),
         end = date(2006, 12, 31),
         function = ri._saldom_2005_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = ri._saldom_2007_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2013, 12, 31),
         function = ri._saldom_2009_2013,
         ),
    ],
    FloatCol(entity= 'foy'))

build_dated_formula('spfcpi',
    [
     dict(start = date(2002, 1, 1), #quid d'avant 2002 ?
         end = date(2002, 12, 31),
         function = ri._spfcpi_2002,
         ),
     dict(start = date(2003, 1, 1),
         end = date(2006, 12, 31),
         function = ri._spfcpi_2003_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2010, 12, 31),
         function = ri._spfcpi_2007_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2013, 12, 31),
         function = ri._spfcpi_2011_2013,
         ),
     dict(start = date(2014, 1, 1),
         end = date(2014, 12, 31),
         function = ri._spfcpi_2014,
         ),
    ],
    FloatCol(entity= 'foy'))

build_dated_formula('cappme',
    [
     dict(start = date(2002, 1, 1), #quid d'avant 2002 ?
         end = date(2002, 12, 31),
         function = ri._cappme_2002,
         ),
     dict(start = date(2003, 1, 1),
         end = date(2003, 12, 31),
         function = ri._cappme_2003,
         ),
     dict(start = date(2004, 1, 1),
         end = date(2004, 12, 31),
         function = ri._cappme_2004,
         ),
     dict(start = date(2005, 1, 1),
         end = date(2008, 12, 31),
         function = ri._cappme_2005_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2010, 12, 31),
         function = ri._cappme_2009_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._cappme_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._cappme_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._cappme_2013,
         ),
    ],
    FloatCol(entity= 'foy'))

build_dated_formula('invfor',
    [
     dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = ri._invfor_2002_2005,
          ),
     dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = ri._invfor_2006_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._invfor_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._invfor_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._invfor_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._invfor_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._invfor_2013,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('invlst',
    [
     dict(start = date(2004, 1, 1),
          end = date(2004, 12, 31),
          function = ri._invlst_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2010, 12, 31),
          function = ri._invlst_2005_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._invlst_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._invlst_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._invlst_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('domlog',
    [
     dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._domlog_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2004, 12, 31),
          function = ri._domlog_2003_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2007, 12, 31),
          function = ri._domlog_2005_2007,
          ),
     dict(start = date(2008, 1, 1),
          end = date(2008, 12, 31),
          function = ri._domlog_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._domlog_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._domlog_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._domlog_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._domlog_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._domlog_2013,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('creaen',
    [
     dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = ri._creaen_2006_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._creaen_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2011, 12, 31),
          function = ri._creaen_2010_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2014, 12, 31),
          function = ri._creaen_2012_2014,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('scelli',
    [
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._scelli_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._scelli_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._scelli_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._scelli_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._scelli_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('locmeu',
    [
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._locmeu_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._locmeu_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._locmeu_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._locmeu_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._locmeu_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('doment',
    [
     dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ri._doment_2005,
          ),
     dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = ri._doment_2006_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._doment_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._doment_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._doment_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._doment_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._doment_2013,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('domsoc',
    [
     dict(start = date(2010, 1, 1),
          end = date(2012, 12, 31),
          function = ri._domsoc_2010_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._domsoc_2013,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula('garext',
    [
     dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._garext_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2005, 12, 31),
          function = ri._garext_2003_2005,
          ),
    ],
    FloatCol(entity = 'foy'))

build_dated_formula(
    'reductions',
    [dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._reductions_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2004, 12, 31),
          function = ri._reductions_2003_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ri._reductions_2005,
          ),
    dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = ri._reductions_2006,
         ),
     dict(start = date(2007, 1, 1),
          end = date(2007, 12, 31),
          function = ri._reductions_2007,
          ),
     dict(start = date(2008, 1, 1),
          end = date(2008, 12, 31),
          function = ri._reductions_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._reductions_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._reductions_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._reductions_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._reductions_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 1, 1),
          function = ri._reductions_2013,
          ),
     ],
    FloatCol(entity = 'foy'))

build_dated_formula('imp_lib',# TODO: Check - de 2000euros
    [
        dict(start = date(2002, 1, 1),
          end = date(2007, 12, 31),
          function = ir._imp_lib__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2012, 12, 31),
          function = ir._imp_lib_2008_,
         ),
    ],
    FloatCol(entity='foy',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))


# Autres crédits d'impôts

build_dated_formula('creimp',  #TODO: Change name to credits_impot (before, take care of imputations)
    [
        dict(  #right way to ident dictionary
            start = date(2002, 1, 1),
            end = date(2002, 12, 31),
            function = ci._creimp_2002,
            ),
        dict(start = date(2003, 1, 1),
                 end = date(2003, 12, 31),
                 function = ci._creimp_2003,
                 ),
        dict(start = date(2004, 1, 1),
                 end = date(2004, 12, 31),
                 function = ci._creimp_2004,
                 ),
        dict(start = date(2005, 1, 1),
                 end = date(2005, 12, 31),
                 function = ci._creimp_2005,
                 ),

        dict(start = date(2006, 1, 1),
                 end = date(2006, 12, 31),
                 function = ci._creimp_2006,
                 ),
        dict(start = date(2007, 1, 1),
                 end = date(2007, 12, 31),
                 function = ci._creimp_2007,
                 ),
        dict(start = date(2008, 1, 1),
                 end = date(2008, 12, 31),
                 function = ci._creimp_2008,
                 ),
        dict(start = date(2009, 1, 1),
                 end = date(2009, 12, 31),
                 function = ci._creimp_2009,
                 ),
        dict(start = date(2010, 1, 1),
                 end = date(2011, 12, 31),
                 function = ci._creimp_2010_2011,
                 ),

        dict(start = date(2012, 1, 1),
                 end = date(2012, 12, 31),
                 function = ci._creimp_2012,
                 ),
        dict(start = date(2013, 1, 1),
                 end = date(2013, 12, 31),
                 function = ci._creimp_2013,
                 ),
        ],
    FloatCol(entity = 'foy'))

build_dated_formula('accult',
 [
  dict(start = date(2002, 1, 1),
       end = date(2012, 12, 31),
       function = ci._accult,
      ),
  dict(start = date(2012, 1, 1),
       end = date(2013, 12, 31),
       function = ri._accult,
      )
 ],
 FloatCol(entity = 'foy'))

build_dated_formula('mecena',
 [
  dict(start = date(2003, 1, 1),
       end = date(2012, 12, 31),
       function = ci._mecena,
      ),
  dict(start = date(2012, 1, 1),
       end = date(2013, 12, 31),
       function = ri._mecena,
      )
 ],
 FloatCol(entity = 'foy'))

build_dated_formula('aidper',
[
     dict(start = date(2002, 1, 1),
      end = date(2003, 12, 31),
      function = ci._aidper_2002_2003,
     ),
     dict(start = date(2004, 1, 1),
      end = date(2005, 12, 31),
      function = ci._aidper_2004_2005,
     ),
     dict(start = date(2006, 1, 1),
      end = date(2009, 12, 31),
      function = ci._aidper_2006_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2011, 12, 31),
      function = ci._aidper_2010_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2012, 12, 31),
      function = ci._aidper_2012,
     ),
     dict(start = date(2013, 1, 1),
      end = date(2013, 12, 31),
      function = ci._aidper_2013,
     ),
],
FloatCol(entity='foy'))
build_dated_formula('quaenv',
[
     dict(start = date(2005, 1, 1),
      end = date(2005, 12, 31),
      function = ci._quaenv_2005,
     ),
     dict(start = date(2006, 1, 1),
      end = date(2008, 12, 31),
      function = ci._quaenv_2006_2008,
     ),
     dict(start = date(2009, 1, 1),
      end = date(2009, 12, 31),
      function = ci._quaenv_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2011, 12, 31),
      function = ci._quaenv_2010_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2012, 12, 31),
      function = ci._quaenv_2012,
     ),
  dict(start = date(2013, 1, 1),
      end = date(2013, 12, 31),
      function = ci._quaenv_2013,
     ),
],
FloatCol(entity='foy'))

build_dated_formula('preetu',
    [
        dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ci._preetu_2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2007, 12, 31),
          function = ci._preetu_2006_2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2015, 12, 31),
          function = ci._preetu_2008_,
         ),
    ],
    FloatCol(entity='foy'))
build_dated_formula('saldom2',
    [
        dict(start = date(2007, 1, 1),
          end = date(2008, 12, 31),
          function = ci._saldom2_2007_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2013, 12, 31),
          function = ci._saldom2_2009_,
         ),
    ],
    FloatCol(entity='foy'))
build_dated_formula('inthab',
[
     dict(start = date(2007, 1, 1),
      end = date(2007, 12, 31),
      function = ci._inthab_2007,
     ),
     dict(start = date(2008, 1, 1),
      end = date(2008, 12, 31),
      function = ci._inthab_2008,
     ),
     dict(start = date(2009, 1, 1),
      end = date(2009, 12, 31),
      function = ci._inthab_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2010, 12, 31),
      function = ci._inthab_2010,
     ),
     dict(start = date(2011, 1, 1),
      end = date(2011, 12, 31),
      function = ci._inthab_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2013, 12, 31),
      function = ci._inthab_2012_2013,
     ),
],
FloatCol(entity='foy'))

build_dated_formula(
    'credits_impot',  # TODO: Change name to imputations
    [
        dict(start = date(2002, 1, 1),
             end = date(2002, 12, 31),
             function = ci._credits_impot_2002,
             ),
        dict(start = date(2003, 1, 1),
             end = date(2004, 12, 31),
             function = ci._credits_impot_2003_2004,
             ),
        dict(start = date(2005, 1, 1),
             end = date(2006, 12, 31),
             function = ci._credits_impot_2005_2006,
             ),
        dict(start = date(2007, 1, 1),
             end = date(2007, 12, 31),
             function = ci._credits_impot_2007,
             ),
        dict(start = date(2008, 1, 1),
             end = date(2008, 12, 31),
             function = ci._credits_impot_2008,
             ),
        dict(start = date(2009, 1, 1),
             end = date(2009, 12, 31),
             function = ci._credits_impot_2009,
             ),
        dict(start = date(2010, 1, 1),
             end = date(2010, 12, 31),
             function = ci._credits_impot_2010,
             ),
        dict(start = date(2011, 1, 1),
             end = date(2011, 12, 31),
             function = ci._credits_impot_2011,
             ),
        dict(start = date(2012, 1, 1),
             end = date(2012, 12, 31),
             function = ci._credits_impot_2012,
             ),
        dict(start = date(2013, 1, 1),
             end = date(2013, 12, 31),
             function = ci._credits_impot_2013,
             ),
        ],
    FloatCol(entity = 'foy'),
    )

build_dated_formula('rev_cap_lib',
    [
        dict(start = date(2002, 1, 1),
          end = date(2007, 12, 31),
          function = ir._rev_cap_lib__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2015, 12, 31),
          function = ir._rev_cap_lib_2008_,
         ),
    ],
    FloatCol(entity='foy',
    url = u"http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"))


############################################################
# Impôt de solidarité sur la fortune
############################################################


build_dated_formula('isf_iai',
    [
        dict(start = date(2011, 1, 1),
          end = date(2015, 12, 31),
          function = isf._isf_iai_2011_,
         ),
        dict(start = date(2002, 1, 1),
          end = date(2010, 12, 31),
          function = isf._isf_iai__2010,
         ),
    ],
    FloatCol(entity='foy'))

build_dated_formula('isf_apres_plaf',
    [
        dict(start = date(2002, 1, 1),
          end = date(2011, 12, 31),
          function = isf._isf_apres_plaf__2011,
         ),
        dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = isf._isf_apres_plaf_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = isf._isf_apres_plaf_2013_,
         ),
    ],
    FloatCol(entity='foy'))


############################################################
# Prestations familiales
############################################################


build_dated_formula('aeeh',
    [
        dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = aeeh._aeeh__2002,
         ),
        dict(start = date(2003, 1, 1),
          end = date(2015, 12, 31),
          function = aeeh._aeeh_2003_,
         ),
    ],
    FloatCol(entity='fam',
    label = u"Allocation d'éducation de l'enfant handicapé",
    url = u"http://vosdroits.service-public.fr/particuliers/N14808.xhtml"))


############################################################
# Allocation adulte handicapé
############################################################


# build_dated_formula('caah',
#     [
#         dict(start = date(2002, 1, 1),
#           end = date(2005, 12, 31),
#           function = aah._caah__2005,
#          ),
#         dict(start = date(2006, 1, 1),
#           end = date(2015, 12, 31), #TODO:actualiser la date (si la loi n'a pas changé)
#           function = aah._caah_2006_,
#          ),
#     ],
#     FloatCol(entity='fam',
#     label = u"Complément de l'allocation adulte handicapé",
#     url = u"http://vosdroits.service-public.fr/particuliers/N12230.xhtml"))
