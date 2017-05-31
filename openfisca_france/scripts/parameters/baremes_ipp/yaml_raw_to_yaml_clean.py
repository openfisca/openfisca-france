# -*- coding: utf-8 -*-


"""Clean up YAML files extracted from IPP's tax and benefit tables."""


import collections
import datetime
import logging
import os
import re
import sys

from biryani import baseconv, custom_conv, datetimeconv, states, strings
import yaml


enable_warnings = True

aad_re = re.compile(ur'AAD(\s+[-+]\s+\d+\s+ans?)?$')
ans_et_mois_re = re.compile(ur"\d+ ans( \d+ mois)?$")
app_name = u"cleanup_yaml"
apres_le_re = re.compile(ur'après le (?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])/(?P<year>[12]\d{3})$')
conv = custom_conv(baseconv, datetimeconv, states)
french_date_re = re.compile(ur'(?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])/(?P<year>[12]\d{3})$')
label_by_alias = {
    u"Commentaires": u"Notes",
    u"Date d'entrée en vigueur": u"Date d'effet",
    u"JORF": u"Parution au JO",
    u"Note": u"Notes",
    u"Parution au JORF": u"Parution au JO",
    u"Publication au JO": u"Parution au JO",
    u"Publication au JORF": u"Parution au JO",
    u"Publication JO": u"Parution au JO",
    u"Référence": u"Références législatives",
    u"Référence legislative": u"Références législatives",
    u"Référence législative": u"Références législatives",
    u"Référence législative - revalorisation des plafonds": u"Références législatives - revalorisation des plafonds",
    u"Référence législative de tous les autres paramètres": u"Références législatives de tous les autres paramètres",
    u"Référence BOI": u"Références BOI",
    u"Références": u"Références législatives",
    u"Références AGIRC": u"Références législatives",
    u"Références législatives (3)": u"Références législatives",
    u"Références législatives (taux d'appel)": u"Références législatives",
    u"Références législatives (taux de cotisation)": u"Références législatives",
    u"Références législatives ou BOI": u"Références législatives",
    u"Remarques": u"Notes",
    }
limite_age_re = re.compile(ur"limite d'âge( - \d+ trimestres?)?$")
log = logging.getLogger(app_name)
trimestres_re = re.compile(ur"\d+ trimestres?$")
year_re = re.compile(ur'[12]\d{3}$')


def N_(message):
    return message


# YAML configuration


class folded_unicode(unicode):
    pass


class literal_unicode(unicode):
    pass


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))


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


def convert_amount_or_number_tree(value, state = None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_amount_or_number_tree,
                drop_none_values = True,
                ),
            conv.empty_to_none,
            ),
        conv.first_match(
            conv.test_isinstance(int),
            conv.test_isinstance(float),
            conv.test_conv(
                conv.pipe(
                    conv.test_isinstance(basestring),
                    conv.function(lambda value: value.lower()),
                    conv.first_match(
                        conv.test_in([
                            u'-',  # TODO: Remove. Only "nc" is valid.
                            u'gmr 2',
                            u'na',  # TODO: Remove. Only "nc" is valid.
                            u'nc',
                            u"pas d'âge minimum",
                            u'pas de limite',
                            u'smic',
                            ]),
                        conv.test(lambda value: value.startswith((
                            u'disparition',
                            u'même',
                            u'plafond',
                            ))),
                        conv.test(lambda value: ans_et_mois_re.match(value) is not None),
                        conv.test(lambda value: apres_le_re.match(value) is not None),
                        conv.test(lambda value: limite_age_re.match(value) is not None),
                        conv.test(lambda value: trimestres_re.match(value) is not None),
                        ),
                    ),
                ),
            conv.pipe(
                conv.test_isinstance(basestring),
                conv.function(lambda value: value.rstrip(u'*')),
                conv.function(lambda value: value.rsplit(None, 1)),
                conv.test(lambda couple: len(couple) == 2, error = N_(u"Invalid (amount, unit) couple")),
                conv.struct(
                    (
                        conv.pipe(
                            # Remove spaces and replace french decimal comma with a french dot.
                            conv.function(lambda value: value.replace(u'\xa0', u'').replace(u' ', u'').replace(
                                u',', u'.')),
                            conv.input_to_float,
                            conv.not_none,
                            ),
                        conv.pipe(
                            conv.function(lambda value: value.upper()),
                            conv.translate({u'F': u'FRF', u'€': u'EUR'}),
                            conv.test_in([
                                u'%',
                                u'AF',  # anciens francs
                                u'CFA',  # francs CFA
                                u'COTISATIONS',
                                u'EUR',
                                u'FRF',
                                ]),
                            ),
                        ),
                    ),
                conv.function(lambda couple: u' '.join([unicode(couple[0]), couple[1]])),
                ),
            conv.fail(error = N_(u'Value is neither a number nor an amount (with a unit)')),
            ),
        )(value, state = state or conv.default_state)


def convert_date_tree(value, state = None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_date_tree,
                drop_none_values = True,
                ),
            conv.empty_to_none,
            ),
        conv.condition(
            conv.test_isinstance(int),
            conv.pipe(
                conv.test_between(1914, 2030),
                conv.function(lambda year: datetime.date(year, 1, 1)),
                ),
            conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.first_match(
                    conv.pipe(
                        conv.test(lambda date: year_re.match(date), error = N_(u'Not a valid year')),
                        conv.function(lambda year: datetime.date(year, 1, 1)),
                        ),
                    input_to_french_date,
                    conv.iso8601_input_to_date,
                    ),
                conv.test(lambda date: 1914 <= date.year <= 2030, error = N_(u'Date with invalid year')),
                ),
            ),
        )(value, state = state or conv.default_state)


def convert_line_tree(value, state = None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_line_tree,
                drop_none_values = True,
                ),
            conv.empty_to_none,
            ),
        conv.condition(
            conv.test_isinstance(basestring),
            conv.pipe(
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                ),
            ),
        )(value, state = state or conv.default_state)


def convert_taxipp_name_tree(value, state = None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_taxipp_name_tree,
                ),
            conv.empty_to_none,
            ),
        conv.pipe(
            conv.test_isinstance(basestring),
            conv.translate({u'nc': None}),
            conv.test(lambda taxipp_name: strings.slugify(taxipp_name, separator = u'_') == taxipp_name.strip(u'_'),
                error = N_(u'Invalid TaxIPP name')),
            ),
        )(value, state = state or conv.default_state)


def rename_keys(new_key_by_old_key):
    def rename_keys_converter(value, state = None):
        if value is None:
            return value, None
        renamed_value = value.__class__()
        for item_key, item_value in value.iteritems():
            new_key = new_key_by_old_key.get(item_key)
            if new_key is None:
                new_key = item_key
            else:
                assert new_key not in value, \
                    u'Renaming of key "{}" by "{}" failed, because new key is already used'.format(item_key,
                        new_key).encode('utf-8')
            renamed_value[new_key] = item_value
        return renamed_value, None

    return rename_keys_converter


def require_one_and_only_one_key(*keys):
    def require_one_and_only_one_key_converter(value, state = None):
        if value is None:
            return value, None
        if state is None:
            state = conv.default_state
        present_keys = set(
            item_key
            for item_key in value
            if item_key in keys
            )
        if not present_keys:
            message = state._(u'One of the following fields is required: {}').format(u', '.join(keys))
            return value, {
                key: message
                for key in keys
                }
        if len(present_keys) == 1:
            return value, None
        message = state._(u'Only one of the following fields must be present: {}').format(u', '.join(sorted(
            present_keys)))
        return value, {
            key: message
            for key in present_keys
            }

    return require_one_and_only_one_key_converter


def warn_keys_alias(new_key_by_old_key):
    def warn_keys_alias_converter(value, state = None):
        if value is None:
            return value, None
        warnings = collections.OrderedDict()
        for item_key, item_value in value.iteritems():
            label = new_key_by_old_key.get(item_key)
            if label is not None:
                warnings[item_key] = u'Label "{}" should be renamed to "{}"'.format(item_key, label)
        return value, warnings or None

    return warn_keys_alias_converter


convert_values_row = conv.pipe(
    conv.test_isinstance(dict),
    rename_keys(label_by_alias),
    conv.struct(
        collections.OrderedDict((
            (u"Age de départ (AAD=Age d'annulation de la décôte)", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.test(lambda value: aad_re.match(value) is not None, error = N_(u'Not a valid "AAD"')),
                )),
            (u"Date", convert_date_tree),
            (u"Date d'effet", convert_date_tree),
            (u"Date de perception du salaire", convert_date_tree),
            (u"Date ISF", convert_date_tree),
            (u"Références législatives", convert_line_tree),
            (u"Parution au JO", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.iso8601_input_to_date,
                conv.date_to_iso8601_str,
                )),
            (u"Références BOI", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Références législatives - définition des ressources et plafonds", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Références législatives - revalorisation des plafonds", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Références législatives des règles de calcul et du paramètre Po", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Références législatives de tous les autres paramètres", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Notes", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            (u"Notes bis", conv.pipe(
                conv.test_isinstance(basestring),
                conv.translate({u'nc': None}),
                conv.cleanup_line,
                )),
            )),
        default = convert_amount_or_number_tree,
        drop_none_values = True,
        keep_value_order = True,
        ),
    require_one_and_only_one_key(
        u"Age de départ (AAD=Age d'annulation de la décôte)",
        u"Date",
        u"Date d'effet",
        u"Date de perception du salaire",
        u"Date ISF",
        ),
    )


convert_sheet = conv.pipe(
    conv.test_isinstance(dict),
    conv.struct(
        collections.OrderedDict((
            (u'Noms TaxIPP', conv.pipe(
                conv.test_isinstance(dict),
                rename_keys(label_by_alias),
                convert_taxipp_name_tree,
                )),
            (u'Valeurs', conv.pipe(
                conv.test_isinstance(list),
                conv.uniform_sequence(convert_values_row),
                )),
            )),
        default = conv.noop,
        drop_none_values = True,
        keep_value_order = True,
        ),
    )


warn_values_row = conv.pipe(
    conv.test_isinstance(dict),
    warn_keys_alias(label_by_alias),
    )


warn_sheet = conv.pipe(
    conv.test_isinstance(dict),
    conv.struct(
        collections.OrderedDict((
            (u'Valeurs', conv.pipe(
                conv.test_isinstance(list),
                conv.uniform_sequence(warn_values_row),
                )),
            )),
        default = conv.noop,
        keep_value_order = True,
        ),
    )


# Functions


def encapsulate_yaml(value):
    if value is None:
        return value
    if isinstance(value, basestring):
        return literal_unicode(value) if u'\n' in value else value
    if isinstance(value, dict):
        return type(value)(
            (item_name, encapsulate_yaml(item_value))
            for item_name, item_value in value.iteritems()
            )
    if isinstance(value, list):
        return [
            encapsulate_yaml(item_value)
            for item_value in value
            ]
    return value


def clean(yaml_raw_dir, yaml_clean_dir):
    file_system_encoding = sys.getfilesystemencoding()

    error_by_directory_name = collections.OrderedDict()
    warning_by_directory_name = collections.OrderedDict()
    for source_dir_encoded, directories_name_encoded, filenames_encoded in os.walk(yaml_raw_dir):
        directories_name_encoded.sort()
        error_by_sheet_name = collections.OrderedDict()
        warning_by_sheet_name = collections.OrderedDict()
        for filename_encoded in sorted(filenames_encoded):
            if not filename_encoded.endswith('.yaml'):
                continue
            filename = filename_encoded.decode(file_system_encoding)
            sheet_name = os.path.splitext(filename)[0]
            source_file_path_encoded = os.path.join(source_dir_encoded, filename_encoded)
            relative_file_path_encoded = source_file_path_encoded[len(yaml_raw_dir):].lstrip(os.sep)
            relative_file_path = relative_file_path_encoded.decode(file_system_encoding)
            if sheet_name.isupper():
                # TODO.
                if sheet_name in (u'ERRORS', u'WARNINGS'):
                    continue
                with open(source_file_path_encoded) as source_file:
                    data = source_file.read()

                target_file_path_encoded = os.path.join(yaml_clean_dir, relative_file_path_encoded)
                target_dir_encoded = os.path.dirname(target_file_path_encoded)
                if not os.path.exists(target_dir_encoded):
                    os.makedirs(target_dir_encoded)
                with open(target_file_path_encoded, 'w') as target_file:
                    target_file.write(data)
            else:
                assert sheet_name.islower(), sheet_name
                log.info(u'Cleaning up file {}'.format(relative_file_path))
                with open(source_file_path_encoded) as source_file:
                    raw_data = yaml.load(source_file)

                data, error = convert_sheet(raw_data)
                if error is None:
                    _, warning = warn_sheet(raw_data)
                else:
                    log.warning('Error in file {}:\n{}'.format(
                        relative_file_path,
                        yaml.dump(error, allow_unicode = True, default_flow_style = False, indent = 2, width = 120),
                        ))
                    warning = None
                clean_data = encapsulate_yaml(data)
                if error:
                    if isinstance(error, basestring) and u'\n' in error:
                        error = literal_unicode(error)
                    data_errors = clean_data.get(u'ERRORS')
                    if data_errors is None:
                        clean_data[u'ERRORS'] = error
                    elif isinstance(data_errors, dict) and isinstance(error, dict):
                        for item_name, item_value in error.iteritems():
                            if item_name not in data_errors:
                                data_errors[item_name] = item_value
                    error_by_sheet_name[sheet_name] = error
                if warning:
                    if isinstance(warning, basestring) and u'\n' in warning:
                        warning = literal_unicode(warning)
                    if enable_warnings:
                        data_warnings = clean_data.get(u'WARNINGS')
                        if data_warnings is None:
                            clean_data[u'WARNINGS'] = warning
                        elif isinstance(data_warnings, dict) and isinstance(warning, dict):
                            for item_name, item_value in warning.iteritems():
                                if item_name not in data_warnings:
                                    data_warnings[item_name] = item_value
                    warning_by_sheet_name[sheet_name] = warning

                target_file_path_encoded = os.path.join(yaml_clean_dir, relative_file_path_encoded)
                target_dir_encoded = os.path.dirname(target_file_path_encoded)
                if not os.path.exists(target_dir_encoded):
                    os.makedirs(target_dir_encoded)
                with open(target_file_path_encoded, 'w') as target_file:
                    yaml.dump(clean_data, target_file, allow_unicode = True, default_flow_style = False, indent = 2,
                        width = 120)

        if error_by_sheet_name or warning_by_sheet_name:
            relative_dir_encoded = source_dir_encoded[len(yaml_raw_dir):].lstrip(os.sep)
            relative_dir_encoded_split = [
                directory_name_encoded
                for directory_name_encoded in os.path.split(relative_dir_encoded)
                if directory_name_encoded
                ]
            if error_by_sheet_name:
                error_by_child_directory_name = error_by_directory_name
                for directory_name in relative_dir_encoded_split[:-1]:
                    error_by_child_directory_name = error_by_child_directory_name.setdefault(
                        directory_name.decode(file_system_encoding), collections.OrderedDict())
                target_file_path_encoded = os.path.join(*([yaml_clean_dir] + relative_dir_encoded_split +
                    [u'ERRORS.yaml'.encode(file_system_encoding)]))
                with open(target_file_path_encoded, 'w') as target_file:
                    yaml.dump(error_by_sheet_name, target_file, allow_unicode = True, default_flow_style = False,
                        indent = 2, width = 120)
                error_by_child_directory_name[relative_dir_encoded_split[-1].decode(file_system_encoding)] = \
                    error_by_sheet_name
            if warning_by_sheet_name:
                warning_by_child_directory_name = warning_by_directory_name
                for directory_name in relative_dir_encoded_split[:-1]:
                    warning_by_child_directory_name = warning_by_child_directory_name.setdefault(
                        directory_name.decode(file_system_encoding), collections.OrderedDict())
                if enable_warnings:
                    target_file_path_encoded = os.path.join(*([yaml_clean_dir] + relative_dir_encoded_split +
                        [u'WARNINGS.yaml'.encode(file_system_encoding)]))
                    with open(target_file_path_encoded, 'w') as target_file:
                        yaml.dump(warning_by_sheet_name, target_file, allow_unicode = True, default_flow_style = False,
                            indent = 2, width = 120)
                warning_by_child_directory_name[relative_dir_encoded_split[-1].decode(file_system_encoding)] = \
                    warning_by_sheet_name

            target_file_path_encoded = os.path.join(yaml_clean_dir, relative_file_path_encoded)
            target_dir_encoded = os.path.dirname(target_file_path_encoded)

    if error_by_directory_name:
        target_file_path_encoded = os.path.join(
            yaml_clean_dir,
            u'ERRORS.yaml'.encode(file_system_encoding),
            )
        with open(target_file_path_encoded, 'w') as target_file:
            yaml.dump(error_by_directory_name, target_file, allow_unicode = True, default_flow_style = False,
                indent = 2, width = 120)
    if warning_by_directory_name:
        target_file_path_encoded = os.path.join(
            yaml_clean_dir,
            u'WARNINGS.yaml'.encode(file_system_encoding),
            )
        with open(target_file_path_encoded, 'w') as target_file:
            yaml.dump(warning_by_directory_name, target_file, allow_unicode = True, default_flow_style = False,
                indent = 2, width = 120)
