# -*- coding: utf-8 -*-

import datetime

from nose.tools import assert_less
from numpy.testing import assert_array_almost_equal

from openfisca_core import periods
from openfisca_france.tests import base


def test_what_if_applied_now():
    year = 2014
    max_sal = 18000
    count = 2
    people = 1
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                max = max_sal,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 1

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf')
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf')
    #    assert_less(max(abs([0, 918] - ir_plaf_qf)), error_margin)
    #    assert_less(max(abs([0, 911.4] - reform_ir_plaf_qf)), error_margin)
    #    assert_less(max(abs([0, -869] - impo)), error_margin)
    #    assert_less(max(abs([0, -911.4 + (1135 - 911.4)] - reform_impo)), error_margin)




def test_reform_vs_counterfactual():
    year = 2015
    max_sal = 18000
    count = 2
    people = 1
    reform = base.get_cached_reform(
        reform_key = 'plf2016_counterfactual',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                max = max_sal,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 1

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf')
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf')
    
    #    assert_less(max(abs([0, 918] - ir_plaf_qf)), error_margin)
    #    assert_less(max(abs([0, 911.4] - reform_ir_plaf_qf)), error_margin)
    #    assert_less(max(abs([0, -869] - impo)), error_margin)
    #    assert_less(max(abs([0, -911.4 + (1135 - 911.4)] - reform_impo)), error_margin)


def test_dossier_de_presse_1(): #WIP
#Célibataire sans enfants1 part : revenu mensuel net = 1593 IR2015 = 1138 IR2016 = 828
    year = 2015
    people = 1
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1),
                       salaire_imposable = 1593*12), #TODO : Comment inputer du revenu mensuel net ?
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 1

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf')
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf')
    print impo #968
    print reform_impo #1051
    #assert abs(impo-1138) < 1
    #assert abs(reform_impo-828) < 1

def test_dossier_de_presse_2(): #WIP
#Couple, sans enfants, retraités 2 parts : revenu mensuel net : 2960 IR2015 = 1911 #IR2016 = 1428
    year = 2015
    people = 2
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1),
                       rst = 2960*12),     #TODO : rst et imposable pas net, voir pour la csg ?
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 1

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf')
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf')
    print impo
    #assert abs(impo-1911) < 1
    #assert abs(reform_impo-1428) < 1

def test_dossier_de_presse_3(): #WIP
#Couple, deux enfants, salariés 3 parts : Rev mensuel net : 3800 IR 2015 : 1879 IR 2016 : 1372
    year = 2015
    people = 4
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1),
                       salaire_imposable = 3800 * 12), #TODO : Comment inputer du revenu mensuel net ?
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 1

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf')
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf')
    print impo
    #assert abs(impo-1879) < error_margin
    #assert abs(reform_impo-1372) < error_margin





if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    # test_what_if_applied_now()
    #test_reform_vs_counterfactual()
    test_dossier_de_presse_1()
    test_dossier_de_presse_2()
    test_dossier_de_presse_3()