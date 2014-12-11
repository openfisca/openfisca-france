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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (maximum as max_, logical_not as not_)

from ..base import *


@reference_formula
class br_mv_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressources individuelle du minimum vieillesse/ASPA"
    entity_class = Individus

    def function(self, salnet, chonet, rstnet, alr, rto_declarant1, rpns, rev_cap_bar_holder, rev_cap_lib_holder, rfon_ms, div_ms,
                 revenus_stage_formation_pro, allocation_securisation_professionnelle, prime_forfaitaire_mensuelle_reprise_activite,
                 dedommagement_victime_amiante, prestation_compensatoire, pensions_invalidite, gains_exceptionnels,
                 indemnites_journalieres_maternite, indemnites_journalieres_maladie, indemnites_journalieres_maladie_professionnelle,
                 indemnites_journalieres_accident_travail, indemnites_chomage_partiel, indemnites_volontariat,
                 tns_total_revenus, rsa_base_ressources_patrimoine_i):
        rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

        out = (salnet + chonet + rstnet + alr + rto_declarant1 + rpns +
               max_(0, rev_cap_bar) + max_(0, rev_cap_lib) + max_(0, rfon_ms) + max_(0, div_ms) +
               # max_(0,etr) +
               revenus_stage_formation_pro + allocation_securisation_professionnelle + prime_forfaitaire_mensuelle_reprise_activite +
               dedommagement_victime_amiante + prestation_compensatoire + pensions_invalidite + gains_exceptionnels +
               indemnites_journalieres_maternite + indemnites_journalieres_maladie + indemnites_journalieres_maladie_professionnelle +
               indemnites_journalieres_accident_travail + indemnites_chomage_partiel + indemnites_volontariat + tns_total_revenus +
               rsa_base_ressources_patrimoine_i
               )

        return out

    def get_output_period(self, period):
        return period


@reference_formula
class br_mv(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressource du minimum vieillesse et assimilés (ASPA)"
    entity_class = Familles

    def function(self, br_mv_i_holder):
        br_mv_i = self.split_by_roles(br_mv_i_holder, roles = [CHEF, PART])
        return br_mv_i[CHEF] + br_mv_i[PART]

    def get_output_period(self, period):
        return period


@reference_formula
class aspa_elig(SimpleFormulaColumn):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées"
    entity_class = Individus

    def function(self, age, inv, P = law.minim):
        condition_age = (age >= P.aspa.age_min) | ((age >= P.aah.age_legal_retraite) & inv)
        return condition_age

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class asi_aspa_nb_alloc(SimpleFormulaColumn):
    column = IntCol
    label = u"Nombre d'allocataires ASI/ASPA"
    entity_class = Familles

    def function(self, aspa_elig_holder, asi_elig_holder):
        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        return (1 * aspa_elig[CHEF] + 1 * aspa_elig[PART] + 1 * asi_elig[CHEF] + 1 * asi_elig[PART])

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class asi_elig(SimpleFormulaColumn):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité"
    entity_class = Individus

    def function(self, aspa_elig, inv, activite):
        return inv & (activite >= 3) & not_(aspa_elig)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class asi(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation supplémentaire d'invalidité"
    start_date = date(2007, 1, 1)
    url = u"http://vosdroits.service-public.fr/particuliers/F16940.xhtml"
    entity_class = Familles

    def function(self, asi_elig_holder, aspa_elig_holder, maries, concub, asi_aspa_nb_alloc, br_mv, P = law.minim):
        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (asi_elig[CHEF] | asi_elig[PART]))
        # Couple d'éligibles mariés
        elig2 = (asi_elig[CHEF] & asi_elig[PART]) * maries
        # Couple d'éligibles non mariés
        elig3 = (asi_elig[CHEF] & asi_elig[PART]) * not_(maries)
        # Un seul éligible et époux éligible ASPA
        elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * maries
        # Un seul éligible et conjoint non marié éligible ASPA
        elig5 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * not_(maries)

        elig = elig1 | elig2 | elig3 | elig4 | elig5

        montant_max = (elig1 * P.asi.montant_seul
            + elig2 * P.asi.montant_couple
            + elig3 * 2 * P.asi.montant_seul
            + elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2)
            + elig5 * (P.asi.montant_seul + P.aspa.montant_couple / 2)) / 4

        ressources = br_mv + montant_max

        plafond_ressources = (elig1 * (P.asi.plaf_seul * not_(concub) + P.asi.plaf_couple * concub)
            + elig2 * P.asi.plaf_couple
            + elig3 * P.asi.plaf_couple
            + elig4 * P.aspa.plaf_couple
            + elig5 * P.aspa.plaf_couple) / 4

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2 | elig3) * (montant_max - depassement)
            + elig4 * (P.asi.montant_couple / 4 / 2 - depassement / 2)
            + elig5 * (P.asi.montant_seul / 4 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_asi = max_(diff, 0) / 3

        # TODO: Faute de mieux, on verse l'asi à la famille plutôt qu'aux individus
        # asi[CHEF] = asi_elig[CHEF]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        # asi[PART] = asi_elig[PART]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        return elig * montant_servi_asi

    def get_variable_period(self, output_period, variable_name):
        if variable_name == 'br_mv':
            return output_period.start.period('month', 3).offset(-3)
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class aspa_couple(DatedFormulaColumn):
    column = BoolCol
    label = u"Couple au sens de l'ASPA"
    entity_class = Familles

    @dated_function(date(2002, 1, 1), date(2006, 12, 31))
    def function_2002_2006(self, maries):
        return maries

    @dated_function(date(2007, 1, 1))
    def function_2007(self, concub):
        return concub

    def get_output_period(self, period):
        return period


@reference_formula
class aspa(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation de solidarité aux personnes agées"
    url = "http://vosdroits.service-public.fr/particuliers/F16871.xhtml"

    def function(self, asi_elig_holder, aspa_elig_holder, maries, concub, asi_aspa_nb_alloc, br_mv, P = law.minim):
        # TODO: Avant la réforme de 2007 n'était pas considéré comme un couple les individus en concubinage ou pacsés.
        # La base de ressources doit pouvoir être individualisée pour refletter ça.

        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (aspa_elig[CHEF] | aspa_elig[PART]))
        # Couple d'éligibles
        elig2 = (aspa_elig[CHEF] & aspa_elig[PART])
        # Un seul éligible et époux éligible ASI
        elig3 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * maries
        # Un seul éligible et conjoint non marié éligible ASI
        elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * not_(maries)

        elig = elig1 | elig2 | elig3 | elig4

        # Le montant est divisé par 4 car on calcule l'ASPA sur une base trimestrielle
        montant_max = (elig1 * P.aspa.montant_seul
            + elig2 * P.aspa.montant_couple
            + elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2)
            + elig4 * (P.asi.montant_seul + P.aspa.montant_couple / 2)) / 4

        ressources = br_mv + montant_max

        # Le montant est divisé par 4 car on calcule l'ASPA sur une base trimestrielle
        plafond_ressources = (elig1 * (P.aspa.plaf_seul * not_(concub) + P.aspa.plaf_couple * concub)
            + (elig2 | elig3 | elig4) * P.aspa.plaf_couple) / 4

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2) * (montant_max - depassement)
            + (elig3 | elig4) * (P.aspa.montant_couple / 4 / 2 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_aspa = max_(diff, 0) / 3

        # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
        # aspa[CHEF] = aspa_elig[CHEF]*montant_servi_aspa*(elig1 + elig2/2)
        # aspa[PART] = aspa_elig[PART]*montant_servi_aspa*(elig1 + elig2/2)
        return elig * montant_servi_aspa

    def get_variable_period(self, output_period, variable_name):
        if variable_name == 'br_mv':
            return output_period.start.period('month', 3).offset(-3)
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')
