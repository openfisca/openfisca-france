# -*- coding: utf-8 -*-


from openfisca_core.parameters import ParameterNode, Scale
from openfisca_france import FranceTaxBenefitSystem


tax_benefit_system = FranceTaxBenefitSystem()
parameters = tax_benefit_system.parameters


def get_parameters_by_unit(parameter, parameters_by_unit = None):
    """
    Build a dictionnary collectiing the legislation parameters according to their units
    """
    if parameters_by_unit is None:
        parameters_by_unit = dict(
            scale = list(),
            none = list(),
            currency = list(),
            rate = list(),
            year = list(),
            )
    for name, sub_parameter in parameter.children.items():
        if isinstance(sub_parameter, ParameterNode):
            get_parameters_by_unit(sub_parameter, parameters_by_unit)
        else:
            if isinstance(sub_parameter, Scale):
                parameters_by_unit['scale'].append(sub_parameter)
            elif 'unit' not in sub_parameter.metadata:
                parameters_by_unit['none'].append(sub_parameter)
            elif sub_parameter.metadata['unit'] == "/1":
                parameters_by_unit['rate'].append(sub_parameter)
            elif sub_parameter.metadata['unit'] == "currency":
                parameters_by_unit['currency'].append(sub_parameter)
            elif sub_parameter.metadata['unit'] == "year":
                parameters_by_unit['year'].append(sub_parameter)
            else:
                raise ValueError("Parameter {} has a stange unit {}".format(
                    sub_parameter.name, sub_parameter.unit))

    return parameters_by_unit


if __name__ == '__main__':
    parameters_by_unit = get_parameters_by_unit(parameters)
    print('Distribution of parameters types:')
    for type_, sub_parameters in parameters_by_unit.items():
        print(type_, len(parameters_by_unit[type_]))

    print('\n')
    print('List of parameters with no units')

    for param in parameters_by_unit['none']:
        print(param.name)
