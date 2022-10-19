from openfisca_france.model.base import *
from openfisca_core import periods
from numpy import logical_or as or_, logical_and as and_

class eligibilite_per(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Eligibilité à la prime exceptionnelle de rentrée"
    definition_period = YEAR

    def formula(individu, period, parameters):

        juin_2022 = periods.period('2021-06')

        eligibilite = individu.famille('rsa', juin_2022) * individu.has_role(Famille.PARENT)
        + individu.famille('apl', juin_2022)
        + individu.famille('alf', juin_2022)
        + individu.famille('als', juin_2022)
        + individu('ass', juin_2022)
        + individu('aer',juin_2022)
        + individu.famille('aspa',juin_2022)
        + individu('aah',juin_2022)

        eligibilite =  individu.famille('ppa',juin_2022)
        
        return eligibilite > 0

class eligibilite_per_etudiants(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289843'
    label = "Eligibilité à la prime exceptionnelle de rentrée des étudiants boursiers"
    definition_period = YEAR

    def formula(individu, period, parameters):
        eligibilite_etudiant = (individu.famille('ppa',juin_2022) > 0) * (individu.famille('apl',juin_2022) > 0)

        return (eligibilite_etudiant) > 0
        
class eligibilite_per_ppa(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Eligibilité à la prime exceptionnelle de rentrée des bénéficiaires de la prime d'activité"
    definition_period = YEAR

    def formula(individu, period, parameters):
        eligibilite_ppa = (individu('bourse_enseignement_sup',juin_2022) > 0) * (individu.famille('apl',juin_2022) > 0)

        return (eligibilite_ppa) > 0
        


class prime_exceptionnelle_rentree(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Prime exceptionnelle de rentrée"
    definition_period = YEAR

    def formula(individu,period,parameters):

    enfant_i = individu.menage.members.has_role(Famille.ENFANT)
    nb_enfants = menage.sum(enfant_i)  
    ppa=0

        if individu('eligibilite_per',period) > 0:    
            ppa = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per
            + nb_enfants * parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per

        elif ((individu('eligibilite_per',period)) == 0 & (individu('eligibilite_per_etudiants',period) > 0)):
            ppa = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per_enfant
            + nb_enfants * parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per_enfant

        elif individu('eligibilite_per',period) == 0 & individu('eligibilite_per_etudiants',period) > 0 & individu.famille(eligibilite_per_ppa,period)
            ppa = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per_ppa
            + nb_enfants * parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per_ppa_activite

        return ppa
