#! /usr/bin/env python
# -*- coding: utf-8 -*-

from openfisca_core import conv
from openfisca_france.scripts.calculateur_impots import base


def define_single_worker_scenario(year, value_by_variable):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a single childless working person)
        from a list of incomes and their amount.

        Parameters
        ---------
        year:
        Year of income

        value_by_variable:
        List of income variables and associated amounts

    """
    scenario = base.tax_benefit_system.new_scenario() # add_variable(), add_column()
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": 1970,
        "statut_marital": u'Célibataire',
        }
    enfants = [
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict()

    for variable, value in value_by_variable.iteritems():
        column = base.tax_benefit_system.column_by_name[variable]
        entity = column.entity.key

        start = 1990 if column.start is None else column.start.year
        end = 2050 if column.end is None else column.end.year
        value = value if conv.test_between(start, end)(year)[1] is None else 0

        if entity == 'individu':
            parent1[variable] = value
        elif entity == 'foyer_fiscal':
            foyer_fiscal[variable] = value
        elif entity == 'famille':
            famille[variable] = value
        elif entity == 'menage':
            menage[variable] = value

    scenario.init_single_entity(
        period = year,
        parent1 = parent1,
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        )
   
    scenario.suggest()
    return scenario