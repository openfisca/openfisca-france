import os
import yaml
from yaml import SafeLoader


from openfisca_france import CountryTaxBenefitSystem as FranceTaxBenefitSystem
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR


def test_revenu_disponible_decomposition():
    # Just ensure that disposable_income can be calculated with and without decomposition.
    # Without decomposition
    tax_benefit_system = FranceTaxBenefitSystem()

    # With decomposition
    decomposition_path = os.path.join(COUNTRY_DIR, 'model', 'decomposition.yaml')
    with open(decomposition_path, 'r') as yaml_file:
        decomposition_tree = yaml.load(yaml_file, Loader = SafeLoader)

    decomposition_tax_benefit_system = FranceTaxBenefitSystem()
    decomposition_tax_benefit_system.add_variables_from_decomposition_tree(decomposition_tree, update = True)

    scenarios_arguments = [
        dict(
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
        for year  in [2018] # in range(2006, 2020)
        ]

@pytest.mark.parametrize("scenario_arguments", scenarios_arguments)
def test_basics(scenario_arguments):
    scenario = tax_benefit_system.new_scenario()
    init_single_entity(scenario, **scenario_arguments)
    simulation = scenario.new_simulation(debug = False)
    period = scenario_arguments['period']
    assert simulation.calculate('revenu_disponible', period = period) is not None, "Can't compute revenu_disponible on period {}".format(period)
    assert simulation.calculate_add('salaire_super_brut', period = period) is not None, \
        "Can't compute salaire_super_brut on period {}".format(period)


    simulation











