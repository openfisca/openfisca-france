import logging

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import (
    apply_bareme, apply_bareme_for_relevant_type_sal)


log = logging.getLogger(__name__)


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


class assiette_cotisations_sociales(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette des cotisations sociales des salaries'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_cotisations_sociales_prive = individu('assiette_cotisations_sociales_prive', period)
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)
        stage_gratification_reintegration = individu('stage_gratification_reintegration', period)
        return (
            (categorie_salarie != TypesCategorieSalarie.non_pertinent)
            * (assiette_cotisations_sociales_prive + remuneration_principale)
            + stage_gratification_reintegration
            )


class assiette_cotisations_sociales_prive(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette des cotisations sociales des salaries du prive'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        avantage_en_nature = individu('avantage_en_nature', period)
        hsup = individu('hsup', period)
        indemnites_compensatrices_conges_payes = individu('indemnites_compensatrices_conges_payes', period)
        indemnite_residence = individu('indemnite_residence', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        primes_salaires_non_exonerees = individu('primes_salaires_non_exonerees', period)
        indemnite_fin_contrat = individu('indemnite_fin_contrat', period)
        reintegration_titre_restaurant_employeur = individu(
            'reintegration_titre_restaurant_employeur', period
            )
        remuneration_apprenti = individu('remuneration_apprenti', period)
        salaire_de_base = individu('salaire_de_base', period)
        categorie_salarie = individu('categorie_salarie', period)

        assiette = (
            salaire_de_base
            + primes_salaires_non_exonerees
            + avantage_en_nature
            + hsup
            + indemnites_compensatrices_conges_payes
            + remuneration_apprenti
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire) * (
                indemnite_residence + primes_fonction_publique
                )
            + reintegration_titre_restaurant_employeur
            + indemnite_fin_contrat
            )

        return assiette


class indemnite_fin_contrat(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnité de fin de contrat'
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F40'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        salaire_de_base = individu('salaire_de_base', period)
        categorie_salarie = individu('categorie_salarie', period)
        apprenti = individu('apprenti', period)

        # Un grand nombre de conditions peuvent invalider cette indemnité, voir le lien ci-dessus.
        # A ajouter au fur et à mesure
        # Pour l'instant, cette variable d'entrée peut les remplacer
        # Elle est cependant fixée à False par défaut
        indemnite_fin_contrat_due = individu('indemnite_fin_contrat_due', period)
        taux = parameters(period).prelevements_sociaux.cotisations_securite_sociale_regime_general.indemnite_fin_contrat.taux

        result = (
            # CDD

            (contrat_de_travail_type == TypesContrat.cdd)

            # non fonction publique
            * (
                (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
                + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
                )
            * not_(apprenti)
            * indemnite_fin_contrat_due
            # 10% du brut
            * taux
            * salaire_de_base
            )

        return result


class reintegration_titre_restaurant_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Prise en charge de l'employeur des dépenses de cantine et des titres restaurants non exonérés de charges sociales"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        valeur_unitaire = individu('titre_restaurant_valeur_unitaire', period)
        volume = individu('titre_restaurant_volume', period)
        taux_employeur = individu('titre_restaurant_taux_employeur', period)
        cantines_titres_restaurants = parameters(period).prelevements_sociaux.cotisations_securite_sociale_regime_general.assiette.cantines_titres_restaurants

        taux_minimum_exoneration = cantines_titres_restaurants.taux_minimum_exoneration
        taux_maximum_exoneration = cantines_titres_restaurants.taux_maximum_exoneration
        seuil_prix_titre = cantines_titres_restaurants.seuil_prix_titre

        condition_exoneration_taux = (
            (taux_minimum_exoneration <= taux_employeur)
            * (taux_maximum_exoneration >= taux_employeur)
            )

        montant_reintegration = volume * (
            condition_exoneration_taux
            * max_(valeur_unitaire * taux_employeur - seuil_prix_titre, 0)
            + not_(condition_exoneration_taux)
            * valeur_unitaire
            * taux_employeur
            )

        return montant_reintegration


# Cotisations proprement dites


class penibilite(Variable):
    value_type = float
    entity = Individu
    label = "Les dépenses liées à l'utilisation du compte pénibilité par le salarié sont prises en charge par un fonds financé par l'employeur"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_01_01(individu, period, parameters):
        exposition_penibilite = individu('exposition_penibilite', period)
        TypesExpositionPenibilite = exposition_penibilite.possible_values
        multiplicateur = parameters(period).cotsoc.cotisations_employeur.prive_cadre.penibilite_multiplicateur_exposition_multiple

        cotisation_base = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'penibilite_base',
            variable_name = 'penibilite',
            )
        cotisation_additionnelle = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'penibilite_additionnelle',
            variable_name = 'penibilite',
            )

        cotisation = switch(
            exposition_penibilite,
            {
                TypesExpositionPenibilite.nulle: cotisation_base,
                TypesExpositionPenibilite.simple: cotisation_base + cotisation_additionnelle,
                TypesExpositionPenibilite.multiple: cotisation_base + cotisation_additionnelle * multiplicateur,
                }
            )

        return cotisation

    def formula_2018(individu, period, parameters):
        return individu.empty_array()


class accident_du_travail(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisations employeur accident du travail et maladie professionelle'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_1991(individu, period, parameters):    # TODO : rajouter formule pré-1991 : s'applique au salaire sous PSS uniquement
        assiette_cotisations_sociales = individu(
            'assiette_cotisations_sociales', period)
        taux_accident_travail = individu('taux_accident_travail', period)
        categorie_salarie = individu('categorie_salarie', period)
        assujetti = (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            )
        # TODO: ajouter contractuel du public salarié de moins d'un an ou à temps partiel
        return - assiette_cotisations_sociales * taux_accident_travail * assujetti


class agff_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation retraite AGFF tranche A (salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # AGFF: Association pour la gestion du fonds de financement (sous-entendu des départs entre 60 et 65 ans)

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'agff',
            variable_name = 'agff_salarie'
            )
        return cotisation


class agff_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation retraite AGFF tranche A (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # TODO: améliorer pour gérer mensuel/annuel

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu(
            'assiette_cotisations_sociales', period)
        categorie_salarie = individu('categorie_salarie', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)

        law = parameters(period)

        cotisation_non_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = 'agffnc',
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )

        cotisation_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = 'agffc',
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation_cadre + cotisation_non_cadre


class quotite_de_travail(Variable):
    value_type = float
    entity = Individu
    label = 'Quotité de travail'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO: gestion annuel/mensuel

    def formula(individu, period, parameters):
        contrat_de_travail = individu('contrat_de_travail', period)
        TypesContratDeTravail = contrat_de_travail.possible_values
        parameters = parameters(period)
        heures_temps_plein = parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
        forfait_jours_remuneres_volume = individu('forfait_jours_remuneres_volume', period)
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        return switch(
            contrat_de_travail,
            {
                TypesContratDeTravail.temps_plein: 1,
                TypesContratDeTravail.temps_partiel: (heures_remunerees_volume / heures_temps_plein),
                TypesContratDeTravail.forfait_jours_annee: (forfait_jours_remuneres_volume / 218),
                TypesContratDeTravail.sans_objet: 0
                }
            )


class agirc_gmp_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC pour la garantie minimale de points (GMP,  salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # TODO: gestion annuel/mensuel

    def formula(individu, period, parameters):
        agirc_salarie = individu('agirc_salarie', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        categorie_salarie = individu('categorie_salarie', period)
        quotite = individu('quotite_de_travail', period)

        cadre_cotisant = (
            (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            & (assiette_cotisations_sociales > 0)
            )

        gmp = parameters(period).prelevements_sociaux.regimes_complementaires_retraite_secteur_prive.gmp
        cotisation_forfaitaire_temps_plein = gmp.cotisation_forfaitaire_mensuelle.part_salariale
        cotisation_forfaitaire = cotisation_forfaitaire_temps_plein * quotite

        # Sachant:
        # - qu'il faut retourner un nombre négatif car c'est un prélèvement,
        # - que la cotisation agirc_salarie est négative car c'est un prélèvement,
        # - que la cotisation_forfaitaire est positive,
        # le montant de la gmp est cotisation_forfaitaire - (-agirc_salarie) soit:
        return - max_(cotisation_forfaitaire + agirc_salarie, 0) * cadre_cotisant


class agirc_gmp_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC pour la garantie minimale de points (GMP, employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # TODO: gestion annuel/mensuel

    def formula(individu, period, parameters):
        agirc_employeur = individu('agirc_employeur', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        categorie_salarie = individu('categorie_salarie', period)
        quotite = individu('quotite_de_travail', period)

        cadre_cotisant = (
            (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            & (assiette_cotisations_sociales > 0)
            )

        gmp = parameters(period).prelevements_sociaux.regimes_complementaires_retraite_secteur_prive.gmp
        cotisation_forfaitaire_temps_plein = gmp.cotisation_forfaitaire_mensuelle.part_patronale
        cotisation_forfaitaire = cotisation_forfaitaire_temps_plein * quotite

        # Sachant:
        # - qu'il faut retourner un nombre négatif car c'est un prélèvement,
        # - que la cotisation agirc_salarie est négative car c'est un prélèvement,
        # - que la cotisation_forfaitaire est positive,
        # le montant de la gmp est cotisation_forfaitaire - (-agirc_salarie) soit:
        return - max_(cotisation_forfaitaire + agirc_employeur, 0) * cadre_cotisant


class agirc_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC tranche B (salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'agirc',
            variable_name = 'agirc_salarie'
            )
        categorie_salarie = individu('categorie_salarie', period)
        return cotisation * (categorie_salarie == TypesCategorieSalarie.prive_cadre)


class agirc_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC tranche B (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'agirc',
            variable_name = 'agirc_employeur'
            )
        categorie_salarie = individu('categorie_salarie', period)
        return cotisation * (categorie_salarie == TypesCategorieSalarie.prive_cadre)


class agirc_arrco_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC-ARRCO (après la fusion, salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'agirc_arrco',
            variable_name = 'agirc_arrco_salarie'
            )
        return cotisation


class agirc_arrco_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation AGIRC-ARRCO (après la fusion, employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'agirc_arrco',
            variable_name = 'agirc_arrco_employeur'
            )
        return cotisation


class ags(Variable):
    value_type = float
    entity = Individu
    label = "Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'ags',
            variable_name = 'ags',
            )
        return cotisation


class apec_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Cotisations agence pour l'emploi des cadres (APEC,  salarié)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'apec',
            variable_name = 'apec_salarie',
            )
        return cotisation * (categorie_salarie == TypesCategorieSalarie.prive_cadre)  # TODO: check public notamment contractuel


class apec_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Cotisations Agenece pour l'emploi des cadres (APEC, employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'apec',
            variable_name = 'apec_employeur',
            )
        return cotisation  # TODO: check public notamment contractuel


class arrco_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation ARRCO tranche 1 (salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # TODO: check gestion mensuel/annuel

    def formula(individu, period, parameters):
        cotisation_minimale = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'arrco',
            variable_name = 'arrco_salarie',
            )
        arrco_tranche_a_taux_salarie = individu('arrco_tranche_a_taux_salarie', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period, options = [ADD])
        plafond_securite_sociale = individu('plafond_securite_sociale', period, options = [ADD])
        categorie_salarie = individu('categorie_salarie', period)

        # cas où l'entreprise applique un taux spécifique
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale)
            * arrco_tranche_a_taux_salarie
            )

        public = (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            )

        return (
            cotisation_minimale
            * (arrco_tranche_a_taux_salarie == 0)
            + cotisation_entreprise
            ) * public


class arrco_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation ARRCO tranche 1 (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'
    # TODO: check gestion mensuel/annuel

    def formula(individu, period, parameters):
        cotisation_minimale = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'arrco',
            variable_name = 'arrco_employeur',
            )
        arrco_tranche_a_taux_employeur = individu('arrco_tranche_a_taux_employeur', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period, options = [ADD])
        plafond_securite_sociale = individu('plafond_securite_sociale', period, options = [ADD])
        categorie_salarie = individu('categorie_salarie', period)

        # cas où l'entreprise applique un taux spécifique
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale)
            * arrco_tranche_a_taux_employeur
            )

        public = (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            )
        return (
            cotisation_minimale * (arrco_tranche_a_taux_employeur == 0) + cotisation_entreprise
            ) * public


class chomage_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation chômage (salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-09-30'

    def formula(individu, period, parameters):
        cotisation_chomage = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'chomage',
            variable_name = 'chomage_salarie',
            )
        asf = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'asf',
            variable_name = 'chomage_salarie',
            )

        return cotisation_chomage + asf


class chomage_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation chômage (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation_chomage = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'chomage',
            variable_name = 'chomage_employeur',
            )
        asf = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'asf',
            variable_name = 'chomage_salarie',
            )

        return cotisation_chomage + asf


class contribution_equilibre_general_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Contribution d'équilibre général (salarie)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'ceg',
            variable_name = 'contribution_equilibre_general_salarie',
            )
        return cotisation


class contribution_equilibre_general_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Contribution d'équilibre général (employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'ceg',
            variable_name = 'contribution_equilibre_general_employeur',
            )
        return cotisation


class contribution_solidarite_autonomie(Variable):
    value_type = float
    entity = Individu
    label = 'Contribution solidarité autonomie (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'csa',
            variable_name = 'contribution_solidarite_autonomie',
            )
        return cotisation


class contribution_equilibre_technique_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Contribution d'équilibre technique (salarie)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):

        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'cet2019',
            variable_name = 'contribution_equilibre_technique_salarie',
            )
        return cotisation * (assiette_cotisations_sociales > plafond_securite_sociale)


class contribution_equilibre_technique_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Contribution d'équilibre technique (employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):

        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'cet2019',
            variable_name = 'contribution_equilibre_technique_employeur',
            )
        return cotisation * (assiette_cotisations_sociales > plafond_securite_sociale)


class cotisation_exceptionnelle_temporaire_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation_exceptionnelle_temporaire (salarie)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'cet',
            variable_name = 'cotisation_exceptionnelle_temporaire_salarie',
            )
        return cotisation


class cotisation_exceptionnelle_temporaire_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation exceptionnelle temporaire (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2018-12-31'

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'cet',
            variable_name = 'cotisation_exceptionnelle_temporaire_employeur',
            )
        return cotisation


class famille(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation famille (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    # L'allègement général de cotisations de 2015 n'est pas dans le barème mais pris en compte dans
    # allegements.allegement_cotisation_allocations_familiales,
    # (sur la base du paramètre prelevements_sociaux/reductions_cotisations_sociales/allegement_cotisation_allocations_familiales/reduction)
    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'famille',
            variable_name = 'famille',
            )
        return cotisation


class mmid_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie (salarié)'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036390317/ et https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036679615'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2018(individu, period, parameters):
        '''
        La cotisation maladie (hors Alsace-Moselle) disparaît à partir du 1er janvier 2018
        '''
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)
        cotisation_regime_alsace_moselle = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'maladie_alsace_moselle',
            variable_name = 'mmid_salarie',
            )

        cotisation = salarie_regime_alsace_moselle * cotisation_regime_alsace_moselle

        return cotisation

    def formula(individu, period, parameters):
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)

        cotisation_regime_general = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'maladie',
            variable_name = 'mmid_salarie',
            )

        cotisation_regime_alsace_moselle = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'maladie_alsace_moselle',
            variable_name = 'mmid_salarie',
            )

        cotisation = cotisation_regime_general + salarie_regime_alsace_moselle * cotisation_regime_alsace_moselle

        return cotisation


class mmid_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie (employeur)'
    reference = 'https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/la-cotisation-maladie---maternit.html'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = 'mmid_employeur',
            )
        return cotisation


class mmida_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # Note: this formula is used only to check fiche_de_paie from memento

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = 'mmida_employeur',
            )
        contribution_solidarite_autonomie = individu('contribution_solidarite_autonomie', period)
        return cotisation + contribution_solidarite_autonomie


class plafond_securite_sociale(Variable):
    value_type = float
    entity = Individu
    label = 'Plafond de la sécurite sociale'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO gérer les plafonds mensuel, trimestriel, annuel

    def formula(individu, period, parameters):
        plafond_temps_plein = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_mensuel
        quotite = individu('quotite_de_travail', period)

        plafond = plafond_temps_plein * quotite

        # 2) Proratisation pour mois incomplet selon la méthode des 30èmes

        # Pour les salariés entrés ou sortis en cours de mois,
        # le plafond applicable est égal à autant de trentièmes du plafond mensuel
        # que le salarié a été présent de jours calendaires. Source urssaf.fr "L’assiette maximale"
        # calcul du nombre de jours calendaires de présence du salarié
        nombre_jours_calendaires = individu('nombre_jours_calendaires', period)
        plafond = plafond * (min_(nombre_jours_calendaires, 30) / 30)

        return plafond


class prevoyance_obligatoire_cadre(Variable):
    value_type = float
    entity = Individu
    label = 'Contribution de prévoyance obligatoire pour les cadres et assimilés'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    '''
    La prévoyance obligatoire des cadres n'est pas soumise à CSG/CRDS ni à cotisations sociales.
    '''
    # TODO: gérer le mode de recouvrement et l'aspect mensuel/annuel

    def formula(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        prevoyance_obligatoire_cadre_taux_employeur = individu(
            'prevoyance_obligatoire_cadre_taux_employeur', period)
        minimum = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.prevoyance.prevoyance_obligatoire
        taux = max_(minimum, prevoyance_obligatoire_cadre_taux_employeur)

        cotisation = - (
            (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            * min_(assiette_cotisations_sociales, plafond_securite_sociale)
            * taux
            )
        return cotisation


class prevoyance_complementaire_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Contributions de prévoyance complémentaire'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    '''
    On définit la prévoyance complémentaire par référence à la prévoyance obligatoire : c'est la partie non obligatoire des contributions de prévoyance totales versées par l'employeur.
    La prévoyance complémentaire est assujettie à CSG et au forfait social, ce qui n'est pas le cas de la prévoyance obligatoire.
    '''

    def formula(individu, period):
        prevoyance_totale = individu('prevoyance_employeur', period)
        prevoyance_obligatoire = individu('prevoyance_obligatoire_cadre', period)
        cotisation = - max_(
            0,
            prevoyance_totale
            - (-prevoyance_obligatoire)
            )

        return cotisation


class complementaire_sante_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Couverture complémentaire santé collective d'entreprise - part employeur"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038610242'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2016_01_01(individu, period, parameters):
        complementaire_sante_part_employeur = individu('complementaire_sante_part_employeur', period)
        minimum = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.complementaire_sante.part_employeur
        part_employeur = max_(complementaire_sante_part_employeur, minimum)
        complementaire_sante_montant = individu('complementaire_sante_montant', period)
        cotisation = - part_employeur * complementaire_sante_montant

        return cotisation

    def formula(individu, period):
        part_employeur = individu('complementaire_sante_part_employeur', period)
        complementaire_sante_montant = individu('complementaire_sante_montant', period)
        cotisation = - part_employeur * complementaire_sante_montant

        return cotisation


class complementaire_sante_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Couverture complémentaire santé collective d'entreprise - part salarié"
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038610242'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2016_01_01(individu, period, parameters):
        complementaire_sante_part_employeur = individu('complementaire_sante_part_employeur', period)
        minimum = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.complementaire_sante.part_employeur
        part_employeur = max_(complementaire_sante_part_employeur, minimum)
        complementaire_sante_montant = individu('complementaire_sante_montant', period)
        cotisation = - (1 - part_employeur) * complementaire_sante_montant

        return cotisation

    def formula(individu, period):
        part_employeur = individu('complementaire_sante_part_employeur', period)
        complementaire_sante_montant = individu('complementaire_sante_montant', period)
        cotisation = - (1 - part_employeur) * complementaire_sante_montant

        return cotisation


class TypesTailleEntreprise(Enum):
    __order__ = 'non_pertinent moins_de_10 de_10_a_19 de_20_a_249 plus_de_250'  # Needed to preserve the enum order in Python 2
    non_pertinent = 'Non pertinent'
    moins_de_10 = 'Moins de 10 salariés'
    de_10_a_19 = 'De 10 à 19 salariés'
    de_20_a_249 = 'De 20 à 249 salariés'
    plus_de_250 = 'Plus de 250 salariés'


class taille_entreprise(Variable):
    value_type = Enum
    possible_values = TypesTailleEntreprise
    default_value = TypesTailleEntreprise.non_pertinent
    entity = Individu
    label = "Catégorie de taille d'entreprise"
    reference = 'http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        taille_entreprise = select(
            [
                (effectif_entreprise <= 0),
                (effectif_entreprise <= 9),
                (effectif_entreprise <= 19),
                (effectif_entreprise <= 249),
                (effectif_entreprise >= 250)
                ],
            [
                TypesTailleEntreprise.non_pertinent,
                TypesTailleEntreprise.moins_de_10,
                TypesTailleEntreprise.de_10_a_19,
                TypesTailleEntreprise.de_20_a_249,
                TypesTailleEntreprise.plus_de_250
                ]
            )
        return taille_entreprise


class taux_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = "Approximation du taux accident à partir de l'exposition au risque donnée"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2012_01_01(individu, period, parameters):
        exposition_accident = individu('exposition_accident', period)
        TypesExpositionAccident = exposition_accident.possible_values
        accident = parameters(period).prelevements_sociaux.cotisations_securite_sociale_regime_general.accidents.taux
        return select(
            [
                exposition_accident == TypesExpositionAccident.faible,
                exposition_accident == TypesExpositionAccident.moyen,
                exposition_accident == TypesExpositionAccident.eleve,
                exposition_accident == TypesExpositionAccident.tres_eleve,
                ],
            [
                accident.faible,
                accident.moyen,
                accident.eleve,
                accident.treseleve
                ]
            )


class vieillesse_deplafonnee_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation vieillesse déplafonnée (salarié)'
    reference = [
        'Article L. 242-1 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044626664'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = 'vieillesse_deplafonnee_salarie',
            )
        return cotisation


class vieillesse_plafonnee_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation vieillesse plafonnée (salarié)'
    reference = [
        'Article L. 242-1 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044626664'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse_plafonnee',
            variable_name = 'vieillesse_plafonnee_salarie',
            )
        return cotisation


class vieillesse_deplafonnee_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation vieillesse déplafonnée'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article L. 242-1 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044626664'
        ]

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = 'vieillesse_deplafonnee_employeur',
            )
        return cotisation


class vieillesse_plafonnee_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation vieillesse plafonnée (employeur)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article L. 242-1 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044626664'
        ]

    def formula(individu, period, parameters):
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'vieillesse_plafonnee',
            variable_name = 'vieillesse_plafonnee_employeur',
            )
        return cotisation


class peec_employeur(Variable):
    value_type = bool
    entity = Individu
    label = "Participation de l'employeur à l'effort de construction (PEEC) communément appelé le 1% logement (employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.service-public.fr/professionnels-entreprises/vosdroits/F22583'


class secteur_activite_employeur(Variable):
    value_type = Enum
    possible_values = TypesSecteurActivite
    default_value = TypesSecteurActivite.non_renseigne
    entity = Individu
    label = "Secteur d'activité (employeur)"
    definition_period = MONTH
    reference = 'https://www.service-public.fr/professionnels-entreprises/vosdroits/N24269'
    set_input = set_input_dispatch_by_period
