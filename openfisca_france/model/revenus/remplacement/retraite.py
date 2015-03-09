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


from ...base import *  # noqa analysis:ignore


build_column('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AS",
                               QUIFOY['conj']: u"1BS",
                               QUIFOY['pac1']: u"1CS",
                               QUIFOY['pac2']: u"1DS",
                               QUIFOY['pac3']: u"1ES",
                               }))  # (f1as, f1bs, f1cs, f1ds, f1es)

reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Retraite brute",
    name = 'rstbrut',
    )

# L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
build_column('aer', IntCol(label = u"Allocation équivalent retraite (AER)"))

build_column('retraite_combattant', FloatCol(entity = 'ind', label = u"Retraite du combattant"))
