from copy import deepcopy

from openfisca_core.tools import assert_near

from openfisca_france.model.base import *  # noqa analysis:ignore
from test_entities import TEST_CASE, tax_benefit_system

class salaire_famille(Variable):
    column = FloatCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        salaire_holder = simulation.compute('salaire', period = period)
        return self.sum_by_entity(salaire_holder)

class salaire_enfants(Variable):
    column = FloatCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        salaire_holder = simulation.compute('salaire', period = period)
        return self.sum_by_entity(salaire_holder, roles = ENFS)

class salaire_enf1(Variable):
    column = FloatCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        salaire_holder = simulation.compute('salaire', period = period)
        salaire = self.split_by_roles(salaire_holder)
        assert_near(salaire[CHEF], [1000, 3000])
        return salaire[ENFS[0]]

class salaire_conj(Variable):
    column = FloatCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        salaire_holder = simulation.compute('salaire', period = period)
        salaire = self.filter_role(salaire_holder, role = CONJ)
        return salaire

class af_chef(Variable):
    column = FloatCol
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        af_holder = simulation.compute('af', period = period)
        return self.cast_from_entity_to_roles(af_holder, roles = [CHEF])

class af_tous(Variable):
    column = FloatCol
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(self, simulation, period):
        af_holder = simulation.compute('af', period = period)
        return self.cast_from_entity_to_roles(af_holder)

class has_enfant_autonome(Variable):
    column = BoolCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(self, simulation, period):
        salaire = simulation.calculate('salaire', period = period)
        condition = salaire > 450
        return self.any_by_roles(condition, roles = ENFS, entity = Famille)


tax_benefit_system.add_variables(salaire_famille, salaire_enfants, salaire_enf1, salaire_conj, af_chef, af_tous, has_enfant_autonome)

TEST_CASE_1 = deepcopy(TEST_CASE)
TEST_CASE_1['individus'][0]['salaire'] = 1000
TEST_CASE_1['individus'][1]['salaire'] = 1500
TEST_CASE_1['individus'][2]['salaire'] = 400
TEST_CASE_1['individus'][4]['salaire'] = 3000
TEST_CASE_1['individus'][5]['salaire'] = 500
TEST_CASE_1['familles'][0]['af'] = 2000
TEST_CASE_1['familles'][1]['af'] = 1200

reference_period = "2013-01"


def new_simulation(test_case):
    return tax_benefit_system.new_scenario().init_from_test_case(
        period = reference_period,
        test_case = TEST_CASE_1
    ).new_simulation()


def test_sum_by_entity():
    simulation = new_simulation(TEST_CASE_1)
    salaire_famille = simulation.calculate('salaire_famille', period = reference_period)
    assert_near(salaire_famille, [2900, 3500])
    salaire_enfants = simulation.calculate('salaire_enfants', period = reference_period)
    assert_near(salaire_enfants, [400, 500])

def test_split_by_roles():
    simulation = new_simulation(TEST_CASE_1)
    salaire_enf1 = simulation.calculate('salaire_enf1', period = reference_period)
    assert_near(salaire_enf1, [400, 500])

def test_filter_role():
    simulation = new_simulation(TEST_CASE_1)
    salaire_enf1 = simulation.calculate('salaire_conj', period = reference_period)
    assert_near(salaire_enf1, [1500, 0])

def test_filter_role():
    simulation = new_simulation(TEST_CASE_1)
    salaire_enf1 = simulation.calculate('salaire_conj', period = reference_period)
    assert_near(salaire_enf1, [1500, 0])

def test_cast_from_entity_to_roles():
    simulation = new_simulation(TEST_CASE_1)
    af_chef = simulation.calculate('af_chef', period = reference_period)
    af_tous = simulation.calculate('af_tous', period = reference_period)
    assert_near(af_chef, [2000, 0, 0, 0, 1200, 0])
    assert_near(af_tous, [2000, 2000, 2000, 2000, 1200, 1200])

def test_any_by_roles():
    simulation = new_simulation(TEST_CASE_1)
    has_enfant_autonome = simulation.calculate('has_enfant_autonome', period = reference_period)
    assert_near(has_enfant_autonome, [False, True])

