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


from __future__ import division

from openfisca_core.formulas import AlternativeFormula, DatedFormula, SelectFormula, SimpleFormula
import openfisca_france


# BROWSER_NAME = 'iceweasel'
BROWSER_NAME = 'chromium'


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
        print variable
        if variable[-len("_holder"):] == "_holder":
            print variable[:-len("_holder")]
            result[result.index(variable)] = variable[:-len("_holder")]
    return sorted(result)
    #    print input_variables


def look_for(variable, year):
    # Attention les liens changent entre la version simplifiée
    import re
    matched = re.match('^f[1-8][a-z]{2}', variable)

    if matched is not None:
        section_number = variable[1]
        case = variable[2:4].upper()

    print "section", section_number
    print "case", case
    import webbrowser
    url_base = "http://www3.finances.gouv.fr/calcul_impot/" + str(year + 1) + "/aides/"
    if section_number == "2":
        url_section = "capitaux_mobiliers.htm#"
    if section_number == "3":
        url_section = "gains_c.htm"
    if section_number == "4":
        url_section = "fonciers.htm"
    # if section_number =="5":
    #      url_section = "charges_s.htm#"
    if section_number == "6":
        url_section = "charges.htm#"
    if section_number == "7":
        url_section = "reductions.htm#"
    if section_number == "8":
        url_section = "autres_imputations.htm#"

    if section_number in ["3", "4"]:
        url = url_base + url_section
    else:
        url = url_base + url_section + case

    browser = webbrowser.get(BROWSER_NAME)
    browser.open_new_tab(url)


if __name__ == '__main__':
    from datetime import date
    print list_ultimate_dependencies('donapd', date(2012, 1, 1))
    # print list_ultimate_dependencies('decote', date(2012, 1, 1))
    # print list_ultimate_dependencies('salbrut', date(2012, 1, 1))
    # print list_ultimate_dependencies('age', date(2012, 1, 1))

    for year in range(2013, 2009, -1):
        look_for("f7wr", year)
