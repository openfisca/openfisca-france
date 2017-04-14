# -*- coding: utf-8 -*-

from __future__ import division

import json
import os

from openfisca_core import decompositions
from cache import tax_benefit_system

decompositions_directory = os.path.dirname(tax_benefit_system.decomposition_file_path)


def test_decomposition(print_decomposition = False):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            code_postal_entreprise = "75001",
            ratio_alternants = .025,
            salaire_de_base = {"2013": 12 * 3000},
            taille_entreprise = 3,
            categorie_salarie = 0,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation()

    xml_file_path = os.path.join(
        decompositions_directory,
        "fiche_de_paie_decomposition.xml"
        )

    decomposition_json = decompositions.get_decomposition_json(
        tax_benefit_system, xml_file_path = xml_file_path)
    simulations = [simulation]
    response = decompositions.calculate(simulations, decomposition_json)
    if print_decomposition:
        print unicode(
            json.dumps(response, encoding = 'utf-8', ensure_ascii = False, indent = 2)
            )


if __name__ == '__main__':
    import argparse
    import logging
    import sys

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

#    test_decomposition(print_decomposition = True)
