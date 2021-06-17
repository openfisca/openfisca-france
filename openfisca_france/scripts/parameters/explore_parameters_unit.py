
from openfisca_core.parameters import ParameterNode, Scale
from openfisca_france import FranceTaxBenefitSystem


tax_benefit_system = FranceTaxBenefitSystem()
parameters = tax_benefit_system.parameters


def get_parameters_by_unit(parameter, parameters_by_unit = None):
    """
    Build a dictionnary collecting the legislation parameters according to their units
    """
    if parameters_by_unit is None:
        parameters_by_unit = dict(
            scale_none = list(),
            scale_currency = list(),
            none = list(),
            currency = list(),
            rate = list(),
            year = list(),
            )

    for sub_parameter in parameter.children.values():
        if isinstance(sub_parameter, ParameterNode):
            get_parameters_by_unit(sub_parameter, parameters_by_unit)
        else:
            if isinstance(sub_parameter, Scale):
                unit = sub_parameter.metadata.get('unit')
                rate_unit = sub_parameter.metadata.get('rate_unit')
                threshold_unit = sub_parameter.metadata.get('threshold_unit')
                if unit is not None:
                    raise ValueError("Scale {} should not have a unit = {}".format(
                        sub_parameter.name, unit))
                elif (rate_unit is None) and (threshold_unit is None):
                    parameters_by_unit['scale_none'].append(sub_parameter)
                elif threshold_unit == "currency":
                    parameters_by_unit['scale_currency'].append(sub_parameter)
                else:
                    raise ValueError("Scale {} has a stange threshold_unit = {}, rate_unit = {}".format(
                        sub_parameter.name, threshold_unit, rate_unit))

                continue

            unit = sub_parameter.metadata.get('unit')

            if unit is None:
                parameters_by_unit['none'].append(sub_parameter)
            elif unit == "/1":
                parameters_by_unit['rate'].append(sub_parameter)
            elif unit == "currency":
                parameters_by_unit['currency'].append(sub_parameter)
            elif unit == "year":
                parameters_by_unit['year'].append(sub_parameter)
            else:
                raise ValueError("Parameter {} has a stange unit {}".format(
                    sub_parameter.name, unit))

    return parameters_by_unit


if __name__ == '__main__':
    import logging

    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)

    parameters_by_unit = get_parameters_by_unit(parameters)

    logger.info('Distribution of parameters types:')

    for type_, sub_parameters in parameters_by_unit.items():
        logger.info(type_, len(sub_parameters))

    logger.info('\n')
    logger.info('List of parameters with no units')

    for param in parameters_by_unit['none']:
        logger.info(param.name)

    logger.info('\n')
    logger.info('List of scale with currency')

    for param in parameters_by_unit['scale_currency']:
        logger.info(param.name)

    logger.info('\n')
    logger.info('List of scale no unit')

    for param in parameters_by_unit['scale_none']:
        logger.info(param.name)
