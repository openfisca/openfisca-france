import logging

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import montant_csg_crds


log = logging.getLogger(__name__)


# TODO: prise_en_charge_employeur_retraite_supplementaire à la CSG/CRDS et au forfait social

# Salariés


class assiette_csg_abattue(Variable):
    value_type = float
    label = 'Assiette CSG - CRDS'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042683657'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        '''
        Assiette CSG - CRDS
            - 01/07/2022 : Ajout de la PPV à partir du 1er août 2022
        '''
        primes_salaires_non_exonerees = individu('primes_salaires_non_exonerees', period)
        prime_partage_valeur_exoneree = individu('prime_partage_valeur_exoneree', period, options=[DIVIDE])

        salaire_de_base = individu('salaire_de_base', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        # indemnites_journalieres_maladie = individu('indemnites_journalieres_maladie', period)
        # TODO: mettre à part ?
        indemnite_residence = individu('indemnite_residence', period)
        indemnite_compensatrice_csg = individu('indemnite_compensatrice_csg', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        hsup = individu('hsup', period)
        remuneration_principale = individu('remuneration_principale', period)
        stage_gratification_reintegration = individu('stage_gratification_reintegration', period)
        indemnite_fin_contrat = individu('indemnite_fin_contrat', period)
        avantage_en_nature = individu('avantage_en_nature', period)

        return (
            + indemnite_fin_contrat
            + indemnite_residence
            + indemnite_compensatrice_csg
            + primes_fonction_publique
            + primes_salaires_non_exonerees
            + prime_partage_valeur_exoneree
            + remuneration_principale
            + salaire_de_base
            + stage_gratification_reintegration
            + supplement_familial_traitement
            + avantage_en_nature
            - hsup
            )


class assiette_csg_non_abattue(Variable):
    value_type = float
    label = 'Assiette CSG - CRDS'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    '''
    L'exclusion des contributions employeur aux contrats de prévoyance obligatoire n'est pas facile à dater, car elle a fait l'objet de différentes
    jurisprudences de la Cour de cassation, dans un sens comme dans l'autre, et de façon assez ancienne.
    voir par exemple Cour de Cassation, Chambre civile 2, du 23 novembre 2006, 05-11.364 : normalement, à cette date et par cette jurisprudence, les primes d'assurances
    prévoyance versées dans le cadre d'une obligation légale et n'acquérant pas de droits complémentaires au salarié sont exonérés de CSG.
    Cependant on retient la date de 2018, car la lecture de l'article L136-2 du CSS, ainsi que celle du cinquième alinéa de l'article L242-1 du CSS, ne font plus
    explicitement mention des contrats de prévoyance à cette date.
    Auparavant, et pour rester cohérent avec certains fichiers de test (notamment tests "fiches de paie"), on continue à inclure la prévoyance obligatoire
    (en particulier celle des cadres, qui est une obligation légale générale au-delà des conventions collectives) dans l'assiette de CSG.
    '''

    def formula_2018_01_01(individu, period, parameters):
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options = [ADD])
        prevoyance_complementaire_employeur = individu('prevoyance_complementaire_employeur', period, options = [ADD])
        return (
            prevoyance_complementaire_employeur
            - complementaire_sante_employeur
            )

    def formula(individu, period, parameters):
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options = [ADD])
        prevoyance_complementaire_employeur = individu('prevoyance_complementaire_employeur', period, options = [ADD])
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period, options = [ADD])

        # TODO + indemnites_journalieres_maladie,
        return (
            - prevoyance_obligatoire_cadre
            + prevoyance_complementaire_employeur
            - complementaire_sante_employeur
            )


class csg_deductible_salaire(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = 'CSG déductible sur les salaires'
    reference = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073189/LEGISCTA000006173055/#LEGIARTI000042340733'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_csg_abattue = individu('assiette_csg_abattue', period)
        assiette_csg_non_abattue = individu('assiette_csg_non_abattue', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)

        csg = parameters(period).prelevements_sociaux.contributions_sociales.csg
        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            law_node = csg.activite.deductible,
            plafond_securite_sociale = plafond_securite_sociale,
            )
        return montant_csg


class csg_imposable_salaire(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = 'CSG imposables sur les salaires'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_csg_abattue = individu('assiette_csg_abattue', period)
        assiette_csg_non_abattue = individu('assiette_csg_non_abattue', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        parameters = parameters(period)

        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.activite.imposable,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return montant_csg


class crds_salaire(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = 'CRDS sur les salaires'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_csg_abattue = individu('assiette_csg_abattue', period)
        assiette_csg_non_abattue = individu('assiette_csg_non_abattue', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)

        law = parameters(period)

        montant_crds = montant_csg_crds(
            law_node = law.prelevements_sociaux.contributions_sociales.crds.activite,
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return montant_crds


class forfait_social(Variable):
    value_type = float
    entity = Individu
    label = 'Forfait social'
    definition_period = MONTH
    calculate_output = calculate_output_add
    set_input = set_input_divide_by_period

    # les contributions destinées au financement des prestations de prévoyance complémentaire versées
    # au bénéfice de leurs salariés, anciens salariés et de leurs ayants droit (entreprises à partir de 10 salariés),
    # la réserve spéciale de participation dans les sociétés coopératives ouvrières de production (Scop).

    def formula_2009_01_01(individu, period, parameters):
        prise_en_charge_employeur_retraite_complementaire = individu('prise_en_charge_employeur_retraite_complementaire', period, options = [ADD])
        parametres = parameters(period).prelevements_sociaux.contributions_assises_specifiquement_accessoires_salaire.forfait_social
        taux_plein = parametres.taux_plein
        assiette_taux_plein = prise_en_charge_employeur_retraite_complementaire  # TODO: compléter l'assiette

        return - assiette_taux_plein * taux_plein

    def formula_2012_08_01(individu, period, parameters):
        prise_en_charge_employeur_retraite_complementaire = individu('prise_en_charge_employeur_retraite_complementaire', period, options = [ADD])
        parametres = parameters(period).prelevements_sociaux.contributions_assises_specifiquement_accessoires_salaire.forfait_social
        taux_plein = parametres.taux_plein
        assiette_taux_plein = prise_en_charge_employeur_retraite_complementaire  # TODO: compléter l'assiette

        # Les cotisations de prévoyance complémentaire qui rentrent en compte dans l'assiette du taux réduit
        # ne concernent que les entreprises de 10 ou 11 employés et plus
        # https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/le-forfait-social/le-forfait-social-au-taux-de-8.html
        seuil_effectif_taux_reduit = parametres.seuil_effectif_prevoyance_complementaire
        prevoyance_complementaire_employeur = individu('prevoyance_complementaire_employeur', period, options = [ADD])
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period, options = [ADD])
        effectif_entreprise = individu('effectif_entreprise', period)
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options = [ADD])
        taux_reduit = parametres.taux_reduit_1  # TODO taux_reduit_2 in 2016
        assiette_taux_reduit = (
            - prevoyance_obligatoire_cadre + prevoyance_complementaire_employeur
            - complementaire_sante_employeur
            ) * (effectif_entreprise >= seuil_effectif_taux_reduit)

        return - (
            assiette_taux_plein * taux_plein + assiette_taux_reduit * taux_reduit
            )

    def formula_2022_07_01(individu, period, parameters):
        # Seule la PPV pérenne est sousmise au forfait social, et cela intégralement
        prime_partage_valeur = individu('prime_partage_valeur', period, options=[DIVIDE])

        prise_en_charge_employeur_retraite_complementaire = individu('prise_en_charge_employeur_retraite_complementaire', period, options=[ADD])
        effectif_entreprise = individu('effectif_entreprise', period)
        parametres = parameters(period).prelevements_sociaux.contributions_assises_specifiquement_accessoires_salaire.forfait_social
        taux_plein = parametres.taux_plein
        # TODO : faire ça propre ! Il faut externaliser le paramètre.
        prime_partage_valeur_a_integrer = prime_partage_valeur * (
            effectif_entreprise >= 250
            )
        assiette_taux_plein = (
            prise_en_charge_employeur_retraite_complementaire  # TODO: compléter l'assiette
            + prime_partage_valeur_a_integrer
            )

        # Les cotisations de prévoyance complémentaire qui rentrent en compte dans l'assiette du taux réduit
        # ne concernent que les entreprises de 10 ou 11 employés et plus
        # https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/le-forfait-social/le-forfait-social-au-taux-de-8.html
        seuil_effectif_taux_reduit = parametres.seuil_effectif_prevoyance_complementaire
        prevoyance_complementaire_employeur = individu('prevoyance_complementaire_employeur', period, options=[ADD])
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period, options = [ADD])

        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options=[ADD])
        taux_reduit = parametres.taux_reduit_1  # TODO taux_reduit_2 in 2016

        assiette_taux_reduit = (
            - prevoyance_obligatoire_cadre + prevoyance_complementaire_employeur
            - complementaire_sante_employeur
            ) * (effectif_entreprise >= seuil_effectif_taux_reduit)

        return -(assiette_taux_plein * taux_plein + assiette_taux_reduit * taux_reduit)


class salaire_imposable(Variable):
    value_type = float
    unit = 'currency'
    cerfa_field = {  # (f1aj, f1bj, f1cj, f1dj, f1ej)
        0: '1AJ',
        1: '1BJ',
        2: '1CJ',
        3: '1DJ',
        4: '1EJ',
        }
    entity = Individu
    label = 'Salaires imposables'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042683657'
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period):
        '''
        Salaires imposables
            - 01/07/2022 : Ajout PPV : prime_partage_valeur
        '''
        salaire_de_base = individu('salaire_de_base', period)
        primes_salaires_non_exonerees = individu('primes_salaires_non_exonerees', period)
        prime_partage_valeur_exoneree = individu('prime_partage_valeur_exoneree', period, options=[DIVIDE])

        primes_fonction_publique = individu('primes_fonction_publique', period)
        indemnite_residence = individu('indemnite_residence', period)
        indemnite_compensatrice_csg = individu('indemnite_compensatrice_csg', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        csg_deductible_salaire = individu('csg_deductible_salaire', period)
        cotisations_salariales = individu('cotisations_salariales', period)
        remuneration_principale = individu('remuneration_principale', period)
        hsup = individu('hsup', period)
        indemnite_fin_contrat = individu('indemnite_fin_contrat', period)
        complementaire_sante_salarie = individu('complementaire_sante_salarie', period)

        return (
            salaire_de_base
            + primes_salaires_non_exonerees
            + prime_partage_valeur_exoneree
            + remuneration_principale
            + primes_fonction_publique
            + indemnite_residence
            + supplement_familial_traitement
            + csg_deductible_salaire
            + cotisations_salariales
            - hsup
            + indemnite_fin_contrat
            + complementaire_sante_salarie
            + indemnite_compensatrice_csg
            )


class salaire_net(Variable):
    value_type = float
    entity = Individu
    label = "Salaires nets d'après définition INSEE"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        salaire_imposable = individu('salaire_imposable', period)
        crds_salaire = individu('crds_salaire', period)
        csg_imposable_salaire = individu('csg_imposable_salaire', period)

        return salaire_imposable + crds_salaire + csg_imposable_salaire

    def formula_2019_01_01(individu, period, parameters):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        salaire_imposable = individu('salaire_imposable', period)
        crds_salaire = individu('crds_salaire', period)
        csg_imposable_salaire = individu('csg_imposable_salaire', period)
        prime_exceptionnelle_pouvoir_achat_exoneree = individu('prime_exceptionnelle_pouvoir_achat_exoneree', period, options = [DIVIDE])
        return salaire_imposable + crds_salaire + csg_imposable_salaire + prime_exceptionnelle_pouvoir_achat_exoneree

    def formula_2022_07_01(individu, period, parameters):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        salaire_imposable = individu('salaire_imposable', period)
        crds_salaire = individu('crds_salaire', period)
        csg_imposable_salaire = individu('csg_imposable_salaire', period)
        prime_partage_valeur_exoneree_exceptionnelle = individu(
            'prime_partage_valeur_exoneree_exceptionnelle',
            period,
            options=[DIVIDE],
            )
        return (
            salaire_imposable  # La prime pérenne est dans le salaire_imposable
            + crds_salaire
            + csg_imposable_salaire
            + prime_partage_valeur_exoneree_exceptionnelle
            )


class tehr(Variable):
    value_type = float
    entity = Individu
    label = 'Taxe exceptionnelle sur les hautes rémunérations (TEHR)'
    reference = [
        'Article 15 de la loi 2013-1278',
        'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000028402680/'
        ]
    calculate_output = calculate_output_divide
    definition_period = YEAR
    end = '2015-01-01'

    def formula(individu, period, parameters):
        salaire_de_base = individu('salaire_de_base', period, options = [ADD])  # TODO: check base
        bareme_tehr = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.tehr.tehr
        return -bareme_tehr.calc(salaire_de_base)


# Non salariés


class assiette_csg_crds_non_salarie(Variable):
    '''Assiette CSG des personnes non salariées'''
    value_type = float
    entity = Individu
    label = 'Assiette CSG des personnes non salariées'
    definition_period = YEAR

    def formula(individu, period):
        rpns_imposables = individu('rpns_imposables', period)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        profession_liberale = (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
        famille_independant = individu('famille_independant', period)
        retraite_complementaire_artisan_commercant = individu('retraite_complementaire_artisan_commercant', period)
        maladie_maternite_artisan_commercant = individu('maladie_maternite_artisan_commercant', period)
        vieillesse_artisan_commercant = individu('vieillesse_artisan_commercant', period)
        maladie_maternite_profession_liberale = individu('maladie_maternite_profession_liberale', period)
        vieillesse_profession_liberale = individu('vieillesse_profession_liberale', period)
        retraite_complementaire_profession_liberale = individu('retraite_complementaire_profession_liberale', period)   # noqa F841

        assiette_cotisation = (
            (artisan + commercant + profession_liberale) * rpns_imposables
            - (  # cotisations are négative
                (artisan + commercant) * (
                    famille_independant
                    + vieillesse_artisan_commercant
                    + maladie_maternite_artisan_commercant
                    + retraite_complementaire_artisan_commercant
                    )
                + profession_liberale * (
                    famille_independant
                    + maladie_maternite_profession_liberale
                    + vieillesse_profession_liberale
                    )
                )
            )
        return assiette_cotisation


class csg_imposable_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette CSG des personnes non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        assiette_csg_crds_non_salarie = individu('assiette_csg_crds_non_salarie', period)
        csg = parameters(period).prelevements_sociaux.contributions_sociales.csg.activite
        taux = csg.imposable.taux
        return - taux * assiette_csg_crds_non_salarie


class csg_deductible_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette CSG des personnes non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        assiette_csg_crds_non_salarie = individu('assiette_csg_crds_non_salarie', period)
        csg = parameters(period).prelevements_sociaux.contributions_sociales.csg.activite
        taux = csg.deductible.taux
        return - taux * assiette_csg_crds_non_salarie


class crds_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette CSG des personnes non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        assiette_csg_crds_non_salarie = individu('assiette_csg_crds_non_salarie', period)
        taux = parameters(period).prelevements_sociaux.contributions_sociales.crds.activite.taux
        return - taux * assiette_csg_crds_non_salarie


class revenus_non_salarie_nets(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus du travail non salariaux nets'
    definition_period = YEAR

    def formula(individu, period):
        rpns_imposables = individu('rpns_imposables', period)
        csg_imposable_non_salarie = individu('csg_imposable_non_salarie', period)
        crds_non_salarie = individu('crds_non_salarie', period)
        microentreprise_i = individu.foyer_fiscal('microentreprise', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        microentreprise = sum(microentreprise_i)
        return rpns_imposables + csg_imposable_non_salarie + crds_non_salarie + microentreprise
