from openfisca_france.model.base import *


class aide_merite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide au mérite"
    definition_period = MONTH
    reference = [
        "https://www.etudiant.gouv.fr/fr/aide-au-merite-1291",
        "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000030722211/"
        ]
    documentation = '''
    Complémentaire à la bourse sur critères sociaux, pour les étudiants
    ayant eu mention très bien au baccalauréat.

    Non modélisé : 
    L'étudiant respecte les conditions d'inscription pédagogique, d'assiduité
    et de présentation aux examens (non applicable si nouveau bachelier).
    '''

    def formula(individu, period, parameters):
        bourse_criteres_sociaux = individu("bourse_criteres_sociaux", period)
        allocation_annuelle = individu("allocation_annuelle", period)
        condition_ressources = bourse_criteres_sociaux + allocation_annuelle

        mention_baccalaureat = individu("mention_baccalaureat", period)
        condition_mention = mention_baccalaureat == TypesMention.mention_tres_bien

        return condition_ressources * condition_mention
