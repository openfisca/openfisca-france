#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract mapping from subcommunes (arrondissements and communes associées) depcom codes to
commune depcom code.
"""


import argparse
import csv
import json
import logging
import os
import sys


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('versement_transport_file', help = u"Versement transport by commune file")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = u"increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING)

    taux_by_commune_depcom = {}
    with open(args.versement_transport_file) as versement_transport_file:
        csv_reader = csv.DictReader(versement_transport_file, delimiter = ';')
        for row in csv_reader:
            # Do not decode row as we read only ASCII.
            print row
            # if row['ACTUAL'] in ('2', '5'):
                # subcommune_depcom = row['DEP'] + row['COM']
                # commune_depcom = row['POLE']
                # commune_depcom_by_subcommune_depcom[subcommune_depcom] = commune_depcom

#    print json.dumps(taux_by_commune_depcom, encoding = 'utf-8', ensure_ascii = False, indent = 2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
