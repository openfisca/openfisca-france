# -*- coding: utf-8 -*-

import datetime

from .cache import tax_benefit_system


def test_parameters():
    parameters = tax_benefit_system.parameters
    assert parameters is not None
    for year in range(2006, datetime.date.today().year + 1):
        parameters_at_instant = tax_benefit_system.get_parameters_at_instant(year)
        assert parameters_at_instant is not None
