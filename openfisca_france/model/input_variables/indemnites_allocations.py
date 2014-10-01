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

import collections
from datetime import date
from functools import partial


from openfisca_core.columns import BoolCol, DateCol, EnumCol, IntCol, FloatCol, StrCol, build_column_couple
from openfisca_core.enumerations import Enum

from ..base import build_column_couple, column_by_name

column_by_name.update(collections.OrderedDict((

    build_column_couple('indemnites_journalieres_maternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de maternité")),
    build_column_couple('indemnites_journalieres_paternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de paternité")),
    build_column_couple('indemnites_journalieres_adoption', FloatCol(entity = 'ind', label = u"Indemnités journalières d'adoption")),
    build_column_couple('indemnites_journalieres_maladie', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie")),
    build_column_couple('indemnites_journalieres_accident_travail', FloatCol(entity = 'ind', label = u"Indemnités journalières d'accident du travail")),
    build_column_couple('indemnites_journalieres_maladie_professionnelle', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie professionnelle")),

    build_column_couple('indemnites_chomage_partiel', FloatCol(entity = 'ind', label = u"Indemnités de chômage partiel")),

    build_column_couple('allocation_aide_retour_emploi', FloatCol(entity = 'ind', label = u"Allocation d'aide au retour à l'emploi")),
    build_column_couple('allocation_securisation_professionnelle', FloatCol(entity = 'ind', label = u"Allocation de sécurisation professionnelle")),
    build_column_couple('prime_forfaitaire_mensuelle_reprise_activite', FloatCol(entity = 'ind', label = u"Prime forfaitaire mensuelle pour la reprise d'activité")),

    build_column_couple('indemnites_volontariat', FloatCol(entity = 'ind', label = u"Indemnités de volontariat")),

    build_column_couple('dedommagement_victime_amiante', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante")),

    build_column_couple('prestation_compensatoire', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante")),

    )))
