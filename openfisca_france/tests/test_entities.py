from copy import deepcopy

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.variables import Variable
from openfisca_core.columns import FloatCol, IntCol, BoolCol
from openfisca_core.tools import assert_near

from openfisca_france.scenarios import Scenario
from openfisca_france.entities import entities, Individus, Familles, FoyersFiscaux, Menages
from openfisca_france.model.base import *  # noqa analysis:ignore


class af(Variable):
    column = FloatCol
    entity_class = Familles

class salaire(Variable):
    column = FloatCol
    entity_class = Individus

class age(Variable):
    column = IntCol
    entity_class = Individus

class autonomie_financiere(Variable):
    column = BoolCol
    entity_class = Individus

# This tests are more about core than france, but we need france entities to run some of them.
# We use a dummy TBS to run the tests faster
class DummyTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        self.Scenario = Scenario
        self.add_variables(af, salaire, age, autonomie_financiere)

tax_benefit_system = DummyTaxBenefitSystem()

TEST_CASE = {
    'individus': [{'id': 'ind0'}, {'id': 'ind1'}, {'id': 'ind2'}, {'id': 'ind3'},{'id': 'ind4'}, {'id': 'ind5'}],
    'familles': [
        {'enfants': ['ind2', 'ind3'], 'parents': ['ind0', 'ind1']},
        {'enfants': ['ind5'], 'parents': ['ind4']}
        ],
    'foyers_fiscaux': [
        {'declarants': ['ind0', 'ind1'], 'personnes_a_charge': ['ind2', 'ind3']},
        {'personnes_a_charge': ['ind5'], 'declarants': ['ind4']}
        ],
    'menages': [
        {'conjoint': 'ind1', 'enfants': ['ind2', 'ind3'], 'personne_de_reference': 'ind0'},
        {'conjoint': None, 'enfants': ['ind5'], 'personne_de_reference': 'ind4'},
        ],
    }

TEST_CASE_AGES = deepcopy(TEST_CASE)
AGES = [40, 37, 7, 9, 54, 20]
for (individu, age) in zip(TEST_CASE_AGES['individus'], AGES):
        individu['age'] = age

def new_simulation(test_case):
    return tax_benefit_system.new_scenario().init_from_test_case(
        period = 2013,
        test_case = test_case
    ).new_simulation()


def test_transpose():
    test_case = deepcopy(TEST_CASE)
    test_case['familles'][0]['af'] = 20000
    test_case['familles'][1]['af'] = 10000
    test_case['foyers_fiscaux'] = [
        TEST_CASE['foyers_fiscaux'][0],
        {'declarants': ['ind4']},
        {'declarants': ['ind5']}
        ]

    simulation = new_simulation(test_case)
    foyer_fiscal = simulation.foyer_fiscal

    af = foyer_fiscal.members.famille('af')
    af_foyer_fiscal = foyer_fiscal.transpose(af, origin_entity = Menages)

    assert_near(af_foyer_fiscal, [20000, 10000, 0])


def test_value_from_person():
    test_case = deepcopy(TEST_CASE_AGES)
    simulation = new_simulation(test_case)

    foyer_fiscal = simulation.foyer_fiscal
    age = foyer_fiscal.members('age')

    age_conjoint = foyer_fiscal.value_from_person(age, role = CONJOINT, default = -1)

    assert_near(age_conjoint, [37, -1])
