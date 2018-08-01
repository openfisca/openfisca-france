# -*- coding: utf-8 -*-

from __future__ import unicode_literals


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

aad_re = re.compile(r"AAD(\s+[-+]\s+\d+\s+ans?)?$")
ans_et_mois_re = re.compile(r"\d+ ans( \d+ mois)?$")
app_name = "cleanup_yaml"
apres_le_re = re.compile(
    r"après le (?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])/(?P<year>[12]\d{3})$"
)
conv = custom_conv(baseconv, datetimeconv, states)
french_date_re = re.compile(
    r"(?P<day>0?[1-9]|[12]\d|3[01])/(?P<month>0?[1-9]|1[0-2])/(?P<year>[12]\d{3})$"
)
label_by_alias = {
    "Commentaires": "Notes",
    "Date d'entrée en vigueur": "Date d'effet",
    "JORF": "Parution au JO",
    "Note": "Notes",
    "Parution au JORF": "Parution au JO",
    "Publication au JO": "Parution au JO",
    "Publication au JORF": "Parution au JO",
    "Publication JO": "Parution au JO",
    "Référence": "Références législatives",
    "Référence legislative": "Références législatives",
    "Référence législative": "Références législatives",
    "Référence législative - revalorisation des plafonds": "Références législatives - revalorisation des plafonds",
    "Référence législative de tous les autres paramètres": "Références législatives de tous les autres paramètres",
    "Référence BOI": "Références BOI",
    "Références": "Références législatives",
    "Références AGIRC": "Références législatives",
    "Références législatives (3)": "Références législatives",
    "Références législatives (taux d'appel)": "Références législatives",
    "Références législatives (taux de cotisation)": "Références législatives",
    "Références législatives ou BOI": "Références législatives",
    "Remarques": "Notes",
}
limite_age_re = re.compile(r"limite d'âge( - \d+ trimestres?)?$")
log = logging.getLogger(app_name)
trimestres_re = re.compile(r"\d+ trimestres?$")
year_re = re.compile(r"[12]\d{3}$")


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
    return dumper.represent_dict(data.items())


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

yaml.add_representer(
    folded_unicode,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str", data, style=">"
    ),
)
yaml.add_representer(
    literal_unicode,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str", data, style="|"
    ),
)
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_representer(
    unicode, lambda dumper, data: dumper.represent_scalar("tag:yaml.org,2002:str", data)
)


# Converters


def input_to_french_date(value, state=None):
    if value is None:
        return None, None
    if state is None:
        state = conv.default_state
    match = french_date_re.match(value)
    if match is None:
        return value, state._("Invalid french date")
    return (
        datetime.date(
            int(match.group("year")), int(match.group("month")), int(match.group("day"))
        ),
        None,
    )


def convert_amount_or_number_tree(value, state=None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_amount_or_number_tree,
                drop_none_values=True,
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
                        conv.test_in(
                            [
                                "-",  # TODO: Remove. Only "nc" is valid.
                                "gmr 2",
                                "na",  # TODO: Remove. Only "nc" is valid.
                                "nc",
                                "pas d'âge minimum",
                                "pas de limite",
                                "smic",
                            ]
                        ),
                        conv.test(
                            lambda value: value.startswith(
                                ("disparition", "même", "plafond")
                            )
                        ),
                        conv.test(
                            lambda value: ans_et_mois_re.match(value) is not None
                        ),
                        conv.test(lambda value: apres_le_re.match(value) is not None),
                        conv.test(lambda value: limite_age_re.match(value) is not None),
                        conv.test(lambda value: trimestres_re.match(value) is not None),
                    ),
                )
            ),
            conv.pipe(
                conv.test_isinstance(basestring),
                conv.function(lambda value: value.rstrip("*")),
                conv.function(lambda value: value.rsplit(None, 1)),
                conv.test(
                    lambda couple: len(couple) == 2,
                    error=N_("Invalid (amount, unit) couple"),
                ),
                conv.struct(
                    (
                        conv.pipe(
                            # Remove spaces and replace french decimal comma with a french dot.
                            conv.function(
                                lambda value: value.replace("\xa0", "")
                                .replace(" ", "")
                                .replace(",", ".")
                            ),
                            conv.input_to_float,
                            conv.not_none,
                        ),
                        conv.pipe(
                            conv.function(lambda value: value.upper()),
                            conv.translate({"F": "FRF", "€": "EUR"}),
                            conv.test_in(
                                [
                                    "%",
                                    "AF",  # anciens francs
                                    "CFA",  # francs CFA
                                    "COTISATIONS",
                                    "EUR",
                                    "FRF",
                                ]
                            ),
                        ),
                    )
                ),
                conv.function(lambda couple: " ".join([unicode(couple[0]), couple[1]])),
            ),
            conv.fail(
                error=N_("Value is neither a number nor an amount (with a unit)")
            ),
        ),
    )(value, state=state or conv.default_state)


def convert_date_tree(value, state=None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_date_tree,
                drop_none_values=True,
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
                conv.translate({"nc": None}),
                conv.first_match(
                    conv.pipe(
                        conv.test(
                            lambda date: year_re.match(date),
                            error=N_("Not a valid year"),
                        ),
                        conv.function(lambda year: datetime.date(year, 1, 1)),
                    ),
                    input_to_french_date,
                    conv.iso8601_input_to_date,
                ),
                conv.test(
                    lambda date: 1914 <= date.year <= 2030,
                    error=N_("Date with invalid year"),
                ),
            ),
        ),
    )(value, state=state or conv.default_state)


def convert_line_tree(value, state=None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring),
                convert_line_tree,
                drop_none_values=True,
            ),
            conv.empty_to_none,
        ),
        conv.condition(
            conv.test_isinstance(basestring),
            conv.pipe(conv.translate({"nc": None}), conv.cleanup_line),
        ),
    )(value, state=state or conv.default_state)


def convert_taxipp_name_tree(value, state=None):
    return conv.condition(
        conv.test_isinstance(dict),
        conv.pipe(
            conv.uniform_mapping(
                conv.test_isinstance(basestring), convert_taxipp_name_tree
            ),
            conv.empty_to_none,
        ),
        conv.pipe(
            conv.test_isinstance(basestring),
            conv.translate({"nc": None}),
            conv.test(
                lambda taxipp_name: strings.slugify(taxipp_name, separator="_")
                == taxipp_name.strip("_"),
                error=N_("Invalid TaxIPP name"),
            ),
        ),
    )(value, state=state or conv.default_state)


def rename_keys(new_key_by_old_key):
    def rename_keys_converter(value, state=None):
        if value is None:
            return value, None
        renamed_value = value.__class__()
        for item_key, item_value in value.items():
            new_key = new_key_by_old_key.get(item_key)
            if new_key is None:
                new_key = item_key
            else:
                assert (
                    new_key not in value
                ), 'Renaming of key "{}" by "{}" failed, because new key is already used'.format(
                    item_key, new_key
                ).encode(
                    "utf-8"
                )
            renamed_value[new_key] = item_value
        return renamed_value, None

    return rename_keys_converter


def require_one_and_only_one_key(*keys):
    def require_one_and_only_one_key_converter(value, state=None):
        if value is None:
            return value, None
        if state is None:
            state = conv.default_state
        present_keys = set(item_key for item_key in value if item_key in keys)
        if not present_keys:
            message = state._("One of the following fields is required: {}").format(
                ", ".join(keys)
            )
            return value, {key: message for key in keys}
        if len(present_keys) == 1:
            return value, None
        message = state._(
            "Only one of the following fields must be present: {}"
        ).format(", ".join(sorted(present_keys)))
        return value, {key: message for key in present_keys}

    return require_one_and_only_one_key_converter


def warn_keys_alias(new_key_by_old_key):
    def warn_keys_alias_converter(value, state=None):
        if value is None:
            return value, None
        warnings = collections.OrderedDict()
        for item_key, item_value in value.items():
            label = new_key_by_old_key.get(item_key)
            if label is not None:
                warnings[item_key] = 'Label "{}" should be renamed to "{}"'.format(
                    item_key, label
                )
        return value, warnings or None

    return warn_keys_alias_converter


convert_values_row = conv.pipe(
    conv.test_isinstance(dict),
    rename_keys(label_by_alias),
    conv.struct(
        collections.OrderedDict(
            (
                (
                    "Age de départ (AAD=Age d'annulation de la décôte)",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.test(
                            lambda value: aad_re.match(value) is not None,
                            error=N_('Not a valid "AAD"'),
                        ),
                    ),
                ),
                ("Date", convert_date_tree),
                ("Date d'effet", convert_date_tree),
                ("Date de perception du salaire", convert_date_tree),
                ("Date ISF", convert_date_tree),
                ("Références législatives", convert_line_tree),
                (
                    "Parution au JO",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.iso8601_input_to_date,
                        conv.date_to_iso8601_str,
                    ),
                ),
                (
                    "Références BOI",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Références législatives - définition des ressources et plafonds",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Références législatives - revalorisation des plafonds",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Références législatives des règles de calcul et du paramètre Po",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Références législatives de tous les autres paramètres",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Notes",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
                (
                    "Notes bis",
                    conv.pipe(
                        conv.test_isinstance(basestring),
                        conv.translate({"nc": None}),
                        conv.cleanup_line,
                    ),
                ),
            )
        ),
        default=convert_amount_or_number_tree,
        drop_none_values=True,
        keep_value_order=True,
    ),
    require_one_and_only_one_key(
        "Age de départ (AAD=Age d'annulation de la décôte)",
        "Date",
        "Date d'effet",
        "Date de perception du salaire",
        "Date ISF",
    ),
)


convert_sheet = conv.pipe(
    conv.test_isinstance(dict),
    conv.struct(
        collections.OrderedDict(
            (
                (
                    "Noms TaxIPP",
                    conv.pipe(
                        conv.test_isinstance(dict),
                        rename_keys(label_by_alias),
                        convert_taxipp_name_tree,
                    ),
                ),
                (
                    "Valeurs",
                    conv.pipe(
                        conv.test_isinstance(list),
                        conv.uniform_sequence(convert_values_row),
                    ),
                ),
            )
        ),
        default=conv.noop,
        drop_none_values=True,
        keep_value_order=True,
    ),
)


warn_values_row = conv.pipe(conv.test_isinstance(dict), warn_keys_alias(label_by_alias))


warn_sheet = conv.pipe(
    conv.test_isinstance(dict),
    conv.struct(
        collections.OrderedDict(
            (
                (
                    "Valeurs",
                    conv.pipe(
                        conv.test_isinstance(list),
                        conv.uniform_sequence(warn_values_row),
                    ),
                ),
            )
        ),
        default=conv.noop,
        keep_value_order=True,
    ),
)


# Functions


def encapsulate_yaml(value):
    if value is None:
        return value
    if isinstance(value, basestring):
        return literal_unicode(value) if "\n" in value else value
    if isinstance(value, dict):
        return type(value)(
            (item_name, encapsulate_yaml(item_value))
            for item_name, item_value in value.items()
        )
    if isinstance(value, list):
        return [encapsulate_yaml(item_value) for item_value in value]
    return value


def clean(yaml_raw_dir, yaml_clean_dir):
    file_system_encoding = sys.getfilesystemencoding()

    error_by_directory_name = collections.OrderedDict()
    warning_by_directory_name = collections.OrderedDict()
    for source_dir_encoded, directories_name_encoded, filenames_encoded in os.walk(
        yaml_raw_dir
    ):
        directories_name_encoded.sort()
        error_by_sheet_name = collections.OrderedDict()
        warning_by_sheet_name = collections.OrderedDict()
        for filename_encoded in sorted(filenames_encoded):
            if not filename_encoded.endswith(".yaml"):
                continue
            filename = filename_encoded.decode(file_system_encoding)
            sheet_name = os.path.splitext(filename)[0]
            source_file_path_encoded = os.path.join(
                source_dir_encoded, filename_encoded
            )
            relative_file_path_encoded = source_file_path_encoded[
                len(yaml_raw_dir) :
            ].lstrip(os.sep)
            relative_file_path = relative_file_path_encoded.decode(file_system_encoding)
            if sheet_name.isupper():
                # TODO.
                if sheet_name in ("ERRORS", "WARNINGS"):
                    continue
                with open(source_file_path_encoded) as source_file:
                    data = source_file.read()

                target_file_path_encoded = os.path.join(
                    yaml_clean_dir, relative_file_path_encoded
                )
                target_dir_encoded = os.path.dirname(target_file_path_encoded)
                if not os.path.exists(target_dir_encoded):
                    os.makedirs(target_dir_encoded)
                with open(target_file_path_encoded, "w") as target_file:
                    target_file.write(data)
            else:
                assert sheet_name.islower(), sheet_name
                log.info("Cleaning up file {}".format(relative_file_path))
                with open(source_file_path_encoded) as source_file:
                    raw_data = yaml.load(source_file)

                data, error = convert_sheet(raw_data)
                if error is None:
                    _, warning = warn_sheet(raw_data)
                else:
                    log.warning(
                        "Error in file {}:\n{}".format(
                            relative_file_path,
                            yaml.dump(
                                error,
                                allow_unicode=True,
                                default_flow_style=False,
                                indent=2,
                                width=120,
                            ),
                        )
                    )
                    warning = None
                clean_data = encapsulate_yaml(data)
                if error:
                    if isinstance(error, basestring) and "\n" in error:
                        error = literal_unicode(error)
                    data_errors = clean_data.get("ERRORS")
                    if data_errors is None:
                        clean_data["ERRORS"] = error
                    elif isinstance(data_errors, dict) and isinstance(error, dict):
                        for item_name, item_value in error.items():
                            if item_name not in data_errors:
                                data_errors[item_name] = item_value
                    error_by_sheet_name[sheet_name] = error
                if warning:
                    if isinstance(warning, basestring) and "\n" in warning:
                        warning = literal_unicode(warning)
                    if enable_warnings:
                        data_warnings = clean_data.get("WARNINGS")
                        if data_warnings is None:
                            clean_data["WARNINGS"] = warning
                        elif isinstance(data_warnings, dict) and isinstance(
                            warning, dict
                        ):
                            for item_name, item_value in warning.items():
                                if item_name not in data_warnings:
                                    data_warnings[item_name] = item_value
                    warning_by_sheet_name[sheet_name] = warning

                target_file_path_encoded = os.path.join(
                    yaml_clean_dir, relative_file_path_encoded
                )
                target_dir_encoded = os.path.dirname(target_file_path_encoded)
                if not os.path.exists(target_dir_encoded):
                    os.makedirs(target_dir_encoded)
                with open(target_file_path_encoded, "w") as target_file:
                    yaml.dump(
                        clean_data,
                        target_file,
                        allow_unicode=True,
                        default_flow_style=False,
                        indent=2,
                        width=120,
                    )

        if error_by_sheet_name or warning_by_sheet_name:
            relative_dir_encoded = source_dir_encoded[len(yaml_raw_dir) :].lstrip(
                os.sep
            )
            relative_dir_encoded_split = [
                directory_name_encoded
                for directory_name_encoded in os.path.split(relative_dir_encoded)
                if directory_name_encoded
            ]
            if error_by_sheet_name:
                error_by_child_directory_name = error_by_directory_name
                for directory_name in relative_dir_encoded_split[:-1]:
                    error_by_child_directory_name = error_by_child_directory_name.setdefault(
                        directory_name.decode(file_system_encoding),
                        collections.OrderedDict(),
                    )
                target_file_path_encoded = os.path.join(
                    *(
                        [yaml_clean_dir]
                        + relative_dir_encoded_split
                        + ["ERRORS.yaml".encode(file_system_encoding)]
                    )
                )
                with open(target_file_path_encoded, "w") as target_file:
                    yaml.dump(
                        error_by_sheet_name,
                        target_file,
                        allow_unicode=True,
                        default_flow_style=False,
                        indent=2,
                        width=120,
                    )
                error_by_child_directory_name[
                    relative_dir_encoded_split[-1].decode(file_system_encoding)
                ] = error_by_sheet_name
            if warning_by_sheet_name:
                warning_by_child_directory_name = warning_by_directory_name
                for directory_name in relative_dir_encoded_split[:-1]:
                    warning_by_child_directory_name = warning_by_child_directory_name.setdefault(
                        directory_name.decode(file_system_encoding),
                        collections.OrderedDict(),
                    )
                if enable_warnings:
                    target_file_path_encoded = os.path.join(
                        *(
                            [yaml_clean_dir]
                            + relative_dir_encoded_split
                            + ["WARNINGS.yaml".encode(file_system_encoding)]
                        )
                    )
                    with open(target_file_path_encoded, "w") as target_file:
                        yaml.dump(
                            warning_by_sheet_name,
                            target_file,
                            allow_unicode=True,
                            default_flow_style=False,
                            indent=2,
                            width=120,
                        )
                warning_by_child_directory_name[
                    relative_dir_encoded_split[-1].decode(file_system_encoding)
                ] = warning_by_sheet_name

            target_file_path_encoded = os.path.join(
                yaml_clean_dir, relative_file_path_encoded
            )
            target_dir_encoded = os.path.dirname(target_file_path_encoded)

    if error_by_directory_name:
        target_file_path_encoded = os.path.join(
            yaml_clean_dir, "ERRORS.yaml".encode(file_system_encoding)
        )
        with open(target_file_path_encoded, "w") as target_file:
            yaml.dump(
                error_by_directory_name,
                target_file,
                allow_unicode=True,
                default_flow_style=False,
                indent=2,
                width=120,
            )
    if warning_by_directory_name:
        target_file_path_encoded = os.path.join(
            yaml_clean_dir, "WARNINGS.yaml".encode(file_system_encoding)
        )
        with open(target_file_path_encoded, "w") as target_file:
            yaml.dump(
                warning_by_directory_name,
                target_file,
                allow_unicode=True,
                default_flow_style=False,
                indent=2,
                width=120,
            )
