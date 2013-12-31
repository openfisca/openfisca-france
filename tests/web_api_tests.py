# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013 OpenFisca Team
# https://github.com/openfisca/openfisca
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


import json
import logging
import urllib2
import urlparse

from biryani1 import baseconv, custom_conv, jsonconv, states


conv = custom_conv(baseconv, jsonconv, states)
headers = {
    'User-Agent': 'OpenFisca-France-Tests/0.2dev (https://www.github.com/openfisca/openfisca-france test@openfisca.fr)',
    }
log = logging.getLogger(__name__)
web_api_url = 'http://localhost:2014/'


api_response_to_value = conv.pipe(
    conv.make_input_to_json(),
    conv.not_none,
    conv.test_isinstance(dict),
    conv.struct(
        dict(
            apiVersion = conv.pipe(
                conv.test_equals('1.0'),
                conv.not_none,
                ),
            context = conv.noop,
            data = conv.test_isinstance(dict),
            method = conv.pipe(
                conv.test_isinstance(basestring),
                conv.not_none,
                ),
            params = conv.test_isinstance(dict),
            url = conv.pipe(
                conv.make_input_to_url(full = True),
                conv.not_none,
                ),
            value = conv.noop,
            ),
        ),
    conv.function(lambda response: response['value']),
    )


def simulate_case_study(**simulation):
    request_data = dict(
        # api_key,
        value = simulation,
        )
    request_headers = headers.copy()
    request_headers['Content-Type'] = 'application/json'
    request = urllib2.Request(urlparse.urljoin(web_api_url, 'api/1/simulate'), headers = request_headers)
    try:
        response = urllib2.urlopen(request, json.dumps(request_data))
    except urllib2.HTTPError as response:
        response_text = response.read()
        try:
            response_dict = json.loads(response_text)
        except ValueError:
            log.error(response_text)
            raise
        log.error(json.dumps(response_dict, ensure_ascii = False, indent = 2, sort_keys = True))
        raise
    assert response.code == 200
    result, error = api_response_to_value(response.read(), state = conv.default_state)
    if error is not None:
        if isinstance(error, dict):
            error = json.dumps(error, ensure_ascii = False, indent = 2, sort_keys = True)
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii = False, indent = 2, sort_keys = True)
        raise ValueError(u'{0} for: {1}'.format(error, value).encode('utf-8'))
    return result


def test_case_study():
    result = simulate_case_study(
        declar = {
            '0': dict(),
            },
        famille = {
            '0': dict(),
            },
        indiv = [
            dict(
                birth = '1965-12-27',
                noichef = 0,
                noidec = 0,
                noipref = 0,
                quifam = 'chef',
                quifoy = 'vous',
                quimen = 'pref',
                ),
            ],
        menage = {
            '0': dict(),
            },
        nmen = 1,
        year = 2006,
        xaxis = 'sali',
        )
    print json.dumps(result, ensure_ascii = False, indent = 2, sort_keys = True)

