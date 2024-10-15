''' xml_to_yaml_france.py : Parse XML parameter files for Openfisca-France and convert them to YAML files. Comments are NOT transformed.

Usage :
  `python xml_to_yaml_france.py output_dir`
or just (output is written in a directory called `yaml_parameters`):
  `python xml_to_yaml_france.py`
'''

import sys
import os

from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR
from openfisca_core.scripts.migrations.v16_2_to_v17 import xml_to_yaml


if len(sys.argv) > 1:
    target_path = sys.argv[1]
else:
    target_path = 'yaml_parameters'

param_dir = os.path.join(COUNTRY_DIR, 'parameters')
param_files = [
    'bouclier_fiscal.xml',
    'bourses_education.xml',
    'cmu.xml',
    'cotsoc.xml',
    'fonc.xml',
    'impot_revenu.xml',
    'prelevements_sociaux.xml',
    'prestations_sociales.xml',
    'taxation_capital.xml',
    'tns.xml',
    ]
legislation_xml_info_list = [
    (os.path.join(param_dir, param_file), [])
    for param_file in param_files
    ]

xml_to_yaml.write_parameters(legislation_xml_info_list, target_path)
