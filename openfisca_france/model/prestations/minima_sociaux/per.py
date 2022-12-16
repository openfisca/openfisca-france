from openfisca_france.model.base import *
from openfisca_core import periods
from numpy import logical_and as and_, logical_not as not_


class eligibilite_per(Variable):
    entity = Famille
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = 'Eligibilité à la prime exceptionnelle de rentrée'
    definition_period = ETERNITY

    def formula(famille, period):

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

        return (eligibilite + eligibilite_ass + eligibilite_aer + eligibilite_aah) > 0


class eligibilite_per_etudiant(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289843'
    label = 'Eligibilité à la prime exceptionnelle de rentrée des étudiants boursiers'
    definition_period = ETERNITY

    def formula(individu, period):
        juin_2022 = periods.period('2022-06')
        eligibilite_etudiant = where(
            not_(individu('boursier', juin_2022)),
            False,
            where(
                and_(individu.has_role(Famille.ENFANT), individu.famille('aide_logement', juin_2022) > 0),
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
    definition_period = ETERNITY

    def formula(famille, period):
        juin_2022 = periods.period('2022-06')
        eligibilite_ppa = (famille('ppa', juin_2022) > 0) * (not_(famille('eligibilite_per', juin_2022)))

        return eligibilite_ppa


class prime_exceptionnelle_rentree(Variable):
    entity = Famille
    value_type = float
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = 'Prime exceptionnelle de rentrée'
    definition_period = YEAR

    def formula(famille, period, parameters):

        enfant_i = famille.members.has_role(Famille.ENFANT)
        nb_enfants = famille.sum(enfant_i)
        parametres_per = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per

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

    def formula(individu, period, parameters):
        enfant_i = individu.famille.members.has_role(Famille.ENFANT)
        nb_enfants = individu.famille.sum(enfant_i)
        parametres_per = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per

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
