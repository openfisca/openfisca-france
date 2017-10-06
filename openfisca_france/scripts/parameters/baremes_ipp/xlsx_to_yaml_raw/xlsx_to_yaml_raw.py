#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Convert IPP's tax and benefit tables from XLSX format to YAML"""


import collections
import logging
import os
import sys

from biryani import strings

import openpyxl
import yaml

from parse_sheet import parse_sheet, literal_unicode


log = logging.getLogger('xlsx_parser')



class folded_unicode(unicode):
    pass

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))



def transform(xls_dir, yaml_raw_dir):
    file_system_encoding = sys.getfilesystemencoding()

    error_by_book_name = collections.OrderedDict()
    for filename_encoded in sorted(os.listdir(xls_dir)):
        if not filename_encoded.endswith('.xlsx'):
            continue
        filename = filename_encoded.decode(file_system_encoding)
        log.info(u'Parsing file {}'.format(filename))
        book_name = os.path.splitext(filename)[0]
        xls_path_encoded = os.path.join(xls_dir, filename_encoded)
        book = openpyxl.load_workbook(filename=xls_path_encoded, data_only=True)  # data_only=True : no formulas

        book_yaml_dir_encoded = os.path.join(yaml_raw_dir, strings.slugify(book_name).encode(file_system_encoding))
        if not os.path.exists(book_yaml_dir_encoded):
            os.makedirs(book_yaml_dir_encoded)

        error_by_sheet_name = collections.OrderedDict()
        sheet_title_by_name = collections.OrderedDict()
        for sheet_name in book.get_sheet_names():
            sheet_title_by_name, sheet_error = parse_sheet(book, sheet_name, sheet_title_by_name, book_yaml_dir_encoded)

            if sheet_error:
                error_by_sheet_name[sheet_name] = sheet_error

        if error_by_sheet_name:
            yaml_file_path_encoded = os.path.join(
                book_yaml_dir_encoded,
                u'ERRORS.yaml'.encode(file_system_encoding),
                )
            with open(yaml_file_path_encoded, 'w') as yaml_file:
                yaml.dump(error_by_sheet_name, yaml_file, allow_unicode = True, default_flow_style = False,
                    indent = 2, width = 120)
            error_by_book_name[book_name] = error_by_sheet_name

    if error_by_book_name:
        yaml_file_path_encoded = os.path.join(
            yaml_raw_dir,
            u'ERRORS.yaml'.encode(file_system_encoding),
            )
        with open(yaml_file_path_encoded, 'w') as yaml_file:
            yaml.dump(error_by_book_name, yaml_file, allow_unicode = True, default_flow_style = False, indent = 2,
                width = 120)
