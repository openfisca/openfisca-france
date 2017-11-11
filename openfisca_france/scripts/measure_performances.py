#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Measure performances of formulas calculations to compare to other OpenFisca implementations."""


import argparse
import logging
import sys
import time

import numpy as np
from openfisca_core import periods, simulations
from openfisca_core.tools import assert_near
from openfisca_france import FranceTaxBenefitSystem


args = None
log = logging.getLogger(__name__)


def add_member(entity, **variables_value_by_name):
    entity.count += 1
    entity.step_size += 1
    member_index = entity.count - 1
    simulation = entity.simulation

    # Add a cell to all arrays of all variables of entity.
    for variable_name, variable_holder in entity.holder_by_name.iteritems():
        column = variable_holder.variable
        if column.definition_period is ETERNITY:
            variable_holder._array = np.hstack((variable_holder._array, [column.default_value]))
        else:
            array_by_period = variable_holder._array_by_period
            if array_by_period is None:
                variable_holder._array_by_period = array_by_period = {}
            for period, array in array_by_period.iteritems():
                array_by_period[period] = np.hstack((array, [column.default_value]))

    # When entity is a person, ensure that the index & role of the person in the other entities are set.
    value_by_name = variables_value_by_name.copy()
    if entity.is_persons_entity:
        for other_entity in simulation.entity_by_key_singular.itervalues():
            if not other_entity.is_persons_entity:
                assert other_entity.count > 0
                value_by_name.setdefault(other_entity.index_for_person_variable_name, other_entity.count - 1)
                role = value_by_name.get(other_entity.role_for_person_variable_name)
                assert role is not None, "Missing role {} in person arguments: {}".format(
                    other_entity.role_for_person_variable_name, value_by_name)
                if role >= other_entity.roles_count:
                    other_entity.roles_count = role + 1

    # Set arguments in variables.
    for variable_name, value in value_by_name.iteritems():
        variable_holder = simulation.get_or_new_holder(variable_name)
        column = variable_holder.variable
        if isinstance(value, dict):
            for period, period_value in value.iteritems():
                array = variable_holder.get_array(period)
                if array is None:
                    array = np.empty(entity.count, dtype = column.dtype)
                    array.fill(column.default_value)
                    variable_holder.put_in_cache(array, period)
                array[member_index] = period_value
        else:
            period = simulation.period
            array = variable_holder.get_array(period)
            if array is None:
                array = np.empty(entity.count, dtype = column.dtype)
                array.fill(column.default_value)
                variable_holder.put_in_cache(array, period)
            array[member_index] = value

    return member_index


def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        # print '%r (%r, %r) %2.9f s' % (method.__name__, args, kw, time.time() - start_time)
        print '{:2.6f} s'.format(time.time() - start_time)
        return result

    return timed


tax_benefit_system = FranceTaxBenefitSystem()


@timeit
def test_irpp(year, irpp, **variables_value_by_name):
    simulation = simulations.Simulation(period = periods.period(year), tax_benefit_system = tax_benefit_system,
        debug = args.verbose)
    famille = simulation.entity_by_key_singular['famille']
    foyer_fiscal = simulation.entity_by_key_singular['foyer_fiscal']
    individu = simulation.entity_by_key_singular['individu']
    menage = simulation.entity_by_key_singular['menage']

    # Dispatch arguments to their respective entities.
    variables_value_by_name_by_entity = {}
    for variable_name, value in variables_value_by_name.iteritems():
        variable_holder = simulation.get_or_new_holder(variable_name)
        entity_variables_value_by_name = variables_value_by_name_by_entity.setdefault(variable_holder.entity, {})
        entity_variables_value_by_name[variable_name] = value

    add_member(famille, **variables_value_by_name_by_entity.get(famille, {}))
    add_member(foyer_fiscal, **variables_value_by_name_by_entity.get(foyer_fiscal, {}))
    add_member(menage, **variables_value_by_name_by_entity.get(menage, {}))
    add_member(individu, quifam = 1, quifoy = 1, quimen = 1, **variables_value_by_name_by_entity.get(individu, {}))
    assert_near(simulation.calculate('irpp'), irpp, absolute_error_margin = 0.51)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    global args
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    print 'salaire_imposable'

    test_irpp(2010, -1181, salaire_imposable =  20000)
    test_irpp(2010, -7934, salaire_imposable =  50000)
    test_irpp(2010, -42338, salaire_imposable =  150000)
    test_irpp(2011, -1181, salaire_imposable =  20000)
    test_irpp(2011, -7934, salaire_imposable =  50000)
    test_irpp(2011, -42338, salaire_imposable =  150000)
    test_irpp(2012, -1181, salaire_imposable =  20000)
    test_irpp(2012, -7934, salaire_imposable =  50000)
    test_irpp(2012, -43222, salaire_imposable =  150000)
    test_irpp(2013, -1170, salaire_imposable =  20000)
    test_irpp(2013, -7889, salaire_imposable =  50000)
    test_irpp(2013, -43076, salaire_imposable =  150000)

    print 'retraite_imposable'

    test_irpp(2010, -1181, retraite_imposable = 20000)
    test_irpp(2010, -8336, retraite_imposable = 50000)
    test_irpp(2010, -46642, retraite_imposable = 150000)
    test_irpp(2011, -1181, retraite_imposable = 20000)
    test_irpp(2011, -8336, retraite_imposable = 50000)
    test_irpp(2011, -46642, retraite_imposable = 150000)
    test_irpp(2012, -1181, retraite_imposable = 20000)
    test_irpp(2012, -8336, retraite_imposable = 50000)
    test_irpp(2012, -46642, retraite_imposable = 150000)
    test_irpp(2013, -1170, retraite_imposable = 20000)
    test_irpp(2013, -8283, retraite_imposable = 50000)
    test_irpp(2013, -46523, retraite_imposable = 150000)

    print 'f2da'

    test_irpp(2010, 0, f2da = 20000)
    test_irpp(2010, 0, f2da = 50000)
    test_irpp(2010, 0, f2da = 150000)
    test_irpp(2011, 0, f2da = 20000)
    test_irpp(2011, 0, f2da = 50000)
    test_irpp(2011, 0, f2da = 150000)
    test_irpp(2012, 0, f2da = 20000)
    test_irpp(2012, 0, f2da = 50000)
    test_irpp(2012, 0, f2da = 150000)
    # test_irpp(2013, 0, f2da = 20000)
    # test_irpp(2013, 0, f2da = 50000)
    # test_irpp(2013, 0, f2da = 150000)

    print 'f2dc'

    test_irpp(2010, 0, f2dc = 20000)
    test_irpp(2010, -2976, f2dc = 50000)
    test_irpp(2010, -22917, f2dc = 150000)
    test_irpp(2011, 0, f2dc = 20000)
    test_irpp(2011, -2976, f2dc = 50000)
    test_irpp(2011, -22917, f2dc = 150000)
    test_irpp(2012, 0, f2dc = 20000)
    test_irpp(2012, -3434, f2dc = 50000)
    test_irpp(2012, -23542, f2dc = 150000)
    # test_irpp(2013, 0, f2dc = 20000)
    # test_irpp(2013, 0, f2dc = 50000)
    # test_irpp(2013, 0, f2dc = 150000)

    print 'f2dh'

    test_irpp(2010, 345, f2dh = 20000)
    test_irpp(2010, 345, f2dh = 50000)
    test_irpp(2010, 345, f2dh = 150000)
    test_irpp(2011, 345, f2dh = 20000)
    test_irpp(2011, 345, f2dh = 50000)
    test_irpp(2011, 345, f2dh = 150000)
    test_irpp(2012, 345, f2dh = 20000)
    test_irpp(2012, 345, f2dh = 50000)
    test_irpp(2012, 345, f2dh = 150000)
    test_irpp(2013, 345, f2dh = 20000)
    test_irpp(2013, 345, f2dh = 50000)
    test_irpp(2013, 345, f2dh = 150000)

    print 'f2tr'

    test_irpp(2010, -1461, f2tr = 20000)
    test_irpp(2010, -9434, f2tr = 50000)
    test_irpp(2010, -48142, f2tr = 150000)
    test_irpp(2011, -1461, f2tr = 20000)
    test_irpp(2011, -9434, f2tr = 50000)
    test_irpp(2011, -48142, f2tr = 150000)
    test_irpp(2012, -1461, f2tr = 20000)
    test_irpp(2012, -9434, f2tr = 50000)
    test_irpp(2012, -48142, f2tr = 150000)
    test_irpp(2013, -1450, f2tr = 20000)
    test_irpp(2013, -9389, f2tr = 50000)
    test_irpp(2013, -48036, f2tr = 150000)

    print 'f2ts'

    test_irpp(2010, -1461, f2ts = 20000)
    test_irpp(2010, -9434, f2ts = 50000)
    test_irpp(2010, -48142, f2ts = 150000)
    test_irpp(2011, -1461, f2ts = 20000)
    test_irpp(2011, -9434, f2ts = 50000)
    test_irpp(2011, -48142, f2ts = 150000)
    test_irpp(2012, -1461, f2ts = 20000)
    test_irpp(2012, -9434, f2ts = 50000)
    test_irpp(2012, -48142, f2ts = 150000)
    test_irpp(2013, -1450, f2ts = 20000)
    test_irpp(2013, -9389, f2ts = 50000)
    test_irpp(2013, -48036, f2ts = 150000)

    print 'f3vg'

    test_irpp(2010, -3600, f3vg = 20000)
    test_irpp(2010, -9000, f3vg = 50000)
    test_irpp(2010, -27000, f3vg = 150000)
    test_irpp(2011, -3800, f3vg = 20000)
    test_irpp(2011, -9500, f3vg = 50000)
    test_irpp(2011, -28500, f3vg = 150000)
    test_irpp(2012, -4800, f3vg = 20000)
    test_irpp(2012, -12000, f3vg = 50000)
    test_irpp(2012, -36000, f3vg = 150000)
    test_irpp(2013, -1450, f3vg = 20000)
    test_irpp(2013, -9389, f3vg = 50000)
    test_irpp(2013, -48036, f3vg = 150000)

    print 'f3vz'

    # test_irpp(2010, 0, f3vz = 20000)
    # test_irpp(2010, 0, f3vz = 50000)
    # test_irpp(2010, 0, f3vz = 150000)
    test_irpp(2011, 0, f3vz = 20000)
    test_irpp(2011, 0, f3vz = 50000)
    test_irpp(2011, 0, f3vz = 150000)
    test_irpp(2012, 0, f3vz = 20000)
    test_irpp(2012, 0, f3vz = 50000)
    test_irpp(2012, 0, f3vz = 150000)
    test_irpp(2013, 0, f3vz = 20000)
    test_irpp(2013, 0, f3vz = 50000)
    test_irpp(2013, 0, f3vz = 150000)

    print 'f4ba'

    test_irpp(2010, -1461, f4ba = 20000)
    test_irpp(2010, -9434, f4ba = 50000)
    test_irpp(2010, -48142, f4ba = 150000)
    test_irpp(2011, -1461, f4ba = 20000)
    test_irpp(2011, -9434, f4ba = 50000)
    test_irpp(2011, -48142, f4ba = 150000)
    test_irpp(2012, -1461, f4ba = 20000)
    test_irpp(2012, -9434, f4ba = 50000)
    test_irpp(2012, -48142, f4ba = 150000)
    test_irpp(2013, -1450, f4ba = 20000)
    test_irpp(2013, -9389, f4ba = 50000)
    test_irpp(2013, -48036, f4ba = 150000)


if __name__ == "__main__":
    sys.exit(main())
