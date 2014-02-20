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


from __future__ import division

import sys
import logging
import nose

import openfisca_france
openfisca_france.init_country()

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_niches():
    """
    test pour un célibataire pour un revenu salarial de 20 000 € 
    
    """

    """
    
    CHARGES DEDUCTIBLES

    """

#    test charges déductibles: pensions alimentaires "f6gi","f6gj","f6el","f6em","f6gp","f6gu".
    tests_list = [


#   Test PA de type 6GI
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
             {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
#    PA de type 6EL
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6el" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6el" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6el" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
#   PA de type 6gj
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
#   un PA de type 6em
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6em" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6em" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6em" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
#   PA de type 6gp
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gp" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gp" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gp" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 860,
                    },
              },
#   PA de type 6gu
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# test plafond
            {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 6000,
                    },
              "output_vars" :
                    {
                     "irpp": 94,
                    },
              }, {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                     "f6gj" : 6000,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
#    test charges déductibles: CSG déductible connue, calculée sur les revenus du patrimoine "f6de".
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6de" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6de" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6de" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
#    test charges déductibles: déductions diverses "f6dd".
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6dd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6dd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6dd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },

#    test charges déductibles: frais d'accueil d'une personnde de plus de 75 ans "f6eu".
# 1 PAC 1800 €

              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# 1 PAC 3600 €
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                    },
              "output_vars" :
                    {
                     "irpp": 586,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                    },
              "output_vars" :
                    {
                     "irpp": 627,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                    },
              "output_vars" :
                    {
                     "irpp": 627,
                    },
              },

# 2 PAC 3600 €
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                     "f6ev" : 2,
                    },
              "output_vars" :
                    {
                     "irpp": 535,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                     "f6ev" : 2,
                    },
              "output_vars" :
                    {
                     "irpp": 576,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6eu" : 3600,
                     "f6ev" : 2,
                    },
              "output_vars" :
                    {
                     "irpp": 576,
                    },
              },

<<<<<<< HEAD
=======
# épargne retraite PERP,PREFON,COREM et CGOS (f6rs, f6rt, f6ru, f6ss, f6st, f6su)
# cotisations et produits assimilés : f6rs (f6rt = conjoint, f6ru= pac, mêmes conditions mais pas testées)
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6rs" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6rs" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6rs" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# test avec 1 pac
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6ru" : 1800,

                    },
              "output_vars" :
                    {
                     "irpp": 118,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6ru" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 159,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6ru" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 159,
                    },
              },

# rachats de cotisations PREFON, COREM et CGOS : f6ss (f6st = conjoint, f6su= pac, mêmes conditions mais pas testées)
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6ss" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6ss" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6ss" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# test avec 1 pac
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6su" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 118,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6su" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 159,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "nbJ": 1,
                     "f6su" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 159,
                    },
              },
# Dépenses de grosses réparations des nus-propriétaires (plafond 25 000€) (f6cb, f6hl, f6hk, f6hj)
# f6cb
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6cb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6cb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6cb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# f6hl (uniquement présente en 2012)
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hl" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
# f6hk (présente en 2012 et 2011)
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hk" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hk" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# f6hj
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6hj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# test 70 000 € pour test plafond
               {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 70000,
                    },
              "output_vars" :
                    {
                     "irpp": 13334,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 70000,
                    },
              "output_vars" :
                    {
                     "irpp": 13334,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 70000,
                    },
              "output_vars" :
                    {
                     "irpp": 13334,
                    },
              },
# test plafond avec f6cb
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 70000,
                     "f6cb" : 28000,
                    },
              "output_vars" :
                    {
                     "irpp": 5834,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 70000,
                     "f6cb" : 28000,
                    },
              "output_vars" :
                    {
                     "irpp": 5834,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 70000,
                     "f6cb" : 28000,
                    },
              "output_vars" :
                    {
                     "irpp": 5834,
                    },
              },

# test déficits globaux antérieurs non encore déduits (f6fa, f6fb, f6fc, f6fd, f6fe, f6fl)
# case f6fa
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fa" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fa" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fa" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# case f6fb
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fb" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# case f6fc
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fc" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fc" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fc" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },

# case f6fd
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fd" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# case f6fe
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fe" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fe" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fe" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
# case f6fl
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fl" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fl" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6fl" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp": 929,
                    },
              },


# test abattements spéciaux

# abattement accordé aux personnes âgées ou invalides
# pour 2010, 2011 et 2012 : 2312€ si rng<14510€, 1156€ si 14510€ < rng < 23390€

# test personnes âgées rng<14510
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 14000,
                     "age": 66,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 14000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 14000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
# test personnes âgées 14510<rng<23390
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 18000,
                     "age": 66,
                    },
              "output_vars" :
                    {
                     "irpp": 670,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 18000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 711,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 18000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 711,
                    },
              },
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 25000,
                     "age": 66,
                    },
              "output_vars" :
                    {
                     "irpp": 1649,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 25000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 1649,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 25000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 1649,
                    },
              },
# test personnes âgées rng>23390
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 28000,
                     "age": 66,
                    },
              "output_vars" :
                    {
                     "irpp": 2189,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 28000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 2189,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 28000,
                     "age" : 66,
                    },
              "output_vars" :
                    {
                     "irpp": 2189,
                    },
              },
# test personnes invalides rng < 14510
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 14000,
                     "caseP": 1,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 14000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 14000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 0,
                    },
              },
# test personnes invalides 14510 < rng < 23390
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 25000,
                     "caseP": 1,
                    },
              "output_vars" :
                    {
                     "irpp": 979,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 25000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 979,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 25000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 979,
                    },
              },
# test personnes invalides rng > 23390
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 28000,
                     "caseP": 1,
                    },
              "output_vars" :
                    {
                     "irpp": 1519,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 28000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 1519,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 28000,
                     "caseP" : 1,
                    },
              "output_vars" :
                    {
                     "irpp": 1519,
                    },
              },
# abattement pour enfants à charge ayant fondé un foyer distinct: 5698€ par personne rattachée
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 38000,
                     "nbN": 3,
                    },
              "output_vars" :
                    {
                     "irpp": 1056,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 38000,
                     "nbN" : 3,
                    },
              "output_vars" :
                    {
                     "irpp": 1056,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 38000,
                     "nbN" : 3,
                    },
              "output_vars" :
                    {
                     "irpp": 1056,
                    },
              },
# on ne peut pas tester le cas d'un enfant à charge de famille dont l'enfant est en garde alternée ?


# test abattements complémentaires
"""
'statmarit'="Veuf",
'nbF'=nb enfant -18 à charge

"caseP"

"caseP"
'nbF'=nb enfant -18 à charge


'statmarit'="Marié",
'caseS'
'nbR'
'nbI'
'caseP'
'caseF'
'caseG'


"""






>>>>>>> 443fe59... suite test_niches
            ]




    """
    
    CREDITS D'IMPOTS

    """





    for test in tests_list:

        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
            if variable in ['sali']:
                test_case.indiv[0].update({ variable: value})
            else:
                test_case.declar[0].update({ variable: value})

        df = simulation.get_results_dataframe(index_by_code = True)

        passed = True
        for variable, value in test['output_vars'].iteritems():

            computed_value = (simulation.output_table.table[variable]).sum()
            test_assertion = abs(abs(computed_value) - value) < 1
            list_var = set(test['input_vars'].keys()) - set(['sali'])
            expression = "Test failed for variables %s on year %i : \n OpenFisca value : %s \n Real value : %s \n" % (list(list_var), year, abs(computed_value), value)

            if not test_assertion:
                print expression
                passed = True
            assert passed, "Test failed for some variables"


if __name__ == '__main__':
    logging.basicConfig(level = logging.CRITICAL, stream = sys.stdout)
    test_niches()
#    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
