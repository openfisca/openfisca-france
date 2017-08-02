# -*- coding: utf-8 -*-

import datetime
import json

from openfisca_core import legislations

from openfisca_france import FranceTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = FranceTaxBenefitSystem()


def test_legislation_xml_file():
    legislation = tax_benefit_system.get_legislation()
    assert legislation is not None
    for year in range(2006, datetime.date.today().year + 1):
        legislation_at_instant = tax_benefit_system.get_legislation_at_instant(year)
        assert legislation_at_instant is not None
