# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore

build_column('indemnites_journalieres_maternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de maternité"))
build_column('indemnites_journalieres_paternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de paternité"))
build_column('indemnites_journalieres_adoption', FloatCol(entity = 'ind', label = u"Indemnités journalières d'adoption"))
build_column('indemnites_journalieres_maladie', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie"))
build_column('indemnites_journalieres_accident_travail', FloatCol(entity = 'ind', label = u"Indemnités journalières d'accident du travail"))
build_column('indemnites_journalieres_maladie_professionnelle', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie professionnelle"))


class indemnites_journalieres(Variable):
    column = FloatCol
    label = u"Total des indemnités journalières"
    entity_class = Individus

    def function(self, simulation, period):
        ressources = [
            'indemnites_journalieres_maternite',
            'indemnites_journalieres_paternite',
            'indemnites_journalieres_adoption',
            'indemnites_journalieres_maladie',
            'indemnites_journalieres_accident_travail',
            'indemnites_journalieres_maladie_professionnelle',
            ]
        total = sum(simulation.calculate(ressource, period) for ressource in ressources)

        return period, total


class indemnites_journalieres_imposables(Variable):
    column = FloatCol
    label = u"Total des indemnités journalières imposables"
    entity_class = Individus
    url = "http://vosdroits.service-public.fr/particuliers/F3152.xhtml"

    def function(self, simulation, period):
        indemnites_journalieres = simulation.calculate('indemnites_journalieres', period)
        indemnites_journalieres_accident_travail = simulation.calculate('indemnites_journalieres_accident_travail', period)
        indemnites_journalieres_maladie_professionnelle = simulation.calculate('indemnites_journalieres_accident_travail', period)
        result = indemnites_journalieres - 0.5 * (
            indemnites_journalieres_accident_travail + indemnites_journalieres_maladie_professionnelle
        )

        return period, result
