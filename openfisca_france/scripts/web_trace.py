#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Send scenario to tracer."""


import datetime
import io
import json
import logging
import os
import urllib
import webbrowser


from openfisca_core import periods

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def trace(scenario, variables, period = None, browser_name = 'chromium',
          api_url = u"http://api.openfisca.fr", json_dumped_file = None):

    scenario_json = scenario.to_json()
    simulation_json = {
        "scenarios": [scenario_json],
        "variables": variables,
        }
    trace_base_url = u"http://www.openfisca.fr/outils/trace"
    url = trace_base_url + "?" + urllib.urlencode({
        "simulation": json.dumps(simulation_json),
        "api_url": api_url,
        })
    browser = webbrowser.get(browser_name)
    browser.open_new_tab(url)
    if json_dumped_file:
        with io.open(json_dumped_file, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(scenario_json, ensure_ascii=False, encoding='utf-8', indent = 2)))


if __name__ == '__main__':
    from base import tax_benefit_system
    period = "2014-12"
    parent1 = dict(
        date_naissance = datetime.date(periods.period(period).start.year - 40, 1, 1),
        salbrut = {"2014-12": 1445.38},
        )

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        period = period,
        parent1 = parent1,
        )
    variables = ["salaire_super_brut"]
    trace(
        scenario,
        variables,
        api_url = u"http://127.0.0.1:2000",
        json_dumped_file = "test_smicard.json",
        )
