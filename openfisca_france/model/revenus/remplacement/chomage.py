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


build_column('chomeur_longue_duree', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                   cerfa_field = {QUIFOY['vous']: u"1AI",
                                  QUIFOY['conj']: u"1BI",
                                  QUIFOY['pac1']: u"1CI",
                                  QUIFOY['pac2']: u"1DI",
                                  QUIFOY['pac3']: u"1EI",
                               }))  # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


build_column('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AP",
                               QUIFOY['conj']: u"1BP",
                               QUIFOY['pac1']: u"1CP",
                               QUIFOY['pac2']: u"1DP",
                               QUIFOY['pac3']: u"1EP",
                               }))  # (f1ap, f1bp, f1cp, f1dp, f1ep)

reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Chômage brut",
    name = 'chobrut',
    )


build_column('indemnites_chomage_partiel', FloatCol(entity = 'ind', label = u"Indemnités de chômage partiel"))
