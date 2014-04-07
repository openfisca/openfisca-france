# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation de système socio-fiscal
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import division

from openfisca_core.columns import (EnumCol, IntCol, BoolCol, AgeCol, FloatCol, DateCol)

import openfisca_france

def check_consistency(table_simu, dataframe, corrige = True):
    '''
    Studies dataframe columns as described in a simulation table columns attribute, and should eventually
    TODO table_simu -> input_table
    Parameters
    ----------
    table_simu : datatable object, typically output table of a simulation
    dataframe : dataframe object that we want to compare
    corrige : if corrige is True, the function tries to correct errors in datatable by passing default values
    '''
    # check_inputs_enumcols(simulation):
    # TODO: eventually should be a method of SurveySimulation specific for france



    is_ok = True
    message = "\n"
    missing_variables = []
    unconsistent_variables = []
    present_variables = []
    count = 0

    from .data.erf.build_survey.utilitaries import control
    print 'Controlling simulation input_table'
    control(table_simu.table, verbose = True)

    # First : study of the datatable / the specification of columns given by table_simu
    for var, varcol in table_simu.column_by_name.iteritems():
        try:
            serie = dataframe[var]
            simu_serie = table_simu.table[var]
            present_variables.append(var)
            # First checks for all if there is any missing data
            if serie.isnull().any() or simu_serie.isnull().any():
                is_ok = False
                if serie.isnull().any():
                    message += "Some missing values in dataframe column %s, \n" % var
                if simu_serie.isnull().any():
                    message += 'Some missing values in input_table column %s \n' % var
                cnt = len(set(simu_serie.isnull())) - len(set(serie.isnull()))
                if 0 < cnt:
                    message += "Warning : %s More NA's in simulation than in original dataframe for %s \n" % (str(cnt), var)

                if corrige:
                    try:
                        message += "Filling NA's with default values for %s... \n" % var
                        serie[serie.isnull()] = varcol.default
                        message += "Done \n"
                    except:
                        message += " Cannot fill NA for column %s, maybe _.default doesn't exist \n" % var

            if not corrige:  # On ne modifie pas la série donc on peut l'amputer, elle n'est pas en return
                serie = serie[serie.notnull()]

            # Then checks if all values are of specified datatype
            # verify type, force type

            if isinstance(varcol, EnumCol):
                try:
                    if set(serie.unique()) > set(sorted(varcol.enum._nums.values())):
                        message += "Some variables out of range for EnumCol variable %s : \n" % var
                        message += str(set(serie.unique()) - set(sorted(varcol.enum._nums.values()))) + "\n"
                        # print varcol.enum._nums
                        # print sorted(serie.unique()), "\n"
                        is_ok = False

                except:
                    is_ok = False
                    message += "Error : no _num attribute for EnumCol.enum %s \n" % var
                    # print varcol.enum
                    # print sorted(serie.unique()), "\n"
                try:
                    varcol.enum._vars

                except:
                    is_ok = False
                    message += "Error : no _var attribute for EnumCol.enum %s \n" % var
                    # print varcol.enum
                    # print sorted(serie.unique())
                    # print "\n"
                try:
                    n = varcol.enum._count
                    if n < len(set(serie.unique())):
                        message += "More types of enum than expected : %s ( expected : %s) \n" % (str(set(serie.unique())), str(n))
                except:
                    message += "Error : no _count attribute for EnumCol.enum %s \n" % var
                try:
                    varcol.enum
                except:
                    is_ok = False
                    message += "Error : not enum attribute for EnumCol %s ! \n" % var
                    # Never happening, enum attribute is initialized to None at least

            if isinstance(varcol, IntCol):
                if serie.dtype not in ('int', 'int16', 'int32', 'int64'):
                    is_ok = False
                    # print serie[serie.notnull()]
                    message += "Some values in column %s are not integer as wanted: %s \n" % (var, serie.dtype)
                    stash = []
                    for v in serie:
                        if not isinstance(v, int):
                            stash.append(v)
                    message += str(list(set(stash))) + " \n"
                    if corrige:
                        message += "Warning, forcing type integer for %s..." % var
                        try:
                            serie = serie.astype(varcol.dtype)
                            message += "Done \n"
                        except:
                            message += "sorry, cannot force type.\n"
                else:
                    message += "Values for %s are in range [%s,%s]\n" % (var, str(serie.min()), str(serie.max()))


            if isinstance(varcol, BoolCol):
                if serie.dtype != 'bool':
                    is_ok = False
                    # print serie[serie.notnull()]
                    message += "Some values in column %s are not boolean as wanted \n" % var
                    if corrige:
                        message += "Warning, forcing type boolean for %s..." % var
                        try:
                            serie = serie.astype(varcol.dtype)
                            message += "Done \n"
                        except:
                            message += "sorry, cannot force type.\n"

            if isinstance(varcol, AgeCol):
                if not serie.dtype in ('int', 'int16', 'int32', 'int64'):
                    is_ok = False
                    message += "Age variable %s not of type int: \n"
                    stash = list(set(serie.value) - set(range(serie.min(), serie.max() + 1)))
                    message += str(stash) + "\n"
                    message += "Total frequency for non-integers for %s is %s \n" % (var, str(len(stash)))
                    if corrige:
                        pass

                if not serie.isin(range(-1, 156)).all():  # Pas plus vieux que 100 ans ?
                    is_ok = False
                    # print serie[serie.notnull()]
                    message += "Age variable %s not in wanted range: \n" % var
                    stash = list(set(serie.unique()) - set(range(-1, 156)))
                    message += str(stash) + "\n"
                    message += "Total frequency of outranges for %s is %s \n" % (var, str(len(stash)))
                    del stash
                    if corrige:
                        try:
                            message += "Fixing the outranges for %s... " % var
                            tmp = serie[serie.isin(range(-1, 156))]
                            serie[~(serie.isin(range(-1, 156)))] = tmp.median()
                            message += "Done \n"
                            del tmp
                        except:
                            message += "sorry, cannot fix outranges.\n"

            if isinstance(varcol, FloatCol):
                if serie.dtype not in ('float', 'float32', 'float64', 'float16'):
                    is_ok = False
                    message += "Some values in column %s are not float as wanted \n" % var
                    stash = list(set(serie.unique()) - set(range(serie.min(), serie.max() + 1)))
                    message += str(stash) + "\n"
                    message += "Total frequency for non-integers for %s is %s \n" % (var, str(len(stash)))

            if isinstance(varcol, DateCol):
                if serie.dtype != 'np.datetime64':
                    is_ok = False
                    # print serie[serie.notnull()]
                    message += "Some values in column %s are not of type date as wanted \n" % var

            if corrige:
                dataframe[var] = serie
            count += 1
            del serie, varcol



        except:
            is_ok = False
            missing_variables.append(var)
            # message = "Oh no ! Something went wrong in the tests. You may have coded like a noob"

    # TODO : Then, comparaison between datatable and table_simu.table ?

    if len(missing_variables) > 0:
        message += "Some variables were not present in the datatable or caused an error:\n" + str(sorted(missing_variables)) + "\n"
        message += "Variables present in both tables :\n" + str(sorted(present_variables)) + "\n"
    else:
        message += "All variables were present in the datatable and were handled without error \n"

    if is_ok:
        print "All is well. Sleep mode activated."
    else:
        print message

    if corrige:
        return dataframe
    else:
        return

    # NotImplementedError

from openfisca_core.formulas import AlternativeFormula, DatedFormula, SelectFormula, SimpleFormula


def find_ultimate_dependancies(variable_name, date, tax_benefit_system = None, input_variables = None):

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
            formula.extract_parameters()

        elif DatedFormula in column_formula_type:
            dated_formula_classes = column.formula_constructor.dated_formulas_class
            formula = [dated_formula_class['formula_class'] for dated_formula_class in dated_formula_classes if dated_formula_class['start'] <= date <= dated_formula_class['end']][0]

        elif SelectFormula in column_formula_type:
            formula = column.formula_constructor.formula_constructor_by_main_variable.items()[0][1]

        elif SimpleFormula in column_formula_type:
            formula = column.formula_constructor
            formula.extract_parameters()

        formula.set_dependencies(column, tax_benefit_system)

        for variable_name in  formula.parameters:
            find_ultimate_dependancies(variable_name, date, input_variables = input_variables)

    return list(input_variables)

def list_ultimate_dependancies(variable_name, date):
    result = sorted(find_ultimate_dependancies(variable_name, date, tax_benefit_system = None, input_variables = None))
    for variable in result:
        print variable
        if variable[-len("_holder"):] == "_holder":
            print variable[:-len("_holder")]
            result[result.index(variable)] = variable[:-len("_holder")]
    return sorted(result)
    #    print input_variables


def look_for(variable, year):
    import re
    matched = re.match('^f[1-8][a-z]{2}', variable)

    if matched is not None:
        section_number = variable[1]
        case = variable[2:4].upper()

    print "section", section_number
    print "case", case
    import webbrowser
    url_base = "http://www3.finances.gouv.fr/calcul_impot/" + str(year+1) + "/aides/"

    if section_number == "3":
        url_section = "gains_c.htm"
    if section_number == "4":
        url_section = "fonciers.htm"
    # if section_number =="5":
    #      url_section = "charges_s.htm#"
    if section_number =="6":
         url_section = "charges_s.htm#"
    if section_number =="7":
         url_section = "reductions_s.htm#"
    if section_number =="8":
         url_section = "autres_imputations_s.htm#"

    if section_number in ["3","4"]:
        url = url_base + url_section
    else:
        url = url_base + url_section + case

    webbrowser.open(url,new=2)



if __name__ == '__main__':
    from datetime import date
    print list_ultimate_dependancies('donapd', date(2012, 1, 1))
#    print list_ultimate_dependancies('decote', date(2012, 1, 1))
#    print list_ultimate_dependancies('salbrut', date(2012, 1, 1))
#    print list_ultimate_dependancies('age', date(2012, 1, 1))

    for year in range(2013, 2009,-1):
        look_for("f7ac", year)
