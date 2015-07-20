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

from numpy import abs as abs_, logical_not as not_, logical_or as or_, maximum as max_

from ...base import *  # noqa analysis:ignore


reference_input_variable(
    name = "inapte_travail",
    column = BoolCol,
    entity_class = Individus,
    label = u"Reconnu inapte au travail",
    )

reference_input_variable(
    name = "taux_invalidite",
    column = FloatCol,
    entity_class = Individus,
    label = u"Taux d'invalidité",
    )


@reference_formula
class br_mv_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressources individuelle du minimum vieillesse/ASPA"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        three_previous_months = period.start.period('month', 3).offset(-3)
        aspa_elig = simulation.calculate('aspa_elig', period)
        aspa_couple_holder = simulation.compute('aspa_couple', period)
        salaire_de_base = simulation.calculate_add('salaire_de_base', three_previous_months)
        chonet = simulation.calculate_add('chonet', three_previous_months)
        rstbrut = simulation.calculate_add('rstbrut', three_previous_months)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', three_previous_months)
        pensions_alimentaires_versees_individu = simulation.calculate(
            'pensions_alimentaires_versees_individu', three_previous_months
            )
        rto_declarant1 = simulation.calculate_add('rto_declarant1', three_previous_months)
        rpns = simulation.calculate_add_divide('rpns', three_previous_months)
        rev_cap_bar_holder = simulation.compute_add_divide('rev_cap_bar', three_previous_months)
        rev_cap_lib_holder = simulation.compute_add_divide('rev_cap_lib', three_previous_months)
        rfon_ms = simulation.calculate_add_divide('rfon_ms', three_previous_months)
        div_ms = simulation.calculate_add_divide('div_ms', three_previous_months)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', three_previous_months)
        allocation_securisation_professionnelle = simulation.calculate(
            'allocation_securisation_professionnelle', three_previous_months
            )
        prime_forfaitaire_mensuelle_reprise_activite = simulation.calculate(
            'prime_forfaitaire_mensuelle_reprise_activite', three_previous_months
            )
        dedommagement_victime_amiante = simulation.calculate('dedommagement_victime_amiante', three_previous_months)
        prestation_compensatoire = simulation.calculate('prestation_compensatoire', three_previous_months)
        pensions_invalidite = simulation.calculate('pensions_invalidite', three_previous_months)
        gains_exceptionnels = simulation.calculate('gains_exceptionnels', three_previous_months)
        indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', three_previous_months)
        indemnites_journalieres = simulation.calculate('indemnites_journalieres', three_previous_months)
        indemnites_volontariat = simulation.calculate('indemnites_volontariat', three_previous_months)
        tns_total_revenus_net = simulation.calculate_add('tns_total_revenus_net', three_previous_months)
        rsa_base_ressources_patrimoine_i = simulation.calculate_add(
            'rsa_base_ressources_patrimoine_i', three_previous_months
            )
        aah = simulation.calculate_add('aah', three_previous_months)
        legislation = simulation.legislation_at(period.start)
        leg_1er_janvier = simulation.legislation_at(period.start.offset('first-of', 'year'))

        aspa_couple = self.cast_from_entity_to_role(aspa_couple_holder, role = VOUS)
        rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

        # Inclus l'AAH si conjoint non pensionné ASPA, retraite et pension invalidité
        # FIXME Il faudrait vérifier que le conjoint est pensionné ASPA, pas qu'il est juste éligible !
        aah = aah * not_(aspa_elig)

        # Abattement sur les salaires (appliqué sur une base trimestrielle)
        abattement_forfaitaire_base = (
            leg_1er_janvier.cotsoc.gen.smic_h_b * legislation.minim.aspa.abattement_forfaitaire_nb_h
            )
        abattement_forfaitaire_taux = (aspa_couple * legislation.minim.aspa.abattement_forfaitaire_tx_couple +
            not_(aspa_couple) * legislation.minim.aspa.abattement_forfaitaire_tx_seul
        )
        abattement_forfaitaire = abattement_forfaitaire_base * abattement_forfaitaire_taux
        salaire_de_base = max_(0, salaire_de_base - abattement_forfaitaire)

        return period, (salaire_de_base + chonet + rstbrut + pensions_alimentaires_percues -
               abs_(pensions_alimentaires_versees_individu) + rto_declarant1 + rpns +
               max_(0, rev_cap_bar) + max_(0, rev_cap_lib) + max_(0, rfon_ms) + max_(0, div_ms) +  # max_(0,etr) +
               revenus_stage_formation_pro + allocation_securisation_professionnelle +
               prime_forfaitaire_mensuelle_reprise_activite + dedommagement_victime_amiante + prestation_compensatoire +
               pensions_invalidite + gains_exceptionnels + indemnites_journalieres + indemnites_chomage_partiel +
               indemnites_volontariat + tns_total_revenus_net + rsa_base_ressources_patrimoine_i + aah
               ) / 3


@reference_formula
class br_mv(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressource du minimum vieillesse et assimilés (ASPA)"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        br_mv_i_holder = simulation.compute('br_mv_i', period)
        ass = simulation.calculate_divide('ass', period)

        br_mv_i = self.split_by_roles(br_mv_i_holder, roles = [CHEF, PART])
        return period, ass + br_mv_i[CHEF] + br_mv_i[PART]


@reference_formula
class aspa_elig(SimpleFormulaColumn):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        age = simulation.calculate('age', period)
        inapte_travail = simulation.calculate('inapte_travail', period)
        taux_invalidite = simulation.calculate('taux_invalidite', period)
        P = simulation.legislation_at(period.start).minim
        condition_invalidite = (taux_invalidite > P.aspa.taux_invalidite_aspa_anticipe) + inapte_travail
        condition_age_base = (age >= P.aspa.age_min)
        condition_age_anticipe = (age >= P.aah.age_legal_retraite) * condition_invalidite

        condition_age = condition_age_base + condition_age_anticipe
        return period, condition_age


@reference_formula
class asi_elig(SimpleFormulaColumn):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        last_month = period.start.period('month').offset(-1)

        aspa_elig = simulation.calculate('aspa_elig', period)
        invalide = simulation.calculate('invalide', period)
        rstnet = simulation.calculate('rstnet', last_month)
        pensions_invalidite = simulation.calculate('pensions_invalidite', last_month)

        condition_situation = invalide & not_(aspa_elig)
        condition_pensionnement = (rstnet + pensions_invalidite) > 0

        return period, condition_situation * condition_pensionnement


@reference_formula
class asi_aspa_nb_alloc(SimpleFormulaColumn):
    column = IntCol
    label = u"Nombre d'allocataires ASI/ASPA"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        aspa_elig_holder = simulation.compute('aspa_elig', period)
        asi_elig_holder = simulation.compute('asi_elig', period)

        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        return period, (1 * aspa_elig[CHEF] + 1 * aspa_elig[PART] + 1 * asi_elig[CHEF] + 1 * asi_elig[PART])


@reference_formula
class asi(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"Allocation supplémentaire d'invalidité"
    start_date = date(2007, 1, 1)
    url = u"http://vosdroits.service-public.fr/particuliers/F16940.xhtml"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        asi_elig_holder = simulation.compute('asi_elig', period)
        aspa_elig_holder = simulation.compute('aspa_elig', period)
        maries = simulation.calculate('maries', period)
        concub = simulation.calculate('concub', period)
        asi_aspa_nb_alloc = simulation.calculate('asi_aspa_nb_alloc', period)
        br_mv = simulation.calculate('br_mv', period)
        P = simulation.legislation_at(period.start).minim

        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (asi_elig[CHEF] | asi_elig[PART]))
        # Couple d'éligibles mariés
        elig2 = asi_elig[CHEF] & asi_elig[PART] & maries
        # Couple d'éligibles non mariés
        elig3 = asi_elig[CHEF] & asi_elig[PART] & not_(maries)
        # Un seul éligible et époux éligible ASPA
        elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) & maries
        # Un seul éligible et conjoint non marié éligible ASPA
        elig5 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4 | elig5

        montant_max = (elig1 * P.asi.montant_seul +
            elig2 * P.asi.montant_couple +
            elig3 * 2 * P.asi.montant_seul +
            elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2) +
            elig5 * (P.asi.montant_seul + P.aspa.montant_couple / 2)) / 12

        ressources = br_mv + montant_max

        plafond_ressources = (elig1 * (P.asi.plaf_seul * not_(concub) + P.asi.plaf_couple * concub) +
            elig2 * P.asi.plaf_couple +
            elig3 * P.asi.plaf_couple +
            elig4 * P.aspa.plaf_couple +
            elig5 * P.aspa.plaf_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2 | elig3) * (montant_max - depassement) +
            elig4 * (P.asi.montant_couple / 12 / 2 - depassement / 2) +
            elig5 * (P.asi.montant_seul / 12 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_asi = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'asi à la famille plutôt qu'aux individus
        # asi[CHEF] = asi_elig[CHEF]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        # asi[PART] = asi_elig[PART]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        return period, elig * montant_servi_asi


@reference_formula
class aspa_couple(DatedFormulaColumn):
    column = BoolCol
    label = u"Couple au sens de l'ASPA"
    entity_class = Familles

    @dated_function(date(2002, 1, 1), date(2006, 12, 31))
    def function_2002_2006(self, simulation, period):
        period = period
        maries = simulation.calculate('maries', period)

        return period, maries

    @dated_function(date(2007, 1, 1))
    def function_2007(self, simulation, period):
        period = period
        concub = simulation.calculate('concub', period)

        return period, concub


@reference_formula
class aspa(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Familles
    label = u"Allocation de solidarité aux personnes agées"
    url = "http://vosdroits.service-public.fr/particuliers/F16871.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        asi_elig_holder = simulation.compute('asi_elig', period)
        aspa_elig_holder = simulation.compute('aspa_elig', period)
        maries = simulation.calculate('maries', period)
        concub = simulation.calculate('concub', period)
        asi_aspa_nb_alloc = simulation.calculate('asi_aspa_nb_alloc', period)
        br_mv = simulation.calculate('br_mv', period)
        P = simulation.legislation_at(period.start).minim

        asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (aspa_elig[CHEF] | aspa_elig[PART]))
        # Couple d'éligibles
        elig2 = (aspa_elig[CHEF] & aspa_elig[PART])
        # Un seul éligible et époux éligible ASI
        elig3 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) & maries
        # Un seul éligible et conjoint non marié éligible ASI
        elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4

        montant_max = (
            elig1 * P.aspa.montant_seul +
            elig2 * P.aspa.montant_couple +
            elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2) +
            elig4 * (P.asi.montant_seul + P.aspa.montant_couple / 2)
            ) / 12

        ressources = br_mv + montant_max

        plafond_ressources = (elig1 * (P.aspa.plaf_seul * not_(concub) + P.aspa.plaf_couple * concub) +
            (elig2 | elig3 | elig4) * P.aspa.plaf_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2) * (montant_max - depassement) +
            (elig3 | elig4) * (P.aspa.montant_couple / 12 / 2 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_aspa = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
        # aspa[CHEF] = aspa_elig[CHEF]*montant_servi_aspa*(elig1 + elig2/2)
        # aspa[PART] = aspa_elig[PART]*montant_servi_aspa*(elig1 + elig2/2)
        return period, elig * montant_servi_aspa
