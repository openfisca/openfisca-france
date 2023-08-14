from openfisca_france.model.base import *

from numpy import timedelta64

from openfisca_france.model.prestations.education import StatutsEtablissementScolaire


class aide_mobilite_internationale_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilite à l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        '''
        Conditions non modélisées :
        - Éligibilité des boursiers bénéficiaires d'une allocation annuelle (dispositif des aides spécifiques).
        - La formation ou stage à l'étranger s'inscrit dans le cadre du cursus d'études.
        - Au cours de l'ensemble des études supérieures, ne peuvent être cumulés plus 9 mois d'aide à la mobilité internationale (sauf pour les étudiants ayant perçu neuf mensualités de l'aide à la mobilité internationale et dont le séjour à l'étranger a été interrompu en raison de l'épidémie de Covid-19, qui peuvent bénéficier de mensualités supplémentaires dans le cadre d'une mobilité ultérieure, dans la limite de la durée de la mobilité non effectuée.)
        '''
        debut_etudes_etranger = individu('debut_etudes_etranger', period)
        fin_etudes_etranger = individu('fin_etudes_etranger', period)
        duree_etudes_etranger = (fin_etudes_etranger - debut_etudes_etranger).astype('timedelta64[M]')
        eligibilite_duree_min = duree_etudes_etranger >= timedelta64(parameters(period).prestations_sociales.education.mobilite.internationale.duree_sejour.mois_min, 'M')
        eligibilite_duree_max = duree_etudes_etranger <= timedelta64(parameters(period).prestations_sociales.education.mobilite.internationale.duree_sejour.mois_max, 'M')

        statuts_etablissement_scolaire = individu('statuts_etablissement_scolaire', period)
        etablissement_eligible = (statuts_etablissement_scolaire == StatutsEtablissementScolaire.public) + (statuts_etablissement_scolaire == StatutsEtablissementScolaire.prive_sous_contrat)

        bourse_criteres_sociaux_eligibilite = individu('bourse_criteres_sociaux_eligibilite', period)

        return bourse_criteres_sociaux_eligibilite * eligibilite_duree_min * eligibilite_duree_max * etablissement_eligible


class aide_mobilite_internationale(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Circulaire du 8-6-2020 - Modalités d’attribution des bourses d’enseignement supérieur - Annexe 9 : Aide à la mobilité internationale',
        'https://www.enseignementsup-recherche.gouv.fr/pid20536/bulletin-officiel.html?cid_bo=152353&cbo=1',
        ]

    def formula(individu, period, parameters):
        '''
        Ce calcul ne détermine qu'une éligibilité potentielle et n'ouvre pas de droits : l'aide est accordée par une évaluation de l'établissement d'origine, en fonction de la durée de votre séjour et de certaines spécificités telles que l'éloignement du pays d'accueil, le coût de la vie du pays choisi.
        '''
        return individu('aide_mobilite_internationale_eligibilite', period) * parameters(period).prestations_sociales.education.mobilite.internationale.montant
