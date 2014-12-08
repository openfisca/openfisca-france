# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division

from numpy import (zeros, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)
from numpy.core.defchararray import startswith

from openfisca_core.accessors import law
from openfisca_core.columns import BoolCol, FloatCol, EnumCol, reference_input_variable
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import SimpleFormulaColumn

from .base import QUIFAM, QUIFOY, reference_formula
from .pfam import nb_enf
from ..entities import Familles, Individus


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']

SCOLARITE_INCONNUE = 0
SCOLARITE_COLLEGE = 1
SCOLARITE_LYCEE = 2


reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        ),
    entity_class = Individus,
    label = u"Scolarité de l'enfant : collège, lycée...",
    name = "scolarite",
    )


@reference_formula
class base_ressource_bourse_college_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources de l'individu prise en compte pour la bourse de collège"
    entity_class = Individus

    def function(self, salnet):
        return salnet

    def get_variable_period(self, output_period, variable_name):
        if variable_name == 'salnet':
            return output_period.offset(-1)
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class base_ressource_bourse_college(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources prise en compte pour la bourse de collège"
    entity_class = Familles

    def function(self, base_ressource_bourse_college_i_holder):
        base_ressource_bourse_college_i = self.split_by_roles(base_ressource_bourse_college_i_holder, roles = [CHEF, PART])
        return base_ressource_bourse_college_i[CHEF] + base_ressource_bourse_college_i[PART]

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class bourse_college(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant de la bourse de collège"
    entity_class = Familles

    def function(self, base_ressource_bourse_college, age_holder, smic55_holder, scolarite_holder, P = law.bourses_education.bourse_college):
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        nb_enfants = nb_enf(age, smic55, 0, 25)

        plafond_taux_1 = P.plafond_taux_1 + P.plafond_taux_1 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_2 = P.plafond_taux_2 + P.plafond_taux_2 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_3 = P.plafond_taux_3 + P.plafond_taux_3 * nb_enfants * P.coeff_enfant_supplementaire

        eligible_taux_3 = base_ressource_bourse_college < plafond_taux_3
        eligible_taux_2 = not_(eligible_taux_3) * (base_ressource_bourse_college < plafond_taux_2)
        eligible_taux_1 = not_(or_(eligible_taux_2, eligible_taux_3)) * (base_ressource_bourse_college < plafond_taux_1)

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)
        nb_enfants_college = zeros(1)
        for key, scolarite in scolarites.iteritems():
            nb_enfants_college += scolarite == SCOLARITE_COLLEGE

        montant = (
            eligible_taux_3 * P.montant_taux_3 +
            eligible_taux_2 * P.montant_taux_2 +
            eligible_taux_1 * P.montant_taux_1
            )

        montant *= nb_enfants_college

        return montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
