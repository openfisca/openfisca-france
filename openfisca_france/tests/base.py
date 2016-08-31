# -*- coding: utf-8 -*-

from openfisca_core.tools import assert_near

from openfisca_france import FranceTaxBenefitSystem, Simulation


__all__ = [
    'assert_near',
    'tax_benefit_system',
    ]

tax_benefit_system = FranceTaxBenefitSystem()
