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


import copy
import datetime
import jsonpatch
import xml.etree.ElementTree

from openfisca_core import conv, legislationsxml
from openfisca_core.reforms import Reform
import openfisca_france

TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_parametric_reform(year):
    legislation_tree = xml.etree.ElementTree.parse(TaxBenefitSystem.PARAM_FILE)
    legislation_xml_json = conv.check(legislationsxml.xml_legislation_to_json)(
        legislation_tree.getroot(),
        state = conv.default_state
        )
    _, legislation_json = legislationsxml.transform_node_xml_json_to_json(legislation_xml_json)

    legislation_json_src = legislation_json
#    import json
#    with open("/tmp/src.json", "w") as f:
#        f.write(
#            json.dumps(legislation_json_src, ensure_ascii = False, encoding = "utf8", indent = 2).encode("utf8"))
#    print str((legislation_json_src['children']['ir']['children']['bareme']['slices'][0]['rate'],))
#    print str((legislation_json_src['children']['ir']['children']['bareme']['slices'][1]['rate'],))
    legislation_json_reform = copy.deepcopy(legislation_json_src)
    legislation_json_reform['children']['ir']['children']['bareme']['slices'][0]['rate'][-1]['value'] = 1

    # import json_delta
    # json_delta: bug with ordered dicts
    #difference = json_delta.diff(p, p_copy)

#    from dictdiffer import diff, patch, swap, revert
#    difference = diff(p, p_copy)
#    print difference (ugly)

    legislation_json_patch = jsonpatch.make_patch(legislation_json_src, legislation_json_reform)
    print legislation_json_patch

    reform = Reform(name = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche",
                    legislation_json_patch = legislation_json_patch)

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    assert max(abs(simulation.calculate('impo') - [0, -7889.20019531, -23435.52929688])) < .0001
    tax_benefit_system.apply_reform(reform = reform)
#    with open("/tmp/reform.json", "w") as f:
#        f.write(
#            json.dumps(
#                tax_benefit_system.legislation_json,
#                ensure_ascii = False,
#                encoding = "utf8",
#                indent = 2,
#                ).encode("utf8"))
    simulation2 = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    assert max(abs(simulation2.calculate('impo') - [0., -13900.20019531, -29446.52929688])) < .0001


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform(2014)
