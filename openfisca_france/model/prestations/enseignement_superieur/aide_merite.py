from openfisca_france.model.base import *


class aide_merite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide au mérite"
    definition_period = MONTH
    reference = [
        "https://www.etudiant.gouv.fr/fr/aide-au-merite-1291",
        "https://www.service-public.fr/particuliers/vosdroits/F1010",
        "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000030722211/"
        ]
    documentation = '''
    Complémentaire à la bourse sur critères sociaux, pour les étudiants
    ayant eu mention très bien au baccalauréat.

    Non modélisé : 
    L'étudiant respecte les conditions d'inscription pédagogique, d'assiduité
    et de présentation aux examens (non applicable si nouveau bachelier).
    L'étudiant éligible à la bourse sur critères sociaux et éligible à une aide au mérite
    en année universitaire N-1 et ayant réalisé un Service Civique
    au titre de cette même année, peut percevoir son aide au mérite en N.
    '''

    def formula(individu, period, parameters):
        # l'individu intègre un établissement supérieur à la rentrée
        etudiant = individu('etudiant', period)

        bourse_criteres_sociaux = individu("bourse_criteres_sociaux", period)
        allocation_annuelle_etudiant = individu("allocation_annuelle_etudiant", period)
        condition_ressources = (bourse_criteres_sociaux + allocation_annuelle_etudiant) > 0

        mention_baccalaureat = individu("mention_baccalaureat", period)
        condition_mention = mention_baccalaureat == TypesMention.mention_tres_bien

        # a déjà perçu l'aide l'année [universitaire] précédente
        annee_glissante = period.start.period('year').offset(-1).offset(-1, 'month')
        aide_merite_eligibilite_an_dernier = individu("aide_merite_eligibilite", annee_glissante, options = [ADD])

        return etudiant * condition_ressources * ( condition_mention + aide_merite_eligibilite_an_dernier )
