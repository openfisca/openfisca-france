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


from numpy import zeros

from ....base import CAT


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
    for type_sal_name, type_sal_index in CAT:
        if type_sal_name not in bareme_by_type_sal_name:  # to deal with public_titulaire_militaire
            continue
        bareme = bareme_by_type_sal_name[type_sal_name].get(bareme_name)  # TODO; should have better warnings
        if bareme is not None:
            cotisation += bareme.calc(
                base * (type_sal == type_sal_index),
                factor = plafond_securite_sociale,
                round_base_decimals = round_base_decimals,
                )
    return - cotisation


def apply_bareme(simulation, period, cotisation_type = None, bareme_name = None, variable_name = None):
    # period = period.start.offset('first-of', 'month').period('month')
    cotisation_mode_recouvrement = simulation.calculate('cotisation_sociale_mode_recouvrement', period)
    cotisation = (
        # en fin d'année
        cotisation_mode_recouvrement == 1) * (
            compute_cotisation_annuelle(
                simulation,
                period,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                )
            ) + (
        # anticipé
        cotisation_mode_recouvrement == 0) * (
            compute_cotisation_anticipee(
                simulation,
                period,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                variable_name = variable_name,
                )
            )
    return cotisation


def compute_cotisation(simulation, period, cotisation_type = None, bareme_name = None):

    assert cotisation_type is not None
    law = simulation.legislation_at(period.start)
    if cotisation_type == "employeur":
        bareme_by_type_sal_name = law.cotsoc.cotisations_employeur
    elif cotisation_type == "salarie":
        bareme_by_type_sal_name = law.cotsoc.cotisations_salarie
    assert bareme_name is not None

    assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
    plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)
    type_sal = simulation.calculate('type_sal', period)

    cotisation = apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name = bareme_by_type_sal_name,
        bareme_name = bareme_name,
        base = assiette_cotisations_sociales,
        plafond_securite_sociale = plafond_securite_sociale,
        type_sal = type_sal,
        )
    return cotisation


def compute_cotisation_annuelle(simulation, period, cotisation_type = None, bareme_name = None):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_cotisation(
            simulation,
            period.start.offset('first-of', 'year').period('year'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )


def compute_cotisation_anticipee(simulation, period, cotisation_type = None, bareme_name = None, variable_name = None):
    if period.start.month < 12:
        return compute_cotisation(
            simulation,
            period.start.offset('first-of', 'month').period('month'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )
    if period.start.month == 12:
        assert variable_name is not None
        cumul = simulation.calculate_add(variable_name, period.start.offset('first-of', 'month').offset(
            -11, 'month').period('month', 11))

        return compute_cotisation(
            simulation,
            period.start.offset('first-of', 'year').period('year'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            ) - cumul
