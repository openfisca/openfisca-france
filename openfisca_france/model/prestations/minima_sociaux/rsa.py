# -*- coding: utf-8 -*-

from __future__ import division


from numpy import (datetime64, floor, logical_and as and_, logical_not as not_, logical_or as or_, maximum as max_, minimum as min_, select, where)

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf, age_en_mois_benjamin


class rsa_base_ressources(DatedVariable):
    column = FloatCol
    label = u"Base ressources du Rmi ou du Rsa"
    entity = Famille

    @dated_function(stop = date(2009, 5, 31))
    def function_rmi(self, simulation, period):
        period = period.this_month
        rsa_base_ressources_prestations_familiales = simulation.calculate('rsa_base_ressources_prestations_familiales', period)
        rsa_base_ressources_minima_sociaux = simulation.calculate('rsa_base_ressources_minima_sociaux', period)
        rsa_base_ressources_i_holder = simulation.compute('rsa_base_ressources_individu', period)

        rsa_base_ressources_i_total = self.sum_by_entity(rsa_base_ressources_i_holder)
        return period, (
            rsa_base_ressources_prestations_familiales +
            rsa_base_ressources_minima_sociaux +
            rsa_base_ressources_i_total
            )

    @dated_function(start = date(2009, 6, 1))
    def function_rsa(self, simulation, period):
        period = period.this_month
        rsa_base_ressources_prestations_familiales = simulation.calculate(
            'rsa_base_ressources_prestations_familiales', period)
        rsa_base_ressources_minima_sociaux = simulation.calculate('rsa_base_ressources_minima_sociaux', period)

        enfant_i = simulation.calculate('est_enfant_dans_famille', period)
        rsa_enfant_a_charge_i = simulation.calculate('rsa_enfant_a_charge', period)
        ressources_individuelles_i = (
            simulation.calculate('rsa_base_ressources_individu', period) +
            simulation.calculate('rsa_revenu_activite_individu', period)
            )

        ressources_individuelles = self.sum_by_entity(
            (not_(enfant_i) + rsa_enfant_a_charge_i) * ressources_individuelles_i
            )

        return period, (
            rsa_base_ressources_prestations_familiales + rsa_base_ressources_minima_sociaux + ressources_individuelles
            )


class rsa_has_ressources_substitution(Variable):
    column = FloatCol
    label = u"Présence de ressources de substitution au mois M, qui désactivent la neutralisation des revenus professionnels interrompus au moins M."
    entity = Individu

    def function(self, simulation, period):
        period = period.this_month
        return period, (
            simulation.calculate('chomage_net', period.this_month) +
            simulation.calculate('indemnites_journalieres', period.this_month) +
            simulation.calculate('retraite_nette', period.this_month)  # +
            ) > 0


class rsa_base_ressources_individu(Variable):
    column = FloatCol
    label = u"Base ressource individuelle du RSA/RMI (hors revenus d'actvité)"
    entity = Individu

    def function(individu, period, legislation):
        period = period.this_month

        # Revenus professionels
        types_revenus_pros = [
            'chomage_net',
            'retraite_nette',
            ]

        has_ressources_substitution = individu('rsa_has_ressources_substitution', period)

        # Les revenus pros interrompus au mois M sont neutralisés s'il n'y a pas de revenus de substitution.
        revenus_pro = sum(
            individu(type_revenu, period.last_3_months, options = [ADD]) * not_(
                (individu(type_revenu, period.this_month) == 0) *
                (individu(type_revenu, period.last_month) > 0) *
                not_(has_ressources_substitution)
                )
            for type_revenu in types_revenus_pros
            )

        types_revenus_non_pros = [
            'allocation_aide_retour_emploi',
            'allocation_securisation_professionnelle',
            'dedommagement_victime_amiante',
            'div_ms',
            'gains_exceptionnels',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'revenus_fonciers_minima_sociaux',
            'rsa_base_ressources_patrimoine_individu',
            'rsa_indemnites_journalieres_hors_activite',
            ]

        # Les revenus non-pro interrompus au mois M sont neutralisés dans la limite d'un montant forfaitaire,
        # sans condition de revenu de substitution.
        neutral_max_forfaitaire = 3 * legislation(period).prestations.minima_sociaux.rmi.rmi
        revenus_non_pros = sum(
            max_(0, individu(type_revenu, period.last_3_months, options = [ADD]) - neutral_max_forfaitaire * (
                (individu(type_revenu, period.this_month) == 0) *
                (individu(type_revenu, period.last_month) > 0)
                ))
            for type_revenu in types_revenus_non_pros
            )

        # Revenus du foyer fiscal que l'on projette sur le premier invidividus
        rev_cap_bar = max_(0, individu.foyer_fiscal('rev_cap_bar', period.last_3_months, options = [ADD]))
        rev_cap_lib = max_(0, individu.foyer_fiscal('rev_cap_lib', period.last_3_months, options = [ADD]))
        retraite_titre_onereux = individu.foyer_fiscal('retraite_titre_onereux', period.last_3_months, options = [ADD])
        revenus_foyer_fiscal = rev_cap_bar + rev_cap_lib + retraite_titre_onereux
        revenus_foyer_fiscal_projetes = revenus_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return period, (revenus_pro + revenus_non_pros + revenus_foyer_fiscal_projetes) / 3



class rsa_base_ressources_minima_sociaux(Variable):
    column = FloatCol
    label = u"Minima sociaux inclus dans la base ressource RSA/RMI"
    entity = Famille

    def function(self, simulation, period):
        period = period.this_month
        three_previous_months = period.last_3_months
        aspa = simulation.calculate('aspa', period)
        asi = simulation.calculate('asi', period)
        ass = simulation.calculate('ass', period)
        aah_holder = simulation.compute_add('aah', three_previous_months)
        caah_holder = simulation.compute_add('caah', three_previous_months)

        aah = self.sum_by_entity(aah_holder) / 3
        caah = self.sum_by_entity(caah_holder) / 3

        return period, aspa + asi + ass + aah + caah


class rsa_base_ressources_prestations_familiales(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"Prestations familiales inclues dans la base ressource RSA/RMI"

    @dated_function(date(2002, 1, 1), date(2003, 12, 31))
    def function_2002(self, simulation, period):
        period = period.this_month
        prestations = [
            'af_base',
            'cf',
            'asf',
            'apje',
            'ape',
            ]
        result = sum(simulation.calculate(prestation, period) for prestation in prestations)

        return period, result

    @dated_function(start = date(2004, 1, 1), stop = date(2014, 3, 31))
    def function_2003(self, simulation, period):
        period = period.this_month
        prestations = [
            'af_base',
            'cf',
            'asf',
            'paje_base',
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        result = sum(simulation.calculate(prestation, period) for prestation in prestations)

        return period, result

    @dated_function(start = date(2014, 4, 1))
    def function_2014(self, simulation, period):
        # TODO : Neutraliser les ressources de type prestations familiales quand elles sont interrompues
        period = period.this_month

        prestations_calculees = [
            'rsa_forfait_asf',
            'paje_base',
           ]
        prestations_autres = [
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        result = sum(simulation.calculate(prestation, period) for prestation in prestations_calculees)
        result += sum(
            simulation.calculate_add(prestation, period.last_3_months) / 3 for prestation in prestations_autres)

        cf_non_majore_avant_cumul = simulation.calculate('cf_non_majore_avant_cumul', period)
        cf = simulation.calculate('cf', period)
        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul

        af_base = simulation.calculate('af_base', period)
        af = simulation.calculate('af', period)

        result = result + cf_non_majore + min_(af_base, af)  # Si des AF on été injectées et sont plus faibles que le cf

        return period, result


class crds_mini(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"CRDS versée sur les minimas sociaux"

    @dated_function(start = date(2009, 6, 1))
    def function_2009_(self, simulation, period):
        """
        CRDS sur les minima sociaux
        """
        period = period.this_month
        rsa_activite = simulation.calculate('rsa_activite', period)
        taux_crds = simulation.legislation_at(period.start).prelevements_sociaux.contributions.crds.taux

        return period, - taux_crds * rsa_activite


class div_ms(Variable):
    column = FloatCol
    entity = Individu
    label = u"Dividende entrant en compte dans le calcul des minimas sociaux"

    def function(self, simulation, period):
        period = period.this_month
        period_declaration = period.this_year
        f3vc_holder = simulation.compute('f3vc', period_declaration)
        f3ve_holder = simulation.compute('f3ve', period_declaration)
        f3vg_holder = simulation.compute('f3vg', period_declaration)
        f3vl_holder = simulation.compute('f3vl', period_declaration)
        f3vm_holder = simulation.compute('f3vm', period_declaration)
        f3vt_holder = simulation.compute('f3vt', period_declaration)

        f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
        f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
        f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
        f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
        f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)
        f3vt = self.cast_from_entity_to_role(f3vt_holder, role = VOUS)

        return period, (f3vc + f3ve + f3vg + f3vl + f3vm + f3vt) / 12


class enceinte_fam(Variable):
    column = BoolCol
    entity = Famille

    def function(self, simulation, period):
        period = period
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        enceinte_holder = simulation.compute('enceinte', period)

        age_en_mois_enf = self.split_by_roles(age_en_mois_holder, roles = ENFS)
        enceinte = self.split_by_roles(enceinte_holder, roles = [CHEF, PART])

        benjamin = age_en_mois_benjamin(age_en_mois_enf)
        enceinte_compat = and_(benjamin < 0, benjamin > -6)
        return period, or_(or_(enceinte_compat, enceinte[CHEF]), enceinte[PART])


class rsa_enfant_a_charge(Variable):
    column = BoolCol
    entity = Individu
    label = u"Enfant pris en compte dans le calcul du RSA"

    def function(individu, period, legislation):
        period = period.this_month

        P_rsa = legislation(period).prestations.minima_sociaux.rsa
        P_rmi = legislation(period).prestations.minima_sociaux.rmi

        enfant = individu('est_enfant_dans_famille', period)
        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)

        ressources = (
            individu('rsa_base_ressources_individu', period) +
            (1 - P_rsa.pente) * individu('rsa_revenu_activite_individu', period)
            )

        # Les parametres ont changé de nom au moment où le RMI est devenu le RSA
        if period.start.date >= date(2009, 6, 01):
            age_pac = P_rsa.age_pac
            majo_rsa = P_rsa.majo_rsa
            montant_base_rsa = P_rsa.montant_de_base_du_rsa
            taux_personne_supp = P_rsa.majoration_rsa.taux_personne_supp
        else:
            age_pac = P_rmi.age_pac
            majo_rsa = P_rmi.majo_rsa
            montant_base_rsa = P_rmi.rmi
            taux_personne_supp = P_rmi.txps

        # Règle CAF: Si un enfant touche des ressources, et que son impact global
        # (augmentation du montant forfaitaire - ressources prises en compte) fait baisser le montant du RSA, alors
        # il doit être exclu du calcul du RSA.
        # Cette règle est complexe, on applique donc l'approximation suivante:
        #       - Cas général: enfant pris en compte si ressources <= augmentation du MF pour un enfant
        #                      supplémentaire (taux marginal).
        #       - Si la présence de l'enfant ouvre droit au RSA majoré, pris en compte si
        #                      ressources <= majoration du RSA pour isolement avec un enfant.
        def ouvre_droit_majoration():
            famille = individu.famille
            enceinte_fam = famille('enceinte_fam', period)
            isole = not_(famille('en_couple', period))
            isolement_recent = famille('rsa_isolement_recent', period)

            presence_autres_enfants = famille.sum(enfant * not_(autonomie_financiere) * (age <= age_pac)) > 1

            # individu.famille.sum retourne un résultat qui n'est pas implicitement projeté sur l'individu.
            return not_(enceinte_fam) * isole * isolement_recent * not_(famille.project(presence_autres_enfants))

        rsa_enf_charge = enfant * not_(autonomie_financiere) * (age <= age_pac) * where(
            ouvre_droit_majoration(),
            ressources < (majo_rsa.pac0 - 1 + majo_rsa.pac_enf_sup) * montant_base_rsa,
            ressources < taux_personne_supp * montant_base_rsa
            )

        return period, rsa_enf_charge


class rsa_nb_enfants(Variable):
    column = IntCol
    entity = Famille
    label = u"Nombre d'enfants pris en compte pour le calcul du RSA"

    def function(self, simulation, period):
        return period, self.sum_by_entity(simulation.compute('rsa_enfant_a_charge', period))


class participation_frais(Variable):
    column = BoolCol
    entity = Menage
    label = u"Partipation aux frais de logement pour un hebergé à titre gratuit"


class rsa_revenu_activite(Variable):
    column = FloatCol
    label = u"Revenus d'activité du RSA"
    entity = Famille
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.this_month
        rsa_revenu_activite_i = simulation.calculate('rsa_revenu_activite_individu', period)
        rsa_enfant_a_charge_i = simulation.calculate('rsa_enfant_a_charge', period)
        enfant_i = simulation.calculate('est_enfant_dans_famille', period)

        return period, self.sum_by_entity(
            (not_(enfant_i) + rsa_enfant_a_charge_i) * rsa_revenu_activite_i
            )

class rsa_indemnites_journalieres_activite(Variable):
    column = FloatCol
    label = u"Indemnités journalières prises en compte comme revenu d'activité"
    entity = Individu

    def function(self, simulation, period):
        period = period.this_month
        m_3 = period.offset(-3,'month')

        def ijss_activite_sous_condition(period):
            return sum(simulation.calculate(ressource, period) for ressource in [
                # IJSS prises en compte comme un revenu d'activité seulement les 3 premiers mois qui suivent l'arrêt de travail
                'indemnites_journalieres_maladie',
                'indemnites_journalieres_accident_travail',
                'indemnites_journalieres_maladie_professionnelle',
            ])


        date_arret_de_travail = simulation.calculate('date_arret_de_travail')
        three_months_ago = datetime64(m_3.start)
        condition_date_arret_travail = date_arret_de_travail > three_months_ago

        # Si la date d'arrêt de travail n'est pas définie (et vaut donc par défaut date.min), mais qu'il n'y a pas d'IJSS à M-3, on estime que l'arrêt est récent.
        is_date_arret_de_travail_undefined = (date_arret_de_travail == date.min)
        condition_arret_recent = is_date_arret_de_travail_undefined * (ijss_activite_sous_condition(m_3) == 0)

        condition_activite = simulation.calculate('salaire_net', period) > 0

        ijss_activite = sum(simulation.calculate(ressource, period) for ressource in [
            # IJSS toujours prises en compte comme un revenu d'activité
            'indemnites_journalieres_maternite',
            'indemnites_journalieres_paternite',
            'indemnites_journalieres_adoption',
        ]) + (condition_date_arret_travail + condition_activite + condition_arret_recent) * ijss_activite_sous_condition(period)

        return period, ijss_activite

class rsa_indemnites_journalieres_hors_activite(Variable):
    column = FloatCol
    label = u"Indemnités journalières prises en compte comme revenu de remplacement"
    entity = Individu

    def function(self, simulation, period):
        period = period.this_month
        return period, simulation.calculate('indemnites_journalieres', period) - simulation.calculate('rsa_indemnites_journalieres_activite', period)

class rsa_revenu_activite_individu(Variable):
    column = FloatCol
    label = u"Revenus d'activité du Rsa - Individuel"
    entity = Individu
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.this_month
        last_3_months = period.last_3_months

        # Note Auto-entrepreneurs:
        # D'après les caisses, le revenu pris en compte pour les AE pour le RSA ne prend en compte que
        # l'abattement standard sur le CA, mais pas les cotisations pour charges sociales.

        types_revenus_activite = [
            'salaire_net',
            'indemnites_chomage_partiel',
            'indemnites_volontariat',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'hsup',
            'etr',
            'tns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite',
            ]

        has_ressources_substitution = simulation.calculate('rsa_has_ressources_substitution', period)

        # Les revenus pros interrompus au mois M sont neutralisés s'il n'y a pas de revenus de substitution.
        return period, sum(
            simulation.calculate_add(type_revenu, last_3_months) * not_(
                (simulation.calculate(type_revenu, period.this_month) == 0) *
                (simulation.calculate(type_revenu, period.last_month) > 0) *
                not_(has_ressources_substitution)
                )
            for type_revenu in types_revenus_activite
            ) / 3


class revenus_fonciers_minima_sociaux(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenus fonciers pour la base ressource du rmi/rsa"

    def function(self, simulation, period):
        period = period.this_month
        period_declaration = period.this_year
        f4ba_holder = simulation.compute('f4ba', period_declaration)
        f4be_holder = simulation.compute('f4be', period_declaration)

        f4ba = self.cast_from_entity_to_role(f4ba_holder, role = VOUS)
        f4be = self.cast_from_entity_to_role(f4be_holder, role = VOUS)

        return period, (f4ba + f4be) / 12


class rsa(DatedVariable):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"Revenu de solidarité active"
    entity = Famille

    @dated_function(start = date(2009, 06, 1))
    def function(self, simulation, period):
        period = period.this_month
        rsa_majore = simulation.calculate('rsa_majore', period)
        rsa_non_majore = simulation.calculate('rsa_non_majore', period)
        rsa_non_calculable = simulation.calculate('rsa_non_calculable', period)

        rsa = (1 - rsa_non_calculable) * max_(rsa_majore, rsa_non_majore)

        return period, rsa


class rsa_base_ressources_patrimoine_individu(DatedVariable):
    column = FloatCol
    label = u"Base de ressources des revenus du patrimoine du RSA"
    entity = Individu
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1))
    def function_2009_(self, simulation, period):
        period = period.this_month
        interets_epargne_sur_livrets = simulation.calculate('interets_epargne_sur_livrets', period)
        epargne_non_remuneree = simulation.calculate('epargne_non_remuneree', period)
        revenus_capital = simulation.calculate('revenus_capital', period)
        valeur_locative_immo_non_loue = simulation.calculate('valeur_locative_immo_non_loue', period)
        valeur_locative_terrains_non_loue = simulation.calculate('valeur_locative_terrains_non_loue', period)
        revenus_locatifs = simulation.calculate('revenus_locatifs', period)
        rsa = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa

        return period, (
            interets_epargne_sur_livrets / 12 +
            epargne_non_remuneree * rsa.patrimoine.taux_interet_forfaitaire_epargne_non_remunere / 12 +
            revenus_capital +
            valeur_locative_immo_non_loue * rsa.patrimoine.abattement_valeur_locative_immo_non_loue +
            valeur_locative_terrains_non_loue * rsa.patrimoine.abattement_valeur_locative_terrains_non_loue +
            revenus_locatifs
            )


class rsa_condition_nationalite(Variable):
    column = BoolCol
    entity = Individu
    label = u"Conditions de nationnalité et de titre de séjour pour bénéficier du RSA"

    def function(self, simulation, period):
        period = period.this_month
        ressortissant_eee = simulation.calculate('ressortissant_eee', period)
        duree_possession_titre_sejour = simulation.calculate('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa.duree_min_titre_sejour

        return period, or_(ressortissant_eee, duree_possession_titre_sejour >= duree_min_titre_sejour)


class rsa_eligibilite(Variable):
    column = BoolCol
    entity = Famille
    label = u"Eligibilité au RSA"

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        age_parents = self.split_by_roles(age_holder, roles = [CHEF, PART])
        activite_holder = simulation.compute('activite', period)
        activite_parents = self.split_by_roles(activite_holder, roles = [CHEF, PART])
        rsa_nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        rsa_eligibilite_tns = simulation.calculate('rsa_eligibilite_tns', period)
        rsa_condition_nationalite = simulation.compute('rsa_condition_nationalite', period)
        condition_nationalite = self.any_by_roles(rsa_condition_nationalite, roles = [CHEF, PART])
        rmi = simulation.legislation_at(period.start).prestations.minima_sociaux.rmi
        rsa = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa
        age_min = (rsa_nb_enfants == 0) * rsa.age_pac

        eligib = (
            (age_parents[CHEF] > age_min) * not_(activite_parents[CHEF] == 2) +
            (age_parents[PART] > age_min) * not_(activite_parents[PART] == 2)
            )
        eligib = eligib * (
            condition_nationalite *
            rsa_eligibilite_tns
            )

        return period, eligib


class rsa_eligibilite_tns(Variable):
    column = BoolCol
    entity = Famille
    label = u"Eligibilité au RSA pour un travailleur non salarié"

    def function(self, simulation, period):
        period = period.this_month
        last_year = period.last_year

        tns_benefice_exploitant_agricole_holder = simulation.compute('tns_benefice_exploitant_agricole', last_year)
        tns_benefice_exploitant_agricole = self.sum_by_entity(tns_benefice_exploitant_agricole_holder)
        tns_employe_holder = simulation.compute('tns_avec_employe', period)
        tns_avec_employe = self.any_by_roles(tns_employe_holder)
        tns_autres_revenus_chiffre_affaires_holder = simulation.compute(
            'tns_autres_revenus_chiffre_affaires', last_year)
        tns_autres_revenus_chiffre_affaires = self.split_by_roles(tns_autres_revenus_chiffre_affaires_holder)
        tns_autres_revenus_type_activite_holder = simulation.compute('tns_autres_revenus_type_activite', period)
        tns_autres_revenus_type_activite = self.split_by_roles(tns_autres_revenus_type_activite_holder)

        has_conjoint = simulation.calculate('nb_parents', period) > 1
        rsa_nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        P = simulation.legislation_at(period.start)
        P_agr = P.tns.exploitant_agricole
        P_micro = P.impot_revenu.rpns.micro
        maj_2p = P_agr.maj_2p
        maj_1e_2ad = P_agr.maj_1e_2ad
        maj_e_sup = P_agr.maj_e_sup

        def eligibilite_agricole(has_conjoint, rsa_nb_enfants, tns_benefice_exploitant_agricole, P_agr):
            plafond_benefice_agricole = P_agr.plafond_rsa * P.cotsoc.gen.smic_h_b
            taux_avec_conjoint = (
                1 + maj_2p + maj_1e_2ad * (rsa_nb_enfants > 0) + maj_e_sup * max_(rsa_nb_enfants - 1, 0)
                )
            taux_sans_conjoint = 1 + maj_2p * (rsa_nb_enfants > 0) + maj_e_sup * max_(rsa_nb_enfants - 1, 0)
            taux_majoration = has_conjoint * taux_avec_conjoint + (1 - has_conjoint) * taux_sans_conjoint
            plafond_benefice_agricole_majore = taux_majoration * plafond_benefice_agricole

            return tns_benefice_exploitant_agricole < plafond_benefice_agricole_majore

        def eligibilite_chiffre_affaire(ca, type_activite, P_micro):
            plaf_vente = P_micro.specialbnc.marchandises.max
            plaf_service = P_micro.specialbnc.services.max

            return ((type_activite == 0) * (ca <= plaf_vente)) + ((type_activite >= 1) * (ca <= plaf_service))

        eligibilite_agricole = eligibilite_agricole(
            has_conjoint, rsa_nb_enfants, tns_benefice_exploitant_agricole, P_agr
            )
        eligibilite_chiffre_affaire = (
            eligibilite_chiffre_affaire(
                tns_autres_revenus_chiffre_affaires[CHEF], tns_autres_revenus_type_activite[CHEF], P_micro
                ) *
            eligibilite_chiffre_affaire(
                tns_autres_revenus_chiffre_affaires[PART], tns_autres_revenus_type_activite[PART], P_micro
                )
            )

        return period, eligibilite_agricole * (1 - tns_avec_employe) * eligibilite_chiffre_affaire


class rsa_forfait_asf(Variable):
    column = FloatCol(default = 0)
    entity = Famille
    label = u"Allocation de soutien familial forfaitisée pour le RSA"
    start_date = date(2014, 4, 1)

    def function(self, simulation, period):
        period = period.this_month
        # Si un ASF est versé, on ne prend pas en compte le montant réel mais un forfait.
        prestations_familiales = simulation.legislation_at(period.start).prestations.prestations_familiales
        minima_sociaux = simulation.legislation_at(period.start).prestations.minima_sociaux

        asf_verse = simulation.calculate('asf', period)
        montant_verse_par_enfant = prestations_familiales.af.bmaf * prestations_familiales.asf.taux_1_parent
        montant_retenu_rsa_par_enfant = prestations_familiales.af.bmaf * minima_sociaux.rmi.forfait_asf.taux1

        asf_retenue = asf_verse * (montant_retenu_rsa_par_enfant / montant_verse_par_enfant)

        return period, asf_retenue


class rsa_forfait_logement(Variable):
    column = FloatCol
    entity = Famille
    label = u"Forfait logement intervenant dans le calcul du Rmi ou du Rsa"

    def function(famille, period, legislation):
        period = period.this_month

        np_pers = famille('nb_parents', period) + famille('rsa_nb_enfants', period)
        aide_logement = famille('aide_logement', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        participation_frais = famille.demandeur.menage('participation_frais', period)
        loyer = famille.demandeur.menage('loyer', period)

        avantage_nature = or_(
            (statut_occupation_logement == 2) * not_(loyer),
            (statut_occupation_logement == 6) * (1 - participation_frais)
            )
        avantage_al = aide_logement > 0


        # Les parametres ont changé de nom au moment où le RMI est devenu le RSA
        # Pour le RSA, on utilise les taux des textes de lois, pour le RMI ils sont déjà aggrégés
        # Il faudrait uniformiser, mais les taux légaux pour le RMI commencent par "1", et ne passent pas en python
        if period.start.date >= date(2009, 6, 01):
            params = legislation(period).prestations.minima_sociaux.rsa
            montant_base = params.montant_de_base_du_rsa
            taux_2p = 1 + params.majoration_rsa.taux_deuxieme_personne
            taux_3p = taux_2p + params.majoration_rsa.taux_troisieme_personne
            forf_logement_taux_1p = params.forfait_logement.taux_1_personne
            forf_logement_taux_2p = params.forfait_logement.taux_2_personnes * taux_2p
            forf_logement_taux_3p = params.forfait_logement.taux_3_personnes_ou_plus * taux_3p
        else:
            params = legislation(period).prestations.minima_sociaux.rmi
            montant_base = params.rmi
            forf_logement_taux_1p = params.forfait_logement.taux1
            forf_logement_taux_2p = params.forfait_logement.taux2
            forf_logement_taux_3p = params.forfait_logement.taux3

        montant_forfait = montant_base * (
            (np_pers == 1) * forf_logement_taux_1p +
            (np_pers == 2) * forf_logement_taux_2p +
            (np_pers >= 3) * forf_logement_taux_3p
            )

        montant_al = avantage_al * min_(aide_logement, montant_forfait)
        montant_nature = avantage_nature * montant_forfait

        return period, max_(montant_al, montant_nature)


class rsa_isolement_recent(Variable):
    column = BoolCol
    entity = Famille
    label = u"Situation d'isolement depuis moins de 18 mois"


class rsa_majore(Variable):
    column = FloatCol
    label = u"Revenu de solidarité active - majoré"
    entity = Famille

    def function(self, simulation, period):
        period = period.this_month
        rsa_socle_majore = simulation.calculate('rsa_socle_majore', period)
        rsa_revenu_activite = simulation.calculate('rsa_revenu_activite', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        rsa_base_ressources = simulation.calculate('rsa_base_ressources', period)
        P = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa

        base_normalise = max_(
            rsa_socle_majore - rsa_forfait_logement - rsa_base_ressources + P.pente * rsa_revenu_activite, 0)

        return period, base_normalise * (base_normalise >= P.rsa_nv)


class rsa_majore_eligibilite(Variable):
    column = BoolCol
    entity = Famille
    label = u"Eligibilité au RSA majoré pour parent isolé"

    def function(self, simulation, period):

        period = period.this_month
        isole = not_(simulation.calculate('en_couple', period))
        isolement_recent = simulation.calculate('rsa_isolement_recent', period)
        enfant_moins_3_ans = nb_enf(simulation, period, 0, 2) > 0
        enceinte_fam = simulation.calculate('enceinte_fam', period)
        nbenf = simulation.calculate('rsa_nb_enfants', period)
        rsa_eligibilite_tns = simulation.calculate('rsa_eligibilite_tns', period)
        eligib = (
            isole *
            (enceinte_fam | (nbenf > 0)) *
            (enfant_moins_3_ans | isolement_recent | enceinte_fam) *
            rsa_eligibilite_tns
            )

        return period, eligib


class rsa_non_calculable(Variable):
    column = EnumCol(
        enum = Enum([
            u"",
            u"tns",
            u"conjoint_tns"
            ]),
        default = 0
        )
    entity = Famille
    label = u"RSA non calculable"

    def function(self, simulation, period):
        period = period.this_month

        # Si le montant du RSA est nul sans tenir compte des revenus
        # TNS pouvant provoquer une non calculabilité (parce que
        # les autres revenus sont trop importants), alors a fortiori
        # la famille ne sera pas éligible au RSA en tenant compte de
        # ces ressources. Il n'y a donc pas non calculabilité.
        eligible_rsa = (
            simulation.calculate('rsa_majore', period) +
            simulation.calculate('rsa_non_majore', period)
            ) > 0
        non_calculable_tns_holder = simulation.compute('rsa_non_calculable_tns_individu', period)
        non_calculable_tns_parents = self.split_by_roles(non_calculable_tns_holder, roles = [CHEF, PART])
        non_calculable = select(
            [non_calculable_tns_parents[CHEF] > 0, non_calculable_tns_parents[PART] > 0],
            [1, 2]
            )
        non_calculable = eligible_rsa * non_calculable

        return period, non_calculable


class rsa_non_calculable_tns_individu(Variable):
    column = BoolCol
    entity = Individu
    label = u"RSA non calculable du fait de la situation de l'individu. Dans le cas des TNS, l'utilisateur est renvoyé vers son PCG"

    def function(self, simulation, period):
        period = period.this_month
        this_year_and_last_year = period.start.offset('first-of', 'year').period('year', 2).offset(-1)
        tns_benefice_exploitant_agricole = simulation.calculate_add(
            'tns_benefice_exploitant_agricole', this_year_and_last_year)
        tns_micro_entreprise_chiffre_affaires = simulation.calculate_add(
            'tns_micro_entreprise_chiffre_affaires', this_year_and_last_year)
        tns_autres_revenus = simulation.calculate_add('tns_autres_revenus', this_year_and_last_year)

        return period, (
            (tns_benefice_exploitant_agricole > 0) +
            (tns_micro_entreprise_chiffre_affaires > 0) +
            (tns_autres_revenus > 0)
            )


class rsa_non_majore(Variable):
    column = FloatCol
    label = u"Revenu de solidarité active - non majoré"
    entity = Famille

    def function(self, simulation, period):
        period = period.this_month
        rsa_socle = simulation.calculate('rsa_socle', period)
        rsa_revenu_activite = simulation.calculate('rsa_revenu_activite', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        rsa_base_ressources = simulation.calculate('rsa_base_ressources', period)
        P = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa

        base_normalise = max_(rsa_socle - rsa_forfait_logement - rsa_base_ressources + P.pente * rsa_revenu_activite, 0)

        return period, base_normalise * (base_normalise >= P.rsa_nv)


class rsa_socle(DatedVariable):
    column = FloatCol
    entity = Famille
    label = "RSA socle"

    @dated_function(stop = date(2009, 5, 31))
    def function_rmi(self, simulation, period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        eligib = simulation.calculate('rsa_eligibilite', period)
        rsa_nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        nb_personnes = nb_parents + rsa_nb_enfants

        rmi = simulation.legislation_at(period.start).prestations.minima_sociaux.rmi
        taux = (
            1 +
            (nb_personnes >= 2) * rmi.txp2 +
            (nb_personnes >= 3) * rmi.txp3 +
            (nb_personnes >= 4) * where(nb_parents == 1, rmi.txps, rmi.txp3) +
            # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rmi.txps
            )
        socle = rmi.rmi

        return period, eligib * socle * taux

    @dated_function(start = date(2009, 6, 1))
    def function_rsa(self, simulation, period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        eligib = simulation.calculate('rsa_eligibilite', period)
        rsa_nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        nb_personnes = nb_parents + rsa_nb_enfants

        rsa = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa
        taux = (
            1 +
            (nb_personnes >= 2) * rsa.majoration_rsa.taux_deuxieme_personne +
            (nb_personnes >= 3) * rsa.majoration_rsa.taux_troisieme_personne +
            (nb_personnes >= 4) * where(
                nb_parents == 1,
                rsa.majoration_rsa.taux_personne_supp, rsa.majoration_rsa.taux_troisieme_personne
                ) +  # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rsa.majoration_rsa.taux_personne_supp
            )
        socle = rsa.montant_de_base_du_rsa

        return period, eligib * socle * taux


class rsa_socle_majore(Variable):
    column = FloatCol
    entity = Famille
    label = u"Majoration pour parent isolé du Revenu de solidarité active socle"
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.this_month
        eligib = simulation.calculate('rsa_majore_eligibilite', period)
        nbenf = simulation.calculate('rsa_nb_enfants', period)

        rsa = simulation.legislation_at(period.start).prestations.minima_sociaux.rsa
        taux = rsa.majo_rsa.pac0 + rsa.majo_rsa.pac_enf_sup * nbenf
        socle = rsa.montant_de_base_du_rsa

        return period, eligib * socle * taux
