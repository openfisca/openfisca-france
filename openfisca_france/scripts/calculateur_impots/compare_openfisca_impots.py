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
tax_benefit_system.neutralize_variable('rpns_individu') # TODO: recheck this, for year before 2014 it doesn't work and the program stop due to rpns_individu


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
    assert year > 2010, 'ERROR : the official DGFiP income tax simulator is available only since 2011 (year of income)'

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
                'value': round(float(element.get('value').replace(" ", ""))), 
                }
        except ValueError:
            fields[code] = {
                'code': code,
                'name': names[code] if (code in names) else u'nom inconnu',
                'value': element.get('value').replace(" ", ""),
                }

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
    # Prise en compte du fait que irpp est sous format négatif
    if (openfisca_variable_name == "irpp") | (openfisca_variable_name == "irpp_noncale"):
        dgfip_value = - dgfip_value
    
    openfisca_value = simulation.calculate(openfisca_variable_name, simulation.period)
    field['openfisca_name'] = openfisca_variable_name
    assert len(openfisca_value) == 1
    if verbose:
        print(u'{} ({}) = {}'.format(code, name, openfisca_variable_name).encode('utf-8'))
        print(u'{} vs {}'.format(dgfip_value, round(openfisca_value[0])).encode('utf-8'))


def compare_variables(fields, simulation, verbose = True):
    iinet = 1

    for code, field in fields.iteritems():
        if code == 'IINETIR' or code == 'IRESTIR':
            iinet = 0
        openfisca_variable_name = openfisca_variable_name_by_tax_calculator_code.get(code)
        
        # Prise en compte des calages dans branche Taxipp d'OpenFisca-france
        if openfisca_variable_name == "irpp" :
            openfisca_variable_name = "irpp_noncale"

        if openfisca_variable_name is not None:
            compare_variable(field, openfisca_variable_name, simulation, verbose)

     # S'il n'y a pas IINETIR et IRESTIR dans les résultats, on compare irpp à IINET (pas exactement la même chose)
    if iinet:
        compare_variable(fields['IINET'], 'irpp_noncale', simulation, verbose)


def define_scenario(year, tax_benefit_system = tax_benefit_system):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = year,
        parent1 = dict(
            activite = u'Actif occupé',
            date_naissance = 1973,
            salaire_imposable = 15000,
            retraite_imposable = 0,
            chomage_imposable = 0,
            statut_marital = u'Marié',
            ),
        parent2 = dict(
             activite = u'Actif occupé',
             date_naissance = 1973,
             salaire_imposable = 38000,
             statut_marital = u'Marié',
             ),
        enfants = [
             dict(
                 activite = u'Étudiant, élève',
                 date_naissance = '1993-02-01',
                 ),
        #     dict(
        #         activite = u'Étudiant, élève',
        #         date_naissance = '2000-04-17',
        #         ),
             ],
        # foyer_fiscal = dict(  #TODO: pb avec f2ck
        #     f5rn = 5000,
        #     mbic_mvct = 2000,
        #     ),
        )
    scenario.suggest()
    return scenario


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    year = 2014
    scenario = define_scenario(year)
    compare(scenario, tested = True)
    return 0


if __name__ == "__main__":
   sys.exit(main())