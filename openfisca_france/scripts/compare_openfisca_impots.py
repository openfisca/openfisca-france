#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Compare income taxes computed by finances.gouv.fr web simulator with OpenFisca results."""


import argparse
import collections
import copy
import datetime
import logging
import math
import os
import sys
import urllib
import urllib2

from lxml import etree
import numpy as np
import openfisca_france


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()

def define_scenario(year):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        parent1 = dict(
            activite = u'Actif occupé',
            birth = 1970,
            cadre = True,
            sali = 24000,
            statmarit = u'Célibataire',
#            rsti=1000,
#            fra=1000,
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                birth = '2002-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                birth = '2000-04-17',
#                ppe_tp_sa=1,
                ),
            ],
        foyer_fiscal = dict(
#                f7is = 1000,
#                nbN = 5,
#                caseT = 0,
#                caseF = 5,
#                f2dc=5000,
#                f2ca=2000,
#                f3vg=1000,
#                f4ba=500,
#                f6gu=800,
#                f7uh=2000,
#                f7wj=300,
            ),
        year = year,
        )
    scenario.suggest()
    return scenario
    

def main():
    year = 2013

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    scenario = define_scenario(year)
    foyer_fiscal = copy.deepcopy(scenario.test_case['foyers_fiscaux'].values()[0])
    impots_arguments = transform_scenario_to_impots_arguments(scenario)
    simulation = scenario.new_simulation(debug = True)

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-'+str(year+1)+'.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))

    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()
    for element in page_doc.xpath('//input[@type="hidden"][@name]'):
        tag = element.tag.lower()
        parent = element.getparent()
        parent_tag = parent.tag.lower()
        if parent_tag == 'table':
            tr = parent[parent.index(element) - 1]
            assert tr.tag.lower() == 'tr', tr
        else:
            assert parent_tag == 'tr'
            tr = parent
        while True:
            name = etree.tostring(tr[1], encoding = unicode, method = 'text').strip().rstrip(u'*').rstrip()
            if name:
                break
            table = tr.getparent()
            tr = table[table.index(tr) - 1]
        code = element.get('name')
        fields[code] = dict(
            code = code,
            name = name,
            value = float(element.get('value').strip()),
            )
    import json
    for code, field in fields.iteritems():
        if code == 'IAVIM':
            # Impôt avant imputations
            openfisca_value = simulation.calculate('iai')
        elif code == 'IDEC':
            # Décote
            openfisca_value = simulation.calculate('decote')
        elif code == 'IDRS2':
            # Droits simples
            openfisca_value = simulation.calculate('ir_plaf_qf')
        elif code == 'IINET':
            # Montant net à payer
            continue
        elif code == 'IINETIR':
            # Impôt sur le revenu net
            openfisca_value = simulation.calculate('irpp')
        elif code == 'IREST':
            # Montant net à restituer
            continue
        elif code == 'ITRED':
            # Total des réductions d'impôt
            openfisca_value = simulation.calculate('reductions')
            continue
        elif code == 'NAPCRP':
            # Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d'activité et de remplacement
            # de source étrangère)
            # TODO
            continue
        elif code == 'NBPT':
            # Nombre de parts
            openfisca_value = simulation.calculate('nbptr')
        elif code == 'PERPPLAFTV':
            # Plafond de déduction pour les revenus 2014 au titre de l'épargne retraite, pour déclarant 1
            # TODO
            continue
        elif code == 'PPETOT':
            # Prime pour l'emploi
            openfisca_value = simulation.calculate('ppe')
        elif code == 'REVKIRE':
            # Revenu fiscal de référence
            openfisca_value = simulation.calculate('rfr')
        elif code == 'RNICOL':
            # Revenu net imposable ou déficit à reporter
            openfisca_value = simulation.calculate('rni')
        elif code == 'RRBG':
            # Revenu brut global ou déficit
            openfisca_value = simulation.calculate('rbg')
        elif code == 'TOTPAC':
            # Nombre de personnes à charge
            openfisca_value = len(foyer_fiscal.get('personnes_a_charge') or [])
        elif code == 'TXMARJ':
            # Taux marginal d'imposition (revenus soumis au barème)
            # TODO
            continue
        elif code == 'TXMOYIMP':
            # Taux moyen d'imposition
            # TODO
            continue
        else:
            raise KeyError(u'Unexpected code {} = {} ({})'.format(code, field['value'], field['name']).encode('utf-8'))
        openfisca_simple_value = openfisca_value
        if isinstance(openfisca_simple_value, np.ndarray):
            assert openfisca_simple_value.shape == (1,), u'For {} ({}). Expected: {}. Got: {}'.format(code,
                field['name'], field['value'], openfisca_value).encode('utf-8')
            openfisca_simple_value = openfisca_simple_value[0]
        openfisca_simple_value = abs(openfisca_simple_value)
        assert abs(field['value'] - openfisca_simple_value) <= 1, \
            u'For {} ({}). Expected: {}. Got: {} ({}). Fields: {}'.format(code, field['name'], field['value'],
                openfisca_simple_value, openfisca_value, json.dumps(fields, encoding = 'utf-8', ensure_ascii = False, indent = 2)).encode('utf-8')

    return 0


def transform_scenario_to_impots_arguments(scenario):
    test_case = scenario.test_case
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        }
    individus = test_case['individus']
    for foyer_fiscal in test_case['foyers_fiscaux'].itervalues():
        foyer_fiscal = foyer_fiscal.copy()

        for declarant_index, declarant_id in enumerate(foyer_fiscal.pop('declarants')):
            declarant = individus[declarant_id].copy()

            birth = declarant.pop('birth')
            impots_arguments['0D{}'.format(chr(ord('A') + declarant_index))] = str(birth.year)

            statmarit = declarant.pop('statmarit', None)
            column = tax_benefit_system.column_by_name['statmarit']
            if statmarit is None:
                statmarit = column.enum._vars[column.default]
            pre_situation_famille = {
                u"Marié": 'M',
                u"Célibataire": 'C',
                u"Divorcé": 'D',
                u"Veuf": 'V',
                u"Pacsé": 'O',
                # u"Jeune veuf": TODO
                }[statmarit if isinstance(statmarit, basestring) else column.enum._vars[statmarit]]
            assert 'pre_situation_famille' not in impots_arguments \
                or impots_arguments['pre_situation_famille'] == pre_situation_famille
            impots_arguments['pre_situation_famille'] = pre_situation_famille

            for column_code, value in declarant.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[declarant_index]] = str(value)

        impots_arguments['0CF'] = len(foyer_fiscal['personnes_a_charge'])
        for personne_a_charge_index, personne_a_charge_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
            personne_a_charge = individus[personne_a_charge_id].copy()

            birth = personne_a_charge.pop('birth')
            impots_arguments['0F{}'.format(personne_a_charge_index)] = str(birth.year) 

            personne_a_charge.pop('statmarit', None)

            for column_code, value in personne_a_charge.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[personne_a_charge_index]] = str(value)

        if foyer_fiscal.pop('caseT', False):
            impots_arguments['0BT'] = '1'

        for column_code, value in foyer_fiscal.iteritems():
            if column_code in (
                    ):
                continue
            column = tax_benefit_system.column_by_name[column_code]
            cerfa_field = column.cerfa_field
            assert cerfa_field is not None and isinstance(cerfa_field, basestring), column_code
            impots_arguments[cerfa_field] = str(value)
    import json
    print json.dumps(impots_arguments, encoding = 'utf-8', ensure_ascii = False, indent = 2)

    return impots_arguments


if __name__ == "__main__":
    sys.exit(main())
