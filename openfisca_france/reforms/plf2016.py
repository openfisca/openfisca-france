# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation
from ..model.base import *


# What if the reform was applied the year before it should

def reform_modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2016 sur revenus 2014",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2014-01-01', 'value': 1165},
                    ],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2014-01-01', 'value': 1920},
                    ],
                },
            },
        }
    reference_legislation_json_copy['children']['plf2016'] = reform_legislation_subtree
    return reference_legislation_json_copy


class plf2016(Reform):
    name = u'Projet de Loi de Finances 2016 appliquée aux revenus 2014'
    # key = 'plf2016'

    class decote(Variable):
        label = u"Décote IR 2016 appliquée en 2015 sur revenus 2014"
        definition_period = YEAR

        # This formula is copy-pasted from the reference decote formula, so that we only change the decote formula for 2014
        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            decote_seuil_celib = simulation.legislation_at(period.start).impot_revenu.decote.seuil_celib
            decote_seuil_couple = simulation.legislation_at(period.start).impot_revenu.decote.seuil_couple
            decote_celib = (ir_plaf_qf < 4 / 3 * decote_seuil_celib) * (decote_seuil_celib - 3 / 4 * ir_plaf_qf)
            decote_couple = (ir_plaf_qf < 4 / 3 * decote_seuil_couple) * (decote_seuil_couple - 3 / 4 * ir_plaf_qf)

            return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

        def formula_2014_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf = simulation.legislation_at(period.start).plf2016

            decote_celib = (ir_plaf_qf < plf.decote_seuil_celib) * (plf.decote_seuil_celib - .75 * ir_plaf_qf)
            decote_couple = (ir_plaf_qf < plf.decote_seuil_couple) * (plf.decote_seuil_couple - .75 * ir_plaf_qf)
            return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    def apply(self):
        self.update_variable(self.decote)
        self.modify_legislation_json(modifier_function = reform_modify_legislation_json)


# Counterfactual ie business as usual

def counterfactual_modify_legislation_json(reference_legislation_json_copy):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflation = .001
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2016 sur revenus 2015",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2016-01-01', },
                    {'start': u'2015-01-01', 'value': round(1135 * (1 + inflation))},
                    ],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2065-01-01', },
                    {'start': u'2015-01-01', 'value': round(1870 * (1 + inflation))},
                    ],
                },
            },
        }
    reference_legislation_json_copy['children']['plf2016_conterfactual'] = reform_legislation_subtree
    return reference_legislation_json_copy

    # WIP : Nouveaux parametres à actualiser :
    # 1° Le 1 est remplacé par les dispositions suivantes :
    # (3) « 1. L'impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède 9 700 € le taux de :
    # (4) « 14 % pour la fraction supérieure à 9 700 € et inférieure ou égale à 26 791 € ;
    # (5) « 30 % pour la fraction supérieure à 26 791 € et inférieure ou égale à 71 826 € ;
    # (6) « 41 % pour la fraction supérieure à 71 826 € et inférieure ou égale à 152 108 € ;
    # (7) « 45 % pour la fraction supérieure à 152 108 €. » ;
    # (8) 2° Au 2 :
    # (9) a) Au premier alinéa, le montant : « 1 508 € » est remplacé par le montant : « 1 510 € » ;
    # (10) b) Au deuxième alinéa, le montant : « 3 558 € » est remplacé par le montant : « 3 562 € » ;
    # (11) c) Au troisième alinéa, le montant : « 901 € » est remplacé par le montant : « 902 € » ;
    # (12) d) Au quatrième alinéa, le montant : « 1 504 € » est remplacé par le montant : « 1 506 € » ;
    # (13) e) Au dernier alinéa, le montant : « 1 680 € » est remplacé par le montant : « 1 682 € » ;
    # (14) 3° Au 4, les mots : « 1 135 € et » sont remplacés par les mots : « 1 165 € et les trois quarts de » et
    # les mots : « 1 870 €
    # et » sont remplacés par les mots : « 1 920 € et les trois quarts de ».
    # (15) II. – Au second alinéa de l'article 196 B du même code, le montant : « 5 726 € » est remplacé par le
    # montant : « 5 732 € ».


class plf2016_counterfactual(Reform):
    name = u'Contrefactuel du PLF 2016 sur les revenus 2015'
    # key = 'plf2016_counterfactual'

    class decote(Variable):
        label = u"Décote IR 2015 appliquée sur revenus 2015 (contrefactuel)"
        definition_period = YEAR

        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            inflator = 1 + .001 + .005
            decote = simulation.legislation_at(period.start).impot_revenu.decote
            assert decote.seuil == 1016
            return (ir_plaf_qf < decote.seuil * inflator) * (decote.seuil * inflator - ir_plaf_qf) * 0.5

    class reduction_impot_exceptionnelle(Variable):
        end = None

        def formula_2015_01_01(self, simulation, period):
            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period.first_month)
            rfr = simulation.calculate('rfr', period)
            inflator = 1 + .001 + .005
            # params = simulation.legislation_at(period.start).impot_revenu.reductions_impots.reduction_impot_exceptionnelle
            seuil = 13795 * inflator
            majoration_seuil = 3536 * inflator
            montant_plafond = 350 * inflator
            plafond = seuil * nb_adult + (nb_parents - nb_adult) * 2 * majoration_seuil
            montant = montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt"
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
        for variable in [self.decote, self.reductions, self.reduction_impot_exceptionnelle]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = counterfactual_modify_legislation_json)


def counterfactual_2014_modify_legislation_json(reference_legislation_json_copy):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflator = 1 + .001 + .005
    reform_year = 2015
    reform_period = periods.period(reform_year)
    # reference_legislation_json_copy = reforms.update_legislation(
    #     legislation_json = reference_legislation_json_copy,
    #     path = ('children', 'ir', 'children', 'reductions_impots', 'children', 'reduction_impot_exceptionnelle',
    #             'children', 'montant_plafond'),
    #     period = reform_period,
    #     value = 350 * inflator,
    #     )
    # reference_legislation_json_copy = reforms.update_legislation(
    #     legislation_json = reference_legislation_json_copy,
    #     path = ('children', 'ir', 'children', 'reductions_impots', 'children', 'reduction_impot_exceptionnelle',
    #             'children', 'seuil'),
    #     period = reform_period,
    #     value = 13795 * inflator,
    #     )
    # reference_legislation_json_copy = reforms.update_legislation(
    #     legislation_json = reference_legislation_json_copy,
    #     path = ('children', 'ir', 'children', 'reductions_impots', 'children', 'reduction_impot_exceptionnelle',
    #             'children', 'majoration_seuil'),
    #     period = reform_period,
    #     value = 3536 * inflator,
    #     )

    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 1, 'threshold'),
        period = reform_period,
        value = 6011 * inflator,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 1, 'rate'),
        period = reform_period,
        value = .055,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 2, 'threshold'),
        period = reform_period,
        value = 11991 * inflator,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 2, 'rate'),
        period = reform_period,
        value = .14,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 3, 'threshold'),
        period = reform_period,
        value = 26631 * inflator,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 3, 'rate'),
        period = reform_period,
        value = .30,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 4, 'threshold'),
        period = reform_period,
        value = 71397 * inflator,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 4, 'rate'),
        period = reform_period,
        value = .40,
        )

    return reference_legislation_json_copy


class plf2016_counterfactual_2014(Reform):
    name = u'Contrefactuel 2014 du PLF 2016 sur les revenus 2015'
    key = 'plf2016_counterfactual_2014'

    class decote(Variable):
        definition_period = YEAR

        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            inflator = 1 + .001 + .005
            decote = simulation.legislation_at(period.start).impot_revenu.decote
            assert decote.seuil == 1016
            return (ir_plaf_qf < decote.seuil * inflator) * (decote.seuil * inflator - ir_plaf_qf) * 0.5

    class reduction_impot_exceptionnelle(Variable):
        end = None

        def formula_2015_01_01(self, simulation, period):
            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period.first_month)
            rfr = simulation.calculate('rfr', period)
            inflator = 1 + .001 + .005
            # params = simulation.legislation_at(period.start).impot_revenu.reductions_impots.reduction_impot_exceptionnelle
            seuil = 13795 * inflator
            majoration_seuil = 3536 * inflator
            montant_plafond = 350 * inflator
            plafond = seuil * nb_adult + (nb_parents - nb_adult) * 2 * majoration_seuil
            montant = montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt"
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
        for variable in [self.decote, self.reduction_impot_exceptionnelle, self.reductions]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = counterfactual_2014_modify_legislation_json)
