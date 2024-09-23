from openfisca_france.model.base import Variable, MONTH, Individu


class pass_sport(Variable):
    label = 'Éligibilité au Pass’Sport'
    definition_period = MONTH
    value_type = float
    reference = ['https://www.legifrance.gouv.fr/loda/id/LEGIARTI000046139655/2022-08-05#LEGIARTI000046139655',
                 'https://www.etudiant.gouv.fr/fr/le-pass-sport-et-les-etudiants-2800']
    entity = Individu
    documentation = '''
    Non modélisé (2023) :
        -  Etre un étudiant âgé au plus de 28 ans révolus et bénéficier, au plus tard le 15 octobre 2022, d'une aide annuelle sous conditions de ressources, dans le cadre des formations sanitaires et sociales en application des articles L. 4151-8 et L. 4383-4 du code de la santé publique ou de l'article L. 451-3 du code de l'action sociale et des familles.
    '''

    def formula_2022_06_30(individu, period, parameters):
        parametres = parameters(period).prestations_sociales.education.pass_sport

        age = individu('age', period)

        boursier = individu('boursier', period)
        age_maximum_profil_boursier = parametres.critere_age.age_maximum_profil_boursier
        eligibilite_age_profil_boursier = age <= age_maximum_profil_boursier
        eligibilite_profil_boursier = boursier * eligibilite_age_profil_boursier

        eligibilite_ars = individu.famille('ars', period.this_year) > 0
        age_maximum_profil_ars = parametres.critere_age.age_maximum_profil_ars
        age_minimum_profil_ars = parametres.critere_age.age_minimum_profil_ars
        eligibilite_age_profil_ars = (age >= age_minimum_profil_ars) * (age <= age_maximum_profil_ars)
        eligibilite_profil_ars = eligibilite_ars * eligibilite_age_profil_ars

        eligibilite_aeeh = individu.famille('aeeh', period) > 0
        age_maximum_profil_aeeh = parametres.critere_age.age_maximum_profil_aeeh
        age_minimum_profil_aeeh = parametres.critere_age.age_minimum_profil_aeeh
        eligibilite_age_profil_aeeh = (age >= age_minimum_profil_aeeh) * (age <= age_maximum_profil_aeeh)
        eligibilite_profil_aeeh = eligibilite_aeeh * eligibilite_age_profil_aeeh

        eligibilite_aah = individu('aah', period) > 0
        age_maximum_profil_aah = parametres.critere_age.age_maximum_profil_aah
        age_minimum_profil_aah = parametres.critere_age.age_minimum_profil_aah
        eligibilite_age_profil_aah = (age >= age_minimum_profil_aah) * (age <= age_maximum_profil_aah)
        eligibilite_profil_aah = (eligibilite_aah * eligibilite_age_profil_aah)

        montant = parametres.montant

        eligibilite = (
            eligibilite_profil_boursier
            + eligibilite_profil_ars
            + eligibilite_profil_aeeh
            + eligibilite_profil_aah
            )

        return montant * eligibilite
