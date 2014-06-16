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


import copy
import logging
import numpy as np
import os

import openfisca_france

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


# On fait l'hypothèse que le scénario ne contient qu'un seul foyer fiscal
def split(scenario):
    tax_benefit_system = scenario.tax_benefit_system
    test_case = scenario.test_case
    foyer_fiscal = test_case['foyers_fiscaux'][0]
    individus = test_case['individus']
    year = scenario.year
    rattachements_possibles = []
    detachements_impossibles = []
    scenarios = []
    impots = []

    for pac_index, pac_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
        pac = individus[pac_id].copy()
        age = year - pac.pop('birth').year - 1
        if 18 <= age < (21 + 4 * (pac['activite'] == 2)):
            rattachements_possibles.append(pac_id)
        else:
            detachements_impossibles.append(pac_id)

    foyers_possibles = partiesDe(list(rattachements_possibles))
    n = len(foyers_possibles)
    j = 1
    min_ = [-1, 0]
    for i in range(0, n):
        scenarios.append(scenario.__class__())
        scenarios[i].__dict__ = copy.copy(scenario.__dict__)
        scenarios[i].test_case = copy.deepcopy(scenario.test_case)
        scenarios[i].test_case['foyers_fiscaux'][0]['personnes_a_charge'] = foyers_possibles[i] + detachements_impossibles
        for jeune in rattachements_possibles:
            if jeune not in foyers_possibles[i]:
                scenarios[i].test_case['foyers_fiscaux'][j] = { 'declarants': [jeune], 'personnes_a_charge': [] }
                j += 1
        scenarios[i].suggest()
        simulation  = scenarios[i].new_simulation()
        irpp = - round(np.sum(simulation.calculate('irpp')))
        if irpp < min_[1] or min_[0] == -1:
            min_ = [i, irpp]
        impots.append(irpp)

    print "Le plus avantageux pour votre famille est que les jeunes rattachés à votre foyer fiscal soient : {}. Vous paierez alors {}€ d'impôts. (Seuls les jeunes éligibles au rattachement sont indiqués (18 <= age < 21 si pas étudiant / 25 sinon. Le calculateur a émis l'hypothèse qu'il n'y avait qu'un seul foyer fiscal au départ, auquel tous les jeunes éligibles étaient rattachés.)".format(foyers_possibles[min_[0]],min_[1])
    return impots


def partiesDe(tab):
    n = len(tab)
    if n == 0:
        return [[]]
    else:
        a = tab.pop()
        tab2 = partiesDe(tab)
        return add(a, tab2)


def add(a, tab):
    n = len(tab)
    for i in range (0, n):
        b = list(tab[i])
        tab.append(b)
        tab[i].append(a)
    return tab


def define_scenario(year):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        parent1 = dict(
            activite = u'Actif occupé',
            birth = 1973,
#            cadre = True,
            sali = 90000,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                birth = '1992-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                birth = '2000-04-17',
                ),
            ],
        foyer_fiscal = dict(  #TODO: pb avec f2ck
#                f7cn = 1500,
                f7rd = 100000
            ),
        year = year,
        )
    scenario.suggest()
    return scenario


def main():
    split(define_scenario(2014))
    return 0


if __name__ == "__main__":
#    sys.exit(main())
    main()
