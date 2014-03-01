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


from __future__ import division

import logging

import openfisca_france
openfisca_france.init_country()
from openfisca_core.baremes import BaremeDict, scaleBaremes
from openfisca_core.enumerations import Enum
from openfisca_core.simulations import ScenarioSimulation

TAUX_DE_PRIME = 1 / 4  # primes (hors supplément familial et indemnité de résidence) / rémunération brute


CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])

DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'

from openfisca_core.legislations import CompactNode


log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés)
#        salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)
#        salaire total 0,55%


from openfisca_france.model.cotisations_sociales.travail import build_sal, build_pat

def modify_parameters(simulation = None):

    if simulation is None:
        simulation = ScenarioSimulation()
        simulation.set_config(year = 2013)
        simulation.set_param()

        print len(simulation.column_by_name)

    for _P in [simulation.P, simulation.P_default]:

        sal = build_sal(_P)
        pat = build_pat(_P)

        _P.cotsoc.__dict__['cotisations_patronales'] = CompactNode()
        _P.cotsoc.__dict__['cotisations_salariales'] = CompactNode()

        for cotisation_name, bareme_dict in {'cotisations_patronales' : pat, 'cotisations_salariales': sal}.iteritems():
            for category in bareme_dict:
                if category in CAT._nums:
                    _P.cotsoc.__dict__[cotisation_name].__dict__[category] = bareme_dict[category]
# model dans legislation
# recherchez à partir du dated_le... qui est dans legilation_test


if __name__ == '__main__':

    modify_parameters()
