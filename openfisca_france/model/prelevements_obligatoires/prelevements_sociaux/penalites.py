# -*- coding: utf-8 -*-

from __future__ import division

import logging


from numpy import logical_not as not_


from openfisca_core.formulas import SimpleFormulaColumn


from ...base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# TODO: mettre les seuils entreprises dans les paramètres


@reference_formula
class penalite_egalite_professionnelle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pénalité visant à favoriser l'égalité professionnelle homme-femme"
    start_date = "2012-01-01"

    def function(self, simulation, period):
        egalite_professionnelle_accord = simulation.calculate('egalite_professionnelle_accord', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = 0  # TODO: comment coder taux ? nouvelle variable ? Dans la loi < 1% déterminé par la direccte
        return period, not_(egalite_professionnelle_accord) * (effectif_entreprise >= 50) * taux


@reference_formula
class penalite_emploi_jeunes(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pénalité visant à favoriser l'emploi des jeunes"
    start_date = "2010-01-01"
    end_date = "2013-09-30"

    def function(self, simulation, period):
        emploi_jeunes_accord = simulation.calculate('emploi_jeunes_accord', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = 0  # TODO: comment coder taux ? nouvelle variable ?
        return period, not_(emploi_jeunes_accord) * (effectif_entreprise >= 300) * taux


@reference_formula
class penalite_emploi_seniors(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pénalité visant à favoriser l'emploi des séniors"
    start_date = "2010-01-01"
    end_date = "2013-09-30"

    def function(self, simulation, period):
        emploi_senior_accord = simulation.calculate('emploi_senior_accord', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = 0  # TODO: comment coder taux ? nouvelle variable ? 1% ?
        return period, not_(emploi_senior_accord) * (effectif_entreprise >= 50) * taux


@reference_formula
class penalite_penibilite(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pénalité visant à favoriser la prévention de la pénibilité"
    # TODO start_date

    def function(self, simulation, period):
        penibilite_prevention_accord = simulation.calculate('penibilite_prevention_accord', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = 0  # TODO: quel taux ?
        return period, not_(penibilite_prevention_accord) * (effectif_entreprise >= 50) * taux


@reference_formula
class penalite_handicapes(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pénalité pour emploi insuffisant de personnes handicapées"
    # TODO start_date

    def function(self, simulation, period):
        # les entreprises sont soumises à une obligation d’emploi en faveur des travailleurs handicapés.
        # Toute entreprise (privée ou public) doit compter au moins 6% de
        # travailleurs ayant une reconnaissance administrative de handicap parmi ses
        # effectifs salariés. A défaut, l’employeur peut verser une contribution annuelle
        # proportionnelle au nombre de salariés handicapés qu’il aurait dû recruter pour
        # remplir son obligation d’emploi.
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, 0 * effectif_entreprise

# TODO penibilite CDD évoquée page 11 du guide IPP est-elle la cotisation pour le CIF des CDD ?
