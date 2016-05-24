import argparse
import logging
import os
import pandas as pd
import pkg_resources
import sys

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


asset_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france').location,
    'openfisca_france',
    'assets',
    'grilles_fonction_publique'
    )


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    # parser.add_argument('--output-dir', default = asset_path, help = u'Where to write the CSV file')
    parser.add_argument('-s', '--source-file', help = 'path of source XLS file', required = True)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = u'Increase output verbosity')
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    xls_path = args.source_file
    read_and_save(xls_path)


def read_and_save(xls_path):
    csv_path = os.path.join(asset_path, 'territoriale_et_hospitaliere.csv') 
    os.listdir(asset_path)
    df = pd.read_excel(xls_path)
    df['categorie_salarie'] = 0
    df.to_csv(csv_path, encoding='utf-8', index = False)


if __name__ == '__main__':
    sys.exit(main())
