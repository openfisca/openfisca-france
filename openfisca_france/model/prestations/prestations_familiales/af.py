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

from numpy import round, maximum as max_, logical_not as not_, logical_or as or_


from ...base import *  # noqa analysis:ignore
from .base_ressource import nb_enf

@reference_formula
class af_enfant_a_charge(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge au sens des allocations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        smic55 = simulation.calculate('smic55', period)
        age = simulation.calculate('age', period)
        rempli_obligation_scolaire = simulation.calculate('rempli_obligation_scolaire', period)

        pfam = simulation.legislation_at(period.start).fam

        condition_enfant = ((age >= pfam.enfants.age_minimal) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.af.age3) * not_(smic55)

        return period, or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


@reference_formula
class af_nbenf(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales"

    def function(self, simulation, period):
        period_mois = period.start.offset('first-of', 'month').period('month')

        af_enfant_a_charge_holder = simulation.compute('af_enfant_a_charge', period_mois)
        af_nbenf = self.sum_by_entity(af_enfant_a_charge_holder)

        return period, af_nbenf


@reference_formula
class af_eligibilite_base(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Allocations familiales - Éligibilité pour la France métropolitaine sous condition de ressources"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        residence_dom = simulation.calculate('residence_dom', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        return period, not_(residence_dom) * (af_nbenf >= 2)


@reference_formula
class af_eligibilite_dom(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Allocations familiales - Éligibilité pour les DOM (hors Mayotte) sous condition de ressources"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        residence_dom = simulation.calculate('residence_dom', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        return period, residence_dom * not_(residence_mayotte) * (af_nbenf >= 1)


@reference_formula
class af_base(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - allocation de base"
    # prestations familiales (brutes de crds)

    @dated_function(start = date(2002, 1, 1))
    def function_2002(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        eligibilite_base = simulation.calculate('af_eligibilite_base', period)
        eligibilite_dom = simulation.calculate('af_eligibilite_dom', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        pfam = simulation.legislation_at(period.start).fam

        eligibilite = or_(eligibilite_base, eligibilite_dom)

        un_seul_enfant = eligibilite_dom * (af_nbenf == 1) * pfam.af.taux.enf_seul
        plus_de_deux_enfants = (af_nbenf >= 2) * pfam.af.taux.enf2
        plus_de_trois_enfants = max_(af_nbenf - 2, 0) * pfam.af.taux.enf3
        taux_total = un_seul_enfant + plus_de_deux_enfants + plus_de_trois_enfants

        return period, eligibilite * round(pfam.af.bmaf * taux_total, 2)

#    @dated_function(start = date(2015, 7, 1))
#    def function_2015(self, simulation, period):
#        period = period.start.offset('first-of', 'month').period('month')
#
#        af_nbenf = simulation.calculate('af_nbenf', period)
#        br_pf = simulation.calculate('br_pf', period) / 12
#
#        legislation_af = simulation.legislation_at(period.start).fam.af
#        bmaf = legislation_af.bmaf
#        modulation = legislation_af.modulation
#
#        af_1enf = round(bmaf * legislation_af.taux.enf1, 2)
#        af_2enf = round(bmaf * legislation_af.taux.enf2, 2)
#        af_enf_supp = round(bmaf * legislation_af.taux.enf3, 2)
#
#        montant_base = (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + max_(af_nbenf - 2, 0) * af_enf_supp
#
#        plafond1 = modulation.plafond1 + (max_(af_nbenf - 2, 0)) * modulation.enfant_supp
#        plafond2 = modulation.plafond2 + (max_(af_nbenf - 2, 0)) * modulation.enfant_supp
#
#        depassement_plafond1 = max_(br_pf - plafond1, 0)
#        depassement_plafond2 = max_(br_pf - plafond2, 0)
#
#        montant_servi = (montant_base -
#            (br_pf > plafond1) * min_(depassement_plafond1, montant_base * modulation.taux1) -
#            (br_pf > plafond2) * min_(depassement_plafond2, montant_base * modulation.taux2)
#            )
#
#        return period, montant_servi


@reference_formula
class af_age_aine(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Allocations familiales - Âge de l'aîné des enfants éligibles"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        age_holder = simulation.compute('age', period)
        age_enfants = self.split_by_roles(age_holder, roles = ENFS)

        af_enfant_a_charge_holder = simulation.compute('af_enfant_a_charge', period)
        af_enfants_a_charge = self.split_by_roles(af_enfant_a_charge_holder, roles = ENFS)

        pfam = simulation.legislation_at(period.start).fam

        # Calcul de l'âge de l'aîné
        age_aine = -9999
        for key, age in age_enfants.iteritems():
            a_charge = af_enfants_a_charge[key] * (age <= pfam.af.age2)
            aine_potentiel = a_charge * (age > age_aine)
            age_aine = aine_potentiel * age + not_(aine_potentiel) * age_aine
        
        return period, age_aine


@reference_formula
class af_majoration_enfant(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations familiales - Majoration pour âge applicable à l'enfant"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        af_enfant_a_charge = simulation.calculate('af_enfant_a_charge', period)
        age = simulation.calculate('age', period)
        age_aine_holder = simulation.compute('af_age_aine', period)
        age_aine = self.cast_from_entity_to_roles(age_aine_holder, roles = ENFS)
        af_nbenf_holder = simulation.compute('af_nbenf', period)
        af_nbenf = self.cast_from_entity_to_roles(af_nbenf_holder, roles = ENFS)
        af_base_holder = simulation.compute('af_base', period)
        af_base = self.cast_from_entity_to_roles(af_base_holder, roles = ENFS)

        pfam = simulation.legislation_at(period.start).fam

        montant_enfant_seul = pfam.af.bmaf * (
            (pfam.af.maj_age_un_enfant.age1 <= age) * (age < pfam.af.maj_age_un_enfant.age2) * pfam.af.maj_age_un_enfant.taux1 +
            (pfam.af.maj_age_un_enfant.age2 <= age) * pfam.af.maj_age_un_enfant.taux2
            )

        montant_plusieurs_enfants = pfam.af.bmaf * (
            (pfam.af.maj_age_deux_enfants.age1 <= age) * (age < pfam.af.maj_age_deux_enfants.age2) * pfam.af.maj_age_deux_enfants.taux1 +
            (pfam.af.maj_age_deux_enfants.age2 <= age) * pfam.af.maj_age_deux_enfants.taux2
            )

        montant = (af_nbenf == 1) * montant_enfant_seul + (af_nbenf > 1) * montant_plusieurs_enfants

        # Attention ! Ne fonctionne pas pour les enfants du même âge (typiquement les jumeaux...)
        pas_aine = or_(af_nbenf != 2, (af_nbenf == 2) * not_(age == age_aine))

        return period, af_enfant_a_charge * (af_base > 0) * pas_aine * montant


@reference_formula
class af_majo(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - majoration pour âge"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_majoration_enfant_holder = simulation.compute('af_majoration_enfant', period)
        af_majoration_enfants = self.sum_by_entity(af_majoration_enfant_holder, roles = ENFS)
        return period, af_majoration_enfants


@reference_formula
class af_forf(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - forfait"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        smic55_holder = simulation.compute('smic55', period)
        P = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        bmaf = P.bmaf
        nbenf_forf = nb_enf(age, smic55, P.age3, P.age3)
        af_forfait = round(bmaf * P.taux.forfait, 2)
        return period, ((af_nbenf >= 2) * nbenf_forf) * af_forfait


@reference_formula
class af(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - total des allocations"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_base = simulation.calculate('af_base', period)
        af_majo = simulation.calculate('af_majo', period)
        af_forf = simulation.calculate('af_forf', period)

        return period, af_base + af_majo + af_forf
