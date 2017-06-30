# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date

from openfisca_core import columns
from openfisca_core.reforms import Reform

from .. import entities
from ..model.base import *
from ..model.prelevements_obligatoires.impot_revenu import reductions_impot


# TODO: les baisses de charges n'ont pas été codées car annulées (toute ou en partie ?)
# par le Conseil constitutionnel

class plfr2014(Reform):
    name = u'Projet de Loi de Finances Rectificative 2014'

    class reduction_impot_exceptionnelle(Variable):
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            janvier = period.first_month

            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period = janvier)
            rfr = simulation.calculate('rfr', period)
            params = simulation.legislation_at(period.start).plfr2014.reduction_impot_exceptionnelle
            plafond = params.seuil * nb_adult + (nb_parents - nb_adult) * 2 * params.majoration_seuil
            montant = params.montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt à intégrer pour l'année 2013"
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            accult = simulation.calculate('accult', period)
            adhcga = simulation.calculate('adhcga', period)
            cappme = simulation.calculate('cappme', period)
            creaen = simulation.calculate('creaen', period)
            daepad = simulation.calculate('daepad', period)
            deffor = simulation.calculate('deffor', period)
            dfppce = simulation.calculate('dfppce', period)
            doment = simulation.calculate('doment', period)
            domlog = simulation.calculate('domlog', period)
            donapd = simulation.calculate('donapd', period)
            duflot = simulation.calculate('duflot', period)
            ecpess = simulation.calculate('ecpess', period)
            garext = simulation.calculate('garext', period)
            intagr = simulation.calculate('intagr', period)
            invfor = simulation.calculate('invfor', period)
            invlst = simulation.calculate('invlst', period)
            ip_net = simulation.calculate('ip_net', period)
            locmeu = simulation.calculate('locmeu', period)
            mecena = simulation.calculate('mecena', period)
            mohist = simulation.calculate('mohist', period)
            patnat = simulation.calculate('patnat', period)
            prcomp = simulation.calculate('prcomp', period)
            reduction_impot_exceptionnelle = simulation.calculate('reduction_impot_exceptionnelle', period)
            repsoc = simulation.calculate('repsoc', period)
            resimm = simulation.calculate('resimm', period)
            rsceha = simulation.calculate('rsceha', period)
            saldom = simulation.calculate('saldom', period)
            scelli = simulation.calculate('scelli', period)
            sofica = simulation.calculate('sofica', period)
            spfcpi = simulation.calculate('spfcpi', period)
            total_reductions = accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + \
                donapd + duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat + \
                prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi + reduction_impot_exceptionnelle
            return min_(ip_net, total_reductions)

    def apply(self):
        for variable in [self.reduction_impot_exceptionnelle, self.reductions]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = modify_legislation_json)


def modify_legislation_json(reference_legislation_json_copy):
    plfr2014_legislation_subtree = {
        "type": "node",
        "description": "Projet de loi de finance rectificative 2014",
        "children": {
            "reduction_impot_exceptionnelle": {
                "type": "node",
                "description": "Réduction d'impôt exceptionnelle",
                "children": {
                    "montant_plafond": {
                        "type": "parameter",
                        "description": "Montant plafond par part pour les deux premières parts",
                        "format": "integer",
                        "unit": "currency",
                        "values": [
                            {'start': u'2015-01-01', },
                            {'start': u'2013-01-01', 'value': 350},
                            ],
                        },
                    "seuil": {
                        "type": "parameter",
                        "description": "Seuil (à partir duquel la réduction décroît) par part pour les deux "
                                       "premières parts",
                        "format": "integer",
                        "unit": "currency",
                        "values": [
                            {'start': u'2015-01-01', },
                            {'start': u'2013-01-01', 'value': 13795},
                            ],
                        },
                    "majoration_seuil": {
                        "type": "parameter",
                        "description": "Majoration du seuil par demi-part supplémentaire",
                        "format": "integer",
                        "unit": "currency",
                        "values": [
                            {'start': u'2015-01-01', },
                            {'start': u'2013-01-01', 'value': 3536},
                            ],
                        },
                    },
                },
            },
        }
    plfrss2014_legislation_subtree = {
        "type": "node",
        "description": "Projet de loi de financement de la sécurité sociale rectificative 2014",
        "children": {
            "exonerations_bas_salaires": {
                "type": "node",
                "description": "Exonérations de cotisations salariées sur les bas salaires",
                "children": {
                    "prive": {
                        "type": "node",
                        "description": "Salariés du secteur privé",
                        "children": {
                            "taux": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.03},
                                    ],
                                },
                            "seuil": {
                                "type": "parameter",
                                "description": "Seuil (en SMIC)",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 1.3},
                                    ],
                                },
                            },
                        },
                    "public": {
                        "type": "node",
                        "description": "Salariés du secteur public",
                        "children": {
                            "taux_1": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.02},
                                    ],
                                },
                            "seuil_1": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 312},
                                    ],
                                },
                            "taux_2": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.018},
                                    ],
                                },
                            "seuil_2": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 328},
                                    ],
                                },
                            "taux_3": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.016},
                                    ],
                                },
                            "seuil_3": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 343},
                                    ],
                                },
                            "taux_4": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.014},
                                    ],
                                },
                            "seuil_4": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 359},
                                    ],
                                },
                            "taux_5": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.012},
                                    ],
                                },
                            "seuil_5": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 375},
                                    ],
                                },
                            "taux_6": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.01},
                                    ],
                                },
                            "seuil_6": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 390},
                                    ],
                                },
                            "taux_7": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.008},
                                    ],
                                },
                            "seuil_7": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 406},
                                    ],
                                },
                            "taux_8": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.007},
                                    ],
                                },
                            "seuil_8": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 421},
                                    ],
                                },
                            "taux_9": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.006},
                                    ],
                                },
                            "seuil_9": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 437},
                                    ],
                                },
                            "taux_10": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.005},
                                    ],
                                },
                            "seuil_10": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 453},
                                    ],
                                },
                            "taux_11": {
                                "type": "parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 0.002},
                                    ],
                                },
                            "seuil_11": {
                                "type": "parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [
                                    {'start': u'2015-01-01', },
                                    {'start': u'2014-01-01', 'value': 468},
                                    ],
                                },
                            },
                        },
                    },
                },
            },
        }
    reference_legislation_json_copy['children']['plfr2014'] = plfr2014_legislation_subtree
    reference_legislation_json_copy['children']['plfrss2014'] = plfrss2014_legislation_subtree
    return reference_legislation_json_copy
