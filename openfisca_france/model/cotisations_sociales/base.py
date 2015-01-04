# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


from numpy import zeros

from ..base import CAT


def apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name = None,
        bareme_name = None,
        type_sal = None,
        base = None,
        plafond_securite_sociale = None,
        round_base_decimals = 2,
        ):
    assert bareme_by_type_sal_name is not None
    assert bareme_name is not None
    assert base is not None
    assert plafond_securite_sociale is not None
    assert type_sal is not None
    cotisation = zeros(len(base))
    for type_sal_enum in CAT:
        if type_sal_enum[0] not in bareme_by_type_sal_name:  # to deal with public_titulaire_militaire
            continue
        bareme = bareme_by_type_sal_name[type_sal_enum[0]].get(bareme_name)  # TODO; should have better warnings
        if bareme:
            cotisation += bareme.calc(
                base * (type_sal == type_sal_enum[1]),
                factor = plafond_securite_sociale,
                round_base_decimals = round_base_decimals,
                )
    return - cotisation
