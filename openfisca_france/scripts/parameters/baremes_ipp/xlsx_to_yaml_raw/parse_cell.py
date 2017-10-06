# -*- coding: utf-8 -*-

import logging
import re
import datetime

import openpyxl
from openpyxl.cell import Cell


log = logging.getLogger('xlsx_parser')


def read_cell(book, sheet, merged_cells_tree, row_index, column_index, empty_white_value = None):
    """Convert an XLS cell (type & value) to an unicode string.
    """
    unmerged_cell_coordinates = merged_cells_tree.get(row_index, {}).get(column_index)
    if unmerged_cell_coordinates is None:
        unmerged_row_index = row_index
        unmerged_column_index = column_index
    else:
        unmerged_row_index, unmerged_column_index = unmerged_cell_coordinates

    cell = sheet.cell(row=unmerged_row_index+1, column=unmerged_column_index+1)
    value = cell.value

    if cell.data_type == Cell.TYPE_FORMULA:
        from IPython.core.debugger import Tracer; Tracer()()

    if value is None:
        background_colour_index = cell.fill.start_color.index
        if background_colour_index == 8:
            value = None  # Blue blank cell: Value is known to not exist.
        else:
            value = empty_white_value  # White blank cell: Value is unknown but does exist.
    elif isinstance(value, unicode):
        if not value:
            value = None
    elif isinstance(value, bool):
        value = bool(value)
    elif cell.data_type == Cell.TYPE_NUMERIC:
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, long):
            value = int(value)
        if u'€' in cell.number_format:
            return value, 'EUR'
        if 'FRF' in cell.number_format:
            return value, 'FRF'
        if '%' in cell.number_format:
            return value*100, '%'
        return value
    else:
        assert False, str((cell.data_type, value))
    return value
