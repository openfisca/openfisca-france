#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Formate les fichiers de paramètre XML avec lxml.

Les fichiers, une fois formatés, peuvent être mergés avec les barêmes IPP avec un diff propre.

"""


import os
import sys

from lxml import etree
from openfisca_core import legislationsxml

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem, COUNTRY_DIR


parameters_dir_path = os.path.join(COUNTRY_DIR, 'parameters')


def main():
    xmlschema = legislationsxml.load_xml_schema()
    france_tax_benefit_system = FranceTaxBenefitSystem()

    for file_path, _ in france_tax_benefit_system.legislation_xml_info_list:
        with open(file_path, 'r') as f:
            tree = etree.parse(f)

        if not xmlschema.validate(tree):
            raise ValueError(xmlschema.error_log.filter_from_errors())

        root_element = tree.getroot()
        output_tree = etree.ElementTree(root_element)

        output_tree.write(file_path, encoding='utf-8', pretty_print=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
