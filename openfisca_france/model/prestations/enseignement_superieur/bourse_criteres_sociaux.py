from openfisca_core.model_api import not_, select, where, Variable, MONTH, set_input_divide_by_period, set_input_dispatch_by_period
from openfisca_france.model.base import Famille, Individu, TypesStatutMarital
from openfisca_france.model.prestations.education import TypesScolarite, StatutsEtablissementScolaire


class bourse_criteres_sociaux(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Montant de la bourse sur critères sociaux (BCS) de l'enseignement supérieur perçue"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        montants = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.montants
        echelon = individu('bourse_criteres_sociaux_echelon', period)

        return montants.calc(echelon)


class bourse_criteres_sociaux_eligibilite_etude(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 1 - Conditions d'études",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Satisfaction des critères d'étude pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        enseignement_superieur = individu('scolarite', period) == TypesScolarite.enseignement_superieur

        temps_plein = not_(individu('alternant', period))

        etablissement = individu('statuts_etablissement_scolaire', period)
        etablissement_eligible = (etablissement == StatutsEtablissementScolaire.public) + (etablissement == StatutsEtablissementScolaire.prive_sous_contrat)

        return enseignement_superieur * temps_plein * etablissement_eligible


class bourse_criteres_sociaux_eligibilite_nationalite(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - 2.3.A",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Satisfaction des critères de nationalité pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2004_07_21(individu, period, parameters):
        '''
        Reference: https://www.education.gouv.fr/bo/2004/30/MENS0401499C.htm
        '''
        ressortissant_eee = individu('ressortissant_eee', period)

        nationalite = individu('nationalite', period)
        ressortissant_pays_eligible = sum([nationalite == str.encode(etat) for etat in parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.nationalites_hors_eee])  # TOOPTIMIZE: string encoding into bytes array should be done at load time

        return ressortissant_eee + ressortissant_pays_eligible

    def formula_2003_04_23(individu, period):
        '''
        Reference: https://www.education.gouv.fr/bo/2003/18/MENS0300894C.htm
        '''
        return individu('resident_ue', period)


class bourse_criteres_sociaux_nombre_enfants_parent_etudiant(Variable):
    value_type = int
    entity = Famille
    reference = [
        "Circulaire ESRS2013435C - Annexe 2 - Critères d'attribution / 1 - Conditions d'âge",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Nombre d'enfants de l'étudiant pour le calcul de la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        return famille.nb_persons(Famille.ENFANT)


class bourse_criteres_sociaux_eligibilite_age(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 2 - Critères d'attribution / 1 - Conditions d'âge",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Satisfaction des critères d'âge pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        age = individu('age', period)
        nb_enf = individu.famille('bourse_criteres_sociaux_nombre_enfants_parent_etudiant', period)
        age_maximum = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.age_maximum
        handicap = individu('handicap', period)

        return (age <= (age_maximum + nb_enf)) + (handicap)


class bourse_criteres_sociaux_eligibilite(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 2 - Critères d'attribution",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Éligibilité aux bourses sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        eligibilite_age = individu('bourse_criteres_sociaux_eligibilite_age', period)
        eligibilite_etude = individu('bourse_criteres_sociaux_eligibilite_etude', period)
        eligibilite_nationalite = individu('bourse_criteres_sociaux_eligibilite_nationalite', period)

        return eligibilite_age * eligibilite_etude * eligibilite_nationalite


class bourse_criteres_sociaux_base_ressources(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Ressources prise en compte pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        autonome = individu('bourse_criteres_sociaux_etudiant_autonome', period)
        ressources_autonome = individu('bourse_criteres_sociaux_base_ressources_etudiant_autonome', period)
        ressources_parentales = individu('bourse_criteres_sociaux_base_ressources_parentale', period)
        return where(autonome, ressources_autonome, ressources_parentales)


class bourse_criteres_sociaux_base_ressources_parentale(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Ressources parentales prises en compte pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class bourse_criteres_sociaux_base_ressources_etudiant_autonome(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources / 1.2.2 - Relatives aux revenus",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Ressources de l'étudiant pour le barème pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu.foyer_fiscal('rbg', period.n_2)


class bourse_criteres_sociaux_etudiant_autonome_ressource_mensuelle(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources / 1.2.2 - Relatives aux revenus",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Ressources mensuelle prise en compte pour déterminer l'autonomie financière de l'étudiant pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu.famille('rsa_base_ressources', period)


class bourse_criteres_sociaux_etudiant_autonome(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources / 1.2.2 - Relatives aux revenus",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Indicatrice de la satisfaction des critères d'autonomie pour l'étudiant dans le cadre de l'évaluation de la bourse sur critères sociaux"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        statut_marital = individu('statut_marital', period)
        en_couple = (statut_marital == TypesStatutMarital.marie) + (statut_marital == TypesStatutMarital.pacse)

        ressources = individu('bourse_criteres_sociaux_etudiant_autonome_ressource_mensuelle', period)
        legislation = parameters(period)

        smic_mensuel_brut = legislation.marche_travail.salaire_minimum.smic.smic_b_horaire * legislation.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
        smic_mensuel_net = smic_mensuel_brut * 8.11 / 10.25
        seuil_ressources = legislation.prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.seuil_ressources_etudiant_autonome * smic_mensuel_net
        eligible_couple = en_couple * (seuil_ressources <= ressources)

        is_parent = individu.has_role(Famille.PARENT)
        propre_declaration_fiscale = not_(individu('enfant_a_charge', period.this_year))
        avec_des_enfants = individu.famille('bourse_criteres_sociaux_nombre_enfants_parent_etudiant', period) > 0

        eligible_etudiant_parent_isole = is_parent * propre_declaration_fiscale * avec_des_enfants

        return eligible_couple + eligible_etudiant_parent_isole


class bourse_criteres_sociaux_points_de_charge(Variable):
    entity = Individu
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Nombre de points de charge pour la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        pts_distance = individu('bourse_criteres_sociaux_points_de_charge_distance_domicile_familial', period)
        pts_charges = individu('bourse_criteres_sociaux_points_de_charge_charges_familiale', period)
        return pts_distance + pts_charges


class bourse_criteres_sociaux_points_de_charge_distance_domicile_familial(Variable):
    entity = Individu
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux / 2.1 - Les charges de l'étudiant",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Distance entre le lieu d'étude et le domicile familial pour le calcul la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        distance = individu('bourse_criteres_sociaux_distance_domicile_familial', period)
        bareme = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.points_de_charge.distance_domicile_familial
        return bareme.calc(distance)


class bourse_criteres_sociaux_distance_domicile_familial(Variable):
    entity = Individu
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux / 2.1 - Les charges de l'étudiant",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Distance en kilomètres entre le lieu d'étude et le domicile familial"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class bourse_criteres_sociaux_nombre_enfants_a_charge(Variable):
    entity = Famille
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux / 2.2 - Les charges de la famille",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Nombre total d'enfants à la charge de la famille pour le calcul de la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class bourse_criteres_sociaux_nombre_enfants_a_charge_dans_enseignement_superieur(Variable):
    entity = Famille
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux / 2.2 - Les charges de la famille",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Nombre total d'enfants à la charge de la famille et étudiants dans l'enseignement supérieur pour le calcul la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class bourse_criteres_sociaux_points_de_charge_charges_familiale(Variable):
    entity = Individu
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 2 - Points de charge à prendre en considération pour l'attribution d'une bourse sur critères sociaux / 2.2 - Les charges de la famille",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Points de charge associés aux charges de la famille pour le alcul la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        nb_enf = individu.famille('bourse_criteres_sociaux_nombre_enfants_a_charge', period)
        nb_enf_ens_sup = individu.famille('bourse_criteres_sociaux_nombre_enfants_a_charge_dans_enseignement_superieur', period)

        nb_enf_hors_ens_sup = nb_enf - nb_enf_ens_sup
        nb_autre_enf_ens_sup = nb_enf_ens_sup - 1

        pts = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.points_de_charge.charges_familiales
        pts_enf = (nb_enf_hors_ens_sup > 0) * nb_enf_hors_ens_sup * pts.par_enfant_a_charge
        pts_ens_sup = (nb_autre_enf_ens_sup > 0) * nb_autre_enf_ens_sup * pts.par_enfant_etudiant
        return pts_enf + pts_ens_sup


class bourse_criteres_sociaux_echelon(Variable):
    entity = Individu
    value_type = int
    reference = [
        "Circulaire ESRS2013435C - Annexe 7 - Taux et cumul de la bourse d'enseignement supérieur sur critères sociaux / 1 - Les taux de bourse d'enseignement supérieur sur critères sociaux",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm",
        "Arrêté du 22 juillet 2020 fixant les plafonds de ressources relatifs aux bourses d'enseignement supérieur du ministère de l'enseignement supérieur, de la recherche et de l'innovation pour l'année universitaire 2020-2021",
        "https://www.legifrance.gouv.fr/eli/arrete/2020/7/22/ESRS2016543A/jo/texte"
        ]
    label = "Échelon de la bourse sur critères sociaux de l'enseignement supérieur en prenant uniquement en compte les critères de ressources et de points de charge"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        points_de_charge = individu('bourse_criteres_sociaux_points_de_charge', period)
        baremes = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.plafond_ressources
        plafond_echelon_0bis = baremes.echelon_0bis.calc(points_de_charge)
        plafond_echelon_1 = baremes.echelon_1.calc(points_de_charge)
        plafond_echelon_2 = baremes.echelon_2.calc(points_de_charge)
        plafond_echelon_3 = baremes.echelon_3.calc(points_de_charge)
        plafond_echelon_4 = baremes.echelon_4.calc(points_de_charge)
        plafond_echelon_5 = baremes.echelon_5.calc(points_de_charge)
        plafond_echelon_6 = baremes.echelon_6.calc(points_de_charge)
        plafond_echelon_7 = baremes.echelon_7.calc(points_de_charge)

        base_ressources = individu('bourse_criteres_sociaux_base_ressources', period)
        echelon = select(
            [
                base_ressources <= plafond_echelon_7,
                base_ressources <= plafond_echelon_6,
                base_ressources <= plafond_echelon_5,
                base_ressources <= plafond_echelon_4,
                base_ressources <= plafond_echelon_3,
                base_ressources <= plafond_echelon_2,
                base_ressources <= plafond_echelon_1,
                base_ressources <= plafond_echelon_0bis,
                ],
            [7, 6, 5, 4, 3, 2, 1, 0], default=-1)

        eligible = individu('bourse_criteres_sociaux_eligibilite', period)
        return where(eligible, echelon, -1)
