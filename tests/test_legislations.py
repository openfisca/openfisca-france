# -*- coding: utf-8 -*-

import datetime
import json

from openfisca_core import legislations, legislationsxml

from openfisca_france import FranceTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = FranceTaxBenefitSystem()


def check_legislation_xml_file(year):
    compact_legislation = tax_benefit_system.get_legislation(year)

    assert compact_legislation is not None


def test_legislation_xml_file():
    for year in range(2006, datetime.date.today().year + 1):
        yield check_legislation_xml_file, year
