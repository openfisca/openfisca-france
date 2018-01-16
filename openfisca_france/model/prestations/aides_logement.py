# -*- coding: utf-8 -*-

from __future__ import division

import csv
import json
import logging
import pkg_resources

from numpy import ceil, fromiter, int16, logical_or as or_, logical_and as and_, nditer

import openfisca_france
from openfisca_core.periods import Instant

from openfisca_france.model.base import *  # noqa  analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


log = logging.getLogger(__name__)

zone_apl_by_depcom = None


class al_nb_personnes_a_charge(Variable):
    value_type = int
    entity = Famille
    label = u"Nombre de personne à charge au sens des allocations logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        '''
        site de la CAF en 2011:

        # Enfant à charge
        Vous assurez financièrement l'entretien et asez la responsabilité
        affective et éducative d'un enfant, que vous ayez ou non un lien de
        parenté avec lui. Il est reconnu à votre charge pour le versement
        des aides au logement jusqu'au mois précédent ses 21 ans.
        Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.

        # Parents âgés ou infirmes
        Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009
        ne dépassent pas 10 386,59 € :
        * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
        60 ans, inaptes au travail, anciens déportés,
        * vos proches parents infirmes âgés de 22 ans ou plus (parents,
        grand-parents, enfants, petits enfants, frères, soeurs, oncles,
        tantes, neveux, nièces).
        '''

        age_max_enfant = parameters(period).prestations.prestations_familiales.cf.age_max
        residence_dom = famille.demandeur.menage('residence_dom', period)

        def al_nb_enfants():
            age_min_enfant = parameters(period).prestations.prestations_familiales.af.age1
            return nb_enf(famille, period, age_min_enfant, age_max_enfant - 1)  # La limite sur l'age max est stricte.

        def al_nb_adultes_handicapes():

            # Variables à valeur pour un individu
            base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
            inapte_travail = famille.members('inapte_travail', period)
            taux_incapacite = famille.members('taux_incapacite', period)
            age = famille.members('age', period)

            # Parametres
            plafond_ressource = parameters(period.n_2.stop).prestations.minima_sociaux.aspa.plafond_ressources_seul * 1.25
            taux_incapacite_minimum = 0.8

            adulte_handicape = (
                ((taux_incapacite > taux_incapacite_minimum) + inapte_travail) *
                (age >= age_max_enfant) *
                (base_ressources_i <= plafond_ressource)
                )

            # Par convention les adultes handicapé à charge de la famille ont le role ENFANT dans la famille
            # Le demandeur et son conjoint ne sont jamais considérés comme à charge
            return famille.sum(adulte_handicape, role = Famille.ENFANT)

        nb_pac = al_nb_enfants() + al_nb_adultes_handicapes()
        nb_pac = where(residence_dom, min_(nb_pac, 6), nb_pac)
        # Dans les DOMs, le barème est fixe à partir de 6 enfants.

        return nb_pac


class al_couple(Variable):
    value_type = bool
    entity = Famille
    label = u'Situation de couple pour le calcul des AL'
    definition_period = MONTH

    def formula(famille, period):
        en_couple = famille('en_couple', period)
        enceinte = famille('enceinte_fam', period)
        couple = en_couple + enceinte  # le barème "couple" est utilisé pour les femmes enceintes isolées

        return couple


class aide_logement_base_ressources_eval_forfaitaire(Variable):
    value_type = float
    entity = Famille
    label = u"Base ressources en évaluation forfaitaire des aides au logement (R351-7 du CCH)"
    definition_period = MONTH

    def formula(famille, period, parameters):
        def eval_forfaitaire_salaries():
            salaire_imposable_i = famille.members('salaire_imposable', period.offset(-1))
            salaire_imposable = famille.sum(salaire_imposable_i, role = Famille.PARENT)
            # Application de l'abattement pour frais professionnels
            params_abattement = parameters(period).impot_revenu.tspr.abatpro
            somme_salaires_mois_precedent = 12 * salaire_imposable
            montant_abattement = round_(
                min_(
                    max_(params_abattement.taux * somme_salaires_mois_precedent, params_abattement.min),
                    params_abattement.max
                    )
                )
            return max_(0, somme_salaires_mois_precedent - montant_abattement)

        def eval_forfaitaire_tns():
            last_july_first = Instant(
                (period.start.year if period.start.month >= 7 else period.start.year - 1,
                7, 1))
            smic_horaire_brut = parameters(last_july_first).cotsoc.gen.smic_h_b
            travailleur_non_salarie_i = famille.members('travailleur_non_salarie', period)
            any_tns = famille.any(travailleur_non_salarie_i)
            return any_tns * 1500 * smic_horaire_brut

        return max_(eval_forfaitaire_salaries(), eval_forfaitaire_tns())


class aide_logement_assiette_abattement_chomage(Variable):
    value_type = float
    entity = Individu
    label = u"Assiette sur lequel un abattement chômage peut être appliqués pour les AL. Ce sont les revenus d'activité professionnelle, moins les abbattements pour frais professionnels."
    definition_period = YEAR

    def formula(individu, period, parameters):
        revenus_non_salarie = individu('rpns', period)
        revenu_salarie = individu('salaire_imposable', period, options = [ADD])
        chomeur_longue_duree = individu('chomeur_longue_duree', period)
        frais_reels = individu('frais_reels', period)
        abatpro = parameters(period).impot_revenu.tspr.abatpro

        abattement_minimum = where(chomeur_longue_duree, abatpro.min2, abatpro.min)
        abattement_forfaitaire = round_(min_(max_(abatpro.taux * revenu_salarie, abattement_minimum), abatpro.max))
        revenus_salarie_apres_abbatement = where(
            frais_reels > abattement_forfaitaire,
            revenu_salarie - frais_reels,
            max_(0, revenu_salarie - abattement_forfaitaire)
            )

        return revenus_non_salarie + revenus_salarie_apres_abbatement


class aide_logement_abattement_chomage_indemnise(Variable):
    value_type = float
    entity = Individu
    label = u"Montant de l'abattement pour personnes au chômage indemnisé (R351-13 du CCH)"
    definition_period = MONTH
    # Article R532-7 du Code de la sécurité sociale
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000031694522&cidTexte=LEGITEXT000006073189"

    def formula(individu, period, parameters):
        chomage_net_m_1 = individu('chomage_net', period.offset(-1))
        chomage_net_m_2 = individu('chomage_net', period.offset(-2))
        condition_abattement = (chomage_net_m_1 > 0) * (chomage_net_m_2 > 0)
        revenus_activite_pro = individu('aide_logement_assiette_abattement_chomage', period.n_2)
        taux_abattement = parameters(period).prestations.aides_logement.ressources.abattement_chomage_indemnise

        return condition_abattement * taux_abattement * revenus_activite_pro


class aide_logement_abattement_depart_retraite(Variable):
    value_type = float
    entity = Individu
    label = u"Montant de l'abattement sur les salaires en cas de départ en retraite"
    definition_period = MONTH
    # Article R532-5 du Code de la sécurité sociale
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006750910&cidTexte=LEGITEXT000006073189&dateTexte=20151231"

    def formula(individu, period, parameters):
        retraite_n_2 = individu('retraite_imposable', period.n_2, options = [ADD])
        activite = individu('activite', period)
        retraite = activite == TypesActivite.retraite
        condition_abattement = (retraite_n_2 == 0) * retraite
        revenus_activite_pro = individu('revenu_assimile_salaire_apres_abattements', period.n_2)

        abattement = condition_abattement * 0.3 * revenus_activite_pro

        return abattement


class aide_logement_neutralisation_rsa(Variable):
    value_type = float
    entity = Famille
    label = u"Abattement sur les revenus n-2 pour les bénéficiaires du RSA"
    definition_period = MONTH
    reference = [
        # Article R532-7 du Code de la sécurité sociale
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000031694522&cidTexte=LEGITEXT000006073189",
        # Article R351-14-1 du Code de la construction et de l'habitation
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006074096&idArticle=LEGIARTI000006897410"
        ]

    def formula(famille, period, parameters):
        # Circular definition, as rsa depends on al.
        # We don't allow it, so default value of rsa will be returned if a recursion is detected.
        rsa_mois_dernier = famille('rsa', period.last_month, max_nb_cycles = 0)

        revenus_a_neutraliser_i = famille.members('revenu_assimile_salaire_apres_abattements', period.n_2)
        revenus_a_neutraliser = famille.sum(revenus_a_neutraliser_i)

        return revenus_a_neutraliser * (rsa_mois_dernier > 0)


class aide_logement_base_ressources_defaut(Variable):
    value_type = float
    entity = Famille
    label = u"Base ressource par défaut des allocations logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        biactivite = famille('biactivite', period)
        Pr = parameters(period).prestations.aides_logement.ressources
        base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
        base_ressources_parents = famille.sum(base_ressources_i, role = Famille.PARENT)
        abattement_chomage_indemnise_i = famille.members('aide_logement_abattement_chomage_indemnise', period)
        abattement_chomage_indemnise = famille.sum(abattement_chomage_indemnise_i, role = Famille.PARENT)
        abattement_depart_retraite_i = famille.members('aide_logement_abattement_depart_retraite', period)
        abattement_depart_retraite = famille.sum(abattement_depart_retraite_i, role = Famille.PARENT)
        neutralisation_rsa = famille('aide_logement_neutralisation_rsa', period)
        abattement_ressources_enfant = parameters(period.n_2.stop).prestations.minima_sociaux.aspa.plafond_ressources_seul * 1.25
        base_ressources_enfants = famille.sum(
            max_(0, base_ressources_i - abattement_ressources_enfant), role = Famille.ENFANT)

        # It would be nicer to be able to write famille.demandeur.has_role(FoyerFiscal.DECLARANT_PRINCIPAL), but it doesn't work as expected at the moment
        declarant_principal_i = famille.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        demandeur_declarant_principal = famille.value_from_person(declarant_principal_i, Famille.DEMANDEUR)
        conjoint_declarant_principal = famille.value_from_person(declarant_principal_i, Famille.CONJOINT)

        # Revenus du foyer fiscal
        rev_coll = (
            famille.demandeur.foyer_fiscal('rev_coll', period.n_2) *  demandeur_declarant_principal +
            famille.conjoint.foyer_fiscal('rev_coll', period.n_2) * conjoint_declarant_principal
            )

        ressources = (
            base_ressources_parents + base_ressources_enfants + rev_coll -
            (abattement_chomage_indemnise + abattement_depart_retraite + neutralisation_rsa)
            )

        # Abattement forfaitaire pour double activité
        abattement_double_activite = biactivite * Pr.dar_1

        # Arrondi aux 100 euros supérieurs
        result = max_(ressources - abattement_double_activite, 0)

        return result


class aide_logement_base_ressources(Variable):
    value_type = float
    entity = Famille
    label = u"Base ressources des allocations logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        mois_precedent = period.offset(-1)
        last_day_reference_year = period.n_2.stop
        base_ressources_defaut = famille('aide_logement_base_ressources_defaut', period)
        base_ressources_eval_forfaitaire = famille(
            'aide_logement_base_ressources_eval_forfaitaire', period)
        en_couple = famille('en_couple', period)

        aah_i = famille.members('aah', mois_precedent)
        aah = famille.sum(aah_i, role = Famille.PARENT)

        age_demandeur = famille.demandeur('age', period)
        age_conjoint = famille.conjoint('age', period)
        smic_horaire_brut_n2 = parameters(last_day_reference_year).cotsoc.gen.smic_h_b

        salaire_imposable_i = famille.members('salaire_imposable', period.offset(-1))
        somme_salaires = famille.sum(salaire_imposable_i, role = Famille.PARENT)

        plafond_eval_forfaitaire = 1015 * smic_horaire_brut_n2

        plafond_salaire_jeune_isole = parameters(period).prestations.aides_logement.ressources.dar_8
        plafond_salaire_jeune_couple = parameters(period).prestations.aides_logement.ressources.dar_9
        plafond_salaire_jeune = where(en_couple, plafond_salaire_jeune_couple, plafond_salaire_jeune_isole)

        neutral_jeune = or_(age_demandeur < 25, and_(en_couple, age_conjoint < 25))
        neutral_jeune &= somme_salaires < plafond_salaire_jeune

        eval_forfaitaire = base_ressources_defaut <= plafond_eval_forfaitaire
        eval_forfaitaire &= base_ressources_eval_forfaitaire > 0
        eval_forfaitaire &= aah == 0
        eval_forfaitaire &= not_(neutral_jeune)

        ressources = where(eval_forfaitaire, base_ressources_eval_forfaitaire, base_ressources_defaut)

        # Planchers de ressources pour étudiants
        # Seul le statut étudiant (et boursier) du demandeur importe, pas celui du conjoint
        Pr = parameters(period).prestations.aides_logement.ressources
        demandeur_etudiant = famille.demandeur('etudiant', period)
        demandeur_boursier = famille.demandeur('boursier', period)
        montant_plancher_ressources = max_(0, demandeur_etudiant * Pr.dar_4 - demandeur_boursier * Pr.dar_5)
        ressources = max_(ressources, montant_plancher_ressources)

        # Arrondi au centime, pour éviter qu'une petite imprécision liée à la recombinaison d'une valeur annuelle éclatée ne fasse monter d'un cran l'arrondi au 100€ supérieur.

        ressources = round_(ressources * 100) / 100

        # Arrondi aux 100 euros supérieurs
        ressources = ceil(ressources / 100) * 100

        return ressources


class aide_logement_loyer_plafond(Variable):
    value_type = float
    entity = Famille
    label = u"Loyer plafond dans le calcul des aides au logement (L2)"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        coloc = famille.demandeur.menage('coloc', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        zone_apl = famille.demandeur.menage('zone_apl', period)

        loyers_plafond = al.loyers_plafond.par_zone[zone_apl]

        plafond_personne_seule = loyers_plafond.personnes_seules
        plafond_couple = loyers_plafond.couples
        plafond_famille = loyers_plafond.un_enfant + (al_nb_pac > 1) * (al_nb_pac - 1) * loyers_plafond.majoration_par_enf_supp

        plafond = select(
            [not_(couple) * (al_nb_pac == 0) + chambre, al_nb_pac > 0],
            [plafond_personne_seule, plafond_famille],
            default = plafond_couple
            )

        coeff_coloc = where(coloc, al.loyers_plafond.colocation, 1)
        coeff_chambre = where(chambre, al.loyers_plafond.chambre, 1)

        return round_(plafond * coeff_coloc * coeff_chambre, 2)


class aide_logement_loyer_seuil_degressivite(Variable):
    value_type = float
    entity = Famille
    label = u"Seuil de degressivité dans le calcul des aides au logement"
    definition_period = MONTH

    def formula_2016_07_01(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        zone_apl = famille.demandeur.menage('zone_apl', period)
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        coloc = famille.demandeur.menage('coloc', period)

        coeff_degressivite = al.loyers_plafond.par_zone[zone_apl].degressivite
        loyer_degressivite = loyer_plafond * coeff_degressivite
        minoration_coloc = loyer_degressivite * 0.25 * coloc
        minoration_chambre = loyer_degressivite * 0.1 * chambre
        loyer_degressivite -= minoration_coloc + minoration_chambre

        return round_(loyer_degressivite, 2)


class aide_logement_loyer_seuil_suppression(Variable):
    value_type = float
    entity = Famille
    label = u"Seuil de suppression dans le calcul des aides au logement"
    definition_period = MONTH

    def formula_2016_07_01(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        zone_apl = famille.demandeur.menage('zone_apl', period)
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        chambre = famille.demandeur.menage('logement_chambre', period)
        coloc = famille.demandeur.menage('coloc', period)

        coeff_suppression = al.loyers_plafond.par_zone[zone_apl].suppression

        loyer_suppression = loyer_plafond * coeff_suppression
        minoration_coloc = loyer_suppression * 0.25 * coloc
        minoration_chambre = loyer_suppression * 0.1 * chambre
        loyer_suppression -= minoration_coloc + minoration_chambre

        return round_(loyer_suppression, 2)


class aide_logement_loyer_reel(Variable):
    value_type = float
    entity = Famille
    label = u"Loyer réel dans le calcul des aides au logement"
    definition_period = MONTH

    def formula(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        loyer = famille.demandeur.menage('loyer', period)
        coeff_meuble = where(statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble, 2 / 3, 1)  # Coeff de 2/3 pour les meublés
        return round_(loyer * coeff_meuble)


class aide_logement_loyer_retenu(Variable):
    value_type = float
    entity = Famille
    label = u"Loyer retenu (hors charge) dans le calcul des aides au logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)

        # loyer retenu
        return min_(loyer_reel, loyer_plafond)


class aide_logement_charges(Variable):
    value_type = float
    entity = Famille
    label = u"Charges retenues dans le calcul des aides au logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        P = parameters(period).prestations.aides_logement.forfait_charges
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        coloc = famille.demandeur.menage('coloc', period)
        montant_coloc = where(couple, 1, 0.5) * P.cas_general + al_nb_pac * P.majoration_par_enfant
        montant_cas_general = P.cas_general + al_nb_pac * P.majoration_par_enfant

        return where(coloc, montant_coloc, montant_cas_general)


class aide_logement_R0(Variable):
    value_type = float
    entity = Famille
    label = u"Revenu de référence, basé sur la situation familiale, pris en compte dans le calcul des AL."
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        pfam_n_2 = parameters(period.start.offset(-2, 'year')).prestations.prestations_familiales
        minim_n_2 = parameters(period.start.offset(-2, 'year')).prestations.minima_sociaux
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        n_2 = period.start.offset(-2, 'year')
        if n_2.date >= date(2009, 6, 01):
            montant_de_base = minim_n_2.rsa.montant_de_base_du_rsa
        else:
            montant_de_base = minim_n_2.rmi.montant_de_base_du_rmi

        R1 = montant_de_base * (
            al.r1.personne_isolee * not_(couple) * (al_nb_pac == 0) +
            al.r1.couple_sans_enf * couple * (al_nb_pac == 0) +
            al.r1.personne_isolee_ou_couple_avec_1_enf * (al_nb_pac == 1) +
            al.r1.personne_isolee_ou_couple_avec_2_enf * (al_nb_pac >= 2) +
            al.r1.majoration_enfant_a_charge_supp * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R2 = pfam_n_2.af.bmaf * (
            al.r2.taux3_dom * residence_dom * (al_nb_pac == 1) +
            al.r2.personnes_isolees_ou_couples_avec_2_enf * (al_nb_pac >= 2) +
            al.r2.majoration_par_enf_supp_a_charge * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R0 = round_(12 * (R1 - R2) * (1 - al.autres.abat_sal))

        return R0

    # cf Décret n° 2014-1739 du 29 décembre 2014 relatif au calcul des aides personnelles au logement
    def formula_2015_01_01(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)

        R0 = (
            al.R0.taux_seul * not_(couple) * (al_nb_pac == 0) +
            al.R0.taux_couple * couple * (al_nb_pac == 0) +
            al.R0.taux1pac * (al_nb_pac == 1) +
            al.R0.taux2pac * (al_nb_pac == 2) +
            al.R0.taux3pac * (al_nb_pac == 3) +
            al.R0.taux4pac * (al_nb_pac == 4) +
            al.R0.taux5pac * (al_nb_pac == 5) +
            al.R0.taux6pac * (al_nb_pac == 6) +
            al.R0.taux_pac_supp * (al_nb_pac > 6) * (al_nb_pac - 6)
            )

        return R0


class aide_logement_taux_famille(Variable):
    value_type = float
    entity = Famille
    label = u"Taux représentant la situation familiale, décroissant avec le nombre de personnes à charge"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        TF_metropole = (
            al.taux_participation_fam.taux_1_adulte * (not_(couple)) * (al_nb_pac == 0) +
            al.taux_participation_fam.taux_2_adulte * (couple) * (al_nb_pac == 0) +
            al.taux_participation_fam.taux_1_enf * (al_nb_pac == 1) +
            al.taux_participation_fam.taux_2_enf * (al_nb_pac == 2) +
            al.taux_participation_fam.taux_3_enf * (al_nb_pac == 3) +
            al.taux_participation_fam.taux_4_enf * (al_nb_pac >= 4) +
            al.taux_participation_fam.taux_enf_supp * (al_nb_pac > 4) * (al_nb_pac - 4)
            )

        TF_dom = (
            al.taux_participation_fam.dom.taux1 * (not_(couple)) * (al_nb_pac == 0) +
            al.taux_participation_fam.dom.taux2 * (couple) * (al_nb_pac == 0) +
            al.taux_participation_fam.dom.taux3 * (al_nb_pac == 1) +
            al.taux_participation_fam.dom.taux4 * (al_nb_pac == 2) +
            al.taux_participation_fam.dom.taux5 * (al_nb_pac == 3) +
            al.taux_participation_fam.dom.taux6 * (al_nb_pac == 4) +
            al.taux_participation_fam.dom.taux7 * (al_nb_pac == 5) +
            al.taux_participation_fam.dom.taux8 * (al_nb_pac >= 6)
            )

        return where(residence_dom, TF_dom, TF_metropole)


class aide_logement_taux_loyer(Variable):
    value_type = float
    entity = Famille
    label = u"Taux obscur basé sur une comparaison du loyer retenu à un loyer de référence."
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        z2 = al.loyers_plafond.par_zone.zone_2

        L = famille('aide_logement_loyer_retenu', period)
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)

        loyer_reference = (
            z2.personnes_seules * (not_(couple)) * (al_nb_pac == 0) +
            z2.couples * (couple) * (al_nb_pac == 0) +
            z2.un_enfant * (al_nb_pac >= 1) +
            z2.majoration_par_enf_supp * (al_nb_pac > 1) * (al_nb_pac - 1)
            )

        RL = L / loyer_reference

        # TODO: paramètres en dur ??
        TL = where(RL >= 0.75,
            al.taux_participation_loyer.taux_tranche_3 * (RL - 0.75) + al.taux_participation_loyer.taux_tranche_2 * (0.75 - 0.45),
            max_(0, al.taux_participation_loyer.taux_tranche_2 * (RL - 0.45))
            )

        return TL


class aide_logement_participation_personnelle(Variable):
    value_type = float
    entity = Famille
    label = u"Participation personelle de la famille au loyer"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement

        R = famille('aide_logement_base_ressources', period)
        R0 = famille('aide_logement_R0', period)
        Rp = max_(0, R - R0)

        loyer_retenu = famille('aide_logement_loyer_retenu', period)
        charges_retenues = famille('aide_logement_charges', period)
        E = loyer_retenu + charges_retenues
        P0 = max_(al.participation_min.taux * E, al.participation_min.montant_forfaitaire)  # Participation personnelle minimale

        Tf = famille('aide_logement_taux_famille', period)
        Tl = famille('aide_logement_taux_loyer', period)
        Tp = Tf + Tl  # Taux de participation

        return P0 + Tp * Rp


class aide_logement_montant_brut_avant_degressivite(Variable):
    value_type = float
    label = u"Montant des aides aux logements en secteur locatif avant degressivité et brut de CRDS"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        locataire = (
            (statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
            )
        accedant = (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)

        loyer_retenu = famille('aide_logement_loyer_retenu', period)
        charges_retenues = famille('aide_logement_charges', period)
        participation_personnelle = famille('aide_logement_participation_personnelle', period)

        montant_locataire = max_(0, loyer_retenu + charges_retenues - participation_personnelle)
        montant_accedants = famille('aides_logement_primo_accedant', period)

        montant = select([locataire, accedant], [montant_locataire, montant_accedants])

        montant = montant * (montant >= al.al_min.montant_min_mensuel.montant_min_apl_al)  # Montant minimal de versement

        return montant


class aide_logement_montant_brut(Variable):
    value_type = float
    entity = Famille
    label = u"Montant des aides au logement après degressivité, avant CRDS"
    definition_period = MONTH

    def formula(famille, period):
        montant_avant_degressivite = famille('aide_logement_montant_brut_avant_degressivite', period)
        return montant_avant_degressivite

    def formula_2016_07_01(famille, period):
        montant_avant_degressivite = famille('aide_logement_montant_brut_avant_degressivite', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)
        loyer_degressivite = famille('aide_logement_loyer_seuil_degressivite', period)
        loyer_suppression = famille('aide_logement_loyer_seuil_suppression', period)
        handicap_i = famille.members('handicap', period)
        handicap = famille.any(handicap_i)

        coeff = select(
            [loyer_reel <= loyer_degressivite, loyer_reel <= loyer_suppression, loyer_reel > loyer_suppression],
            [1, 1 - ((loyer_reel - loyer_degressivite) / (loyer_suppression - loyer_degressivite)), 0]
            )

        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        accedant = (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)
        locataire_foyer = (statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
        exception = accedant + locataire_foyer + handicap
        coeff = where(exception, 1, coeff)

        montant = round_(montant_avant_degressivite * coeff, 2)

        return montant


class aide_logement_montant(Variable):
    value_type = float
    entity = Famille
    label = u"Montant des aides au logement net de CRDS"
    definition_period = MONTH

    def formula(famille, period):
        aide_logement_montant_brut = famille('aide_logement_montant_brut', period)
        crds_logement = famille('crds_logement', period)
        montant = round_(aide_logement_montant_brut + crds_logement, 2)

        return montant


class alf(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Allocation logement familiale"
    reference = u"http://vosdroits.service-public.fr/particuliers/F13132.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        result = (al_nb_pac >= 1) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) * aide_logement_montant
        return result


class als_non_etudiant(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement sociale (non étudiante)"
    definition_period = MONTH

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        etudiant = famille.members('etudiant', period)
        no_parent_etudiant = not_(famille.any(etudiant, role = Famille.PARENT))

        return (
            (al_nb_pac == 0) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) *
            no_parent_etudiant * aide_logement_montant
            )

class als_etudiant(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Allocation logement sociale (étudiante)"
    reference = u"https://www.caf.fr/actualites/2012/etudiants-tout-savoir-sur-les-aides-au-logement"
    definition_period = MONTH

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)

        etudiant = famille.members('etudiant', period)
        parent_etudiant = famille.any(etudiant, role = Famille.PARENT)

        return (
            (al_nb_pac == 0) * (statut_occupation_logement != 3) * not_(proprietaire_proche_famille) *
            parent_etudiant * aide_logement_montant
        )

class als(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Allocation logement sociale"
    reference = u"http://vosdroits.service-public.fr/particuliers/F1280.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        als_non_etudiant = famille('als_non_etudiant', period)
        als_etudiant = famille('als_etudiant', period)
        result = (als_non_etudiant + als_etudiant)

        return result


class apl(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Aide personnalisée au logement"
    # (réservée aux logements conventionné, surtout des HLM, et financé par le fonds national de l'habitation)"
    reference = u"http://vosdroits.service-public.fr/particuliers/F12006.xhtml",
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)

        return aide_logement_montant * (statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)


class TypesAideLogementNonCalculable(Enum):
    __order__ = 'calculable locataire_foyer'  # Needed to preserve the enum order in Python 2
    calculable = u"Calculable"
    locataire_foyer = u"Non calculable (Locataire foyer)"


class aide_logement_non_calculable(Variable):
    value_type = Enum
    possible_values = TypesAideLogementNonCalculable
    default_value = TypesAideLogementNonCalculable.calculable
    entity = Famille
    label = u"Aide au logement non calculable"
    definition_period = MONTH

    def formula(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)

        return where(
            statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer,
            TypesAideLogementNonCalculable.locataire_foyer,
            TypesAideLogementNonCalculable.calculable
            )


class aide_logement(Variable):
    value_type = float
    entity = Famille
    label = u"Aide au logement (tout type)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        apl = famille('apl', period)
        als = famille('als', period)
        alf = famille('alf', period)

        return max_(max_(apl, als), alf)


class crds_logement(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"CRDS des allocations logement"
    reference = u"http://vosdroits.service-public.fr/particuliers/F17585.xhtml"
    definition_period = MONTH

    def formula(famille, period, parameters):
        aide_logement_montant_brut = famille('aide_logement_montant_brut', period)
        crds = parameters(period).prestations.prestations_familiales.af.crds
        return -aide_logement_montant_brut * crds


class zone_apl(Variable):
    value_type = Enum
    possible_values = TypesZoneApl   # defined in model/base.py
    default_value = TypesZoneApl.zone_2
    entity = Menage
    label = u"Zone APL"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period):
        '''
        Retrouve la zone APL (aide personnalisée au logement) de la commune
        en fonction du depcom (code INSEE)
        '''
        depcom = menage('depcom', period)

        preload_zone_apl()
        default_value = 2
        zone = fromiter(
            (
                zone_apl_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom
                ),
            dtype = int16,
            )
        return select(
            (zone == 1, zone == 2, zone == 3),
            # The .index is not striclty necessary, but it improves perfomances by avoiding a later encoding
            (TypesZoneApl.zone_1.index, TypesZoneApl.zone_2.index, TypesZoneApl.zone_3.index)
        )


def preload_zone_apl():
    global zone_apl_by_depcom
    if zone_apl_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/20110914_zonage.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            zone_apl_by_depcom = {
                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
                row['CODGEO']: int(row['Zonage'][0])
                for row in csv_reader
                }
        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/commune_depcom_by_subcommune_depcom.json',
                ) as json_file:
            commune_depcom_by_subcommune_depcom = json.load(json_file)
            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
                zone_apl_by_depcom[subcommune_depcom] = zone_apl_by_depcom[commune_depcom]

class aides_logement_primo_accedant(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula_2007_07(famille, period, parameters):
        loyer = famille.demandeur.menage('loyer', period)
        plafond_mensualite = famille('aides_logement_primo_accedant_plafond_mensualite', period)
        L = min_(loyer, plafond_mensualite)
        C = famille('aide_logement_charges', period)
        K = famille('aides_logement_primo_accedant_k', period)
        Lo = famille('aides_logement_primo_accedant_loyer_minimal', period)

        return K * max_(0, (L + C - Lo))

class aides_logement_primo_accedant_k(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants K"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        coef_k = parameters(period).prestations.al_param_accal.constante_du_coefficient_k
        multi_n = parameters(period).prestations.al_param_accal.multiplicateur_de_n
        R = famille('aides_logement_primo_accedant_ressources', period)
        N = famille('aides_logement_primo_accedant_nb_part', period)

        return coef_k - ( R / (multi_n * N))

class  aides_logement_primo_accedant_nb_part(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants nombre de part"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        prestations = parameters(period).prestations
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)

        return (
           prestations.al_param_accal.n_0_personnes_a_charge.isole * not_(couple) * (al_nb_pac == 0) +
           prestations.al_param_accal.n_0_personnes_a_charge.menage * couple * (al_nb_pac == 0) +
           prestations.al_param.parametre_n['1_personne_a_charge'] * (al_nb_pac == 1) +
           prestations.al_param.parametre_n['2_personnes_a_charge'] * (al_nb_pac == 2) +
           prestations.al_param.parametre_n['3_personnes_a_charge'] * (al_nb_pac == 3) +
           prestations.al_param.parametre_n['4_personnes_a_charge'] * (al_nb_pac >= 4) +
           prestations.al_param.majoration_n_par_personne_a_charge_supplementaire * (al_nb_pac > 4) * (al_nb_pac - 4)
         )

class  aides_logement_primo_accedant_loyer_minimal(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants loyer minimal"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        prestations = parameters(period).prestations
        bareme = prestations.al_param_accal.bareme_loyer_minimun_lo
        baseRessource = famille('aides_logement_primo_accedant_ressources', period)
        majoration_loyer = prestations.al_param.majoration_du_loyer_minimum_lo
        N = famille('aides_logement_primo_accedant_nb_part', period)

        return (bareme.calc(baseRessource / N) * N + majoration_loyer) / 12

class aides_logement_primo_accedant_plafond_mensualite(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants plafond mensualité"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006737237&cidTexte=LEGITEXT000006073189&dateTexte=20170811"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al_plaf_acc = parameters(period).prestations.al_plafonds_accession
        zone_apl = famille.demandeur.menage('zone_apl', period)

        plafonds = al_plaf_acc[zone_apl]

        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)

        return (
           plafonds.personne_isolee_sans_enfant * not_(couple) * (al_nb_pac == 0) +
           plafonds.menage_seul * couple * (al_nb_pac == 0) +
           plafonds.menage_ou_isole_avec_1_enfant * (al_nb_pac == 1) +
           plafonds.menage_ou_isole_avec_2_enfants * (al_nb_pac == 2) +
           plafonds.menage_ou_isole_avec_3_enfants * (al_nb_pac == 3) +
           plafonds.menage_ou_isole_avec_4_enfants * (al_nb_pac == 4) +
           plafonds.menage_ou_isole_avec_5_enfants * (al_nb_pac >= 5) +
           plafonds.menage_ou_isole_par_enfant_en_plus * (al_nb_pac > 5) * (al_nb_pac - 5)
         )

class  aides_logement_primo_accedant_ressources(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation logement pour les primo-accédants ressources"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=0E9C46E37CA82EB75BD1482030D54BB5.tpdila18v_2?idArticle=LEGIARTI000021632291&cidTexte=LEGITEXT000006074096&dateTexte=20170623&categorieLien=id&oldAction="
    definition_period = MONTH

    def formula(famille, period, parameters):
        baseRessource = famille('aide_logement_base_ressources', period)
        loyer = famille.demandeur.menage('loyer', period)
        coef_plancher_ressources = parameters(period).prestations.aides_logement.ressources.dar_3
        return max_(baseRessource, loyer * coef_plancher_ressources)
