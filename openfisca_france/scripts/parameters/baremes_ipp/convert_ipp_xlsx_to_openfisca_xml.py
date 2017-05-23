#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Convertit les barèmes de l'IPP au format XLSX vers le format XML des paramètres d'OpenFisca.

Nécessite l'installation de :
- ssconvert :
    - Debian : `apt install gnumeric`
    - macOS : `brew install gnumeric`
- xlrd : `pip install xlrd`
"""


import argparse
import glob
import logging
import os
import subprocess
import sys
import tempfile
import urllib
import zipfile

import xls_to_yaml_raw
import yaml_clean_to_xml
import yaml_raw_to_yaml_clean


app_name = os.path.splitext(os.path.basename(__file__))[0]
default_zip_url = u'https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-xlsx/repository/archive.zip?ref=master'  # noqa
log = logging.getLogger(app_name)


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--tmp-dir', default = None, help = u"Where to write intermediary files")
    parser.add_argument('--xml-dir', default = None, help = u"Where to write XML files")
    parser.add_argument('--zip-url', default = default_zip_url, help = u"URL of the ZIP file to download")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = u"Increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO)

    if args.xml_dir is not None and not os.path.exists(args.xml_dir):
        log.error(u'Directory {!r} does not exist.'.format(args.xml_dir))
        return 1

    if not cmd_exists('ssconvert'):
        log.error(u'Command "ssconvert" must be installed. It is provided by the "gnumeric" spreadsheet. '
            u'Under a Debian GNU/Linux distribution, type `sudo apt install gnumeric`. '
            u'Under macOS, type `brew install gnumeric`.')
        return 1

    tmp_dir = tempfile.mkdtemp(prefix='baremes-ipp-') \
        if args.tmp_dir is None \
        else args.tmp_dir
    log.info(u'Temporary directory is {!r}.'.format(tmp_dir))

    zip_file_path = os.path.join(tmp_dir, u"xlsx_files.zip")
    urllib.urlretrieve(args.zip_url, zip_file_path)
    log.info(u'ZIP file downloaded and saved as {!r}.'.format(zip_file_path))

    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(tmp_dir)
    # Find the name of the only directory in `xlsx_dir_path`, ending by the git commit ID in SHA-1 format.
    xlsx_dir_path = glob.glob(os.path.join(tmp_dir, 'ipp-tax-and-benefit-tables-xlsx-master*'))[0]
    log.info(u'ZIP file extracted to {!r}.'.format(xlsx_dir_path))

    log.info(u'Converting XLSX files to XLS...')
    xls_dir_path = os.path.join(tmp_dir, 'xls')
    os.mkdir(xls_dir_path)
    for xlsx_file_name in os.listdir(xlsx_dir_path):
        if not xlsx_file_name.endswith('.xlsx'):
            continue
        source_path = os.path.join(xlsx_dir_path, xlsx_file_name)
        target_path = os.path.join(xls_dir_path, '{}.xls'.format(os.path.splitext(xlsx_file_name)[0]))
        subprocess.check_call(['ssconvert', '--export-type=Gnumeric_Excel:excel_biff8', source_path, target_path])
    log.info(u'XLS files written to {!r}.'.format(xls_dir_path))

    log.info(u'Converting XLS files to YAML raw...')
    yaml_raw_dir_path = os.path.join(tmp_dir, 'yaml_raw')
    os.mkdir(yaml_raw_dir_path)
    xls_to_yaml_raw.transform(xls_dir_path, yaml_raw_dir_path)
    log.info(u'YAML raw files written to {!r}.'.format(yaml_raw_dir_path))

    log.info(u'Converting YAML raw files to YAML clean...')
    yaml_clean_dir_path = os.path.join(tmp_dir, 'yaml_clean')
    os.mkdir(yaml_clean_dir_path)
    yaml_raw_to_yaml_clean.clean(yaml_raw_dir_path, yaml_clean_dir_path)
    log.info(u'YAML clean files written to {!r}.'.format(yaml_clean_dir_path))

    log.info(u'Converting YAML clean files to XML...')
    if args.xml_dir is None:
        xml_dir_path = os.path.join(tmp_dir, 'xml')
        os.mkdir(xml_dir_path)
    else:
        xml_dir_path = args.xml_dir
    yaml_clean_to_xml.transform(yaml_clean_dir_path, xml_dir_path)
    log.info(u'XML files written to {!r}'.format(xml_dir_path))


if __name__ == "__main__":
    sys.exit(main())
