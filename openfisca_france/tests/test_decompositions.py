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


import json
import os
import xml.etree.ElementTree

from openfisca_core import conv, decompositions, decompositionsxml

from openfisca_france.tests import base


def check_decomposition_xml_file(file_path):
    decomposition_tree = xml.etree.ElementTree.parse(os.path.join(file_path))
    decomposition_xml_json = conv.check(decompositionsxml.xml_decomposition_to_json)(decomposition_tree.getroot(),
        state = conv.default_state)

    decomposition_xml_json, errors = decompositionsxml.make_validate_node_xml_json(base.tax_benefit_system)(
        decomposition_xml_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(decomposition_xml_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(decomposition_xml_json, ensure_ascii = False,
                indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(decomposition_xml_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    decomposition_json = decompositionsxml.transform_node_xml_json_to_json(decomposition_xml_json)

    decomposition_json, errors = decompositions.make_validate_node_json(base.tax_benefit_system)(
        decomposition_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(decomposition_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(decomposition_json, ensure_ascii = False, indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(decomposition_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))


def test_decomposition_xml_files():
    decompositions_directory = base.tax_benefit_system.DECOMP_DIR
    files_path = [
        os.path.join(
            decompositions_directory,
            base.tax_benefit_system.DEFAULT_DECOMP_FILE,
            ),
        os.path.join(
            decompositions_directory,
            'fiche_de_paie_decomposition.xml',
            )
        ]
    for file_path in files_path:
        yield check_decomposition_xml_file, file_path


if __name__ == '__main__':
    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'test_decompositions:test_decomposition_xml_files'])
