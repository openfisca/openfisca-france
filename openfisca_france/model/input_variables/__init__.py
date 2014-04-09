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


from . import (base,
               section_1_traitements_salaires_ppe_pensions_rentes,
               section_2_revenus_valeurs_capitaux_mobiliers,
               section_3_plus_values,
               section_4_revenus_fonciers,
               section_5_revenus_professions_non_salaries,
               section_6_charges_deductibles,
               section_7_reductions_et_credits_d_impots,
               section_8_divers,
               isf,
               survey_variables)

column_by_name = base.column_by_name.copy()

for col_by_name in [
    section_1_traitements_salaires_ppe_pensions_rentes.column_by_name,
    section_2_revenus_valeurs_capitaux_mobiliers.column_by_name,
    section_3_plus_values.column_by_name,
    section_4_revenus_fonciers.column_by_name,
    section_5_revenus_professions_non_salaries.column_by_name,
    section_6_charges_deductibles.column_by_name,
    section_7_reductions_et_credits_d_impots.column_by_name,
    section_8_divers.column_by_name,
    isf.column_by_name,
    survey_variables.column_by_name,
    ]:

    column_by_name.update(col_by_name)
