# -*- coding: utf-8 -*-

from functools import partial
from numpy import busday_count as original_busday_count, datetime64, timedelta64
from openfisca_france.model.base import *  # noqa analysis:ignore


class indemnites_stage(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités de stage"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class revenus_stage_formation_pro(Variable):
    value_type = float
    entity = Individu
    label = u"Revenus de stage de formation professionnelle"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class bourse_recherche(Variable):
    value_type = float
    entity = Individu
    label = u"Bourse de recherche"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class sal_pen_exo_etr(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AC",
        QUIFOY['conj']: u"1BC",
        QUIFOY['pac1']: u"1CC",
        QUIFOY['pac2']: u"1DC",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class frais_reels(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AK",
        QUIFOY['conj']: u"1BK",
        QUIFOY['pac1']: u"1CK",
        QUIFOY['pac2']: u"1DK",
        QUIFOY['pac3']: u"1EK",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Frais réels"
    definition_period = YEAR


class hsup(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AU",
        QUIFOY['conj']: u"1BU",
        QUIFOY['pac1']: u"1CU",
        QUIFOY['pac2']: u"1DU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Heures supplémentaires : revenus exonérés connus"
    # start_date = date(2007, 1, 1)
    end = '2013-12-13'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class ppe_du_sa(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AV",
        QUIFOY['conj']: u"1BV",
        QUIFOY['pac1']: u"1CV",
        QUIFOY['pac2']: u"1DV",
        QUIFOY['pac3']: u"1QV",
        }
    value_type = int
    entity = Individu
    label = u"Prime pour l'emploi des salariés: nombre d'heures payées"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        contrat_travail = individu('contrat_de_travail', period)
        travail_temps_decompte_en_heures = (
            (contrat_travail == TypesContratDeTravail.temps_partiel)
            + (contrat_travail == TypesContratDeTravail.forfait_heures_semaines)
            + (contrat_travail == TypesContratDeTravail.forfait_heures_mois)
            + (contrat_travail == TypesContratDeTravail.forfait_heures_annee)
            + (contrat_travail == TypesContratDeTravail.forfait_jours_annee)
        )

        return heures_remunerees_volume * travail_temps_decompte_en_heures


class ppe_tp_sa(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AX",
        QUIFOY['conj']: u"1BX",
        QUIFOY['pac1']: u"1CX",
        QUIFOY['pac2']: u"1DX",
        QUIFOY['pac3']: u"1QX",
        }
    value_type = bool
    entity = Individu
    label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière"
    definition_period = YEAR

    def formula(individu, period):
        mois = period.first_month
        indicateur = individu('contrat_de_travail', mois) == 0
        # On parcours tous les mois de l'année pour s'assurer que l'individu était employé à temps plein
        # durant toute l'année.
        while mois.start.month < 12:
            mois = mois.offset(1)
            indicateur = indicateur & (individu('contrat_de_travail', mois) == 0)
        return indicateur


class exposition_accident(Variable):
    value_type = Enum
    possible_values = TypesExpositionAccident  # defined in model/base.py
    default_value = TypesExpositionAccident.faible
    entity = Individu
    label = u"Exposition au risque pour les accidents du travail"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class exposition_penibilite(Variable):
    value_type = Enum
    possible_values = TypesExpositionPenibilite   # defined in model/base.py
    default_value = TypesExpositionPenibilite.nulle
    entity = Individu
    label = u"Exposition à un ou plusieurs facteurs de pénibilité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class allegement_fillon_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesAllegementModeRecouvrement  # defined in model/base.py
    default_value = TypesAllegementModeRecouvrement.fin_d_annee
    entity = Individu
    label = u"Mode de recouvrement des allègements Fillon"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class allegement_cotisation_allocations_familiales_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesAllegementModeRecouvrement  # defined in model/base.py
    default_value = TypesAllegementModeRecouvrement.fin_d_annee
    entity = Individu
    label = u"Mode de recouvrement de l'allègement de la cotisation d'allocations familiales"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class apprentissage_contrat_debut(Variable):
    value_type = date
    entity = Individu
    label = u"Date de début du contrat d'apprentissage"
    definition_period = MONTH


class arrco_tranche_a_taux_employeur(Variable):
    value_type = float
    entity = Individu
    label = u"Taux ARRCO tranche A employeur) propre à l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class arrco_tranche_a_taux_salarie(Variable):
    value_type = float
    entity = Individu
    label = u"Taux ARRCO tranche A salarié) propre à l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class assujettie_taxe_salaires(Variable):
    value_type = bool
    entity = Individu
    label = u"Entreprise assujettie à la taxe sur les salaires"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class avantage_en_nature_valeur_reelle(Variable):
    value_type = float
    entity = Individu
    label = u"Avantages en nature (Valeur réelle)"
    definition_period = MONTH


class indemnites_compensatrices_conges_payes(Variable):
    value_type = float
    entity = Individu
    label = u"indemnites_compensatrices_conges_payes"
    definition_period = MONTH


class indemnite_fin_contrat_due(Variable):
    value_type = bool
    entity = Individu
    label = u"indemnite_fin_contrat_due"
    definition_period = MONTH


class contrat_de_travail(Variable):
    value_type = Enum
    possible_values = TypesContratDeTravail  # defined in model/base.py
    default_value = TypesContratDeTravail.temps_plein
    entity = Individu
    label = u"Type contrat de travail"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_debut(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = u"Date d'arrivée dans l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_fin(Variable):
    value_type = date
    default_value = date(2099, 12, 31)
    entity = Individu
    label = u"Date de départ de l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_duree(Variable):
    value_type = Enum
    possible_values = TypesContratDeTravailDuree  # defined in model/base.py
    default_value = TypesContratDeTravailDuree.cdi
    entity = Individu
    label = u"Type (durée determinée ou indéterminée) du contrat de travail"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period



class cotisation_sociale_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesCotisationSocialeModeRecouvrement   # defined in model/base.py
    default_value = TypesCotisationSocialeModeRecouvrement.mensuel
    entity = Individu
    label = u"Mode de recouvrement des cotisations sociales"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class entreprise_est_association_non_lucrative(Variable):
    value_type = bool
    entity = Individu
    label = u"L'entreprise est une association à but non lucratif, par exemple loi de 1901"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class depcom_entreprise(Variable):
    value_type = str
    max_length = 5
    entity = Individu
    label = u"Localisation entreprise (depcom)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class code_postal_entreprise(Variable):
    value_type = str
    max_length = 5
    entity = Individu
    label = u"Localisation entreprise (Code postal)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class salarie_regime_alsace_moselle(Variable):
    entity = Individu
    value_type = bool
    label = u"Le salarié cotise au régime de l'Alsace-Moselle"
    definition_period = MONTH
    # Attention : ce n'est pas équivalent au fait de travailler en Alsace-Moselle !
    # http://regime-local.fr/salaries/


class effectif_entreprise(Variable):
    entity = Individu
    value_type = int
    base_function = requested_period_last_value
    label = u"Effectif de l'entreprise"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class entreprise_assujettie_cet(Variable):
    value_type = bool
    entity = Individu
    label = u"Entreprise assujettie à la contribution économique territoriale"
    definition_period = MONTH


class entreprise_assujettie_is(Variable):
    value_type = bool
    entity = Individu
    label = u"Entreprise assujettie à l'impôt sur les sociétés (IS)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class entreprise_benefice(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Bénéfice de l'entreprise"
    definition_period = MONTH
    calculate_output = calculate_output_add


class entreprise_bilan(Variable):
    value_type = float
    entity = Individu
    label = u"Bilan de l'entreprise"
    definition_period = MONTH


class entreprise_chiffre_affaire(Variable):
    value_type = float
    entity = Individu
    label = u"Chiffre d'affaire de l'entreprise"
    definition_period = MONTH


class entreprise_creation(Variable):
    value_type = date
    entity = Individu
    label = u"Date de création de l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nombre_tickets_restaurant(Variable):
    value_type = int
    entity = Individu
    base_function = requested_period_last_value
    label = u"Nombre de tickets restaurant"
    definition_period = MONTH


class nouvelle_bonification_indiciaire(Variable):
    value_type = float
    entity = Individu
    label = u"Nouvelle bonification indicaire"
    definition_period = MONTH


class prevoyance_obligatoire_cadre_taux_employe(Variable):
    value_type = float
    default_value = 0.015  # 1.5% est le minimum en 2014
    entity = Individu
    base_function = requested_period_last_value
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres"
    definition_period = MONTH


class prevoyance_obligatoire_cadre_taux_employeur(Variable):
    value_type = float
    default_value = 0.015  # 1.5% est le minimum en 2014
    entity = Individu
    base_function = requested_period_last_value
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres"
    definition_period = MONTH


class primes_salaires(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités, primes et avantages en argent (brut)"
    definition_period = MONTH


class complementaire_sante_montant(Variable):
    value_type = float
    entity = Individu
    label = u"Montant de la complémentaire santé obligatoire retenue par l'employeur"
    definition_period = MONTH


class complementaire_sante_taux_employeur(Variable):
    value_type = float
    default_value = 0.5
    # La part minimum légale est de 50 %
    entity = Individu
    label = u"Part de la complémentaire santé obligatoire payée par l'employeur"
    definition_period = MONTH


class prise_en_charge_employeur_prevoyance_complementaire(Variable):
    value_type = float
    entity = Individu
    label = u"Part salariale des cotisations de prévoyance complémentaire prise en charge par l'employeur"
    definition_period = MONTH


class prise_en_charge_employeur_retraite_complementaire(Variable):
    value_type = float
    entity = Individu
    label = u"Part salariale des cotisations de retraite complémentaire prise en charge par l'employeur"
    definition_period = MONTH


class prise_en_charge_employeur_retraite_supplementaire(Variable):
    value_type = float
    entity = Individu
    label = u"Part salariale des cotisations de retraite supplémentaire prise en charge par l'employeur"
    definition_period = MONTH


class ratio_alternants(Variable):
    value_type = float
    entity = Individu
    label = u"Ratio d'alternants dans l'effectif moyen"
    definition_period = MONTH


class remboursement_transport_base(Variable):
    value_type = float
    entity = Individu
    label = u"Base pour le calcul du remboursement des frais de transport"
    definition_period = MONTH


class indemnites_forfaitaires(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités forfaitaires (transport, nourriture)"
    definition_period = MONTH


class salaire_de_base(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire de base, en général appelé salaire brut, la 1ère ligne sur la fiche de paie"
    set_input = set_input_divide_by_period
    reference = u'http://www.insee.fr/fr/methodes/default.asp?page=definitions/salaire-mensuel-base-smb.htm'
    definition_period = MONTH


class titre_restaurant_taux_employeur(Variable):
    value_type = float
    default_value = 0.5
    entity = Individu
    label = u"Taux de participation de l'employeur au titre restaurant"
    definition_period = MONTH


class titre_restaurant_valeur_unitaire(Variable):
    value_type = float
    entity = Individu
    label = u"Valeur faciale unitaire du titre restaurant"
    definition_period = MONTH


class titre_restaurant_volume(Variable):
    value_type = int
    entity = Individu
    label = u"Volume des titres restaurant"
    definition_period = MONTH


class traitement_indiciaire_brut(Variable):
    value_type = float
    entity = Individu
    label = u"Traitement indiciaire brut (TIB)"
    definition_period = MONTH


class categorie_salarie(Variable):
    value_type = Enum
    possible_values = TypesCategorieSalarie  # defined in model/base.py
    default_value = TypesCategorieSalarie.prive_non_cadre
    entity = Individu
    label = u"Catégorie de salarié"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class heures_duree_collective_entreprise(Variable):
    value_type = int  # TODO default la valeur de la durée légale ?
    entity = Individu
    label = u"Durée mensuelle collective dans l'entreprise (heures, temps plein)"
    definition_period = MONTH


class heures_non_remunerees_volume(Variable):
    value_type = float
    entity = Individu
    label = u"Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)"
    set_input = set_input_divide_by_period
    definition_period = MONTH


class heures_remunerees_volume(Variable):
    value_type = float
    entity = Individu
    label = u"Volume des heures rémunérées contractuellement (heures/mois, temps partiel)"
    set_input = set_input_divide_by_period
    definition_period = MONTH


class forfait_heures_remunerees_volume(Variable):
    value_type = int
    entity = Individu
    label = u"Volume des heures rémunérées à un forfait heures"
    definition_period = MONTH


class forfait_jours_remuneres_volume(Variable):
    value_type = int
    entity = Individu
    label = u"Volume des heures rémunérées à forfait jours"
    definition_period = MONTH


class volume_jours_ijss(Variable):
    value_type = int
    entity = Individu
    label = u"Volume des jours pour lesquels sont versés une idemnité journalière par la sécurité sociale"
    definition_period = MONTH


class avantage_en_nature(Variable):
    value_type = float
    entity = Individu
    label = u"Avantages en nature"
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)
        avantage_en_nature_valeur_forfaitaire = simulation.calculate('avantage_en_nature_valeur_forfaitaire', period)

        return avantage_en_nature_valeur_reelle + avantage_en_nature_valeur_forfaitaire


class avantage_en_nature_valeur_forfaitaire(Variable):
    value_type = float
    entity = Individu
    label = u"Evaluation fofaitaire des avantages en nature "
    definition_period = MONTH

    # TODO: complete this function
    def formula(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)

        return avantage_en_nature_valeur_reelle * 0


class depense_cantine_titre_restaurant_employe(Variable):
    value_type = float
    entity = Individu
    label = u"Dépense de cantine et de titre restaurant à charge de l'employe"
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period

        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return - valeur_unitaire * volume * (1 - taux_employeur)


class depense_cantine_titre_restaurant_employeur(Variable):
    value_type = float
    entity = Individu
    label = u"Dépense de cantine et de titre restaurant à charge de l'employeur"
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period
        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)  # Compute with jours ouvrables ?
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return valeur_unitaire * volume * taux_employeur


class nombre_jours_calendaires(Variable):
    value_type = float
    entity = Individu
    label = u"Nombre de jours calendaires travaillés"
    definition_period = MONTH
    default_value = 30

    def formula(self, simulation, period):
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)

        busday_count = partial(original_busday_count, weekmask = "1" * 7)
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month'))
        jours_travailles = max_(
            busday_count(
                max_(contrat_de_travail_debut, debut_mois),
                min_(contrat_de_travail_fin, fin_mois) + timedelta64(1, 'D')
                ),
            0,
            )

        return jours_travailles


class remboursement_transport(Variable):
    value_type = float
    entity = Individu
    label = u"Remboursement partiel des frais de transport par l'employeur"
    definition_period = MONTH

    def formula(self, simulation, period):

        remboursement_transport_base = simulation.calculate('remboursement_transport_base', period)
        # TODO: paramètres en dur dans le code
        return - .5 * remboursement_transport_base


# Fonction publique

class gipa(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnité de garantie individuelle du pouvoir d'achat"
    definition_period = MONTH
    # TODO: à coder

    def formula(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        return self.zeros()


class indemnite_residence(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnité de résidence des fonctionnaires"
    definition_period = MONTH

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        salaire_de_base = individu('salaire_de_base', period)
        categorie_salarie = individu('categorie_salarie', period)
        zone_apl = individu.menage('zone_apl', period)
        _P = parameters(period)

        P = _P.fonc.indem_resid
        min_zone_1, min_zone_2, min_zone_3 = P.min * P.taux.zone1, P.min * P.taux.zone2, P.min * P.taux.zone3
        taux = P.taux.zone1 * (zone_apl == TypesZoneApl.zone_1) + P.taux.zone2 * (zone_apl == TypesZoneApl.zone_2) + P.taux.zone3 * (zone_apl == TypesZoneApl.zone_3)
        plancher = min_zone_1 * (zone_apl == TypesZoneApl.zone_1) + min_zone_2 * (zone_apl == TypesZoneApl.zone_2) + min_zone_3 * (zone_apl == TypesZoneApl.zone_3)
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            + (categorie_salarie == TypesCategorieSalarie.non_pertinent)
        )
        return max_(
            plancher,
            taux * (traitement_indiciaire_brut + salaire_de_base)
            ) * public


class indice_majore(Variable):
    value_type = float
    entity = Individu
    label = u"Indice majoré"
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        _P = simulation.parameters_at(period.start)

        traitement_annuel_brut = _P.fonc.IM_100
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            + (categorie_salarie == TypesCategorieSalarie.non_pertinent)
        )

        return (traitement_indiciaire_brut * 100 * 12 / traitement_annuel_brut) * public


class primes_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = u"Calcul des primes pour les fonctionnaries"
    reference = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml"
    definition_period = MONTH

    def formula(self, simulation, period):
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat) +
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) +
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        return TAUX_DE_PRIME * traitement_indiciaire_brut * public


class af_nbenf_fonc(Variable):
    value_type = int
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales pour les fonctionnaires"
    entity = Famille
    definition_period = MONTH

    def formula(self, simulation, period):
        """
            Cette variable est une version légèrement modifiée de `af_nbenf`. Elle se base sur le salaire de base, tandis que `af_nbenf` se base sur le salaire net.
            On ne peut pas utiliser la variable `af_nbenf` dans le calcul de `supp_familial_traitement` (ci-dessous) car `af_nbenf` dépend du `salaire_net`, et `salaire_net` dépends de `supp_familial_traitement`. Cela créerait une boucle infinie.
            D'où l'introduction de cette variable alternative.
        """
        salaire_de_base_mensualise = simulation.calculate_add('salaire_de_base', period.start.period('month', 6).offset(-6)) / 6
        law = simulation.parameters_at(period.start)
        nbh_travaillees = 169
        smic_mensuel_brut = law.cotsoc.gen.smic_h_b * nbh_travaillees
        autonomie_financiere = (
            salaire_de_base_mensualise >=
            (law.prestations.prestations_familiales.af.seuil_rev_taux * smic_mensuel_brut)
            )
        age = simulation.calculate('age', period)
        condition_enfant = (
            (age >= law.prestations.prestations_familiales.af.age1) *
            (age <= law.prestations.prestations_familiales.af.age2) *
            not_(autonomie_financiere)
            )
        return simulation.famille.sum(condition_enfant, role = Famille.ENFANT)


class supp_familial_traitement(Variable):
    value_type = float
    entity = Individu
    label = u"Supplément familial de traitement"
    definition_period = MONTH
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def formula(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        _P = parameters(period)

        fonc_nbenf = individu.famille('af_nbenf_fonc', period) * individu.has_role(Famille.DEMANDEUR)

        P = _P.fonc.supp_fam
        part_fixe_1 = P.fixe.enf1
        part_fixe_2 = P.fixe.enf2
        part_fixe_supp = P.fixe.enfsupp
        part_fixe = (
            part_fixe_1 * (fonc_nbenf == 1) + part_fixe_2 * (fonc_nbenf == 2) +
            part_fixe_supp * max_(0, fonc_nbenf - 2)
            )
        # pct_variable_1 = 0
        pct_variable_2 = P.prop.enf2
        pct_variable_3 = P.prop.enf3
        pct_variable_supp = P.prop.enfsupp
        pct_variable = (
            pct_variable_2 * (fonc_nbenf == 2) + (pct_variable_3) * (fonc_nbenf == 3) +
            pct_variable_supp * max_(0, fonc_nbenf - 3))

        indice_maj_min = P.IM_min
        indice_maj_max = P.IM_max

        traitement_brut_mensuel_min = _traitement_brut_mensuel(indice_maj_min, _P)
        plancher_mensuel_1 = part_fixe
        plancher_mensuel_2 = part_fixe + traitement_brut_mensuel_min * pct_variable_2
        plancher_mensuel_3 = part_fixe + traitement_brut_mensuel_min * pct_variable_3
        plancher_mensuel_supp = traitement_brut_mensuel_min * pct_variable_supp

        plancher = (plancher_mensuel_1 * (fonc_nbenf == 1) +
                    plancher_mensuel_2 * (fonc_nbenf == 2) +
                    plancher_mensuel_3 * (fonc_nbenf >= 3) +
                    plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

        traitement_brut_mensuel_max = _traitement_brut_mensuel(indice_maj_max, _P)
        plafond_mensuel_1 = part_fixe
        plafond_mensuel_2 = part_fixe + traitement_brut_mensuel_max * pct_variable_2
        plafond_mensuel_3 = part_fixe + traitement_brut_mensuel_max * pct_variable_3
        plafond_mensuel_supp = traitement_brut_mensuel_max * pct_variable_supp

        plafond = (plafond_mensuel_1 * (fonc_nbenf == 1) + plafond_mensuel_2 * (fonc_nbenf == 2) +
                   plafond_mensuel_3 * (fonc_nbenf == 3) +
                   plafond_mensuel_supp * max_(0, fonc_nbenf - 3))
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )
        sft = public * min_(
            max_(part_fixe + pct_variable * traitement_indiciaire_brut, plancher),
            plafond
            )
        # Nota Bene:
        # categorie_salarie is an enum :
        # class TypesCategorieSalarie(Enum):
        #   prive_non_cadre = u'prive_non_cadre'
        #   prive_cadre = u'prive_cadre'
        #   public_titulaire_etat = u'public_titulaire_etat'
        #   public_titulaire_militaire = u'public_titulaire_militaire'
        #   public_titulaire_territoriale = u'public_titulaire_territoriale'
        #   public_titulaire_hospitaliere = u'public_titulaire_hospitaliere'
        #   public_non_titulaire = u'public_non_titulaire'
        #   non_pertinent = u'non_pertinent'
        return sft


def _traitement_brut_mensuel(indice_maj, law):
    Indice_majore_100_annuel = law.fonc.IM_100
    traitement_brut = Indice_majore_100_annuel * indice_maj / 100 / 12
    return traitement_brut


class remuneration_principale(Variable):
    value_type = float
    entity = Individu
    label = u"Rémunération principale des agents titulaires de la fonction publique"
    definition_period = MONTH

    def formula(self, simulation, period):
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = simulation.calculate('nouvelle_bonification_indiciaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        return (
            public * (
                traitement_indiciaire_brut + nouvelle_bonification_indiciaire
                )
            )


class salaire_net_a_payer(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire net à payer (fiche de paie)"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(self, simulation, period):
        '''
        Calcul du salaire net à payer après déduction des sommes
        dues par les salarié avancées par l'employeur
        '''
        salaire_net = simulation.calculate_add('salaire_net', period)
        depense_cantine_titre_restaurant_employe = simulation.calculate(
            'depense_cantine_titre_restaurant_employe', period)
        indemnites_forfaitaires = simulation.calculate('indemnites_forfaitaires', period)
        remuneration_apprenti = simulation.calculate('remuneration_apprenti', period)
        stage_gratification = simulation.calculate('stage_gratification', period)
        salaire_net_a_payer = (
            salaire_net +
            remuneration_apprenti +
            stage_gratification +
            depense_cantine_titre_restaurant_employe +
            indemnites_forfaitaires
            )
        return salaire_net_a_payer


class salaire_super_brut_hors_allegements(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire super-brut (fiche de paie): rémunération + cotisations sociales employeur"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        remuneration_apprenti = simulation.calculate('remuneration_apprenti', period)

        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        cotisations_employeur = simulation.calculate('cotisations_employeur', period)
        depense_cantine_titre_restaurant_employeur = simulation.calculate(
            'depense_cantine_titre_restaurant_employeur', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            'reintegration_titre_restaurant_employeur', period)
        indemnite_fin_contrat = simulation.calculate('indemnite_fin_contrat', period)
        salaire_super_brut_hors_allegements = (
            salaire_de_base + remuneration_principale + remuneration_apprenti +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement + indemnite_fin_contrat +
            depense_cantine_titre_restaurant_employeur - reintegration_titre_restaurant_employeur -
            cotisations_employeur
            )

        return salaire_super_brut_hors_allegements


class salaire_super_brut(Variable):
    value_type = float
    entity = Individu
    label = u"Coût du travail à court terme. Inclut les exonérations et allègements de charges"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(self, simulation, period):
        period = period
        salaire_super_brut_hors_allegements = simulation.calculate('salaire_super_brut_hors_allegements', period)
        exonerations_et_allegements = simulation.calculate('exonerations_et_allegements', period)

        return salaire_super_brut_hors_allegements - exonerations_et_allegements


class exonerations_et_allegements(Variable):
    value_type = float
    entity = Individu
    label = u"Charges, aides et crédits différées ou particulières"
    definition_period = MONTH

    def formula(self, simulation, period):
        exoneration_cotisations_employeur_apprenti = simulation.calculate_add(
            'exoneration_cotisations_employeur_apprenti', period)
        exoneration_cotisations_employeur_geographiques = simulation.calculate(
            'exoneration_cotisations_employeur_geographiques', period)
        exoneration_cotisations_employeur_jei = simulation.calculate_add(
            'exoneration_cotisations_employeur_jei', period)
        exoneration_cotisations_employeur_stagiaire = simulation.calculate_add(
            'exoneration_cotisations_employeur_stagiaire', period)

        allegement_fillon = simulation.calculate_add('allegement_fillon', period)
        allegement_cot_alloc_fam = simulation.calculate_add('allegement_cotisation_allocations_familiales', period)

        return (
            allegement_fillon +
            allegement_cot_alloc_fam +
            exoneration_cotisations_employeur_geographiques +
            exoneration_cotisations_employeur_jei +
            exoneration_cotisations_employeur_apprenti +
            exoneration_cotisations_employeur_stagiaire
            )


class cout_du_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Coût du travail à long terme. Inclut les charges, aides et crédits différés"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula(self, simulation, period):
        salaire_super_brut = simulation.calculate('salaire_super_brut', period)
        cout_differe = simulation.calculate('cout_differe', period)

        return salaire_super_brut - cout_differe


class cout_differe(Variable):
    value_type = float
    entity = Individu
    label = u"Charges, aides et crédits différées ou particulières"
    definition_period = MONTH

    def formula(self, simulation, period):
        credit_impot_competitivite_emploi = simulation.calculate_add('credit_impot_competitivite_emploi', period)
        aide_premier_salarie = simulation.calculate_add('aide_premier_salarie', period)
        aide_embauche_pme = simulation.calculate_add('aide_embauche_pme', period)
        tehr = simulation.calculate_divide('tehr', period)

        return credit_impot_competitivite_emploi + aide_premier_salarie + aide_embauche_pme + tehr
