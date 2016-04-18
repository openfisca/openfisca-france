# -*- coding: utf-8 -*-

from __future__ import division

from functools import partial

from numpy import (absolute as abs_, apply_along_axis, array, int32, logical_not as not_, logical_or as or_,
                   maximum as max_, minimum as min_, select)

from ...base import *  # noqa analysis:ignore


class acs_montant(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Montant de l'ACS en cas d'éligibilité"

    @dated_function(start = date(2009, 8, 1))
    def function_2009(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        P = simulation.legislation_at(period.start).cmu

        ages_couple = self.split_by_roles(age_holder, roles = [CHEF, PART])
        ages_pac = self.split_by_roles(age_holder, roles = ENFS)

        return period, ((nb_par_age(ages_couple, 0, 15) + nb_par_age(ages_pac, 0, 15)) * P.acs_moins_16_ans +
            (nb_par_age(ages_couple, 16, 49) + nb_par_age(ages_pac, 16, 25)) * P.acs_16_49_ans +
            nb_par_age(ages_couple, 50, 59) * P.acs_50_59_ans +
            nb_par_age(ages_couple, 60, 200) * P.acs_plus_60_ans)


class cmu_forfait_logement_base(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Forfait logement applicable en cas de propriété ou d'occupation à titre gratuit"

    def function(self, simulation, period):
        period = period.this_month
        cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu.forfait_logement
        law_rsa = simulation.legislation_at(period.start).minim.rmi

        return period, forfait_logement(cmu_nbp_foyer, P, law_rsa)


class cmu_forfait_logement_al(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Forfait logement applicable en cas d'aide au logement"

    def function(self, simulation, period):
        period = period.this_month
        cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu.forfait_logement_al
        law_rsa = simulation.legislation_at(period.start).minim.rmi

        return period, forfait_logement(cmu_nbp_foyer, P, law_rsa)


class cmu_nbp_foyer(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Familles
    label = u"Nombre de personnes dans le foyer CMU"

    def function(self, simulation, period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        cmu_nb_pac = simulation.calculate('cmu_nb_pac', period)

        return period, nb_parents + cmu_nb_pac


class cmu_eligible_majoration_dom(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        residence_guadeloupe = simulation.calculate('residence_guadeloupe', period)
        residence_martinique = simulation.calculate('residence_martinique', period)
        residence_guyane = simulation.calculate('residence_guyane', period)
        residence_reunion = simulation.calculate('residence_reunion', period)

        return period, residence_guadeloupe | residence_martinique | residence_guyane | residence_reunion


class cmu_c_plafond(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond annuel de ressources pour l'éligibilité à la CMU-C"

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        alt_holder = simulation.compute('garde_alternee', period)
        cmu_eligible_majoration_dom = simulation.calculate('cmu_eligible_majoration_dom', period)
        # cmu_nbp_foyer = simulation.calculate('cmu_nbp_foyer', period)
        P = simulation.legislation_at(period.start).cmu

        PAC = [PART] + ENFS

        # Calcul du coefficient personnes à charge, avec prise en compte de la garde alternée

        # Tableau des coefficients
        coefficients_array = array(
            [P.coeff_p2, P.coeff_p3_p4, P.coeff_p3_p4] + [P.coeff_p5_plus] * (len(PAC) - 3)
            )

        # Tri des personnes à charge, le conjoint en premier, les enfants par âge décroissant
        age_by_role = self.split_by_roles(age_holder, roles = PAC)
        alt_by_role = self.split_by_roles(alt_holder, roles = PAC)

        age_and_alt_matrix = array(
            [
                (role == PART) * 10000 + age_by_role[role] * 10 + alt_by_role[role] - (age_by_role[role] < 0) * 999999
                for role in sorted(age_by_role)
                ]
            ).transpose()

        # Calcul avec matrices intermédiaires
        reverse_sorted = partial(sorted, reverse = True)

        sorted_age_and_alt_matrix = apply_along_axis(reverse_sorted, 1, age_and_alt_matrix)
        # Calcule weighted_alt_matrix, qui vaut 0.5 pour les enfants en garde alternée, 1 sinon.
        sorted_present_matrix = sorted_age_and_alt_matrix >= 0
        sorted_alt_matrix = (sorted_age_and_alt_matrix % 10) * sorted_present_matrix
        weighted_alt_matrix = sorted_present_matrix - sorted_alt_matrix * 0.5

        # Calcul final du coefficient
        coeff_pac = weighted_alt_matrix.dot(coefficients_array)

        return period, (P.plafond_base *
            (1 + cmu_eligible_majoration_dom * P.majoration_dom) *
            (1 + coeff_pac)
            )


class acs_plafond(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond annuel de ressources pour l'éligibilité à l'ACS"

    def function(self, simulation, period):
        period = period.this_month
        cmu_c_plafond = simulation.calculate('cmu_c_plafond', period)
        P = simulation.legislation_at(period.start).cmu

        return period, cmu_c_plafond * (1 + P.majoration_plafond_acs)


class cmu_base_ressources_individu(Variable):
    column = FloatCol
    label = u"Base de ressources de l'individu prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_year = period.last_year
        last_month = period.last_month

        salaire_net = simulation.calculate_add('salaire_net', previous_year)
        chomage_net = simulation.calculate('chomage_net', previous_year)
        retraite_nette = simulation.calculate('retraite_nette', previous_year)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        pensions_alimentaires_versees_individu = simulation.calculate(
            'pensions_alimentaires_versees_individu', previous_year
            )
        rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_individu', previous_year)
        aah = simulation.calculate_add('aah', previous_year)
        indemnites_journalieres = simulation.calculate('indemnites_journalieres', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro_annee = simulation.calculate('revenus_stage_formation_pro', previous_year)
        allocation_securisation_professionnelle = simulation.calculate(
            'allocation_securisation_professionnelle', previous_year
            )
        prime_forfaitaire_mensuelle_reprise_activite = simulation.calculate(
            'prime_forfaitaire_mensuelle_reprise_activite', previous_year
            )
        dedommagement_victime_amiante = simulation.calculate('dedommagement_victime_amiante', previous_year)
        prestation_compensatoire = simulation.calculate('prestation_compensatoire', previous_year)
        retraite_combattant = simulation.calculate('retraite_combattant', previous_year)
        pensions_invalidite = simulation.calculate('pensions_invalidite', previous_year)
        indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', previous_year)
        bourse_enseignement_sup = simulation.calculate('bourse_enseignement_sup', previous_year)
        bourse_recherche = simulation.calculate('bourse_recherche', previous_year)
        gains_exceptionnels = simulation.calculate('gains_exceptionnels', previous_year)
        revenus_stage_formation_pro_last_month = simulation.calculate('revenus_stage_formation_pro', last_month)
        chomage_last_month = simulation.calculate('chomage_net', last_month)

        def revenus_tns():
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', previous_year)

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        P = simulation.legislation_at(period.start).cmu

        # Revenus de stage de formation professionnelle exclus si plus perçus depuis 1 mois
        revenus_stage_formation_pro = revenus_stage_formation_pro_annee * (revenus_stage_formation_pro_last_month > 0)

        # Abattement sur revenus d'activité si chômage ou formation professionnelle
        abattement_chomage_fp = or_(chomage_last_month > 0, revenus_stage_formation_pro_last_month > 0)

        return period, ((salaire_net + indemnites_chomage_partiel) * (1 - abattement_chomage_fp * P.abattement_chomage) +
            indemnites_stage + aah + chomage_net + retraite_nette + pensions_alimentaires_percues -
            abs_(pensions_alimentaires_versees_individu) + rsa_base_ressources_patrimoine_i +
            allocation_securisation_professionnelle + indemnites_journalieres +
            prime_forfaitaire_mensuelle_reprise_activite + dedommagement_victime_amiante + prestation_compensatoire +
            retraite_combattant + pensions_invalidite + bourse_enseignement_sup + bourse_recherche +
            gains_exceptionnels + revenus_tns() + revenus_stage_formation_pro)


class cmu_base_ressources(Variable):
    column = FloatCol
    label = u"Base de ressources prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        previous_year = period.start.period('year').offset(-1)
        aspa = simulation.calculate_add('aspa', previous_year)
        ass = simulation.calculate_add('ass', previous_year)
        asi = simulation.calculate_add('asi', previous_year)
        af = simulation.calculate_add('af', previous_year)
        cf = simulation.calculate_add('cf', previous_year)
        asf = simulation.calculate_add('asf', previous_year)
        paje_clca = simulation.calculate_add('paje_clca', previous_year)
        paje_prepare = simulation.calculate_add('paje_prepare', previous_year)
        aide_logement = simulation.calculate_add('aide_logement', previous_year)
        statut_occupation_logement = simulation.calculate('statut_occupation_logement_famille', period)
        cmu_forfait_logement_base = simulation.calculate('cmu_forfait_logement_base', period)
        cmu_forfait_logement_al = simulation.calculate('cmu_forfait_logement_al', period)
        age_holder = simulation.compute('age', period)
        cmu_base_ressources_i_holder = simulation.compute('cmu_base_ressources_individu', period)
        P = simulation.legislation_at(period.start).cmu

        cmu_br_i_par = self.split_by_roles(cmu_base_ressources_i_holder, roles = [CHEF, PART])
        cmu_br_i_pac = self.split_by_roles(cmu_base_ressources_i_holder, roles = ENFS)

        age_pac = self.split_by_roles(age_holder, roles = ENFS)

        forfait_logement = (((statut_occupation_logement == 2) + (statut_occupation_logement == 6)) * cmu_forfait_logement_base +
            (aide_logement > 0) * min_(cmu_forfait_logement_al, aide_logement))

        res = cmu_br_i_par[CHEF] + cmu_br_i_par[PART] + forfait_logement

        res += (aspa + ass + asi + af + cf + asf)

        res += paje_clca + paje_prepare

        for key, age in age_pac.iteritems():
            res += (0 <= age) * (age <= P.age_limite_pac) * cmu_br_i_pac[key]

        return period, res


class cmu_nb_pac(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Familles
    label = u"Nombre de personnes à charge au titre de la CMU"

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        P = simulation.legislation_at(period.start).cmu

        ages = self.split_by_roles(age_holder, roles = ENFS)
        return period, nb_par_age(ages, 0, P.age_limite_pac)


class cmu_c(Variable):
    '''
    Détermine si le foyer a droit à la CMU complémentaire
    '''
    column = BoolCol
    label = u"Éligibilité à la CMU-C"
    entity_class = Familles

    def function(self, simulation, period):
        # Note : Cette variable est calculée pour un an, mais si elle est demandée pour une période plus petite, elle
        # répond pour la période demandée.
        this_month = period.this_month
        this_rolling_year = this_month.start.period('year')
        if period.stop > this_rolling_year.stop:
            period = this_rolling_year
        else:
            period = this_month

        cmu_c_plafond = simulation.calculate('cmu_c_plafond', this_month)
        cmu_base_ressources = simulation.calculate('cmu_base_ressources', this_month)
        residence_mayotte = simulation.calculate('residence_mayotte', this_month)

        rsa_socle = simulation.calculate('rsa_socle', this_month)
        rsa_socle_majore = simulation.calculate('rsa_socle_majore', this_month)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', this_month)
        rsa_base_ressources = simulation.calculate('rsa_base_ressources', this_month)
        socle = max_(rsa_socle, rsa_socle_majore)
        rsa = simulation.calculate('rsa', this_month)

        eligibilite_basique = cmu_base_ressources <= cmu_c_plafond
        eligibilite_rsa = (rsa > 0) * (rsa_base_ressources < socle - rsa_forfait_logement)

        return period, not_(residence_mayotte) * or_(eligibilite_basique, eligibilite_rsa)


class acs(Variable):
    column = FloatCol
    label = u"Montant (mensuel) de l'ACS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month

        cmu_c = simulation.calculate('cmu_c', period)
        cmu_base_ressources = simulation.calculate('cmu_base_ressources', period)
        acs_plafond = simulation.calculate('acs_plafond', period)
        acs_montant = simulation.calculate('acs_montant', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        return period, not_(residence_mayotte) * not_(cmu_c) * (cmu_base_ressources <= acs_plafond) * acs_montant / 12


############################################################################
# Helper functions
############################################################################


def forfait_logement(nbp_foyer, P, law_rsa):
    '''
    Calcule le forfait logement en fonction du nombre de personnes dans le "foyer CMU" et d'un jeu de taux
    '''
    return 12 * rsa_socle_base(nbp_foyer, law_rsa) * select(
            [nbp_foyer == 1, nbp_foyer == 2, nbp_foyer > 2],
            [P.taux_1p, P.taux_2p, P.taux_3p_plus]
            )

def nb_par_age(age_by_role, min, max):
    '''
    Calcule le nombre d'individus ayant un âge compris entre min et max
    '''
    return sum(
        (min <= age) & (age <= max)
        for age in age_by_role.itervalues()
        )


def rsa_socle_base(nbp, P):
    '''
    Calcule le RSA socle du foyer pour nombre de personnes donné
    '''
    return P.rmi * (1 +
        P.txp2 * (nbp >= 2) +
        P.txp3 * (nbp >= 3) +
        P.txps * max_(0, nbp - 3)
        )
