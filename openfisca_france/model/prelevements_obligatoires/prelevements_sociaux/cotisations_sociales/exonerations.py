import numpy as np
from numpy import datetime64, timedelta64

from openfisca_france.model.base import *
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal


class jei_date_demande(Variable):
    value_type = date
    default_value = date(2099, 12, 31)
    entity = Individu
    label = "Date de demande (et d'octroi) du statut de jeune entreprise innovante (JEI)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class exoneration_cotisations_employeur_tode_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'exonération de cotisations employeur agricole pour travailleur occasionnel demandeur d'emploi (TO-DE)"
    reference = [
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037947610/',
        'https://www.msa.fr/lfp/employeur/exonerations-travailleurs-occasionnels'
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    end = '2025-12-31'
    documentation = '''
        Non modélisé (2022), tout employeur MSA sauf ces employeurs :
        Coopératives d'utilisation de matériel agricole (CUMA).
        Coopératives de transformation, conditionnement et commercialisation.
        Entreprises paysagistes.
        Structures exerçant des activités de tourisme à la ferme.
        Entreprises de service (Crédit agricole, Groupama, caisses de MSA, groupements professionnels agricoles, Chambres d'agriculture…).
        Artisans ruraux.
        Entreprises de travail temporaire (ETT) et les entreprises de travail temporaire d'insertion (ETTI).
        Entreprises de travaux agricoles, ruraux et forestiers (ETARF).
    '''

    def formula_2019(individu, period):
        # employeur relevant de la MSA
        secteur_agricole = individu('secteur_activite_employeur', period) == TypesSecteurActivite.agricole
        regime_agricole = individu('regime_securite_sociale', period) == RegimeSecuriteSociale.regime_agricole

        # salarié travailleur occasionnel agricole
        travailleur_occasionnel_agricole = individu('travailleur_occasionnel_agricole', period)

        return (secteur_agricole + regime_agricole) * travailleur_occasionnel_agricole


class exoneration_cotisations_employeur_tode(Variable):
    value_type = float
    entity = Individu
    label = "Exonération de cotisations employeur agricole pour travailleur occasionnel demandeur d'emploi (TO-DE)"
    reference = [
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037947610/',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038026966'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2025-12-31'
    documentation = '''
        Exonération de cotisations et contributions employeur sur les bas salaires.

        Non modélisé (2022):
        La durée maximale d’application de l’exonération TO-DE est fixée à 119 jours
        consécutifs ou non, par employeur, par salarié et par année civile.
    '''

    def formula_2019(individu, period, parameters):
        # l'individu est le travailleur occasionnel
        eligible = individu('exoneration_cotisations_employeur_tode_eligibilite', period)

        # cotisations assurances sociales agricoles (ASA) - identiques régime général
        mmid_employeur_net_allegement = individu('mmid_employeur_net_allegement', period)

        famille = individu('famille_net_allegement', period)
        accident_du_travail = individu('accident_du_travail', period)
        fnal = individu('fnal', period)

        vieillesse_deplafonnee_employeur = individu('vieillesse_deplafonnee_employeur', period)
        vieillesse_plafonnee_employeur = individu('vieillesse_plafonnee_employeur', period)
        agirc_arrco_employeur = individu('agirc_arrco_employeur', period)
        contribution_equilibre_general_employeur = individu('contribution_equilibre_general_employeur', period)

        contribution_solidarite_autonomie = individu('contribution_solidarite_autonomie', period)
        chomage_employeur = individu('chomage_employeur', period)

        # les cotisations sont des prélèvements, l'exonération leur opposé
        assiette_exoneration = -1 * (
            mmid_employeur_net_allegement
            + famille
            + accident_du_travail
            + fnal
            + vieillesse_deplafonnee_employeur
            + vieillesse_plafonnee_employeur
            + agirc_arrco_employeur
            + contribution_equilibre_general_employeur
            + contribution_solidarite_autonomie
            + chomage_employeur
            )

        # Exonération totale à <= 1.2 Smic
        # Puis dégressive : 1,2 × C/0,40 × (1,6 × montant mensuel du Smic/ rémunération mensuelle brute hors heures supplémentaires et complémentaires-1)
        # Devient nulle à >= 1.6 Smic

        salaire_de_base = individu('salaire_de_base', period)
        smic_proratise = individu('smic_proratise', period)

        parameters_tode = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.agricole.tode
        coefficient_degressivite = parameters_tode.plafond - parameters_tode.plafond_exoneration_integrale
        exoneration_degressive = parameters_tode.plafond_exoneration_integrale * (assiette_exoneration / coefficient_degressivite) * (parameters_tode.plafond * smic_proratise / salaire_de_base - 1)

        sous_plancher = salaire_de_base <= (parameters_tode.plafond_exoneration_integrale * smic_proratise)
        sous_plafond = salaire_de_base < (parameters_tode.plafond * smic_proratise)
        exoneration = where(sous_plancher, assiette_exoneration, sous_plafond * exoneration_degressive)

        # non cumul avec l'allègement général de cotisations employeur sur les bas salaires (Fillon)
        choix_exoneration_cotisations_employeur_agricole = individu('choix_exoneration_cotisations_employeur_agricole', period)

        return choix_exoneration_cotisations_employeur_agricole * eligible * exoneration


class choix_exoneration_cotisations_employeur_agricole(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "L'employeur agricole choisit une exonération de cotisations employeur spécifique au secteur agricole"
    reference = 'https://www.msa.fr/lfp/employeur/exonerations-travailleurs-occasionnels'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = '''
    Pour un travailleur occasionnel, l'employeur agricole a le choix
    entre la réduction générale de cotisations sur les bas salaires (Fillon)
    et la TO-DE.
    La TO-DE est plus avantageuse mais à son arrêt au 12.2022,
    la réduction Fillon sera applicable.
    '''


class exoneration_cotisations_employeur_geographiques(Variable):
    value_type = float
    entity = Individu
    label = "Exonérations de cotisations employeur dépendant d'une zone géographique"
    reference = 'https://www.apce.com/pid815/aides-au-recrutement.html?espace=1&tp=1'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        exoneration_cotisations_employeur_zfu = individu('exoneration_cotisations_employeur_zfu', period, options = [ADD])
        exoneration_cotisations_employeur_zrd = individu('exoneration_cotisations_employeur_zrd', period, options = [ADD])
        exoneration_cotisations_employeur_zrr = individu('exoneration_cotisations_employeur_zrr', period, options = [ADD])
        exoneration_lodeom = individu('exoneration_lodeom', period, options=[ADD])

        exonerations_geographiques = (
            exoneration_cotisations_employeur_zfu
            + exoneration_cotisations_employeur_zrd
            + exoneration_cotisations_employeur_zrr
            + exoneration_lodeom
            )

        return exonerations_geographiques


class exoneration_cotisations_employeur_jei(Variable):
    value_type = float
    entity = Individu
    label = 'Exonération de cotisations employeur pour JEI (jeune entreprise innovante)'
    reference = 'http://www.apce.com/pid1653/jeune-entreprise-innovante.html?pid=1653&pagination=2'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2004_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        jei_date_demande = individu('jei_date_demande', period)
        jeune_entreprise_innovante = individu('jeune_entreprise_innovante', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        smic_proratise = individu('smic_proratise', period)

        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_employeur
        bareme_names = ['vieillesse_deplafonnee', 'vieillesse_plafonnee', 'maladie', 'famille']

        exoneration = smic_proratise * 0.0
        for bareme_name in bareme_names:
            exoneration += apply_bareme_for_relevant_type_sal(
                bareme_by_type_sal_name = bareme_by_type_sal_name,
                bareme_name = bareme_name,
                categorie_salarie = categorie_salarie,
                base = assiette_allegement,
                plafond_securite_sociale = plafond_securite_sociale,
                round_base_decimals = 2,
                )

        exoneration_relative_year_passed = exoneration_relative_year(period, jei_date_demande)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            }  # TODO: move to parameters file
        for year_passed, rate in rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                exoneration[condition_on_year_passed] = rate * exoneration

        return - exoneration * jeune_entreprise_innovante

    # À compter de 2011, l'exonération JEI est modifiée avec l'introduction, par l'article 175 de la LOI n° 2010-1657 du 29 décembre 2010 de finances pour 2011, d'une double limite de l'exonération. L'exonération s'applique uniquement sur la part de la rémunération inférieur à 4,5 fois le Smic, et un montant maximal par établissement est instauré.

    def formula_2011_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        jei_date_demande = individu('jei_date_demande', period)
        jeune_entreprise_innovante = individu('jeune_entreprise_innovante', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        smic_proratise = individu('smic_proratise', period)
        categorie_salarie = individu('categorie_salarie', period)

        # Cette formule ne tient pas compte du montant maximal d'exonération dont chaque établissement peut bénéficier et qui est de 5 PSS (231 840 € en 2024)

        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_employeur
        bareme_names = ['vieillesse_deplafonnee', 'vieillesse_plafonnee', 'maladie', 'famille']
        plafond_part_remuneration = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.jei.plafond_part_remuneration

        exoneration = smic_proratise * 0.0
        for bareme_name in bareme_names:
            exoneration += apply_bareme_for_relevant_type_sal(
                bareme_by_type_sal_name = bareme_by_type_sal_name,
                bareme_name = bareme_name,
                categorie_salarie = categorie_salarie,
                base = min_(assiette_allegement, plafond_part_remuneration * smic_proratise),
                plafond_securite_sociale = plafond_securite_sociale,
                round_base_decimals = 2,
                )

        exoneration_relative_year_passed = exoneration_relative_year(period, jei_date_demande)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            }  # TODO: move to parameters file
        for year_passed, rate in rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                exoneration[condition_on_year_passed] = rate * exoneration

        return - exoneration * jeune_entreprise_innovante


class exoneration_cotisations_employeur_zfu(Variable):
    value_type = float
    entity = Individu
    label = "Exonération de cotisations employeur pour l'embauche en ZFU (zone franche urbaine)"
    reference = 'http://www.apce.com/pid553/exoneration-dans-les-zfu.html?espace=1&tp=1&pagination=2'
    definition_period = MONTH
    set_input = set_input_divide_by_period

# TODO
# Ce dispositif d'exonération sociale est fermé depuis le 1er janvier 2015 mais reste applicable aux entreprises qui
# en bénéficiaient avant cette date.
# - ne pas être détenues à plus de 25 % par des entreprises employant plus de 250 salariés et dont le chiffre d'affaires
#   ou dont le bilan excède 50 M€ ou 43 M€,
# - disposer des éléments d'exploitation ou des stocks nécessaires à l'activité des salariés,
# - être à jour de ses cotisations sociales ou avoir souscrit à un engagement d'apurement progressif de ses dettes.
#
# Secteurs d'activité concernés
#
# L'exonération est applicable, quel que soit le secteur d'activité.
# Toutefois, les entreprises exerçant une activité principale dans les secteurs de la construction automobile,
# construction navale, fabrication de fibres textiles artificielles ou synthétiques, sidérurgie ou des transports
# routiers de marchandises, ne pourront pas bénéficier de cette exonération.

# Embauche de résidents (clause d'embauche locale)
# Pour les entreprises qui se créent ou s'implantent dans une ZFU à compter du 1er janvier 2012,  le bénéfice de
# l'exonération des cotisations sociales est subordonnée lors de toute nouvelle embauche à la condition que la moitié
# de salariés embauchés ou employés résident en ZFU ou en zone urbaine sensible.
#
# Le respect de la condition d'embauche locale est apprécié à la date d'effet de la nouvelle embauche dès la deuxième
# embauche.
#
# Précision : les salariés employés sont ceux déjà présents dans l'entreprise à la date de la nouvelle embauche, les
# salariés embauchés sont ceux recrutés depuis la date de création ou d'implantation de l'entreprise en ZFU.
#
# Est considéré comme résident le salarié habitant soit dans la ZFU d'implantation, soit dans l'une des ZUS de l'unité
# urbaine où se trouve la ZFU. Le maire peut, à la demande de l'employeur, fournir des éléments d'informations relatifs
# à la qualité de résident dans la zone afin de déterminer si la proportion exigée est respectée.
#
# Si la proportion n'est pas respectée à la date d'effet de l'embauche, l'employeur dispose d'un délai de 3 mois pour
# régulariser la situation. A défaut, le bénéfice de l'exonération est suspendu du 1er jour du mois suivant
# l'expiration du délai de 3 mois, jusqu'au 1er jour du mois suivant la date où la condition est de nouveau remplie.
#
# Le salarié résident doit être titulaire d'un contrat à durée indéterminée ou d'un contrat à durée déterminée d'au
# moins 12 mois, conclu pour une durée minimale de 16 heures par semaine.
# 5 ans +
# Dans les entreprises de 5 salariés et plus, les cotisations employeur bénéficient d'un abattement sur la base
# imposable pendant 3 ans de :
# - 60 % la première année,
# - 40 % la seconde année,
# - 20 % la troisième année.
#
# Dans les entreprises de moins de 5 salariés, un abattement est appliqué sur 9 ans de la manière suivante :
# - 60 % les 5 premières années,
# - 40 % les 2 années suivantes,
# - 20 % les deux dernières années.
#
# Le cumul de l'ensemble des aides publiques de minimis (allégements fiscaux, sociaux et aides des collectivités
# territoriales) ne peut dépasser le plafond des aides de minimis, fixé à 200 000 euros sur une période glissante de 36
# mois (100 000 euros pour les entreprises de transport routier).

    def formula(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        entreprise_bilan = individu('entreprise_bilan', period)
        taux_versement_transport = individu('taux_versement_transport', period)

        # TODO: move to parameters file
        entreprise_eligible = (entreprise_chiffre_affaire <= 1e7) | (entreprise_bilan <= 1e7)

        smic_proratise = individu('smic_proratise', period)
        zone_franche_urbaine = individu('zone_franche_urbaine', period)

        duree_cdd_eligible = (contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D'))
        # TODO: move to parameters file
        contrat_de_travail_eligible = (contrat_de_travail_debut <= datetime64('2014-12-31')) * ((contrat_de_travail_type == TypesContrat.cdi) + ((contrat_de_travail_type == TypesContrat.cdd) * (duree_cdd_eligible)))
        # TODO: move to parameters file

        eligible = (
            contrat_de_travail_eligible
            * (effectif_entreprise <= 50)
            * zone_franche_urbaine
            * entreprise_eligible
            )

        bareme_by_name = parameters(period).cotsoc.cotisations_employeur['prive_non_cadre']

        if period.start.year < 2007:
            fnal_contrib = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.fnal.contribution_plus_de_10_salaries
            fnal_contrib_seuil = 10
        elif period.start.year >= 2007 and period.start.year < 2020:
            fnal_contrib = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.fnal.contribution_plus_de_20_salaries
            fnal_contrib_seuil = 20
        else:
            fnal_contrib = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.fnal.contribution_plus_de_50_salaries
            fnal_contrib_seuil = 50

        if period.start.year < 2019:
            taux_maladie = bareme_by_name['maladie'].rates[0]
        else:
            taux_maladie = 0

        if period.start.year < 2015:
            fnal_cotisation = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.fnal.cotisation.rates[0]
        else:
            fnal_cotisation = 0

        taux_max = (
            bareme_by_name['vieillesse_deplafonnee'].rates[0]
            + bareme_by_name['vieillesse_plafonnee'].rates[0]
            + taux_maladie
            + bareme_by_name['famille'].rates[0]
            + fnal_cotisation
            + fnal_contrib.rates[0] * (effectif_entreprise >= fnal_contrib_seuil)
            + taux_versement_transport
            )

        # TODO: move to parameters file : voir http://www.urssaf.fr/images/ref_lc2009-077.pdf
        seuil_max = 2
        seuil_min = 1.4

        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_debut)

        large_rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .60,
            6: .40,
            7: .20,
            }  # TODO: move to parameters file

        small_rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .60,
            6: .60,
            7: .60,
            8: .60,
            9: .60,
            10: .40,
            11: .40,
            12: .20,
            13: .20,
            }  # TODO: move to parameters file

        large_taux_exoneration = eligible * 0.0
        small_taux_exoneration = eligible * 0.0

        for year_passed, rate in large_rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                large_taux_exoneration[condition_on_year_passed] = rate * taux_exoneration

        for year_passed, rate in small_rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                small_taux_exoneration[condition_on_year_passed] = rate * taux_exoneration

        exoneration_cotisations_zfu = (
            eligible
            * assiette_allegement
            * (
                small_taux_exoneration
                * (effectif_entreprise <= 5)
                + large_taux_exoneration
                * (effectif_entreprise > 5)
                )
            )

        return exoneration_cotisations_zfu
        # TODO: propager dans le temps


class exoneration_cotisations_employeur_zrd(Variable):
    value_type = float
    entity = Individu
    label = "Exonération de cotisations employeur pour l'embauche en ZRD (zone de restructuration de la Défense)"
    reference = 'http://www.apce.com/pid11668/exoneration-dans-les-zrd.html?espace=1&tp=1'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    # L'exonération a été créée en 2009 par la loi de finances rectificative du 30 décembre 2008.

    def formula_2009_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        entreprise_creation = individu('entreprise_creation', period)
        smic_proratise = individu('smic_proratise', period)
        zone_restructuration_defense = individu('zone_restructuration_defense', period)
        seuils = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.zrd
        t_max_parameters = parameters(period).prelevements_sociaux

        eligible = zone_restructuration_defense

        # Paramètre T mis en dur initialement dans la formule et laissé tel quel car le paramètre reductions_cotisations_sociales.alleg_gen.mmid.taux existe uniquement depuis 2019.

        taux_max = .281 if period.start.year < 2019 else (t_max_parameters.cotisations_securite_sociale_regime_general.mmid.employeur.maladie.rates[0] - t_max_parameters.reductions_cotisations_sociales.alleg_gen.mmid.taux + t_max_parameters.cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_plafonnee.rates[0] + t_max_parameters.cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_deplafonnee.rates[0] + t_max_parameters.cotisations_securite_sociale_regime_general.famille.employeur.famille.rates[0] - t_max_parameters.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales.reduction)

        seuil_max = seuils.plafond_part_remuneration
        seuil_min = seuils.plafond_exoneration_integrale_part_remuneration

        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)

        exoneration_relative_year_passed = exoneration_relative_year(period, entreprise_creation)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 2 / 3,
            4: 1 / 3,
            }  # TODO: move to parameters file
        ratio = eligible * 0.0
        for year_passed, rate in rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                ratio[condition_on_year_passed] = rate

        exoneration_cotisations_zrd = ratio * taux_exoneration * assiette_allegement * eligible

        return exoneration_cotisations_zrd


class exoneration_cotisations_employeur_zrr(Variable):
    value_type = float
    entity = Individu
    label = "Exonération de cotisations employeur pour l'embauche en ZRR (zone de revitalisation rurale)"
    reference = 'http://www.apce.com/pid538/embauches-en-zru-et-zrr.html?espace=1&tp=1'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    # Les entreprises et groupements d'employeurs exerçant une activité industrielle, commerciale, artisanale, agricole
    # ou libérale et cotisant au régime d'assurance chômage.
    # Les entreprises concernées, y compris chacune de celles appartenant à un groupement d'employeurs, doivent avoir
    # au moins un établissement situé en zone de revitalisation rurale.
    #
    # A noter : les associations à but non lucratif sont exclues du dispositif. Par contre, quelle que soit leur forme
    # juridique, les entreprises d'insertion ou d'intérim d'insertion peuvent en bénéficier. Les régies de quartier
    # peuvent en bénéficier lorsque leur activité est susceptible d'entraîner l'assujettissement à la TVA à l'impôt sur
    # les sociétés ainsi qu'à la contribution économique territoriale qu'elles en soient effectivement redevables
    # ou non.
    #
    # L'employeur ne doit avoir procédé à aucun licenciement économique durant les 12 mois précédant l'embauche.

    def formula_1997_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        smic_proratise = individu('smic_proratise', period)
        zone_revitalisation_rurale = individu('zone_revitalisation_rurale', period)
        seuils = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.zrr

        duree_cdd_eligible = contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D')
        # TODO: move to parameters file
        contrat_de_travail_eligible = (contrat_de_travail_type == TypesContrat.cdi) + ((contrat_de_travail_type == TypesContrat.cdd) * (duree_cdd_eligible))

        duree_validite = (
            datetime64(period.start) + timedelta64(1, 'D') - contrat_de_travail_debut
            ).astype('timedelta64[Y]') < timedelta64(1, 'Y')

        eligible = (
            contrat_de_travail_eligible
            * (effectif_entreprise <= 50)
            * zone_revitalisation_rurale
            * duree_validite
            )

        taux_max = .281
        plafond = seuils.plafond_exoneration_integrale_part_remuneration

        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
        taux_exoneration = round_(
            taux_max * max_(plafond * (1 - ratio_smic_salaire), 0),
            4,
            )
        exoneration_cotisations_zrr = taux_exoneration * assiette_allegement * eligible

        return exoneration_cotisations_zrr

    def formula_2008_03_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        smic_proratise = individu('smic_proratise', period)
        zone_revitalisation_rurale = individu('zone_revitalisation_rurale', period)
        seuils = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.zrr
        t_max_parameters = parameters(period).prelevements_sociaux

        duree_cdd_eligible = contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D')
        # TODO: move to parameters file
        contrat_de_travail_eligible = (contrat_de_travail_type == TypesContrat.cdi) + ((contrat_de_travail_type == TypesContrat.cdd) * (duree_cdd_eligible))

        duree_validite = (
            datetime64(period.start) + timedelta64(1, 'D') - contrat_de_travail_debut
            ).astype('timedelta64[Y]') < timedelta64(1, 'Y')

        eligible = (
            contrat_de_travail_eligible
            * (effectif_entreprise <= 50)
            * zone_revitalisation_rurale
            * duree_validite
            )

        if period.start.year < 2015:
            taux_max = 0.281
        elif period.start.year < 2019:
            taux_max = 0.2655
        else:
            taux_max = (t_max_parameters.cotisations_securite_sociale_regime_general.mmid.employeur.maladie.rates[0] - t_max_parameters.reductions_cotisations_sociales.alleg_gen.mmid.taux + t_max_parameters.cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_plafonnee.rates[0] + t_max_parameters.cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_deplafonnee.rates[0] + t_max_parameters.cotisations_securite_sociale_regime_general.famille.employeur.famille.rates[0] - t_max_parameters.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales.reduction)

        seuil_max = seuils.plafond_part_remuneration
        seuil_min = seuils.plafond_exoneration_integrale_part_remuneration

        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_cotisations_zrr = taux_exoneration * assiette_allegement * eligible

        return exoneration_cotisations_zrr


# Aides à la création
class exoneration_is_creation_zrr(Variable):
    value_type = float
    entity = Individu
    label = "Exonérations fiscales pour création d'une entreprise en zone de revitalisation rurale (ZRR)"
    reference = 'http://www.apce.com/pid11690/exonerations-d-impots-zrr.html?espace=1&tp=1'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula(individu, period):
        decembre = period.first_month.offset(11, 'month')
        effectif_entreprise = individu('effectif_entreprise', decembre)
        entreprise_benefice = individu('entreprise_benefice', period, options = [ADD])
        # TODO: MODIFIER avec création d'entreprise
        contrat_de_travail_type = individu('contrat_de_travail_type', decembre)

        TypesContrat = contrat_de_travail_type.possible_values

        contrat_de_travail_debut = individu('contrat_de_travail_debut', decembre)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', decembre)
        duree_eligible = contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D')
        # TODO: move to parameters file
        contrat_de_travail_eligible = (contrat_de_travail_type == TypesContrat.cdi) + ((contrat_de_travail_type == TypesContrat.cdd) * (duree_eligible))
        zone_revitalisation_rurale = individu('zone_revitalisation_rurale', decembre)

        eligible = (
            contrat_de_travail_eligible
            * (effectif_entreprise <= 50)
            * zone_revitalisation_rurale
            )

        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_debut)

        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .75,
            6: .50,
            7: .25,
            }  # TODO: move to parameters file
        taux_exoneraion = eligible * 0.0

        for year_passed, rate in rate_by_year_passed.items():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            taux_exoneraion[condition_on_year_passed] = rate

        return taux_exoneraion * entreprise_benefice
        # TODO: mettre sur toutes les années


# # class bassin_emploi_redynamiser(Variable):
#     value_type = bool
#     entity = Individu
#     label = "L'entreprise est située danns un bassin d'emploi à redynamiser(BER)"
#     # La liste des bassins d'emploi à redynamiser a été fixée par le décret n°2007-228 du 20 février 2007.
#     # Actuellement, deux régions sont concernées : Champagne-Ardenne (zone d'emploi de la Vallée de la Meuse)
#     # et Midi-Pyrénées (zone d'emploi de Lavelanet).
#
#     def formula(individu, period, parameters):
#         effectif_entreprise = individu('effectif_entreprise', period)
#         return (effectif_entreprise >= 1) * False

class jeune_entreprise_innovante(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est une jeune entreprise innovante"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        # Toute entreprise existante au 1er janvier 2004 ou créée entre le 1er janvier 2004 et le 31 décembre 2016 à
        # condition de remplir les conditions suivantes :
        #
        # avoir moins de 8 ans d'existence au moment de la demande
        #
        # être réellement nouvelle, c'est-à-dire ne pas avoir été créée dans le cadre d'une concentration,
        # d'une restructuration, d'une extension d'activité préexistante ou d'une reprise
        #
        # employer moins de 250 personnes au cours de l'exercice au titre duquel elle demande à bénéficier de ce statut
        #
        # réaliser un chiffre d'affaires inférieur à 50 M€  et disposer d'un total de bilan inférieur à 43 M€
        #
        # être indépendante, c'est-à-dire que son capital doit être détenu pour 50 % au minimum par :
        #
        # - des personnes physiques
        #
        # - une ou plusieurs autres JEI dont 50 % du capital au moins est détenu par des personnes physiques
        #
        # - des associations ou fondations reconnues d'utilité publique à caractère scientifique
        #
        # - des établissements de recherche et d'enseignement et leurs filiales
        #
        # - des structures d'investissement sous réserve qu'il n'y ait pas de lien de dépendance telles que des :
        #   -  fonds communs de placement dans l'innovation (FCPI)
        #   -  sociétés de capital-risque
        #   -  fonds d'investissement de proximité (FIP)
        #   -  sociétés de développement régional (SDR)
        #   -  sociétés financières d'innovation (SFI)
        #   -  sociétés unipersonnelles d'investissements à risques (SUIR).
        #
        # réaliser des dépenses de R§D représentant au moins 15 % des charges fiscalement déductibles au titre du même
        # exercice.
        effectif_entreprise = individu('effectif_entreprise', period)
        entreprise_bilan = individu('entreprise_bilan', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        entreprise_creation = individu('entreprise_creation', period)
        # entreprise_depenses_rd =  individu('entreprise_depenses_rd', period)
        jei_date_demande = individu('jei_date_demande', period)
        # TODO: move to parameters file
        # entreprise_depenses_rd > .15 TODO
        independance = True

        jeune_entreprise_innovante = (
            independance
            * (effectif_entreprise < 250)
            * (entreprise_creation <= datetime64('2016-12-31'))
            * ((jei_date_demande + timedelta64(1, 'D') - entreprise_creation).astype('timedelta64[Y]') < timedelta64(8, 'Y'))
            * (entreprise_chiffre_affaire < 50e6)
            * (entreprise_bilan < 43e6)
            )

        return jeune_entreprise_innovante


class bassin_emploi_redynamiser(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est située dans un bassin d'emploi à redynamiser (BER)"
    # La liste des bassins d'emploi à redynamiser a été fixée par le décret n°2007-228 du 20 février 2007.
    # Actuellement, deux régions sont concernées : Champagne-Ardenne (zone d'emploi de la Vallée de la Meuse)
    # et Midi-Pyrénées (zone d'emploi de Lavelanet).
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        effectif_entreprise = individu('effectif_entreprise', period)

        return (effectif_entreprise >= 1) * False


class zone_restructuration_defense(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est située dans une zone de restructuration de la Défense (ZRD)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        effectif_entreprise = individu('effectif_entreprise', period)
        return (effectif_entreprise >= 1) * False


class zone_franche_urbaine(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est située danns une zone franche urbaine (ZFU)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        effectif_entreprise = individu('effectif_entreprise', period)
        return (effectif_entreprise >= 1) * False


class zone_revitalisation_rurale(Variable):
    value_type = bool
    entity = Individu
    label = "L'entreprise est située dans une zone de revitalisation rurale (ZRR)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        effectif_entreprise = individu('effectif_entreprise', period)
        return (effectif_entreprise >= 1) * False


# Helpers

def compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min = 1):
    ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
    # règle d'arrondi: 4 décimales au dix-millième le plus proche ( # TODO: reprise de l'allègement Fillon unchecked)
    return round_(
        taux_max * min_(1, max_(seuil_max * seuil_min * ratio_smic_salaire - seuil_min, 0) / (seuil_max - seuil_min)),
        4,
        )


def exoneration_relative_year(period, other_date):
    return (datetime64(period.start) + timedelta64(1, 'D') - other_date).astype('timedelta64[Y]')


# Pour la Guadeloupe, la Guyane, la Martinique et la Réunion
# Dispositif de compétitivité
# Types de bénéficiaire du régime de perfectionnement actif
class TypesPerfectionnementActif(Enum):
    __order__ = 'non_renseigne beneficiaire non_beneficiaire'
    non_renseigne = 'Non renseigné'
    beneficiaire = 'Bénéficiaire du régime de perfectionnement actif'
    non_beneficiaire = 'Non bénéficiaire du régime de perfectionnement actif'


# Bénéficiaire du régime de perfectionnement actif
class perfectionnement_actif(Variable):
    value_type = Enum
    possible_values = TypesPerfectionnementActif
    default_value = TypesPerfectionnementActif.non_renseigne
    entity = Individu
    label = 'Bénéficiaire du régime de perfectionnement actif'
    reference = ''
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


# Types de secteurs d'activité de l'employeur
# Peut peut-être être fusionné avec TypeSecteurActivite dans openfisca_france.model.base
class TypesSecteurActiviteLODEOM(Enum):
    __order__ = 'non_renseigne batiment transport_aerien desserte_maritime compta_conseil presse audiovisuel divers autre_secteur'
    non_renseigne = 'Non renseigné'
    batiment = 'Bâtiment, Travaux publics'
    transport_aerien = 'Transport aérien'
    desserte_maritime = 'Desserte maritime'
    compta_conseil = 'Comptabilité, Conseil aux entreprises, Ingénierie, Etudes techniques'
    presse = 'Presse'
    audiovisuel = 'Production audiovisuelle'
    divers = "Industrie, Restauration, Environnement, Agronutrition, Energies renouvelables, NTIC, Centres d'appel, Pêche, Cultures marines, Aquaculture, Agriculture, Nautisme, Hôtellerie, Recherche et développement"
    autre_secteur = 'Autre secteur'


# Secteur d'activité de l'employeur
class secteur_activite_employeur_lodeom(Variable):
    value_type = Enum
    possible_values = TypesSecteurActiviteLODEOM
    default_value = TypesSecteurActiviteLODEOM.non_renseigne
    entity = Individu
    label = 'Eligibilité au dispositif compétitivité de LODEOM'
    reference = ''
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


# Effectif de l'entreprise dans les DROM
class effectif_entreprise_drom(Variable):
    entity = Individu
    value_type = int
    label = "Effectif de l'entreprise dans le DROM"
    set_input = set_input_dispatch_by_period
    # is_period_size_independant = True
    definition_period = MONTH


# Définition de la classe d'éligibilité au dispositif compétitivité
class eligibilite_lodeom_competitivite(Variable):
    value_type = bool
    entity = Individu
    label = 'Eligibilité au dispositif compétitivité de LODEOM'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042683758'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # Sont concernés :
    # - les employeurs de moins de 11 salariés
    # - les employeurs des secteurs du bâtiment, des travaux publics, des transports aériens pour certaines liaisons et ceux assurant la desserte maritime entre certains points

    def formula_2009_01_01(individu, period):
        # Extraction des variables d'intérêt
        depcom_entreprise = individu('depcom_entreprise', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_11_salaries = effectif_entreprise_drom < 11  # Ajouter dans les paramètres
        # Définition de l'appartenance à certains secteurs
        secteur_batiment = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.batiment
        secteur_aerien = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.transport_aerien
        secteur_maritime = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.desserte_maritime

        # Distinction suivant la période
        # Avant le 1er janvier 2019 tous les salariés dans les DROM sont éligibles
        # Définition de l'appartenance à certains secteurs
        secteur_presse = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.presse
        secteur_audiovisuel = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.audiovisuel
        secteur_divers_eligible = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.divers

        # Définition de l'éligibilité
        eligibilite = dep_drom * (effectif_moins_11_salaries + secteur_batiment + secteur_aerien + secteur_maritime + secteur_presse + secteur_audiovisuel + secteur_divers_eligible)

        return eligibilite

    def formula_2019_01_01(individu, period):
        # Extraction des variables d'intérêt
        depcom_entreprise = individu('depcom_entreprise', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_11_salaries = effectif_entreprise_drom < 11  # Ajouter dans les paramètres
        # Définition de l'appartenance à certains secteurs
        secteur_batiment = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.batiment
        secteur_aerien = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.transport_aerien
        secteur_maritime = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.desserte_maritime
        # A partir du premier janvier 2019, restriction à certains secteurs pour les plus de 11 salariés
        # Extraction des variables d'intérêt
        perfectionnement_actif = individu('perfectionnement_actif', period)

        # Définition de l'éligibilité au régime de perfectionnement actif
        beneficiaire_perfectionnement_actif = perfectionnement_actif == TypesPerfectionnementActif.beneficiaire

        # Définition de l'éligibilité
        eligibilite = dep_drom * (effectif_moins_11_salaries + secteur_batiment + secteur_aerien + secteur_maritime + beneficiaire_perfectionnement_actif)

        return eligibilite


# /!\ Revoir si la formule est bonne pour toutes les dates depuis 2009
# Définition de la classe définissant le montant associé au dispositif de compétitivité
class exoneration_lodeom_competitivite(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'exonération associé au dispositif compétitivité de LODEOM"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041404691'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2009_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite = individu('eligibilite_lodeom_competitivite', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite

        # Définition de la petite entreprise
        petite_entreprise = (effectif_entreprise_drom < 11)
        # Valorisation des paramètres d'intérêt
        # Moins de 11 salariés
        seuil_moins_de_11_salaries = lodeom_competitivite.seuil_entreprises_de_moins_de_11_salaries
        pente_moins_de_11_salaries = lodeom_competitivite.pente_entreprises_de_moins_de_11_salaries
        plafond_moins_de_11_salaries = lodeom_competitivite.plafond_entreprises_de_moins_de_11_salaries
        # Plus de 11 salariés
        seuil_11_salaries_et_plus = lodeom_competitivite.seuil_entreprises_de_11_salaries_et_plus
        pente_11_salaries_et_plus = lodeom_competitivite.pente_entreprises_de_11_salaries_et_plus
        plafond_11_salaries_et_plus = lodeom_competitivite.plafond_entreprises_de_11_salaries_et_plus
        # Communs
        taux = lodeom_competitivite.taux

        # Définition des paramètres applicables
        seuil = (
            seuil_11_salaries_et_plus * not_(petite_entreprise)
            + seuil_moins_de_11_salaries * petite_entreprise
            )
        plafond = (
            plafond_11_salaries_et_plus * not_(petite_entreprise)
            + plafond_moins_de_11_salaries * petite_entreprise
            )
        pente = (
            pente_11_salaries_et_plus * not_(petite_entreprise)
            + pente_moins_de_11_salaries * petite_entreprise
            )
        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)

        # Formule de calcul du taux d'exonération
        # Règle d'arrondi : 4 décimales la plus proche
        taux_exoneration = round_(taux * min_(1, seuil / pente * max_(plafond * ratio_smic_salaire - 1, 0)), 4)

        return eligibilite_lodeom_competitivite * taux_exoneration * assiette_allegement

    def formula_2009_05_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite = individu('eligibilite_lodeom_competitivite', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite

        # Extraction des variables d'intérêt
        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
        # Distinction suivant l'effectif de l'entreprise
        # Valorisation des paramètres d'intérêt
        # Moins de 11 salariés
        seuil_moins_de_11_salaries = lodeom_competitivite.seuil_entreprises_de_moins_de_11_salaries
        seuil_intermediaire_moins_de_11_salaries = lodeom_competitivite.seuil_median_entreprises_de_moins_de_11_salaries
        pente_moins_de_11_salaries = lodeom_competitivite.pente_entreprises_de_moins_de_11_salaries
        plafond_moins_de_11_salaries = lodeom_competitivite.plafond_entreprises_de_moins_de_11_salaries
        # Plus de 11 salariés
        seuil_11_salaries_et_plus = lodeom_competitivite.seuil_entreprises_de_11_salaries_et_plus
        pente_11_salaries_et_plus = lodeom_competitivite.pente_entreprises_de_11_salaries_et_plus
        plafond_11_salaries_et_plus = lodeom_competitivite.plafond_entreprises_de_11_salaries_et_plus
        # Communs
        taux = lodeom_competitivite.taux

        # Calculs moins de 11 salariés
        # Calcul du taux d'exonération entre le seuil intermédiaire et le plafond
        taux_exoneration_intermediaire_plafond = round_(taux * min_(1, seuil_moins_de_11_salaries / pente_moins_de_11_salaries * max_(plafond_moins_de_11_salaries * ratio_smic_salaire - 1, 0)), 4)
        # Calcul des montants d'exonération
        montant_exoneration_moins_de_11_salaries = np.where((assiette_allegement / smic_proratise >= seuil_moins_de_11_salaries), taux * seuil_moins_de_11_salaries * smic_proratise, taux * assiette_allegement)
        montant_exoneration_moins_de_11_salaries = np.where((assiette_allegement / smic_proratise >= seuil_intermediaire_moins_de_11_salaries), taux_exoneration_intermediaire_plafond * assiette_allegement, montant_exoneration_moins_de_11_salaries)

        # Calculs plus de 11 salariés
        # Calcul du taux d'exonération
        taux_exoneration = round_(taux * min_(1, seuil_11_salaries_et_plus / pente_11_salaries_et_plus * max_(plafond_11_salaries_et_plus * ratio_smic_salaire - 1, 0)), 4)
        # Calcul du montant d'exonération
        montant_exoneration_11_salaries_et_plus = taux_exoneration * assiette_allegement

        # Calcul du montant total d'exonération
        montant_exoneration = np.where(effectif_entreprise_drom < 11, montant_exoneration_moins_de_11_salaries, montant_exoneration_11_salaries_et_plus)

        return eligibilite_lodeom_competitivite * montant_exoneration

    def formula_2019_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite = individu('eligibilite_lodeom_competitivite', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite

        # A partir du 1er janvier 2019
        # Définition de la petite entreprise
        petite_entreprise = (effectif_entreprise_drom < 50)
        # Valorisation des paramèetres d'intérêt
        seuil = lodeom_competitivite.seuil
        plafond = lodeom_competitivite.plafond
        tx_max = (
            lodeom_competitivite.entreprises_de_50_salaries_et_plus * not_(petite_entreprise)
            + lodeom_competitivite.entreprises_de_moins_de_50_salaries * petite_entreprise
            )
        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)

        # Formule de calcul du taux d'exonération
        # Règle d'arrondi : 4 décimales la plus proche
        taux_exoneration = round_(tx_max * min_(1, seuil / (plafond - seuil) * max_(plafond * ratio_smic_salaire - 1, 0)), 4)

        return eligibilite_lodeom_competitivite * taux_exoneration * assiette_allegement


# Types de secteurs d'activité de l'employeur
# Peut peut-être être fusionné avec TypeSecteurActivite dans openfisca_france.model.base
class TypesSecteurActivite199UndeciesBCGI(Enum):
    __order__ = 'non_renseigne commerce tabac cafes_restaurants conseil_expertise education sante_social immobilier_location navigation services_entreprises loisirs associations poste autre_secteur'
    non_renseigne = 'Non renseigné'
    commerce = 'Commerce et réparation automobile'
    tabac = 'Tabac'
    cafes_restaurants = 'Cafés-restaurants'
    conseil_expertise = 'Conseils et expertise'
    education = 'Education'
    sante_social = 'Santé-social'
    immobilier_location = 'Activités immobilières et les activités de location de meublés de tourisme'
    navigation = 'Navigation de croisière, location sans opérateurs'
    services_entreprises = "Services aux entreprises à l'exception de la maintenance, des activités de nettoyage et de conditionnement et des centres d'appel"
    loisirs = "Loisirs sportifs et culturels à l'exception des jeux de hasard et de la production audiovisuelle et cinématographique"
    associations = 'Associations'
    poste = 'Activités postales'
    autre_secteur = 'Autre secteur'


# Secteur d'activité de l'employeur
class secteur_activite_employeur_199undeciesBCGI(Variable):
    value_type = Enum
    possible_values = TypesSecteurActivite199UndeciesBCGI
    default_value = TypesSecteurActivite199UndeciesBCGI.non_renseigne
    entity = Individu
    label = "Secteurs d'activité définissant l'éligibilité à la réduction d'impôt au titre d'investissements réalisés en outre-mer"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041524650'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


# Définition de la classe d'éligibilité à la réduction d'impôt révue à l'article 199 undecies B du CGI
class eligibilite_199undeciesBCGI(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité à la réduction d'impôt révue à l'article 199 undecies B du CGI"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041524650'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2009_01_01(individu, period):
        # Extraction des variables d'intérêt
        secteur_activite_employeur_199undeciesBCGI = individu('secteur_activite_employeur_199undeciesBCGI', period)
        depcom_entreprise = individu('depcom_entreprise', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion, à Mayotte, à Saint-Pierre et Miquelon, en Nouvelle-Calédonie, En Polynésie Française, à Saint Martin, à Saint Barthélémy, à Wallis-et-Futuna, dans les Terres australes et antarctiques françaises
        dep_eligible = np.array([depcom_cell[:3] in ['971', '972', '973', '974', '975', '976', '977', '978', '984', '986', '987', '988'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974', '975', '976', '977', '978', '984', '986', '987', '988'] for depcom_cell in depcom_entreprise])

        # Critère sur le secteur d'activité
        secteur_eligible = secteur_activite_employeur_199undeciesBCGI == TypesSecteurActivite199UndeciesBCGI.autre_secteur

        # Définition de l'éligibilite
        eligibilite = dep_eligible * secteur_eligible

        return eligibilite

    def formula_2014_07_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        secteur_activite_employeur_199undeciesBCGI = individu('secteur_activite_employeur_199undeciesBCGI', period)
        depcom_entreprise = individu('depcom_entreprise', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion, à Mayotte, à Saint-Pierre et Miquelon, en Nouvelle-Calédonie, En Polynésie Française, à Saint Martin, à Saint Barthélémy, à Wallis-et-Futuna, dans les Terres australes et antarctiques françaises
        dep_eligible = np.array([depcom_cell[:3] in ['971', '972', '973', '974', '975', '976', '977', '978', '984', '986', '987', '988'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974', '975', '976', '977', '978', '984', '986', '987', '988'] for depcom_cell in depcom_entreprise])

        # Critère sur le secteur d'activité
        secteur_eligible = secteur_activite_employeur_199undeciesBCGI == TypesSecteurActivite199UndeciesBCGI.autre_secteur

        # Définition de l'éligibilite
        eligibilite = dep_eligible * secteur_eligible
        # A partir du 1er juillet 2014, il y a un critère additionnel sur le chiffre d'affaire dans les départements d'outre-mer
        # Définition de l'appartenance à un département d'outre-mer (Guadeloupe, la Guyane, la Martinique et la Réunion, à Mayotte)
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974', '976'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974', '976'] for depcom_cell in depcom_entreprise])
        # Extraction de la variable d'intérêt
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        # Extraction des paramètres d'intérêt
        seuil = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.reduction_impot_199undeciesBCGI.seuil
        # Critère sur le chiffre d'affaires
        chiffre_affaires_inferieur_seuil = entreprise_chiffre_affaire < seuil
        # Eligibilité
        eligibilite = not_(dep_drom) * eligibilite + dep_drom * chiffre_affaires_inferieur_seuil

        return eligibilite


# Définition de la classe d'éligibilité au dispositif compétitivité
class eligibilite_lodeom_competitivite_renforcee(Variable):
    value_type = bool
    entity = Individu
    label = 'Eligibilité au dispositif compétitivité renforcée de LODEOM'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042683758'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # Sont concernés :
    # - les employeurs de moins de 250 salariés au chiffre d'affaire annuel inférieur à 50 millions d'euros
    # - les employeurs des secteurs du bâtiment, des travaux publics, des transports aériens pour certaines liaisons et ceux assurant la desserte maritime entre certains points

    def formula_2009_01_01(individu, period):
        # Extraction des variables d'intérêt
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)
        depcom_entreprise = individu('depcom_entreprise', period)
        eligibilite_199undeciesBCGI = individu('eligibilite_199undeciesBCGI', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_250_salaries = effectif_entreprise_drom < 250
        chiffre_affaire_inferieur_50m = entreprise_chiffre_affaire < 50000000
        # Définition de l'appartenance à certains secteurs
        secteur_divers_eligible = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.divers
        beneficiaire_perfectionnement_actif = perfectionnement_actif == TypesPerfectionnementActif.beneficiaire
        # Définition de l'éligibilité
        eligibilite = dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_divers_eligible + beneficiaire_perfectionnement_actif)

        # Ajout de l'éligibilité si éligible au 199 undecies B
        eligibilite += dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * eligibilite_199undeciesBCGI

        return eligibilite

    def formula_2019_01_01(individu, period):
        # Extraction des variables d'intérêt
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)
        depcom_entreprise = individu('depcom_entreprise', period)
        eligibilite_199undeciesBCGI = individu('eligibilite_199undeciesBCGI', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_250_salaries = effectif_entreprise_drom < 250
        chiffre_affaire_inferieur_50m = entreprise_chiffre_affaire < 50000000
        # Définition de l'appartenance à certains secteurs
        secteur_divers_eligible = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.divers
        beneficiaire_perfectionnement_actif = perfectionnement_actif == TypesPerfectionnementActif.beneficiaire
        # Définition de l'éligibilité
        eligibilite = dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_divers_eligible + beneficiaire_perfectionnement_actif)

        # Appartenance au département de la Guyane
        dep_guyane = np.array([depcom_cell[:3] == '973' if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] == '973' for depcom_cell in depcom_entreprise])
        # Appartenance au secteur "comptabilité-conseil"
        secteur_compta_conseil = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.compta_conseil
        # Ajout de l'éligibilité
        eligibilite += dep_guyane * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_compta_conseil + eligibilite_199undeciesBCGI)

        return eligibilite

    def formula_2020_01_01(individu, period):
        # Extraction des variables d'intérêt
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)
        depcom_entreprise = individu('depcom_entreprise', period)
        eligibilite_199undeciesBCGI = individu('eligibilite_199undeciesBCGI', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_250_salaries = effectif_entreprise_drom < 250
        chiffre_affaire_inferieur_50m = entreprise_chiffre_affaire < 50000000
        # Définition de l'appartenance à certains secteurs
        secteur_divers_eligible = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.divers
        beneficiaire_perfectionnement_actif = perfectionnement_actif == TypesPerfectionnementActif.beneficiaire
        # Définition de l'éligibilité
        eligibilite = dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_divers_eligible + beneficiaire_perfectionnement_actif)

        # Appartenance au département de la Guyane
        dep_guyane = np.array([depcom_cell[:3] == '973' if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] == '973' for depcom_cell in depcom_entreprise])
        # Appartenance au secteur "comptabilité-conseil"
        secteur_compta_conseil = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.compta_conseil
        # Appartenance au secteur de la presse
        secteur_presse = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.presse
        # Ajout du secteur de la presse
        eligibilite += dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_presse + dep_guyane * (secteur_compta_conseil + eligibilite_199undeciesBCGI))

        return eligibilite

    def formula_2021_01_01(individu, period):
        # Extraction des variables d'intérêt
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        secteur_activite_employeur_lodeom = individu('secteur_activite_employeur_lodeom', period)
        depcom_entreprise = individu('depcom_entreprise', period)
        eligibilite_199undeciesBCGI = individu('eligibilite_199undeciesBCGI', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_250_salaries = effectif_entreprise_drom < 250
        chiffre_affaire_inferieur_50m = entreprise_chiffre_affaire < 50000000
        # Définition de l'appartenance à certains secteurs
        secteur_divers_eligible = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.divers
        beneficiaire_perfectionnement_actif = perfectionnement_actif == TypesPerfectionnementActif.beneficiaire
        # Définition de l'éligibilité
        eligibilite = dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_divers_eligible + beneficiaire_perfectionnement_actif)

        # Appartenance au département de la Guyane
        dep_guyane = np.array([depcom_cell[:3] == '973' if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] == '973' for depcom_cell in depcom_entreprise])
        # Appartenance au secteur "comptabilité-conseil"
        secteur_compta_conseil = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.compta_conseil
        # Appartenance au secteur audiovisuel
        secteur_audiovisuel = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.audiovisuel
        # Appartenance au secteur de la presse
        secteur_presse = secteur_activite_employeur_lodeom == TypesSecteurActiviteLODEOM.presse
        # Ajout du secteur audiovisuel parmi les secteurs éligibles
        eligibilite += dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (secteur_audiovisuel + secteur_presse + dep_guyane * (secteur_compta_conseil + eligibilite_199undeciesBCGI))

        return eligibilite


# /!\ Revoir si la formule est bonne pour toutes les dates depuis 2009
# Définition de la classe définissant le montant associé au dispositif de compétitivité renforcée
class exoneration_lodeom_competitivite_renforcee(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'exonération associé au dispositif compétitivité renforcée de LODEOM"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041404691'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2009_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite_renforcee = individu('eligibilite_lodeom_competitivite_renforcee', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite_renforcee = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite_renforcee

        # Valorisation des paramètres d'intérêt
        seuil = lodeom_competitivite_renforcee.seuil
        plafond = lodeom_competitivite_renforcee.plafond
        taux = lodeom_competitivite_renforcee.taux

        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)

        # Formule de calcul du taux d'exonération
        # Règle d'arrondi : 4 décimales la plus proche
        taux_exoneration = round_(taux * min_(1, seuil / (plafond - seuil) * max_(plafond * ratio_smic_salaire - 1, 0)), 4)

        return eligibilite_lodeom_competitivite_renforcee * taux_exoneration * assiette_allegement

    def formula_2009_05_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite_renforcee = individu('eligibilite_lodeom_competitivite_renforcee', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite_renforcee = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite_renforcee

        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
        # Valorisation des paramètres
        seuil = lodeom_competitivite_renforcee.seuil
        seuil_intermediaire = lodeom_competitivite_renforcee.seuil_intermediaire
        plafond = lodeom_competitivite_renforcee.plafond
        taux = lodeom_competitivite_renforcee.taux
        # Calcul du taux d'exonération applicable entre le seuil intermédiaire et le plafond
        taux_exoneration_intermediaire_plafond = round_(taux * min_(1, seuil / (plafond - seuil_intermediaire) * max_(plafond * ratio_smic_salaire - 1, 0)), 4)
        # Calcul du montant d'exonération
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil), taux * seuil * smic_proratise, taux * assiette_allegement)
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil_intermediaire), taux_exoneration_intermediaire_plafond * assiette_allegement, montant_exoneration)

        return eligibilite_lodeom_competitivite_renforcee * montant_exoneration

    def formula_2014_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite_renforcee = individu('eligibilite_lodeom_competitivite_renforcee', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite_renforcee = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite_renforcee

        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
        # Valorisation des paramètres
        seuil = lodeom_competitivite_renforcee.seuil
        seuil_intermediaire = lodeom_competitivite_renforcee.seuil_intermediaire
        plafond = lodeom_competitivite_renforcee.plafond
        taux = lodeom_competitivite_renforcee.taux
        # Calcul du taux d'exonération applicable entre le seuil intermédiaire et le plafond
        taux_exoneration_intermediaire_plafond = round_(taux * min_(1, seuil * max_(plafond * ratio_smic_salaire - 1, 0)), 4)
        # Calcul du montant d'exonération
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil), taux * seuil * smic_proratise, taux * assiette_allegement)
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil_intermediaire), taux_exoneration_intermediaire_plafond * assiette_allegement, montant_exoneration)

        return eligibilite_lodeom_competitivite_renforcee * montant_exoneration

    def formula_2019_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_competitivite_renforcee = individu('eligibilite_lodeom_competitivite_renforcee', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Extraction des paramètres d'intérêt
        lodeom_competitivite_renforcee = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_competitivite_renforcee
        # Extraction des variables d'intérêt
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        # Définition de la petite entreprise
        petite_entreprise = (effectif_entreprise_drom < 50)
        # Valorisation des paramètres d'intérêt
        seuil = lodeom_competitivite_renforcee.seuil
        plafond = lodeom_competitivite_renforcee.plafond
        tx_max = (
            lodeom_competitivite_renforcee.entreprises_de_50_salaries_et_plus * not_(petite_entreprise)
            + lodeom_competitivite_renforcee.entreprises_de_moins_de_50_salaries * petite_entreprise
            )
        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)

        # Formule de calcul du taux d'exonération
        # Règle d'arrondi : 4 décimales la plus proche
        taux_exoneration = round_(tx_max * min_(1, seuil / (plafond - seuil) * max_(plafond * ratio_smic_salaire - 1, 0)), 4)

        return eligibilite_lodeom_competitivite_renforcee * taux_exoneration * assiette_allegement


# Définition des types d'occupation de salariés
class TypesOccupationSalarieLODEOM(Enum):
    __order__ = 'non_renseigne telecommunication informatique infographie conception_objets_connectes autre_occupation'
    non_renseigne = 'Non renseignée'
    telecommunication = 'Télécommunication'
    informatique = 'Informatique'
    infographie = 'Infographie'
    conception_objets_connectes = "Conception d'objets connectés"
    autre_occupation = 'Autre occupation'


# Définition de l'occupation d'un poste pour le salarié (découpée dans le cadre de LODEOM)
class occupation_salarie_lodeom(Variable):
    value_type = Enum
    possible_values = TypesOccupationSalarieLODEOM
    default_value = TypesOccupationSalarieLODEOM.non_renseigne
    entity = Individu
    label = 'Occupation du salarié (découpée pour être compatible avec les activités éligibles à LODEOM innovation et croissance)'
    reference = ''
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


# Définition de l'éligibilité à LODEOM innovation et croissance
class eligibilite_lodeom_innovation_croissance(Variable):
    value_type = bool
    entity = Individu
    label = 'Eligibilité au dispositif innovation et croissance de LODEOM'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042683758'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # Sont concernés

    def formula(individu, period):
        # Extraction des variables d'intérêt
        depcom_entreprise = individu('depcom_entreprise', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        entreprise_chiffre_affaire = individu('entreprise_chiffre_affaire', period)
        occupation_salarie_lodeom = individu('occupation_salarie_lodeom', period)

        # Définition de l'appartenance à la Guadeloupe, la Guyane, la Martinique et la Réunion
        # dep_drom = depcom_entreprise[:3] in ['971', '972', '973', '974']
        dep_drom = np.array([depcom_cell[:3] in ['971', '972', '973', '974'] if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8')[:3] in ['971', '972', '973', '974'] for depcom_cell in depcom_entreprise])

        # Définition de l'éligibilité suivant l'effectif de l'entreprise
        effectif_moins_250_salaries = effectif_entreprise_drom < 250
        chiffre_affaire_inferieur_50m = entreprise_chiffre_affaire < 50000000
        # Définition de l'appartenance à certaines occupations
        occupation_telecommunication = occupation_salarie_lodeom == TypesOccupationSalarieLODEOM.telecommunication
        occupation_informatique = occupation_salarie_lodeom == TypesOccupationSalarieLODEOM.informatique
        occupation_infographie = occupation_salarie_lodeom == TypesOccupationSalarieLODEOM.infographie
        occupation_conception_objets_connectes = occupation_salarie_lodeom == TypesOccupationSalarieLODEOM.conception_objets_connectes

        # Définition de l'éligibilité
        eligibilite = dep_drom * effectif_moins_250_salaries * chiffre_affaire_inferieur_50m * (occupation_telecommunication + occupation_informatique + occupation_infographie + occupation_conception_objets_connectes)

        return eligibilite


# Définition du montant d'exonération associé à LODEOM innovation et croissance
class exoneration_lodeom_innovation_croissance(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'exonération associé au dispositif innovation et croissance de LODEOM"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041404691'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):
        # Extraction des variables d'intérêt
        eligibilite_lodeom_innovation_croissance = individu('eligibilite_lodeom_innovation_croissance', period)
        effectif_entreprise_drom = individu('effectif_entreprise_drom', period)
        smic_proratise = individu('smic_proratise', period)
        assiette_allegement = individu('assiette_allegement', period)
        # Définition de la petite entreprise
        petite_entreprise = (effectif_entreprise_drom < 50)
        # Extraction des paramètres d'intérêt
        lodeom_innovation_croissance = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.exonerations_geo_cotis.lodeom_innovation_croissance
        seuil = lodeom_innovation_croissance.seuil
        seuil_intermediaire = lodeom_innovation_croissance.seuil_intermediaire
        plafond = lodeom_innovation_croissance.plafond
        tx_max = (
            lodeom_innovation_croissance.entreprises_de_50_salaries_et_plus * not_(petite_entreprise)
            + lodeom_innovation_croissance.entreprises_de_moins_de_50_salaries * petite_entreprise
            )
        # Ratio smic/salaire
        ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)

        # Formule de calcul du taux d'exonération
        # Règle d'arrondi : 4 décimales la plus proche
        # Calcul du taux d'exonération entre le seuil et le seuil intermédiaire
        taux_exoneration_seuil_intermediaire = round_(tx_max * seuil / seuil_intermediaire, 4)

        # Taux d'exonération entre le seuil intermédiaire et le plafond
        taux_exoneration = round_(taux_exoneration_seuil_intermediaire * min_(1, seuil_intermediaire / (plafond - seuil_intermediaire) * max_(plafond * ratio_smic_salaire - 1, 0)), 4)

        # Calculant du montant d'exonération
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil), tx_max * seuil * smic_proratise, tx_max * assiette_allegement)
        montant_exoneration = np.where((assiette_allegement / smic_proratise >= seuil_intermediaire), taux_exoneration * assiette_allegement, montant_exoneration)

        return eligibilite_lodeom_innovation_croissance * montant_exoneration


# Définition du montant d'exonération LODEOM quelque soit le dispositif
class exoneration_lodeom(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'exonération LODEOM"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041404691'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        # Extraction des différents allègements LODEOM
        exoneration_lodeom_competitivite = individu('exoneration_lodeom_competitivite', period)
        exoneration_lodeom_competitivite_renforcee = individu('exoneration_lodeom_competitivite_renforcee', period)
        exoneration_lodeom_innovation_croissance = individu('exoneration_lodeom_innovation_croissance', period)

        # Hiérachie des barèmes les plus favorables
        # exoneration_lodeom_innovation_croissance > exoneration_lodeom_competitivite_renforcee > exoneration_lodeom_competitivite
        return exoneration_lodeom_innovation_croissance + not_(exoneration_lodeom_innovation_croissance) * exoneration_lodeom_competitivite_renforcee + not_(exoneration_lodeom_innovation_croissance + exoneration_lodeom_competitivite_renforcee) * exoneration_lodeom_competitivite
