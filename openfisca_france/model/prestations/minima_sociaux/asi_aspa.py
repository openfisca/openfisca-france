# -*- coding: utf-8 -*-

from __future__ import division

from numpy import abs as abs_, logical_not as not_, logical_or as or_, maximum as max_, minimum as min_, where

from openfisca_france.model.base import *  # noqa analysis:ignore


class inapte_travail(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Reconnu inapte au travail"

class taux_incapacite(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Taux d'incapacité"


class asi_aspa_base_ressources_individu(Variable):
    column = FloatCol
    label = u"Base ressources individuelle du minimum vieillesse/ASPA"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        last_year = period.last_year
        three_previous_months = period.last_3_months
        legislation = simulation.legislation_at(period.start)
        leg_1er_janvier = simulation.legislation_at(period.start.offset('first-of', 'year'))



        ressources_incluses = [
            'allocation_securisation_professionnelle',
            'chomage_net',
            'dedommagement_victime_amiante',
            'div_ms',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_volontariat',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_brute',
            'retraite_titre_onereux_declarant1',
            'revenus_fonciers_minima_sociaux',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu',
            'salaire_de_base',
        ]

        def revenus_capitaux():
            rev_cap_bar_holder = simulation.compute_add_divide('rev_cap_bar', three_previous_months)
            rev_cap_lib_holder = simulation.compute_add_divide('rev_cap_lib', three_previous_months)
            rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
            rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
            return max_(0, rev_cap_bar) + max_(0, rev_cap_lib)

        def revenus_tns():
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', three_previous_months)

           # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year) * (3 / 12)
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year) * (3 / 12)
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year) * (3 / 12)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus


        pension_invalidite = (simulation.calculate('pensions_invalidite', period) > 0)
        aspa_eligibilite = simulation.calculate('aspa_eligibilite', period)
        asi_eligibilite = simulation.calculate('asi_eligibilite', period)

        # Inclus l'AAH si conjoint non éligible ASPA, retraite et pension invalidité
        aah = simulation.calculate_add('aah', three_previous_months)
        aah = aah * not_(aspa_eligibilite) * not_(asi_eligibilite) * not_(pension_invalidite)

        pensions_alimentaires_versees = simulation.calculate_add(
            'pensions_alimentaires_versees_individu', three_previous_months
            )

        def abattement_salaire():
            aspa_couple_holder = simulation.compute('aspa_couple', period)
            aspa_couple = self.cast_from_entity_to_roles(aspa_couple_holder)

            # Abattement sur les salaires (appliqué sur une base trimestrielle)
            abattement_forfaitaire_base = (
                leg_1er_janvier.cotsoc.gen.smic_h_b * legislation.cotsoc.gen.nb_heure_travail_mensuel
                )

            taux_abattement_forfaitaire = where(
                aspa_couple,
                legislation.minim.aspa.abattement_forfaitaire_tx_couple,
                legislation.minim.aspa.abattement_forfaitaire_tx_seul
                )

            abattement_forfaitaire = abattement_forfaitaire_base * taux_abattement_forfaitaire
            salaire_de_base = simulation.calculate_add('salaire_de_base', three_previous_months)

            return min_(salaire_de_base, abattement_forfaitaire)


        base_ressources_3_mois = sum(
            max_(0, simulation.calculate_add(ressource_type, three_previous_months))
            for ressource_type in ressources_incluses
            ) + aah + revenus_capitaux() + revenus_tns() - abs_(pensions_alimentaires_versees) - abattement_salaire()

        return period, base_ressources_3_mois / 3


class asi_aspa_base_ressources(Variable):
    column = FloatCol
    label = u"Base ressource du minimum vieillesse et assimilés (ASPA)"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        asi_aspa_base_ressources_i_holder = simulation.compute('asi_aspa_base_ressources_individu', period)
        ass = simulation.calculate('ass', period)

        asi_aspa_base_ressources_i = self.split_by_roles(asi_aspa_base_ressources_i_holder, roles = [CHEF, PART])
        return period, ass + asi_aspa_base_ressources_i[CHEF] + asi_aspa_base_ressources_i[PART]


class aspa_eligibilite(Variable):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month

        age = simulation.calculate('age', period)
        inapte_travail = simulation.calculate('inapte_travail', period)
        taux_incapacite = simulation.calculate('taux_incapacite', period)
        P = simulation.legislation_at(period.start).minim
        condition_invalidite = (taux_incapacite > P.aspa.taux_incapacite_aspa_anticipe) + inapte_travail
        condition_age_base = (age >= P.aspa.age_min)
        condition_age_anticipe = (age >= P.aah.age_legal_retraite) * condition_invalidite
        condition_age = condition_age_base + condition_age_anticipe
        condition_nationalite = simulation.calculate('asi_aspa_condition_nationalite', period)

        return period, condition_age * condition_nationalite


class asi_eligibilite(Variable):
    column = BoolCol
    label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        last_month = period.start.period('month').offset(-1)

        non_eligible_aspa = not_(simulation.calculate('aspa_eligibilite', period))
        touche_pension_invalidite = simulation.calculate('pensions_invalidite', period) > 0
        handicap = simulation.calculate('handicap', period)
        touche_retraite = simulation.calculate('retraite_nette', last_month) > 0
        condition_nationalite = simulation.calculate('asi_aspa_condition_nationalite', period)

        eligible = (
            non_eligible_aspa *
            condition_nationalite *
            (handicap * touche_retraite + touche_pension_invalidite)
            )

        return period, eligible


class asi_aspa_condition_nationalite(Variable):
    column = BoolCol
    label = u"Condition de nationnalité et de titre de séjour pour bénéficier de l'ASPA ou l'ASI"
    entity_class = Individus

    def function(self, simulation, period):
        ressortissant_eee = simulation.calculate('ressortissant_eee', period)
        duree_possession_titre_sejour= simulation.calculate('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = simulation.legislation_at(period.start).minim.aspa.duree_min_titre_sejour

        return period, or_(ressortissant_eee, duree_possession_titre_sejour >= duree_min_titre_sejour)


class asi_aspa_nb_alloc(Variable):
    column = IntCol
    label = u"Nombre d'allocataires ASI/ASPA"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        aspa_elig_holder = simulation.compute('aspa_eligibilite', period)
        asi_elig_holder = simulation.compute('asi_eligibilite', period)

        asi_eligibilite = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_eligibilite = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        return period, (1 * aspa_eligibilite[CHEF] + 1 * aspa_eligibilite[PART] + 1 * asi_eligibilite[CHEF] + 1 * asi_eligibilite[PART])


class asi(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"Allocation supplémentaire d'invalidité"
    start_date = date(2007, 1, 1)
    url = u"http://vosdroits.service-public.fr/particuliers/F16940.xhtml"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        asi_elig_holder = simulation.compute('asi_eligibilite', period)
        aspa_elig_holder = simulation.compute('aspa_eligibilite', period)
        maries = simulation.calculate('maries', period)
        en_couple = simulation.calculate('en_couple', period)
        asi_aspa_nb_alloc = simulation.calculate('asi_aspa_nb_alloc', period)
        base_ressources = simulation.calculate('asi_aspa_base_ressources', period)
        P = simulation.legislation_at(period.start).minim

        asi_eligibilite = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_eligibilite = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (asi_eligibilite[CHEF] | asi_eligibilite[PART]))
        # Couple d'éligibles mariés
        elig2 = asi_eligibilite[CHEF] & asi_eligibilite[PART] & maries
        # Couple d'éligibles non mariés
        elig3 = asi_eligibilite[CHEF] & asi_eligibilite[PART] & not_(maries)
        # Un seul éligible et époux éligible ASPA
        elig4 = ((asi_eligibilite[CHEF] & aspa_eligibilite[PART]) | (asi_eligibilite[PART] & aspa_eligibilite[CHEF])) & maries
        # Un seul éligible et conjoint non marié éligible ASPA
        elig5 = ((asi_eligibilite[CHEF] & aspa_eligibilite[PART]) | (asi_eligibilite[PART] & aspa_eligibilite[CHEF])) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4 | elig5

        montant_max = (elig1 * P.asi.montant_seul +
            elig2 * P.asi.montant_couple +
            elig3 * 2 * P.asi.montant_seul +
            elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2) +
            elig5 * (P.asi.montant_seul + P.aspa.montant_couple / 2)) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (elig1 * (P.asi.plaf_seul * not_(en_couple) + P.asi.plaf_couple * en_couple) +
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
        # asi[CHEF] = asi_eligibilite[CHEF]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        # asi[PART] = asi_eligibilite[PART]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        return period, elig * montant_servi_asi


class aspa_couple(DatedVariable):
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
        en_couple = simulation.calculate('en_couple', period)

        return period, en_couple


class aspa(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Familles
    label = u"Allocation de solidarité aux personnes agées"
    url = "http://vosdroits.service-public.fr/particuliers/F16871.xhtml"

    def function(self, simulation, period):
        period = period.this_month
        asi_elig_holder = simulation.compute('asi_eligibilite', period)
        aspa_elig_holder = simulation.compute('aspa_eligibilite', period)
        maries = simulation.calculate('maries', period)
        en_couple = simulation.calculate('en_couple', period)
        asi_aspa_nb_alloc = simulation.calculate('asi_aspa_nb_alloc', period)
        base_ressources = simulation.calculate('asi_aspa_base_ressources', period)
        P = simulation.legislation_at(period.start).minim

        asi_eligibilite = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
        aspa_eligibilite = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (aspa_eligibilite[CHEF] | aspa_eligibilite[PART]))
        # Couple d'éligibles
        elig2 = (aspa_eligibilite[CHEF] & aspa_eligibilite[PART])
        # Un seul éligible et époux éligible ASI
        elig3 = ((asi_eligibilite[CHEF] & aspa_eligibilite[PART]) | (asi_eligibilite[PART] & aspa_eligibilite[CHEF])) & maries
        # Un seul éligible et conjoint non marié éligible ASI
        elig4 = ((asi_eligibilite[CHEF] & aspa_eligibilite[PART]) | (asi_eligibilite[PART] & aspa_eligibilite[CHEF])) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4

        montant_max = (
            elig1 * P.aspa.montant_seul +
            elig2 * P.aspa.montant_couple +
            elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2) +
            elig4 * (P.asi.montant_seul + P.aspa.montant_couple / 2)
            ) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (elig1 * (P.aspa.plaf_seul * not_(en_couple) + P.aspa.plaf_couple * en_couple) +
            (elig2 | elig3 | elig4) * P.aspa.plaf_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2) * (montant_max - depassement) +
            (elig3 | elig4) * (P.aspa.montant_couple / 12 / 2 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_aspa = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
        # aspa[CHEF] = aspa_eligibilite[CHEF]*montant_servi_aspa*(elig1 + elig2/2)
        # aspa[PART] = aspa_eligibilite[PART]*montant_servi_aspa*(elig1 + elig2/2)
        return period, elig * montant_servi_aspa
