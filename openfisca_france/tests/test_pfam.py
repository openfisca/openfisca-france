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


import datetime
import nose

import openfisca_france
openfisca_france.init_country()

from openfisca_core.simulations import ScenarioSimulation


def create_couple_simulation(year):
    # Instatantiation creates a unique individual
    simulation = ScenarioSimulation()
    simulation.set_config(year = year,
                          nmen = 2,
                          maxrev = 100000,
                          x_axis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')
    return simulation


def test_af2():
    '''
    test avec 2 enfants
    de moins de 11 ans
    '''
    af_2enf = {2006: 1412.64, 2007: 1436.64, 2008: 1451.04, 2009: 1494.48}

    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(2000, 1, 1),
                                     'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2000, 1, 1),
                                     'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        assert abs(df.loc["af"][0] - af_2enf[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af2b():
    ''' test avec 2 enfants
    un de 14 ans en 2006 et un de 16 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
    '''
    af_2enfb = {2006: 1809.96, 2007: 1840.68, 2008: 2176.56, 2009: 2241.72}

    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1992, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1990, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        assert abs(df.loc["af"][0] - af_2enfb[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af2c():
    '''
    test avec 2 enfants
    un de 15 ans en 2006 et un de 18 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
    '''
    af_2enfc = {2006: 1809.96, 2007 : 2154.96, 2008: 0.0, 2009: 0.0}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1991, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1988, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        assert abs(df.loc["af"][0] - af_2enfc[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af2m():
    '''
    test avec 2 enfants
    de plus de 16 ans et donc la majo pour âge pour le second
    '''
    af_2enfm = {2006: 2118.96, 2007: 2154.96, 2008: 2176.56, 2009: 2241.72}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1990, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1990, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_2enfm[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af3():
    '''
    test avec 3 enfants
    de moins de 11 ans
    '''
    af_3enf = {2006: 3222.60, 2007: 3277.32, 2008: 3310.08, 2009: 3409.32}

    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(2003, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2004, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enf[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af3m():
    '''
    test avec 3 enfants
    de plus de 14 ans et donc avec 3 majo pour âge
    '''
    af_3enfm = {2006: 5341.56, 2007: 5432.28, 2008: 5486.64, 2009: 5651.04}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1990, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1990, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(1990, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enfm[year]) < 1e-3
#       montant AF annuel brut de CRDS



def test_af3m1():
    '''
    test avec 3 enfants
    2 bb et 1+ 14 ans (1 majo pour âge) + test limite inf du forfait puisqu'il a 19 ans en 2009
    '''
    af_3enf1m = {2006: 3928.92, 2007 : 3995.64, 2008: 4035.60, 2009: 4156.56}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1990, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2005, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enf1m[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af31f06():
    '''
    test avec 3 enfants
    2 bébés et un de 20 ans en 2006  puis 20 ans en 2008 et enfin 20 ans en 2009(test forfait)
    '''
    af_3enf1f06 = {2006: 2305.80, 2007: 1436.64, 2008: 1451.04, 2009: 1494.48}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1986, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2005, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enf1f06[year]) < 1e-3
#       montant AF annuel brut de CRDS


af_3enf1f08 = {2006: 3928.92, 2007 : 3995.64, 2008: 2368.56, 2009: 1494.48}

def test_af31f08():
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1988, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2005, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enf1f08[year]) < 1e-3
#       montant AF annuel brut de CRDS



def test_af31f09():
    af_3enf1f09 = {2006: 3928.92, 2007: 3995.64, 2008: 4035.60, 2009: 2439.48}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1989, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(2005, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enf1f09[year]) < 1e-3
#       montant AF annuel brut de CRDS



def test_af3bis():
    '''
    3 enfants, un de  14 ans en 2007, un de 20 ans en 2008 et un bb
    donc,1majo en 2006, 2 majo en 2007 et un forfait en 08 (pas de majo pour l'ainé de 2 enf à charge)
    '''
    af_3enfbis = {2006: 4326.24, 2007 : 4399.68, 2008: 2368.56, 2009: 1494.48}

    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1988, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1993, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        print af_3enfbis[year]
        assert abs(df.loc["af"][0] - af_3enfbis[year]) < 1e-3
#       montant AF annuel brut de CRDS




def test_af3ter():
    '''
    3 enfants, un de 19 ans en 2006, un de 19 ans en 2007, et un bb
    donc 2 majo en 2006, 1 forfait en 2007,
    rien en  2008 (car pas 3 enf a charge en 2007 du coups n'a plus droit au forfait)
    rien en 2009
    '''
    af_3enfter = {2006: 4635.24, 2007 : 2345.04, 2008: 0.0, 2009: 0.0}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1987, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1988, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enfter[year]) < 1e-3
#       montant AF annuel brut de CRDS


def test_af3qua():
    '''
    3 enfants, un de 15 ans en 06, un de 18 ans en 06 et un bb
    donc  majo 11 ans et une majo 16 ans en 2006, 2 majo 16 ans en 2007,
    1 forfait 20 ans en  2008 et les al seules pour 2 enf en 2009
    '''
    af_3enfqua = {2006: 4326.24, 2007 : 4713.96, 2008: 2368.56, 2009: 1494.48}
    for year in range(2006, 2010):
        simulation = create_couple_simulation(year)
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime.date(1991, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(3, datetime.date(1988, 1, 1), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2005, 1, 1), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        assert abs(df.loc["af"][0] - af_3enfqua[year]) < 1e-3
#       montant AF annuel brut de CRDS




if __name__ == '__main__':


    test_af2()


#    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)





'''


 test avec 5 enfants
    de moins de 11 ans



af_5enf = {2006: 6842.40, 2007 : 6958.68, 2008: 7028.16, 2009: 7239.12}

def test_af5():
    for year in range(2009,2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = year, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2001,1,1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2002,1,1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(6, datetime(2003,1,1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(7, datetime(2004,1,1).date(), 'pac', 'enf')


        df = simulation.get_results_dataframe(index_by_code=True)
#        print df.loc["af"][0]
#        print af_2enf[year]
#        print type(df.loc["af"][0])
#        print type(af_2enf[year])
#        print abs(df.loc["af"][0] - af_2enf[year]) < 1e-3
        assert abs(df.loc["af"][0] - af_5enf[year]) < 1e-3
#       montant AF annuel brut de CRDS
'''
