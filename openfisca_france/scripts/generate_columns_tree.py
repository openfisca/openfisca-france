#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate the columns tree from flat dictionary of columns.

When tree already exists, don't change location of columns that have already been placed in tree.
"""


import argparse
import collections
import logging
import os
import pprint
import sys

from openfisca_core import formulas

from openfisca_france import FranceTaxBenefitSystem, model
try:
    from openfisca_france.model.datatrees import columns_name_tree_by_entity
except ImportError:
    columns_name_tree_by_entity = collections.OrderedDict()


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
tax_benefit_system = FranceTaxBenefitSystem()


class PrettyPrinter(pprint.PrettyPrinter):
    """Override pprint PrettyPrinter to correctly handle diacritical characters."""
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return ('u"""{}"""'.format(object.encode('utf8')), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

pretty_printer = PrettyPrinter()


def cleanup_tree(entity, tree):
    children = []
    for child in (tree.get('children') or []):
        if isinstance(child, basestring):
            # Child is a column name.
            column = tax_benefit_system.column_by_name.get(child)
            if column is not None and column.entity == entity and is_valid_input_column(column):
                children.append(child)
        else:
            assert isinstance(child, dict), child
            if child.get('label') != u'Autres':
                child = cleanup_tree(entity, child)
                if child is not None:
                    children.append(child)
    if not children:
        return None
    tree = tree.copy()
    tree['children'] = children
    return tree


def is_valid_input_column(column):
    return column.name not in ('age', 'age_en_mois', 'idfam', 'idfoy', 'idmen', 'quifam', 'quifoy', 'quimen') \
        and issubclass(column.formula_class, formulas.SimpleFormula) and column.formula_class.function is None \
        and not column.survey_only


def iter_placed_tree(tree):
    assert tree.get('children'), tree
    for child in tree['children']:
        if isinstance(child, basestring):
            # Child is a column name.
            yield child
        else:
            if child.get('label') != u'Autres':
                for column_name in iter_placed_tree(child):
                    yield column_name


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    global columns_name_tree_by_entity
    columns_name_tree_by_entity = collections.OrderedDict(
        (entity, columns_name_tree)
        for entity, columns_name_tree in (
            (entity1, cleanup_tree(entity1, columns_name_tree1))
            for entity1, columns_name_tree1 in columns_name_tree_by_entity.iteritems()
            )
        if columns_name_tree is not None
        )
    placed_columns_name = set(
        column_name
        for columns_name_tree in columns_name_tree_by_entity.itervalues()
        for column_name in iter_placed_tree(columns_name_tree)
        )

    for name, column in tax_benefit_system.column_by_name.iteritems():
        if not is_valid_input_column(column):
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

    datatrees_module_path = os.path.join(os.path.dirname(model.__file__), 'datatrees.py')
    with open(datatrees_module_path, 'w') as datatree_file:
        datatree_file.write('''\
# -*- coding: utf-8 -*-

import collections


columns_name_tree_by_entity = collections.OrderedDict([
''')
        for entity in ('ind', 'fam', 'foy', 'men'):
            datatree_file.write('    ({}, '.format(pretty_printer.pformat(entity)))
            write_tree(datatree_file, columns_name_tree_by_entity[entity])
            datatree_file.write('),\n')
        datatree_file.write('    ])\n')
    return 0


def write_tree(tree_file, tree, level = 1):
        tree_file.write('collections.OrderedDict([\n')
        label = tree.get('label')
        if label is not None:
            tree_file.write('    ' * (level + 1))
            tree_file.write("('label', {}),\n".format(pretty_printer.pformat(label)))
        children = tree.get('children')
        if children is not None:
            tree_file.write('    ' * (level + 1))
            tree_file.write("('children', [\n".format(pretty_printer.pformat(label)))
            for child in children:
                tree_file.write('    ' * (level + 2))
                if isinstance(child, basestring):
                    tree_file.write(pretty_printer.pformat(child))
                    tree_file.write(',')
                    column = tax_benefit_system.column_by_name[child]
                    label = column.label
                    if label is not None:
                        label = label.strip() or None
                        if label == child:
                            label = None
                        if label is not None:
                            tree_file.write('  # ')
                            tree_file.write(column.label.strip().encode('utf-8'))
                    tree_file.write('\n')
                else:
                    write_tree(tree_file, child, level = level + 2)
                    tree_file.write(',\n')
            tree_file.write('    ' * (level + 2))
            tree_file.write("]),\n")
        tree_file.write('    ' * (level + 1))
        tree_file.write('])')


if __name__ == "__main__":
    sys.exit(main())
