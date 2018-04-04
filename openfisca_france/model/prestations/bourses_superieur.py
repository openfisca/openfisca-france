# -*- coding: utf-8 -*-

from __future__ import division

import csv
import pkg_resources

from numpy import fromiter, int16

import openfisca_france

from openfisca_france.model.base import *  # noqa analysis:ignore

# NB : les variables de bourses de l'enseignment supérieur sont au niveau Individu, car elles sont versées au jeune et dépendent de la distance établissement scolaire-domicile familial qui est spécifique au jeune


class base_ressource_bourse_superieur(Variable):
    entity = Individu
    value_type = int
    label = u"Base ressource entrant dans le calcul des bourses de l'enseignement supérieur "
    reference = "http://www.enseignementsup-recherche.gouv.fr/pid20536/bulletin-officiel.html?cid_bo=115546&cbo=1"
    definition_period = MONTH

    def formula(individu, period, parameters):

        rbg_foyer = individu.foyer_fiscal('rbg', period.this_year.n_2) # Ex : pour l'année scolaire 2017-2018 c'est les revenus 2015 qui comptent
        
        # Cas particuliers à traiter : 
        # (Cf. annexe 3.1.1 de la référence ci-dessus)
        # - Cas des parents séparés => prendre les deux RBG si pas de pension alimentaire prevue
        # - Cas de parents concubins non mariés => prendre les deux RBG
        # - Cas des enfants mariés/pacsés/avec enfants à charge => prendre son propre RBG

        return rbg_foyer


class bourse_superieur_points_de_charge(Variable):
    value_type = float
    label = u"Nombre de points de charge pour la bourse sur critère social de l'enseignement supérieur"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):

        eligible = individu('bourse_superieur_eligibilite', period.this_year)

        distance = individu('distance_domicile_etablissement_superieur', period)
        points_eloignement = (
            0 * (distance < 30) +
            1 * (distance >= 30) * (distance < 250) +
            2 * (distance >= 250)
        )

        nb_enfants = individu.famille('nb_enfants_a_charge', period)
        nb_enfants_dans_enseignement_sup = individu.famille('nb_enfants_a_charge_superieur', period)
        points_de_charge_famille = (
            2 * (nb_enfants - 1) +
            4 * (nb_enfants_dans_enseignement_sup - 1) 
            )

        return (points_eloignement + points_de_charge_famille) * eligible


class bourse_superieur_annuel(Variable):
    value_type = float
    entity = Individu
    label = u"Montant annuel de la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH

    def formula(individu, period, parameters):

        age = individu('age', period) # NB : age au 01/09/N normalement
        est_etudiant = individu('etudiant', period)
        echelon = individu('echelon_bourse', period)
        eligible = individu('bourse_superieur_eligibilite', period.this_year)
        P = parameters(period).bourses_education.bourse_superieur

        montant_bourse_annuel = P.montant[echelon] # NB : normalement montant bourse = montant annuel sur 10 mois (pas de bourses juillet-aout), pour simplifier on divise par 12 pour obtenir montant mensuel

        return eligible * montant_bourse_annuel


class bourse_superieur_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = u"Eligibilité à une bourse de l'enseignement supérieur"
    definition_period = YEAR

    def formula(individu, period, parameters):

        age = individu('age', period.first_month) # NB : age au 01/09/N normalement
        est_etudiant = individu('etudiant', period.first_month)
        eligible = (age > 17) * (age <= 28) * est_etudiant # TODO : gérer le fait qu'on peut être étudiant et avoir moins de 18ans
        
        return eligible


class bourse_superieur(Variable):
    value_type = float
    entity = Individu
    label = u"Montant mensuel de la bourse sur critères sociaux de l'enseignement supérieur"
    definition_period = MONTH

    def formula(individu, period, parameters):

        montant_bourse_annuel = individu('bourse_superieur_annuel', period) # NB : normalement montant bourse = montant annuel sur 10 mois (pas de bourses juillet-aout), pour simplifier on divise par 12 pour obtenir montant mensuel
        eligible = individu('bourse_superieur_eligibilite', period.this_year)

        return (montant_bourse_annuel / 12) * eligible


class boursier(Variable):
    value_type = bool
    entity = Individu
    label = u"Élève ou étudiant boursier"
    definition_period = MONTH

    # 4 conditions selon la loi : age, ressources, nationalite, type diplome

    # Moins de 28 ans au 1er septembre de la formation normalement sauf dérogation (handicap, service civique, armée..)
    # En principe : boursier sur 7 périodes maxi
    # Conditions de maintien de bourses spécifiques à partir du 3e droit (3ème année)


class distance_domicile_etablissement_superieur(Variable):
    value_type = float
    entity = Individu
    label = u"Distance (en km) entre le domicile familial et l'établissement d'enseignement supérieur"
    definition_period = MONTH
    default_value = 30 # Temporaire


class TypesEchelonBourse(Enum):
    __order__ = 'echelon_0 echelon_1 echelon_2 echelon_3 echelon_4 echelon_5 echelon_6 echelon_7 non_boursier'  # Needed to preserve the enum order in Python 2
    echelon_0 = u"Echelon 0"
    echelon_1 = u"Echelon 1"
    echelon_2 = u"Echelon 2"
    echelon_3 = u"Echelon 3"
    echelon_4 = u"Echelon 4"
    echelon_5 = u"Echelon 5"
    echelon_6 = u"Echelon 6"
    echelon_7 = u"Echelon 7"
    non_boursier = u"Non boursier"


class echelon_bourse(Variable):
    entity = Individu
    value_type = Enum
    possible_values = TypesEchelonBourse
    default_value = TypesEchelonBourse.non_boursier
    label = u"Echelon de la bourse perçue (de 0 à 7)"
    definition_period = MONTH

    def formula(individu, period, parameters):

        points_de_charge = individu('bourse_superieur_points_de_charge', period)
        revenus_famille = individu('base_ressource_bourse_superieur', period)
        eligible = individu('bourse_superieur_eligibilite', period.this_year)
        P = parameters(period).bourses_education.bourse_superieur
 
        echelons = [7, 6, 5, 4, 3, 2, 1, 0]

        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/bourses_superieur/plafonds2017_2018.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            plafonds_ressources_by_pts = {
                int(row['PTS']): [
                    int(row['echelon_0']),
                    int(row['echelon_1']),
                    int(row['echelon_2']),
                    int(row['echelon_3']),
                    int(row['echelon_4']),
                    int(row['echelon_5']),
                    int(row['echelon_6']),
                    int(row['echelon_7']),
                    ]
                for row in csv_reader
                }

        plafonds_ressources = [
            fromiter(
                (plafonds_ressources_by_pts.get(pts_cell)[echelon] for pts_cell in points_de_charge),
                dtype = float,
            )
            for echelon in echelons
            ]

        echelon_bourse = apply_thresholds(
            revenus_famille, 
            thresholds = plafonds_ressources,
            choices = [7, 6, 5, 4, 3, 2, 1, 0, 9999]
        ) * eligible

        return select(
            (echelon_bourse == 9999, echelon_bourse == 0, echelon_bourse == 1, echelon_bourse == 2, echelon_bourse == 3, echelon_bourse == 4, echelon_bourse == 5, echelon_bourse == 6, echelon_bourse == 7),
            (TypesEchelonBourse.non_boursier.index, TypesEchelonBourse.echelon_0.index, TypesEchelonBourse.echelon_1.index, TypesEchelonBourse.echelon_2.index, TypesEchelonBourse.echelon_3.index, TypesEchelonBourse.echelon_4.index, TypesEchelonBourse.echelon_5.index, TypesEchelonBourse.echelon_6.index, TypesEchelonBourse.echelon_7.index,)
        )


class nb_enfants_a_charge(Variable):
    value_type = int
    entity = Famille
    label = u"Nombre d'enfants à charge, à prendre en compte pour le calcul des bourses"
    definition_period = MONTH

    # NB : enfants à charge = enfants rattachés fiscalement à un ou aux parents de la famille en N-2 + ceux éventuellement nés depuis

    def formula (famille, period, paramaters):
        age_i = famille.members('age', period)
        nb_enfants = famille.sum(age_i >= 0, role = Famille.ENFANT) 
    
        return nb_enfants


class nb_enfants_a_charge_superieur(Variable):
    value_type = int
    entity = Famille
    label = u"Nombre d'enfants à charge étudiants dans l'enseignement supérieur, à prendre en compte pour le calcul des bourses"
    definition_period = MONTH
    default_value = 1 # provisoire (utiliser les cases 7EF et 7EG de la déclaration 2042 ?)

    # NB : enfants à charge = rattachés fiscalement aux parents en N-2
    # NB2 : enfants étudiants = inscrit dans l'enseignement supérieur l'année N (de demande de la bourse)


def main():

    import openfisca_france

    tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()
    year = 2018
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = year,
        parent1 = dict(
            activite = u'actif',
            date_naissance = 1970,
            salaire_imposable = 20000,
            statut_marital = u'marie',
            ),
        parent2 = dict(
             activite = u'actif',
             date_naissance = 1973,
             salaire_imposable = 10000,
             statut_marital = u'marie',
             ),
        enfants = [
            dict(
                 activite = u'etudiant',
                 date_naissance = '1993-02-01',
                 ),
            dict(
                activite = u'etudiant',
                date_naissance = '1994-04-17',
                ),
             ],
        )
    scenario.suggest()

    simulation = scenario.new_simulation(debug = True)

    eligibilite = simulation.calculate('bourse_superieur_eligibilite', simulation.period)
    print("Eligibilite : {}".format(eligibilite))
    base_ressource = simulation.calculate('base_ressource_bourse_superieur', simulation.period.first_month)
    print("Base ressource : {}".format(base_ressource))
    points =  simulation.calculate('bourse_superieur_points_de_charge', simulation.period.first_month)
    print("Points de charge : {}".format(points))
    echelon = simulation.calculate('echelon_bourse', simulation.period.first_month)
    print("Echelon : {}".format(echelon))
    bourse_superieur = simulation.calculate('bourse_superieur', simulation.period.first_month)
    print("Montant mensuel bourse : {}".format(bourse_superieur))


if __name__ == "__main__":
    import sys
    
    sys.exit(main())