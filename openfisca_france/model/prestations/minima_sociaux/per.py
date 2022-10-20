from openfisca_france.model.base import *
from openfisca_core import periods
from numpy import logical_or as or_, logical_and as and_

class eligibilite_per(Variable):
    entity = Famille
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Eligibilité à la prime exceptionnelle de rentrée"
    definition_period = ETERNITY

    def formula(famille,period):

        juin_2022 = periods.period('2022-06')

        eligibilite = famille('rsa', juin_2022)
        + famille('apl', juin_2022)
        + famille('alf', juin_2022)
        + famille('als', juin_2022)
        + famille('aspa',juin_2022)

        eligibilite_ass_i = famille.members('ass', juin_2022)
        eligibilite_ass = famille.sum(eligibilite_ass_i)

        eligibilite_aer_i = famille.members('aer',juin_2022)
        eligibilite_aer = famille.sum(eligibilite_aer_i)

        eligibilite_aah_i = famille.members('aah',juin_2022)
        eligibilite_aah = famille.sum(eligibilite_aah_i)

        return (eligibilite + eligibilite_ass + eligibilite_aer + eligibilite_aah ) > 0

#class eligibilite_per_etudiant(Variable):
#    entity = Individu
#    value_type = bool
#    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289843'
#    label = "Eligibilité à la prime exceptionnelle de rentrée des étudiants boursiers"
#    definition_period = YEAR

#    def formula(individu):
#        juin_2022 = periods.period('2022-06')
#        eligibilite_etudiant = (individu.famille('bourse_enseignement_sup',juin_2022) > 0) * (individu.famille('aide_logement',juin_2022) == 0)

#        return (eligibilite_etudiant) > 0
        
class eligibilite_per_ppa(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Eligibilité à la prime exceptionnelle de rentrée des bénéficiaires de la prime d'activité"
    definition_period = ETERNITY

    def formula(individu,period):
        juin_2022 = periods.period('2022-06')
        eligibilite_ppa = (individu('ppa',juin_2022) > 0)

        return (eligibilite_ppa) > 0
        


class prime_exceptionnelle_rentree(Variable):
    entity = Famille
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046289935'
    label = "Prime exceptionnelle de rentrée"
    definition_period = YEAR

    def formula(famille,period,parameters):

        enfant_i = famille.members.has_role(Famille.ENFANT)
        nb_enfants = famille.sum(enfant_i)  
        parametres_per = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.per
        ppa=0

        if famille('eligibilite_per',period) > 0:    
            ppa = parametres_per.per + nb_enfants * parametres_per.per_enfant

        #elif ((famille('eligibilite_per',period)) == 0 & (famille('eligibilite_per_etudiant',period) > 0)):
        #    ppa = parametres_per.per_etudiant + nb_enfants * parametres_per.per_etudiant_enfant

        elif (famille('eligibilite_per',period) == 0)  & (famille('eligibilite_per_ppa',period) > 0):
        # & (famille('eligibilite_per_etudiants') == 0)
            ppa = parametres_per.per_ppa + nb_enfants * parametres_per.per_ppa_enfant

        return ppa
