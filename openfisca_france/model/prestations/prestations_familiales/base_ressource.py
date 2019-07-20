# -*- coding: utf-8 -*-

from numpy import logical_or as or_

from openfisca_france.model.base import *


class autonomie_financiere(Variable):
    value_type = bool
    entity = Individu
    label = "Indicatrice d'autonomie financière vis-à-vis des prestations familiales"
    definition_period = MONTH
    reference = [
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006750602&cidTexte=LEGITEXT000006073189',
        'https://www.service-public.fr/particuliers/vosdroits/F16947'
        ]

    def formula(individu, period, parameters):
        # D'après service-public.fr, la condition de dépassement du salaire plafonds n'est pas évalué de la même manière suivant si l'enfant est étudiant ou salarié/apprenti/stagiaire.
        salaire_net_mensualise = individu('salaire_net', period.start.period('month', 6).offset(-6), options = [ADD]) / 6

        _P = parameters(period)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees

        return salaire_net_mensualise >= (_P.prestations.prestations_familiales.af.seuil_rev_taux * smic_mensuel_brut)


class prestations_familiales_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant considéré à charge au sens des prestations familiales"
    definition_period = MONTH

    def formula(individu, period, parameters):
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = parameters(period).prestations.prestations_familiales

        condition_enfant = (
            (age >= pfam.enfants.age_minimal)
            * (age < pfam.enfants.age_intermediaire)
            * rempli_obligation_scolaire
            )

        condition_jeune = (
            (age >= pfam.enfants.age_intermediaire)
            * (age < pfam.enfants.age_limite)
            * not_(autonomie_financiere)
            )

        return or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


class prestations_familiales_base_ressources_individu(Variable):
    value_type = float
    is_period_size_independent = True
    entity = Individu
    label = "Base ressource individuelle des prestations familiales"
    definition_period = MONTH

    def formula(individu, period):
        annee_fiscale_n_2 = period.n_2

        traitements_salaires_pensions_rentes = individu('traitements_salaires_pensions_rentes', annee_fiscale_n_2)
        hsup = individu('hsup', annee_fiscale_n_2, options = [ADD])
        glo = individu('glo', annee_fiscale_n_2)
        plus_values = individu.foyer_fiscal('assiette_csg_plus_values', annee_fiscale_n_2) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        rpns = individu('rpns', annee_fiscale_n_2)
        rpns_pvce = individu('rpns_pvce', annee_fiscale_n_2)
        rpns_pvct = individu('rpns_pvct', annee_fiscale_n_2)
        rpns_mvct = individu('moins_values_court_terme_non_salaries', annee_fiscale_n_2)
        rpns_mvlt = individu('moins_values_long_terme_non_salaries', annee_fiscale_n_2)

        return traitements_salaires_pensions_rentes + hsup + glo + plus_values + rpns + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt


class biactivite(Variable):
    value_type = bool
    entity = Famille
    label = "Indicatrice de biactivité"
    definition_period = MONTH

    def formula(famille, period, parameters):
        '''
        Hypothèses/points à éclaircir :
           (1) A partir d'une certaine date sont apparemment pris en compte
               dans les "revenus professinnels" les indemnités journalières.
               Cf. circulaire interministérielle DSS/2B n°2011-447 du 01/12/2011
               Regarder davantage ce point
           (2) On n'a pas pris en compte les abbattements présents dans la
               variable abattement_salaires_pensions, car il s'agit d'une
               variable dépendant conjointement des salaires et des pensions
               (or, les pensions ne doivent pas être pris en compte ici, et
               cette variable ne peut pas être décomposée entre une part salaire et
               une part pensions). Mais cette variable n'existe que jusqu'à 2005
               inclus.
        '''
        annee_fiscale_n_2 = period.n_2

        pfam = parameters(annee_fiscale_n_2).prestations.prestations_familiales
        seuil_rev = 12 * pfam.af.bmaf

        condition_ressource = (
            famille.members('rpns_individu', annee_fiscale_n_2)
            + famille.members('revenu_assimile_salaire_apres_abattements', annee_fiscale_n_2)
            >= seuil_rev
            )
        deux_parents = famille.nb_persons(role = Famille.PARENT) == 2

        return deux_parents * famille.all(condition_ressource, role = Famille.PARENT)


class rev_coll(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenus perçus par le foyer fiscal à prendre en compte dans la base ressource des prestations familiales"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        # Quand rev_coll est calculé sur une année glissante, rente_viagere_titre_onereux_net et pensions_alimentaires_versees sont calculés sur l'année légale correspondante.
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        rev_cat_rvcm = foyer_fiscal('revenu_categoriel_capital', period)  # Supprimée en 2018
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])  # Supprimée en 2018
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])  # Existe à partir de 2018
        abat_spe = foyer_fiscal('abat_spe', period)
        revenu_categoriel_foncier = foyer_fiscal('revenu_categoriel_foncier', period)
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        # est supprimée à partir de 2018
        rev_cat_pv = foyer_fiscal('revenu_categoriel_plus_values', period)
        plus_values_prelevement_forfaitaire_unique_ir = foyer_fiscal('plus_values_prelevement_forfaitaire_unique_ir', period)  # Apparait à partir de 2018

        # TODO: ajouter les revenus de l'étranger etr*0.9
        return (
            + revenu_categoriel_foncier
            + pensions_alimentaires_versees  # négatif
            + rente_viagere_titre_onereux_net
            + rev_cat_rvcm
            + revenus_capitaux_prelevement_liberatoire
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + rev_cat_pv
            + plus_values_prelevement_forfaitaire_unique_ir
            - abat_spe
            - f7ga
            - f7gb
            - f7gc
            )


class prestations_familiales_base_ressources_communes(Variable):
    value_type = float
    entity = Famille
    label = "Ressources non individualisables prises en compte pour les prestations familiales"
    reference = [
        "Article D521-4 du Code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000030678081&cidTexte=LEGITEXT000006073189&categorieLien=id"
        ]
    definition_period = MONTH

    def formula(famille, period):
        annee_fiscale_n_2 = period.n_2

        demandeur_declarant_principal = famille.demandeur.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        conjoint_declarant_principal = famille.conjoint.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        rev_coll = (
            famille.demandeur.foyer_fiscal('rev_coll', annee_fiscale_n_2)
            * demandeur_declarant_principal
            + famille.conjoint.foyer_fiscal('rev_coll', annee_fiscale_n_2)
            * conjoint_declarant_principal
            )

        return rev_coll


class prestations_familiales_base_ressources(Variable):
    value_type = float
    entity = Famille
    label = "Base ressource des prestations familiales"
    reference = [
        "Article D521-4 du Code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000030678081&cidTexte=LEGITEXT000006073189&categorieLien=id"
        ]
    definition_period = MONTH

    def formula(famille, period):
        base_ressources_i = famille.members('prestations_familiales_base_ressources_individu', period)
        enfant_i = famille.members('est_enfant_dans_famille', period)
        enfant_a_charge_i = famille.members('prestations_familiales_enfant_a_charge', period)
        ressources_i = (not_(enfant_i) + enfant_a_charge_i) * base_ressources_i
        base_ressources_i_total = famille.sum(ressources_i)

        ressources_communes = famille('prestations_familiales_base_ressources_communes', period)

        return base_ressources_i_total + ressources_communes


############################################################################
# Helper functions
############################################################################


def nb_enf(famille, period, age_min, age_max):
    """
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    """

    assert period.unit == 'month'
    assert period.size == 1

    age = famille.members('age', period)
    autonomie_financiere = famille.members('autonomie_financiere', period)

#        Les allocations sont dues à compter du mois civil qui suit la naissance
#        ag1==0 ou suivant les anniversaires ag1>0.
#        Un enfant est reconnu à charge pour le versement des prestations
#        jusqu'au mois précédant son age limite supérieur (ag2 + 1) mais
#        le versement à lieu en début de mois suivant
    condition = (
        (age >= age_min)
        * (age <= age_max)
        * not_(autonomie_financiere)
        )

    return famille.sum(condition, role = Famille.ENFANT)
