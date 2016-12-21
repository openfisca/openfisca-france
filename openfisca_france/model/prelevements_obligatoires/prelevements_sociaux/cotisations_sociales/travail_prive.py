# -*- coding: utf-8 -*-

from __future__ import division

import logging


from numpy import int16, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_


from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme, apply_bareme_for_relevant_type_sal


log = logging.getLogger(__name__)


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


class assiette_cotisations_sociales(Variable):
    column = FloatCol
    entity = Individu
    label = u"Assiette des cotisations sociales des salaries"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        assiette_cotisations_sociales_prive = simulation.calculate('assiette_cotisations_sociales_prive', period)
        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        return period, (
            assiette_cotisations_sociales_prive +
            assiette_cotisations_sociales_public +
            stage_gratification_reintegration
            )


class assiette_cotisations_sociales_prive(Variable):
    column = FloatCol
    entity = Individu
    label = u"Assiette des cotisations sociales des salaries du prive"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        avantage_en_nature = simulation.calculate('avantage_en_nature', period)
        hsup = simulation.calculate('hsup', period)
        indemnites_compensatrices_conges_payes = simulation.calculate('indemnites_compensatrices_conges_payes', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        indemnite_fin_contrat = simulation.calculate('indemnite_fin_contrat', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            "reintegration_titre_restaurant_employeur", period
            )
        remuneration_apprenti = simulation.calculate('remuneration_apprenti', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        assiette = (
            salaire_de_base +
            primes_salaires +
            avantage_en_nature +
            hsup +
            indemnites_compensatrices_conges_payes +
            remuneration_apprenti +
            (categorie_salarie == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique) +
            reintegration_titre_restaurant_employeur + indemnite_fin_contrat
            )
        return period, assiette * (assiette > 0)


class indemnite_fin_contrat(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnité de fin de contrat"
    url = u"https://www.service-public.fr/particuliers/vosdroits/F40"

    def function(self, simulation, period):
        month = period.start.offset('first-of', 'month').period(u'month')
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        apprenti = simulation.calculate('apprenti', month)

        # Un grand nombre de conditions peuvent invalider cette indemnité, voir le lien ci-dessus.
        # A ajouter au fur et à mesure
        # Pour l'instant, cette variable d'entrée peut les remplacer
        # Elle est cependant fixée à False par défaut
        indemnite_fin_contrat_due = simulation.calculate('indemnite_fin_contrat_due', period)

        taux = simulation.legislation_at(period.start).cotsoc.indemnite_fin_contrat.taux

        result = (
            # CDD
            (contrat_de_travail_duree == 1) *
            # non fonction publique
            (
                (categorie_salarie == 0) +
                (categorie_salarie == 1)
            ) *
            not_(apprenti) *
            indemnite_fin_contrat_due *
            # 10% du brut
            taux * salaire_de_base
            )
        return period, result

class reintegration_titre_restaurant_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Prise en charge de l'employeur des dépenses de cantine et des titres restaurants non exonérés de charges sociales"  # noqa

    def function(self, simulation, period):
        period = period  # TODO
        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)
        cantines_titres_restaurants = simulation.legislation_at(
            period.start).cotsoc.assiette.cantines_titres_restaurants

        taux_minimum_exoneration = cantines_titres_restaurants.taux_minimum_exoneration
        taux_maximum_exoneration = cantines_titres_restaurants.taux_maximum_exoneration
        seuil_prix_titre = cantines_titres_restaurants.seuil_prix_titre
        condition_exoneration_taux = (
            (taux_minimum_exoneration <= taux_employeur) *
            (taux_maximum_exoneration >= taux_employeur)
            )
        montant_reintegration = volume * (
            condition_exoneration_taux * max_(valeur_unitaire * taux_employeur - seuil_prix_titre, 0) +
            not_(condition_exoneration_taux) * valeur_unitaire * taux_employeur
            )
        return period, montant_reintegration


# Cotisations proprement dites


class accident_du_travail(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisations employeur accident du travail et maladie professionelle"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate(
            'assiette_cotisations_sociales', period)
        taux_accident_travail = simulation.calculate('taux_accident_travail', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        assujetti = categorie_salarie <= 1  # TODO: ajouter contractuel du public salarié de moins d'un an ou à temps partiel
        return period, - assiette_cotisations_sociales * taux_accident_travail * assujetti


class agff_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation retraite AGFF tranche A (salarié)"
    # AGFF: Association pour la gestion du fonds de financement (sous-entendu des départs entre 60 et 65 ans)

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "agff",
            variable_name = self.__class__.__name__
            )
        return period, cotisation


class agff_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation retraite AGFF tranche A (employeur)"
    # TODO: améliorer pour gérer mensuel/annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate(
            'assiette_cotisations_sociales', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)

        law = simulation.legislation_at(period.start)

        cotisation_non_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = "agffnc",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )

        cotisation_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = "agffc",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return period, cotisation_cadre + cotisation_non_cadre


class agirc_gmp_assiette(Variable):
    column = FloatCol
    entity = Individu
    label = u"Assiette de la cotisation AGIRC pour la garantie minimale de points (GMP,  salarié)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        gmp = simulation.legislation_at(period.start).prelevements_sociaux.gmp
        assiette = max_(
            (gmp.salaire_charniere_annuel / 12 - assiette_cotisations_sociales) * (assiette_cotisations_sociales > 0),
            0,
            )
        return period, assiette


class agirc_gmp_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP,  salarié)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        agirc_gmp_assiette = simulation.calculate('agirc_gmp_assiette', period)
        agirc_salarie = simulation.calculate('agirc_salarie', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        gmp = simulation.legislation_at(period.start).prelevements_sociaux.gmp
        cotisation_forfaitaire = gmp.cotisation_forfaitaire_mensuelle_en_euros.part_salariale
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_salarie.prive_cadre.agirc.rates[1]
        sous_plafond_securite_sociale = (
            (assiette_cotisations_sociales <= plafond_securite_sociale) & (assiette_cotisations_sociales > 0)
            )
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * agirc_gmp_assiette * taux
            )
        return period, min_((cotisation - agirc_salarie) * (categorie_salarie == 1), 0)  # cotisation are negative


class agirc_gmp_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP, employeur)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):

        period = period.start.period(u'month').offset('first-of')
        agirc_employeur = simulation.calculate('agirc_employeur', period)
        agirc_gmp_assiette = simulation.calculate('agirc_gmp_assiette', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        gmp = simulation.legislation_at(period.start).prelevements_sociaux.gmp
        cotisation_forfaitaire = gmp.cotisation_forfaitaire_mensuelle_en_euros.part_patronale
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_cadre']['agirc'].rates[1]

        sous_plafond_securite_sociale = (
            (assiette_cotisations_sociales <= plafond_securite_sociale) & (assiette_cotisations_sociales > 0)
            )
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * agirc_gmp_assiette * taux
            )
        return period, min_((cotisation - agirc_employeur) * (categorie_salarie == 1), 0)  # cotisation are negative


class agirc_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation AGIRC tranche B (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "agirc",
            variable_name = self.__class__.__name__
            )
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        return period, cotisation * (categorie_salarie == 1)


class agirc_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation AGIRC tranche B (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "employeur",
            bareme_name = "agirc",
            variable_name = self.__class__.__name__
            )
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        return period, cotisation * (categorie_salarie == 1)


class ags(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)"  # noqa analysis:ignore

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "employeur",
            bareme_name = "chomfg",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class apec_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisations agence pour l'emploi des cadres (APEC,  salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "salarie",
            bareme_name = "apec",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * (categorie_salarie == 1)  # TODO: check public notamment contractuel


class apec_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisations Agenece pour l'emploi des cadres (APEC, employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "apec",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation  # TODO: check public notamment contractuel


class arrco_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation ARRCO tranche 1 (salarié)"
    # TODO: check gestion mensuel/annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation_minimale = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "arrco",
            variable_name = self.__class__.__name__,
            )
        arrco_tranche_a_taux_salarie = simulation.calculate('arrco_tranche_a_taux_salarie', period)
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        # cas où l'entreprise applique un taux spécifique
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale) *
            arrco_tranche_a_taux_salarie
            )
        return period, (
            cotisation_minimale * (arrco_tranche_a_taux_salarie == 0) + cotisation_entreprise
            ) * (categorie_salarie <= 1)


class arrco_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation ARRCO tranche 1 (employeur)"
    # TODO: check gestion mensuel/annuel

    def function(self, simulation, period):
        cotisation_minimale = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "arrco",
            variable_name = self.__class__.__name__,
            )
        arrco_tranche_a_taux_employeur = simulation.calculate('arrco_tranche_a_taux_employeur', period)
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        # cas où l'entreprise applique un taux spécifique
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale) *
            arrco_tranche_a_taux_employeur
            )
        return period, (
            cotisation_minimale * (arrco_tranche_a_taux_employeur == 0) + cotisation_entreprise
            ) * (categorie_salarie <= 1)


class chomage_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation chômage tranche A (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "assedic",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class chomage_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation chômage tranche A (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "assedic",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class contribution_solidarite_autonomie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution solidarité autonomie (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "csa",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class cotisation_exceptionnelle_temporaire_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation_exceptionnelle_temporaire (salarie)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'cet',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class cotisation_exceptionnelle_temporaire_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation exceptionnelle temporaire (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'cet',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class famille(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation famille (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'famille',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class mmid_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation maladie (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salarie_regime_alsace_moselle = simulation.calculate('salarie_regime_alsace_moselle', period)

        cotisation_regime_general = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )

        cotisation_regime_alsace_moselle = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maladie_alsace_moselle',
            variable_name = self.__class__.__name__,
            )

        cotisation = cotisation_regime_general + salarie_regime_alsace_moselle * cotisation_regime_alsace_moselle


        return period, cotisation


class mmid_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation maladie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


# TODO: this formula is used only to check fiche_de_paie from memento
class mmida_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation maladie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )
        contribution_solidarite_autonomie = simulation.calculate('contribution_solidarite_autonomie', period)
        return period, cotisation + contribution_solidarite_autonomie


class mhsup(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"Heures supplémentaires comptées négativement"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        hsup = simulation.calculate('hsup', period)

        return period, -hsup


class plafond_securite_sociale(Variable):
    column = FloatCol
    entity = Individu
    label = u"Plafond de la securite sociale"
    # TODO gérer les plafonds mensuel, trimestriel, annuel

    def function(self, simulation, period):

        period = period.start.period(u'month').offset('first-of')
        plafond_temps_plein = simulation.legislation_at(period.start).cotsoc.gen.plafond_securite_sociale
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        contrat_de_travail = simulation.calculate('contrat_de_travail', period)
        heures_remunerees_volume = simulation.calculate('heures_remunerees_volume', period)
        forfait_jours_remuneres_volume = simulation.calculate('forfait_jours_remuneres_volume', period)
        heures_duree_collective_entreprise = simulation.calculate('heures_duree_collective_entreprise', period)

        # TODO : handle contrat_de_travail > 1

        # 1) Proratisation pour temps partiel

        duree_legale_mensuelle = 35 * 52 / 12  # ~151,67
        heures_temps_plein = switch(heures_duree_collective_entreprise, {0: duree_legale_mensuelle, 1: heures_duree_collective_entreprise})

        plafond = switch(
            contrat_de_travail,
             {  # temps plein
                0: plafond_temps_plein,
                # temps partiel
                1: plafond_temps_plein * (heures_remunerees_volume / heures_temps_plein),
                # forfait jour
                5: plafond_temps_plein * (forfait_jours_remuneres_volume / 218)
             })

        # 2) Proratisation pour mois incomplet selon la méthode des 30èmes

        # calcul du nombre de jours calendaires de présence du salarié
        nombre_jours_calendaires = simulation.calculate('nombre_jours_calendaires', period)

        # Pour les salariés entrés ou sortis en cours de mois,
        # le plafond applicable est égal à autant de trentièmes du plafond mensuel
        # que le salarié a été présent de jours calendaires. Source urssaf.fr "L’assiette maximale"

        plafond = plafond * (min_(nombre_jours_calendaires, 30) / 30)

        return period, plafond


class prevoyance_obligatoire_cadre(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation de prévoyance pour les cadres et assimilés"
    # TODO: gérer le mode de recouvrement et l'aspect mensuel/annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        prevoyance_obligatoire_cadre_taux_employeur = simulation.calculate(
            'prevoyance_obligatoire_cadre_taux_employeur', period)

        cotisation = - (
            (categorie_salarie == CAT['prive_cadre']) *
            min_(assiette_cotisations_sociales, plafond_securite_sociale) *
            prevoyance_obligatoire_cadre_taux_employeur
            )
        return period, cotisation


class complementaire_sante_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Couverture complémentaire santé collective d'entreprise - part employeur"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        complementaire_sante_taux_employeur = simulation.calculate(
            'complementaire_sante_taux_employeur', period)
        complementaire_sante_montant = simulation.calculate('complementaire_sante_montant', period)

        cotisation = - complementaire_sante_taux_employeur * complementaire_sante_montant
        return period, cotisation


class complementaire_sante_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Couverture complémentaire santé collective d'entreprise - part salarié"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        complementaire_sante_taux_employeur = simulation.calculate(
            'complementaire_sante_taux_employeur', period)
        complementaire_sante_montant = simulation.calculate('complementaire_sante_montant', period)

        cotisation = - (1 - complementaire_sante_taux_employeur) * complementaire_sante_montant
        return period, cotisation


class taille_entreprise(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Non pertinent",
                u"Moins de 10 salariés",
                u"De 10 à 19 salariés",
                u"De 20 à 249 salariés",
                u"Plus de 250 salariés",
                ],
            ),
        default = 0,
        )
    entity = Individu
    label = u"Catégorie de taille d'entreprise"
    url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321"

    def function(self, simulation, period):
        period = period
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        taille_entreprise = (
            (effectif_entreprise > 0).astype(int16) +
            (effectif_entreprise > 9).astype(int16) +
            (effectif_entreprise > 19).astype(int16) +
            (effectif_entreprise > 249).astype(int16)
            )
        return period, taille_entreprise


class taux_accident_travail(Variable):
    column = FloatCol
    entity = Individu
    label = u"Approximation du taux accident à partir de l'exposition au risque donnée"
    start_date = date(2012, 1, 1)

    def function(self, simulation, period):
        period_extract = period.start.period(u'month').offset('first-of')
        exposition_accident = simulation.calculate('exposition_accident', period_extract)
        accident = simulation.legislation_at(period_extract.start).cotsoc.accident

        return period, (exposition_accident == 0) * accident.faible + (exposition_accident == 1) * accident.moyen \
            + (exposition_accident == 2) * accident.eleve + (exposition_accident == 3) * accident.treseleve


class vieillesse_deplafonnee_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation vieillesse déplafonnée (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class vieillesse_plafonnee_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation vieillesse plafonnée (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class vieillesse_deplafonnee_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation vieillesse déplafonnée"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


class vieillesse_plafonnee_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation vieillesse plafonnée (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'vieillesse_plafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation
