#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Functions used to build the tests  """

from openfisca_core import conv
from openfisca_france.scripts.calculateur_impots import base

# TODO: peut-être mutualiser les deux fonctions


def input_scenario_to_json(value, state = None):
    """
    Function that reformat and check the JSON file containing a scenario
    """
    return conv.pipe(
        conv.make_input_to_json(),
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                scenario = conv.pipe(
                    conv.test_isinstance(dict),
                    base.tax_benefit_system.Scenario.make_json_to_instance(
                        tax_benefit_system = base.tax_benefit_system),
                    conv.not_none,
                    ),
                ),
            ),
        )(value, state = state or conv.default_state)


def input_to_json_data(value, state = None):
    """
    Function that reformat and check the JSON file containing the input of a test (scenario + official results associated)
    """
    return conv.pipe(
        conv.make_input_to_json(),
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                resultat_officiel = conv.pipe(
                    conv.test_isinstance(dict),
                    conv.uniform_mapping(
                        conv.pipe(
                            conv.test_isinstance(basestring),
                            conv.not_none,
                            ),
                        conv.pipe(
                            conv.test_isinstance(dict),
                            conv.struct(
                                dict(
                                    code = conv.pipe(
                                        conv.test_isinstance(basestring),
                                        conv.not_none,
                                        ),
                                    name = conv.pipe(
                                        conv.test_isinstance(basestring),
                                        conv.not_none,
                                        ),
                                    value = conv.pipe(
                                        conv.test_isinstance(float),
                                        conv.not_none,
                                        ),
                                    openfisca_name = conv.pipe(
                                        conv.test_isinstance(basestring),
                                        ),
                                    ),
                                ),
                            conv.not_none,
                            ),
                        ),
                    conv.not_none,
                    ),
                scenario = conv.pipe(
                    conv.test_isinstance(dict),
                    # conv.struct(
                    #     dict(
                    #         test_case = conv.pipe(
                    #             conv.test_isinstance(dict),
                    #             # For each entity convert its members from a dict to a list.
                    #             conv.uniform_mapping(
                    #                 conv.noop,
                    #                 conv.pipe(
                    #                     conv.test_isinstance(dict),
                    #                     conv.function(transform_entity_member_by_id_to_members),
                    #                     ),
                    #                 ),
                    #             ),
                    #         ),
                    #     default = conv.noop,
                    #     ),
                    base.tax_benefit_system.Scenario.make_json_to_instance(
                        tax_benefit_system = base.tax_benefit_system),
                    conv.not_none,
                    ),
                ),
            ),
        )(value, state = state or conv.default_state)


def transform_entity_member_by_id_to_members(member_by_id):
    members = []
    for id, member in member_by_id.iteritems():
        assert 'id' not in member or member['id'] == id
        member['id'] = id
        members.append(member)
    return members