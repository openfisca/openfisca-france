from openfisca_core.periods import Instant, Period
from openfisca_france.model.base import *


class aide_merite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide au mérite"
    definition_period = MONTH
    reference = [
        'https://www.etudiant.gouv.fr/fr/aide-au-merite-1291',
        'https://www.service-public.fr/particuliers/vosdroits/F1010',
        'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000030722211/'
        ]
    set_input = set_input_dispatch_by_period
    documentation = '''
    Complémentaire à la bourse sur critères sociaux, pour les étudiants
    ayant eu mention très bien au baccalauréat.

    Non modélisé :
    L'étudiant respecte les conditions d'inscription pédagogique, d'assiduité
    et de présentation aux examens (non applicable si nouveau bachelier)
    ou redouble pour raisons médicales.
    L'étudiant éligible à la bourse sur critères sociaux et éligible à une aide au mérite
    en année universitaire N-1 et ayant réalisé un Service Civique
    au titre de cette même année, peut percevoir son aide au mérite en N.
    Un étudiant ne peut bénéficier de plus de 3 fois de l'aide au mérite.
    '''

    def formula(individu, period):

        def periode_universitaire_precedente(mois_calcul):
            nb_mois_annee_courante = mois_calcul.date.month - mois_calcul.this_year.date.month + 1

            # https://www.campusfrance.org/fr/node/2176
            if nb_mois_annee_courante < 9:
                debut_annee_courante = mois_calcul.last_year
            else:
                debut_annee_courante = mois_calcul.this_year

            rentree_an_passe = Instant((debut_annee_courante.offset(-1), 9, 1))
            periode_universitaire_precedente = str(Period((MONTH, rentree_an_passe, 10)))
            return periode_universitaire_precedente

        # l'individu intègre un établissement supérieur à la rentrée
        etudiant = individu('etudiant', period)

        bourse_criteres_sociaux = individu('bourse_criteres_sociaux', period)
        allocation_annuelle_etudiant = individu('allocation_annuelle_etudiant', period)
        condition_ressources = (bourse_criteres_sociaux + allocation_annuelle_etudiant) > 0

        mention_baccalaureat = individu('mention_baccalaureat', period)
        condition_mention = (
            (mention_baccalaureat == TypesMention.mention_tres_bien)
            + (mention_baccalaureat == TypesMention.mention_tres_bien_felicitations_jury)
            )

        # a déjà perçu l'aide l'année [universitaire] précédente
        periode_universitaire_precedente = periode_universitaire_precedente(period)
        aide_merite_eligibilite_an_dernier = individu(
            'aide_merite_eligibilite',
            periode_universitaire_precedente,
            options = [ADD]
            )

        return etudiant * condition_ressources * (condition_mention + aide_merite_eligibilite_an_dernier)


class aide_merite_montant(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide au mérite pour l'année universitaire"
    definition_period = MONTH
    reference = [
        'https://www.etudiant.gouv.fr/fr/aide-au-merite-1291',
        'https://www.service-public.fr/particuliers/vosdroits/F1010',
        'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000030722211/'
        ]
    documentation = '''
    Aide versée en 9 mensualités.

    Non modélisé :
    Pour un baccalauréat obtenu avant 2015, quelques conditions d'attribution diffèrent
    et le montant de l'aide est de 1800€/an.
    '''

    def formula(individu, period, parameters):
        aide_merite_eligibilite = individu('aide_merite_eligibilite', period.first_month)
        return aide_merite_eligibilite * parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.aide_merite.montant_annuel
