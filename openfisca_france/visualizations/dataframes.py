# -*- coding: utf-8 -*-


import pandas

from openfisca_core import decompositions

from . import OutNode


def from_decomposition_json(simulation, decomposition_json = None, reference_simulation = None,
        remove_null = False, label = True, name = False):
    assert label or name, "At least label or name should be True"
    if decomposition_json is None:
        decomposition_json = decompositions.get_decomposition_json(simulation.tax_benefit_system)
    data = OutNode.init_from_decomposition_json(simulation, decomposition_json)

    index = [row.desc for row in data if row.desc not in ('root')]
    data_frame = None
    for row in data:
        if row.desc not in ('root'):
            if data_frame is None:
                value_columns = ['value_' + str(i) for i in range(len(row.vals))] if len(row.vals) > 1 else ['value']
                data_frame = pandas.DataFrame(index = index, columns = ['name'] + value_columns)

            data_frame['name'][row.desc] = row.code
            data_frame.loc[row.desc, value_columns] = row.vals

    data_frame.index.name = "label"
    if remove_null:
        variables_to_remove = []
        for variable in data_frame.index:
            if (data_frame.loc[variable, value_columns] == 0).all():
                variables_to_remove.append(variable)
        data_frame.drop(variables_to_remove, inplace = True)

    data_frame.reset_index(inplace = True)

    return data_frame
