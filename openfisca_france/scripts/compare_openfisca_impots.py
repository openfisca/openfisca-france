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

#TODO: reduce margin error from 2 to 0 by coding the floor and round rules

"""Compare income taxes computed by finances.gouv.fr web simulator with OpenFisca results."""


import argparse
import collections
import json
import logging
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
            sali = 100000,
            statmarit = u'Célibataire',
            ),
        enfants = [
#            dict(
#                activite = u'Étudiant, élève',
#                birth = '2002-02-01',
#                ),
#            dict(
#                activite = u'Étudiant, élève',
#                birth = '2000-04-17',
#                ),
            ],
        foyer_fiscal = dict(
                f7up = 6250, #TODO: pb avec f2ck
            ),
        year = year,
        )
    scenario.suggest()
    return scenario
    

def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    year = 2013
    scenario = define_scenario(year)
    compare(scenario, tested = True)
    return 0


def compare(scenario, tested = False, fichier = ''):
    year = scenario.year
    totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')

    impots_arguments = transform_scenario_to_impots_arguments(scenario)
    simulation = scenario.new_simulation(debug = True)

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-'+str(year+1)+'.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))

    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()
    names = {   'CIGE': u'Crédit aides aux personnes',
                'IAVIM': u'Impôt avant imputations',
                'IDEC': u'Décote',
                'IDRS2': u'Droits simples',
                'IINET': u'Montant net à payer',
                'IINETIR': u'Impôt sur le revenu net',
                'IREST': u'Montant net à restituer',
                'ITRED': u'Total des réductions d\'impôt',
                'NAPCRP': u'Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d\'activité et de remplacement',
                'NBPT': u'Nombre de parts',
                'NBP': u'Nombre de parts',
                'PERPPLAFTV': u'Plafond de déduction pour les revenus 2014 au titre de l\'épargne retraite, pour déclarant 1',
                'PPETOT': u'Prime pour l\'emploi',
                'REVKIRE': u'Revenu fiscal de référence',
                'RNICOL': u'Revenu net imposable ou déficit à reporter',
                'RRBG': u'Revenu brut global ou déficit',
                'TOTPAC': u'Nombre de personnes à charge',
                'TXMARJ': u'Taux marginal d\'imposition',
                'TXMOYIMP': u'Taux moyen d\'imposition',
                'IRETS' : u'?',#TODO
                'IRESTIR': u'?',#TODO (f8tb)
                'CIRELANCE': u'Crédit d\'impôt exceptionnel sur les revenus 2008',
                'RNI': u'?',#TODO
                'CIRCM': u'?',#TODO (f2dc)
                'BCSG': u'?',#TODO (f2dc)
                'BRDS': u'?',#TODO (f2dc)
                'NAPCS': u'?',#TODO (f2dc)
                'NAPRD': u'?',#TODO (f2dc)
                'NAPPS': u'?',#TODO (f2dc)
                'CICA': u'?',#TODO (f4tq)
                'CIHABPRIN': u'?',#TODO (f7vy)
                'CIPRETUD': u'?',#TODO (f7uk)
                'I2DH': u'?',#TODO (f2dh)
                'BPRS': u'?',#TODO (f2ch)
                'CIDEVDUR': u'?',#TODO (f7wf)
                'CIADCRE': u'?',#TODO (f7dg)      
                'RFOR': u'?',#TODO (f7up)            
            }
    for element in page_doc.xpath('//input[@type="hidden"][@name]'): 
        code = element.get('name')
        fields[code] = {
            'code' : code,
            'name' : names[code] if (code in names) else u'nom inconnu',
            'value' : float(element.get('value').replace(" ","")),
            } 
    if tested:
        for code, field in fields.iteritems():
            compare_variable(code,field,simulation,totpac, year, fichier)
#            print u'{} : {} ({})'.format(code, fields[code]['value'], fields[code]['name']).encode('utf-8')
#    print simulation.calculate('irpp')
    return fields


def compare_variable(code,field,simulation,totpac, year, fichier = ''):
    for a in range(0,1):
            if code == 'IAVIM':
                openfisca_value = simulation.calculate('iai')
            elif code == 'IDEC':
                openfisca_value = simulation.calculate('decote')
            elif code == 'IDRS2':
                openfisca_value = simulation.calculate('ir_plaf_qf')
            elif code == 'IINETIR' or code == 'IINET':
                openfisca_value = simulation.calculate('irpp')
            elif code == 'ITRED':
                openfisca_value = simulation.calculate('reductions')
            elif code == 'NBPT' or code == 'NBP':
                openfisca_value = simulation.calculate('nbptr')
            elif code == 'PPETOT':
                openfisca_value = simulation.calculate('ppe')
            elif code == 'REVKIRE':
                openfisca_value = simulation.calculate('rfr')
            elif code == 'RNICOL':
                openfisca_value = simulation.calculate('rni')
            elif code == 'RRBG':
                openfisca_value = simulation.calculate('rbg')
            elif code == 'TOTPAC':
                openfisca_value = len(totpac or [])
            elif code in ('BCSG', 'BPRS', 'BRDS', 'CIADCRE', 'CICA', 'CIDEVDUR', 'CIGE', 'CIHABPRIN', 'CIPRETUD', 'CIRCM', 'CIRELANCE', 'I2DH', 'IREST', 'IRESTIR', 'IRETS', 'ITRED', 'NAPCR', 'NAPCRP', 'NAPCS', 'NAPPS', 'NAPRD', 'PERPPLAFTV', 'RFOR', 'RNI', 'TXMARJ', 'TXMOYIMP'):
                continue 
            else:
                print 'Code inconnu :', code
                continue
            openfisca_simple_value = openfisca_value
            if isinstance(openfisca_simple_value, np.ndarray):
                assert openfisca_simple_value.shape == (1,), u'For {} ({}). Expected: {}. Got: {}'.format(code,
                    field['name'], field['value'], openfisca_value).encode('utf-8')
                openfisca_simple_value = openfisca_simple_value[0]
            openfisca_simple_value = abs(openfisca_simple_value)
            if not abs(field['value'] - openfisca_simple_value) < 2:
                print u'In {}. ({})\nFor {} ({}). Expected: {}. Got: {}).'.format(fichier, year, code, field['name'], field['value'], openfisca_simple_value).encode('utf-8')


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

   # print json.dumps(impots_arguments, encoding = 'utf-8', ensure_ascii = False, indent = 2)

    return impots_arguments


if __name__ == "__main__":
    sys.exit(main())
