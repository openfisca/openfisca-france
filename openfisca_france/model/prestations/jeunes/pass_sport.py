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

    def formula_2022_06_30(individu, period):

        age = individu('age', period)

        boursier = individu('boursier', period)
        eligibilite_age_profil_boursier = age <= 28

        ars = individu.famille('ars', period.this_year)
        eligibilite_age_profil_ars = (age >= 6) * (age <= 17)

        aeeh = individu.famille('aeeh', period)
        eligibilite_age_profil_aeeh = (age >= 6) * (age <= 19)

        aah = individu('aah', period)
        eligibilite_age_profil_aah = (age >= 16) * (age <= 30)

        montant = 50

        return montant * ((boursier * eligibilite_age_profil_boursier) + (ars * eligibilite_age_profil_ars) + (aeeh * eligibilite_age_profil_aeeh) + (aah * eligibilite_age_profil_aah))
