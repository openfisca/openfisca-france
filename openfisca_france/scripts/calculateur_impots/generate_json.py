#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ########## DESCRIPTION ############
# Ce programme contient export_json, utilisé par d'autres scripts pour écrire un fichier .json contenant un scenario
# et le résultat de la simulation officielle (DGFiP) correspondant si le fichier n'existe pas déjà, et qui compare
# ensuite le résultat d'OpenFisca avec le résultat officiel


import codecs
import hashlib
import json
import os
import sys

from ..scripts.compare_openfisca_impots import compare
from . import base


def define_scenario(year = 2013):
    scenario = base.tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = year,
        parent1 = dict(
            activite = u'Actif occupé',
            date_naissance = 1970,
            salaire_imposable = 24000,
            statut_marital = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '2002-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '2000-04-17',
                ),
            ],
        foyer_fiscal = dict(
            f8ta = 3000,
            ),
        )
    scenario.suggest()
    return scenario


def add_official(scenario, fichier, tested = False):
    json_scenario = scenario.to_json()
    fields = compare(scenario, tested, fichier)
    return {'scenario': json_scenario, 'resultat_officiel': fields}


def export_json(scenario, var = "", tested = True):
    # On peut passer un scenario en entrée, ou un scenario assorti d'une
    # variable : dans ce cas le scenario est créé par create_json_then_test
    json_scenario = scenario.to_json()
    string_scenario = json.dumps(json_scenario, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
    h = var + '-' + hashlib.sha256(string_scenario).hexdigest()
    h2 = var + '-' + str(scenario.period.date.year) + '-' + hashlib.sha256(string_scenario).hexdigest()
    # Le fichier de sortie est nommé :
    # [variable éventuelle]-[année du scénario (sauf pour .json créés avant 05/14)]-[Hash du scenario]
    if not (os.path.isfile(os.path.join('json', h + '.json')) or os.path.isfile(os.path.join('json', h2 + '.json'))):
        # TODO: scenario > single entity
        with codecs.open(os.path.join('json', h2 + '.json'), 'w', encoding = 'utf-8') as fichier:
            json.dump(add_official(scenario, h2, tested), fichier, encoding = 'utf-8', ensure_ascii = False, indent = 2,
                sort_keys = True)
    elif os.path.isfile(os.path.join('json', h + '.json')):
        compare(scenario, tested, h)
    else:
        compare(scenario, tested, h2)


def main():
    scenario = define_scenario()
    export_json(scenario)


if __name__ == "__main__":
    sys.exit(main())
