#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import argparse
import datetime
import json
import logging
import os
import sys

from openfisca_core.formulas import AlternativeFormula, DatedFormula, SelectFormula, SimpleFormula
import openfisca_france


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def find_ultimate_dependencies(variable_name, date, tax_benefit_system = None, input_variables = None):
    if input_variables is None:
        input_variables = set()
    elif isinstance(input_variables, list):
        input_variables = set(input_variables)

    if tax_benefit_system is None:
        TaxBenefitSystem = openfisca_france.init_country()
        tax_benefit_system = TaxBenefitSystem()

    if variable_name not in TaxBenefitSystem.prestation_by_name:
        input_variables.add(variable_name)
        pass
    else:
        column = TaxBenefitSystem.prestation_by_name[variable_name]
        column_formula_type = column.formula_constructor.__bases__

        if AlternativeFormula in column_formula_type:
            formula = column.formula_constructor.alternative_formulas_constructor[0]
            formula.extract_variables_name()

        elif DatedFormula in column_formula_type:
            dated_formula_classes = column.formula_constructor.dated_formulas_class
            formula = [
                dated_formula_class['formula_class']
                for dated_formula_class in dated_formula_classes
                if dated_formula_class['start'] <= date <= dated_formula_class['end']
                ][0]

        elif SelectFormula in column_formula_type:
            formula = column.formula_constructor.formula_constructor_by_main_variable.items()[0][1]

        elif SimpleFormula in column_formula_type:
            formula = column.formula_constructor
            formula.extract_variables_name()

        formula.set_dependencies(column, tax_benefit_system.column_by_name)

        for variable_name in formula.variables_name:
            find_ultimate_dependencies(variable_name, date, input_variables = input_variables)

    return list(input_variables)


def list_ultimate_dependencies(variable_name, date):
    result = sorted(find_ultimate_dependencies(variable_name, date, tax_benefit_system = None, input_variables = None))
    for variable in result:
        if variable[-len("_holder"):] == "_holder":
            print variable[:-len("_holder")]
            result[result.index(variable)] = variable[:-len("_holder")]
    return sorted(result)


def main():
    mkdate = lambda datestring: datetime.datetime.strptime(datestring, '%Y-%m-%d').date()

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('variable_name', help = u'Name of the variable to list its dependencies. Example: "donapd"')
    parser.add_argument('date', help = u'Date to list dependencies. Example: 2012-1-1', type = mkdate)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "Increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    print json.dumps(list_ultimate_dependencies(args.variable_name, args.date), encoding = 'utf-8', indent = 2)
    # print list_ultimate_dependencies('donapd', date(2012, 1, 1))
    # print list_ultimate_dependencies('decote', date(2012, 1, 1))
    # print list_ultimate_dependencies('salbrut', date(2012, 1, 1))
    # print list_ultimate_dependencies('age', date(2012, 1, 1))


if __name__ == '__main__':
    sys.exit(main())
