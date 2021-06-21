#! /usr/bin/python3
"""
Ce script sert à placer dans l'ordre chronologique les clef de certain paramètres
tel que 'values', 'reference', 'official_journal_date' et 'notes'.
Ceci afin de passer de l'ordre anté-chronologique utilisé par l'IPP à l'ordre
chronologique d'OpenFisca.
Python3.7 or above mandatory !!!
"""
import yaml
import collections
import shutil
import platform
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


def order_key(key_dict, key):
    if key_dict[key] is None:
        return None
    logging.debug(f"Changing {key}...")
    # We build an ordered dict with the sorted items to keep them sorted
    od = collections.OrderedDict(sorted(key_dict[key].items()))
    # We return a dict, that keep order since Python 3.7
    return dict(od)


def check(file):
    if int(platform.python_version_tuple()[0]) < 3 and int(platform.python_version_tuple()[1]) < 7:
        logging.error('We need Python 3.7 or above !')
        sys.exit(2)
    logging.info(f"Reading {file}")
    with open(file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
    # Iterate the keys to find the ones we whant to sort
    for key in config.keys():
        if key == 'values':
            config[key] = order_key(config, key)
        elif key == 'metadata':
            for key2 in config[key].keys():
                if key2 in ('reference', 'official_journal_date', 'notes'):
                    config[key][key2] = order_key(config[key], key2)
    # Make a backup
    shutil.move(file, file + '-backup')

    # Replace the original file
    # sort_keys=False to avoid sorting all keys, even the root keys.
    with open(file, 'w') as out:
        out.write(yaml.dump(config, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error(f'ERROR Wrong argument !\nUsage : {sys.argv[0]} <yaml filename>')
        exit(1)
    check(sys.argv[1])
