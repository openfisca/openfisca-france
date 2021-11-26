from openfisca_france.model.base import *

from numpy import datetime64

# Références juridiques - Code de la sécurité sociale
#
# Article L821-1 / 821-8
# https://www.legifrance.gouv.fr/affichCode.do;jsessionid=0E604431776A4B1ED8D2F8EB55A1A99C.tplgfr35s_1?idSectionTA=LEGISCTA000006141693&cidTexte=LEGITEXT000006073189&dateTexte=20180412
#
# Article R821-1 / 821-9
# https://www.legifrance.gouv.fr/affichCode.do;jsessionid=0E604431776A4B1ED8D2F8EB55A1A99C.tplgfr35s_1?idSectionTA=LEGISCTA000006142017&cidTexte=LEGITEXT000006073189&dateTexte=20181010
#
# Article D821-1 / 821-11
# https://www.legifrance.gouv.fr/affichCode.do;jsessionid=157287C570B3AE9450A0BD88AA902970.tplgfr38s_1?idSectionTA=LEGISCTA000006141593&cidTexte=LEGITEXT000006073189&dateTexte=20180731


class aah_date_debut_incarceration(Variable):
    value_type = date
    default_value = date.max
    label = "La date de début d'incarcération"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aah_date_debut_hospitalisation(Variable):
    value_type = date
    default_value = date.max
    label = "La date de début d'hospitalisation"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aah_base_ressources(Variable):
    value_type = float
    label = "Base ressources de l'allocation adulte handicapé"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        law = parameters(period)
        aah = law.prestations.minima_sociaux.aah.abattements

        en_activite = individu('salaire_imposable', period) > 0

        def assiette_conjoint(revenus_conjoint):
            return (1 - law.impot_revenu.tspr.abatpro.taux) * (1 - aah.abattement_conjoint) * revenus_conjoint

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = 12 * law.marche_travail.salaire_minimum.smic_h_b * law.marche_travail.salaire_minimum.nb_heure_travail_mensuel
            tranche1 = min_(aah.tranche_smic * smic_brut_annuel, revenus_demandeur)
            tranche2 = revenus_demandeur - tranche1
            return (1 - aah.abattement_activite_tranche_inf) * tranche1 + (1 - aah.abattement_activite_tranche_sup) * tranche2

        def base_ressource_eval_trim():
            three_previous_months = period.first_month.start.period('month', 3).offset(-3)
            base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
            base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])

            base_ressource_demandeur = assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_trimestrielle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_trimestrielle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource_demandeur + assiette_conjoint(base_ressource_conjoint)

        def base_ressource_eval_annuelle():
            base_ressource = individu('aah_base_ressources_eval_annuelle', period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_eval_annuelle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_eval_annuelle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return assiette_revenu_activite_demandeur(base_ressource) + assiette_conjoint(base_ressource_conjoint)

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12
            )

        # TODO: - Prendre en compte les abattements temporaires sur les ressources en cas de changement de situation
        #       - La formule du calcul de la base de ressource est celle en vigueur à partir de 2011, avant 2011:
        #           - les abattements sur les revenus d'activité de l'allocataire diffèrent (art. D821-9 du CSS)
        #           - l'abattement pour les personnes invalides (défini dans l'art. 157 du CGI) sur le revenu net global est pris en compte (art. R821-4 du CSS)
        #           - l'évaluation de tous les revenus est annuelle (pas d'évaluation trimestrielle avant 2011)


class aah_base_ressources_activite_eval_trimestrielle(Variable):
    value_type = float
    label = "Base de ressources des revenus d'activité de l'AAH pour un individu, évaluation trimestrielle"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    '''
        N'entrent pas en compte dans les ressources :
        L'allocation compensatrice tierce personne, les allocations familiales,
        l'allocation de logement, la retraite du combattant, les rentes viagères
        constituées en faveur d'une personne handicapée ou dans la limite d'un
        montant fixé à l'article D.821-6 du code de la sécurité sociale (1 830 €/an),
        lorsqu'elles ont été constituées par une personne handicapée pour elle-même.
        Le RMI (article R 531-10 du code de la sécurité sociale).
        A partir du 1er juillet 2007, votre Caf, pour le calcul de votre Aah,
        continue à prendre en compte les ressources de votre foyer diminuées de 20%.
        Notez, dans certaines situations, la Caf évalue forfaitairement vos
        ressources à partir de votre revenu mensuel.
    '''

    def formula(individu, period):
        period = period.first_month
        three_previous_months = period.start.period('month', 3).offset(-3)
        last_year = period.last_year

        ressources_a_inclure = [
            'chomage_net',
            'indemnites_chomage_partiel',
            'indemnites_journalieres_imposables',
            'indemnites_stage',
            'revenus_stage_formation_pro',
            'salaire_net',
            ]

        ressources = sum(
            [individu(ressource, three_previous_months, options = [ADD]) for ressource in ressources_a_inclure]
            )

        def revenus_tns():
            revenus_auto_entrepreneur = individu('rpns_auto_entrepreneur_benefice', three_previous_months, options = [ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', last_year) * 3 / 12
            rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', last_year) * 3 / 12
            rpns_autres_revenus = individu('rpns_autres_revenus', last_year) * 3 / 12

            return revenus_auto_entrepreneur + rpns_micro_entreprise_benefice + rpns_benefice_exploitant_agricole + rpns_autres_revenus

        return (ressources + revenus_tns()) * 4


class aah_base_ressources_activite_milieu_protege(Variable):
    value_type = float
    label = "Base de ressources de l'AAH des revenus d'activité en milieu protégé pour un individu"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


class aah_base_ressources_hors_activite_eval_trimestrielle(Variable):
    value_type = float
    label = "Base de ressources hors revenus d'activité de l'AAH pour un individu, évaluation trimestrielle"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    '''
        N'entrent pas en compte dans les ressources :
        L'allocation compensatrice tierce personne, les allocations familiales,
        l'allocation de logement, la retraite du combattant, les rentes viagères
        constituées en faveur d'une personne handicapée ou dans la limite d'un
        montant fixé à l'article D.821-6 du code de la sécurité sociale (1 830 €/an),
        lorsqu'elles ont été constituées par une personne handicapée pour elle-même.
        Le RMI (article R 531-10 du code de la sécurité sociale).
        A partir du 1er juillet 2007, votre Caf, pour le calcul de votre Aah,
        continue à prendre en compte les ressources de votre foyer diminuées de 20%.
        Notez, dans certaines situations, la Caf évalue forfaitairement vos
        ressources à partir de votre revenu mensuel.
    '''

    def formula(individu, period):
        period = period.first_month
        three_previous_months = period.start.period('month', 3).offset(-3)

        ressources_a_inclure = [
            'asi',
            'allocation_securisation_professionnelle',
            'bourse_recherche',
            'gains_exceptionnels',
            'pensions_alimentaires_percues',
            'pensions_alimentaires_versees_individu',
            'pensions_invalidite',
            'prestation_compensatoire',
            'retraite_nette',
            'rsa_base_ressources_patrimoine_individu',
            ]

        ressources = sum(
            [individu(ressource, three_previous_months, options = [ADD]) for ressource in ressources_a_inclure]
            )

        return ressources * 4


class aah_base_ressources_eval_annuelle(Variable):
    value_type = float
    label = "Base de ressources de l'AAH pour un individu, évaluation annuelle"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        return (
            individu('salaire_imposable', period.n_2, options = [ADD])
            + individu('rpns_imposables', period.n_2)
            + individu('revenu_assimile_pension', period.n_2)
            )


class aah_restriction_substantielle_durable_acces_emploi(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = "Restriction substantielle et durable pour l'accès à l'emploi reconnue par la commission des droits et de l'autonomie des personnes handicapées"
    reference = [
        "Article L821-2 du Code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=17BE3036A19374AA1C8C7A4169702CD7.tplgfr24s_2?idArticle=LEGIARTI000020039305&cidTexte=LEGITEXT000006073189&dateTexte=20180731"
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aah_eligible(Variable):
    value_type = bool
    label = "Eligibilité à l'Allocation adulte handicapé"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    '''
        Allocation adulte handicapé

        Conditions liées au handicap
        La personne doit être atteinte d’un taux d’incapacité permanente :
        - d’au moins 80 %,
        - ou compris entre 50 et 79 %. Dans ce cas, elle doit remplir deux conditions
        supplémentaires : être dans l’impossibilité de se procurer un emploi compte
        tenu de son handicap et ne pas avoir travaillé depuis au moins 1 an
        Condition de résidence
        L'AAH peut être versée aux personnes résidant en France métropolitaine ou
        dans les départements d'outre-mer ou à Saint-Pierre et Miquelon de façon permanente.
        Les personnes de nationalité étrangère doivent être en possession d'un titre de séjour
        régulier ou être titulaire d'un récépissé de renouvellement de titre de séjour.
        Condition d'âge
        Age minimum : Le demandeur ne doit plus avoir l'âge de bénéficier de l'allocation d'éducation de l'enfant
        handicapé, c'est-à-dire qu'il doit être âgé :
        - de plus de vingt ans,
        - ou de plus de seize ans, s'il ne remplit plus les conditions pour ouvrir droit aux allocations familiales.
        Pour les montants http://www.handipole.org/spip.php?article666

        Âge max_
        Le versement de l'AAH prend fin à partir de l'âge minimum légal de départ à la retraite en cas d'incapacité
        de 50 % à 79 %. À cet âge, le bénéficiaire bascule dans le régime de retraite pour inaptitude.
        En cas d'incapacité d'au moins 80 %, une AAH différentielle (c'est-à-dire une allocation mensuelle réduite)
        peut être versée au-delà de l'âge minimum légal de départ à la retraite en complément d'une retraite inférieure
        au minimum vieillesse.
    '''

    def formula(individu, period, parameters):
        law = parameters(period).prestations.minima_sociaux.aah
        taux_incapacite = individu('taux_incapacite', period)
        rsdae = individu('aah_restriction_substantielle_durable_acces_emploi', period)

        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        eligible_aah = (
            ((taux_incapacite >= law.taux_incapacite) + (taux_incapacite >= law.taux_incapacite_rsdae) * rsdae)
            * (age <= law.age_legal_retraite)
            * ((age >= law.age_minimal) + ((age >= 16) * (autonomie_financiere)))
            )

        return eligible_aah

        # TODO: dated_function : avant 2008, il fallait ne pas avoir travaillé pendant les 12 mois précédant la demande.


class aah_base_non_cumulable(Variable):
    value_type = float
    label = "Montant de l'Allocation adulte handicapé (hors complément) pour un individu, mensualisée"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu('pensions_invalidite', period) + individu('asi', period.last_month)


class aah_plafond_ressources(Variable):
    value_type = float
    label = "Montant plafond des ressources pour bénéficier de l'Allocation adulte handicapé (hors complément)"
    entity = Individu
    reference = [
        "Article D821-2 du Code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=4B54EC7065520E4812F84677B918A48E.tplgfr28s_2?idArticle=LEGIARTI000019077584&cidTexte=LEGITEXT000006073189&dateTexte=20081218"
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        law = parameters(period).prestations

        en_couple = individu.famille('en_couple', period)
        af_nbenf = individu.famille('af_nbenf', period)
        montant_max = law.minima_sociaux.aah.montant

        return montant_max * (
            + 1
            + en_couple
            * law.minima_sociaux.aah.majoration_plafond_couple
            + law.minima_sociaux.aah.majoration_plafond_personne_a_charge
            * af_nbenf
            )


class aah_base(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "Montant de l'Allocation adulte handicapé (hors complément) pour un individu, mensualisée"
    entity = Individu
    reference = [
        "Article L821-1 du Code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=53AFF5AA4010B01F0539052A33180B39.tplgfr35s_1?idArticle=LEGIARTI000033813790&cidTexte=LEGITEXT000006073189&dateTexte=20180412"
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        law = parameters(period).prestations

        aah_eligible = individu('aah_eligible', period)
        aah_base_ressources = individu('aah_base_ressources', period)
        plaf_ress_aah = individu('aah_plafond_ressources', period)
        # Le montant de l'AAH est plafonné au montant de base.
        montant_max = law.minima_sociaux.aah.montant
        montant_aah = min_(montant_max, max_(0, plaf_ress_aah - aah_base_ressources))

        aah_base_non_cumulable = individu('aah_base_non_cumulable', period)

        return aah_eligible * min_(montant_aah, max_(0, montant_max - aah_base_non_cumulable))


class aah(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "Allocation adulte handicapé mensualisée"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006754198"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        aah_base = individu('aah_base', period)
        aah_parameters = parameters(period).prestations.minima_sociaux.aah
        m_2 = datetime64(period.offset(-60, 'day').start)

        aah_date_debut_hospitalisation = individu("aah_date_debut_hospitalisation", period)
        aah_date_debut_incarceration = individu("aah_date_debut_incarceration", period)
        aah_reduction = (aah_date_debut_hospitalisation <= m_2) + (aah_date_debut_incarceration <= m_2)

        return where(aah_reduction, aah_base * aah_parameters.taux_aah_hospitalise_ou_incarcere, aah_base)


class eligibilite_caah(Variable):
    entity = Individu
    value_type = float
    label = "Eligibilité aux compléments à l'aah"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2015_07_01(individu, period, parameters):
        annee_precedente = period.start.period('year').offset(-1)
        prestations = parameters(period).prestations
        taux_incapacite_min = prestations.minima_sociaux.aah.taux_incapacite
        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)  # montant asi de la famille
        benef_asi = (asi_eligibilite * (asi > 0))
        taux_incapacite = individu('taux_incapacite', period)

        locataire_foyer = (individu.menage('statut_occupation_logement', period) == TypesStatutOccupationLogement.locataire_foyer)
        salaire_net = individu('salaire_net', annee_precedente, options = [ADD])

        return (
            (taux_incapacite >= taux_incapacite_min)
            * ((aah > 0) | (benef_asi > 0))
            * not_(locataire_foyer)
            * (salaire_net == 0)
            )


class caah(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "Complément d'allocation adulte handicapé (mensualisé)"
    entity = Individu
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula_2019_12_01(individu, period, parameters):
        eligibilite_caah = individu('eligibilite_caah', period)
        mva = individu('mva', period)
        return mva * eligibilite_caah

    def formula_2015_07_01(individu, period, parameters):
        eligibilite_caah = individu('eligibilite_caah', period)
        complement_ressources_aah = individu('complement_ressources_aah', period)
        mva = individu('mva', period)
        return max_(complement_ressources_aah, mva) * eligibilite_caah

    def formula_2005_07_01(individu, period, parameters):
        law = parameters(period).prestations

        garantie_ressources = law.minima_sociaux.caah.garantie_ressources
        aah_montant = law.minima_sociaux.aah.montant

        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)
        benef_asi = (asi_eligibilite * (asi > 0))

        # montant allocs logement de la famille
        al = individu.famille('aide_logement_montant', period)
        taux_incapacite = individu('taux_incapacite', period)

        elig_cpl = ((aah > 0) | (benef_asi > 0)) * (taux_incapacite >= law.minima_sociaux.aah.taux_incapacite)
        # TODO: & logement indépendant & inactif 12 derniers mois
        # & capa de travail < 5%
        compl_ress = elig_cpl * max_(garantie_ressources - aah_montant, 0)

        elig_mva = (al > 0) * ((aah > 0) | (benef_asi > 0))
        # TODO: & logement indépendant & pas de revenus professionnels
        # propres & capa de travail < 5% & taux d'incapacité >= 80%
        # TODO: rentrer mva dans paramètres. mva (mensuelle) = 104,77 en 2015, était de 101,80 en 2006, et de 119,72 en 2007
        mva = 0.0 * elig_mva

        return max_(compl_ress, mva)

    # TODO FIXME start date
    def formula_2002_01_01(individu, period, parameters):
        law = parameters(period).prestations

        cpltx = law.minima_sociaux.caah.taux_montant_complement_ressources
        aah_montant = law.minima_sociaux.aah.montant

        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)
        benef_asi = (asi_eligibilite * (asi > 0))
        # montant allocs logement de la famille
        al = individu.famille('aide_logement_montant', period)
        taux_incapacite = individu('taux_incapacite', period)

        # TODO: & logement indépendant
        elig_ancien_caah = (al > 0) * ((aah > 0) | (benef_asi > 0)) * (taux_incapacite >= law.minima_sociaux.aah.taux_incapacite)

        ancien_caah = cpltx * aah_montant * elig_ancien_caah
        # En fait le taux cpltx perdure jusqu'en 2008

        return ancien_caah


class complement_ressources_aah(Variable):
    entity = Individu
    value_type = float
    label = "Le complément de ressources"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006745305&dateTexte=&categorieLien=cid"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = "2019-11-30"

    def formula_2015_07_01(individu, period, parameters):
        prestations = parameters(period).prestations
        garantie_ressources = prestations.minima_sociaux.caah.garantie_ressources
        aah_montant = prestations.minima_sociaux.aah.montant
        taux_capacite_travail_max = prestations.minima_sociaux.aah.taux_capacite_travail
        taux_capacite_travail = individu('taux_capacite_travail', period)

        return (taux_capacite_travail < taux_capacite_travail_max) * max_(garantie_ressources - aah_montant, 0)


class mva(Variable):
    entity = Individu
    value_type = float
    label = "Majoration pour la vie autonome"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=6E5B97C7E6C7E06666BCFFA11871E70B.tplgfr43s_2?idArticle=LEGIARTI000006745350&cidTexte=LEGITEXT000006073189&dateTexte=20190124"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(individu, period, parameters):
        prestations = parameters(period).prestations
        al = individu.famille('aide_logement_montant', period)  # montant allocs logement de la famille
        mva_montant = prestations.minima_sociaux.caah.majoration_vie_autonome

        return mva_montant * (al > 0)


class pch(Variable):
    entity = Individu
    value_type = float
    label = "Prestation de compensation du handicap"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
