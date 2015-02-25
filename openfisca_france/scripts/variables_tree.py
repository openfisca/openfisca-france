#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import pyclbr


import openfisca_france

TaxBenfitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenfitSystem()


def print_computed_variables():
    def set_deep_key(modified_dict, keys, value):
        last_key = keys.pop()
        for key in keys:
            modified_dict = modified_dict.setdefault(key, {})
        modified_dict.setdefault(last_key, []).append(value)
        modified_dict[last_key] = sorted(modified_dict[last_key])

    modules_name = [
        module_name for module_name in sys.modules.keys()
        if module_name.startswith('openfisca_france.model') and not module_name.endswith('__future__')]

    keys_by_class_name = {}
    for module_name in modules_name:
        try:
            classes_data = pyclbr.readmodule(module_name)
        except:
            classes_data = dict()

        for class_name, class_data in classes_data.items():
            if class_name in tax_benefit_system.column_by_name.keys():
                keys_by_class_name[class_name] = module_name.split('.')[1:]

    # print sorted(computed_variable_names)

    computed_variables = dict()
    for class_name, keys in keys_by_class_name.iteritems():
        set_deep_key(computed_variables, keys, class_name)

    import pprint
    pprint.pprint(computed_variables)

    log_file = open('variables' + '.txt', 'w')
    pprint.pprint(computed_variables, stream = log_file, indent = 2)


def print_input_variables():

    modules_name = [
        module_name for module_name in sys.modules.keys()
        if module_name.startswith('openfisca_france.model.input_variables') and not module_name.endswith('__future__')]

    keys_by_class_name = {}
    for module_name in modules_name:
        try:
            classes_data = pyclbr.readmodule(module_name)
        except:
            classes_data = dict()

        for class_name, class_data in classes_data.items():
            if class_name in tax_benefit_system.column_by_name.keys():
                print module_name, class_name
                keys_by_class_name[class_name] = module_name.split('.')[1:]


if __name__ == '__main__':

    print_computed_variables()
