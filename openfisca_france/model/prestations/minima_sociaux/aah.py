from openfisca_core.periods import Period

from openfisca_france.model.base import *

from numpy import datetime64, absolute as abs_

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


class aah_base_ressources_conjugalisee(Variable):
    value_type = float
    label = "Base ressources de l'allocation adulte handicapé avant déconjugalisation"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):  # formule pour les cas les plus anciens, moins vérifiée (sans abattement à part celui de 20% sur les revenus du conjoint)
        _parameters = parameters(period)
        aah = _parameters.prestations_sociales.prestations_etat_de_sante.invalidite.aah

        def assiette_conjoint(revenus_conjoint):
            return (1 - _parameters.impot_revenu.calcul_revenus_imposables.deductions.abatpro.taux) * (1 - aah.abattement_conjoint.abattement_proportionnel) * revenus_conjoint

        def base_ressource_eval_annuelle():
            base_ressource = individu('aah_base_ressources_activite_eval_annuelle', period) + individu('aah_base_ressources_hors_activite_eval_annuelle', period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource + assiette_conjoint(base_ressource_conjoint)

        return base_ressource_eval_annuelle() / 12

    def formula_2005_07_01(individu, period, parameters):
        parameters = parameters(period)
        aah = parameters.prestations_sociales.prestations_etat_de_sante.invalidite.aah

        def assiette_conjoint(revenus_conjoint):
            return (1 - parameters.impot_revenu.calcul_revenus_imposables.deductions.abatpro.taux) * (1 - aah.abattement_conjoint.abattement_proportionnel) * revenus_conjoint

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_horaire = parameters.marche_travail.salaire_minimum.smic.smic_b_horaire
            seuil1 = aah.travail_ordinaire.tranche_smic_horaire1 * smic_brut_horaire
            seuil2 = aah.travail_ordinaire.tranche_smic_horaire2 * smic_brut_horaire
            seuil3 = aah.travail_ordinaire.tranche_smic_horaire3 * smic_brut_horaire
            seuil4 = aah.travail_ordinaire.tranche_smic_horaire4 * smic_brut_horaire
            total_tranche1 = min_(seuil1, revenus_demandeur) * (1 - aah.travail_ordinaire.abattement_300)
            total_tranche2 = max_(0, min_(revenus_demandeur - seuil1, seuil2 - seuil1)) * (1 - aah.travail_ordinaire.abattement_700)
            total_tranche3 = max_(0, min_(revenus_demandeur - seuil2, seuil3 - seuil2)) * (1 - aah.travail_ordinaire.abattement_1100)
            total_tranche4 = max_(0, min_(revenus_demandeur - seuil3, seuil4 - seuil3)) * (1 - aah.travail_ordinaire.abattement_1500)
            total_tranche5 = max_(0, revenus_demandeur - seuil4)
            return total_tranche1 + total_tranche2 + total_tranche3 + total_tranche4 + total_tranche5

        def base_ressource_eval_annuelle():
            base_ressource_activite = assiette_revenu_activite_demandeur(individu('aah_base_ressources_activite_eval_annuelle', period))
            base_ressource = base_ressource_activite + individu('aah_base_ressources_hors_activite_eval_annuelle', period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource + assiette_conjoint(base_ressource_conjoint)

        return base_ressource_eval_annuelle() / 12

    def formula_2011(individu, period, parameters):
        parameters = parameters(period)
        aah = parameters.prestations_sociales.prestations_etat_de_sante.invalidite.aah

        en_activite = (individu('salaire_imposable', period, options = [ADD]) + individu('rpns_imposables', period.last_year) > 0)

        def assiette_conjoint(revenus_conjoint):
            return (1 - parameters.impot_revenu.calcul_revenus_imposables.deductions.abatpro.taux) * (1 - aah.abattement_conjoint.abattement_proportionnel) * revenus_conjoint

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = 12 * parameters.marche_travail.salaire_minimum.smic.smic_b_horaire * parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
            total_tranche1 = min_(aah.travail_ordinaire.tranche_smic * smic_brut_annuel, revenus_demandeur)
            total_tranche2 = max_(0, revenus_demandeur - total_tranche1)
            return (1 - aah.travail_ordinaire.abattement_30) * total_tranche1 + (1 - aah.travail_ordinaire.abattement_sup) * total_tranche2

        def base_ressource_eval_trim():
            three_previous_months = Period(('month', period.first_month.start, 3)).offset(-3)
            base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
            base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])

            base_ressource_demandeur = max_(0, assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite)

            base_ressource_demandeur_conjoint = max_(0, individu.famille.demandeur('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_trimestrielle', period))
            base_ressource_conjoint_conjoint = max_(0, individu.famille.conjoint('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_trimestrielle', period))
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource_demandeur + assiette_conjoint(base_ressource_conjoint)

        def base_ressource_eval_annuelle():
            base_ressource_activite = assiette_revenu_activite_demandeur(individu('aah_base_ressources_activite_eval_annuelle', period))
            base_ressource = base_ressource_activite + individu('aah_base_ressources_hors_activite_eval_annuelle', period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource + assiette_conjoint(base_ressource_conjoint)

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12
            )

    def formula_2022_01_01(individu, period, parameters):
        parameters = parameters(period)
        aah = parameters.prestations_sociales.prestations_etat_de_sante.invalidite.aah

        en_activite = ((individu('salaire_imposable', period, options = [ADD]) + individu('rpns_imposables', period.last_year) > 0))

        def assiette_conjoint(revenus_conjoint):
            af_nbenf = individu.famille('af_nbenf', period)
            revenus = (1 - parameters.impot_revenu.calcul_revenus_imposables.deductions.abatpro.taux) * revenus_conjoint
            return max_(revenus - (aah.abattement_conjoint.abattement_forfaitaire.base + aah.abattement_conjoint.abattement_forfaitaire.majoration_pac * af_nbenf), 0)

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = 12 * parameters.marche_travail.salaire_minimum.smic.smic_b_horaire * parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
            total_tranche1 = min_(aah.travail_ordinaire.tranche_smic * smic_brut_annuel, revenus_demandeur)
            total_tranche2 = max_(0, revenus_demandeur - total_tranche1)
            return (1 - aah.travail_ordinaire.abattement_30) * total_tranche1 + (1 - aah.travail_ordinaire.abattement_sup) * total_tranche2

        def base_ressource_eval_trim():
            three_previous_months = Period(('month', period.first_month.start, 3)).offset(-3)
            base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
            base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])

            base_ressource_demandeur = max_(0, assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_trimestrielle', period)
            base_ressource_conjoint_conjoint = max_(0, individu.famille.conjoint('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_trimestrielle', period))
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource_demandeur + assiette_conjoint(base_ressource_conjoint)

        def base_ressource_eval_annuelle():
            base_ressource_activite = assiette_revenu_activite_demandeur(individu('aah_base_ressources_activite_eval_annuelle', period))
            base_ressource = base_ressource_activite + individu('aah_base_ressources_hors_activite_eval_annuelle', period)

            base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_annuelle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_annuelle', period)
            base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

            return base_ressource + assiette_conjoint(base_ressource_conjoint)

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12
            )


class aah_base_ressources_deconjugalisee(Variable):
    value_type = float
    label = "Base ressources de l'allocation adulte handicapé après déconjugalisation"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2023_10_01(individu, period, parameters):
        parameters = parameters(period)
        aah = parameters.prestations_sociales.prestations_etat_de_sante.invalidite.aah

        en_activite = ((individu('salaire_imposable', period, options = [ADD]) + individu('rpns_imposables', period.last_year)) > 0)

        def assiette_revenu_activite_demandeur(revenus_demandeur):
            smic_brut_annuel = 12 * parameters.marche_travail.salaire_minimum.smic.smic_b_horaire * parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
            total_tranche1 = min_(aah.travail_ordinaire.tranche_smic * smic_brut_annuel, revenus_demandeur)
            total_tranche2 = max_(0, revenus_demandeur - total_tranche1)
            return (1 - aah.travail_ordinaire.abattement_30) * total_tranche1 + (1 - aah.travail_ordinaire.abattement_sup) * total_tranche2

        def base_ressource_eval_trim():
            three_previous_months = Period(('month', period.first_month.start, 3)).offset(-3)
            base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
            base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])

            base_ressource_demandeur = max_(0, assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite)

            return base_ressource_demandeur

        def base_ressource_eval_annuelle():
            base_ressource_activite = assiette_revenu_activite_demandeur(individu('aah_base_ressources_activite_eval_annuelle', period))
            base_ressource = base_ressource_activite + individu('aah_base_ressources_hors_activite_eval_annuelle', period)

            return base_ressource

        return where(
            en_activite,
            base_ressource_eval_trim() / 12,
            base_ressource_eval_annuelle() / 12
            )
        # TODO: - Prendre en compte les abattements temporaires sur les ressources en cas de changement de situation (6 mois pour retour à l'emploi, un an pour inactivité)
        #       - La formule du calcul de la base de ressource est celle en vigueur à partir de 2011, avant 2011:
        #           - l'abattement pour les personnes invalides (défini dans l'art. 157 du CGI) sur le revenu net global est pris en compte (art. R821-4 du CSS)


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
        three_previous_months = Period(('month', period.start, 3)).offset(-3)
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
        three_previous_months = Period(('month', period.start, 3)).offset(-3)

        ressources_a_inclure = [
            'asi',
            'allocation_securisation_professionnelle',
            'bourse_recherche',
            'gains_exceptionnels',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'retraite_nette',
            'rsa_base_ressources_patrimoine_individu',
            ]

        ressources = sum(
            [individu(ressource, three_previous_months, options = [ADD]) for ressource in ressources_a_inclure]
            )
        # On récupère le montant absolu des pensions alimentaires versées au cas où la valeur reçue est négative
        pensions_alimentaires_versees = abs_(individu(
            'pensions_alimentaires_versees_individu', three_previous_months, options = [ADD]))

        # On soustrait le montant des pensions alimentaires versées à la base des ressources
        return (ressources - pensions_alimentaires_versees) * 4


class aah_base_ressources_activite_eval_annuelle(Variable):
    value_type = float
    label = "Base de ressources de l'AAH pour un individu, évaluation annuelle"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article R532-5 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006750910'
        ]
    # TODO prendre en compte l'abattement sur les revenus de l'année précédente entre 2005 et 2010 lorsqu'une période d'inactivité
    # sans revenu de remplacement survient (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006739692/2005-07-01/)
    # et les autres abattements sur reprise d'activité https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000023086051/#JORFARTI000023086056 (notamment Art.D. 821-9 1°)

    def formula(individu, period, parameters):
        return (
            individu('salaire_imposable', period.n_2, options = [ADD])
            + individu('rpns_imposables', period.n_2)
            + individu('chomage_imposable', period.n_2, options = [ADD]))


class aah_base_ressources_hors_activite_eval_annuelle(Variable):
    value_type = float
    label = "Base de ressources de l'AAH pour un individu, évaluation annuelle"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article R532-5 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006750910'
        ]
    # TODO prendre en compte l'abattement sur les revenus de l'année précédente entre 2005 et 2010 lorsqu'une période d'inactivité
    # sans revenu de remplacement survient (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006739692/2005-07-01/)

    def formula(individu, period, parameters):
        return (individu('revenu_assimile_pension', period.n_2))


class aah_restriction_substantielle_durable_acces_emploi(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = "Restriction substantielle et durable pour l'accès à l'emploi reconnue par la commission des droits et de l'autonomie des personnes handicapées"
    reference = [
        'Article L821-2 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=17BE3036A19374AA1C8C7A4169702CD7.tplgfr24s_2?idArticle=LEGIARTI000020039305&cidTexte=LEGITEXT000006073189&dateTexte=20180731'
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aah_eligible(Variable):
    value_type = bool
    label = "Eligibilité à l'Allocation adulte handicapé"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = ['Article 821-1 du Code de la sécurité sociale', 'https://www.legifrance.gouv.fr/codes/id/LEGIARTI000006739685/']

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

        Avant 2011, l'allocation était perçue uniquement pour les personnes sans activité les douze mois précédents
        (ref https://www.legifrance.gouv.fr/codes/id/LEGIARTI000006739685/2005-06-30/),
        mais ce n'était pas le cas avant 2005 ref https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000002101708
    '''

    def formula_2011_01_01(individu, period, parameters):
        parameters_aah = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
        taux_incapacite = individu('taux_incapacite', period)
        taux_incapacite_max = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite)
        taux_incapacite_rsdae = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite_rsdae)
        rsdae = individu('aah_restriction_substantielle_durable_acces_emploi', period)

        age = individu('age', period)
        prestations_familiales_enfant_a_charge = individu('prestations_familiales_enfant_a_charge', period)
        eligible_aah = (
            (taux_incapacite_max + (taux_incapacite_rsdae * rsdae * (age <= parameters_aah.age_legal_retraite)))
            * ((age >= parameters_aah.age_minimal) + ((age >= parameters_aah.age_fin_educ) * not_(prestations_familiales_enfant_a_charge)))
            )

        return eligible_aah

    def formula_2005_07_01(individu, period, parameters):
        parameters_aah = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
        taux_incapacite = individu('taux_incapacite', period)
        taux_incapacite_max = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite)
        taux_incapacite_rsdae = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite_rsdae)
        rsdae = individu('aah_restriction_substantielle_durable_acces_emploi', period)

        age = individu('age', period)
        prestations_familiales_enfant_a_charge = individu('prestations_familiales_enfant_a_charge', period)
        eligible_aah = (
            (taux_incapacite_max + (taux_incapacite_rsdae * rsdae * (age <= parameters_aah.age_legal_retraite))
            * (individu('salaire_imposable', period.last_year, options=[ADD]) <= 0))
            * ((age >= parameters_aah.age_minimal) + ((age >= parameters_aah.age_fin_educ) * not_(prestations_familiales_enfant_a_charge)))
            )
        return eligible_aah

    def formula(individu, period, parameters):
        parameters_aah = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
        taux_incapacite = individu('taux_incapacite', period)
        taux_incapacite_max = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite)
        taux_incapacite_rsdae = (taux_incapacite >= parameters_aah.taux_capacite.taux_incapacite_rsdae)
        rsdae = individu('aah_restriction_substantielle_durable_acces_emploi', period)

        age = individu('age', period)
        prestations_familiales_enfant_a_charge = individu('prestations_familiales_enfant_a_charge', period)
        eligible_aah = (
            (taux_incapacite_max + (taux_incapacite_rsdae * rsdae
            * (age <= parameters_aah.age_legal_retraite)))
            * ((age >= parameters_aah.age_minimal) + ((age >= parameters_aah.age_fin_educ) * not_(prestations_familiales_enfant_a_charge)))
            )
        return eligible_aah


class aah_base_non_cumulable(Variable):
    value_type = float
    label = "Montant de l'Allocation adulte handicapé (hors complément) pour un individu, mensualisée"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu('pensions_invalidite', period) + individu('asi', period.last_month)


class aah_plafond_ressources_conjugalise(Variable):
    value_type = float
    label = "Montant plafond des ressources pour bénéficier de l'Allocation adulte handicapé (hors complément) avant déconjugalisation"
    entity = Individu
    reference = [
        'Article D821-2 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=4B54EC7065520E4812F84677B918A48E.tplgfr28s_2?idArticle=LEGIARTI000019077584&cidTexte=LEGITEXT000006073189&dateTexte=20081218'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    '''
         A partir du 01/10/2023, la déconjugalisation est la règle par défaut.
         Seules les personnes ayant droit à la conjugalisation sans interruption
         depuis cette date peuvent garder l'ancien calcul.
    '''

    def formula(individu, period, parameters):
        parameters = parameters(period).prestations_sociales

        en_couple = individu.famille('en_couple', period)
        af_nbenf = individu.famille('af_nbenf', period)
        montant_max = parameters.prestations_etat_de_sante.invalidite.aah.montant

        return montant_max * (
            + 1
            + en_couple
            * parameters.prestations_etat_de_sante.invalidite.aah.majoration_plafond.majoration_plafond_couple
            + parameters.prestations_etat_de_sante.invalidite.aah.majoration_plafond.majoration_par_enfant_supplementaire
            * af_nbenf
            )


class aah_plafond_ressources_deconjugalise(Variable):
    value_type = float
    label = "Montant plafond des ressources pour bénéficier de l'Allocation adulte handicapé (hors complément) après déconjugalisation"
    entity = Individu
    reference = [
        'Article D821-2 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=4B54EC7065520E4812F84677B918A48E.tplgfr28s_2?idArticle=LEGIARTI000019077584&cidTexte=LEGITEXT000006073189&dateTexte=20081218'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        parameters = parameters(period).prestations_sociales

        af_nbenf = individu.famille('af_nbenf', period)
        montant_max = parameters.prestations_etat_de_sante.invalidite.aah.montant

        return montant_max * (
            + 1
            + parameters.prestations_etat_de_sante.invalidite.aah.majoration_plafond.majoration_par_enfant_supplementaire
            * af_nbenf
            )


class aah_conjugalise_eligible(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Eligibilité à la conjugalisation de l'AAH après le 01/10/2023"
    reference = [
        'Décret 2022-1694 du 28 décembre 2022',
        'https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000046830064'
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aah_base(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "Montant de l'Allocation adulte handicapé (hors complément) pour un individu, mensualisée"
    entity = Individu
    reference = [
        'Article L821-1 du Code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=53AFF5AA4010B01F0539052A33180B39.tplgfr35s_1?idArticle=LEGIARTI000033813790&cidTexte=LEGITEXT000006073189&dateTexte=20180412'
        " D'après service-public : 'Si vous touchez une pension ou une rente, vous recevez la différence entre le montant de votre pension ou rente et le montant maximal de l'AAH', le montant évoqué est donc le maximal"]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        parameters = parameters(period).prestations_sociales

        aah_eligible = individu('aah_eligible', period)
        aah_base_ressources_conjugalisee = individu('aah_base_ressources_conjugalisee', period)
        plaf_ress_aah_conjugalise = individu('aah_plafond_ressources_conjugalise', period)
        # Le montant de l'AAH est plafonné au montant de base.
        montant_max = parameters.prestations_etat_de_sante.invalidite.aah.montant
        montant_aah = min_(montant_max, max_(0, plaf_ress_aah_conjugalise - aah_base_ressources_conjugalisee))

        aah_base_non_cumulable = individu('aah_base_non_cumulable', period)

        return aah_eligible * min_(max_(0, montant_aah), max_(0, montant_max - aah_base_non_cumulable))

    def formula_2023_10_01(individu, period, parameters):
        parameters = parameters(period).prestations_sociales
        # Le montant de l'AAH est plafonné au montant de base.
        montant_max = parameters.prestations_etat_de_sante.invalidite.aah.montant
        aah_eligible = individu('aah_eligible', period)
        aah_base_non_cumulable = individu('aah_base_non_cumulable', period)
        aah_conjugalise_eligible = individu('aah_conjugalise_eligible', period)

        aah_base_ressources_conjugalisee = individu('aah_base_ressources_conjugalisee', period)
        plaf_ress_aah_conjugalise = individu('aah_plafond_ressources_conjugalise', period)
        montant_aah_conjugalise = min_(montant_max, max_(0, plaf_ress_aah_conjugalise - aah_base_ressources_conjugalisee))
        aah_conjugalise = aah_eligible * min_(max_(0, montant_aah_conjugalise), max_(0, montant_max - aah_base_non_cumulable))

        aah_base_ressources_deconjugalisee = individu('aah_base_ressources_deconjugalisee', period)
        plaf_ress_aah_deconjugalise = individu('aah_plafond_ressources_deconjugalise', period)
        montant_aah_deconjugalise = min_(montant_max, max_(0, plaf_ress_aah_deconjugalise - aah_base_ressources_deconjugalisee))
        aah_deconjugalise = aah_eligible * min_(max_(0, montant_aah_deconjugalise), max_(0, montant_max - aah_base_non_cumulable))

        return where(aah_conjugalise_eligible, max_(aah_conjugalise, aah_deconjugalise), aah_deconjugalise)


class aah(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = 'Allocation adulte handicapé mensualisée'
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006754198'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        aah_base = individu('aah_base', period)
        aah_parameters = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
        m_2 = datetime64(period.offset(-60, 'day').start)

        aah_date_debut_hospitalisation = individu('aah_date_debut_hospitalisation', period)
        aah_date_debut_incarceration = individu('aah_date_debut_incarceration', period)
        pers_charge = (individu.foyer_fiscal('nb_pac', period.last_year) > 0)
        aah_reduction = ((aah_date_debut_hospitalisation <= m_2) + (aah_date_debut_incarceration <= m_2)) * not_(pers_charge)

        return where(aah_reduction, aah_base * aah_parameters.pourcentage_aah.prison_hospitalisation, aah_base)
        # montant_max_aah = parameters.prestations_etat_de_sante.invalidite.aah.montant
        # est-ce cela, ou plutôt where(aah_reduction, min_(aah_base, aah_parameters.pourcentage_aah.prison_hospitalisation * montant_max_aah), aah_base)
        # ce qui expliquerait la phrase : L'intéressé ne peut recevoir une allocation plus élevée que celle qu'il percevrait s'il n'était pas hospitalisé, placé dans une maison d'accueil spécialisée ou incarcéré.
        # TODO: exemption de baisse également si paiement d'un forfait journalier (lors de l'hospitalisation), et si le conjoint ne travaille pas pour une raison reconnue valable
        # jusqu'en 2005, un taux différent selon si marié ou pas (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031828843/2016-01-01/)


class eligibilite_caah(Variable):
    entity = Individu
    value_type = float
    label = "Eligibilité aux compléments à l'aah"
    reference = ['https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039802699']

    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2015_07_01(individu, period, parameters):
        annee_precedente = Period(('year', period.start, 1)).offset(-1)
        prestations = parameters(period).prestations_sociales
        taux_incapacite_min = prestations.prestations_etat_de_sante.invalidite.aah.taux_capacite.taux_incapacite
        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)  # montant asi de la famille
        benef_asi = (asi_eligibilite * (asi > 0))
        taux_incapacite = individu('taux_incapacite', period)
        locataire_foyer = (individu.menage('statut_occupation_logement', period) == TypesStatutOccupationLogement.locataire_foyer)
        logement_independant = (individu.has_role(Menage.PERSONNE_DE_REFERENCE) + individu.has_role(Menage.CONJOINT)) * not_(locataire_foyer)

        activite_12_mois = individu('salaire_imposable', annee_precedente, options = [ADD]) + individu('rpns_imposables', annee_precedente)  # substitution à vérifier

        return (
            (taux_incapacite >= taux_incapacite_min)
            * ((aah > 0) | (benef_asi > 0))
            * logement_independant
            * (activite_12_mois == 0)
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
        invalidite = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite
        annee_precedente = Period(('year', period.start, 1)).offset(-1)
        activite_12_mois = individu('salaire_imposable', annee_precedente, options = [ADD]) + individu('rpns_imposables', annee_precedente)

        garantie_ressources = invalidite.caah.garantie_ressources
        aah_montant = invalidite.aah.montant

        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)
        benef_asi = (asi_eligibilite * (asi > 0))

        # montant allocs logement de la famille
        al = individu.famille('aide_logement_montant', period)
        taux_incapacite = individu('taux_incapacite', period)
        # taux_capacite = individu('taux_capacite_travail', period) dans la législation, mais moins usité que le taux d'incapacité

        locataire_foyer = (individu.menage('statut_occupation_logement', period) == TypesStatutOccupationLogement.locataire_foyer)
        logement_independant = (individu.has_role(Menage.PERSONNE_DE_REFERENCE) + individu.has_role(Menage.CONJOINT)) * not_(locataire_foyer)
        incapacite = (taux_incapacite >= invalidite.aah.taux_capacite.taux_incapacite)

        elig_cpl = ((aah > 0) | (benef_asi > 0)) * incapacite * (activite_12_mois == 0) * logement_independant  # * non_capacite
        # TODO: revenus professionnels ?
        compl_ress = elig_cpl * max_(garantie_ressources - aah_montant, 0)

        elig_mva = (al > 0) * ((aah > 0) | (benef_asi > 0)) * incapacite * (activite_12_mois == 0) * logement_independant  # * non_capacite

        mva = invalidite.caah.majoration_vie_autonome * elig_mva

        return max_(compl_ress, mva)

    def formula_1994_07_01(individu, period, parameters):
        prestations_etat_de_sante = parameters(period).prestations_sociales.prestations_etat_de_sante
        cpltx = prestations_etat_de_sante.invalidite.caah.taux_montant_complement_ressources
        aah_montant = prestations_etat_de_sante.invalidite.aah.montant
        aah = individu('aah', period)
        asi_eligibilite = individu('asi_eligibilite', period)
        asi = individu('asi', period)
        benef_asi = (asi_eligibilite * (asi > 0))
        al = individu.famille('aide_logement_montant', period)
        taux_incapacite = individu('taux_incapacite', period)
        locataire_foyer = (individu.menage('statut_occupation_logement', period) == TypesStatutOccupationLogement.locataire_foyer)
        elig_ancien_caah = (al > 0) * ((aah > 0) | (benef_asi > 0)) * (taux_incapacite >= prestations_etat_de_sante.invalidite.aah.taux_capacite.taux_incapacite) * not_(locataire_foyer)
        ancien_caah = cpltx * aah_montant * elig_ancien_caah
        # En fait le taux cpltx perdure jusqu'en 2008 officiellement, la différence garantie-ressource et aah restant cependant constante égale à la valeur du complément d'allocation, 179,31
        return ancien_caah


class complement_ressources_aah(Variable):
    entity = Individu
    value_type = float
    label = 'Le complément de ressources'
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006745305&dateTexte=&categorieLien=cid'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2019-11-30'

    def formula_2015_07_01(individu, period, parameters):
        prestations = parameters(period).prestations_sociales
        garantie_ressources = prestations.prestations_etat_de_sante.invalidite.caah.garantie_ressources
        aah_montant = prestations.prestations_etat_de_sante.invalidite.aah.montant
        taux_capacite_travail_max = prestations.prestations_etat_de_sante.invalidite.aah.taux_capacite.taux_capacite_travail
        taux_capacite_travail = individu('taux_capacite_travail', period)

        return (taux_capacite_travail < taux_capacite_travail_max) * max_(garantie_ressources - aah_montant, 0)


class mva(Variable):
    entity = Individu
    value_type = float
    label = 'Majoration pour la vie autonome'
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=6E5B97C7E6C7E06666BCFFA11871E70B.tplgfr43s_2?idArticle=LEGIARTI000006745350&cidTexte=LEGITEXT000006073189&dateTexte=20190124'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(individu, period, parameters):
        prestations = parameters(period).prestations_sociales
        al = individu.famille('aide_logement_montant', period)  # montant allocs logement de la famille
        mva_montant = prestations.prestations_etat_de_sante.invalidite.caah.majoration_vie_autonome

        return mva_montant * (al > 0)


class pch(Variable):  # inutilisée pour l'instant
    entity = Individu
    value_type = float
    label = 'Prestation de compensation du handicap'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
