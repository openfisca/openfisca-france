# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np

from .. import init_country


TaxBenefitSystem = init_country()
tax_benefit_system = TaxBenefitSystem()


def assert_near(value, target_value, error_margin = 1):
    if isinstance(value, (list, tuple)):
        value = np.array(value)
    if isinstance(target_value, (list, tuple)):
        target_value = np.array(target_value)
    if isinstance(value, np.ndarray):
        assert (target_value - error_margin < value).all() and (value < target_value + error_margin).all(), \
            '{} differs from {} with a margin {} > {}'.format(value, target_value, abs(value - target_value),
                error_margin)
    else:
        assert target_value - error_margin < value < target_value + error_margin, \
            '{} differs from {} with a margin {} > {}'.format(value, target_value, abs(value - target_value),
                error_margin)
