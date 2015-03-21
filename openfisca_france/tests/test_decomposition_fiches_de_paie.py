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


from __future__ import division

import json
import os

from openfisca_core import decompositions
from openfisca_france.tests.base import tax_benefit_system


def test_decomposition(print_decomposition = False):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            code_postal_entreprise = "75001",
            ratio_alternants = .025,
            salaire_de_base = {"2013": 12 * 3000},
            taille_entreprise = 3,
            type_sal = 0,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation(debug = True)

    xml_file_path = os.path.join(
        tax_benefit_system.DECOMP_DIR,
        "fiche_de_paie_decomposition.xml"
        )

    decomposition_json = decompositions.get_decomposition_json(tax_benefit_system, xml_file_path = xml_file_path)
    simulations = [simulation]
    response = decompositions.calculate(simulations, decomposition_json)
    if print_decomposition:
        print unicode(
            json.dumps(response, encoding = 'utf-8', ensure_ascii = False, indent = 2)
            )


if __name__ == '__main__':
    import argparse
    import logging
    import sys

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

#    test_decomposition(print_decomposition = True)
