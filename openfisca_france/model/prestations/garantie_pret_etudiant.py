from openfisca_france.model.base import *


class garantie_pret_etudiant_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité à la garantie de l'État au prêt étudiant"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.service-public.fr/particuliers/vosdroits/F986"

    def formula_2020_06_08(individu, period, parameters):
        majeur = individu('majeur', period)

        age = individu('age', period)
        condition_age = (age <= parameters(period).prestations.garantie_pret_etudiant.age_max)

        etudiant = individu('etudiant', period)
        condition_nationalite = individu('garantie_pret_etudiant_condition_nationalite', period)

        return majeur * etudiant * condition_age * condition_nationalite


class garantie_pret_etudiant_condition_nationalite(Variable):
    value_type = bool
    label = "Remplissage de la condition de nationalité ou de résidence pour la garantie de l'État au prêt étudiant"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.service-public.fr/particuliers/vosdroits/F986"

    def formula_2021_02_19(individu, period, parameters):
        nationalite_francaise = individu('nationalite', period) == b'FR'

        ressortissant_eee = individu('ressortissant_eee', period)
        residence_continue_annees = individu('residence_continue_annees', period)
        duree_min_residence_continue_annees = parameters(period).prestations.garantie_pret_etudiant.duree_min_residence_continue_annees
        eligibilite_eee = ressortissant_eee * residence_continue_annees >= duree_min_residence_continue_annees

        return nationalite_francaise + eligibilite_eee
