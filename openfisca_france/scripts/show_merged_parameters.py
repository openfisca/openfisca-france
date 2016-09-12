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
import yaml

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem


country_package_dir_path = pkg_resources.get_distribution('OpenFisca-France').location

package_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
param_dir = os.path.join(package_dir, 'param')

app_name = os.path.splitext(os.path.basename(__file__))[0]
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


def get_attributes_by_parameter_name(param_translations, tax_benefit_system, variable_names_by_parameter_name):
    with open(param_translations) as param_translations_file:
        param_translations = yaml.load(param_translations_file)
    original_name_by_name = {
        value: key
        for key, value in param_translations.iteritems()
        if value
        }
    legislation_json = tax_benefit_system.get_legislation(with_source_file_infos=True)
    parameters_json = get_flat_parameters(legislation_json)
    attributes_by_parameter_name = dict()
    for parameter_json in parameters_json:
        name = parameter_json['name']
        attributes_by_parameter_name[name] = dict(
            used_by_variables = variable_names_by_parameter_name.get(name),
            description = parameter_json.get('description'),
            origin = parameter_json['origin'],
            original_name = original_name_by_name.get(name) if parameter_json['origin'] == 'ipp' else None,
            conflicts = parameter_json.get('conflicts') if name not in conflicting_parameters_to_ignore else None,
            )
    return attributes_by_parameter_name


def get_attributes_by_parameter_name_dataframe():
    tax_benefit_system = FranceTaxBenefitSystem()
    variable_names_by_parameter_name = get_variable_names_by_parameter_name(tax_benefit_system)
    attributes_by_parameter_name = get_attributes_by_parameter_name(
        param_translations = os.path.join(param_dir, 'param-to-parameters.yaml'),
        tax_benefit_system = tax_benefit_system,
        variable_names_by_parameter_name = variable_names_by_parameter_name,
        )
    import pandas as pd
    return pd.DataFrame.from_dict(attributes_by_parameter_name, orient = 'index')


def get_variable_names_by_parameter_name(tax_benefit_system):
    parser = input_variables_extractors.setup(tax_benefit_system)
    get_input_variables_and_parameters = suppress_stdout(parser.get_input_variables_and_parameters)
    variable_names_by_parameter_name = collections.defaultdict(list)
    for column in tax_benefit_system.column_by_name.values():
        _, parameter_names = get_input_variables_and_parameters(column)
        if parameter_names is not None:
            for parameter_name in parameter_names:
                variable_names_by_parameter_name[parameter_name].append(column.name)
    return variable_names_by_parameter_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-p', '--param-translations',
        default = os.path.join(param_dir, 'param-to-parameters.yaml'),
        help = 'path of YAML file containing the association between param elements and OpenFisca parameters')
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    tax_benefit_system = FranceTaxBenefitSystem()
    variable_names_by_parameter_name = get_variable_names_by_parameter_name(tax_benefit_system)
    attributes_by_parameter_name = get_attributes_by_parameter_name(
        args.param_translations,
        tax_benefit_system = tax_benefit_system,
        variable_names_by_parameter_name = variable_names_by_parameter_name,
        )

    for name, attributes in attributes_by_parameter_name.iteritems():
        origin = attributes['origin']
        description = attributes['description']
        print(u'{}: {}'.format(
            name,
            u' ; '.join(filter(None, [
                u'origin: {}'.format(origin),
                u'description: {}'.format(description) if description else None,
                u'old name {}'.format(attributes['original_name']) if attributes['original_name'] else None,
                u'still used by {}'.format(u', '.join(attributes['used_by_variables']))
                if origin == 'openfisca' and attributes['used_by_variables'] else None,
                u'conflicts: {}'.format(u', '.join(attributes['conflicts'])) if attributes['conflicts'] else None,
                ]))
            )).encode('utf-8')


conflicting_parameters_to_ignore = [
    # IPP est plus à jour
    'impot_revenu.charges_deductibles.accueil_personne_agee.plafond',
    'impot_revenu.plafond_qf.celib',
    'impot_revenu.plafond_qf.celib_enf',
    'impot_revenu.plafond_qf.veuf',
    'prestations.prestations_familiales.paje.base.avant_2014.majoration_biact_parent_isoles',
    'prestations.prestations_familiales.paje.base.avant_2014.plafond_ressources_0_enf',
    'impot_revenu.charges_deductibles.pensions_alimentaires.plafond',
    'impot_revenu.plafond_qf.reduc_postplafond',
    'impot_revenu.rpns.micro.imputation_sur_le_revenu_global.plafond_deficits_agricoles',
    'impot_revenu.rvcm.abatmob'
    'prestations.prestations_familiales.ars.plafond_ressources',
    # IPP utilise les paramètres apparaissant dans la législation
    'prestations.prestations_familiales.af.modulation.majoration_plafond_par_enfant_supplementaire',
    'prestations.prestations_familiales.af.modulation.plafond_tranche_1',
    'prestations.prestations_familiales.af.modulation.plafond_tranche_2',
    'impot_revenu.rpns.micro.microfoncier.taux'  # 0.33 vs .33333333
    ]


if __name__ == "__main__":
    sys.exit(main())
