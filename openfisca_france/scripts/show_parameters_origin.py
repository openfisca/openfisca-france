#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""For each parameter of the tax and benefit system, show its origin."""


import argparse
import collections
import pkg_resources
import json
import logging
import os
import sys

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
            both_origins = node_json.get('both_origins')
            if both_origins is not None:
                parameter_json['both_origins'] = both_origins
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


def get_parameters_origin_dataframe():
    tax_benefit_system = FranceTaxBenefitSystem()
    legislation_json = tax_benefit_system.get_legislation(with_source_file_infos=True)
    parameters_json = get_flat_parameters(legislation_json)
    result = dict()
    for parameter_json in parameters_json:
        if 'origin' in parameter_json or 'both_origins' in parameter_json:
            result[parameter_json['name']] = dict(
                origin = parameter_json['origin'] if 'origin' in parameter_json else None,
                both_origins = True if parameter_json.get('both_origins') else False,
                )

    import pandas as pd
    return pd.DataFrame.from_dict(result, orient = 'index')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    tax_benefit_system = FranceTaxBenefitSystem()
    legislation_json = tax_benefit_system.get_legislation(with_source_file_infos=True)
    parameters_json = get_flat_parameters(legislation_json)
    for parameter_json in parameters_json:
        if 'origin' in parameter_json or 'both_origins' in parameter_json:
            print(u'{}: {}'.format(
                parameter_json['name'],
                u' '.join(filter(None, [
                    u'origin={}'.format(parameter_json['origin'])
                    if 'origin' in parameter_json
                    else None,
                    u'both_origins (cf param-to-parameters.yaml)'.format(parameter_json['both_origins'])
                    if parameter_json.get('both_origins')
                    else None,
                    ]))
                )).encode('utf-8')
        else:
            print(u'{}: no origin'.format(parameter_json['name'])).encode('utf-8')



if __name__ == "__main__":
    sys.exit(main())
