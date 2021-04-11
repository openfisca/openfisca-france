from openfisca_france.model.base import *

from numpy import timedelta64

from openfisca_france.model.prestations.education import StatutsEtablissementScolaire


class aide_mobilite_internationale_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilite à l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        debut_etudes_etranger = individu('debut_etudes_etranger', period)
        fin_etudes_etranger = individu('fin_etudes_etranger', period)
        duree_etudes_etranger = (fin_etudes_etranger - debut_etudes_etranger).astype('timedelta64[M]')
        eligibilite_duree_min = duree_etudes_etranger >= timedelta64(parameters(period).prestations.aide_mobilite_internationale.duree_sejour.mois_min, 'M')
        eligibilite_duree_max = duree_etudes_etranger <= timedelta64(parameters(period).prestations.aide_mobilite_internationale.duree_sejour.mois_max, 'M')

        statuts_etablissement_scolaire = individu('statuts_etablissement_scolaire', period)
        etablissement_eligible = (statuts_etablissement_scolaire == StatutsEtablissementScolaire.public) + (statuts_etablissement_scolaire == StatutsEtablissementScolaire.prive_sous_contrat)

        bourse_criteres_sociaux_eligibilite = individu('bourse_criteres_sociaux_eligibilite', period)

        return bourse_criteres_sociaux_eligibilite * eligibilite_duree_min * eligibilite_duree_max * etablissement_eligible


class aide_mobilite_internationale(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu('bourse_criteres_sociaux_eligibilite', period) * parameters(period).prestations.aide_mobilite_internationale.montant
