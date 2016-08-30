#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""For each parameter of the tax and benefit system, show its origin."""


import argparse
import collections
import pkg_resources
import logging
import os
import sys

from openfisca_parsers import input_variables_extractors

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem


app_name = os.path.splitext(os.path.basename(__file__))[0]
country_package_dir_path = pkg_resources.get_distribution('OpenFisca-France').location
log = logging.getLogger(app_name)


def get_relative_file_path(absolute_file_path):
    '''
    Example:
    absolute_file_path = "/home/xxx/Dev/openfisca/openfisca-france/openfisca_france/param/param.xml"
    result = "openfisca_france/param/param.xml"
    '''
    global country_package_dir_path
    assert country_package_dir_path is not None
    relative_file_path = absolute_file_path[len(country_package_dir_path):]
    if relative_file_path.startswith('/'):
        relative_file_path = relative_file_path[1:]
    return relative_file_path


def get_flat_parameters(legislation_json):
    # Adapted from openfisca_web_api.environment
    def walk_legislation_json(node_json, parameters_json, names):
        children_json = node_json.get('children') or None
        if children_json is None:
            parameter_json = node_json.copy()  # No need to deepcopy since it is a leaf.
            parameter_json['name'] = u'.'.join(names)
            origin = node_json.get('origin')
            if origin is not None:
                parameter_json['origin'] = origin
            if 'xml_file_path' in node_json:
                parameter_json['xml_file_path'] = get_relative_file_path(node_json['xml_file_path'])
            parameter_json = collections.OrderedDict(sorted(parameter_json.iteritems()))
            parameters_json.append(parameter_json)
        else:
            for child_name, child_json in children_json.iteritems():
                walk_legislation_json(
                    names=names + [child_name],
                    node_json=child_json,
                    parameters_json=parameters_json,
                    )

    parameters_json = []
    walk_legislation_json(
        names=[],
        node_json=legislation_json,
        parameters_json=parameters_json,
        )
    return parameters_json


def suppress_stdout(f):
    def _suppress_stdout(*args, **kwargs):
        import sys
        from cStringIO import StringIO
        backup = sys.stdout
        try:
            sys.stdout = StringIO()
            result = f(*args, **kwargs)
        finally:
            sys.stdout.close()
            sys.stdout = backup
        return result
    return _suppress_stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    tax_benefit_system = FranceTaxBenefitSystem()

    parser = input_variables_extractors.setup(tax_benefit_system)
    captured_get_input_variables_and_parameters = suppress_stdout(parser.get_input_variables_and_parameters)
    variable_names_by_parameter_name = collections.defaultdict(list)
    for column in tax_benefit_system.column_by_name.values():
        _, parameter_names = captured_get_input_variables_and_parameters(column)
        if parameter_names is not None:
            for parameter_name in parameter_names:
                variable_names_by_parameter_name[parameter_name].append(column.name)

    legislation_json = tax_benefit_system.get_legislation(with_source_file_infos=True)
    parameters_json = get_flat_parameters(legislation_json)
    for parameter_json in parameters_json:
        variable_names = variable_names_by_parameter_name.get(parameter_json['name'])
        print(u'{}: {}'.format(
            parameter_json['name'],
            u' ; '.join(filter(None, [
                u'used by variables: {}'.format(u', '.join(variable_names))
                if variable_names is not None else 'used by no variable',
                u'origin: {}'.format(parameter_json['origin'])
                if 'origin' in parameter_json
                else None,
                u'conflicts: {}'.format(u', '.join(parameter_json['conflicts']))
                if 'conflicts' in parameter_json
                else None,
                ]))
            )).encode('utf-8')


if __name__ == "__main__":
    sys.exit(main())
