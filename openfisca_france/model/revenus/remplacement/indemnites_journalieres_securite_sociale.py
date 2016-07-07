# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

class indemnites_journalieres_maternite(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières de maternité"


class indemnites_journalieres_paternite(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières de paternité"


class indemnites_journalieres_adoption(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières d'adoption"


class indemnites_journalieres_maladie(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières de maladie"


class indemnites_journalieres_accident_travail(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières d'accident du travail"


class indemnites_journalieres_maladie_professionnelle(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités journalières de maladie professionnelle"




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
