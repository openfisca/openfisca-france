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


from openfisca_core import columns
import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def check_input_column_consumers(column):
    if column.name not in (
            'idfam',
            'idfoy',
            'idmen',
            'noi',
            'prenom',
            'quifam',
            'quifoy',
            'quimen',
            ):
        assert column.consumers, u'Input column {} has no consumer'.format(column.name).encode('utf-8')


def test():
    for column in tax_benefit_system.column_by_name.itervalues():
        if column.formula_constructor is None:
            yield check_input_column_consumers, column


if __name__ == '__main__':
    test()
