#! /usr/bin/env python
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


"""Generate the columns tree from flat dictionary of columns.

When tree already exists, don't change location of columns that have already been placed in tree.
"""


import argparse
import codecs
import collections
import itertools
import json
import logging
import os
import pprint
import sys

from openfisca_france.model import data
try:
    from openfisca_france.model.datatrees import columns_name_tree_by_entity
except ImportError:
    columns_name_tree_by_entity = collections.OrderedDict()


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def iter_tree(tree):
    assert tree.get('children'), tree
    for child in (tree.get('children') or []):
        if isinstance(child, basestring):
            # Child is a column name.
            yield child
        else:
            assert isinstance(child, dict), child
            for column_name in iter_tree(child):
                yield column_name


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    placed_columns_name = set(
        column_name
        for columns_name_tree in columns_name_tree_by_entity.itervalues()
        for column_name in iter_tree(columns_name_tree)
        )

    for name, column in data.column_by_name.iteritems():
        if name in ('age', 'agem', 'idfam', 'idfoy', 'idmen', 'noi', 'quifam', 'quifoy', 'quimen'):
            continue
        if column.survey_only:
            continue
        if name in placed_columns_name:
            continue
        placed_columns_name.add(name)
        entity_children = columns_name_tree_by_entity.setdefault(column.entity, collections.OrderedDict()).setdefault(
            'children', [])
        if entity_children and entity_children[-1].get('label') == u'Autres':
            last_entity_child = entity_children[-1]
        else:
            last_entity_child = collections.OrderedDict(label = u'Autres')
            entity_children.append(last_entity_child)
        last_entity_child.setdefault('children', []).append(name)

    datatrees_module_path = os.path.join(os.path.dirname(data.__file__), 'datatrees.py') 
    with codecs.open(datatrees_module_path, 'w', encoding = 'utf-8') as datatree_file:
        datatree_file.write(u'''\
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


columns_name_tree_by_entity = collections.OrderedDict([
''')
        for entity in ('ind', 'fam', 'foy', 'men'):
            datatree_file.write(u'    ({}, '.format(pprint.pformat(entity)))
            write_tree(datatree_file, columns_name_tree_by_entity[entity])
            datatree_file.write(u'),\n')
        datatree_file.write(u'    ])\n')
    return 0


def write_tree(tree_file, tree, level = 1):
        tree_file.write(u'collections.OrderedDict([\n')
        label = tree.get('label')
        if label is not None:
            tree_file.write(u'    ' * (level + 1))
            tree_file.write(u"('label', {}),\n".format(pprint.pformat(label)))
        children = tree.get('children')
        if children is not None:
            tree_file.write(u'    ' * (level + 1))
            tree_file.write(u"('children', [\n".format(pprint.pformat(label)))
            for child in children:
                tree_file.write(u'    ' * (level + 2))
                if isinstance(child, basestring):
                    tree_file.write(pprint.pformat(child)),
                else:
                    write_tree(tree_file, child, level = level + 2)
                tree_file.write(u',\n')
            tree_file.write(u'    ' * (level + 2))
            tree_file.write(u"]),\n")
        tree_file.write(u'    ' * (level + 1))
        tree_file.write(u'])')


if __name__ == "__main__":
    sys.exit(main())
