from openfisca_france.model.base import Individu, Variable, MONTH


class crous_logement_eligibilite(Variable):
    entity = Individu
    value_type = bool
    label = "Éligibilité aux logements proposés par le CROUS"
    definition_period = MONTH
    reference = "https://www.etudiant.gouv.fr/fr/comment-se-passe-l-attribution-des-logements-en-residence-73"

    def formula(individu, period):
        """
        Tous les étudiants sont éligibles aux logements proposés par le CROUS mais
        les non boursiers ont une probabilité très faible d'en obtenir.
        Pour une résidence donnée, les dossiers sont classés par « indice social » défini par :
        - revenu brut global (+ 1) divisé par le nombre total de points de charge (+ 1)
        Pour informer de façon pertinente c'est à dire sans trop de faux positif ni trop de faux négatifs,
        les étudiants boursiers sont considérés éligibles et les autre non
        """
        return individu('bourse_criteres_sociaux_echelon', period) >= 0
