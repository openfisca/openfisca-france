from openfisca_france.model.base import *
from openfisca_core import periods
from numpy import logical_and as and_, logical_not as not_, logical_or as or_


class eligibilite_per(Variable):
    entity = Famille
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = 'Eligibilité à la prime exceptionnelle de rentrée'
    definition_period = YEAR
    end = '2022-12-31'

    def formula_2022(famille, period):

        juin_2022 = periods.period('2022-06')

        eligibilite = famille('rsa', juin_2022)
        + famille('apl', juin_2022)
        + famille('alf', juin_2022)
        + famille('als', juin_2022)
        + famille('aspa', juin_2022)

        eligibilite_ass_i = famille.members('ass', juin_2022)
        eligibilite_ass = famille.sum(eligibilite_ass_i)

        eligibilite_aer_i = famille.members('aer', juin_2022)
        eligibilite_aer = famille.sum(eligibilite_aer_i)

        eligibilite_aah_i = famille.members('aah', juin_2022)
        eligibilite_aah = famille.sum(eligibilite_aah_i)

        eligibilite_pfmra_i = famille.members('prime_forfaitaire_mensuelle_reprise_activite', juin_2022)
        eligibilite_pfmra = famille.sum(eligibilite_pfmra_i)

        return (eligibilite + eligibilite_ass + eligibilite_aer + eligibilite_aah + eligibilite_pfmra) > 0


class eligibilite_per_etudiant(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289843'
    label = 'Eligibilité à la prime exceptionnelle de rentrée des étudiants boursiers'
    definition_period = YEAR
    end = '2022-12-31'

    def formula_2022(individu, period):
        juin_2022 = periods.period('2022-06')
        annee_2022 = periods.period('2022')
        eligibilite_etudiant = where(
            not_(or_(individu('bourse_criteres_sociaux', juin_2022) > 0, individu('bourse_enseignement_sup', juin_2022) > 0)),
            False,
            where(
                and_(individu.has_role(Famille.DEMANDEUR), individu.famille('eligibilite_per', annee_2022)),
                False,
                True
                )
            )

        return eligibilite_etudiant


class eligibilite_per_ppa(Variable):
    entity = Famille
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046556491'
    label = 'Eligibilité à la prime exceptionnelle de rentrée des bénéficiaires de la prime d activité'
    definition_period = YEAR
    end = '2022-12-31'

    def formula_2022(famille, period):
        juin_2022 = periods.period('2022-06')
        eligibilite_ppa = (famille('ppa', juin_2022) > 0) * (not_(famille('eligibilite_per', juin_2022)))

        return eligibilite_ppa


class prime_exceptionnelle_rentree_non_etudiant(Variable):
    entity = Famille
    value_type = float
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = 'Prime exceptionnelle de rentrée'
    definition_period = YEAR
    end = '2022-12-31'

    def formula_2022(famille, period, parameters):

        juin_2022 = periods.period('2022-06')
        prestations_familiales_enfant_a_charge_i = famille.members('prestations_familiales_enfant_a_charge', juin_2022)
        nb_enfants = famille.sum(prestations_familiales_enfant_a_charge_i)
        parametres_per = parameters(period).prestations_sociales.solidarite_insertion.minima_sautre_solidarite.prime_exceptionnelle_rentree

        per = where(
            famille('eligibilite_per', period),
            parametres_per.per + nb_enfants * parametres_per.per_enfant,
            where(
                famille('eligibilite_per_ppa', period),
                parametres_per.per_ppa + nb_enfants * parametres_per.per_ppa_enfant,
                0
                )
            )

        return per


class prime_exceptionnelle_rentree_etudiant(Variable):
    entity = Individu
    value_type = float
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289843'
    label = 'Prime exceptionnelle de rentrée pour les étudiants boursiers'
    definition_period = YEAR
    end = '2022-12-31'

    def formula_2022(individu, period, parameters):

        '''
        Hypothèse : Si l'étudiant  est un enfant dans sa famille, ses enfants ne sont pas identifiés. La majoration pour enfant ne rentre donc pas en compte dans le calcul.
        '''

        juin_2022 = periods.period('2022-06')
        prestations_familiales_enfant_a_charge_i = individu.famille.members('prestations_familiales_enfant_a_charge', juin_2022)
        nb_enfants = individu.famille.sum(prestations_familiales_enfant_a_charge_i)
        parametres_per = parameters(period).prestations_sociales.solidarite_insertion.minima_sautre_solidarite.prime_exceptionnelle_rentree
        per_etudiant = where(
            not_(individu('eligibilite_per_etudiant', period)),
            0,
            where(
                individu.has_role(Famille.ENFANT),
                parametres_per.per_etudiant,
                parametres_per.per_etudiant + nb_enfants * parametres_per.per_etudiant_enfant
                )
            )

        return per_etudiant
