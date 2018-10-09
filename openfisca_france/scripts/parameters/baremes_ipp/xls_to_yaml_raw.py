#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


"""Convert IPP's tax and benefit tables from XLS format to YAML, trying to preserve its content as much as possible."""


import collections
import datetime
import logging
import os
import re
import sys
import traceback

from biryani import baseconv, custom_conv, datetimeconv, states
from biryani import strings
import xlrd
import yaml


aad_re = re.compile(r'AAD(\s+[-+]\s+\d+\s+ans?)?$')
app_name = os.path.splitext(os.path.basename(__file__))[0]
conv = custom_conv(baseconv, datetimeconv, states)
french_date_re = re.compile(r'(?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])/(?P<year>[12]\d{3})$')
log = logging.getLogger(app_name)
number_re = re.compile(u'\d+\.?$')
parameters = []
year_re = re.compile(r'[12]\d{3}$')


# YAML configuration


class folded_unicode(unicode):  # noqa F821
    pass


class literal_unicode(unicode):  # noqa F821
    pass


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))  # noqa F821


# Converters


def input_to_french_date(value, state = None):
    if value is None:
        return None, None
    if state is None:
        state = conv.default_state
    match = french_date_re.match(value)
    if match is None:
        return value, state._(u'Invalid french date')
    return datetime.date(int(match.group('year')), int(match.group('month')), int(match.group('day'))), None


cell_to_row_first_cell = conv.condition(
    conv.test_isinstance(int),
    conv.pipe(
        conv.test_between(1914, 2020),
        conv.function(lambda year: datetime.date(year, 1, 1)),
        ),
    conv.pipe(
        conv.test_isinstance(basestring),  # noqa F821
        conv.first_match(
            conv.pipe(
                conv.test(lambda date: year_re.match(date), error = u'Not a valid year'),
                conv.function(lambda year: datetime.date(year, 1, 1)),
                ),
            input_to_french_date,
            conv.iso8601_input_to_date,
            conv.test(lambda value: aad_re.match(value) is not None, error = u'Not a valid "AAD"'),
            ),
        ),
    )


# Functions


def get_hyperlink(sheet, row_index, column_index):
    return sheet.hyperlink_map.get((row_index, column_index))


def get_unmerged_cell_coordinates(row_index, column_index, merged_cells_tree):
    unmerged_cell_coordinates = merged_cells_tree.get(row_index, {}).get(column_index)
    if unmerged_cell_coordinates is None:
        return row_index, column_index
    return unmerged_cell_coordinates


def transform_amount_tuple_to_str(amount):
    # Replace (value, unit) couple to a string.
    value, unit = amount
    if unit == u'%':
        value *= 100
    return u'{} {}'.format(value, unit)


def transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, column_index, empty_white_value = None):
    """Convert an XLS cell (type & value) to an unicode string.

    Code taken from http://code.activestate.com/recipes/546518-simple-conversion-of-excel-files-into-csv-and-yaml/

    Type Codes:
    EMPTY   0
    TEXT    1 a Unicode string
    NUMBER  2 float
    DATE    3 float
    BOOLEAN 4 int; 1 means TRUE, 0 means FALSE
    ERROR   5
    BLANK   6
    """
    unmerged_cell_coordinates = merged_cells_tree.get(row_index, {}).get(column_index)
    if unmerged_cell_coordinates is None:
        unmerged_row_index = row_index
        unmerged_column_index = column_index
    else:
        unmerged_row_index, unmerged_column_index = unmerged_cell_coordinates
    type = sheet.row_types(unmerged_row_index)[unmerged_column_index]
    value = sheet.row_values(unmerged_row_index)[unmerged_column_index]
    if type == 0:
        xf_index = sheet.cell_xf_index(row_index, column_index)
        xf = book.xf_list[xf_index]  # Get an XF object.
        background_colour_index = xf.background.background_colour_index
        if background_colour_index == 8:
            value = None  # Blue blank cell: Value is known to not exist.
        else:
            value = empty_white_value  # White blank cell: Value is unknown but does exist.
    elif type == 1:
        if not value:
            value = None
    elif type == 2:
        # NUMBER
        value_int = int(value)
        if value_int == value:
            value = value_int
        xf_index = sheet.cell_xf_index(row_index, column_index)
        xf = book.xf_list[xf_index]  # Get an XF object.
        format_key = xf.format_key
        format = book.format_map[format_key]  # Get a Format object.
        format_str = format.format_str  # This is the "number format string".
        if format_str in (
                u'0',
                u'0.000',
                u'0.00000',
                u'General',
                u'GENERAL',
                u'#,##0',
                u'_-* #,##0\ _€_-;\-* #,##0\ _€_-;_-* \-??\ _€_-;_-@_-',
                ) or format_str.endswith(u'0.00'):
            return value
        if u'€' in format_str:
            return (value, u'EUR')
        if u'FRF' in format_str or u'\F\R\F' in format_str or format_str.endswith(u'\ "F"'):
            return (value, u'FRF')
        assert format_str.endswith(u'%'), 'Unexpected format "{}" for value: {}'.format(format_str, value)
        return (value, u'%')
    elif type == 3:
        # DATE
        y, m, d, hh, mm, ss = xlrd.xldate_as_tuple(value, book.datemode)
        date = u'{0:04d}-{1:02d}-{2:02d}'.format(y, m, d) if any(n != 0 for n in (y, m, d)) else None
        value = u'T'.join(
            fragment
            for fragment in (
                date,
                (u'{0:02d}:{1:02d}:{2:02d}'.format(hh, mm, ss)
                    if any(n != 0 for n in (hh, mm, ss)) or date is None
                    else None),
                )
            if fragment is not None
            )
    elif type == 4:
        value = bool(value)
    elif type == 5:
        # ERROR
        value = xlrd.error_text_from_code[value]
    elif type == 6:
        xf_index = sheet.cell_xf_index(row_index, column_index)
        xf = book.xf_list[xf_index]  # Get an XF object.
        background_colour_index = xf.background.background_colour_index
        if background_colour_index == 8:
            value = None  # Blue blank cell: Value is known to not exist.
        else:
            value = empty_white_value  # White blank cell: Value is unknown but does exist.
    else:
        assert False, str((type, value))
    return value


def transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index, column_index, empty_white_value = None):
    cell = transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, column_index,
        empty_white_value = empty_white_value)
    if isinstance(cell, int):
        # Convert integer (a date) to a string.
        cell = unicode(cell)  # noqa F821
    if isinstance(cell, tuple):
        cell = transform_amount_tuple_to_str(cell)
    assert cell is None or isinstance(cell, basestring), u'Expected a string. Got: {}'.format(cell).encode('utf-8')  # noqa F821
    return cell


def transform(xls_dir, yaml_raw_dir):
    file_system_encoding = sys.getfilesystemencoding()

    error_by_book_name = collections.OrderedDict()
    warning_by_book_name = collections.OrderedDict()
    for filename_encoded in sorted(os.listdir(xls_dir)):
        if not filename_encoded.endswith('.xls'):
            continue
        filename = filename_encoded.decode(file_system_encoding)
        log.info(u'Parsing file {}'.format(filename))
        book_name = os.path.splitext(filename)[0]
        xls_path_encoded = os.path.join(xls_dir, filename_encoded)
        book = xlrd.open_workbook(filename = xls_path_encoded, formatting_info = True)

        book_yaml_dir_encoded = os.path.join(yaml_raw_dir, strings.slugify(book_name).encode(file_system_encoding))
        if not os.path.exists(book_yaml_dir_encoded):
            os.makedirs(book_yaml_dir_encoded)

        error_by_sheet_name = collections.OrderedDict()
        sheet_english_title_by_name = collections.OrderedDict()
        sheet_title_by_name = collections.OrderedDict()
        warning_by_sheet_name = collections.OrderedDict()
        for sheet_name in book.sheet_names():
            log.info(u'  Parsing sheet {}.'.format(sheet_name))
            sheet = book.sheet_by_name(sheet_name)
            sheet_error = None
            sheet_warning = None

            try:
                # Extract coordinates of merged cells.
                merged_cells_tree = {}
                for row_low, row_high, column_low, column_high in sheet.merged_cells:
                    for row_index in range(row_low, row_high):
                        cell_coordinates_by_merged_column_index = merged_cells_tree.setdefault(
                            row_index, {})
                        for column_index in range(column_low, column_high):
                            cell_coordinates_by_merged_column_index[column_index] = (row_low, column_low)

                if sheet_name.startswith((u'Sommaire', u'Outline')):
                    french = sheet_name.startswith(u'Sommaire')
                    # Associate the titles of the sheets to their Excel names.
                    book_title = transform_xls_cell_to_str(book, sheet, merged_cells_tree, 1, 1)
                    if not book_title:
                        book_title = transform_xls_cell_to_str(book, sheet, merged_cells_tree, 2, 1)
                    book_title = book_title.strip()
                    assert book_title
                    book_description = transform_xls_cell_to_str(book, sheet, merged_cells_tree, 4, 1)
                    if not book_description:
                        book_description = transform_xls_cell_to_str(book, sheet, merged_cells_tree, 5, 1)
                    book_description = book_description.strip()
                    assert book_description

                    for column_index in range(1, 4):
                        current_heading = u'Annexes' if french else u'Annexes'
                        sheet_title_by_slug_by_heading = collections.OrderedDict()
                        for row_index in range(sheet.nrows):
                            heading = transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, 1)
                            if isinstance(heading, basestring):  # noqa F821
                                heading = heading.strip()
                                if not heading:
                                    continue
                                if heading == book_title or heading == book_description:
                                    continue
                                if number_re.match(heading) is None:
                                    current_heading = heading
                                    continue
                            linked_sheet_number = transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index,
                                column_index)
                            if isinstance(linked_sheet_number, int) or (isinstance(linked_sheet_number, basestring) and number_re.match(linked_sheet_number) is not None):  # noqa F821
                                linked_sheet_title = transform_xls_cell_to_str(book, sheet, merged_cells_tree,
                                    row_index, column_index + 1)
                                if linked_sheet_title is not None:
                                    linked_sheet_title = linked_sheet_title.strip()
                                if linked_sheet_title:
                                    hyperlink = get_hyperlink(sheet, row_index, column_index + 1)
                                    if hyperlink is not None and hyperlink.type == u'workbook':
                                        linked_sheet_name = hyperlink.textmark.split(u'!', 1)[0].strip(u'"').strip(u"'")
                                        sheet_title_by_slug = sheet_title_by_slug_by_heading.setdefault(current_heading,
                                            collections.OrderedDict())
                                        sheet_title_by_slug[strings.slugify(linked_sheet_name)] = linked_sheet_title

                                        if french:
                                            sheet_title_by_name[linked_sheet_name] = linked_sheet_title
                                        else:
                                            sheet_english_title_by_name[linked_sheet_name] = linked_sheet_title
                        if sheet_title_by_slug_by_heading:
                            break
                    assert sheet_title_by_slug_by_heading

                    book_notes = []
                    for column_index in range(8, 12):
                        for row_index in range(sheet.nrows):
                            note = transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index, column_index)
                            if note and note.strip() == book_description:
                                continue
                            if book_notes or note:
                                book_notes.append((note or u'').rstrip())
                                if note:
                                    blank_notes_count = 0
                                elif blank_notes_count >= 1:
                                    break
                                else:
                                    blank_notes_count += 1
                        if book_notes:
                            break
                    while book_notes and not book_notes[-1]:
                        del book_notes[-1]
                    assert book_notes

                    sheet_node = collections.OrderedDict((
                        (u'Titre' if french else u'Title', book_title),
                        (u'Description' if french else u'Description', book_description),
                        (u'Sommaire' if french else u'Table of Content', sheet_title_by_slug_by_heading),
                        (u'Notes' if french else u'Notes', literal_unicode(u'\n'.join(book_notes))),
                        (u'Données initiales' if french else u'Source Data', collections.OrderedDict((
                            (u'Producteur' if french else u'Producer', u'Institut des politiques publiques'),
                            (u'Format', u'XLS'),
                            (u'URL', u'http://www.ipp.eu/outils/baremes-ipp/' if french
                                else u'http://www.ipp.eu/en/tools/ipp-tax-and-benefit-tables/'),
                            ))),
                        (u'Convertisseur' if french else u'Converter', collections.OrderedDict((
                            (u'URL', u'https://git.framasoft.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters'),  # noqa
                            ))),
                        (u'Données générées' if french else u'Generated Data', collections.OrderedDict((
                            (u'Format', u'YAML'),
                            (u'URL', u'https://git.framasoft.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-yaml-raw'),  # noqa
                            ))),
                        (u'Licence' if french else u'License',
                            u'Licence ouverte <http://www.etalab.gouv.fr/licence-ouverte-open-licence>' if french
                            else u'Open Licence <http://www.etalab.gouv.fr/licence-ouverte-open-licence>'),
                        ))

                    yaml_file_path_encoded = os.path.join(
                        book_yaml_dir_encoded,
                        (strings.slugify(sheet_name, transform = strings.upper) + u'.yaml').encode(
                            file_system_encoding),
                        )
                elif sheet_name.startswith(u'Abréviation'):
                    log.warning(u'    Ignoring sheet {} of book {}.'.format(sheet_name, book_name))
                    sheet_warning = u'Sheet ignored.'

                    sheet_title = sheet_title_by_name.get(sheet_name, sheet_name)
                    sheet_node = collections.OrderedDict((
                        (u'Titre' if french else u'Title', sheet_title),
                        ))

                    yaml_file_path_encoded = os.path.join(
                        book_yaml_dir_encoded,
                        (strings.slugify(sheet_name, transform = strings.upper) + u'.yaml').encode(
                            file_system_encoding),
                        )
                else:
                    descriptions_rows = []
                    labels_rows = []
                    notes_rows = []
                    state = 'taxipp_names'
                    taxipp_names_row = None
                    values_rows = []
                    for row_index in range(sheet.nrows):
                        columns_count = len(sheet.row_values(row_index))
                        if state == 'taxipp_names':
                            taxipp_names_row = [
                                (taxipp_name or u'').strip()
                                for taxipp_name in (
                                    transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index, column_index)
                                    for column_index in range(columns_count)
                                    )
                                ]
                            state = 'labels'
                            if all(
                                    not taxipp_name
                                    for taxipp_name in taxipp_names_row
                                    ):
                                # The first row is empty => This sheet doesn't contain TaxIPP names.
                                continue
                            # When any TaxIPP name is in lowercase, assume that this row is really the TaxIPP names row.
                            if any(
                                    taxipp_name and taxipp_name[0].islower()
                                    for taxipp_name in taxipp_names_row
                                    ):
                                continue
                            else:
                                log.info(u'    Sheet "{}" of XLS file "{}" has no row for TaxIPP names.'.format(
                                    sheet_name, filename))
                                # warning = u'Row not found'
                                # if sheet_warning is None:
                                #     sheet_warning = collections.OrderedDict()
                                # if isinstance(sheet_warning, dict):
                                #     sheet_warning[u'Noms TaxIPP'] = warning
                                # else:
                                #     assert isinstance(sheet_warning, basestring), sheet_warning
                                #     sheet_warning = u'\n\n'.join(
                                #         fragment
                                #         for fragment in (sheet_warning, warning)
                                #         if fragment
                                #         )
                                taxipp_names_row = []
                        if state == 'labels':
                            first_cell_value, error = conv.pipe(cell_to_row_first_cell, conv.not_none)(
                                transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, 0),
                                state = conv.default_state)
                            if error is not None:
                                # First cell of row is not a the first cell of a row of values => Assume it is a label.
                                labels_rows.append([
                                    u' '.join((label or u'').split()).strip()
                                    for label in (
                                        transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index,
                                            column_index)
                                        for column_index in range(columns_count)
                                        )
                                    ])
                                continue
                            state = 'values'
                        if state == 'values':
                            first_cell_value, error = cell_to_row_first_cell(
                                transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, 0),
                                state = conv.default_state)
                            if error is None:
                                # First cell of row is a valid date or year.
                                values_row = [
                                    value.strip() if isinstance(value, basestring) else value  # noqa F821
                                    for value in (
                                        transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index,
                                            column_index, empty_white_value = u'nc')
                                        for column_index in range(columns_count)
                                        )
                                    ]
                                if isinstance(first_cell_value, datetime.date):
                                    assert first_cell_value.year < 2601, 'Invalid date {} in {} at row {}'.format(
                                        first_cell_value, sheet_name, row_index + 1)
                                    values_rows.append(values_row)
                                    continue
                                if isinstance(first_cell_value, basestring) and aad_re.match(first_cell_value) is not None:  # noqa F821
                                    values_rows.append(values_row)
                                    continue
                                if all(value in (None, u'', u'nc') for value in values_row):
                                    # If first cell is empty and all other cells in line are also empty, ignore this
                                    # line.
                                    continue
                                # First cell has no date and other cells in row are not empty => Assume it is a note.
                            state = 'notes'
                        if state == 'notes':
                            first_cell_value = transform_xls_cell_to_json(book, sheet, merged_cells_tree, row_index, 0)
                            if isinstance(first_cell_value, basestring) and first_cell_value.strip().lower() == 'notes':  # noqa F821
                                notes_rows.append([
                                    (line or u'').rstrip()
                                    for line in (
                                        transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index,
                                            column_index)
                                        for column_index in range(columns_count)
                                        )
                                    ])
                                continue
                            state = 'description'
                        assert state == 'description'
                        descriptions_rows.append([
                            (line or u'').strip()
                            for line in (
                                transform_xls_cell_to_str(book, sheet, merged_cells_tree, row_index, column_index)
                                for column_index in range(columns_count)
                                )
                            ])

                    sheet_node = collections.OrderedDict()

                    sheet_title = sheet_title_by_name.get(sheet_name)
                    if sheet_title is not None:
                        sheet_node[u'Titre'] = sheet_title

                    sheet_node[u'Titre court'] = sheet_name

                    labels = []
                    for labels_row in labels_rows:
                        for column_index, label in enumerate(labels_row):
                            if label is None:
                                continue
                            label = label.strip()
                            if not label:
                                continue
                            while column_index >= len(labels):
                                labels.append([])
                            column_labels = labels[column_index]
                            if not column_labels or column_labels[-1] != label:
                                column_labels.append(label)
                    labels = [
                        (tuple(
                            label_stripped
                            for label_stripped in (
                                (label or u'').strip()
                                for label in column_labels1
                                )
                            if label_stripped
                            ) if column_labels1 else None) or (u'Colonne sans titre',)
                        for index, column_labels1 in enumerate(labels, 1)
                        ]
                    assert labels

                    taxipp_name_by_column_labels = collections.OrderedDict()
                    for column_labels, taxipp_name in zip(labels, taxipp_names_row):
                        if not taxipp_name:
                            continue
                        taxipp_name_by_column_label = taxipp_name_by_column_labels
                        for column_label in column_labels[:-1]:
                            taxipp_name_by_column_label = taxipp_name_by_column_label.setdefault(column_label,
                                collections.OrderedDict())
                        taxipp_name_by_column_label[column_labels[-1]] = taxipp_name
                    if taxipp_name_by_column_labels:
                        sheet_node[u'Noms TaxIPP'] = taxipp_name_by_column_labels

                    sheet_values = []
                    for value_row in values_rows:
                        cell_by_column_labels = collections.OrderedDict()
                        for column_labels, cell in zip(labels, value_row):
                            if cell is None or cell == '':
                                continue
                            cell_by_column_label = cell_by_column_labels
                            for column_label in column_labels[:-1]:
                                cell_by_column_label = cell_by_column_label.setdefault(column_label,
                                    collections.OrderedDict())
                            # Merge (amount, unit) couples to a string to simplify YAML.
                            if isinstance(cell, tuple):
                                cell = transform_amount_tuple_to_str(cell)
                            if isinstance(cell, basestring) and u'\n' in cell:  # noqa F821
                                cell = literal_unicode(cell)
                            cell_by_column_label[column_labels[-1]] = cell
                        sheet_values.append(cell_by_column_labels)
                    if sheet_values:
                        sheet_node[u'Valeurs'] = sheet_values

                    notes = u'\n'.join([
                        line.rstrip()
                        for line in u'\n'.join([
                            u' | '.join(
                                cell for cell in row
                                if cell
                                ).rstrip()
                            for row in notes_rows
                            ]).split(u'\n')
                        ]).rstrip()
                    if notes:
                        sheet_node[u'Notes'] = literal_unicode(notes)

                    description = u'\n'.join([
                        line.rstrip()
                        for line in u'\n'.join([
                            u' | '.join(
                                cell for cell in row
                                if cell
                                ).rstrip()
                            for row in descriptions_rows
                            ]).split(u'\n')
                        ]).rstrip()
                    if description:
                        sheet_node[u'Description'] = literal_unicode(description)

                    yaml_file_path_encoded = os.path.join(
                        book_yaml_dir_encoded,
                        (strings.slugify(sheet_name) + u'.yaml').encode(file_system_encoding),
                        )

                if sheet_error:
                    sheet_node[u'ERRORS'] = literal_unicode(sheet_error) \
                        if isinstance(sheet_error, basestring) and u'\n' in sheet_error else sheet_error  # noqa F821
                if sheet_warning:
                    sheet_node[u'WARNINGS'] = literal_unicode(sheet_warning) \
                        if isinstance(sheet_warning, basestring) and u'\n' in sheet_warning else sheet_warning  # noqa F821
                with open(yaml_file_path_encoded, 'w') as yaml_file:
                    yaml.dump(sheet_node, yaml_file, allow_unicode = True, default_flow_style = False, indent = 2,
                        width = 120)
            except:  # noqa E722
                message = u'An exception occurred when parsing sheet "{}" of XLS file "{}".'.format(sheet_name,
                    filename)
                log.exception(u'    {}'.format(message))
                sheet_error = literal_unicode(u'\n\n'.join(
                    fragment
                    for fragment in (
                        unicode(sheet_error) if sheet_error is not None else None,  # noqa F821
                        message,
                        traceback.format_exc().decode('utf-8'),
                        )
                    if fragment
                    ))

            if sheet_error:
                error_by_sheet_name[sheet_name] = sheet_error
            if sheet_warning:
                warning_by_sheet_name[sheet_name] = sheet_warning

        if error_by_sheet_name:
            yaml_file_path_encoded = os.path.join(
                book_yaml_dir_encoded,
                u'ERRORS.yaml'.encode(file_system_encoding),
                )
            with open(yaml_file_path_encoded, 'w') as yaml_file:
                yaml.dump(error_by_sheet_name, yaml_file, allow_unicode = True, default_flow_style = False,
                    indent = 2, width = 120)
            error_by_book_name[book_name] = error_by_sheet_name
        if warning_by_sheet_name:
            yaml_file_path_encoded = os.path.join(
                book_yaml_dir_encoded,
                u'WARNINGS.yaml'.encode(file_system_encoding),
                )
            with open(yaml_file_path_encoded, 'w') as yaml_file:
                yaml.dump(warning_by_sheet_name, yaml_file, allow_unicode = True, default_flow_style = False,
                    indent = 2, width = 120)
            warning_by_book_name[book_name] = warning_by_sheet_name

    if error_by_book_name:
        yaml_file_path_encoded = os.path.join(
            yaml_raw_dir,
            u'ERRORS.yaml'.encode(file_system_encoding),
            )
        with open(yaml_file_path_encoded, 'w') as yaml_file:
            yaml.dump(error_by_book_name, yaml_file, allow_unicode = True, default_flow_style = False, indent = 2,
                width = 120)
    if warning_by_book_name:
        yaml_file_path_encoded = os.path.join(
            yaml_raw_dir,
            u'WARNINGS.yaml'.encode(file_system_encoding),
            )
        with open(yaml_file_path_encoded, 'w') as yaml_file:
            yaml.dump(warning_by_book_name, yaml_file, allow_unicode = True, default_flow_style = False, indent = 2,
                width = 120)
