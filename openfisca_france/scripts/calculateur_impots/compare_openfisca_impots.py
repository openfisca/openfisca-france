#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Compare income taxes computed by finances.gouv.fr web simulator with OpenFisca results for a given scenario."""

# TODO: reduce margin error from 2 to 0 by coding the floor and round rules


import argparse
import collections
import cStringIO
import logging
import os
import sys
import urllib
import urllib2

from lxml import etree

import openfisca_france
from openfisca_france.scripts.calculateur_impots.base import (
    call_tax_calculator,
    general_variable_name_by_tax_calculator_code,
    openfisca_variable_name_by_tax_calculator_code,
    transform_scenario_to_tax_calculator_inputs,
    )


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()
#tax_benefit_system.neutralize_variable('rpns_individu') # TODO: recheck this, for year before 2014 it doesn't work and the program stop due to rpns_individu


def compare(scenario, tested = False, verbose = False):
    """
        Function that computes the official DGFiP income tax simulation (loaded from its website) of a given scenario and compares 
        it to the OpenFisca income tax simulation. It compares the income tax amount but also all possible variables common to both 
        simulations.

        Parameters
        ---------
        scenario: 
        Scenario = year of simulation, family situation and income situation of the fiscal household considered

        tested: Default = False
        If tested = False, it will only return both simulations but won't do a comparison.
        
    """
    year = scenario.period.date.year
    assert year > 2010, 'The official DGFiP income tax simulator is available only since 2011 (year of income)'

    impots_arguments = transform_scenario_to_tax_calculator_inputs(scenario)
    simulation = scenario.new_simulation(debug = True)

    response_html = call_tax_calculator(year, impots_arguments)
    page_doc = etree.parse(cStringIO.StringIO(response_html), etree.HTMLParser())
    fields = collections.OrderedDict()
    names = general_variable_name_by_tax_calculator_code

    for element in page_doc.xpath('//input[@type="hidden"][@name]'):
        code = element.get('name')
        try:
            fields[code] = {
                'code': code,
                'name': names[code] if (code in names) else u'nom inconnu',
                'value': float(element.get('value').replace(" ", "").replace("*","")),
                'openfisca_name': openfisca_variable_name_by_tax_calculator_code.get(code),
                }
        except ValueError:
            fields[code] = {
                'code': code,
                'name': names[code] if (code in names) else u'nom inconnu',
                'value': element.get('value').replace(" ", ""),
                'openfisca_name': openfisca_variable_name_by_tax_calculator_code.get(code),
                }
        # Converting taxes into negative numbers (as in OpenFisca)
        if (fields[code]['code'] == "IINET") | (fields[code]['code'] == "IINETIR") | (fields[code]['code'] == "IRESTIR"):
            fields[code]['value'] = -fields[code]['value'] 

    # If the simulator has no fields IINETIR or IRESTIR, we take field IINET and compare it to the irpp variable of OpenFisca (even if these 2 variables are not entirely the same thing)
    if ("IINETIR" not in fields.keys()) and ("IRESTIR" not in fields.keys()) and ("IINET" in fields.keys()): 
        fields['IINET']['openfisca_name'] = "irpp"

    if tested:
        compare_variables(fields, simulation, verbose = verbose)

    return fields, simulation


def compare_variable(field, openfisca_variable_name, simulation, verbose = False):
    """
        Function that compares the value of a given variable from the DGFiP income tax simulation to the one of a given
        OpenFisca associated variable

        Parameters
        ---------
        field: 
        Contains the code, name and value of the output variable from the DGFiP income tax simulator

        openfisca_variable_name:
        Contains the name of the associated variable from OpenFisca

        simulation: 
        verbose: Default = False
        
    """
    code = field['code']
    name = field['name']
    dgfip_value = field['value']
    
    openfisca_value = simulation.calculate(openfisca_variable_name, simulation.period)
    openfisca_variable_name = field['openfisca_name']
    assert len(openfisca_value) == 1
    if verbose: 
        print(u'Comparaison DGFiP vs OpenFisca')
        if (openfisca_variable_name == 'nbptr'):
            print(u'{} ({}) = {}'.format(code, name, openfisca_variable_name).encode('utf-8'))
            print(u'{} vs {}'.format(dgfip_value, openfisca_value[0]).encode('utf-8'))
        else:
            print(u'{} ({}) = {}'.format(code, name, openfisca_variable_name).encode('utf-8'))
            print(u'{} vs {}'.format(round(dgfip_value), round(openfisca_value[0])).encode('utf-8'))


def compare_variables(fields, simulation, verbose = True):

    for code, field in fields.iteritems():
        openfisca_variable_name = field['openfisca_name']
        if openfisca_variable_name is not None:
            compare_variable(field, openfisca_variable_name, simulation, verbose)


def define_scenario(year, tax_benefit_system = tax_benefit_system):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = year,
        parent1 = dict(
            activite = u'actif',
            date_naissance = 1970,
            salaire_imposable = 200000,
            #retraite_imposable = 0,
            #chomage_imposable = 0,
            #nbic_mvct = 20000,
            #mbnc_mvct = 10000,
            # f6ss = 200,
            # f6ps = 200,
            statut_marital = u'marie',
            ),
        parent2 = dict(
             activite = u'actif',
             date_naissance = 1973,
             salaire_imposable = 15000,
             statut_marital = u'marie',
             ),
        # enfants = [
        #     dict(
        #          activite = u'etudiant',
        #          date_naissance = '1993-02-01',
        #          ),
        #     dict(
        #         activite = u'etudiant',
        #         date_naissance = '2000-04-17',
        #         ),
        #      ],
        foyer_fiscal = dict(
            #f8ta = 20000,
            #f6ps = 10000,
            # f2ch = 100,
            # f2dc = 500,
            # f2fu = 1000,
            # f2go = 1000,
            # f2tr = 5000,
            # f2ts = 9000,
            # f2ab = 10000,
            #f8vm = 10000,
            ),
        )
    scenario.suggest()
    return scenario


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    year = 2017 # Année de revenus
    scenario = define_scenario(year)
    compare(scenario, tested = True, verbose = True)
    return 0


if __name__ == "__main__":
   sys.exit(main())