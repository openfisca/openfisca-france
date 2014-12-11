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


from __future__ import division

import copy
import logging

from numpy import maximum as max_, minimum as min_
from openfisca_core import formulas, reforms, tools

from ..base import *


log = logging.getLogger(__name__)


def _reductions_2013(accult, adhcga, cappme, creaen, daepad, deffor, dfppce, doment, domlog, donapd, duflot, ecpess,
                     garext, intagr, invfor, invlst, ip_net, locmeu, mecena, mohist, patnat, prcomp, repsoc, resimm,
                     rsceha, saldom, scelli, sofica, spfcpi, reduction_impot_exceptionnelle):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2013
    '''
    total_reductions = (accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
                        duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat +
                        prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi +
                        reduction_impot_exceptionnelle)
    return min_(ip_net, total_reductions)


def build_reform_entity_class_by_key_plural(tax_benefit_system):
    reform_entity_class_by_key_plural = tax_benefit_system.entity_class_by_key_plural.copy()
    FoyersFiscaux = reform_entity_class_by_key_plural['foyers_fiscaux']
    ReformFoyersFiscaux = type('ReformFoyersFiscaux', (FoyersFiscaux, ),
        {'column_by_name': FoyersFiscaux.column_by_name.copy()})
    reform_entity_class_by_key_plural['foyers_fiscaux'] = ReformFoyersFiscaux

    # reduction_impot_exceptionnelle
    class reduction_impot_exceptionnelle(formulas.SimpleFormulaColumn):
        column = FloatCol
        entity_class = FoyersFiscaux
        label = u"Réduction d'impôt exceptionnelle"

        def function(self, rfr, nb_adult, nb_par, _P):
            parametres = _P.plfr2014.reduction_impot_exceptionnelle
            plafond = parametres.seuil * nb_adult + (nb_par - nb_adult) * 2 * parametres.majoration_seuil
            montant = parametres.montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

        def get_output_period(self, period):
            return period.start.offset('first-of', 'month').period('year')

    ReformFoyersFiscaux.column_by_name['reduction_impot_exceptionnelle'] = reduction_impot_exceptionnelle

    # reductions

    reductions_column = FoyersFiscaux.column_by_name['reductions']
    reform_reductions_column = tools.empty_clone(reductions_column)
    reform_reductions_column.__dict__ = reductions_column.__dict__.copy()

    reductions_formula_class_2013 = reform_reductions_column.formula_class.dated_formulas_class[-1]['formula_class']  # noqa
    reform_reductions_formula_class_2013 = type(
        'reform_reductions_formula_class_2013',
        (reductions_formula_class_2013, ),
        {'function': staticmethod(_reductions_2013)},
        )
    reform_reductions_formula_class_2013.extract_variables_name()

    reform_dated_formulas_class = reform_reductions_column.formula_class.dated_formulas_class[:]
    reform_dated_formulas_class[-1] = reform_dated_formulas_class[-1].copy()
    reform_dated_formulas_class[-1]['formula_class'] = reform_reductions_formula_class_2013

    reform_dated_formula_class = type('reform_dated_formula_class', (reform_reductions_column.formula_class, ),
        {'dated_formulas_class': reform_dated_formulas_class})

    reform_reductions_column.formula_class = reform_dated_formula_class

    ReformFoyersFiscaux.column_by_name['reductions'] = reform_reductions_column

    return reform_entity_class_by_key_plural


def build_new_legislation_nodes():
    return {
        "plfr2014": {
            "@type": "Node",
            "description": "Projet de loi de finance 2014",
            "children": {
                "reduction_impot_exceptionnelle": {
                    "@type": "Node",
                    "description": "Réduction d'impôt exceptionnelle",
                    "children": {
                        "montant_plafond": {
                            "@type": "Parameter",
                            "description": "Montant plafond par part pour les deux premières parts",
                            "format": "integer",
                            "unit": "currency",
                            "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 350}],
                            },
                        "seuil": {
                            "@type": "Parameter",
                            "description": "Seuil (à partir duquel la réduction décroît) par part pour les deux "
                                           "premières parts",
                            "format": "integer",
                            "unit": "currency",
                            "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 13795}],
                            },
                        "majoration_seuil": {
                            "@type": "Parameter",
                            "description": "Majoration du seuil par demi-part supplémentaire",
                            "format": "integer",
                            "unit": "currency",
                            "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 3536}],
                            },
                        },
                    },
                },
            },
        }


def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(build_new_legislation_nodes())
    return reforms.Reform(
        entity_class_by_key_plural = build_reform_entity_class_by_key_plural(tax_benefit_system),
        legislation_json = reform_legislation_json,
        name = u'PLFR2014',
        reference = tax_benefit_system,
        )
