import pytest

from .cache import tax_benefit_system


@pytest.mark.parametrize('name, unit', [
    ('nb_pac', 'people'),
    ('nbptr', 'part_quotient_familial'),
    ('abattement_pensions_retraites', 'currency'),
    ])
def test_ir_variable_units(name, unit):
    assert tax_benefit_system.get_variable(name).unit == unit
