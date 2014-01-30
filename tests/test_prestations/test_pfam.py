# -*- coding:utf-8 -*-
# Created on 14 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

import nose
from openfisca_core.simulations import ScenarioSimulation
from datetime import datetime


''' test avec 2 enfants
    de moins de 11 ans
'''

af_2enf = {2006: 1412.64, 2007: 1436.64, 2008: 1451.04, 2009: 1494.48}


def test_af2():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr,
                              nmen = 2,
                              maxrev = 100000,
                              x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime.date(1975, 1, 1),
                                     'conj', 'part')
        simulation.scenario.addIndiv(2, datetime.date(1975, 2, 2),
                                     'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime.date(2000, 1, 1),
                                     'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime.date(2000, 1, 1),
                                     'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
#        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
#       montant AF annuel brut de CRDS

''' test avec 2 enfants
    un de 14 ans en 2006 et un de 16 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
'''


af_2enfb = {2006: 1809.96, 2007: 1840.68, 2008: 2176.56, 2009: 2241.72}


def test_af2b():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2,
                              maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1992, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1990, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
#        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_2enfb[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 2 enfants
    un de 15 ans en 2006 et un de 18 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
'''


af_2enfc = {2006: 1809.96, 2007 : 2154.96, 2008: 0.0, 2009: 0.0}


def test_af2c():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1991, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1988, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
#        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_2enfc[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 2 enfants
    de plus de 16 ans et donc la majo pour âge pour le second
'''


af_2enfm = {2006: 2118.96, 2007 : 2154.96, 2008: 2176.56, 2009: 2241.72}

def test_af2m():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1990, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1990, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enfm[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_2enfm[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 3 enfants
    de moins de 11 ans
'''

af_3enf = {2006: 3222.60, 2007 : 3277.32, 2008: 3310.08, 2009: 3409.32}

def test_af3():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(2003, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2004, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enf[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 3 enfants
    de plus de 14 ans et donc avec 3 majo pour âge
'''

af_3enfm = {2006: 5341.56, 2007 : 5432.28, 2008: 5486.64, 2009: 5651.04}

def test_af3m():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1990, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1990, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(1990, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enfm[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 3 enfants
    2 bb et 1+ 14 ans (1 majo pour âge) + test limite inf du forfait puisqu'il a 19 ans en 2009
'''

af_3enf1m = {2006: 3928.92, 2007 : 3995.64, 2008: 4035.60, 2009: 4156.56}

def test_af3m1():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1990, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2005, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enf1m[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' test avec 3 enfants
    2 bébés et un de 20 ans en 2006  puis 20 ans en 2008 et enfin 20 ans en 2009(test forfait)
'''

af_3enf1f06 = {2006: 2305.80, 2007 : 1436.64, 2008: 1451.04, 2009: 1494.48}

def test_af31f06():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1986, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2005, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enf1f06[yr]) < 1e-3
#       montant AF annuel brut de CRDS


af_3enf1f08 = {2006: 3928.92, 2007 : 3995.64, 2008: 2368.56, 2009: 1494.48}

def test_af31f08():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1988, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2005, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enf1f08[yr]) < 1e-3
#       montant AF annuel brut de CRDS


af_3enf1f09 = {2006: 3928.92, 2007 : 3995.64, 2008: 4035.60, 2009: 2439.48}

def test_af31f09():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1989, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2005, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enf1f09[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' 3 enfants, un de  14 ans en 2007, un de 20 ans en 2008 et un bb
    donc,1majo en 2006, 2 majo en 2007 et un forfait en 08 (pas de majo pour l'ainé de 2 enf à charge)
'''

af_3enfbis = {2006: 4326.24, 2007 : 4399.68, 2008: 2368.56, 2009: 1494.48}

def test_af3bis():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1988, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1993, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
        print af_3enfbis[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enfbis[yr]) < 1e-3
#       montant AF annuel brut de CRDS


''' 3 enfants, un de 19 ans en 2006, un de 19 ans en 2007, et un bb
    donc 2 majo en 2006, 1 forfait en 2007,
    rien en  2008 (car pas 3 enf a charge en 2007 du coups n'a plus droit au forfait)
    rien en 2009
'''

af_3enfter = {2006: 4635.24, 2007 : 2345.04, 2008: 0.0, 2009: 0.0}

def test_af3ter():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1987, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1988, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enfter[yr]) < 1e-3
#       montant AF annuel brut de CRDS




''' 3 enfants, un de 15 ans en 06, un de 18 ans en 06 et un bb
    donc  majo 11 ans et une majo 16 ans en 2006, 2 majo 16 ans en 2007,
    1 forfait 20 ans en  2008 et les al seules pour 2 enf en 2009
'''

af_3enfqua = {2006: 4326.24, 2007 : 4713.96, 2008: 2368.56, 2009: 1494.48}

def test_af3qua():
    for yr in range(2006, 2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975, 1, 1).date(), 'conj', 'part')
        simulation.scenario.addIndiv(2, datetime(1975, 2, 2).date(), 'conj', 'part')
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(1991, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(1988, 1, 1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(5, datetime(2005, 1, 1).date(), 'pac', 'enf')
        df = simulation.get_results_dataframe(index_by_code = True)
        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_3enfqua[yr]) < 1e-3
#       montant AF annuel brut de CRDS







if __name__ == '__main__':


    test_af2()


    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)





'''


 test avec 5 enfants
    de moins de 11 ans



af_5enf = {2006: 6842.40, 2007 : 6958.68, 2008: 7028.16, 2009: 7239.12}

def test_af5():
    for yr in range(2009,2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, nmen = 2, maxrev = 100000, x_axis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part')
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
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_5enf[yr]) < 1e-3
#       montant AF annuel brut de CRDS
'''
