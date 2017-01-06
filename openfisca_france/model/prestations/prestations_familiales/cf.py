# -*- coding: utf-8 -*-

from __future__ import division

from numpy import (round, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)

from openfisca_france.model.base import *  # noqa analysis:ignore


class cf_enfant_a_charge(Variable):
    column = BoolCol
    entity = Individu
    label = u"Complément familial - Enfant considéré à charge"

    def function(individu, period, legislation):
        period = period.this_month

        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age = individu('age', period)

        pfam = legislation(period).prestations.prestations_familiales

        condition_age = (age >= 0) * (age < pfam.cf.age_max)
        condition_situation = est_enfant_dans_famille * not_(autonomie_financiere)

        return period, condition_age * condition_situation


class cf_enfant_eligible(Variable):
    column = BoolCol
    entity = Individu
    label = u"Complément familial - Enfant pris en compte pour l'éligibilité"

    def function(individu, period, legislation):
        period = period.this_month

        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = legislation(period).prestations.prestations_familiales

        condition_enfant = ((age >= pfam.cf.age_min) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.cf.age_max)

        return period, or_(condition_enfant, condition_jeune) * cf_enfant_a_charge


class cf_dom_enfant_eligible(Variable):
    column = BoolCol
    entity = Individu
    label = u"Complément familial (DOM) - Enfant pris en compte pour l'éligibilité"

    def function(individu, period, legislation):
        period = period.this_month

        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = legislation(period).prestations.prestations_familiales

        condition_age = (age >= pfam.cf.age_minimal_dom) * (age < pfam.cf.age_maximal_dom)
        condition_situation = cf_enfant_a_charge * rempli_obligation_scolaire

        return period, condition_age * condition_situation


class cf_dom_enfant_trop_jeune(Variable):
    column = BoolCol
    entity = Individu
    label = u"Complément familial (DOM) - Enfant trop jeune pour ouvrir le droit"

    def function(individu, period, legislation):
        period = period.this_month

        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        age = individu('age', period)

        pfam = legislation(period).prestations.prestations_familiales

        condition_age = (age >= 0) * (age < pfam.cf.age_min)

        return period, condition_age * est_enfant_dans_famille


class cf_ressources_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"Complément familial - Ressources de l'individu prises en compte"

    def function(individu, period):
        period = period.this_month

        base_ressources = individu('prestations_familiales_base_ressources_individu', period)
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        cf_enfant_a_charge = individu('cf_enfant_a_charge', period)

        return period, or_(not_(est_enfant_dans_famille), cf_enfant_a_charge) * base_ressources


class cf_plafond(Variable):
    column = FloatCol
    entity = Famille
    label = u"Plafond d'éligibilité au Complément Familial"

    def function(famille, period, legislation):
        period = period.this_month

        pfam = legislation(period).prestations.prestations_familiales

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

        return period, plafond


class cf_majore_plafond(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"Plafond d'éligibilité au Complément Familial majoré"

    @dated_function(date(2014, 4, 1))
    def function(famille, period, legislation):
        period = period.this_month
        plafond_base = famille('cf_plafond', period)
        pfam = legislation(period).prestations.prestations_familiales
        return period, plafond_base * pfam.cf.plafond_cf_majore


class cf_ressources(Variable):
    column = FloatCol
    entity = Famille
    label = u"Ressources prises en compte pour l'éligibilité au complément familial"

    def function(famille, period):
        period = period.this_month
        cf_ressources_individu_i = famille.members('cf_ressources_individu', period)
        ressources = famille.sum(cf_ressources_individu_i)
        return period, ressources


class cf_eligibilite_base(Variable):
    column = BoolCol
    entity = Famille
    label = u"Éligibilité au complément familial sous condition de ressources et avant cumul"

    def function(famille, period, legislation):
        period = period.this_month

        residence_dom = famille.demandeur.menage('residence_dom', period)

        cf_enfant_eligible = famille.members('cf_enfant_eligible', period)
        cf_nbenf = famille.sum(cf_enfant_eligible)

        return period, not_(residence_dom) * (cf_nbenf >= 3)


class cf_eligibilite_dom(Variable):
    column = BoolCol
    entity = Famille
    label = u"Éligibilité au complément familial pour les DOM sous condition de ressources et avant cumul"


    def function(famille, period, legislation):
        period = period.this_month

        residence_dom = famille.demandeur.menage('residence_dom', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        cf_dom_enfant_eligible = famille.members('cf_dom_enfant_eligible', period)
        cf_nbenf = famille.sum(cf_dom_enfant_eligible)

        cf_dom_enfant_trop_jeune = famille.members('cf_dom_enfant_trop_jeune', period)
        cf_nbenf_trop_jeune = famille.sum(cf_dom_enfant_trop_jeune)

        condition_composition_famille = (cf_nbenf >= 1) * (cf_nbenf_trop_jeune == 0)
        condition_residence = residence_dom * not_(residence_mayotte)

        return period, condition_composition_famille * condition_residence


class cf_non_majore_avant_cumul(Variable):
    column = FloatCol
    entity = Famille
    label = u"Complément familial non majoré avant cumul"

    def function(famille, period, legislation):
        period = period.this_month

        eligibilite_base = famille('cf_eligibilite_base', period)
        eligibilite_dom = famille('cf_eligibilite_dom', period)
        ressources = famille('cf_ressources', period)
        plafond = famille('cf_plafond', period)

        pfam = legislation(period).prestations.prestations_familiales

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

        return period, max_(eligibilite * montant, eligibilite_diff * montant_diff)


class cf_majore_avant_cumul(DatedVariable):
    column = FloatCol
    entity = Famille
    label = u"Complément familial majoré avant cumul"

    @dated_function(date(2014, 4, 1))
    def function(famille, period, legislation):
        period = period.this_month

        eligibilite_base = famille('cf_eligibilite_base', period)
        eligibilite_dom = famille('cf_eligibilite_dom', period)
        ressources = famille('cf_ressources', period)
        plafond_majore = famille('cf_majore_plafond', period)

        pfam = legislation(period).prestations.prestations_familiales

        eligibilite_sous_condition = or_(eligibilite_base, eligibilite_dom)

        # Montant
        montant = pfam.af.bmaf * (pfam.cf.taux_cf_majore * eligibilite_base + pfam.cf.taux_majore_dom * eligibilite_dom)

        eligibilite = eligibilite_sous_condition * (ressources <= plafond_majore)

        return period, eligibilite * montant


class cf_montant(Variable):
    column = FloatCol
    entity = Famille
    label = u"Montant du complément familial, avant prise en compte d'éventuels cumuls"

    def function(famille, period):
        period = period.this_month

        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', period)
        cf_majore_avant_cumul = famille('cf_majore_avant_cumul', period)

        return period, max_(cf_non_majore_avant_cumul, cf_majore_avant_cumul)


class cf(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Complément familial"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(famille, period, legislation):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.this_month
        paje_base = famille('paje_base', period)
        apje_avant_cumul = famille('apje_avant_cumul', period)
        ape_avant_cumul = famille('ape_avant_cumul', period)
        cf_montant = famille('cf_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        cf_brut = not_(paje_base) * (apje_avant_cumul <= cf_montant) * (ape_avant_cumul <= cf_montant) * cf_montant
        return period, not_(residence_mayotte) * round(cf_brut, 2)
