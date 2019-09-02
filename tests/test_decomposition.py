import datetime
import logging
import os
import numpy as np
import yaml


from openfisca_france import CountryTaxBenefitSystem as FranceTaxBenefitSystem
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR
from openfisca_france.scenarios import init_single_entity


log = logging.getLogger(__name__)

ABSOLUTE_ERROR = 1e-4

def visit(node, decomposition_simulation, simulation, period):
    variable_name = node["variable_name"]
    children = node.get("children")

    def compare():
        if variable_name in simulation.tax_benefit_system.variables:
            decomposition_result = decomposition_simulation.calculate_add(variable_name, period = period)
            result = simulation.calculate_add(variable_name, period = period)
            assert (np.abs(decomposition_result - result) < ABSOLUTE_ERROR).all(), "{}: decomposition = {} != {} = original".format(
                    variable_name,
                    decomposition_result,
                    result,
                    )
            log.debug("{} : ok".format(variable_name))

        else:
            log.info("Variable {} is not available in original tax-benefit system".format(variable_name))

    if children:
        for child_node in children:
            visit(child_node, decomposition_simulation, simulation, period)
        compare()
    else:
        compare()
        return


def test_revenu_disponible_decomposition():
    # Just ensure that disposable_income can be calculated with and without decomposition.
    # Without decomposition

    tax_benefit_system = FranceTaxBenefitSystem()
    # With decomposition
    decomposition_path = os.path.join(COUNTRY_DIR, 'model', 'decomposition.yaml')
    with open(decomposition_path, 'r') as yaml_file:
        decomposition_tree = yaml.load(yaml_file, Loader = yaml.SafeLoader)

    decomposition_tax_benefit_system = FranceTaxBenefitSystem()
    decomposition_tax_benefit_system.add_variables_from_decomposition_tree(decomposition_tree, update = True)

    year = 2018
    scenario_arguments = dict(
        period = year,
        parent1 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            effectif_entreprise = 25,
            categorie_salarie = "prive_non_cadre",
            ),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        menage = dict(
            zone_apl = "zone_1",
            ),
        )

    for tbs in [tax_benefit_system, decomposition_tax_benefit_system]:
        scenario = tbs.new_scenario()
        init_single_entity(scenario, **scenario_arguments)
        period = scenario_arguments['period']
        if tbs == decomposition_tax_benefit_system:
            decomposition_simulation = scenario.new_simulation(debug = False)
        else:
            simulation = scenario.new_simulation(debug = False)

    visit(decomposition_tree, decomposition_simulation, simulation, period)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)

    test_revenu_disponible_decomposition()
