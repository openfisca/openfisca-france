from functools import partial
from numpy import busday_count as original_busday_count, datetime64, timedelta64, where
from openfisca_france.model.base import *


class indemnites_stage(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités de stage'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class revenus_stage_formation_pro(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus de stage de formation professionnelle'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class bourse_recherche(Variable):
    value_type = float
    entity = Individu
    label = 'Bourse de recherche'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class sal_pen_exo_etr(Variable):
    cerfa_field = {
        0: '1AC',
        1: '1BC',
        2: '1CC',
        3: '1DC',
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif'
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class frais_reels(Variable):
    cerfa_field = {
        0: '1AK',
        1: '1BK',
        2: '1CK',
        3: '1DK',
        4: '1EK',
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Frais réels'
    definition_period = YEAR


class hsup(Variable):
    cerfa_field = {
        0: '1AU',
        1: '1BU',
        2: '1CU',
        3: '1DU',
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Heures supplémentaires : revenus exonérés connus'
    # start_date = date(2007, 1, 1)
    end = '2013-12-13'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class ppe_du_sa(Variable):
    cerfa_field = {
        0: '1AV',
        1: '1BV',
        2: '1CV',
        3: '1DV',
        4: '1QV',
        }
    value_type = int
    entity = Individu
    label = "Prime pour l'emploi des salariés: nombre d'heures payées"
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
        0: '1AX',
        1: '1BX',
        2: '1CX',
        3: '1DX',
        4: '1QX',
        }
    value_type = bool
    entity = Individu
    label = "Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière"
    definition_period = YEAR

    def formula(individu, period):
        mois = period.first_month
        indicateur = individu('contrat_de_travail', mois) == 0
        # On parcours tous les mois de l'année pour s'assurer que l'individu était employé à temps plein
        # durant toute l'année.
        while mois.start.month < 12:
            mois = mois.offset(1)
            indicateur = indicateur & (individu('contrat_de_travail', mois) == 0)
        return indicateur


class TypesExpositionAccident(Enum):
    __order__ = 'faible moyen eleve tres_eleve'  # Needed to preserve the enum order in Python 2
    faible = 'Faible'
    moyen = 'Moyen'
    eleve = 'Élevé'
    tres_eleve = 'Très élevé'


class exposition_accident(Variable):
    value_type = Enum
    possible_values = TypesExpositionAccident
    default_value = TypesExpositionAccident.faible
    entity = Individu
    label = 'Exposition au risque pour les accidents du travail'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesExpositionPenibilite(Enum):
    __order__ = 'nulle simple multiple'  # Needed to preserve the enum order in Python 2
    nulle = "Nulle, pas d'exposition de l'employé à un facteur de pénibilité"
    simple = 'Simple, exposition à un seul facteur de pénibilité'
    multiple = 'Multiple, exposition à plusieurs facteurs de pénibilité'


class exposition_penibilite(Variable):
    value_type = Enum
    possible_values = TypesExpositionPenibilite
    default_value = TypesExpositionPenibilite.nulle
    entity = Individu
    label = 'Exposition à un ou plusieurs facteurs de pénibilité'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesAllegementModeRecouvrement(Enum):
    # Informations sur la régularisation de la réduction appliquée sur le site des URSSAF : https://www.urssaf.fr/portail/home/employeur/beneficier-dune-exoneration/exonerations-generales/la-reduction-generale/le-calcul-de-la-reduction/etape-2--le-calcul-de-la-reducti/la-regularisation.html
    __order__ = 'fin_d_annee anticipe progressif'  # Needed to preserve the enum order in Python 2
    fin_d_annee = "Paiement en fin d'année des cotisations avec l'allègement exact"
    anticipe = "Paiement anticipé des cotisations et régularisation de l'allègement en fin de période"
    progressif = "Paiement anticipé des cotisations et régularisation progressive de l'allègement"  # La régularisation est faite à chaque paiement anticipé, «en faisant masse des éléments nécessaires au calcul de la réduction»


class allegement_fillon_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesAllegementModeRecouvrement
    default_value = TypesAllegementModeRecouvrement.fin_d_annee
    entity = Individu
    label = 'Mode de recouvrement des allègements Fillon'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class allegement_cotisation_allocations_familiales_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesAllegementModeRecouvrement
    default_value = TypesAllegementModeRecouvrement.fin_d_annee
    entity = Individu
    label = "Mode de recouvrement de l'allègement de la cotisation d'allocations familiales"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class allegement_cotisation_maladie_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesAllegementModeRecouvrement
    default_value = TypesAllegementModeRecouvrement.fin_d_annee
    entity = Individu
    label = "Mode de recouvrement de l'allègement des cotisations maladie sur les bas et moyens salaires (Ex-CICE)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class apprentissage_contrat_debut(Variable):
    value_type = date
    entity = Individu
    label = "Date de début du contrat d'apprentissage"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class arrco_tranche_a_taux_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Taux ARRCO tranche A employeur) propre à l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class arrco_tranche_a_taux_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Taux ARRCO tranche A salarié) propre à l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class assujettie_taxe_salaires(Variable):
    value_type = bool
    entity = Individu
    label = 'Entreprise assujettie à la taxe sur les salaires'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class avantage_en_nature_valeur_reelle(Variable):
    value_type = float
    entity = Individu
    label = 'Avantages en nature (Valeur réelle)'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_compensatrices_conges_payes(Variable):
    value_type = float
    entity = Individu
    label = 'indemnites_compensatrices_conges_payes'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnite_fin_contrat_due(Variable):
    value_type = bool
    entity = Individu
    label = 'indemnite_fin_contrat_due'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class TypesContratDeTravail(Enum):
    __order__ = 'temps_plein temps_partiel forfait_heures_semaines forfait_heures_mois forfait_heures_annee forfait_jours_annee sans_objet'  # Needed to preserve the enum order in Python 2
    temps_plein = 'Temps plein'
    temps_partiel = 'Temps partiel'
    forfait_heures_semaines = 'Convention de forfait heures sur la semaine'
    forfait_heures_mois = 'Convention de forfait heures sur le mois'
    forfait_heures_annee = 'Convention de forfait heures sur l’année'
    forfait_jours_annee = 'Convention de forfait hours sur l’année'
    sans_objet = 'Non renseigné'


class contrat_de_travail(Variable):
    value_type = Enum
    possible_values = TypesContratDeTravail
    default_value = TypesContratDeTravail.temps_plein
    entity = Individu
    label = 'Type de contrat de travail'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class date_debut_recherche_emploi(Variable):
    value_type = date
    default_value = date(1, 1, 1)
    entity = Individu
    label = "Date de début d'une activité en recherche d'emploi selon Pôle Emploi (exemple : entretien d'embauche, concours public, examen certifiant)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_debut(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date d'arrivée dans l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_fin(Variable):
    value_type = date
    default_value = date(2099, 12, 31)
    entity = Individu
    label = "Date de départ de l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesContrat(Enum):
    __order__ = 'aucun cdi cdd ctt formation'  # Needed to preserve the enum order in Python 2
    aucun = 'Aucun contrat'
    cdi = 'Contrat de travail à durée indéterminée (CDI)'
    cdd = 'Contrat de travail à durée déterminée (CDD)'
    ctt = 'Contrat de travail temporaire (CTT)'
    formation = 'Formation'


class contrat_de_travail_type(Variable):
    value_type = Enum
    possible_values = TypesContrat
    default_value = TypesContrat.cdi
    entity = Individu
    label = 'Type du contrat de travail'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_aide(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est en contrat aidé"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://dares.travail-emploi.gouv.fr/definitions-et-concepts/contrats-aides'


class duree_formation(Variable):
    value_type = float
    entity = Individu
    label = 'Durée de la formation en heures'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class TypesLieuEmploiFormation(Enum):
    non_renseigne = 'Non renseigné'
    metropole_hors_corse = 'Métropole hors Corse'
    corse = 'Corse'
    guadeloupe = 'Guadeloupe'
    martinique = 'Martinique'
    guyane = 'Guyane'
    la_reunion = 'La réunion'
    saint_pierre_et_miquelon = 'Saint Pierre et Miquelon'
    mayotte = 'Mayotte'
    saint_bartelemy = 'Saint Bartelemy'
    saint_martin = 'Saint Martin'


class lieu_emploi_ou_formation(Variable):
    value_type = Enum
    possible_values = TypesLieuEmploiFormation
    default_value = TypesLieuEmploiFormation.non_renseigne
    entity = Individu
    label = "Zone de l'emploi ou de la formation"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class contrat_de_travail_duree(Variable):
    value_type = float
    default_value = 0.
    entity = Individu
    label = 'Durée du contrat de travail en mois'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesCategoriesDemandeurEmploi(Enum):
    # http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobre-2016-bope-n2016-80.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201
    # https://allocation-chomage.fr/categorie-chomeur/

    __order__ = 'pas_de_categorie categorie_1 categorie_2 categorie_3 categorie_4 categorie_5 categorie_6 categorie_7 categorie_8'\
                # Needed to preserve the enum order in Python 2

    pas_de_categorie = 'Aucune catégorie'
    categorie_1 = 'Catégorie 1 - Personnes sans emploi, immédiatement disponibles en recherche de CDI plein temps.'
    categorie_2 = 'Catégorie 2 - Personnes sans emploi, immédiatement disponibles en recherche de CDI à temps partiel.'
    categorie_3 = 'Catégorie 3 - Personnes sans emploi, immédiatement disponibles en recherche de CDD.'
    categorie_4 = 'Catégorie 4 - Personnes sans emploi, non immédiatement disponibles et à la recherche d’un emploi.'
    categorie_5 = "Catégorie 5 - Personnes non immédiatement disponibles, parce que titulaires d'un ou de plusieurs emplois, et à la recherche d'un autre emploi."
    categorie_6 = "Catégorie 6 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à plein temps."
    categorie_7 = "Catégorie 7 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à temps partiel."
    categorie_8 = "Catégorie 8 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDD."


class pole_emploi_categorie_demandeur_emploi(Variable):
    reference = [
        'http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobre-2016-bope-n2016-80.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201',
        'Annexe 3 : la fiche 3 - Les effets de l’inscription'
        ]
    value_type = Enum
    possible_values = TypesCategoriesDemandeurEmploi
    default_value = TypesCategoriesDemandeurEmploi.pas_de_categorie
    entity = Individu
    label = 'Le classement des demandeurs d’emploi dans les différentes catégories d’inscription à Pôle Emploi'
    definition_period = MONTH


class TypesCotisationSocialeModeRecouvrement(Enum):
    __order__ = 'mensuel annuel mensuel_strict'  # Needed to preserve the enum order in Python 2
    mensuel = "Mensuel avec régularisation en fin d'année"
    annuel = 'Annuel'
    mensuel_strict = 'Mensuel strict'


class cotisation_sociale_mode_recouvrement(Variable):
    value_type = Enum
    possible_values = TypesCotisationSocialeModeRecouvrement
    default_value = TypesCotisationSocialeModeRecouvrement.mensuel_strict
    entity = Individu
    label = 'Mode de recouvrement des cotisations sociales'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class entreprise_est_association_non_lucrative(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est une association à but non lucratif, par exemple loi de 1901"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class depcom_entreprise(Variable):
    value_type = str
    max_length = 5
    entity = Individu
    label = 'Localisation entreprise (depcom)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class code_postal_entreprise(Variable):
    value_type = str
    max_length = 5
    entity = Individu
    label = 'Localisation entreprise (Code postal)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class salarie_regime_alsace_moselle(Variable):
    entity = Individu
    value_type = bool
    label = "Le salarié cotise au régime de l'Alsace-Moselle"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # Attention : ce n'est pas équivalent au fait de travailler en Alsace-Moselle !
    # http://regime-local.fr/salaries/


class effectif_entreprise(Variable):
    entity = Individu
    value_type = int
    label = "Effectif de l'entreprise"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class entreprise_assujettie_cet(Variable):
    value_type = bool
    entity = Individu
    label = 'Entreprise assujettie à la contribution économique territoriale'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class entreprise_assujettie_is(Variable):
    value_type = bool
    entity = Individu
    label = "Entreprise assujettie à l'impôt sur les sociétés (IS)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class entreprise_benefice(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Bénéfice de l'entreprise"
    definition_period = MONTH
    calculate_output = calculate_output_add


class entreprise_bilan(Variable):
    value_type = float
    entity = Individu
    label = "Bilan de l'entreprise"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class entreprise_chiffre_affaire(Variable):
    value_type = float
    entity = Individu
    label = "Chiffre d'affaire de l'entreprise"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class entreprise_creation(Variable):
    value_type = date
    entity = Individu
    label = "Date de création de l'entreprise"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nombre_tickets_restaurant(Variable):
    value_type = int
    entity = Individu
    label = 'Nombre de tickets restaurant'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class nouvelle_bonification_indiciaire(Variable):
    value_type = float
    entity = Individu
    label = 'Nouvelle bonification indicaire'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prevoyance_obligatoire_cadre_taux_employe(Variable):
    value_type = float
    default_value = 0.015  # 1.5% est le minimum en 2014
    entity = Individu
    label = 'Taux de cotisation employeur pour la prévoyance obligatoire des cadres'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class prevoyance_obligatoire_cadre_taux_employeur(Variable):
    value_type = float
    default_value = 0.015  # 1.5% est le minimum en 2014
    entity = Individu
    label = 'Taux de cotisation employeur pour la prévoyance obligatoire des cadres'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class primes_salaires(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités, primes et avantages en argent (brut)'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prime_partage_valeur(Variable):
    value_type = float
    entity = Individu
    label = 'Prime pérenne de partage de la valeur (PPV)'
    definition_period = (YEAR)  # La PPV est versée en fonction du salaire des 12 derniers mois
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046188457/2022-08-18'
    set_input = set_input_divide_by_period
    documentation = '''
        La PPV exonérée représente l'éxonération de la prime des cotisations salariales,
        patronales et l'impôt sur le revenu. La PPV prévoit l'absence de substitution et
        donc le caractère « fantôme » de la prime au regard des ressources des
        administrations publiques et singulièrement de la sécurité sociale.

        la condition de rémunération est valable jusqu'au 31 décembre 2023.
        Alors, lorsque la rémunération est inférieure à 3 SMIC, la PPV est **aussi**
        exonérée d'impôt sur le revenu, ainsi que des contributions prévues
        à l'article L. 136-1 du code de la sécurité sociale
        [CSG activité = https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033712581]
        et à l'article 14 de l'ordonnance n° 96-50 du 24 janvier 1996 relative au remboursement
        de la dette sociale (⑯).
        [CRDS = https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000038834962/]
        Néanmoins, elle est incluse dans le revenu fiscal de référence (⑰).
        => Sous 3 SMIC les 12 derniers mois, on est en plus exonéré d'IR, CSG et CRDS.

        Pour tout niveau de revenu :
        PPV est exonérée, dans la limite de 3 000 euros :
        * de toutes les cotisations sociales d'origine légale ou conventionnelle à la charge du salarié et de l'employeur,
        ainsi que des participations, taxes et contributions prévues :
        * à l'article 235 bis du code général des impôts
        [PEEC applicable au-dessus de 50 salariés = https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038586341/]
        * et à l'article L. 6131-1 du code du travail,
        [
            contribution unique à la formation professionnelle (CFP ?),
            la contribution supplémentaire,
            contribution dédiée au financement du compte personnel de formation
            = article L. 6131-1 du code du travail
            ]
        dans leur rédaction en vigueur à la date de son versement.
        '''


class prime_partage_valeur_exceptionnelle(Variable):
    value_type = float
    entity = Individu
    label = 'Prime exceptionnelle de partage de la valeur (PPV)'
    definition_period = (YEAR)  # La PPV est versée en fonction du salaire des 12 derniers mois
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046188457/2022-08-18'
    set_input = set_input_divide_by_period


class prime_partage_valeur_exoneree_exceptionnelle(Variable):
    value_type = float
    entity = Individu
    label = 'Prime exceptionnelle de partage de la valeur (PPV), partie exonérée'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046188457/2022-08-18'

    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        '''
        La prime exceptionnelle de partage de la valeur (PPV),
        est réservée aux salariés qui ont un salaire de base inférieur à 3 x SMIC.
        Elle ne peut plus être versée après le 31 décembre 2023.
        '''

        prime_partage_valeur = individu('prime_partage_valeur_exceptionnelle', period)
        accord_interessement = individu('accord_interessement', period.first_month)
        ppv_parameters = parameters(period).marche_travail.primes_exceptionnelles.prime_partage_valeur
        plafond_ppv_exoneree = where(
            accord_interessement,
            ppv_parameters.plafond_exoneration_avec_accord_interessement,
            ppv_parameters.plafond_exoneration,
            )
        # Le plafond doit être diminué de la prime PEPA éventuellement versée début 2022
        prime_exceptionnelle_pouvoir_achat = individu('prime_exceptionnelle_pouvoir_achat', period)
        plafond_ppv_exoneree = plafond_ppv_exoneree - prime_exceptionnelle_pouvoir_achat
        ppv_eligibilite_exceptionnelle = individu('ppv_eligibilite_exceptionnelle', period)
        return (
            min_(prime_partage_valeur, plafond_ppv_exoneree)
            * ppv_eligibilite_exceptionnelle  # Neutralisation de la prime pour >= 3 x SMIC
            )


class prime_partage_valeur_non_exoneree_exceptionnelle(Variable):
    value_type = float
    entity = Individu
    label = 'Prime exceptionnelle de partage de la valeur (PPV), partie non exonérée'
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        prime_partage_valeur_exceptionnelle = individu('prime_partage_valeur_exceptionnelle', period)
        ppv_eligibilite_exceptionnelle = individu('ppv_eligibilite_exceptionnelle', period)
        prime_partage_valeur_exoneree_exceptionnelle = individu('prime_partage_valeur_exoneree_exceptionnelle', period)
        return (
            prime_partage_valeur_exceptionnelle
            - prime_partage_valeur_exoneree_exceptionnelle
            ) * ppv_eligibilite_exceptionnelle  # Neutralisation de la prime pour >= 3 x SMIC


class ppv_eligibilite_exceptionnelle(Variable):
    '''
    Cette variable sert à neutraliser la prime pour les personnes qui touchent plus que 3xSMIC
    Car dans ce cas il n'est pas autorisé de leur verser la prime exceptionnelle.
    L'employeur doit alors opter pour la prime temporaire/exceptionnelle.
    '''

    value_type = float
    entity = Individu
    label = 'Eligibilité aux exonérations complémentaires pour la PPV'
    definition_period = YEAR
    set_input = set_input_dispatch_by_period
    end = '2023-12-31'
    documentation = '''
    L'individu est éligible à des exonérations complémentaires
    sur la prime de partage de valeur (PPV) pour une rémunération
    inférieure à 3 SMIC : exonération de CSG, CRDS
    et impôt sur le revenu.
    '''

    def formula_2022_07_01(individu, period, parameters):
        annee_glissante = period.start.period('year').offset(-1)
        salaire_de_base_annuel = individu('salaire_de_base', annee_glissante, options=[ADD])
        smic_b_annuel = parameters(period).marche_travail.salaire_minimum.smic.smic_b_mensuel * 12
        quotite_de_travail = individu('quotite_de_travail', period, options=[ADD]) / 12
        plafond_salaire = parameters(period).marche_travail.primes_exceptionnelles.prime_partage_valeur.plafond_salaire
        return (salaire_de_base_annuel) < (
            smic_b_annuel * plafond_salaire * quotite_de_travail
            )


class prime_partage_valeur_exoneree(Variable):
    value_type = float
    entity = Individu
    label = 'Prime pérenne de partage de la valeur (PPV), partie exonérée'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046188457/2022-08-18'
    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        '''
        Il y a deux plafond suivant que l'employeur ait ou non :
        # * un dispositif d'intéressement,
        # * TODO : par un organisme d'intérêt général
        # * TODO : ou, s'agissant des primes versées aux travailleurs handicapés,
        #          par un établissement ou service d'aide par le travail
        '''

        prime_partage_valeur = individu('prime_partage_valeur', period)
        accord_interessement = individu('accord_interessement', period.first_month)

        ppv_parameters = parameters(period).marche_travail.primes_exceptionnelles.prime_partage_valeur
        plafond_ppv_exoneree = where(
            accord_interessement,
            ppv_parameters.plafond_exoneration_avec_accord_interessement,
            ppv_parameters.plafond_exoneration,
            )
        return min_(prime_partage_valeur, plafond_ppv_exoneree)


class prime_partage_valeur_non_exoneree(Variable):
    value_type = float
    entity = Individu
    label = 'Prime pérenne de partage de la valeur (PPV), partie non exonérée'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046188457/2022-08-18'
    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        prime_partage_valeur = individu('prime_partage_valeur', period)
        prime_partage_valeur_exoneree = individu(
            'prime_partage_valeur_exoneree', period
            )
        return prime_partage_valeur - prime_partage_valeur_exoneree


class prime_exceptionnelle_pouvoir_achat(Variable):
    value_type = float
    entity = Individu
    label = "Prime exceptionnelle de pouvoir d'achat (prime Macron)"
    definition_period = YEAR  # La pepa est versée en fonction du salaire des 12 derniers mois
    set_input = set_input_divide_by_period


class accord_interessement(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu travaille dans une entreprise couverte par un accord d'intéressement"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class prime_exceptionnelle_pouvoir_achat_exoneree(Variable):
    value_type = float
    entity = Individu
    label = "Prime exceptionnelle de pouvoir d'achat (prime Macron), partie exonérée"
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000043805912'
    #  La pepa exonérée représente l'éxonération de la prime des cotisations salariales, patronales et l’impôt sur le revenu. La pepa prévoit l'absence de substitution et donc le caractère « fantôme » de la prime au regard des ressources des administrations publiques et singulièrement de la sécurité sociale.
    set_input = set_input_divide_by_period
    end = '2022-03-31'

    def formula_2019_01_01(individu, period, parameters):
        '''
        Voici l'explication du dispositif :
        https://boss.gouv.fr/portail/accueil/mesures-exceptionnelles/instruction-du-19-aout-2021.html
        Prime exceptionnelle de pouvoir d'achat (prime Macron), voici comment j'ai écrit mon calcul :
        si salaire < 3 SMIC alors
            si prime pepa < 1000 alors
                exoneration = min (prime pepa, 1000)
            sinon (cas prime pepa >= 1000)
                si accord interessement ou effectif salarié < 50
                    alors exoneration= min (prime pepa,2000)
                sinon
                    exoneration = min (prime pepa, 1000)
        sinon
            Pas d'exonération
        '''
        annee_glissante = period.start.period('year').offset(-1)
        salaire_de_base_annuel = individu('salaire_de_base', annee_glissante, options=[ADD])
        smic_b_annuel = parameters(period).marche_travail.salaire_minimum.smic.smic_b_mensuel * 12
        quotite_de_travail = individu('quotite_de_travail', period, options=[ADD]) / 12
        plafond_salaire = parameters(period).marche_travail.primes_exceptionnelles.prime_pepa.plafond_salaire

        # "une rémunération inférieure à trois fois la valeur annuelle du salaire minimum de croissance
        # correspondant à la durée de travail prévue au contrat"
        condition_remuneration = (
            salaire_de_base_annuel
            ) < (
                smic_b_annuel * plafond_salaire * quotite_de_travail
                )

        prime_exceptionnelle_pouvoir_achat = individu(
            'prime_exceptionnelle_pouvoir_achat',
            period)

        plafond_exoneration = parameters(period).marche_travail.primes_exceptionnelles.prime_pepa.plafond_exoneration
        prime_inf_seuil_1 = prime_exceptionnelle_pouvoir_achat <= plafond_exoneration

        accord_interessement = individu('accord_interessement', period.first_month)
        effectif_entreprise = individu('effectif_entreprise', period.first_month)
        plafond_effectif_entreprise = parameters(period).marche_travail.primes_exceptionnelles.prime_pepa.plafond_effectif_entreprise
        condition_entreprise = accord_interessement + (effectif_entreprise < plafond_effectif_entreprise)
        plafond_exoneration_avec_accord_interessement = parameters(period).marche_travail.primes_exceptionnelles.prime_pepa.plafond_exoneration_avec_accord_interessement
        return (condition_remuneration
                * where(
                    prime_inf_seuil_1,
                    min_(prime_exceptionnelle_pouvoir_achat, plafond_exoneration),
                    where(
                        condition_entreprise,
                        min_(prime_exceptionnelle_pouvoir_achat, plafond_exoneration_avec_accord_interessement),
                        plafond_exoneration
                        )
                    )
                )


class prime_exceptionnelle_pouvoir_achat_non_exoneree(Variable):
    value_type = float
    entity = Individu
    label = "Prime exceptionnelle de pouvoir d'achat (prime Macron), partie non exonérée"
    definition_period = YEAR
    set_input = set_input_divide_by_period
    end = '2022-03-31'

    def formula_2019_01_01(individu, period, parameters):
        prime_exceptionnelle_pouvoir_achat = individu('prime_exceptionnelle_pouvoir_achat', period)
        prime_exceptionnelle_pouvoir_achat_exoneree =\
            individu('prime_exceptionnelle_pouvoir_achat_exoneree', period)
        return prime_exceptionnelle_pouvoir_achat - prime_exceptionnelle_pouvoir_achat_exoneree


class primes_salaires_non_exonerees(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités, primes et avantages en argent non exonérés (brut)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        primes_salaires = individu('primes_salaires', period)
        prime_partage_valeur_non_exoneree = individu('prime_partage_valeur_non_exoneree', period, options=[DIVIDE])
        prime_partage_valeur_non_exoneree_exceptionnelle = individu('prime_partage_valeur_non_exoneree_exceptionnelle', period, options=[DIVIDE])
        return (
            primes_salaires
            + prime_partage_valeur_non_exoneree
            + prime_partage_valeur_non_exoneree_exceptionnelle
            )

    def formula_2019_01_01(individu, period, parameters):
        primes_salaires = individu('primes_salaires', period)
        prime_exceptionnelle_pouvoir_achat_non_exoneree =\
            individu('prime_exceptionnelle_pouvoir_achat_non_exoneree', period, options = [DIVIDE])
        return primes_salaires + prime_exceptionnelle_pouvoir_achat_non_exoneree

    def formula(individu, period, parameters):
        primes_salaires = individu('primes_salaires', period)
        return primes_salaires


class complementaire_sante_montant(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la complémentaire santé obligatoire retenue par l'employeur"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class complementaire_sante_taux_employeur(Variable):
    value_type = float
    default_value = 0.5
    # La part minimum légale est de 50 %
    entity = Individu
    label = "Part de la complémentaire santé obligatoire payée par l'employeur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class prise_en_charge_employeur_prevoyance_complementaire(Variable):
    value_type = float
    entity = Individu
    label = "Part salariale des cotisations de prévoyance complémentaire prise en charge par l'employeur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class prise_en_charge_employeur_retraite_complementaire(Variable):
    value_type = float
    entity = Individu
    label = "Part salariale des cotisations de retraite complémentaire prise en charge par l'employeur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class prise_en_charge_employeur_retraite_supplementaire(Variable):
    value_type = float
    entity = Individu
    label = "Part salariale des cotisations de retraite supplémentaire prise en charge par l'employeur"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class ratio_alternants(Variable):
    value_type = float
    entity = Individu
    label = "Ratio d'alternants dans l'effectif moyen"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # TODO modéliser cette variable, dont la définition intervient dans le calcul de la Contribution supplémentaire d'apprentissage, et change au cours du temps.


class remboursement_transport_base(Variable):
    value_type = float
    entity = Individu
    label = 'Base pour le calcul du remboursement des frais de transport'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_forfaitaires(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités forfaitaires (transport, nourriture)'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class salaire_de_base(Variable):
    # Salaire brut sans les primes et les heures supplémentaires - généralement la première ligne du bulletin de paye.
    value_type = float
    entity = Individu
    label = 'Salaire de base'
    set_input = set_input_divide_by_period
    reference = 'https://www.insee.fr/fr/metadonnees/definition/c1937'
    definition_period = MONTH
    unit = 'currency'


class titre_restaurant_taux_employeur(Variable):
    value_type = float
    default_value = 0.5
    entity = Individu
    label = "Taux de participation de l'employeur au titre restaurant"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class titre_restaurant_valeur_unitaire(Variable):
    value_type = float
    entity = Individu
    label = 'Valeur faciale unitaire du titre restaurant'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class titre_restaurant_volume(Variable):
    value_type = int
    entity = Individu
    label = 'Volume des titres restaurant'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class traitement_indiciaire_brut(Variable):
    value_type = float
    entity = Individu
    label = 'Traitement indiciaire brut (TIB)'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class categorie_salarie(Variable):
    value_type = Enum
    possible_values = TypesCategorieSalarie  # defined in model/base.py
    default_value = TypesCategorieSalarie.prive_non_cadre
    entity = Individu
    label = 'Catégorie de salarié'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class heures_duree_collective_entreprise(Variable):
    value_type = int  # TODO default la valeur de la durée légale ?
    entity = Individu
    label = "Durée mensuelle collective dans l'entreprise (heures, temps plein)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class heures_non_remunerees_volume(Variable):
    value_type = float
    entity = Individu
    label = 'Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)'
    set_input = set_input_divide_by_period
    definition_period = MONTH


class heures_remunerees_volume(Variable):
    # N'est pas pris en compte lorsque type_contrat_travail = temps_plein
    value_type = float
    entity = Individu
    label = 'Volume des heures rémunérées contractuellement'
    set_input = set_input_divide_by_period
    definition_period = MONTH


class forfait_heures_remunerees_volume(Variable):
    value_type = int
    entity = Individu
    label = 'Volume des heures rémunérées à un forfait heures'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class forfait_jours_remuneres_volume(Variable):
    value_type = int
    entity = Individu
    label = 'Volume des heures rémunérées à forfait jours'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class volume_jours_ijss(Variable):
    value_type = int
    entity = Individu
    label = 'Volume des jours pour lesquels sont versés une idemnité journalière par la sécurité sociale'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class avantage_en_nature(Variable):
    value_type = float
    entity = Individu
    label = 'Avantages en nature'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        period = period
        avantage_en_nature_valeur_reelle = individu('avantage_en_nature_valeur_reelle', period)
        avantage_en_nature_valeur_forfaitaire = individu('avantage_en_nature_valeur_forfaitaire', period)

        return avantage_en_nature_valeur_reelle + avantage_en_nature_valeur_forfaitaire


class avantage_en_nature_valeur_forfaitaire(Variable):
    value_type = float
    entity = Individu
    label = 'Evaluation fofaitaire des avantages en nature '
    definition_period = MONTH
    set_input = set_input_divide_by_period

    # TODO: coplete this function
    def formula(individu, period, parameters):
        period = period
        avantage_en_nature_valeur_reelle = individu('avantage_en_nature_valeur_reelle', period)

        return avantage_en_nature_valeur_reelle * 0


class depense_cantine_titre_restaurant_employe(Variable):
    value_type = float
    entity = Individu
    label = "Dépense de cantine et de titre restaurant à charge de l'employe"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        period = period

        valeur_unitaire = individu('titre_restaurant_valeur_unitaire', period)
        volume = individu('titre_restaurant_volume', period)
        taux_employeur = individu('titre_restaurant_taux_employeur', period)

        return - valeur_unitaire * volume * (1 - taux_employeur)


class depense_cantine_titre_restaurant_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Dépense de cantine et de titre restaurant à charge de l'employeur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        period = period
        valeur_unitaire = individu('titre_restaurant_valeur_unitaire', period)
        volume = individu('titre_restaurant_volume', period)  # Compute with jours ouvrables ?
        taux_employeur = individu('titre_restaurant_taux_employeur', period)

        return valeur_unitaire * volume * taux_employeur


class nombre_jours_calendaires(Variable):
    value_type = float
    entity = Individu
    label = 'Nombre de jours calendaires travaillés'
    definition_period = MONTH
    default_value = 30
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)

        busday_count = partial(original_busday_count, weekmask = '1' * 7)
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
    label = "Remboursement partiel des frais de transport par l'employeur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):

        remboursement_transport_base = individu('remboursement_transport_base', period)
        # TODO: paramètres en dur dans le code
        return - .5 * remboursement_transport_base


# Fonction publique

class gipa(Variable):
    value_type = float
    entity = Individu
    label = "Indemnité de garantie individuelle du pouvoir d'achat"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO: à coder


class indemnite_residence(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnité de résidence des fonctionnaires'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        salaire_de_base = individu('salaire_de_base', period)
        categorie_salarie = individu('categorie_salarie', period)
        zone_apl = individu.menage('zone_apl', period)
        TypesZoneApl = zone_apl.possible_values
        indemnite_residence = parameters(period).marche_travail.remuneration_dans_fonction_publique.indemnite_residence
        (min_zone_1, min_zone_2, min_zone_3) = (
            indemnite_residence.min * indemnite_residence.taux.zone1,
            indemnite_residence.min * indemnite_residence.taux.zone2,
            indemnite_residence.min * indemnite_residence.taux.zone3
            )
        taux = select(
            [
                (zone_apl == TypesZoneApl.zone_1),
                (zone_apl == TypesZoneApl.zone_2),
                (zone_apl == TypesZoneApl.zone_3),
                ],
            [
                indemnite_residence.taux.zone1,
                indemnite_residence.taux.zone2,
                indemnite_residence.taux.zone3,
                ],
            default = 0
            )
        plancher = select(
            [
                (zone_apl == TypesZoneApl.zone_1),
                (zone_apl == TypesZoneApl.zone_2),
                (zone_apl == TypesZoneApl.zone_3),
                ],
            [
                min_zone_1,
                min_zone_2,
                min_zone_3,
                ],
            default = 0
            )
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )
        return max_(
            plancher,
            taux * (traitement_indiciaire_brut + salaire_de_base)
            ) * public


class indice_majore(Variable):
    value_type = float
    entity = Individu
    label = 'Indice majoré'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        period = period.start.period('month').offset('first-of')
        categorie_salarie = individu('categorie_salarie', period)
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        traitement_annuel_brut = parameters(period).prestations_sociales.fonc.IM_100
        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        return (traitement_indiciaire_brut * 100 * 12 / traitement_annuel_brut) * public


class primes_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = 'Calcul des primes pour les fonctionnaries'
    reference = 'http://vosdroits.service-public.fr/particuliers/F465.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        # period = period.first_month
        categorie_salarie = individu('categorie_salarie', period)
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)

        public = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        return TAUX_DE_PRIME * traitement_indiciaire_brut * public


class af_nbenf_fonc(Variable):
    value_type = int
    label = "Nombre d'enfants dans la famille au sens des allocations familiales pour les fonctionnaires"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        '''
            Cette variable est une version légèrement modifiée de `af_nbenf`. Elle se base sur le salaire de base, tandis que `af_nbenf` se base sur le salaire net.
            On ne peut pas utiliser la variable `af_nbenf` dans le calcul de `supplement_familial_traitement` (ci-dessous) car `af_nbenf` dépend du `salaire_net`, et `salaire_net` dépends de `supplement_familial_traitement`. Cela créerait une boucle infinie.
            D'où l'introduction de cette variable alternative.
        '''

        salaire_de_base_mensualise = famille.members('salaire_de_base', period.start.period('month', 6).offset(-6), options = [ADD])
        law = parameters(period)
        nbh_travaillees = 169
        smic_mensuel_brut = law.marche_travail.salaire_minimum.smic.smic_b_horaire * nbh_travaillees

        autonomie_financiere = (salaire_de_base_mensualise >= (
            law.prestations_sociales.prestations_familiales.def_pac.revenu_plafond_pac_non_scolaire
            * smic_mensuel_brut
            ))

        age = famille.members('age', period)

        condition_enfant = (
            (age >= law.prestations_sociales.prestations_familiales.prestations_generales.af.af_cm.age1)
            * (age <= law.prestations_sociales.prestations_familiales.prestations_generales.af.af_cm.age2)
            * not_(autonomie_financiere)
            )

        return famille.sum(condition_enfant, role = Famille.ENFANT)


class supplement_familial_traitement(Variable):
    value_type = float
    entity = Individu
    label = 'Supplément familial de traitement'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def formula(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        fonction_publique = parameters(period).marche_travail.remuneration_dans_fonction_publique
        indice_majore_100 = 100 * fonction_publique.indicefp.point_indice_en_nominal

        fonc_nbenf = individu.famille('af_nbenf_fonc', period) * individu.has_role(Famille.DEMANDEUR)

        sft = fonction_publique.sft

        part_fixe = (
            sft.part_fixe.un_enfant * (fonc_nbenf == 1)
            + sft.part_fixe.deux_enfants * (fonc_nbenf >= 2)
            + sft.part_fixe.enfant_supplementaire * max_(0, fonc_nbenf - 2)
            )

        pct_variable = (
            sft.part_proportionnelle.deux_enfants * (fonc_nbenf == 2)
            + sft.part_proportionnelle.trois_enfants * (fonc_nbenf >= 3)
            + sft.part_proportionnelle.enfant_supplementaire * max_(0, fonc_nbenf - 3)
            )

        indice_maj_min = sft.im_plancher
        indice_maj_max = sft.im_plafond

        traitement_brut_mensuel_min = _traitement_brut_mensuel(indice_maj_min, indice_majore_100)
        plancher = part_fixe + traitement_brut_mensuel_min * pct_variable

        traitement_brut_mensuel_max = _traitement_brut_mensuel(indice_maj_max, indice_majore_100)
        plafond = part_fixe + traitement_brut_mensuel_max * pct_variable

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

        return sft


def _traitement_brut_mensuel(indice_maj, indice_majore_100_annuel):
    traitement_brut = indice_majore_100_annuel * indice_maj / 100 / 12
    return traitement_brut


class remuneration_principale(Variable):
    value_type = float
    entity = Individu
    label = 'Rémunération principale des agents titulaires de la fonction publique'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    unit = 'currency'

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = individu('nouvelle_bonification_indiciaire', period)
        categorie_salarie = individu('categorie_salarie', period)

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
    label = 'Salaire net à payer (fiche de paie)'
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        '''
        Calcul du salaire net à payer après déduction des sommes
        dues par les salarié avancées par l'employeur
        '''
        salaire_net = individu('salaire_net', period, options = [ADD])
        depense_cantine_titre_restaurant_employe = individu(
            'depense_cantine_titre_restaurant_employe', period)
        indemnites_forfaitaires = individu('indemnites_forfaitaires', period)
        remuneration_apprenti = individu('remuneration_apprenti', period)
        stage_gratification = individu('stage_gratification', period)
        salaire_net_a_payer = (
            salaire_net
            + remuneration_apprenti
            + stage_gratification
            + depense_cantine_titre_restaurant_employe
            + indemnites_forfaitaires
            )
        return salaire_net_a_payer


class salaire_super_brut_hors_allegements(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire super-brut (fiche de paie): rémunération + cotisations sociales employeur'
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_de_base = individu('salaire_de_base', period)
        remuneration_principale = individu('remuneration_principale', period)
        remuneration_apprenti = individu('remuneration_apprenti', period)

        primes_fonction_publique = individu('primes_fonction_publique', period)
        indemnite_residence = individu('indemnite_residence', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        cotisations_employeur = individu('cotisations_employeur', period)
        depense_cantine_titre_restaurant_employeur = individu('depense_cantine_titre_restaurant_employeur', period)
        reintegration_titre_restaurant_employeur = individu('reintegration_titre_restaurant_employeur', period)
        indemnite_fin_contrat = individu('indemnite_fin_contrat', period)
        primes_salaires_non_exonerees = individu('primes_salaires_non_exonerees', period)
        salaire_super_brut_hors_allegements = (
            salaire_de_base
            + remuneration_apprenti
            + indemnite_fin_contrat
            + remuneration_principale
            + primes_fonction_publique
            + indemnite_residence
            + supplement_familial_traitement
            + depense_cantine_titre_restaurant_employeur
            - reintegration_titre_restaurant_employeur
            - cotisations_employeur
            + primes_salaires_non_exonerees
            )

        return salaire_super_brut_hors_allegements


class salaire_super_brut(Variable):
    value_type = float
    entity = Individu
    label = 'Coût du travail à court terme. Inclut les exonérations et allègements de charges'
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period
        salaire_super_brut_hors_allegements = individu('salaire_super_brut_hors_allegements', period)
        exonerations_et_allegements = individu('exonerations_et_allegements', period)
        return salaire_super_brut_hors_allegements - exonerations_et_allegements

    def formula_2019_01_01(individu, period, parameters):
        period = period
        salaire_super_brut_hors_allegements = individu('salaire_super_brut_hors_allegements', period)
        exonerations_et_allegements = individu('exonerations_et_allegements', period)
        prime_exceptionnelle_pouvoir_achat_exoneree = individu('prime_exceptionnelle_pouvoir_achat_exoneree', period, options = [DIVIDE])
        return salaire_super_brut_hors_allegements - exonerations_et_allegements + prime_exceptionnelle_pouvoir_achat_exoneree

    def formula_2022_07_01(individu, period, parameters):
        '''
        Apparition de la PPV le 1er aout 2022:
        Au niveau du salaire super brut, la PPV se comporte comme la PEPA.
        Pour tout niveau de revenu, la part de prime sous plafond est exonérée
        de toutes les cotisations sociales d'origine légale ou conventionnelle
        à la charge du salarié et de l'employeur (mais pas de contribution
        "forfait social") et la part de la prime non exonérée
        (sur plafond) est soumise aux cotisations.
        '''
        period = period
        salaire_super_brut_hors_allegements = individu('salaire_super_brut_hors_allegements', period)
        exonerations_et_allegements = individu('exonerations_et_allegements', period)
        prime_partage_valeur_exoneree = individu('prime_partage_valeur_exoneree', period, options=[DIVIDE])
        prime_partage_valeur_exoneree_exceptionnelle = individu('prime_partage_valeur_exoneree_exceptionnelle', period, options=[DIVIDE])
        return (
            salaire_super_brut_hors_allegements
            - exonerations_et_allegements
            + prime_partage_valeur_exoneree
            + prime_partage_valeur_exoneree_exceptionnelle
            )


class exonerations_et_allegements(Variable):
    value_type = float
    entity = Individu
    label = 'Exonérations et allègements'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        exoneration_cotisations_employeur_apprenti = individu(
            'exoneration_cotisations_employeur_apprenti', period, options = [ADD])
        exoneration_cotisations_employeur_geographiques = individu(
            'exoneration_cotisations_employeur_geographiques', period)
        exoneration_cotisations_employeur_jei = individu(
            'exoneration_cotisations_employeur_jei', period, options = [ADD])
        exoneration_cotisations_employeur_stagiaire = individu(
            'exoneration_cotisations_employeur_stagiaire', period, options = [ADD])

        allegement_fillon = individu('allegement_fillon', period, options = [ADD])
        allegement_cotisation_maladie = individu('allegement_cotisation_maladie', period, options = [ADD])
        allegement_cotisation_allocations_familiales = individu('allegement_cotisation_allocations_familiales', period, options = [ADD])

        return (
            allegement_fillon
            + allegement_cotisation_maladie
            + allegement_cotisation_allocations_familiales
            + exoneration_cotisations_employeur_geographiques
            + exoneration_cotisations_employeur_jei
            + exoneration_cotisations_employeur_apprenti
            + exoneration_cotisations_employeur_stagiaire
            )


class cout_du_travail(Variable):
    value_type = float
    entity = Individu
    label = 'Coût du travail à long terme. Inclut les charges, aides et crédits différés'
    set_input = set_input_divide_by_period
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        salaire_super_brut = individu('salaire_super_brut', period)
        cout_differe = individu('cout_differe', period)
        return salaire_super_brut - cout_differe


class cout_differe(Variable):
    value_type = float
    entity = Individu
    label = 'Charges, aides et crédits différés ou particuliers'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        credit_impot_competitivite_emploi = individu('credit_impot_competitivite_emploi', period, options = [ADD])
        aide_premier_salarie = individu('aide_premier_salarie', period, options = [ADD])
        aide_embauche_pme = individu('aide_embauche_pme', period, options = [ADD])
        tehr = individu('tehr', period, options = [DIVIDE])

        return credit_impot_competitivite_emploi + aide_premier_salarie + aide_embauche_pme + tehr


class TypesConges(Enum):
    non_renseigne = 'Non renseigné'
    conge_parental = 'Congé parental'
    conge_maternite_paternite = 'Congé maternité ou paternité'
    conge_presence_parentale = 'Congé de présence parentale'
    conge_conventionnel = 'Congé conventionnel'
    conge_sans_solde = 'Congé sans solde'
    disponibilite = 'Mise en disponibilité (fonction publique)'
    conge_sabbatique = 'Congé sabbatique'


class type_conges(Variable):
    value_type = Enum
    possible_values = TypesConges
    default_value = TypesConges.non_renseigne
    entity = Individu
    label = 'Type de congés en cours'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
