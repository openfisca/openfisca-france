from numpy import datetime64, logical_or as or_

from openfisca_core.periods import Period

from openfisca_france.model.base import *


class autonomie_financiere(Variable):
    value_type = bool
    entity = Individu
    label = "Indicatrice d'autonomie financière vis-à-vis des prestations familiales"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000006750602&cidTexte=LEGITEXT000006073189',
        'https://www.service-public.fr/particuliers/vosdroits/F16947'
        ]

    def formula(individu, period, parameters):
        # D'après service-public.fr, la condition de dépassement du salaire plafonds n'est pas évalué de la même manière suivant si l'enfant est étudiant ou salarié/apprenti/stagiaire.
        salaire_net_mensualise = individu('salaire_net', Period(('month', period.start, 6)).offset(-6), options = [ADD]) / 6

        _P = parameters(period)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.marche_travail.salaire_minimum.smic.smic_b_horaire * nbh_travaillees

        return salaire_net_mensualise >= (_P.prestations_sociales.prestations_familiales.def_pac.revenu_plafond_pac_non_scolaire * smic_mensuel_brut)


class prestations_familiales_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = 'Enfant considéré à charge au sens des prestations familiales'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        est_enfant_dans_famille = individu('est_enfant_dans_famille', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age = individu('age', period)
        rempli_obligation_scolaire = individu('rempli_obligation_scolaire', period)

        pfam = parameters(period).prestations_sociales.prestations_familiales

        condition_enfant = (
            (age >= pfam.def_pac.enfants.age_minimal)
            * (age < pfam.def_pac.enfants.age_intermediaire)
            * rempli_obligation_scolaire
            )

        condition_jeune = (
            (age >= pfam.def_pac.enfants.age_intermediaire)
            * (age < pfam.def_pac.enfants.age_limite)
            * not_(autonomie_financiere)
            )

        return or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


class prestations_familiales_base_ressources_individu(Variable):
    value_type = float
    is_period_size_independent = True
    entity = Individu
    label = 'Base ressource individuelle des prestations familiales'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        annee_fiscale_n_2 = period.n_2

        traitements_salaires_pensions_rentes = individu('traitements_salaires_pensions_rentes', annee_fiscale_n_2)
        hsup = individu('hsup', annee_fiscale_n_2, options = [ADD])
        rpns = individu('rpns_imposables', annee_fiscale_n_2)
        rpns_pvce = individu('rpns_pvce', annee_fiscale_n_2)
        rpns_exon = individu('rpns_exon', annee_fiscale_n_2)

        return traitements_salaires_pensions_rentes + hsup + rpns + rpns_pvce + rpns_exon


class biactivite(Variable):
    value_type = bool
    entity = Famille
    label = 'Indicatrice de biactivité'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

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

        bmaf = parameters(annee_fiscale_n_2).prestations_sociales.prestations_familiales.bmaf.bmaf
        seuil_rev = 12 * bmaf

        condition_ressource = (
            famille.members('rpns_imposables', annee_fiscale_n_2)
            + famille.members('revenu_assimile_salaire_apres_abattements', annee_fiscale_n_2)
            >= seuil_rev
            )
        deux_parents = famille.nb_persons(role = Famille.PARENT) == 2

        return deux_parents * famille.all(condition_ressource, role = Famille.PARENT)


class rev_coll(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus perçus par le foyer fiscal à prendre en compte dans la base ressource des prestations familiales'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        # Quand rev_coll est calculé sur une année glissante, rente_viagere_titre_onereux_net et pensions_alimentaires_versees sont calculés sur l'année légale correspondante.
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        rev_cat_rvcm = foyer_fiscal('revenu_categoriel_capital', period)
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        abat_spe = foyer_fiscal('abattements_speciaux_prestations_familiales', period)
        revenu_categoriel_foncier = foyer_fiscal('revenu_categoriel_foncier', period)
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        plus_values = foyer_fiscal('assiette_csg_plus_values', period)  # Cette variable ne correspond probablement pas exactement à la législation exacte (revenus nets catégoriels retenus pour l'IR, à taux propostionnel ou libératoire : cf. art. R532-3 du CSS), que ce soit en termes de champ des plus-values (PV) et de leur mesure (abattements ou pas, etc.). Néanmoins, cette variable constitue une bonne approximation. Les autres contiennent d'autres limites (les PV au barème, via revenu_categoriel_plus_values ou au PFU, via plus_values_prelevement_forfaitaire_unique_ir, ne regroupent pas toutes les plus-values ; les variables rfr_plus_values_hors_rni et revenu_categoriel_plus_values non-plus (ex : gains de levée d'option assimilés salaires).

        # TODO: ajouter les revenus de l'étranger etr*0.9
        return (
            revenu_categoriel_foncier
            + pensions_alimentaires_versees  # négatif
            + rente_viagere_titre_onereux_net
            + rev_cat_rvcm
            + revenus_capitaux_prelevement_liberatoire
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + plus_values
            - abat_spe
            - f7ga
            - f7gb
            - f7gc
            )


class prestations_familiales_base_ressources_communes(Variable):
    value_type = float
    entity = Famille
    label = 'Ressources non individualisables prises en compte pour les prestations familiales'
    reference = [
        'Article D521-4 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000030678081&cidTexte=LEGITEXT000006073189&categorieLien=id'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

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
    label = 'Base ressource des prestations familiales'
    reference = [
        'Article D521-4 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000030678081&cidTexte=LEGITEXT000006073189&categorieLien=id'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

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
    '''
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    '''

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


class abattements_speciaux_prestations_familiales(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Abattements spéciaux concernant les personnes agées ou invalides et les enfants à charge'
    reference = [
        'http://bofip.impots.gouv.fr/bofip/2036-PGP',
        'https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000002185185'
        ]
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        dateLimite = datetime64('1931-01-01')

        age_declarant = foyer_fiscal.declarant_principal('age', period.first_month)
        date_naissance_declarant = foyer_fiscal.declarant_principal('date_naissance', period.first_month)

        # Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte
        # d'invalidité d'au moins 80%
        declarant_invalide = foyer_fiscal('caseP', period.this_year)

        age_conjoint = foyer_fiscal.declarant_principal('age', period.first_month)
        date_naissance_conjoint = foyer_fiscal.conjoint('date_naissance', period.first_month)

        # Conjoint·e titulaire d'une pension ou d'une carte d'invalidité (vivant ou
        # décédé l'année de perception des revenus)
        conjoint_invalide = foyer_fiscal('caseF', period.this_year)

        # Revenu net global
        revenu_net_global = foyer_fiscal('rng', period)

        # Nombre d'enfants marié·e·s/pacse·é·s et d'enfants non mari·é·s charg·é·s de
        # famille
        nombre_enfants = foyer_fiscal('nbN', period)

        # Abattements pour revenu net imposable
        abattements = parameters(period).impot_revenu.calcul_revenus_imposables.abat_rni

        # Abattement pour personnes agées de + de 65 ans ou invalide
        abattement_age_ou_invalidite = abattements.contribuable_age_invalide

        # Abattement pour rattachement d'enfants mari·é·s
        abattement_enfant_marie = abattements.enfant_marie

        # Vecteur de foyers eligibles aux abattements spéciaux
        foyers_eligibles = (
            (((date_naissance_declarant < dateLimite) | declarant_invalide) & (age_declarant > 0))
            + (((date_naissance_conjoint < dateLimite) | conjoint_invalide) & (age_conjoint > 0))
            )

        # Vecteur de montants d'abattement pour personnes âges ou invalides
        abattement_special_personne_agee_invalide = (
            foyers_eligibles
            * abattement_age_ou_invalidite.calc(revenu_net_global)
            )

        # Vecteur de montants d'abattement pour enfants à charge
        abattement_special_enfants_a_charge = (
            nombre_enfants
            * abattement_enfant_marie
            )

        # Le montant total d'abattement ne peut pas être supérieur au revenu net global
        return min_(revenu_net_global, abattement_special_personne_agee_invalide + abattement_special_enfants_a_charge)
