# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (round, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)

from ...base import *  # noqa analysis:ignore


@reference_formula
class cf_enfant_a_charge(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Complément familial - Enfant considéré à charge"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        smic55 = simulation.calculate('smic55', period)
        age = simulation.calculate('age', period)
        rempli_obligation_scolaire = simulation.calculate('rempli_obligation_scolaire', period)

        pfam = simulation.legislation_at(period.start).fam

        condition_enfant = ((age >= pfam.cf.age1) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.cf.age2) * not_(smic55)

        return period, or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


@reference_formula
class cf_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Complément familial - Ressources de l'individu prises en compte"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        br_pf_i = simulation.calculate('br_pf_i', period)
        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        cf_enfant_a_charge = simulation.calculate('cf_enfant_a_charge', period)

        return period, or_(not_(est_enfant_dans_famille), cf_enfant_a_charge) * br_pf_i


@reference_formula
class cf_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial avant d'éventuels cumuls"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(self, simulation, period):
        """
        Complément familial
        Vous avez au moins 3 enfants à charge tous âgés de plus de 3 ans.
        Vos ressources ne dépassent pas certaines limites.
        Vous avez peut-être droit au Complément Familial à partir du mois
        suivant les 3 ans du 3ème, 4ème, etc. enfant.

        # TODO:
        # En théorie, il faut comparer les revenus de l'année n-2 à la bmaf de
        # l'année n-2 pour déterminer l'éligibilité avec le cf_seuil. Il faudrait
        # pouvoir déflater les revenus de l'année courante pour en tenir compte.
        """
        period = period.start.offset('first-of', 'month').period('month')

        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        cf_ressources_i_holder = simulation.compute('cf_ressources_i', period)
        cf_enfant_a_charge_holder = simulation.compute('cf_enfant_a_charge', period)

        pfam = simulation.legislation_at(period.start).fam
        pfam_n_2 = simulation.legislation_at(period.start.offset(-2, 'year')).fam

        cf_nbenf = self.sum_by_entity(cf_enfant_a_charge_holder)
        ressources = self.sum_by_entity(cf_ressources_i_holder)

        bmaf = pfam.af.bmaf
        bmaf2 = pfam_n_2.af.bmaf

        cf_base_n_2 = pfam.cf.tx * bmaf2
        cf_base = pfam.cf.tx * bmaf

        cf_plaf_tx = 1 + pfam.cf.plaf_tx1 * min_(cf_nbenf, 2) + pfam.cf.plaf_tx2 * max_(cf_nbenf - 2, 0)
        cf_majo = isol | biact
        cf_plaf = pfam.cf.plaf * cf_plaf_tx + pfam.cf.plaf_maj * cf_majo
        cf_plaf2 = cf_plaf + 12 * cf_base_n_2

        cf = (cf_nbenf >= 3) * (
            (ressources <= cf_plaf) * cf_base + (ressources > cf_plaf) * max_(cf_plaf2 - ressources, 0) / 12
            )

        return period, cf


@reference_formula
class cf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.start.offset('first-of', 'month').period('month')
        paje_base_temp = simulation.calculate('paje_base_temp', period)
        apje_temp = simulation.calculate_divide('apje_temp', period)
        ape_temp = simulation.calculate_divide('ape_temp', period)
        cf_temp = simulation.calculate('cf_temp', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        cf_brut = (paje_base_temp < cf_temp) * (apje_temp <= cf_temp) * (ape_temp <= cf_temp) * cf_temp
        return period, not_(residence_mayotte) * round(cf_brut, 2)
