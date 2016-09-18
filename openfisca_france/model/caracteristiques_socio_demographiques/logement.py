# -*- coding: utf-8 -*-

from numpy import logical_not as not_, logical_or as or_
from numpy.core.defchararray import startswith


from openfisca_france.model.base import *  # noqa analysis:ignore


class coloc(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Vie en colocation"

class logement_chambre(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Le logement est considéré comme une chambre"


class loyer(Variable):
    column = FloatCol()
    entity_class = Menages
    set_input = set_input_divide_by_period
    label = u"Loyer ou mensualité d'emprunt pour un primo-accédant"

class loyer_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"Zone apl de la personne"
    variable = loyer
class depcom(Variable):
    column = FixedStrCol(max_length = 5)
    entity_class = Menages
    label = u"Code INSEE (depcom) du lieu de résidence"

class loyer_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Zone apl de la famille"
    role = CHEF
    variable = loyer_individu

class charges_locatives(Variable):
    column = FloatCol()
    entity_class = Menages
    set_input = set_input_divide_by_period
    label = u'Charges locatives'

class proprietaire_proche_famille(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint"

class habite_chez_parents(Variable):
    column = BoolCol
    entity_class = Individus
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
    entity_class = Menages
    label = u"Statut d'occupation du logement"
    set_input = set_input_dispatch_by_period


class residence_dom(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        residence_guadeloupe = simulation.calculate('residence_guadeloupe', period)
        residence_martinique = simulation.calculate('residence_martinique', period)
        residence_guyane = simulation.calculate('residence_guyane', period)
        residence_reunion = simulation.calculate('residence_reunion', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)
        return period, or_(or_(residence_guadeloupe, residence_martinique), or_(or_(residence_reunion, residence_guyane), residence_mayotte))


class residence_guadeloupe(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '971')


class residence_martinique(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '972')


class residence_guyane(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '973')


class residence_reunion(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '974')


class residence_mayotte(Variable):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '976')
