# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


"""Tools to use income taxes calculator from finances.gouv.fr web site."""


import urllib
import urllib2


def call_tax_calculator(year, inputs):
    url = 'http://www3.finances.gouv.fr/cgi-bin/calc-{}.cgi'.format(year)
    request = urllib2.Request(url, headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request, urllib.urlencode(inputs))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    return response_html


def transform_scenario_to_tax_calculator_inputs(scenario):
    tax_benefit_system = scenario.tax_benefit_system
    test_case = scenario.test_case
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        }
    individu_by_id = {
        individu['id']: individu
        for individu in test_case['individus']
        }
    for foyer_fiscal in test_case['foyers_fiscaux']:
        foyer_fiscal = foyer_fiscal.copy()

        for declarant_index, declarant_id in enumerate(foyer_fiscal.pop('declarants')):
            declarant = individu_by_id[declarant_id].copy()

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
                or impots_arguments['pre_situation_famille'] == pre_situation_famille, str((impots_arguments,
                    pre_situation_famille))
            impots_arguments['pre_situation_famille'] = pre_situation_famille

            for column_code, value in declarant.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[declarant_index]] = str(value)

        impots_arguments['0CF'] = len(foyer_fiscal['personnes_a_charge'])
        for personne_a_charge_index, personne_a_charge_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
            personne_a_charge = individu_by_id[personne_a_charge_id].copy()

            birth = personne_a_charge.pop('birth')
            impots_arguments['0F{}'.format(personne_a_charge_index)] = str(birth.year)

            personne_a_charge.pop('statmarit', None)

            for column_code, value in personne_a_charge.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.column_by_name[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[personne_a_charge_index]] = str(value)

        if foyer_fiscal.pop('caseT', False):
            impots_arguments['0BT'] = '1'

        for column_code, value in foyer_fiscal.iteritems():
            if column_code == 'id':
                continue
            if column_code == 'f7uf':
                impots_arguments['7UG'] = str(value)  # bug dans le site des impots
            if column_code == 'f7ud':
                impots_arguments['7UE'] = str(value)  # bug dans le site des impots
            if column_code == 'f7vc':
                impots_arguments['7VD'] = str(value)  # bug dans le site des impots
            column = tax_benefit_system.column_by_name[column_code]
            cerfa_field = column.cerfa_field
            assert cerfa_field is not None and isinstance(cerfa_field, basestring), column_code
            impots_arguments[cerfa_field] = int(value) if isinstance(value, bool) else str(value)

    return impots_arguments
