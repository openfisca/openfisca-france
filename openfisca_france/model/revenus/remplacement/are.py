from numpy import ceil, floor, round, busday_count, datetime64, maximum, minimum, timedelta64, where

from openfisca_core.periods import Period

from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesMotifFinContrat

from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.remplacement import TypesTauxCSGRemplacement

from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import (
    montant_csg_crds
    )

# Commentaires :
# - Règles  issues de la convention d’assurance chômage du 15 novembre 2024 - appliquée depuis le 1er janvier/1er avril 2025 : à compléter à terme
# - Règles explicitées dans la CIRCULAIRE n° 2025-03 du 1er avril 2025 de l'Unédic

# - Contrat débute au début d'un mois et finit à la fin d'un mois
# - Salarié privé, pas de formation, hors cas particuliers
# - Pas de possibilité de mélanger ARE et reprise d'emploi pour le moment (ou toute autre activité) : version la plus simpliste du simulateur
# - Calculs non reliés au reste du système (prestations, impôts etc.)
# - Revalorisation des salaires non considérée pour le calcul du SR
# - Calculs/fonctions CSG/CRDS repris d'une modélisation précédente
# - Contrats successifs avec pause(s) : le module de calcul ne décompte pas les jours qui auraient pu être indemnisés durant ces pauses (on repart à 0 à chaque fin de contrat)
# - Date naissance nécessaire pour le moment
# - Pas d'intégration des arrêts maladie etc.

# - Logique de calcul ici utilisée :
# -- Etablissement des paramètres d'ouverture de droits le mois suivant la fin d'un contrat
# -- "Gel" des dates de début/fin d'indemnisation/durée nette
# -- "Gel" du SJR pour le calcul des allocations mensuelles
# -- Logique à revoir : les boucles internes aux variables ci-dessus ne sont pas nécessairement ultra lisibles

# - Une partie des paramètres existaient déjà dans des sous-dossiers de 'allocations_assurance_chomage' : j'ai recrée un dossier avec tous les paramètres de l'ARE (hors CSG/CRDS)


MAX_MOIS_PRC = 36
MAX_MOIS_ARE = 36


class are_age_fin_contrat(Variable):
    value_type = int
    entity = Individu
    label = "Âge de l'individu à la date de fin du dernier contrat de travail"
    definition_period = MONTH

    def formula(individu, period):
        date_naissance = individu('date_naissance', period)
        fin_dernier_contrat = individu('fin_dernier_contrat', period)

        annee_fin  = fin_dernier_contrat.astype('datetime64[Y]')
        annee_nais = date_naissance.astype('datetime64[Y]')

        delta_annee = annee_fin.astype(int) - annee_nais.astype(int)

        mois_fin  = fin_dernier_contrat.astype('datetime64[M]').astype(int) % 12 + 1
        mois_nais = date_naissance.astype('datetime64[M]').astype(int) % 12 + 1

        jour_fin  = (fin_dernier_contrat - fin_dernier_contrat.astype('datetime64[M]')).astype(int) + 1
        jour_nais = (date_naissance - date_naissance.astype('datetime64[M]')).astype(int) + 1

        anniversaire_non_passe = (
            (mois_fin < mois_nais) |
            ((mois_fin == mois_nais) & (jour_fin < jour_nais))
        )

        return where(anniversaire_non_passe, delta_annee - 1, delta_annee)


class are_periode_reference_affiliation(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de mois précédent la fin du contrat à considérer pour déterminer l'éligibilité à l'ARE"
    definition_period = MONTH
    unit = 'month'
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 3']

    def formula(individu, period, parameters):
        fin_dernier_contrat = individu('fin_dernier_contrat', period)
        fin_default_value = datetime64(date(2099, 12, 31))
        avec_contrat = fin_dernier_contrat != fin_default_value

        age_fin_contrat = individu('are_age_fin_contrat', period)
        age_seuil = parameters(period).chomage.allocations_assurance_chomage.are.eligibilite.categorie_age
        periode_affiliation = parameters(period).chomage.allocations_assurance_chomage.are.eligibilite.periode_reference_affiliation

        return where(age_fin_contrat >= age_seuil,
                     periode_affiliation.seconde_categorie,
                     periode_affiliation.premiere_categorie) * avec_contrat


# On suppose ici que l'on fait le bilan le mois suivant la fin du dernier contrat
class are_debut_prc(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date de début de la période de référence calcul (PRC)"
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 3']

    def formula(individu, period):
        periode_consideree = individu('are_periode_reference_affiliation', period)

        default_date = datetime64(date(1870, 1, 1))
        result = individu.get_holder('are_debut_prc').default_array()

        for i in range(MAX_MOIS_PRC, 0, -1):
            dans_periode = i <= periode_consideree
            a_travaille = individu('salaire_de_base', period.offset(-i, 'month')) > 0

            debut_contrat = individu('contrat_de_travail_debut', period.offset(-i, 'month'))
            debut_mois = datetime64(period.offset(-i, 'month').start)

            date_candidate = maximum(debut_contrat, debut_mois)
            result = where(dans_periode * a_travaille * (result == default_date), date_candidate, result)

        return result


class are_jours_travailles(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours d'affiliation/travaillés sur la période de référence ARE"
    unit = 'day'
    definition_period = MONTH

    def formula(individu, period):
        periode_consideree = individu('are_periode_reference_affiliation', period)

        def jours_travailles(i):
            salaire = individu('salaire_de_base', period.offset(-i, 'month'))
            quotite = individu('quotite_de_travail', period.offset(-i, 'month'))

            jours_travail = individu('nombre_jours_travailles', period.offset(-i, 'month'))
            return (salaire > 0) * quotite * jours_travail

        return sum([
            jours_travailles(i) * (i <= periode_consideree)
            for i in range(MAX_MOIS_PRC, 0, -1)
        ]).astype(int)


class are_jours_prc(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours calendaires sur la prc"
    unit = 'day'
    definition_period = MONTH

    def formula(individu, period):
        date_debut_prc = individu('are_debut_prc', period)
        fin_dernier_contrat = individu('fin_dernier_contrat', period)

        fin_default_value = datetime64(date(2099, 12, 31))
        avec_contrat = fin_dernier_contrat != fin_default_value

        return (fin_dernier_contrat + timedelta64(1, 'D') - date_debut_prc).astype('timedelta64[D]').astype(int) * avec_contrat


class are_eligible_ouverture(Variable):
    value_type = bool
    entity = Individu
    label = "Conditions d'ouverture des droits ARE (motif + affiliation, sans condition de période d'indemnisation)"
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Articles 2 et 3']
    
    def formula(individu, period, parameters):
        fin_dernier_contrat = individu('fin_dernier_contrat', period)
        sans_contrat = fin_dernier_contrat < datetime64(period.start)

        motif = individu('motif_fin_dernier_contrat', period)
        motif_eligible = (
            (motif == TypesMotifFinContrat.licenciement)
            + (motif == TypesMotifFinContrat.fin_cdd)
            + (motif == TypesMotifFinContrat.rupture_conventionnelle)
            + (motif == TypesMotifFinContrat.demission_legitime)
            ).astype(bool)

        jours_travailles = individu('are_jours_travailles', period)
        seuil_jours_travailles = parameters(period).chomage.allocations_assurance_chomage.are.eligibilite.duree_minimale_affiliation.jours_travailles

        return motif_eligible * (jours_travailles >= seuil_jours_travailles) * sans_contrat


# Il s'agit ici de récupérer la valeur d'éligibilité ARE au moment de l'ouverture
class are_debut_indemnisation(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date de début de l'indemnisation ARE"
    definition_period = MONTH

    def formula(individu, period):
        fin_contrat = individu('fin_dernier_contrat', period)
        default = datetime64(date(1870, 1, 1))
        fin_contrat_default = datetime64(date(2099, 12, 31))

        # M0 = premier jour du mois suivant la fin du contrat
        mois_m0 = fin_contrat.astype('datetime64[M]') + 1
        debut_candidate = mois_m0.astype('datetime64[D]')

        mois_courant = datetime64(period.start).astype('datetime64[M]').astype(int)
        delta = mois_courant - mois_m0.astype(int)

        eligible_a_m0 = individu.filled_array(False)
        for i in range(0, MAX_MOIS_ARE):
            eligible_a_m0 = where(
                delta == i,
                individu('are_eligible_ouverture', period.offset(-i, 'month')),
                eligible_a_m0
            )

        return where(
            (fin_contrat != fin_contrat_default) & eligible_a_m0,
            debut_candidate,
            default
        )


class are_duree_max_indemnisation(Variable):
    value_type = int
    entity = Individu
    label = "Durée maximale d'indemnisation ARE selon la catégorie d'âge"
    unit = 'day'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 9']
    
    def formula(individu, period, parameters):
        params = parameters(period).chomage.allocations_assurance_chomage.are.duree_indemnisation
        age_fin_contrat = individu('are_age_fin_contrat', period)

        fin_contrat = individu('fin_dernier_contrat', period)
        fin_contrat_default = datetime64(date(2099, 12, 31))
        avec_contrat = fin_contrat != fin_contrat_default

        return where(
            age_fin_contrat < params.categorie_age.max_premiere_categorie,
            params.duree_maximale_indemnisation.premiere_categorie,
            where(
                age_fin_contrat < params.categorie_age.max_seconde_categorie,
                params.duree_maximale_indemnisation.seconde_categorie,
                params.duree_maximale_indemnisation.troisieme_categorie
            )
        ) * avec_contrat


class are_duree_brute_indemnisation(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours d'indemnisation, sans coefficient de conjoncture et seuil/plafond"
    definition_period = MONTH
    unit = 'day'
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 9']
    
    def formula(individu, period, parameters):
        max_inactivite = parameters(period).chomage.allocations_assurance_chomage.are.duree_indemnisation.plafonnement_inactivite
        jours_travailles = individu('are_jours_travailles', period)
        jours_prc = individu('are_jours_prc', period)
        jours_travailles_calendaires = ceil(jours_travailles * 1.4)

        jours_non_travailles_prc = jours_prc - jours_travailles_calendaires

        duree_brute = (
            jours_travailles_calendaires
            + min_(jours_non_travailles_prc, floor(jours_travailles_calendaires * max_inactivite))
        )

        return duree_brute


class are_duree_nette_indemnisation(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours d'indemnisation, avec coefficient de conjoncture et seuil/plafond"
    definition_period = MONTH
    unit = 'day'
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 9']

    def formula(individu, period, parameters):
        duree_brute = individu('are_duree_brute_indemnisation', period)
        coef_conjoncture = parameters(period).chomage.allocations_assurance_chomage.are.duree_indemnisation.coefficient_conjoncture
        duree_min = parameters(period).chomage.allocations_assurance_chomage.are.duree_indemnisation.duree_minimale_indemnisation
        duree_max = individu('are_duree_max_indemnisation', period)

        fin_contrat = individu('fin_dernier_contrat', period)
        fin_contrat_default = datetime64(date(2099, 12, 31))
        avec_contrat = fin_contrat != fin_contrat_default

        return max_(
            min_(ceil(duree_brute * coef_conjoncture).astype(int), duree_max),
            duree_min) * avec_contrat


# Il s'agit ici de récupérer la valeur au moment de l'ouverture
class are_duree_nette_gelee(Variable):
    value_type = int
    entity = Individu
    label = "Durée nette d'indemnisation ARE gelée à la date d'ouverture des droits"
    unit = 'day'
    definition_period = MONTH

    def formula(individu, period):
        debut = individu('are_debut_indemnisation', period)
        default = datetime64(date(1870, 1, 1))

        debut_mois = debut.astype('datetime64[M]').astype(int)
        mois_courant = datetime64(period.start).astype('datetime64[M]').astype(int)
        delta = mois_courant - debut_mois

        result = individu.filled_array(0)
        for i in range(0, MAX_MOIS_ARE):
            result = where(
                (delta == i) & (debut != default),
                individu('are_duree_nette_indemnisation', period.offset(-i, 'month')),
                result
            )
        return result


class are_fin_indemnisation(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date de fin de l'indemnisation ARE"
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 9']
    
    def formula(individu, period):
        debut = individu('are_debut_indemnisation', period)
        default = datetime64(date(1870, 1, 1))
        duree_j = individu('are_duree_nette_gelee', period)

        duree_m = duree_j // 30
        duree_j_reliquat = duree_j - duree_m * 30

        mois_fin_debut = (debut.astype('datetime64[M]') + duree_m.astype('timedelta64[M]'))
        mois_suivant_fin = (mois_fin_debut + timedelta64(1, 'M'))

        nb_jours_dernier_mois = (mois_suivant_fin.astype('datetime64[D]') - mois_fin_debut.astype('datetime64[D]')).astype(int)

        fin = where(duree_j_reliquat > nb_jours_dernier_mois,
                    mois_fin_debut.astype('datetime64[D]') + (nb_jours_dernier_mois - 1).astype('timedelta64[D]'),
                    mois_fin_debut.astype('datetime64[D]') + (duree_j_reliquat - 1).astype('timedelta64[D]'))
            
        return where(debut != default, fin, default)


class are_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'Allocation de Retour à l'Emploi (ARE)"
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 9']

    def formula(individu, period):
        debut = individu('are_debut_indemnisation', period)
        fin = individu('are_fin_indemnisation', period)
        default = datetime64(date(1870, 1, 1))

        dans_periode = (
            (debut != default) &
            (datetime64(period.start) >= debut) &
            (datetime64(period.start) <= fin)
        )
        sans_remuneration = individu('salaire_de_base', period) == 0

        return dans_periode * sans_remuneration


class are_sr(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de référence (SJR) utilisé pour l'ARE"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 11']

    def formula(individu, period, parameters):
        periode_consideree = individu('are_periode_reference_affiliation', period)

        def salaire_plafonne(i):
            salaire = individu('salaire_de_base', period.offset(-i, 'month'))
            pmss = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_mensuel
            return minimum(salaire, 4 * pmss)

        return sum([
            salaire_plafonne(i) * (i <= periode_consideree)
            for i in range(MAX_MOIS_PRC, 0, -1)
        ])


class are_duree_calcul_sjr(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours utilisés pour le diviseur dans le calcul du SJR"
    definition_period = MONTH
    unit = 'day'
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 13']

    def formula(individu, period, parameters):
        duree_brute = individu('are_duree_brute_indemnisation', period)
        duree_min = parameters(period).chomage.allocations_assurance_chomage.are.duree_indemnisation.duree_minimale_indemnisation
        duree_max = individu('are_duree_max_indemnisation', period)

        fin_contrat = individu('fin_dernier_contrat', period)
        fin_contrat_default = datetime64(date(2099, 12, 31))
        avec_contrat = fin_contrat != fin_contrat_default

        return max_(
            min_(duree_brute.astype(int), duree_max),duree_min) * avec_contrat


class are_sjr(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence (SJR) calculé pour l'ARE"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 13']

    def formula(individu, period):
        salaire_reference = individu('are_sr', period)
        duree_retenue = individu('are_duree_calcul_sjr', period)

        return where(duree_retenue > 0, round_(salaire_reference / duree_retenue, 2), 0)

# Il s'agit ici de récupérer la valeur au moment de l'ouverture : à modifier à terme pour intégrer les revalorisations des rémunérations
class are_sjr_gele(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence (SJR) gelé à la date d'ouverture des droits ARE"
    unit = 'currency'
    definition_period = MONTH

    def formula(individu, period):
        debut = individu('are_debut_indemnisation', period)
        default = datetime64(date(1870, 1, 1))

        debut_mois = debut.astype('datetime64[M]').astype(int)
        mois_courant = datetime64(period.start).astype('datetime64[M]').astype(int)
        delta = mois_courant - debut_mois

        result = individu.filled_array(0.)
        for i in range(0, MAX_MOIS_ARE):
            result = where(
                (delta == i) & (debut != default),
                individu('are_sjr', period.offset(-i, 'month')),
                result
            )
        return result


class are_date_debut_degressivite(Variable):
    value_type = date
    default_value = date(2099, 12, 31)
    entity = Individu
    label = "Date à partir de laquelle la dégressivité ARE s'applique (2099-12-31 si inapplicable)"
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 17bis']

    def formula(individu, period, parameters):
        params_deg = parameters(period).chomage.allocations_assurance_chomage.are.degressivite
        params_alloc = parameters(period).chomage.allocations_assurance_chomage.are.allocation

        debut = individu('are_debut_indemnisation', period)
        fin = individu('are_fin_indemnisation', period)
        default_debut = datetime64(date(1870, 1, 1))
        default_deg = datetime64(date(2099, 12, 31))
        sjr = individu('are_sjr_gele', period)
        age = individu('are_age_fin_contrat', period)

        alloc_pleine = maximum(
            params_alloc.partie_fixe + params_alloc.partie_prop * sjr,
            params_alloc.pourcentage_sjr_seuil * sjr
        )
        alloc_pleine = minimum(alloc_pleine, params_alloc.pourcentage_sjr_plafond * sjr)

        jours_deg = params_deg.jours_application

        duree_m_deg = jours_deg // 30
        duree_j_reliquat_deg = jours_deg % 30

        date_deg = (
            debut.astype('datetime64[M]') + timedelta64(duree_m_deg, 'M')
        ).astype('datetime64[D]') + timedelta64(duree_j_reliquat_deg, 'D')

        conditions = (
            (debut != default_debut) &
            (age < params_deg.age_application) &
            (alloc_pleine >= params_deg.montant_minimum_application) &
            (date_deg <= fin)
        )

        return where(conditions, date_deg, default_deg)


class are_smic_journalier(Variable):
    value_type = float
    entity = Individu
    label = "Montant du smic brut journalier : smic horaire * 5 (35h étant sur 7 jours)"
    unit = 'currency'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period, parameters):
        smic_h = parameters(period).marche_travail.salaire_minimum.smic.smic_b_horaire

        return ceil(5 * smic_h)

## TAUX PLEIN
class are_allocation_journaliere_super_brute_tx_plein(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière super brute de l'ARE à taux plein, avant toute déduction"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Articles 14 à 16']

    def formula(individu, period, parameters):
        params_alloc = parameters(period).chomage.allocations_assurance_chomage.are.allocation

        sjr = individu('are_sjr_gele', period)

        alloc_pleine = maximum(
            params_alloc.partie_fixe + params_alloc.partie_prop * sjr,
            params_alloc.pourcentage_sjr_seuil * sjr
        )
        alloc_pleine = minimum(alloc_pleine, params_alloc.pourcentage_sjr_plafond * sjr)

        return individu('are_eligible', period) * round_(alloc_pleine,2)


class are_retraires_complementaires_tx_plein(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la participation au financement des retraites complémentaires pour l'allocation à taux plein"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 19']

    def formula(individu, period, parameters):
        super_brute = individu('are_allocation_journaliere_super_brute_tx_plein', period)
        sjr = individu('are_sjr_gele', period)

        taux = parameters(period).chomage.allocations_assurance_chomage.are.prelevements.retraites_complementaires
        seuil = parameters(period).chomage.allocations_assurance_chomage.are.allocation.minimum_hors_mayotte

        return - max_(min_(super_brute - seuil, round(taux * sjr, 2)), 0)


class are_allocation_journaliere_brute_tx_plein(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière brute de l'ARE à taux plein, après éventuelle déduction de PRC"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Articles 14 à 16']

    def formula(individu, period, parameters):
        super_brute = individu('are_allocation_journaliere_super_brute_tx_plein', period)
        prc = individu('are_retraires_complementaires_tx_plein', period)

        return individu('are_eligible', period) * (super_brute + prc)

# Calculs en partie repris d'une précédente modélisation de l'ARE : probablement quelques cas limites et pas ultra lisible
# L'ordre d'application correspond à ma compréhension de la CIRCULAIRE UNEDIC (et aux tests FT)
class are_csg_deductible_tx_plein(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG déductible sur les allocations chômage (taux plein)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        brute = individu('are_allocation_journaliere_brute_tx_plein', period)

        montant_csg_ded_th = -round(montant_csg_crds(
            base_avec_abattement = brute,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.deductible,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ), 2)

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute - smic_j, montant_csg_ded_th), 0)


class are_csg_non_deductible_tx_plein(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG non déductible sur les allocations chômage (taux plein)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        csg_ded = individu('are_csg_deductible_tx_plein', period)

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        brute = individu('are_allocation_journaliere_brute_tx_plein', period)

        montant_csg_non_ded_th = -round(montant_csg_crds(
            base_avec_abattement = brute,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.imposable,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ), 2)

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute + csg_ded - smic_j, montant_csg_non_ded_th), 0)


class are_crds_tx_plein(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CRDS sur les allocations chômage (taux plein)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        csg_ded = individu('are_csg_deductible_tx_plein', period)
        csg_non_ded = individu('are_csg_non_deductible_tx_plein', period)

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        eligible = (
            (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit)
            + (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein)
            )

        brute = individu('are_allocation_journaliere_brute_tx_plein', period)

        montant_crds_th = -round(montant_csg_crds(
                base_avec_abattement = brute,
                abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
                law_node = parameters.prelevements_sociaux.contributions_sociales.crds,
                plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
                ), 2) * eligible

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute + csg_ded + csg_non_ded - smic_j, montant_crds_th), 0)


class are_allocation_nette_journaliere_tx_plein(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière nette de l'ARE (taux plein), après déduction des prélèvements"
    unit = 'currency'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period):
        brut = individu('are_allocation_journaliere_brute_tx_plein', period)
        csg_deductible = individu('are_csg_deductible_tx_plein', period)
        csg_non_deductible = individu('are_csg_non_deductible_tx_plein', period)
        crds = individu('are_crds_tx_plein', period)

        return individu('are_eligible', period) * (brut + csg_deductible + csg_non_deductible + crds)


## TAUX DEGRESSIF
class are_allocation_journaliere_super_brute_tx_deg(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière super brute de l'ARE à taux dégressif, avant toute déduction"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Articles 14 à 16 + 17bis']

    def formula(individu, period, parameters):
        params_deg = parameters(period).chomage.allocations_assurance_chomage.are.degressivite
        taux_deg = params_deg.taux
        montant_min = params_deg.montant_minimum_application

        alloc_tx_plein = individu('are_allocation_journaliere_super_brute_tx_plein', period)

        date_deg = individu('are_date_debut_degressivite', period)
        default_deg = datetime64(date(2099, 12, 31))
        degressivite = date_deg != default_deg

        return max_(
            round_(alloc_tx_plein * taux_deg, 0),
            montant_min) * degressivite
    

class are_allocation_journaliere_brute_tx_deg(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière brute de l'ARE à taux dégressif, après éventuelle déduction de PRC"
    unit = 'currency'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Articles 14 à 16']

    def formula(individu, period, parameters):
        super_brute = individu('are_allocation_journaliere_super_brute_tx_deg', period)
        prc = individu('are_retraires_complementaires_tx_plein', period)

        return individu('are_eligible', period) * (super_brute + prc)

class are_csg_deductible_tx_deg(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG déductible sur les allocations chômage (taux dégressif)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        brute = individu('are_allocation_journaliere_brute_tx_deg', period)

        montant_csg_ded_th = -round(montant_csg_crds(
            base_avec_abattement = brute,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.deductible,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ), 2)

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute - smic_j, montant_csg_ded_th), 0)


class are_csg_non_deductible_tx_deg(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG non déductible sur les allocations chômage (taux dégressif)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        csg_ded = individu('are_csg_deductible_tx_deg', period)

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        brute = individu('are_allocation_journaliere_brute_tx_deg', period)

        montant_csg_non_ded_th = -round(montant_csg_crds(
            base_avec_abattement = brute,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.imposable,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ), 2)

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute + csg_ded - smic_j, montant_csg_non_ded_th), 0)


class are_crds_tx_deg(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CRDS sur les allocations chômage (taux dégressif)'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula(individu, period, parameters):
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        csg_ded = individu('are_csg_deductible_tx_deg', period)
        csg_non_ded = individu('are_csg_non_deductible_tx_deg', period)

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        eligible = (
            (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit)
            + (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein)
            )

        brute = individu('are_allocation_journaliere_brute_tx_deg', period)

        montant_crds_th = -round(montant_csg_crds(
                base_avec_abattement = brute,
                abattement_parameter = parameters.prelevements_sociaux.contributions_sociales.csg.activite.abattement,
                law_node = parameters.prelevements_sociaux.contributions_sociales.crds,
                plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
                ), 2) * eligible

        smic_j = individu('are_smic_journalier', period)

        return - max_(min_(brute + csg_ded + csg_non_ded - smic_j, montant_crds_th), 0)


class are_allocation_nette_journaliere_tx_deg(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière nette de l'ARE (taux dégressif), après déduction des prélèvements"
    unit = 'currency'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period):
        brut = individu('are_allocation_journaliere_brute_tx_deg', period)
        csg_deductible = individu('are_csg_deductible_tx_deg', period)
        csg_non_deductible = individu('are_csg_non_deductible_tx_deg', period)
        crds = individu('are_crds_tx_deg', period)

        return individu('are_eligible', period) * (brut + csg_deductible + csg_non_deductible + crds)


## Pas sûr de la façon dont on doit intégrer les jours non indemnisés
## La formule actuelle ne traite pas le cas où la date de fin est 28 février... on compte 30 jours
class are_jours_indemnises_mensuels(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours indemnisés sur le mois courant"
    unit = 'day'
    definition_period = MONTH
    reference = ['https://www.unedic.org/ged/documents/regulatory_texts/pdf/TXT-RG-Reglement_general_annexe_a_la_convention.pdf',
                 'Article 24']

    def formula(individu, period, parameters):
        debut = individu('are_debut_indemnisation', period)
        fin = individu('are_fin_indemnisation', period)

        duree_nette = individu('are_duree_nette_gelee', period)

        debut_courant = datetime64(period.start)
        reliquat_j = max_(
            duree_nette - ((debut_courant.astype('datetime64[M]') - debut.astype('datetime64[M]')).astype(int) * 30),
            0)

        last_month = reliquat_j <= 30

        default = datetime64(date(1870, 1, 1))

        return where(
            (debut != default) & (debut_courant <= fin),
                     where(last_month,
                        reliquat_j,
                        30),
                    0)


class are_jours_indemnises_mensuels_tx_plein(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours indemnisés à taux plein sur le mois courant"
    unit = 'day'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period, parameters):
        debut = individu('are_debut_indemnisation', period)
        default = datetime64(date(1870, 1, 1))

        fin = individu('are_fin_indemnisation', period)

        debut_deg = individu('are_date_debut_degressivite', period)
        default_deg = datetime64(date(2099, 12, 31))
        
        jours_mois = individu('are_jours_indemnises_mensuels', period)
        
        jours_deg = parameters(period).chomage.allocations_assurance_chomage.are.degressivite.jours_application

        debut_courant = datetime64(period.start)

        j_plein = where(debut_courant.astype('datetime64[M]') <= debut_deg.astype('datetime64[M]'),
            max_(
                min_(
                    jours_deg - ((debut_courant.astype('datetime64[M]') - debut.astype('datetime64[M]')).astype(int) * 30),
                    30),
            0),
           0)        

        return where(
            (debut != default) & (debut_courant <= fin),
                     where(debut_deg != default_deg,
                        j_plein,
                        jours_mois),
                    0)


class are_jours_indemnises_mensuels_tx_deg(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de jours indemnisés à taux dégressif sur le mois courant"
    unit = 'day'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period, parameters):
        jours_total = individu('are_jours_indemnises_mensuels', period)
        jours_plein = individu('are_jours_indemnises_mensuels_tx_plein', period)

        return jours_total - jours_plein


class are_allocation_super_brute_mensuelle(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle super brute de l'ARE, avant déduction des prélèvements"
    unit = 'currency'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period, parameters):
        jours_plein = individu('are_jours_indemnises_mensuels_tx_plein', period)
        jours_deg = individu('are_jours_indemnises_mensuels_tx_deg', period)        

        tx_plein = individu('are_allocation_journaliere_super_brute_tx_plein', period)
        tx_deg = individu('are_allocation_journaliere_super_brute_tx_deg', period)

        return jours_plein * tx_plein + jours_deg * tx_deg


class are_allocation_nette_mensuelle(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle nette de l'ARE, après déduction des prélèvements"
    unit = 'currency'
    definition_period = MONTH
    reference = ['']

    def formula(individu, period, parameters):
        jours_plein = individu('are_jours_indemnises_mensuels_tx_plein', period)
        jours_deg = individu('are_jours_indemnises_mensuels_tx_deg', period)        

        tx_plein = individu('are_allocation_nette_journaliere_tx_plein', period)
        tx_deg = individu('are_allocation_nette_journaliere_tx_deg', period)

        return jours_plein * tx_plein + jours_deg * tx_deg