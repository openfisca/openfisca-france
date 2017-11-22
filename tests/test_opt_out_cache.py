import openfisca_france
import datetime

tbs = openfisca_france.FranceTaxBenefitSystem()

reference_period = "2016-01"

scenario = tbs.new_scenario().init_from_attributes(
    period = reference_period,
    input_variables = {
        'date_naissance': datetime.date(1980, 1, 1),
        'loyer': 500,
        'statut_occupation_logement': 3,
        },
    )


def test_variable_in_blacklist():
    simulation = scenario.new_simulation(opt_out_cache = True)
    simulation.calculate('aide_logement_montant_brut', period = reference_period)
    assert(simulation.get_or_new_holder('aide_logement_R0')._array_by_period is None)


def test_variable_not_in_blacklist():
    simulation = scenario.new_simulation(opt_out_cache = True)
    simulation.calculate('aide_logement_montant_brut', period = reference_period)
    assert(simulation.get_or_new_holder('aide_logement_montant_brut')._array_by_period is not None)
