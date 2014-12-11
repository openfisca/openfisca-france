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

import logging

from numpy import logical_not as not_, maximum as max_, minimum as min_, around, logical_or as or_

from .base import *

log = logging.getLogger(__name__)


@reference_formula
class credits_impot(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"credits_impot"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, accult, acqgpl, aidper, creimp, drbail, prlire):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2002 """
        return accult + acqgpl + aidper + creimp + drbail + prlire

    @dated_function(start = date(2003, 1, 1), stop = date(2004, 12, 31))
    def function_20030101_20041231(self, accult, acqgpl, aidper, creimp, drbail, mecena, prlire):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2003 et 2004 """
        return accult + acqgpl + aidper + creimp + drbail + mecena + prlire

    @dated_function(start = date(2005, 1, 1), stop = date(2006, 12, 31))
    def function_20050101_20061231(self, accult, acqgpl, aidmob, aidper, assloy, ci_garext, creimp, divide, direpa, drbail, jeunes, mecena, preetu, prlire, quaenv):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2005 et 2006 """
        return (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + jeunes +
                mecena + preetu + prlire + quaenv)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, accult, acqgpl, aidmob, aidper, assloy, ci_garext, creimp, divide, direpa, drbail, inthab, jeunes, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2007 """
        return (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab +
                jeunes + mecena + preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, accult, aidmob, aidper, assloy, ci_garext, creimp, creimp_exc_2008, divide, direpa, drbail, inthab, jeunes, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2008 """
        return (accult + aidmob + aidper + assloy + ci_garext + creimp + creimp_exc_2008 + divide + direpa + drbail +
                inthab + jeunes + mecena + preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, accult, aidper, assloy, ci_garext, creimp, divide, direpa, drbail, inthab, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2009 """
        return (accult + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, accult, aidper, assloy, autent, ci_garext, creimp, direpa, drbail, inthab, jeunes, mecena, percvm, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2010 """
        return (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + percvm +
                preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, accult, aidper, assloy, autent, ci_garext, creimp, direpa, drbail, inthab, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2011 """
        return (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, accult, aidper, assloy, autent, ci_garext, cotsyn, creimp, direpa, drbail, inthab, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2012 """
        return (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, accult, aidper, assloy, autent, ci_garext, cotsyn, creimp, direpa, drbail, inthab, mecena, preetu, prlire, quaenv, saldom2):
        """ Crédits d'impôt crédités l'impôt sur les revenus de 2013 """
        return (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class nb_pac2(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_pac2"

    def function(self, nbF, nbJ, nbR, nbH):
        return nbF + nbJ + nbR - nbH / 2

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class accult(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"accult"
    start_date = date(2002, 1, 1)

    def function(self, f7uo, _P):
        '''
        Acquisition de biens culturels (case 7UO)
        2002-
        '''
        P = _P.ir.credits_impot.accult
        return P.taux * f7uo

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class acqgpl(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"acqgpl"
    start_date = date(2002, 1, 1)
    stop_date = date(2007, 12, 31)

    def function(self, f7up, f7uq, period, acqgpl = law.ir.credits_impot.acqgpl):
        '''
        Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
        2002-2007
        '''
        return f7up * acqgpl.mont_up + f7uq * acqgpl.mont_uq

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class aidmob(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"aidmob"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, f1ar, f1br, f1cr, f1dr, f1er, _P):
        '''
        Crédit d'impôt aide à la mobilité
        2005-2008
        '''
        return (f1ar + f1br + f1cr + f1dr + f1er) * _P.ir.credits_impot.aidmob.montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class aidper(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"aidper"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, marpac, nb_pac2, nbH, f7wi, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2002-2003
        '''
        P = _P.ir.credits_impot.aidper

        n = nb_pac2 - nbH / 2
        max0 = (P.max * (1 + marpac) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        return P.taux_wi * min_(f7wi, max0)

    @dated_function(start = date(2004, 1, 1), stop = date(2005, 12, 31))
    def function_20040101_20051231(self, marpac, nb_pac2, nbH, f7wi, f7wj, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2004-2005
        '''
        P = _P.ir.credits_impot.aidper

        n = nb_pac2 - nbH/2
        max0 = (P.max * (1 + marpac) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        max1 = max_(0, max0 - f7wj)
        return (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    @dated_function(start = date(2006, 1, 1), stop = date(2009, 12, 31))
    def function_20060101_20091231(self, marpac, nb_pac2, f7wi, f7wj, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2006-2009
        cf. cerfa 50796
        '''
        P = _P.ir.credits_impot.aidper

        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wj)
        return (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, marpac, nb_pac2, f7sf, f7wi, f7wj, f7wl, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7SF, 7WI, 7WJ, 7WL).
        2010-2011
        '''
        P = _P.ir.credits_impot.aidper
        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wl - f7sf)
        max2 = max_(0, max1 - f7wj)
        return P.taux_wl * min_(f7wl+f7sf, max0) + P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, marpac, nb_pac2, f7wi, f7wj, f7wl, f7wr, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL, 7WR).
        2012
        '''
        P = _P.ir.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements (7sa) et de la nature des
        #travaux, c'est un peu le bordel)
        max00 = P.max * (1 + marpac)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0,f7wl-max00))
        max2 = max_(0, max1 - f7wj)
        return (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) +
                P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2))

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, marpac, nb_pac2, f7wj, f7wl, f7wr, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2013
        '''
        P = _P.ir.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements et de la nature des
        #travaux, c'est un peu le bordel)
        max00 = P.max * (1 + marpac)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0,f7wl-max00))

        return (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) + P.taux_wj *
                min_(f7wj, max1))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class assloy(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"assloy"
    start_date = date(2005, 1, 1)

    def function(self, f4bf, _P):
        '''
        Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
        2005-
        '''
        return _P.ir.credits_impot.assloy.taux * f4bf

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class autent(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"autent"
    start_date = date(2009, 1, 1)

    def function(self, f8uy):
        '''
        Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
        2009-
        '''
        return f8uy

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class ci_garext(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ci_garext"
    start_date = date(2005, 1, 1)

    def function(self, f7ga, f7gb, f7gc, f7ge, f7gf, f7gg, _P):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
        2005-
        '''
        P = _P.ir.credits_impot.garext
        max1 = P.max
        return P.taux * (min_(f7ga, max1) +
                              min_(f7gb, max1) +
                              min_(f7gc, max1) +
                              min_(f7ge, max1 / 2) +
                              min_(f7gf, max1 / 2) +
                              min_(f7gg, max1 / 2))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class creimp_exc_2008(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"creimp_exc_2008"

    def function(self, rni, nbptr, iai, mohist, elig_creimp_exc_2008):
        '''
        Crédit d'impôt exceptionnel sur les revenus 2008
        http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf
        '''
        #TODO: gérer les DOM-TOM, corriger les formules, inclure 7KA
        rpp = rni / nbptr
        return (elig_creimp_exc_2008 * (mohist < 10700) * (rpp <= 12475) * around((2/3) * min_(12475, iai) * (rpp < 11674) +
                (rpp > 11673) * max_(0, 8317 * (12475 - rpp) / 802)))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class creimp(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"creimp"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, f2ab, f8ta, f8tb, f8tc, f8td_2002_2005, f8te, f8tf, f8tg, f8th):
        '''Avoir fiscaux et crédits d'impôt 2002 '''
        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th)

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_20030101_20031231(self, f2ab, f8ta, f8tb, f8tc, f8td_2002_2005, f8te, f8tf, f8tg, f8th, f8to, f8tp):
        '''Avoir fiscaux et crédits d'impôt 2003 '''
        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp)

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_20040101_20041231(self, f2ab, f8ta, f8tb, f8tc, f8td_2002_2005, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz):
        '''Avoir fiscaux et crédits d'impôt 2004 '''
        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz)

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, f2ab, f8ta, f8tb, f8tc, f8td_2002_2005, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wc, f8we):
        '''Avoir fiscaux et crédits d'impôt 2005 '''
        return  (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa +
                f8wb + f8wc + f8we)

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wc, f8wd, f8we, f8wr, f8ws, f8wt, f8wu):
        '''Avoir fiscaux et crédits d'impôt 2006 '''
        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8we + f8wr + f8ws + f8wt + f8wu)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wc, f8wd, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx):
        '''Avoir fiscaux et crédits d'impôt 2007 '''
        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wc, f8wd, f8we, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx):
        '''Avoir fiscaux et crédits d'impôt 2008'''
        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f2ab, f8ta, f8tb, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wd, f8we, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx):
        '''Avoir fiscaux et crédits d'impôt 2009'''
        return  (f2ab + f8ta + f8tb + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
                f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8tz, f8uz, f8wa, f8wb, f8wd, f8we, f8wr, f8wt, f8wu, f8wv):
        '''Avoir fiscaux et crédits d'impôt 2011 '''
        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
        f8we + f8wr + f8wt + f8wu + f8wv)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f2ab, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8to, f8tp, f8ts, f8tz, f8uz, f8wa, f8wb, f8wd, f8we, f8wr, f8wt, f8wu, f8wv):
        '''Avoir fiscaux et crédits d'impôt 2012 '''
        return (f2ab + f8ta + f8tb + f8tc +f8te - f8tf + f8tg + f8th + f8to - f8tp + f8ts + f8tz + f8uz + f8wa + f8wb +
                f8wd + f8we + f8wr + f8wt + f8wu + f8wv)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f2ab, f2ck, f8ta, f8tb, f8tc, f8te, f8tf, f8tg, f8th, f8tl, f8to, f8tp, f8ts, f8tz, f8uw, f8uz, f8wa, f8wb, f8wc, f8wd, f8we, f8wr, f8wt, f8wu):
        '''Avoir fiscaux et crédits d'impôt 2013 '''
        return (f2ab + f2ck + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tl + f8ts + f8tz + f8uw +
                f8uz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8wt + f8wu)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class direpa(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"direpa"

    def function(self, f2bg):
        '''
        Crédit d’impôt directive « épargne » (case 2BG)
        2006-
        '''
        return f2bg

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class divide(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"divide"
    start_date = date(2005, 1, 1)
    stop_date = date(2009, 12, 31)

    def function(self, marpac, f2dc, f2gr, _P):
        '''
        Crédit d'impôt dividendes
        2005-2009
        '''
        P = _P.ir.credits_impot.divide

        max1 = P.max * (marpac + 1)
        return min_(P.taux * (f2dc + f2gr), max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class drbail(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"drbail"

    def function(self, f4tq, _P):
        '''
        Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
        2002-
        '''
        P = _P.ir.credits_impot.drbail
        return P.taux * f4tq

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class inthab(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"inthab"

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7uh, P = law.ir.credits_impot.inthab):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7UH)
        2007
        '''
        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add
        return P.taux1 * min_(max0, f7uh)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vy, f7vz, _P):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2008
        '''
        P = _P.ir.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vy, 0)
        return (P.taux1 * min_(f7vy, max0) +
                    P.taux3 * min_(f7vz, max1))

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vx, f7vy, f7vz, _P):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2009
        '''
        P = _P.ir.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux3 * min_(f7vz, max2))

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vw, f7vx, f7vy, f7vz, _P):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2010
        '''
        P = _P.ir.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vz, max3))

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vu, f7vw, f7vv, f7vx, f7vy, f7vz, _P):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        P = _P.ir.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vu, max3) +
                    P.taux4 * min_(f7vz, max4) +
                    P.taux5 * min_(f7vv, max5))

    @dated_function(start = date(2012, 1, 1), stop = date(2013, 12, 31))
    def function_20120101_20131231(self, marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vt, f7vu, f7vv, f7vw, f7vx, f7vy, f7vz, _P):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        P = _P.ir.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (marpac + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        max6 = max_(max5 - f7vv, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vu, max3) +
                    P.taux4 * min_(f7vz, max4) +
                    P.taux5 * min_(f7vv, max5) +
                    P.taux6 * min_(f7vt, max6))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class jeunes(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"jeunes"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, jeunes_ind_holder):
        return self.sum_by_entity(jeunes_ind_holder)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class jeunes_ind(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"jeunes_ind"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, age, nbptr_holder, rfr_holder, sali, marpac_holder, elig_creimp_jeunes, _P):
        '''
        Crédit d'impôt en faveur des jeunes
        2005-2008

        rfr de l'année où jeune de moins de 26 à travaillé six mois
        cf. http://www3.finances.gouv.fr/calcul_impot/2009/pdf/form-2041-GY.pdf
        Attention seuls certains
        '''
        #TODO: vérifier si les jeunes sous le foyer fiscal de leurs parents sont éligibles

        P = _P.ir.credits_impot.jeunes
        rfr = self.cast_from_entity_to_roles(rfr_holder)
        nbptr = self.cast_from_entity_to_roles(nbptr_holder)
        marpac = self.cast_from_entity_to_roles(marpac_holder)

        elig = (age < P.age) * (rfr < P.rfr_plaf * (marpac * P.rfr_mult + not_(marpac)) + max_(0, nbptr - 2) * .5 *
                P.rfr_maj + (nbptr == 1.5) * P.rfr_maj)
        montant = (P.min <= sali) * (sali < P.int) * P.montant + (P.int <= sali) * (sali <= P.max) * (P.max - sali) * P.taux
        return elig_creimp_jeunes * elig * max_(25, montant)  # D'après  le document num. 2041 GY

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

                                # somme calculée sur formulaire 2041


@reference_formula
class mecena(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"mecena"
    start_date = date(2003, 1, 1)

    def function(self, f7us):
        '''
        Mécénat d'entreprise (case 7US)
        2003-
        '''
        return f7us

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class percvm(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"percvm"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, f3vv_end_2010, _P):
        '''
        Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
        -2010
        '''
        return _P.ir.credits_impot.percvm.taux * f3vv_end_2010

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class preetu(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"preetu"

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, f7uk, _P):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2005
        '''
        P = _P.ir.credits_impot.preetu

        return P.taux * min_(f7uk, P.max)

    @dated_function(start = date(2006, 1, 1), stop = date(2007, 12, 31))
    def function_20060101_20071231(self, f7uk, f7vo, _P):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2006-2007
        '''
        P = _P.ir.credits_impot.preetu

        max1 = P.max * (1 + f7vo)
        return P.taux * min_(f7uk, max1)

    @dated_function(start = date(2008, 1, 1), stop = date(2015, 12, 31))
    def function_20080101_20151231(self, f7uk, f7vo, f7td, _P):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2008-
        '''
        P = _P.ir.credits_impot.preetu

        max1 = P.max * f7vo
        return P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class prlire(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prélèvement libératoire à restituer (case 2DH)"
    stop_date = date(2013, 12, 31)

    def function(self, f2dh, f2ch, marpac, _P):
        '''
        Prélèvement libératoire à restituer (case 2DH)
        2002-
        http://www2.impots.gouv.fr/documentation/2013/brochure_ir/index.html#122/z
        '''
        plaf_resid = max_(_P.ir.rvcm.abat_assvie * (1 + marpac) - f2ch, 0)
        return _P.ir.credits_impot.prlire.taux * min_(f2dh, plaf_resid)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class quaenv(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"quaenv"

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, marpac, nb_pac2, f7wf, f7wg, f7wh, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH)
        2005
        '''
        P = _P.ir.credits_impot.quaenv

        n = nb_pac2
        max0 = P.max * (1 + marpac) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return (P.taux_wf * min_(f7wf, max0) +
            P.taux_wg * min_(f7wg, max1) +
            P.taux_wh * min_(f7wh, max2))

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, marpac, nb_pac2, f7wf, f7wg, f7wh, f7wq, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WQ)
        2006-2008
        '''
        P = _P.ir.credits_impot.quaenv

        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return (P.taux_wf * min_(f7wf, max0) +
                    P.taux_wg * min_(f7wg, max1) +
                    P.taux_wh * min_(f7wh, max2) +
                    P.taux_wq * min_(f7wq, max3))

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, marpac, nb_pac2, f7we, f7wf, f7wg, f7wh, f7wk, f7wq, f7sb, f7sc, f7sd, f7se, rfr, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WK, 7WQ, 7SB, 7SC, 7SD, 7SE)
        2009
        '''
        P = _P.ir.credits_impot.quaenv
        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wg)
        max6 = max_(0, max5 - f7sc)
        max7 = max_(0, max6 - f7wh)
        max8 = max_(0, max7 - f7sb)

        return or_(not_(f7we), rfr < 45000) * (P.taux_wf * min_(f7wf, max0) +
                    P.taux_se * min_(f7se, max1) +
                    P.taux_wk * min_(f7wk, max2) +
                    P.taux_sd * min_(f7sd, max3) +
                    P.taux_wg * min_(f7wg, max4) +
                    P.taux_sc * min_(f7sc, max5) +
                    P.taux_wh * min_(f7wh, max6) +
                    P.taux_sb * min_(f7sb, max7) +
                    P.taux_wq * min_(f7wq, max8))

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, marpac, nb_pac2, f7we, f7wf, f7wg, f7wh, f7wk, f7wq, f7sb, f7sd, f7se, f7sh, rfr, _P):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
        2010-2011
        '''
        P = _P.ir.credits_impot.quaenv
        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wh)
        max6 = max_(0, max5 - f7sb)
        max7 = max_(0, max6 - f7wq)
        return not_(f7wg) * or_(not_(f7we), (rfr < 45000)) * (
                    P.taux_wf * min_(f7wf, max0) +
                    P.taux_se * min_(f7se, max1) +
                    P.taux_wk * min_(f7wk, max2) +
                    P.taux_sd * min_(f7sd, max3) +
                    P.taux_wh * min_(f7wh, max4) +
                    P.taux_sb * min_(f7sb, max5) +
                    P.taux_wq * min_(f7wq, max6) +
                    P.taux_sh * min_(f7sh, max7))

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7sd, f7se, f7sf, f7sg, f7sh, f7si, f7sj, f7sk, f7sl, f7sm, f7sn, f7so, f7sp, f7sq, f7sr, f7ss, f7tt, f7tu, f7tv, f7tw, f7tx, f7ty, f7st, f7su, f7sv, f7sw, f7sz, f7wc, f7we, f7wg, f7wh, f7wk, marpac, nb_pac2, quaenv_bouquet, rfr, P = law.ir.credits_impot.quaenv):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        '''
        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2
        maxi1 = max_(0, max0 - f7ty)
        maxi2 = max_(0, maxi1 - f7tx)
        maxi3 = max_(0, maxi2 - f7tw)
        maxi4 = max_(0, maxi3 - f7tv)
        maxi5 = max_(0, maxi4 - f7tu)
        collectif = (P.taux_ty * min_(f7ty, max0) + P.taux_tx * min_(f7tx, maxi1) + P.taux_tw * min_(f7tw, maxi2) +
                P.taux_tv * min_(f7tv, maxi3) + P.taux_tu * min_(f7tu, maxi4) + P.taux_tt * min_(f7tt, maxi5))

        max1 = max_(0, max0 - quaenv_bouquet * (f7ss + f7st) - not_(quaenv_bouquet) * (f7ss + f7st + f7sv))
        max2 = max_(0, max1 - quaenv_bouquet * (f7sn + f7sr + f7sq) - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr))
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = (max_(0, max3 - quaenv_bouquet * (f7se) -
                not_(quaenv_bouquet) * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)))
        max5 = max_(0, max4 - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp) - not_(quaenv_bouquet) * (f7sm))
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))
        montant = (quaenv_bouquet * (
                        min_(max8, P.taux10 * (f7sk + f7sl)) +
                        min_(max7, P.taux11 * f7sm) +
                        min_(max6, P.taux15 * (f7sf + f7si + f7su + f7sw)) +
                        min_(max5, P.taux18 * (f7sd + f7sj)) +
                        min_(max4, P.taux23 * (f7sg + f7sh + f7so + f7sp)) +
                        min_(max3, P.taux26 * f7se) +
                        min_(max2, P.taux32 * f7sv) +
                        min_(max1, P.taux34 * (f7sn + f7sr + f7sq)) +
                        min_(max0, P.taux40 * (f7ss + f7st))) +
                    (not_(quaenv_bouquet) * (
                        min_(max0, P.taux32 * (f7ss + f7st + f7sv)) +
                        min_(max1, P.taux26 * (f7sn + f7sq + f7sr)) +
                        min_(max2, P.taux17 * f7se) +
                        min_(max3, P.taux15 * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)) +
                        min_(max4, P.taux11 * f7sm) +
                        min_(max5, P.taux10 * (f7sd + f7wk * (f7sj + f7sk + f7sl))))
                    ))
        return not_(f7wg) * or_(not_(f7we), (rfr < 30000)) * (montant + collectif) + f7sz

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f7sd, f7se, f7sf, f7sg, f7sh, f7si, f7sj, f7sk, f7sl, f7sm, f7sn, f7so, f7sp, f7sq, f7sr, f7ss, f7st, f7su, f7sv, f7sw, f7sz, f7wc, f7we, f7wg, f7wh, f7wk, marpac, nb_pac2, quaenv_bouquet, rfr, P = law.ir.credits_impot.quaenv):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        '''
        max0 = P.max * (1 + marpac) + P.pac1 * nb_pac2
        max1 = max_(0, max0 - quaenv_bouquet * (f7ss + f7st) - not_(quaenv_bouquet) * (f7ss + f7st + f7sv))
        max2 = max_(0, max1 - quaenv_bouquet * (f7sn + f7sr + f7sq) - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr))
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = (max_(0, max3 - quaenv_bouquet * (f7se) -
                not_(quaenv_bouquet) * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)))
        max5 = max_(0, max4 - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp) - not_(quaenv_bouquet) * (f7sm))
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))

        montant = (quaenv_bouquet * (
                        min_(max8, P.taux10 * (f7sk + f7sl)) +
                        min_(max7, P.taux11 * f7sm) +
                        min_(max6, P.taux15 * (f7sf + f7si + f7su + f7sw)) +
                        min_(max5, P.taux18 * (f7sd + f7sj)) +
                        min_(max4, P.taux23 * (f7sg + f7sh + f7so + f7sp)) +
                        min_(max3, P.taux26 * f7se) +
                        min_(max2, P.taux32 * f7sv) +
                        min_(max1, P.taux34 * (f7sn + f7sr + f7sq)) +
                        min_(max0, P.taux40 * (f7ss + f7st))) +
                    (not_(quaenv_bouquet) * (
                        min_(max0, P.taux32 * (f7ss + f7st + f7sv)) +
                        min_(max1, P.taux26 * (f7sn + f7sq + f7sr)) +
                        min_(max2, P.taux17 * f7se) +
                        min_(max3, P.taux15 * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)) +
                        min_(max4, P.taux11 * f7sm) +
                        min_(max5, P.taux10 * (f7sd + f7wk * (f7sj + f7sk + f7sl))))
                    ))
        return or_(not_(or_(f7we, f7wg)), (rfr < 30000)) * montant + f7sz

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class quaenv_bouquet(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"quaenv_bouquet"
    start_date = date(2013, 1, 1)

    def function(self, f7sd, f7se, f7sn, f7so, f7sp, f7sq, f7sr, f7ss, f7st, f7ve, f7vf, f7vg, f7wa, f7wb, f7wc, f7wf, f7wh, f7wq, f7ws, f7wt):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2013
        '''
        t1 = or_(or_(f7wt * f7ws, f7wq), f7wf)
        t2 = or_(f7wc * f7wb, f7wa)
        t3 = or_(f7vg * f7vf, f7ve)
        t4 = or_(f7sn > 0, f7so > 0)
        t5 = or_(f7sr > 0, f7ss > 0)
        t6 = or_(or_(or_(f7st > 0, f7sp > 0), or_(f7sq > 0, f7sd > 0)), f7se > 0)
        bouquet = (t1 + t2 + t3 + t4 + t5 + t6 > 1)
        return or_(bouquet, f7wh)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class saldom2(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"saldom2"

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, nb_pac2, f7db, f7dg, f7dl, _P):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2007-2008
        '''
        P = _P.ir.reductions_impots.saldom

        isinvalid = f7dg

        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    @dated_function(start = date(2009, 1, 1), stop = date(2013, 12, 31))
    def function_20090101_20131231(self, nb_pac2, f7db, f7dg, f7dl, f7dq, _P):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2009-2010
        '''
        P = _P.ir.reductions_impots.saldom

        isinvalid = f7dg

        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
