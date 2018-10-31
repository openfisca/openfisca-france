# -*- coding: utf-8 -*-

from numpy.core.defchararray import startswith


from openfisca_france.model.base import *


class coloc(Variable):
    value_type = bool
    entity = Menage
    label = u"Vie en colocation"
    definition_period = MONTH


class logement_crous(Variable):
    value_type = bool
    entity = Menage
    label = u"Le logement est gérée par les CROUS "
    definition_period = MONTH


class logement_chambre(Variable):
    value_type = bool
    entity = Menage
    label = u"Le logement est considéré comme une chambre"
    definition_period = MONTH


class loyer(Variable):
    value_type = float
    entity = Menage
    set_input = set_input_divide_by_period
    label = u"Loyer ou mensualité d'emprunt pour un primo-accédant"
    definition_period = MONTH


class depcom(Variable):
    value_type = str
    max_length = 5
    entity = Menage
    label = u"Code INSEE (depcom) du lieu de résidence"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class charges_locatives(Variable):
    value_type = float
    entity = Menage
    set_input = set_input_divide_by_period
    label = u'Charges locatives'
    definition_period = MONTH


class proprietaire_proche_famille(Variable):
    value_type = bool
    entity = Famille
    label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint"
    definition_period = MONTH


class habite_chez_parents(Variable):
    value_type = bool
    entity = Individu
    label = u"L'individu habite chez ses parents"
    definition_period = MONTH


class statut_occupation_logement(Variable):
    value_type = Enum
    possible_values = TypesStatutOccupationLogement  # defined in model/base.py
    entity = Menage
    default_value = TypesStatutOccupationLogement.non_renseigne
    label = u"Statut d'occupation du logement"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class residence_dom(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period):
        residence_guadeloupe = menage('residence_guadeloupe', period)
        residence_martinique = menage('residence_martinique', period)
        residence_guyane = menage('residence_guyane', period)
        residence_reunion = menage('residence_reunion', period)
        residence_mayotte = menage('residence_mayotte', period)

        return residence_guadeloupe + residence_martinique + residence_reunion + residence_guyane + residence_mayotte


class residence_guadeloupe(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'971')


class residence_martinique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'972')


class residence_guyane(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'973')


class residence_reunion(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'974')


class residence_mayotte(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'976')


class residence_saint_bartelemy(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'977')


class residence_saint_martin(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'978')
