from openfisca_france.model.base import Individu, Menage, TypesActivite, TypesStatutOccupationLogement, Variable, MONTH, set_input_dispatch_by_period
from numpy import datetime64


class locapass_eligibilite(Variable):
    entity = Individu
    value_type = bool
    label = "Indicatrice d'éligibilité au dispositif Loca-Pass"
    definition_period = MONTH
    reference = 'https://www.actionlogement.fr/l-avance-loca-pass'

    def formula(individu, period, parameters):
        params = parameters(period).action_logement.locapass

        eligibilite_individu = individu('locapass_eligibilite_individu', period)
        eligibilite_logement = individu.menage('locapass_eligibilite_logement', period)
        eligibilite_date_entree_logement = individu.menage('date_entree_logement', period) >= datetime64(period.offset(-params.delai_max_en_mois_apres_entree_logement, 'month').start)
        return eligibilite_individu * eligibilite_logement * eligibilite_date_entree_logement


class locapass_eligibilite_logement(Variable):
    entity = Menage
    value_type = bool
    label = "Satisfaction des conditions d'éligibilité relatives au logement pour le dispositif Loca-Pass"
    definition_period = MONTH

    def formula(menage, period):
        statut_occupation = menage('statut_occupation_logement', period)
        return (
            + (statut_occupation == TypesStatutOccupationLogement.locataire_hlm)
            + (statut_occupation == TypesStatutOccupationLogement.locataire_vide)
            + (statut_occupation == TypesStatutOccupationLogement.locataire_meuble)
            + (statut_occupation == TypesStatutOccupationLogement.locataire_foyer)
            )


class locapass_eligibilite_individu(Variable):
    entity = Individu
    value_type = bool
    label = "Satisfaction des conditions d'éligibilité relatives au demandeur pour le dispositif Loca-Pass"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        eligibilite_salarie = individu('locapass_eligibilite_salarie', period)
        locapass_eligibilite_jeunes = individu('locapass_eligibilite_jeunes', period)
        locapass_eligibilite_etudiant = individu('locapass_eligibilite_etudiant', period)
        return eligibilite_salarie + locapass_eligibilite_jeunes + locapass_eligibilite_etudiant


class locapass_eligibilite_salarie(Variable):
    entity = Individu
    value_type = bool
    label = "Indicatrice d'éligibilité au dispositif Loca-Pass pour les salariés"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        return individu('activite', period) == TypesActivite.actif


class locapass_eligibilite_jeunes(Variable):
    entity = Individu
    value_type = bool
    label = "Indicatrice d'éligibilité au dispositif Loca-Pass pour les jeunes"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        age = individu('age', period)
        age_max = parameters(period).action_logement.locapass.jeunes.age_max
        eligibilite_age = age <= age_max

        activite = individu('activite', period)
        alternant = individu('alternant', period)
        eligibilite_activite = (activite == TypesActivite.chomeur) + alternant * (activite == TypesActivite.etudiant)

        return eligibilite_age * eligibilite_activite


class locapass_eligibilite_etudiant_contrat(Variable):
    '''
    Approximation des conditions suivantes :
    - d’un contrat à durée déterminée (CDD) de trois mois minimum en cours au moment de la demande d'aide,
    - d’un ou plusieurs CDD pour une durée cumulée de trois mois minimum au cours des six mois précédant la demande d'aide,
    - ou d’une convention de stage d'au moins trois mois en cours au moment de la demande,
    '''
    entity = Individu
    value_type = bool
    label = "Satisfaction de la condition de loca-pass relative au contrat de travail pour les étudiants"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        nb_mois_travailles = sum([(individu('salaire_net', period.offset(-i)) > 0) for i in range(6)])
        return nb_mois_travailles >= 3


class locapass_eligibilite_etudiant(Variable):
    entity = Individu
    value_type = bool
    label = "Indicatrice d'éligibilité au dispositif Loca-Pass pour les étudiants"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        etudiant = individu('etudiant', period)
        boursier = individu('boursier', period)
        eligibilite_contrat = individu('locapass_eligibilite_etudiant_contrat', period)

        return etudiant * (boursier + eligibilite_contrat)
