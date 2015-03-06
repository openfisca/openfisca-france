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


def montant_csg_crds(base_avec_abattement = None, base_sans_abattement = None, indicatrice_taux_plein = None,
        indicatrice_taux_reduit = None, law_node = None, plafond_securite_sociale = None):
    assert law_node is not None
    assert plafond_securite_sociale is not None
    if base_sans_abattement is None:
        base_sans_abattement = 0
    if base_avec_abattement is None:
        base = base_sans_abattement
    else:
        base = base_avec_abattement - law_node.abattement.calc(
            base_avec_abattement,
            factor = plafond_securite_sociale,
            round_base_decimals = 2,
            ) + base_sans_abattement
    if indicatrice_taux_plein is None and indicatrice_taux_reduit is None:
        return -law_node.taux * base
    else:
        return - (law_node.taux_plein * indicatrice_taux_plein + law_node.taux_reduit * indicatrice_taux_reduit) * base
