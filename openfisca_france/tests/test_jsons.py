#! /usr/bin/env python
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


"""Teste tous les fichiers .json créés par un script"""


import datetime
import json
import logging
import os
import sys

from biryani.baseconv import check
from nose.tools import assert_equal

from .base import assert_near, tax_benefit_system


json_dir_path = os.path.join(os.path.dirname(__file__), 'json')
log = logging.getLogger(__name__)


def check_variable(args):
    scenario = args['scenario']
    simulation = scenario.new_simulation(debug = True)
    code = args['code']
    openfisca_value = None
    if code == 'IAVIM':
        openfisca_name = 'iai'
    elif code == 'IDEC':
        openfisca_name = 'decote'
    elif code == 'IDRS2':
        openfisca_name = 'ir_plaf_qf'
    elif code == 'IINETIR' or code == 'IRESTIR':
        openfisca_name = 'irpp'
    elif code == 'ITRED':
        openfisca_name = 'reductions'
    elif code == 'NBPT' or code == 'NBP':
        openfisca_name = 'nbptr'
    elif code == 'PPETOT':
        openfisca_name = 'ppe'
    elif code == 'REVKIRE':
        openfisca_name = 'rfr'
    elif code == 'RNICOL':
        openfisca_name = 'rni'
    elif code == 'RRBG':
        openfisca_name = 'rbg'
    # TODO: Checker si le montant net CSG/CRDS correspond à NAPCS, NAPRDS, checker IINET
    elif code == 'TOTPAC':
        openfisca_name = "len(args['totpac'] or [])"
        openfisca_value = len(args['totpac'] or [])  # Codes ignorés pour la comparaison
    elif code in ('AVFISCOPTER', 'BCSG', 'BPRS', 'BRDS', 'CIADCRE', 'CICA', 'CICORSE', 'CIDEPENV', 'CIDEVDUR',
            'CIGARD', 'CIGE', 'CIHABPRIN', 'CIMOBIL', 'CIPERT', 'CIPRETUD', 'RILMIA', 'IINET',
            'CIRCM', 'CIRELANCE', 'CITEC', 'IAVF2', 'I2DH', 'IREST', 'IRESTIR', 'RILMIH',
            'IRETS', 'ITRED', 'NAPCR', 'NAPCRP', 'NAPCS', 'RRIRENOV', 'RCELHL', 'RLOCIDEFG',
            'NAPPS', 'NAPRD', 'PERPPLAFTC', 'PERPPLAFTV', 'RAH', 'RCEL', 'RCELREPGX', 'RCELREPGW', 'RDONS',
            'RCELHJK', 'RCELREPHR', 'RCELRREDLA', 'RRESIVIEU', 'RMEUBLE', 'RREDMEUB', 'RSOCREPR', 'RRPRESCOMP',
            'RCONS', 'RPECHE', 'RCELREPGS', 'RCELREPGU', 'RCELREPGT', 'RPATNAT', 'RPATNATOT', 'RPRESCOMPREP',
            'RDIFAGRI', 'REI', 'RFOR', 'RTELEIR', 'RTOURREP', 'RTOUREPA', 'RTOUHOTR', 'RRESINEUV',
            'RFORET', 'RHEBE', 'RILMIC', 'RILMIB', 'RRESIMEUB', 'RREPMEU', 'RREPNPRO', 'TEFF',
            'RPROREP', 'RINVRED', 'RREDREP', 'RILMIX', 'PERPPLAFTP',
            'RILMIZ', 'RILMJI', 'RILMJS', 'RCODJT', 'RCODJU', 'RCODJV', 'RCODJW', 'RCODJX',
            'RIDOMENT', 'RIDOMPROE1', 'RIDOMPROE2', 'RLOGDOM', 'RREPA', 'RDUFLOGIH', 'IPROP',
            'RIDOMPROE3', 'RIDOMPROE4', 'RIDOMPROE5', 'RTITPRISE', 'RRDOM', 'RINVDOMTOMLG', 'RCOTFOR',
            'RNI', 'RNOUV', 'RRESTIMO', 'RTOUR', 'RCELRREDLC', 'RCELRREDLB', 'RCELNBGL', 'RCELFD',
            'RCELLIER', 'RCELHNO', 'RCELHM', 'RCELHR', 'RCELRREDLS', 'RCELRREDLZ', 'RCELFABC',
            'RCELREPHS', 'RCELNBGL', 'RCELCOM', 'RCELNQ', 'RCELRREDLD', 'RCELRREDLE', 'RCELRREDLF',
            'RTOURHOT', 'RTOURES', 'RTOURNEUF', 'RCELREPHR', 'RCINE', 'RFCPI', 'RINNO', 'RAA',
            'RCELREPGJ', 'RCELREPGK', 'RCELREPGL', 'RCELREPGP', 'RSOUFIP', 'RCODELOP',
            'RTOURTRA', 'TXMARJ', 'RSURV', 'RAIDE', 'RCELREPHA', 'RCELREPHB', 'RCELJP', 'RCELJOQR',
            'RCELREPHD', 'RCELREPHE', 'RCELREPHF', 'RCELREPHH', 'RCEL2012', 'RCELJBGL', 'RCOLENT',
            'RCELREPHT', 'RCELREPHU', 'RCELREPHV', 'RCELREPHW', 'RCELREPHX', 'RCELREPHZ', 'RCELRRED09', 'TXMOYIMP',
            'RFIPC', 'RILMJX', 'RILMJV', 'RCELREPGV', 'RCELRREDLM', 'RCELRREDMG', 'RILMJW', 'RCELREPHG'):
        return
    else:
        raise ValueError(u'"code" inconnu')
    log.info(u'Comparing impôts.gouv.fr variable {} with OpenFisca variable {}'.format(code, openfisca_name))
    log.info(u'Scenario:\n{}'.format(json.dumps(scenario.to_json(), encoding = 'utf_8', ensure_ascii = False,
        indent = 2)))
    if openfisca_value is None:
        openfisca_array = simulation.calculate(openfisca_name)
        assert_equal(openfisca_array.shape, (1,))
        openfisca_value = openfisca_array[0]
    assert_near(abs(openfisca_value), args['field']['value'], absolute_error_margin = 2)


def test_jsons():
    for json_file_name in os.listdir(json_dir_path):
        with open(os.path.join(json_dir_path, json_file_name)) as json_file:
            content = json.load(json_file)
        scenario_json = content['scenario']
        scenario = check(tax_benefit_system.Scenario.make_json_to_instance(tax_benefit_system = tax_benefit_system))(
            scenario_json)
        if 'year' in scenario_json:
            year = scenario_json['year']
        else:
            date = datetime.datetime.strptime(scenario_json['date'], "%Y-%m-%d")
            year = date.year
        totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')
        for code, field in content['resultat_officiel'].iteritems():
            yield check_variable, {
                'code': code,
                'field': field,
                'json_file_name': json_file_name,
                'scenario': scenario,
                'totpac': totpac,
                'year': year,
                }


if __name__ == "__main__":
    sys.exit(test_jsons())
