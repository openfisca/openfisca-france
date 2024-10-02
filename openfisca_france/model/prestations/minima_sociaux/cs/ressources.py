from numpy import absolute as abs_, logical_and as and_, logical_or as or_, logical_not as not_, maximum as max_, select, where, sum as sum_

from openfisca_core.periods import Period

from openfisca_france.model.base import (
    Variable,
    Individu,
    Famille,
    FoyerFiscal,
    MONTH,
    ADD,
    TypesStatutOccupationLogement,
    TypesActivite,
    set_input_divide_by_period,
    )


class css_cmu_base_ressources_individu(Variable):
    value_type = float
    label = "Base de ressources de l'individu prise en compte pour l'éligibilité à la ACS / CMU-C / CSS"
    reference = [
        'Article R861-8 du code de la Sécurité Sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000034424885&cidTexte=LEGITEXT000006073189&dateTexte=20180829',
        'Article R861-10 du code de la Sécurité Sociale pour les ressources exclues',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000030055485&cidTexte=LEGITEXT000006073189&dateTexte=20180829',
        "Circulaire N°DSS/2A/2002/110 du 22 février 2002 relative à la notion de ressources à prendre en compte pour l'appréciation du droit à la protection complémentaire en matière de santé",
        'http://circulaire.legifrance.gouv.fr/pdf/2009/04/cir_6430.pdf'
        ]
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        # Rolling year
        previous_year = compute_previous_year(period)
        # N-1
        last_year = period.last_year
        last_month = period.last_month

        parametres_cmu = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.cmu

        ressources_a_inclure = [
            'css_base_ressources_aah_individu',
            'allocation_securisation_professionnelle',
            'ass',
            'bourse_recherche',
            'caah',
            'chomage_net',
            'dedommagement_victime_amiante',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_stage',
            'indemnites_compensatrices_conges_payes',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_combattant',
            'retraite_nette',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu',
            'salaire_net',
            'rente_accident_travail',
            ]

        boursier = individu('boursier', period)
        bourse = not_(boursier) * individu('bourse_enseignement_sup', period)

        ressources = sum([
            individu(ressource, previous_year, options = [ADD])
            for ressource in ressources_a_inclure
            ])

        pensions_alim_versees = abs_(individu(
            'pensions_alimentaires_versees_individu',
            previous_year, options = [ADD])
            )

        return (
            ressources
            + bourse
            + revenus_tns(individu, previous_year, last_year)
            - pensions_alim_versees
            - abattement_chomage(individu, period, previous_year, parametres_cmu)
            - neutralisation_stage_formation_pro(individu, previous_year, last_month)
            )

class css_base_ressources_aah_individu(Variable):
    value_type = float
    label = "Base de ressources AAH de l'individu prise en compte pour l'éligibilité à la CSS après application de l'abattement"
    reference = [
        'Bulletin officiel Santé - Protection sociale - Solidarité n° 2021/6 du 16 avril 2021 - Instruction interministérielle N° DSS/SD2A/2021/71 du 30 mars 2021',
        'https://sante.gouv.fr/fichiers/bo/2021/2021.6.sante.pdf#page=75',
        'Bulletin officiel Santé - Protection sociale - Solidarité n° 2023/24 du 29 décembre 2023 - Instruction interministérielle N° DSS/SD2A/2023/98 du 22 décembre 2023',
        'https://sante.gouv.fr/fichiers/bo/2023/2023.24.sante.pdf#page=82',
    ]
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        return individu('aah', period)

    def formula_2021_04_01(individu, period, parameters):
        return max_(individu('aah', period) - parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.abattements.aah, 0)

class css_abattement_asi_individu(Variable):
    value_type = float
    label = "Base de ressources ASI de l'individu prise en compte pour l'éligibilité à la CSS après application de l'abattement"
    reference = [
        'Bulletin officiel Santé - Protection sociale - Solidarité n° 2021/6 du 16 avril 2021 - Instruction interministérielle N° DSS/SD2A/2021/71 du 30 mars 2021',
        'https://sante.gouv.fr/fichiers/bo/2021/2021.6.sante.pdf#page=75'
    ]
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        return 0

    def formula_2021_04_01(individu, period, parameters):

        abattement_asi_personne_seule = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.abattements.asi.personne_seule
        abattement_asi_couple = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.abattements.asi.couple/2
        adulte_ayant_asi = where(and_(
            individu.has_role(FoyerFiscal.DECLARANT),
            individu('asi', period)),
            True, False)
        appliquer_abattement_couple = sum_(adulte_ayant_asi) > 1
        aah = individu('aah', period)
        return select(
            [aah > 0, appliquer_abattement_couple and adulte_ayant_asi, adulte_ayant_asi],
            [0, abattement_asi_couple, abattement_asi_personne_seule],
            0)

class css_base_ressources_aspa_asv(Variable):
    value_type = float
    label = "Base de ressources ASPA/ASV de pour une famille prise en compte pour l'éligibilité à la CSS après application de l'abattement"
    reference = [
        'Bulletin officiel Santé - Protection sociale - Solidarité n° 2021/6 du 16 avril 2021 - Instruction interministérielle N° DSS/SD2A/2021/71 du 30 mars 2021',
        'https://sante.gouv.fr/fichiers/bo/2021/2021.6.sante.pdf#page=75'
    ]
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        return famille('aspa', period)
    def formula_2021_04_01(famille, period, parameters):
        aspa = famille('aspa', period)
        aspa_couple = famille('aspa_couple', period)
        abattement_aspa_personne_seule = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.abattements.aspa_asv.personne_seule
        abattement_aspa_couple = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.abattements.aspa_asv.couple
        return select(
            [aspa > 0 and aspa_couple, aspa > 0],
            [max_(aspa - abattement_aspa_couple, 0), max_(aspa - abattement_aspa_personne_seule, 0)],
            aspa)

class css_cmu_base_ressources(Variable):
    value_type = float
    label = "Base de ressources prise en compte pour l'éligibilité à la ACS / CMU-C / CSS"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        previous_year = compute_previous_year(period)

        ressources_famille_a_inclure = [
            'af',
            'asf',
            'css_base_ressources_aspa_asv',
            'cf',
            'paje_clca',
            'paje_prepare',
            ]

        ressources_famille = sum([
            famille(ressource, previous_year, options = [ADD])
            for ressource in ressources_famille_a_inclure
            ])

        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        css_cmu_forfait_logement_base = famille('css_cmu_forfait_logement_base', period)
        css_cmu_forfait_logement_al = famille('css_cmu_forfait_logement_al', period)

        parametres_cmu = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.cmu

        proprietaire = (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire)
        heberge_titre_gratuit = (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement)

        forfait_logement = (
            (proprietaire + heberge_titre_gratuit)
            * css_cmu_forfait_logement_base
            + css_cmu_forfait_logement_al
            )

        ressources_individuelles = famille.members('css_cmu_base_ressources_individu', period)
        ressources_individuelles_asi = famille.members('asi', previous_year, options = [ADD])
        abattements_asi_individuelles = famille.members('css_abattement_asi_individu', previous_year, options = [ADD])

        ressources_asi_parents = max_(famille.sum(ressources_individuelles_asi, role = Famille.PARENT) - famille.sum(abattements_asi_individuelles), 0)
        ressources_parents = famille.sum(ressources_individuelles, role = Famille.PARENT) + ressources_asi_parents

        age = famille.members('age', period)
        condition_enfant_a_charge = (age >= 0) * (age <= parametres_cmu.age_limite_pac)
        ressources_asi_enfants = famille.sum(ressources_individuelles_asi * condition_enfant_a_charge, role = Famille.ENFANT)
        ressources_enfants = famille.sum(ressources_individuelles * condition_enfant_a_charge, role = Famille.ENFANT) + ressources_asi_enfants

        return forfait_logement + ressources_famille + ressources_parents + ressources_enfants

# Helper functions

def compute_previous_year(period):
    return Period(('year', period.start, 1)).offset(-1).offset(-1, 'month')

# Abattement sur revenus d'activité si :
# - IJ maladie
# - chômage
# - ass
# - formation professionnelle
def abattement_chomage(individu, period, previous_year, parametres_cmu):
    indemnites_journalieres_maladie = individu('indemnites_journalieres_maladie', period)

    chomage = individu('activite', period) == TypesActivite.chomeur
    indemnites_chomage_partiel = individu('indemnites_chomage_partiel', period)
    chomage_net = individu('chomage_net', period)

    ass = individu('ass', period)

    revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period)

    condition_ij_maladie = indemnites_journalieres_maladie > 0
    condition_chomage = chomage * ((indemnites_chomage_partiel + chomage_net) > 0)
    condition_ass = ass > 0
    condition_revenus_formation_pro = revenus_stage_formation_pro > 0

    eligibilite_abattement_chomage = or_(condition_ij_maladie, or_(condition_chomage, or_(condition_ass, condition_revenus_formation_pro)))

    salaire_net = individu('salaire_net', previous_year, options = [ADD])

    return eligibilite_abattement_chomage * salaire_net * parametres_cmu.abattement_chomage


# Revenus de stage de formation professionnelle exclus si plus perçus depuis 1 mois
def neutralisation_stage_formation_pro(individu, previous_year, last_month):
    revenus_stage_formation_pro_last_month = individu('revenus_stage_formation_pro', last_month)
    revenus_stage_formation_pro_annee = individu('revenus_stage_formation_pro', previous_year, options = [ADD])
    return (revenus_stage_formation_pro_last_month == 0) * revenus_stage_formation_pro_annee


def revenus_tns(individu, previous_year, last_year):
    revenus_auto_entrepreneur = individu('rpns_auto_entrepreneur_benefice', previous_year, options = [ADD])

    # Les revenus TNS hors AE sont estimés en se basant sur N-1
    rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', last_year)
    rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', last_year)
    rpns_autres_revenus = individu('rpns_autres_revenus', last_year)

    return revenus_auto_entrepreneur + rpns_micro_entreprise_benefice + rpns_benefice_exploitant_agricole + rpns_autres_revenus
