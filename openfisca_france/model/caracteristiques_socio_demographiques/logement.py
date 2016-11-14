# -*- coding: utf-8 -*-

from numpy import logical_not as not_, logical_or as or_
from numpy.core.defchararray import startswith


from openfisca_france.model.base import *  # noqa analysis:ignore

class coloc(Variable):
    column = BoolCol
    entity = Menage
    label = u"Vie en colocation"

class logement_chambre(Variable):
    column = BoolCol
    entity = Menage
    label = u"Le logement est considéré comme une chambre"

class loyer(Variable):
    column = FloatCol
    entity = Menage
    set_input = set_input_divide_by_period
    label = u"Loyer ou mensualité d'emprunt pour un primo-accédant"

class depcom(Variable):
    column = FixedStrCol(max_length = 5)
    entity = Menage
    label = u"Code INSEE (depcom) du lieu de résidence"

class charges_locatives(Variable):
    column = FloatCol
    entity = Menage
    set_input = set_input_divide_by_period
    label = u'Charges locatives'

class proprietaire_proche_famille(Variable):
    column = BoolCol
    entity = Famille
    label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint"

class habite_chez_parents(Variable):
    column = BoolCol
    entity = Individu
    label = u"L'individu habite chez ses parents"

class statut_occupation_logement(Variable):
    column = EnumCol(
        enum = Enum([
            u"Non renseigné",
            u"Accédant à la propriété",
            u"Propriétaire (non accédant) du logement",
            u"Locataire d'un logement HLM",
            u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
            u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
            u"Logé gratuitement par des parents, des amis ou l'employeur",
            u"Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)",
            u"Sans domicile stable"])
    )
    entity = Menage
    label = u"Statut d'occupation du logement"
    set_input = set_input_dispatch_by_period

class residence_dom(Variable):
    column = BoolCol
    entity = Menage

    def function(menage, period):
        residence_guadeloupe = menage('residence_guadeloupe', period)
        residence_martinique = menage('residence_martinique', period)
        residence_guyane = menage('residence_guyane', period)
        residence_reunion = menage('residence_reunion', period)
        residence_mayotte = menage('residence_mayotte', period)

        return period, residence_guadeloupe + residence_martinique + residence_reunion +residence_guyane + residence_mayotte


class residence_guadeloupe(Variable):
    column = BoolCol
    entity = Menage

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        return period, startswith(depcom, '971')


class residence_martinique(Variable):
    column = BoolCol
    entity = Menage

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        return period, startswith(depcom, '972')


class residence_guyane(Variable):
    column = BoolCol
    entity = Menage

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        return period, startswith(depcom, '973')


class residence_reunion(Variable):
    column = BoolCol
    entity = Menage

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        return period, startswith(depcom, '974')


class residence_mayotte(Variable):
    column = BoolCol
    entity = Menage

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        return period, startswith(depcom, '976')
