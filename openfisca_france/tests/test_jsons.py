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


"""Teste tous les fichiers .json créés par un script"""


import datetime
import json
import os
import sys

from biryani1.baseconv import check
from nose.tools import assert_equal, assert_less
import numpy

from . import base


json_dir_path = os.path.join(os.path.dirname(__file__), 'json')


def check_variable(ctx):
    code = ctx['code']
    simulation = ctx['simulation']
    if code == 'IAVIM':
        openfisca_value = simulation.calculate('iai')
    elif code == 'IDEC':
        openfisca_value = simulation.calculate('decote')
    elif code == 'IDRS2':
        openfisca_value = simulation.calculate('ir_plaf_qf')
    elif code == 'IINETIR' or code == 'IRESTIR':
        openfisca_value = -simulation.calculate('irpp')
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
    # TODO: Checker si le montant net CSG/CRDS correspond à NAPCS, NAPRDS, checker IINET
    elif code == 'TOTPAC':
        openfisca_value = len(ctx['totpac'] or [])  # Codes ignorés pour la comparaison
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
    if isinstance(openfisca_value, numpy.ndarray):
        assert_equal(openfisca_value.shape, (1,))
        openfisca_value = openfisca_value[0]
    error_margin = 2
    assert_less(abs(ctx['field']['value'] - openfisca_value), error_margin)


def test_jsons():
    for json_file_name in os.listdir(json_dir_path):
        with open(os.path.join(json_dir_path, json_file_name)) as json_file:
            content = json.load(json_file)
        scenario_json = content['scenario']
        scenario = check(base.tax_benefit_system.Scenario.make_json_to_instance(
            tax_benefit_system = base.tax_benefit_system))(scenario_json)
        if 'year' in scenario_json:
            year = scenario_json['year']
        else:
            date = datetime.datetime.strptime(scenario_json['date'], "%Y-%m-%d")
            year = date.year
        totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')
        simulation = scenario.new_simulation()
        for code, field in content['resultat_officiel'].iteritems():
            ctx = {
                'code': code,
                'field': field,
                'json_file_name': json_file_name,
                'simulation': simulation,
                'totpac': totpac,
                'year': year,
                }
            yield check_variable, ctx


if __name__ == "__main__":
    sys.exit(test_jsons())
