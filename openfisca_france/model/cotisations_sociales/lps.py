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

from numpy import maximum as max_

from ..data import QUIFOY


VOUS = QUIFOY['vous']


############################################################################
# # Impôt Landais, Piketty, Saez
############################################################################

def _base_csg(self, salbrut, chobrut, rstbrut, rev_cap_bar_holder, rev_cap_lib_holder):
    '''
    Assiette de la csg
    '''
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

    return salbrut + chobrut + rstbrut + rev_cap_bar + rev_cap_lib


def _ir_lps(self, base_csg, nbF_holder, nbH_holder, statmarit, _P):
    '''
    Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par
    Landais, Piketty, Saez (2011)
    '''
    nbF = self.cast_from_entity_to_role(nbF_holder, role = VOUS)
    nbH = self.cast_from_entity_to_role(nbH_holder, role = VOUS)

    P = _P.lps
    nbEnf = (nbF + nbH / 2)
    ae = nbEnf * P.abatt_enfant
    re = nbEnf * P.reduc_enfant
    ce = nbEnf * P.credit_enfant

    couple = (statmarit == 1) | (statmarit == 5)
    ac = couple * P.abatt_conj
    rc = couple * P.reduc_conj

    return -max_(0, P.bareme.calc(max_(base_csg - ae - ac, 0)) - re - rc) + ce
