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
from openfisca_core.columns import FloatCol
from openfisca_core.enumerations import Enum


log = logging.getLogger(__name__)

CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])


def _alleg_plfrss2014_prive(salbrut, sal_h_b, type_sal, _P):
    '''
    Allègement de cotisations salariées sur les bas et moyens salaires du secteur privé
    '''
    taux = taux_alleg_plfrss2014_prive(sal_h_b, _P)
    allegement = taux * salbrut * (
        (type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre'])
        )
    return allegement


def _alleg_plfrss2014_public(salbrut, type_sal, _P):
    '''
    Allègement de cotisations salariées sur les bas et moyens salaires du secteur public
    '''
    taux = taux_alleg_plfrss2014_public(salbrut, _P)
    allegement = taux * salbrut * (
        (type_sal == CAT['public_titulaire_etat'])
        | (type_sal == CAT['public_titulaire_militaire'])
        | (type_sal == CAT['public_titulaire_territoriale'])
        | (type_sal == CAT['public_non_titulaire'])  # TODO: check this category
        )
    return allegement


# Helper functions


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
        "plfrss2014": {
            "@type": "Node",
            "description": "Projet de loi de financement de la sécurité sociale rectificative 2014",
            "children": {
                "exonerations_bas_salaires": {
                    "@type": "Node",
                    "description": "Exonérations de cotisations salariées sur les bas salaires",
                    "children": {
                        "prive": {
                            "@type": "Node",
                            "description": "Salariés du secteur privé",
                            "children": {
                                "taux": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.03}],
                                    },
                                "seuil": {
                                    "@type": "Parameter",
                                    "description": "Seuil (en SMIC)",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 1.3}],
                                    },
                                },
                            },
                        "public": {
                            "@type": "Node",
                            "description": "Salariés du secteur public",
                            "children": {
                                "taux_1": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.02}],
                                    },
                                "seuil_1": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 312}],
                                    },
                                "taux_2": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.018}],
                                    },
                                "seuil_2": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 328}],
                                    },
                                "taux_3": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.016}],
                                    },
                                "seuil_3": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 343}],
                                    },
                                "taux_4": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.014}],
                                    },
                                "seuil_4": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 359}],
                                    },
                                "taux_5": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.012}],
                                    },
                                "seuil_5": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 375}],
                                    },
                                "taux_6": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.01}],
                                    },
                                "seuil_6": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 390}],
                                    },
                                "taux_7": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.008}],
                                    },
                                "seuil_7": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 406}],
                                    },
                                "taux_8": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.007}],
                                    },
                                "seuil_8": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 421}],
                                    },
                                "taux_9": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.006}],
                                    },
                                "seuil_9": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 437}],
                                    },
                                "taux_10": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.005}],
                                    },
                                "seuil_10": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 453}],
                                    },
                                "taux_11": {
                                    "@type": "Parameter",
                                    "description": "Taux",
                                    "format": "rate",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.002}],
                                    },
                                "seuil_11": {
                                    "@type": "Parameter",
                                    "description": "Indice majoré plafond",
                                    "format": "integer",
                                    "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 468}],
                                    },
                                },
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


def taux_alleg_plfrss2014_prive(sal_h_b, P):
    '''
    Exonération de cotisations des salariés du secteur privé PLFRSS2014
    http://www.assemblee-nationale.fr/14/projets/pl2044-ei.asp#P139_9932
    '''
    # La divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    smic_h_b = P.gen.smic_h_b
    seuil = P.plfrss2014.exonerations_bas_salaires.prive.seuil
    taux = P.plfrss2014.exonerations_bas_salaires.prive.taux
    if seuil <= 1:
        return 0
    return (taux * min_(1, max_(seuil * smic_h_b / (sal_h_b + 1e-10) - 1, 0) / (seuil - 1)))


def taux_alleg_plfrss2014_public(salbrut, P):
    '''
    Exonération cotisations des salariés du secteur public PLFRSS2014
    http://www.assemblee-nationale.fr/14/projets/pl2044-ei.asp#P139_9932
    '''
    parametres = P.plfrss2014.exonerations_bas_salaires.public
    alleg = (parametres.taux_1 * (salbrut <= parametres.seuil_1)
             + parametres.taux_2 * (parametres.seuil_1 < salbrut <= parametres.seuil_2)
             + parametres.taux_10 * (parametres.seuil_2 < salbrut <= parametres.seuil_3)
             + parametres.taux_10 * (parametres.seuil_3 < salbrut <= parametres.seuil_4)
             + parametres.taux_10 * (parametres.seuil_4 < salbrut <= parametres.seuil_5)
             + parametres.taux_10 * (parametres.seuil_5 < salbrut <= parametres.seuil_6)
             + parametres.taux_10 * (parametres.seuil_6 < salbrut <= parametres.seuil_7)
             + parametres.taux_10 * (parametres.seuil_7 < salbrut <= parametres.seuil_8)
             + parametres.taux_10 * (parametres.seuil_8 < salbrut <= parametres.seuil_9)
             + parametres.taux_10 * (parametres.seuil_9 < salbrut <= parametres.seuil_10)
             + parametres.taux_11 * (parametres.seuil_10 < salbrut <= parametres.seuil_11)
             )
    return alleg


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
