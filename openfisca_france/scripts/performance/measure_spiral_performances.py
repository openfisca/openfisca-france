#! /usr/bin/env python
import time
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.situation_examples import couple

tax_benefit_system = FranceTaxBenefitSystem()

NB_RUN = 10

situation = {
    'individus': {
        'demandeur': {
            'salaire_imposable': {
                '2017-12': 62191,
                '2018-01': 62191,
                '2018-02': 62191,
                '2018-03': 62191,
                '2018-04': 62191,
                '2018-05': 62191,
                '2018-06': 62191,
                '2018-07': 62191,
                '2018-08': 62191,
                '2018-09': 62191,
                '2018-10': 62191,
                '2018-11': 62191,
                '2018-12': 62191,
                '2016-01': 62191,
                '2016-02': 62191,
                '2016-03': 62191,
                '2016-04': 62191,
                '2016-05': 62191,
                '2016-06': 62191,
                '2016-07': 62191,
                '2016-08': 62191,
                '2016-09': 62191,
                '2016-10': 62191,
                '2016-11': 62191,
                '2016-12': 62191
                }
            }
        },
    'familles': {
        '_': {
            'parents': [
                'demandeur'
                ]
            }
        },
    'foyers_fiscaux': {
        '_': {
            'declarants': [
                'demandeur'
                ],
            'personnes_a_charge': []
            }
        },
    'menages': {
        '_': {
            'personne_de_reference': [
                'demandeur'
                ]
            }
        }
    }


def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        delta = time.time() - start_time
        return result, delta

    return timed


def test_revenu_disponible():
    def new_simulation():
        return SimulationBuilder().build_from_dict(tax_benefit_system, couple)

    simulations = [new_simulation() for i in range(NB_RUN)]

    @timeit
    def run_test():
        for simulation in simulations:
            simulation.calculate('revenu_disponible', 2018)

    result, delta = run_test()
    print('{:2.6f} s'.format(delta / NB_RUN))  # noqa T201


def test_spiral():
    def new_simulation():
        return SimulationBuilder().build_from_dict(tax_benefit_system, situation)

    simulations = [new_simulation() for i in range(NB_RUN)]

    @timeit
    def run_test():
        for simulation in simulations:
            simulation.calculate('ass', '2018-12')
            simulation.calculate('logement_social_eligible', '2018-12')

    result, delta = run_test()
    print('{:2.6f} s'.format(delta / NB_RUN))  # noqa T201


print('Premier test revenu disponible')  # noqa T201
test_revenu_disponible()
print('Second test revenu disponible')  # noqa T201
test_revenu_disponible()
print('3e test revenu disponible')  # noqa T201
test_revenu_disponible()

print('Premier test ciblé spirale')  # noqa T201
test_spiral()
print('Second test ciblé spirale')  # noqa T201
test_spiral()
print('3e test ciblé spirale')  # noqa T201
test_spiral()
