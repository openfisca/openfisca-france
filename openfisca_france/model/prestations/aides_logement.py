# -*- coding: utf-8 -*-

import csv
import codecs
import json
import logging
import pkg_resources
import sys

from numpy import ceil, datetime64, fromiter, int16, logical_or as or_, logical_and as and_, logical_not as not_

import openfisca_france
from openfisca_core.periods import Instant

from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


log = logging.getLogger(__name__)


class aide_logement(Variable):
    value_type = float
    entity = Famille
    label = "Aide au logement (tout type)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        apl = famille('apl', period)
        als = famille('als', period)
        alf = famille('alf', period)

        return max_(max_(apl, als), alf)


class apl(Variable):
    documentation = "Réservée aux logements conventionnés, surtout des HLM, et financée par le fonds national de l'habitation."
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "Aide personnalisée au logement"
    reference = "http://vosdroits.service-public.fr/particuliers/F12006.xhtml",
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)

        return aide_logement_montant * logement_conventionne


class als(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "Allocation logement sociale"
    reference = "http://vosdroits.service-public.fr/particuliers/F1280.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)

        return (al_nb_pac == 0) * not_(logement_conventionne) * not_(proprietaire_proche_famille) * aide_logement_montant


class alf(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "Allocation logement familiale"
    reference = "http://vosdroits.service-public.fr/particuliers/F13132.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        aide_logement_montant = famille('aide_logement_montant', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        proprietaire_proche_famille = famille('proprietaire_proche_famille', period)
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)

        return (al_nb_pac >= 1) * not_(logement_conventionne) * not_(proprietaire_proche_famille) * aide_logement_montant


class aide_logement_montant(Variable):
    value_type = float
    entity = Famille
    label = "Montant des aides au logement net de CRDS"
    definition_period = MONTH

    def formula(famille, period):
        aide_logement_montant_brut = famille('aide_logement_montant_brut_crds', period)
        crds_logement = famille('crds_logement', period)
        montant = round_(aide_logement_montant_brut + crds_logement, 2)

        return montant


class aide_logement_montant_brut_crds(Variable):
    value_type = float
    entity = Famille
    label = "Montant des aides au logement brut de CRDS"
    reference = "https://www.legifrance.gouv.fr/eli/decret/2018/2/27/2018-136/jo/article_1"
    definition_period = MONTH

    def formula_2018(famille, period, parameters):
        rls = parameters(period).prestations.reduction_loyer_solidarite
        aide_logement_montant_brut = famille('aide_logement_montant_brut', period)
        reduction_loyer_solidarite = famille('reduction_loyer_solidarite', period)

        taux_rls = rls.fraction_baisse_aide_logement
        rls_apl = reduction_loyer_solidarite * taux_rls

        return max_(0, (aide_logement_montant_brut - rls_apl))

    def formula(famille, period, parameters):
        return famille('aide_logement_montant_brut', period)


class aide_logement_montant_brut(Variable):
    value_type = float
    entity = Famille
    label = "Montant des aides au logement après degressivité et abattement forfaitaire, avant CRDS"
    reference = "https://www.legifrance.gouv.fr/eli/decret/2017/9/28/TERL1721632D/jo/texte"
    definition_period = MONTH

    def formula_2016_07_01(famille, period, parameters):
        montant_avant_degressivite = famille('aide_logement_montant_brut_avant_degressivite', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)
        zone_apl = famille.demandeur.menage('zone_apl', period)
        loyer_plafond = famille('aide_logement_loyer_plafond', period)

        coefficients = parameters(period).prestations.aides_logement.loyers_plafond.par_zone[zone_apl]
        loyer_degressivite = round_(loyer_plafond * (coefficients.degressivite), 2)
        loyer_suppression = round_(loyer_plafond * (coefficients.suppression), 2)

        coeff = select(
            [loyer_reel <= loyer_degressivite, loyer_reel <= loyer_suppression, loyer_reel > loyer_suppression],
            [1, 1 - ((loyer_reel - loyer_degressivite) / (loyer_suppression - loyer_degressivite)), 0]
            )

        handicap_i = famille.members('handicap', period)
        handicap = famille.any(handicap_i)

        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        accedant = (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)
        locataire_foyer = (statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
        exception = accedant + locataire_foyer + handicap
        coeff = where(exception, 1, coeff)

        montant_avant_degressivite_et_coeff = round_(montant_avant_degressivite * coeff, 2)

        abattement_forfaitaire = parameters(period).prestations.aides_logement.autres.abattement_forfaitaire

        return max_(0, montant_avant_degressivite_et_coeff - abattement_forfaitaire)

    def formula(famille, period):
        return famille('aide_logement_montant_brut_avant_degressivite', period)


class aide_logement_montant_brut_avant_degressivite(Variable):
    value_type = float
    label = "Montant des aides aux logements en secteur locatif avant degressivité et brut de CRDS"
    reference = "https://www.legifrance.gouv.fr/eli/arrete/2018/2/27/TERL1801552A/jo/article_1"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        locataire = ((statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble))

        accedant = famille.demandeur.menage('aides_logement_primo_accedant_eligibilite', period)

        locataire_logement_foyer = statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer

        loyer_retenu = famille('aide_logement_loyer_retenu', period)
        charges_retenues = famille('aide_logement_charges', period)
        participation_personnelle = famille('aide_logement_participation_personnelle', period)

        montant_accedant_et_foyer = famille('aides_logement_accedant_et_foyer', period)
        montant_locataire = max_(0, loyer_retenu + charges_retenues - participation_personnelle)

        montant = select([locataire, accedant + locataire_logement_foyer],
                         [montant_locataire, montant_accedant_et_foyer])

        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        type_aide = where(logement_conventionne, 'apl', 'non_apl', )
        seuil_versement = al.al_min.montant_min_mensuel.montant_min_apl_al[type_aide]
        minimum_atteint = montant >= seuil_versement

        return minimum_atteint * montant


class TypeEtatLogementFoyer(Enum):
    non_renseigne = "Non renseigne"
    logement_rehabilite = "Logement rehabilité"
    logement_non_rehabilite = "Logement non rehabilité"


class etat_logement_foyer(Variable):
    value_type = Enum
    possible_values = TypeEtatLogementFoyer
    entity = Menage
    default_value = TypeEtatLogementFoyer.non_renseigne
    label = "Etat du logement crous"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class logement_conventionne(Variable):
    value_type = bool
    entity = Menage
    label = "Logement conventionné"
    definition_period = MONTH


class TypeEtatLogement(Enum):
    order__ = ' non_renseigne construction_acquisition_logement_neuf travaux_amelioration_residence_principale agrandissement_amenagement acquisition_amelioration acquisition_sans_amelioration_logement_existant amelioration'  # Needed to preserve the enum order in Python 2
    non_renseigne = "Non renseigné"
    # Logement neuf
    construction_acquisition_logement_neuf = "Construction Acquisition d'un logement NEUF"
    # Logement ancien
    acquisition_amelioration = "Acquisition Amélioration"
    acquisition_sans_amelioration_logement_existant = "Acquisition sans amélioration d'un logement existant"
    amelioration = "Amélioration"
    agrandissement_amenagement = "Agrandissement Aménagement"


class etat_logement(Variable):
    value_type = Enum
    possible_values = TypeEtatLogement  # defined in model/base.py
    entity = Menage
    default_value = TypeEtatLogement.non_renseigne
    label = "Etat du logement"
    reference = "http://www.msa.fr/lfy/documents/11566/48471/Certificat+de+pret+pour+APL.pdf"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class aide_logement_date_pret_conventionne(Variable):
    value_type = date
    default_value = date.max
    entity = Menage
    label = "Date de contraction du prêt conventionné "
    definition_period = ETERNITY


class date_debut_chomage(Variable):
    value_type = date
    default_value = date.max
    entity = Individu
    label = "Date de début de chômage"
    definition_period = ETERNITY


class aides_logement_primo_accedant_eligibilite(Variable):
    value_type = bool
    default_value = False
    entity = Menage
    reference = "https://www.legifrance.gouv.fr/eli/loi/2017/12/30/CPAX1723900L/jo/article_126"
    definition_period = MONTH

    def formula(menage, period):
        statut_occupation_logement = menage('statut_occupation_logement', period)
        accedant = (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)

        zone_apl = menage('zone_apl', period)
        aide_logement_etat_logement = menage('etat_logement', period)
        aide_logement_date_pret_conventionne = menage('aide_logement_date_pret_conventionne', period)
        est_logement_ancien = (
            (aide_logement_etat_logement == TypeEtatLogement.acquisition_amelioration)
            + (aide_logement_etat_logement == TypeEtatLogement.acquisition_sans_amelioration_logement_existant)
            + (aide_logement_etat_logement == TypeEtatLogement.amelioration)
            + (aide_logement_etat_logement == TypeEtatLogement.agrandissement_amenagement)
            )

        est_zone_3 = (zone_apl == TypesZoneApl.zone_3)
        date_pret_conventionne_avant_2018_01 = (aide_logement_date_pret_conventionne < date(2018, 1, 1))
        date_pret_conventionne_avant_2020_01 = (aide_logement_date_pret_conventionne < date(2020, 1, 1))

        eligibilite = select(
            [date_pret_conventionne_avant_2018_01, date_pret_conventionne_avant_2020_01],
            [True, (est_logement_ancien * est_zone_3)], default = False
            )

        return accedant * eligibilite


class aides_logement_foyer_chambre_non_rehabilite_eligibilite(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        logement_crous = famille.demandeur.menage('logement_crous', period)
        etat_logement_foyer = famille.demandeur.menage('etat_logement_foyer', period)
        logement_chambre = famille.demandeur.menage('logement_chambre', period)

        return (
            logement_crous
            * not_(logement_conventionne)
            * (logement_chambre * (etat_logement_foyer == TypeEtatLogementFoyer.logement_non_rehabilite))
            )


class aides_logement_foyer_personne_agee_eligibilite(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        aides_logement_foyer_personne_agee_eligibilite = not_(logement_conventionne) * (famille.demandeur('age', period) >= 62)

        return aides_logement_foyer_personne_agee_eligibilite


class al_nb_personnes_a_charge(Variable):
    value_type = int
    entity = Famille
    label = "Nombre de personne à charge au sens des allocations logement"
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
                ((taux_incapacite > taux_incapacite_minimum) + inapte_travail)
                * (age >= age_max_enfant)
                * (base_ressources_i <= plafond_ressource)
                )

            # Par convention les adultes handicapé à charge de la famille ont le role ENFANT dans la famille
            # Le demandeur et son conjoint ne sont jamais considérés comme à charge
            return famille.sum(adulte_handicape, role = Famille.ENFANT)

        nb_pac = al_nb_enfants() + al_nb_adultes_handicapes()
        nb_pac = where(residence_dom, min_(nb_pac, 6), nb_pac)
        # Dans les DOMs, le barème est fixe à partir de 6 enfants.

        return nb_pac


class aide_logement_base_ressources_patrimoine(Variable):
    value_type = float
    label = "Base de ressources des revenus du patrimoine des aides au logement"
    entity = Famille
    reference = "https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000033243725&categorieLien=id"
    definition_period = MONTH

    def formula_2016_10_01(famille, period, parameters):
        '''
        Exclusion des titulaires de l'AAH, AEEH et des personnes résidant en EHPAD :
        'Les personnes titulaires de l’AAH ainsi que les personnes âgées dépendantes en EHPAD
        ne sont pas concernées par la mesure.'
        Lien: http://www.cohesion-territoires.gouv.fr/IMG/pdf/160923_edl_apl_detailles_patrimoine.pdf
        '''
        livret_a_i = famille.members('livret_a', period)
        livret_a = famille.sum(livret_a_i)
        epargne_revenus_non_imposables_i = famille.members('epargne_revenus_non_imposables', period)
        epargne_revenus_non_imposables = famille.sum(epargne_revenus_non_imposables_i)
        epargne_revenus_imposables_i = famille.members('epargne_revenus_imposables', period)
        epargne_revenus_imposables = famille.sum(epargne_revenus_imposables_i)

        valeur_patrimoine_loue_i = famille.members('valeur_patrimoine_loue', period)
        valeur_patrimoine_loue = famille.sum(valeur_patrimoine_loue_i)
        valeur_immo_non_loue_i = famille.members('valeur_immo_non_loue', period)
        valeur_immo_non_loue = famille.sum(valeur_immo_non_loue_i)
        valeur_terrains_non_loues_i = famille.members('valeur_terrains_non_loues', period)
        valeur_terrains_non_loues = famille.sum(valeur_terrains_non_loues_i)

        valeur_locative_immo_non_loue_i = famille.members('valeur_locative_immo_non_loue', period)
        valeur_locative_immo_non_loue = famille.sum(valeur_locative_immo_non_loue_i)
        valeur_locative_terrains_non_loues_i = famille.members('valeur_locative_terrains_non_loues', period)
        valeur_locative_terrains_non_loues = famille.sum(valeur_locative_terrains_non_loues_i)

        # Les abatements sont les mêmes que pour le RSA
        abattements = parameters(period).prestations.minima_sociaux.rsa.patrimoine

        capitaux_non_productifs = livret_a + epargne_revenus_non_imposables
        foncier = valeur_patrimoine_loue + valeur_immo_non_loue + valeur_terrains_non_loues

        patrimoine = epargne_revenus_imposables + capitaux_non_productifs + foncier

        statut_logement = famille.demandeur.menage("statut_occupation_logement", period)
        est_locataire_foyer = (statut_logement == TypesStatutOccupationLogement.locataire_foyer)
        membres_famille_percoit_aah = famille.members('aah', period) > 0
        famille_percoit_aah = famille.any(membres_famille_percoit_aah)
        famille_percoit_aeeh = famille('aeeh', period) > 0

        seuil_valorisation = parameters(period).prestations.aides_logement.patrimoine.seuil_valorisation

        return not_(est_locataire_foyer) * not_(famille_percoit_aah) * not_(famille_percoit_aeeh) * (
            (patrimoine > seuil_valorisation) * (
                + capitaux_non_productifs * abattements.taux_interet_forfaitaire_epargne_non_imposable
                + valeur_locative_immo_non_loue * abattements.abattement_valeur_locative_immo_non_loue
                + valeur_locative_terrains_non_loues * abattements.abattement_valeur_locative_terrains_non_loues
                )
            )


class al_couple(Variable):
    value_type = bool
    entity = Famille
    label = 'Situation de couple pour le calcul des AL'
    definition_period = MONTH

    def formula(famille, period):
        en_couple = famille('en_couple', period)
        enceinte = famille('enceinte_fam', period)
        couple = en_couple + enceinte  # le barème "couple" est utilisé pour les femmes enceintes isolées

        return couple


class aide_logement_base_ressources_eval_forfaitaire(Variable):
    value_type = float
    entity = Famille
    label = "Base ressources en évaluation forfaitaire des aides au logement (R351-7 du CCH)"
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
    label = "Assiette sur lequel un abattement chômage peut être appliqués pour les AL. Ce sont les revenus d'activité professionnelle, moins les abbattements pour frais professionnels."
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
    label = "Montant de l'abattement pour personnes au chômage indemnisé (R351-13 du CCH)"
    definition_period = MONTH
    # Article R532-7 du Code de la sécurité sociale
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000031694522&cidTexte=LEGITEXT000006073189"

    def formula(individu, period, parameters):
        activite = individu('activite', period)
        date_debut_chomage = individu('date_debut_chomage', period)
        two_months_ago = datetime64(period.offset(-2, 'month').start)
        condition_abattement = (activite == TypesActivite.chomeur) * (date_debut_chomage < two_months_ago)
        revenus_activite_pro = individu('aide_logement_assiette_abattement_chomage', period.n_2)
        taux_abattement = parameters(period).prestations.aides_logement.ressources.abattement_chomage_indemnise

        return condition_abattement * taux_abattement * revenus_activite_pro


class aide_logement_abattement_depart_retraite(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'abattement sur les salaires en cas de départ en retraite"
    definition_period = MONTH
    # Article R532-5 du Code de la sécurité sociale
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006750910&cidTexte=LEGITEXT000006073189&dateTexte=20151231"

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
    label = "Abattement sur les revenus n-2 pour les bénéficiaires du RSA"
    definition_period = MONTH
    reference = [
        # Article R532-7 du Code de la sécurité sociale
        "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000031694522&cidTexte=LEGITEXT000006073189",
        # Article R351-14-1 du Code de la construction et de l'habitation
        "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006074096&idArticle=LEGIARTI000006897410"
        ]

    def formula(famille, period, parameters):
        # Circular definition, as rsa depends on al.
        # We don't allow it, so default value of rsa will be returned if a recursion is detected.
        rsa_mois_dernier = famille('rsa', period.last_month)

        revenus_a_neutraliser_i = famille.members('revenu_assimile_salaire_apres_abattements', period.n_2)
        revenus_a_neutraliser = famille.sum(revenus_a_neutraliser_i)

        return revenus_a_neutraliser * (rsa_mois_dernier > 0)


class aide_logement_base_ressources_defaut(Variable):
    value_type = float
    entity = Famille
    label = "Base ressource par défaut des allocations logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        biactivite = famille('biactivite', period)
        Pr = parameters(period).prestations.aides_logement.ressources
        base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
        base_ressources_parents = famille.sum(base_ressources_i, role = Famille.PARENT)
        ressources_patrimoine = famille('aide_logement_base_ressources_patrimoine', period)
        abattement_chomage_indemnise_i = famille.members('aide_logement_abattement_chomage_indemnise', period)
        abattement_chomage_indemnise = famille.sum(abattement_chomage_indemnise_i, role = Famille.PARENT)
        abattement_depart_retraite_i = famille.members('aide_logement_abattement_depart_retraite', period)
        abattement_depart_retraite = famille.sum(abattement_depart_retraite_i, role = Famille.PARENT)
        neutralisation_rsa = famille('aide_logement_neutralisation_rsa', period)
        abattement_ressources_enfant = parameters(period.n_2.stop).prestations.minima_sociaux.aspa.plafond_ressources_seul * 1.25
        base_ressources_enfants = famille.sum(
            max_(0, base_ressources_i - abattement_ressources_enfant), role = Famille.ENFANT)

        demandeur_declarant_principal = famille.demandeur.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        conjoint_declarant_principal = famille.conjoint.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        # Revenus du foyer fiscal
        aide_logement_base_revenus_fiscaux = (
            famille.demandeur.foyer_fiscal('aide_logement_base_revenus_fiscaux', period.n_2) * demandeur_declarant_principal
            + famille.conjoint.foyer_fiscal('aide_logement_base_revenus_fiscaux', period.n_2) * conjoint_declarant_principal
            )

        ressources = (
            base_ressources_parents
            + base_ressources_enfants
            + ressources_patrimoine
            + aide_logement_base_revenus_fiscaux
            - (abattement_chomage_indemnise + abattement_depart_retraite + neutralisation_rsa)
            )

        # Abattement forfaitaire pour double activité
        abattement_double_activite = biactivite * Pr.dar_1

        # Arrondi aux 100 euros supérieurs
        result = max_(ressources - abattement_double_activite, 0)

        return result


class aide_logement_base_revenus_fiscaux(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenus fiscaux perçus par le foyer fiscal à prendre en compte dans la base ressource des aides au logement"
    reference = [
        "Code de la construction et de l'habitation - Article R351-5",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=F039735F667F9271DFB284F78105BDC0.tplgfr31s_3?idArticle=LEGIARTI000021632267&cidTexte=LEGITEXT000006074096&dateTexte=20171123",
        "Code de la sécurité sociale - Article R831-6",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=9A3FFF4142B563EB5510DDE9F2870BF4.tplgfr41s_2?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000020080073&dateTexte=20171222&categorieLien=cid#LEGIARTI000020080073",
        "Code de la sécurité sociale - Article D542-10",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=F1CF3B807CE064C9F518B442EF8C856F.tpdila22v_1?idArticle=LEGIARTI000020986758&cidTexte=LEGITEXT000006073189&dateTexte=20170803&categorieLien=id&oldAction=&nbResultRech="
        ]
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        # Supprimée à partir de 2018
        rev_cat_rvcm = foyer_fiscal('revenu_categoriel_capital', period)
        # Supprimée à partir de 2018
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        # Apparait à partir de 2018
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        revenu_categoriel_foncier = foyer_fiscal('revenu_categoriel_foncier', period)
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        # Supprimée à partir de 2018
        rev_cat_pv = foyer_fiscal('revenu_categoriel_plus_values', period)
        # Apparait à partir de 2018
        plus_values_prelevement_forfaitaire_unique_ir = foyer_fiscal('plus_values_prelevement_forfaitaire_unique_ir', period)

        abat_spe = foyer_fiscal('abat_spe', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        invV, invC = caseP, caseF
        naissanceP = foyer_fiscal.declarant_principal('date_naissance', period)
        naissanceC = foyer_fiscal.conjoint('date_naissance', period)
        dateLimite = datetime64('1931-01-01')
        apply_abat_spe = (abat_spe > 0) * (invV + invC + (naissanceP < dateLimite) + (naissanceC < dateLimite))

        return (
            + revenu_categoriel_foncier
            + pensions_alimentaires_versees
            + rente_viagere_titre_onereux_net
            + rev_cat_rvcm
            + revenus_capitaux_prelevement_liberatoire
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + rev_cat_pv
            + plus_values_prelevement_forfaitaire_unique_ir
            - abat_spe * apply_abat_spe
            - f7ga
            - f7gb
            - f7gc
            )


class aide_logement_base_ressources(Variable):
    value_type = float
    entity = Famille
    label = "Base ressources des allocations logement"
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
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        montant_plancher_ressources = (statut_occupation_logement != TypesStatutOccupationLogement.locataire_foyer) * max_(0, demandeur_etudiant * Pr.dar_4 - demandeur_boursier * Pr.dar_5)
        montant_plancher_ressources_logement_foyer = (statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer) * max_(0, demandeur_etudiant * Pr.dar_11 - demandeur_boursier * Pr.dar_12)
        ressources = max_(ressources, max_(montant_plancher_ressources, montant_plancher_ressources_logement_foyer))

        # Arrondi au centime, pour éviter qu'une petite imprécision liée à la recombinaison d'une valeur annuelle éclatée ne fasse monter d'un cran l'arrondi au 100€ supérieur.

        ressources = round_(ressources * 100) / 100

        # Arrondi aux 100 euros supérieurs
        ressources = ceil(ressources / 100) * 100

        accedant = famille.demandeur.menage('aides_logement_primo_accedant_eligibilite', period)
        plancher = famille.demandeur.menage('aides_logement_primo_accedant_ressources', period)

        return where(accedant, max_(ressources, plancher), ressources)


class aides_logement_primo_accedant_ressources(Variable):
    value_type = float
    entity = Menage
    label = "Allocation logement pour les primo-accédants, plancher de ressources"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=0E9C46E37CA82EB75BD1482030D54BB5.tpdila18v_2?idArticle=LEGIARTI000021632291&cidTexte=LEGITEXT000006074096&dateTexte=20170623&categorieLien=id&oldAction="
    definition_period = MONTH

    def formula(menage, period, parameters):
        loyer = menage('loyer', period)
        coef_plancher_ressources = parameters(period).prestations.aides_logement.ressources.dar_3
        return loyer * coef_plancher_ressources


class aide_logement_loyer_plafond(Variable):
    value_type = float
    entity = Famille
    label = "Loyer plafond dans le calcul des aides au logement (L2)"
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


class aide_logement_loyer_reel(Variable):
    value_type = float
    entity = Famille
    label = "Loyer réel dans le calcul des aides au logement"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=F2CE61DFFD9BD9F08700031784123828.tplgfr28s_2?idArticle=LEGIARTI000006737243&cidTexte=LEGITEXT000006073189&categorieLien=id&dateTexte="
    definition_period = MONTH

    def formula(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        loyer = famille.demandeur.menage('loyer', period)
        categorie_apl = famille.demandeur.menage('logement_conventionne', period)
        logement_chambre = famille.demandeur.menage('logement_chambre', period)
        locataire_meuble = statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble

        # Coeff de 2/3 pour les logements meublés pour l'AL
        coeff_meuble_al = where(locataire_meuble, 2 / 3, 1)
        # Coeff de 2/3 pour les seules chambres meublées pour l'APL
        coeff_meuble_apl = where(locataire_meuble * logement_chambre, 2 / 3, 1)
        return where(categorie_apl, round_(loyer * coeff_meuble_apl), round_(loyer * coeff_meuble_al))


class aide_logement_loyer_retenu(Variable):
    value_type = float
    entity = Famille
    label = "Loyer retenu (hors charge) dans le calcul des aides au logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        loyer_plafond = famille('aide_logement_loyer_plafond', period)
        loyer_reel = famille('aide_logement_loyer_reel', period)

        # loyer retenu
        return min_(loyer_reel, loyer_plafond)


class aide_logement_charges(Variable):
    value_type = float
    entity = Famille
    label = "Charges retenues dans le calcul des aides au logement"
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
    label = "Revenu de référence, basé sur la situation familiale, pris en compte dans le calcul des AL."
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        pfam_n_2 = parameters(period.start.offset(-2, 'year')).prestations.prestations_familiales
        minim_n_2 = parameters(period.start.offset(-2, 'year')).prestations.minima_sociaux
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        n_2 = period.start.offset(-2, 'year')
        if n_2.date >= date(2009, 6, 1):
            montant_de_base = minim_n_2.rsa.montant_de_base_du_rsa
        else:
            montant_de_base = minim_n_2.rmi.montant_de_base_du_rmi

        R1 = montant_de_base * (
            al.r1.personne_isolee * not_(couple) * (al_nb_pac == 0)
            + al.r1.couple_sans_enf * couple * (al_nb_pac == 0)
            + al.r1.personne_isolee_ou_couple_avec_1_enf * (al_nb_pac == 1)
            + al.r1.personne_isolee_ou_couple_avec_2_enf * (al_nb_pac >= 2)
            + al.r1.majoration_enfant_a_charge_supp * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R2 = pfam_n_2.af.bmaf * (
            al.r2.taux3_dom * residence_dom * (al_nb_pac == 1)
            + al.r2.personnes_isolees_ou_couples_avec_2_enf * (al_nb_pac >= 2)
            + al.r2.majoration_par_enf_supp_a_charge * (al_nb_pac > 2) * (al_nb_pac - 2)
            )

        R0 = round_(12 * (R1 - R2) * (1 - al.autres.abat_sal))

        return R0

    # cf Décret n° 2014-1739 du 29 décembre 2014 relatif au calcul des aides personnelles au logement
    def formula_2015_01_01(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)

        R0 = (
            al.R0.taux_seul * not_(couple) * (al_nb_pac == 0)
            + al.R0.taux_couple * couple * (al_nb_pac == 0)
            + al.R0.taux1pac * (al_nb_pac == 1)
            + al.R0.taux2pac * (al_nb_pac == 2)
            + al.R0.taux3pac * (al_nb_pac == 3)
            + al.R0.taux4pac * (al_nb_pac == 4)
            + al.R0.taux5pac * (al_nb_pac == 5)
            + al.R0.taux6pac * (al_nb_pac == 6)
            + al.R0.taux_pac_supp * (al_nb_pac > 6) * (al_nb_pac - 6)
            )

        return R0


class aide_logement_taux_famille(Variable):
    value_type = float
    entity = Famille
    label = "Taux représentant la situation familiale, décroissant avec le nombre de personnes à charge"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        residence_dom = famille.demandeur.menage('residence_dom', period)

        TF_metropole = (
            al.taux_participation_fam.taux_1_adulte * (not_(couple)) * (al_nb_pac == 0)
            + al.taux_participation_fam.taux_2_adulte * (couple) * (al_nb_pac == 0)
            + al.taux_participation_fam.taux_1_enf * (al_nb_pac == 1)
            + al.taux_participation_fam.taux_2_enf * (al_nb_pac == 2)
            + al.taux_participation_fam.taux_3_enf * (al_nb_pac == 3)
            + al.taux_participation_fam.taux_4_enf * (al_nb_pac >= 4)
            + al.taux_participation_fam.taux_enf_supp * (al_nb_pac > 4) * (al_nb_pac - 4)
            )

        TF_dom = (
            al.taux_participation_fam.dom.taux1 * (not_(couple)) * (al_nb_pac == 0)
            + al.taux_participation_fam.dom.taux2 * (couple) * (al_nb_pac == 0)
            + al.taux_participation_fam.dom.taux3 * (al_nb_pac == 1)
            + al.taux_participation_fam.dom.taux4 * (al_nb_pac == 2)
            + al.taux_participation_fam.dom.taux5 * (al_nb_pac == 3)
            + al.taux_participation_fam.dom.taux6 * (al_nb_pac == 4)
            + al.taux_participation_fam.dom.taux7 * (al_nb_pac == 5)
            + al.taux_participation_fam.dom.taux8 * (al_nb_pac >= 6)
            )

        return where(residence_dom, TF_dom, TF_metropole)


class aide_logement_taux_loyer(Variable):
    value_type = float
    entity = Famille
    label = "Taux obscur basé sur une comparaison du loyer retenu à un loyer de référence."
    definition_period = MONTH

    def formula(famille, period, parameters):
        al = parameters(period).prestations.aides_logement
        z2 = al.loyers_plafond.par_zone.zone_2

        L = famille('aide_logement_loyer_retenu', period)
        couple = famille('al_couple', period)
        al_nb_pac = famille('al_nb_personnes_a_charge', period)

        loyer_reference = (
            z2.personnes_seules * (not_(couple)) * (al_nb_pac == 0)
            + z2.couples * (couple) * (al_nb_pac == 0)
            + z2.un_enfant * (al_nb_pac >= 1)
            + z2.majoration_par_enf_supp * (al_nb_pac > 1) * (al_nb_pac - 1)
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
    label = "Participation personelle de la famille au loyer"
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


class TypesAideLogementNonCalculable(Enum):
    __order__ = 'calculable locataire_foyer'  # Needed to preserve the enum order in Python 2
    calculable = "Calculable"
    locataire_foyer = "Non calculable (Locataire foyer)"


class aide_logement_non_calculable(Variable):
    value_type = Enum
    possible_values = TypesAideLogementNonCalculable
    default_value = TypesAideLogementNonCalculable.calculable
    entity = Famille
    label = "Aide au logement non calculable"
    definition_period = MONTH

    def formula(famille, period):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)

        return where(
            statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer,
            TypesAideLogementNonCalculable.locataire_foyer,
            TypesAideLogementNonCalculable.calculable
            )


class crds_logement(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "CRDS des allocations logement"
    reference = "http://vosdroits.service-public.fr/particuliers/F17585.xhtml"
    definition_period = MONTH

    def formula(famille, period, parameters):
        aide_logement_montant_brut = famille('aide_logement_montant_brut_crds', period)
        crds = parameters(period).prestations.prestations_familiales.af.crds
        return -aide_logement_montant_brut * crds


class TypesZoneApl(Enum):
    __order__ = 'non_renseigne zone_1 zone_2 zone_3'  # Needed to preserve the enum order in Python 2
    non_renseigne = "Non renseigné"
    zone_1 = "Zone 1"
    zone_2 = "Zone 2"
    zone_3 = "Zone 3"


zone_apl_by_depcom = None


def preload_zone_apl():
    global zone_apl_by_depcom
    if zone_apl_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/20110914_zonage.csv',
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
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
            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.items():
                zone_apl_by_depcom[subcommune_depcom] = zone_apl_by_depcom[commune_depcom]


class zone_apl(Variable):
    value_type = Enum
    possible_values = TypesZoneApl
    default_value = TypesZoneApl.zone_2
    entity = Menage
    label = "Zone APL"
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
                zone_apl_by_depcom.get(depcom_cell if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8'), default_value)
                for depcom_cell in depcom
                ),
            dtype = int16,
            )
        return select(
            (zone == 1, zone == 2, zone == 3),
            # The .index is not striclty necessary, but it improves perfomances by avoiding a later encoding
            (TypesZoneApl.zone_1.index, TypesZoneApl.zone_2.index, TypesZoneApl.zone_3.index)
            )


class aides_logement_accedant_et_foyer(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les primo-accédants"
    reference = ["https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid",
                 "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000035671385&dateTexte=&categorieLien=id",
                 "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=8A5E748B84270643BC39A1D691F4FC5C.tplgfr27s_2?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006739837&dateTexte=20181031&categorieLien=cid#LEGIARTI000006739837"
                 ]
    definition_period = MONTH

    def formula_2007_07(famille, period, parameters):
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        accedant = (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)
        locataire_logement_foyer = statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        forfait_charges = accedant + (locataire_logement_foyer * not_(logement_conventionne))

        loyer = famille.demandeur.menage('loyer', period)
        plafond_mensualite = famille('aides_logement_plafond_mensualite', period)
        L = where(locataire_logement_foyer * not_(logement_conventionne), plafond_mensualite, min_(plafond_mensualite, loyer))
        C = forfait_charges * famille('aide_logement_charges', period)
        K = famille('aides_logement_k', period)
        Lo = famille('aides_logement_loyer_minimal', period)

        return (L > 0) * K * max_(0, (L + C - Lo))


class aides_logement_k(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers loyer minimal"
    reference = ["https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006074096&idArticle=LEGIARTI000006898932&dateTexte=&categorieLien=cid",
                 "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"]
    definition_period = MONTH

    def formula(famille, period, parameters):
        accedant = famille.demandeur.menage('aides_logement_primo_accedant_eligibilite', period)
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        coef_k_accedant = famille('aides_logement_primo_accedant_k', period)
        coef_k_apl = famille('aides_logement_foyer_k_apl', period)
        coef_k_al = famille('aides_logement_foyer_k_al', period)
        return select([accedant, logement_conventionne], [coef_k_accedant, coef_k_apl], coef_k_al)


class aides_logement_primo_accedant_k(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les primo-accédants K"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        param = parameters(period).prestations.al_param_accal

        coef_k = param.constante_du_coefficient_k
        multi_n = param.multiplicateur_de_n

        R = famille('aide_logement_base_ressources', period)
        N = famille('aides_logement_nb_part', period)

        return coef_k - (R / (multi_n * N))


class aides_logement_foyer_k_al(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers loyer minimal"
    reference = ["https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006074096&idArticle=LEGIARTI000006898932&dateTexte=&categorieLien=cid",
                 "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"]
    definition_period = MONTH

    def formula(famille, period, parameters):
        param = parameters(period).prestations.al_param_accal
        param2 = parameters(period).prestations.al_param

        coef_k = param.constante_du_coefficient_k
        multi_n = param2.multiplicateur_de_n_dans_la_formule_de_k

        R = famille('aide_logement_base_ressources', period)
        N = famille('aides_logement_nb_part', period)

        return coef_k - (R / (multi_n * N))


class aides_logement_foyer_k_apl(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers loyer minimal"
    reference = ["https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006074096&idArticle=LEGIARTI000006898932&dateTexte=&categorieLien=cid",
                 "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"]
    definition_period = MONTH

    def formula(famille, period, parameters):
        param = parameters(period).prestations.al_param_accal
        param1 = parameters(period).prestations.al_param_accapl.multiplicateur_de_n

        r_apl1 = param1.dans_la_formule_de_kl_numerateur

        coef_k = param.constante_du_coefficient_k_apl1
        multi_n = param1.dans_la_formule_de_kl

        R = famille('aide_logement_base_ressources', period)
        N = famille('aides_logement_nb_part', period)

        return coef_k - (((R - (r_apl1 * N))) / (multi_n * N))


class aides_logement_categorie(Variable):
    value_type = str
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        categorie_apl = famille.demandeur.menage('logement_conventionne', period)
        return where(categorie_apl, 'apl', 'al')


class aides_logement_nb_part(Variable):
    value_type = float
    entity = Famille
    label = "Nombre de parts (paramètre N) pour l'aide au logement"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)

        categorie = famille('aides_logement_categorie', period)
        params = parameters(period).prestations.al_param.parametre_n[categorie]

        return (
            params['isole_0_personne_a_charge'] * not_(couple) * (al_nb_pac == 0)
            + params['menage_0_personnes_a_charge'] * couple * (al_nb_pac == 0)
            + params['1_personne_a_charge'] * (al_nb_pac == 1)
            + params['2_personnes_a_charge'] * (al_nb_pac == 2)
            + params['3_personnes_a_charge'] * (al_nb_pac == 3)
            + params['4_personnes_a_charge'] * (al_nb_pac >= 4)
            + params['majoration_n_par_personne_a_charge_supplementaire'] * (al_nb_pac > 4) * (al_nb_pac - 4)
            )


class aides_logement_loyer_minimal(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers loyer minimal"
    reference = "https://www.legifrance.gouv.fr/eli/arrete/2007/11/8/MLVU0759263A/jo/article_2"
    definition_period = MONTH

    def formula(famille, period, parameters):
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        loyer_al = famille('aides_logement_loyer_minimal_al', period)
        loyer_apl = famille('aides_logement_loyer_minimal_apl', period)
        return where(logement_conventionne, loyer_apl, loyer_al)


class aides_logement_loyer_minimal_al(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement loyer minimal"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737341&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(famille, period, parameters):
        N = famille('aides_logement_nb_part', period)

        prestations = parameters(period).prestations
        bareme = prestations.al_param_accal.bareme_loyer_minimum_lo
        majoration_loyer = prestations.al_param.majoration_du_loyer_minimum_lo

        baseRessource = famille('aide_logement_base_ressources', period)

        return (bareme.calc(baseRessource / N) * N + majoration_loyer) / 12


class aides_logement_loyer_minimal_apl(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers loyer minimal"
    reference = "https://www.legifrance.gouv.fr/eli/arrete/2007/11/8/MLVU0759263A/jo/article_2"
    definition_period = MONTH

    # Temporairement limitée à après 2007-11 pour pallier des carences de valeurs de paramètres
    def formula_2007_11_01(famille, period, parameters):
        N = famille('aides_logement_nb_part', period)

        prestations = parameters(period).prestations
        bareme = prestations.al_param_accal.bareme_loyer_minimum_lo_apl1
        majoration_loyer = prestations.al_param_accal.majoration_du_loyer_minimum_lo_apl1 * N

        baseRessource = famille('aide_logement_base_ressources', period)

        return (bareme.calc(baseRessource / N) * N + majoration_loyer) / 12


class aides_logement_plafond_mensualite(Variable):
    value_type = float
    entity = Famille
    label = "Plafond de mensualités (formule commune)"
    definition_period = MONTH

    def formula(famille, period, parameters):
        accedant = famille.demandeur.menage('aides_logement_primo_accedant_eligibilite', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        locataire_logement_foyer = statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer

        aides_accedants = famille('aides_logement_primo_accedant_plafond_mensualite', period)
        aides_foyer = famille('aides_logement_foyer_plafond_mensualite', period)

        return select([accedant, locataire_logement_foyer], [aides_accedants, aides_foyer])


class aides_logement_primo_accedant_plafond_mensualite(Variable):
    value_type = float
    entity = Famille
    label = "Allocation logement pour les primo-accédants plafond mensualité"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006737237&cidTexte=LEGITEXT000006073189&dateTexte=20170811"
    definition_period = MONTH

    def formula(famille, period, parameters):
        zone_apl = famille.demandeur.menage('zone_apl', period)
        plafonds = parameters(period).prestations.al_plafonds_accession[zone_apl]

        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)

        return (
            plafonds.personne_isolee_sans_enfant * not_(couple) * (al_nb_pac == 0)
            + plafonds.menage_seul * couple * (al_nb_pac == 0)
            + plafonds.menage_ou_isole_avec_1_enfant * (al_nb_pac == 1)
            + plafonds.menage_ou_isole_avec_2_enfants * (al_nb_pac == 2)
            + plafonds.menage_ou_isole_avec_3_enfants * (al_nb_pac == 3)
            + plafonds.menage_ou_isole_avec_4_enfants * (al_nb_pac == 4)
            + plafonds.menage_ou_isole_avec_5_enfants * (al_nb_pac >= 5)
            + plafonds.menage_ou_isole_par_enfant_en_plus * (al_nb_pac > 5) * (al_nb_pac - 5)
            )


class aides_logement_foyer_conventionne_plafond(Variable):

    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers plafond"
    reference = "https://www.legifrance.gouv.fr/eli/arrete/2017/9/28/TERL1725443A/jo/article_11"
    definition_period = MONTH

    def formula(famille, period, parameters):
        zone_apl = famille.demandeur.menage('zone_apl', period)
        plafonds = parameters(period).prestations.al_plafonds_logement_foyer.conventionne[zone_apl]

        al_nb_pac = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)

        return (
            plafonds.personne_isolee_sans_enfant * not_(couple) * (al_nb_pac == 0)
            + plafonds.menage_seul * couple * (al_nb_pac == 0)
            + plafonds.menage_ou_isole_avec_1_enfant * (al_nb_pac == 1)
            + plafonds.menage_ou_isole_avec_2_enfants * (al_nb_pac == 2)
            + plafonds.menage_ou_isole_avec_3_enfants * (al_nb_pac == 3)
            + plafonds.menage_ou_isole_avec_4_enfants * (al_nb_pac == 4)
            + plafonds.menage_ou_isole_par_enfant_en_plus * (al_nb_pac > 4) * (al_nb_pac - 4)
            )


class aides_logement_foyer_plafond_mensualite(Variable):

    value_type = float
    entity = Famille
    label = "Allocation logement pour les logements foyers plafond mensualité"
    reference = ["https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000035665875&dateTexte=&categorieLien=id",
                 "https://www.legifrance.gouv.fr/eli/arrete/2017/9/28/TERL1725443A/jo/article_11"]
    definition_period = MONTH

    # Temporairement limitée à après 2017 pour pallier des carences de valeurs de paramètres
    def formula_2017_10(famille, period, parameters):
        plafond_crous = parameters(period).prestations.al_plafonds_logement_foyer_crous
        plafond_foyer = parameters(period).prestations.al_plafonds_logement_foyer

        statut_couple = where(famille('al_couple', period), 'couple', 'personne_isolee')

        foyer_plafond = plafond_crous.rehabilitee[statut_couple]
        foyer_chambre_non_rehabilite_plafond = plafond_crous.non_rehabilitee[statut_couple]
        foyer_personne_agee_plafond = plafond_foyer.personne_agee[statut_couple]

        foyer_conventionne_plafond = famille('aides_logement_foyer_conventionne_plafond', period)

        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        foyer_chambre_non_rehabilite_eligibilite = famille('aides_logement_foyer_chambre_non_rehabilite_eligibilite', period)
        foyer_personne_agee_eligibilite = famille('aides_logement_foyer_personne_agee_eligibilite', period)

        return select(
            [foyer_personne_agee_eligibilite, foyer_chambre_non_rehabilite_eligibilite, logement_conventionne],
            [foyer_personne_agee_plafond, foyer_chambre_non_rehabilite_plafond, foyer_conventionne_plafond],
            default = foyer_plafond
            )
