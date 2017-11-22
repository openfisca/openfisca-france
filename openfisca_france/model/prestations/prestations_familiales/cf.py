# -*- coding: utf-8 -*-

from __future__ import division

from numpy import round, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore


class cf_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = u"Complément familial - Enfant considéré à charge"
    definition_period = MONTH

    def formula(individu, period, parameters):
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age = individu('age', period)

        pfam = parameters(period).prestations.prestations_familiales

        condition_age = (age >= 0) * (age < pfam.cf.age_max)
        condition_situation = est_enfant_dans_famille * not_(autonomie_financiere)

        return condition_age * condition_situation


class cf_enfant_eligible(Variable):
    value_type = bool
    entity = Individu
    label = u"Complément familial - Enfant pris en compte pour l'éligibilité"
    definition_period = MONTH

    def formula(individu, period, parameters):
        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = parameters(period).prestations.prestations_familiales

        condition_enfant = ((age >= pfam.cf.age_min) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.cf.age_max)

        return or_(condition_enfant, condition_jeune) * cf_enfant_a_charge


class cf_dom_enfant_eligible(Variable):
    value_type = bool
    entity = Individu
    label = u"Complément familial (DOM) - Enfant pris en compte pour l'éligibilité"
    definition_period = MONTH

    def formula(individu, period, parameters):
        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = parameters(period).prestations.prestations_familiales

        condition_age = (age >= pfam.cf.age_minimal_dom) * (age < pfam.cf.age_maximal_dom)
        condition_situation = cf_enfant_a_charge * rempli_obligation_scolaire

        return condition_age * condition_situation


class cf_dom_enfant_trop_jeune(Variable):
    value_type = bool
    entity = Individu
    label = u"Complément familial (DOM) - Enfant trop jeune pour ouvrir le droit"
    definition_period = MONTH

    def formula(individu, period, parameters):
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        age = individu('age', period)

        pfam = parameters(period).prestations.prestations_familiales

        condition_age = (age >= 0) * (age < pfam.cf.age_min)

        return condition_age * est_enfant_dans_famille


class cf_ressources_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Complément familial - Ressources de l'individu prises en compte"
    definition_period = MONTH

    def formula(individu, period):
        base_ressources = individu('prestations_familiales_base_ressources_individu', period)
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)

        return or_(not_(est_enfant_dans_famille), cf_enfant_a_charge) * base_ressources


class cf_plafond(Variable):
    value_type = float
    entity = Famille
    label = u"Plafond d'éligibilité au Complément Familial"
    definition_period = MONTH

    def formula(famille, period, parameters):
        pfam = parameters(period).prestations.prestations_familiales

        eligibilite_base = famille('cf_eligibilite_base', period)
        eligibilite_dom = famille('cf_eligibilite_dom', period)
        isole = not_(famille('en_couple', period))
        biactivite = famille('biactivite', period)

        # Calcul du nombre d'enfants à charge au sens du CF
        cf_enfant_a_charge_i = famille.members('cf_enfant_a_charge', period)
        cf_nbenf = famille.sum(cf_enfant_a_charge_i)

        # Calcul du taux à appliquer au plafond de base pour la France métropolitaine
        taux_plafond_metropole = 1 + pfam.cf.majoration_plafond_2_premiers_enf * min_(cf_nbenf, 2) + pfam.cf.majoration_plafond_3eme_enf_et_plus * max_(cf_nbenf - 2, 0)

        # Majoration du plafond pour biactivité ou isolement (France métropolitaine)
        majoration_plafond = (isole | biactivite)

        # Calcul du plafond pour la France métropolitaine
        plafond_metropole = pfam.cf.plafond_de_ressources_0_enfant * taux_plafond_metropole + pfam.cf.majoration_plafond_biact_isole * majoration_plafond

        # Calcul du taux à appliquer au plafond de base pour les DOM
        taux_plafond_dom = 1 + cf_nbenf * pfam.ars.majoration_par_enf_supp

        # Calcul du plafond pour les DOM
        plafond_dom = pfam.ars.plafond_ressources * taux_plafond_dom

        plafond = (eligibilite_base * plafond_metropole + eligibilite_dom * plafond_dom)

        return plafond


class cf_majore_plafond(Variable):
    value_type = float
    entity = Famille
    label = u"Plafond d'éligibilité au Complément Familial majoré"
    definition_period = MONTH

    def formula_2014_04_01(famille, period, parameters):
        plafond_base = famille('cf_plafond', period)
        pfam = parameters(period).prestations.prestations_familiales
        return plafond_base * pfam.cf.plafond_cf_majore


class cf_ressources(Variable):
    value_type = float
    entity = Famille
    label = u"Ressources prises en compte pour l'éligibilité au complément familial"
    definition_period = MONTH

    def formula(famille, period):
        cf_ressources_individu_i = famille.members('cf_ressources_individu', period)
        ressources = famille.sum(cf_ressources_individu_i)
        return ressources


class cf_eligibilite_base(Variable):
    value_type = bool
    entity = Famille
    label = u"Éligibilité au complément familial sous condition de ressources et avant cumul"
    definition_period = MONTH

    def formula(famille, period, parameters):
        residence_dom = famille.demandeur.menage('residence_dom', period)

        cf_enfant_eligible = famille.members('cf_enfant_eligible', period)
        cf_nbenf = famille.sum(cf_enfant_eligible)

        return not_(residence_dom) * (cf_nbenf >= 3)


class cf_eligibilite_dom(Variable):
    value_type = bool
    entity = Famille
    label = u"Éligibilité au complément familial pour les DOM sous condition de ressources et avant cumul"
    definition_period = MONTH


    def formula(famille, period, parameters):
        residence_dom = famille.demandeur.menage('residence_dom', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        cf_dom_enfant_eligible = famille.members('cf_dom_enfant_eligible', period)
        cf_nbenf = famille.sum(cf_dom_enfant_eligible)

        cf_dom_enfant_trop_jeune = famille.members('cf_dom_enfant_trop_jeune', period)
        cf_nbenf_trop_jeune = famille.sum(cf_dom_enfant_trop_jeune)

        condition_composition_famille = (cf_nbenf >= 1) * (cf_nbenf_trop_jeune == 0)
        condition_residence = residence_dom * not_(residence_mayotte)

        return condition_composition_famille * condition_residence


class cf_non_majore_avant_cumul(Variable):
    value_type = float
    entity = Famille
    label = u"Complément familial non majoré avant cumul"
    definition_period = MONTH

    def formula(famille, period, parameters):
        eligibilite_base = famille('cf_eligibilite_base', period)
        eligibilite_dom = famille('cf_eligibilite_dom', period)
        ressources = famille('cf_ressources', period)
        plafond = famille('cf_plafond', period)

        pfam = parameters(period).prestations.prestations_familiales

        eligibilite_sous_condition = or_(eligibilite_base, eligibilite_dom)

        # Montant
        montant = pfam.af.bmaf * (pfam.cf.taux_cf_base * eligibilite_base + pfam.cf.taux_base_dom * eligibilite_dom)

        # Complément familial
        eligibilite = eligibilite_sous_condition * (ressources <= plafond)

        # Complément familial différentiel
        plafond_diff = plafond + 12 * montant
        eligibilite_diff = not_(eligibilite) * eligibilite_sous_condition * (
            ressources <= plafond_diff)
        montant_diff = (plafond_diff - ressources) / 12

        return max_(eligibilite * montant, eligibilite_diff * montant_diff)


class cf_majore_avant_cumul(Variable):
    value_type = float
    entity = Famille
    label = u"Complément familial majoré avant cumul"
    definition_period = MONTH

    def formula_2014_04_01(famille, period, parameters):
        eligibilite_base = famille('cf_eligibilite_base', period)
        eligibilite_dom = famille('cf_eligibilite_dom', period)
        ressources = famille('cf_ressources', period)
        plafond_majore = famille('cf_majore_plafond', period)

        pfam = parameters(period).prestations.prestations_familiales

        eligibilite_sous_condition = or_(eligibilite_base, eligibilite_dom)

        # Montant
        montant = pfam.af.bmaf * (pfam.cf.taux_cf_majore * eligibilite_base + pfam.cf.taux_majore_dom * eligibilite_dom)

        eligibilite = eligibilite_sous_condition * (ressources <= plafond_majore)

        return eligibilite * montant


class cf_montant(Variable):
    value_type = float
    entity = Famille
    label = u"Montant du complément familial, avant prise en compte d'éventuels cumuls"
    definition_period = MONTH

    def formula(famille, period):
        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', period)
        cf_majore_avant_cumul = famille('cf_majore_avant_cumul', period)

        return max_(cf_non_majore_avant_cumul, cf_majore_avant_cumul)


class cf(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Complément familial"
    reference = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        paje_base = famille('paje_base', period)
        apje_avant_cumul = famille('apje_avant_cumul', period)
        ape_avant_cumul = famille('ape_avant_cumul', period)
        cf_montant = famille('cf_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        cf_brut = not_(paje_base) * (apje_avant_cumul <= cf_montant) * (ape_avant_cumul <= cf_montant) * cf_montant
        return not_(residence_mayotte) * round(cf_brut, 2)
