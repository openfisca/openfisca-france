# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import logical_not as not_, maximum as max_, minimum as min_, around, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)


class credits_impot(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédits d'impôt pour l'impôt sur les revenus"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2002 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        acqgpl = simulation.calculate('acqgpl', period)
        aidper = simulation.calculate('aidper', period)
        creimp = simulation.calculate('creimp', period)
        drbail = simulation.calculate('drbail', period)
        prlire = simulation.calculate('prlire', period)

        return period, accult + acqgpl + aidper + creimp + drbail + prlire

    @dated_function(start = date(2003, 1, 1), stop = date(2004, 12, 31))
    def function_20030101_20041231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2003 et 2004 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        acqgpl = simulation.calculate('acqgpl', period)
        aidper = simulation.calculate('aidper', period)
        creimp = simulation.calculate('creimp', period)
        drbail = simulation.calculate('drbail', period)
        mecena = simulation.calculate('mecena', period)
        prlire = simulation.calculate('prlire', period)

        return period, accult + acqgpl + aidper + creimp + drbail + mecena + prlire

    @dated_function(start = date(2005, 1, 1), stop = date(2006, 12, 31))
    def function_20050101_20061231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2005 et 2006 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        acqgpl = simulation.calculate('acqgpl', period)
        aidmob = simulation.calculate('aidmob', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        divide = simulation.calculate('divide', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        jeunes = simulation.calculate('jeunes', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)

        return period, (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + jeunes +
                mecena + preetu + prlire + quaenv)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2007 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        acqgpl = simulation.calculate('acqgpl', period)
        aidmob = simulation.calculate('aidmob', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        divide = simulation.calculate('divide', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        jeunes = simulation.calculate('jeunes', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab +
                jeunes + mecena + preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2008 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidmob = simulation.calculate('aidmob', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        creimp_exc_2008 = simulation.calculate('creimp_exc_2008', period)
        divide = simulation.calculate('divide', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        jeunes = simulation.calculate('jeunes', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidmob + aidper + assloy + ci_garext + creimp + creimp_exc_2008 + divide + direpa + drbail +
                inthab + jeunes + mecena + preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2009 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        divide = simulation.calculate('divide', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2010 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        autent = simulation.calculate('autent', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        jeunes = simulation.calculate('jeunes', period)
        mecena = simulation.calculate('mecena', period)
        percvm = simulation.calculate('percvm', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + percvm +
                preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2011 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        autent = simulation.calculate('autent', period)
        ci_garext = simulation.calculate('ci_garext', period)
        creimp = simulation.calculate('creimp', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2012 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        autent = simulation.calculate('autent', period)
        ci_garext = simulation.calculate('ci_garext', period)
        cotsyn = simulation.calculate('cotsyn', period)
        creimp = simulation.calculate('creimp', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, simulation, period):
        """ Crédits d'impôt crédités l'impôt sur les revenus de 2013 """
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        autent = simulation.calculate('autent', period)
        ci_garext = simulation.calculate('ci_garext', period)
        cotsyn = simulation.calculate('cotsyn', period)
        creimp = simulation.calculate('creimp', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    @dated_function(start = date(2014, 1, 1))  # Not checked
    def function_2014__(self, simulation, period):
        """ Crédits d'impôt crédités l'impôt sur les revenus de 2014 et + (non vérifié)"""
        period = period.this_year
        accult = simulation.calculate('accult', period)
        aidper = simulation.calculate('aidper', period)
        assloy = simulation.calculate('assloy', period)
        autent = simulation.calculate('autent', period)
        ci_garext = simulation.calculate('ci_garext', period)
        cotsyn = simulation.calculate('cotsyn', period)
        creimp = simulation.calculate('creimp', period)
        direpa = simulation.calculate('direpa', period)
        drbail = simulation.calculate('drbail', period)
        inthab = simulation.calculate('inthab', period)
        mecena = simulation.calculate('mecena', period)
        preetu = simulation.calculate('preetu', period)
        prlire = simulation.calculate('prlire', period)
        quaenv = simulation.calculate('quaenv', period)
        saldom2 = simulation.calculate('saldom2', period)

        return period, (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)


class nb_pac2(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"nb_pac2"

    def function(self, simulation, period):
        period = period.this_year
        nbF = simulation.calculate('nbF', period)
        nbJ = simulation.calculate('nbJ', period)
        nbR = simulation.calculate('nbR', period)
        nbH = simulation.calculate('nbH', period)

        return period, nbF + nbJ + nbR - nbH / 2


class accult(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Acquisition de biens culturels"
    start_date = date(2002, 1, 1)

    def function(self, simulation, period):
        '''
        Acquisition de biens culturels (case 7UO)
        2002-
        '''
        period = period.this_year
        f7uo = simulation.calculate('f7uo', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.accult
        return period, P.taux * f7uo


class acqgpl(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte"
    start_date = date(2002, 1, 1)
    stop_date = date(2007, 12, 31)

    def function(self, simulation, period):
        '''
        Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
        2002-2007
        '''
        period = period.this_year
        f7up = simulation.calculate('f7up', period)
        f7uq = simulation.calculate('f7uq', period)
        acqgpl = simulation.legislation_at(period.start).impot_revenu.credits_impot.acqgpl

        return period, f7up * acqgpl.mont_up + f7uq * acqgpl.mont_uq


class aidmob(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, simulation, period):
        '''
        Crédit d'impôt aide à la mobilité
        2005-2008
        '''
        period = period.this_year
        f1ar = simulation.calculate('f1ar', period)
        f1br = simulation.calculate('f1br', period)
        f1cr = simulation.calculate('f1cr', period)
        f1dr = simulation.calculate('f1dr', period)
        f1er = simulation.calculate('f1er', period)
        _P = simulation.legislation_at(period.start)

        return period, (f1ar + f1br + f1cr + f1dr + f1er) * _P.impot_revenu.credits_impot.aidmob.montant


class aidper(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de l’aide aux personnes"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2002-2003
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        nbH = simulation.calculate('nbH', period)
        f7wi = simulation.calculate('f7wi', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper

        n = nb_pac2 - nbH / 2
        max0 = (P.max * (1 + maries_ou_pacses) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        return period, P.taux_wi * min_(f7wi, max0)

    @dated_function(start = date(2004, 1, 1), stop = date(2005, 12, 31))
    def function_20040101_20051231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2004-2005
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        nbH = simulation.calculate('nbH', period)
        f7wi = simulation.calculate('f7wi', period)
        f7wj = simulation.calculate('f7wj', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper

        n = nb_pac2 - nbH/2
        max0 = (P.max * (1 + maries_ou_pacses) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        max1 = max_(0, max0 - f7wj)
        return period, (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    @dated_function(start = date(2006, 1, 1), stop = date(2009, 12, 31))
    def function_20060101_20091231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2006-2009
        cf. cerfa 50796
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wi = simulation.calculate('f7wi', period)
        f7wj = simulation.calculate('f7wj', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wj)
        return period, (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7SF, 7WI, 7WJ, 7WL).
        2010-2011
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7sf = simulation.calculate('f7sf', period)
        f7wi = simulation.calculate('f7wi', period)
        f7wj = simulation.calculate('f7wj', period)
        f7wl = simulation.calculate('f7wl', period)
        _P = simulation.legislation_at(period.start)


        P = _P.impot_revenu.credits_impot.aidper
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wl - f7sf)
        max2 = max_(0, max1 - f7wj)
        return period, P.taux_wl * min_(f7wl+f7sf, max0) + P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL, 7WR).
        2012
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wi = simulation.calculate('f7wi', period)
        f7wj = simulation.calculate('f7wj', period)
        f7wl = simulation.calculate('f7wl', period)
        f7wr = simulation.calculate('f7wr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements (7sa) et de la nature des
        #travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0,f7wl-max00))
        max2 = max_(0, max1 - f7wj)
        return period, (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) +
                P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2))

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2013
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wj = simulation.calculate('f7wj', period)
        f7wl = simulation.calculate('f7wl', period)
        f7wr = simulation.calculate('f7wr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements et de la nature des
        # travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0, f7wl - max00))

        return period, (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) + P.taux_wj *
                min_(f7wj, max1))

    @dated_function(start = date(2014, 1, 1))
    def function_2014__(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2014 et supérieurs non vérifiée
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wj = simulation.calculate('f7wj', period)
        f7wl = simulation.calculate('f7wl', period)
        f7wr = simulation.calculate('f7wr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements et de la nature des
        # travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0, f7wl - max00))

        return period, (
            P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) +
            P.taux_wj * min_(f7wj, max1)
            )


class assloy(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt primes d’assurance pour loyers impayés"
    start_date = date(2005, 1, 1)

    def function(self, simulation, period):
        '''
        Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
        2005-
        '''
        period = period.this_year
        f4bf = simulation.calculate('f4bf', period)
        _P = simulation.legislation_at(period.start)

        return period, _P.impot_revenu.credits_impot.assloy.taux * f4bf


class autent(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"autent"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
        2009-
        '''
        period = period.this_year
        f8uy = simulation.calculate('f8uy', period)

        return period, f8uy


class ci_garext(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Frais de garde des enfants à l’extérieur du domicile"
    start_date = date(2005, 1, 1)

    def function(self, simulation, period):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
        2005-
        '''
        period = period.this_year
        f7ga = simulation.calculate('f7ga', period)
        f7gb = simulation.calculate('f7gb', period)
        f7gc = simulation.calculate('f7gc', period)
        f7ge = simulation.calculate('f7ge', period)
        f7gf = simulation.calculate('f7gf', period)
        f7gg = simulation.calculate('f7gg', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.garext
        max1 = P.plafond
        return period, P.taux * (min_(f7ga, max1) +
                              min_(f7gb, max1) +
                              min_(f7gc, max1) +
                              min_(f7ge, max1 / 2) +
                              min_(f7gf, max1 / 2) +
                              min_(f7gg, max1 / 2))


class creimp_exc_2008(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d'impôt exceptionnel sur les revenus 2008"

    def function(self, simulation, period):
        '''
        Crédit d'impôt exceptionnel sur les revenus 2008
        http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf
        '''
        period = period.this_year
        rni = simulation.calculate('rni', period)
        nbptr = simulation.calculate('nbptr', period)
        iai = simulation.calculate('iai', period)
        mohist = simulation.calculate('mohist', period)
        elig_creimp_exc_2008 = simulation.calculate('elig_creimp_exc_2008', period)

        #TODO: gérer les DOM-TOM, corriger les formules, inclure 7KA
        rpp = rni / nbptr
        return period, (elig_creimp_exc_2008 * (mohist < 10700) * (rpp <= 12475) * around((2/3) * min_(12475, iai) * (rpp < 11674) +
                (rpp > 11673) * max_(0, 8317 * (12475 - rpp) / 802)))


class creimp(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Avoirs fiscaux et crédits d'impôt"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8td_2002_2005 = simulation.calculate('f8td_2002_2005', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)

        return period, (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th)

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_20030101_20031231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8td_2002_2005 = simulation.calculate('f8td_2002_2005', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)

        return period, (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp)

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_20040101_20041231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8td_2002_2005 = simulation.calculate('f8td_2002_2005', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)

        return period, (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz)

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8td_2002_2005 = simulation.calculate('f8td_2002_2005', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wc = simulation.calculate('f8wc', period)
        f8we = simulation.calculate('f8we', period)

        return period,  (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa +
                f8wb + f8wc + f8we)

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wc = simulation.calculate('f8wc', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8ws = simulation.calculate('f8ws', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)

        return period,  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8we + f8wr + f8ws + f8wt + f8wu)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wc = simulation.calculate('f8wc', period)
        f8wd = simulation.calculate('f8wd', period)
        f8wr = simulation.calculate('f8wr', period)
        f8ws = simulation.calculate('f8ws', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)
        f8wv = simulation.calculate('f8wv', period)
        f8wx = simulation.calculate('f8wx', period)

        return period,  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wc = simulation.calculate('f8wc', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8ws = simulation.calculate('f8ws', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)
        f8wv = simulation.calculate('f8wv', period)
        f8wx = simulation.calculate('f8wx', period)

        return period,  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8ws = simulation.calculate('f8ws', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)
        f8wv = simulation.calculate('f8wv', period)
        f8wx = simulation.calculate('f8wx', period)

        return period,  (f2ab + f8ta + f8tb + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
                f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)
        f8wv = simulation.calculate('f8wv', period)

        return period, (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
        f8we + f8wr + f8wt + f8wu + f8wv)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8ts = simulation.calculate('f8ts', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)
        f8wv = simulation.calculate('f8wv', period)

        return period, (f2ab + f8ta + f8tb + f8tc +f8te - f8tf + f8tg + f8th + f8to - f8tp + f8ts + f8tz + f8uz + f8wa + f8wb +
                f8wd + f8we + f8wr + f8wt + f8wu + f8wv)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, simulation, period):
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)
        f2ck = simulation.calculate('f2ck', period)
        f8ta = simulation.calculate('f8ta', period)
        f8tb = simulation.calculate('f8tb', period)
        f8tc = simulation.calculate('f8tc', period)
        f8te = simulation.calculate('f8te', period)
        f8tf = simulation.calculate('f8tf', period)
        f8tg = simulation.calculate('f8tg', period)
        f8th = simulation.calculate('f8th', period)
        f8tl = simulation.calculate('f8tl', period)
        f8to = simulation.calculate('f8to', period)
        f8tp = simulation.calculate('f8tp', period)
        f8ts = simulation.calculate('f8ts', period)
        f8tz = simulation.calculate('f8tz', period)
        f8uw = simulation.calculate('f8uw', period)
        f8uz = simulation.calculate('f8uz', period)
        f8wa = simulation.calculate('f8wa', period)
        f8wb = simulation.calculate('f8wb', period)
        f8wc = simulation.calculate('f8wc', period)
        f8wd = simulation.calculate('f8wd', period)
        f8we = simulation.calculate('f8we', period)
        f8wr = simulation.calculate('f8wr', period)
        f8wt = simulation.calculate('f8wt', period)
        f8wu = simulation.calculate('f8wu', period)

        return period, (f2ab + f2ck + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tl + f8ts + f8tz + f8uw +
                f8uz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8wt + f8wu)


class direpa(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt directive « épargne »"

    def function(self, simulation, period):
        '''
        Crédit d’impôt directive « épargne » (case 2BG)
        2006-
        '''
        period = period.this_year
        f2bg = simulation.calculate('f2bg', period)

        return period, f2bg


class divide(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d'impôt dividendes"
    start_date = date(2005, 1, 1)
    stop_date = date(2009, 12, 31)

    def function(self, simulation, period):
        '''
        Crédit d'impôt dividendes
        2005-2009
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        f2dc = simulation.calculate('f2dc', period)
        f2gr = simulation.calculate('f2gr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.divide

        max1 = P.max * (maries_ou_pacses + 1)
        return period, min_(P.taux * (f2dc + f2gr), max1)


class drbail(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail"

    def function(self, simulation, period):
        '''
        Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
        2002-
        '''
        period = period.this_year
        f4tq = simulation.calculate('f4tq', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.drbail
        return period, P.taux * f4tq


class inthab(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt intérêts des emprunts pour l’habitation principale"

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7UH)
        2007
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7uh = simulation.calculate('f7uh', period)
        P = simulation.legislation_at(period.start).impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add
        return period, P.taux1 * min_(max0, f7uh)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2008
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7vy = simulation.calculate('f7vy', period)
        f7vz = simulation.calculate('f7vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vy, 0)
        return period, (P.taux1 * min_(f7vy, max0) +
                    P.taux3 * min_(f7vz, max1))

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2009
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7vx = simulation.calculate('f7vx', period)
        f7vy = simulation.calculate('f7vy', period)
        f7vz = simulation.calculate('f7vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        return period, (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux3 * min_(f7vz, max2))

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2010
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7vw = simulation.calculate('f7vw', period)
        f7vx = simulation.calculate('f7vx', period)
        f7vy = simulation.calculate('f7vy', period)
        f7vz = simulation.calculate('f7vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        return period, (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vz, max3))

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7vu = simulation.calculate('f7vu', period)
        f7vw = simulation.calculate('f7vw', period)
        f7vv = simulation.calculate('f7vv', period)
        f7vx = simulation.calculate('f7vx', period)
        f7vy = simulation.calculate('f7vy', period)
        f7vz = simulation.calculate('f7vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        return period, (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vu, max3) +
                    P.taux4 * min_(f7vz, max4) +
                    P.taux5 * min_(f7vv, max5))

    @dated_function(start = date(2012, 1, 1), stop = date(2013, 12, 31))
    def function_20120101_20131231(self, simulation, period):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        nbG = simulation.calculate('nbG', period)
        nbR = simulation.calculate('nbR', period)
        f7vt = simulation.calculate('f7vt', period)
        f7vu = simulation.calculate('f7vu', period)
        f7vv = simulation.calculate('f7vv', period)
        f7vw = simulation.calculate('f7vw', period)
        f7vx = simulation.calculate('f7vx', period)
        f7vy = simulation.calculate('f7vy', period)
        f7vz = simulation.calculate('f7vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        max6 = max_(max5 - f7vv, 0)
        return period, (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vu, max3) +
                    P.taux4 * min_(f7vz, max4) +
                    P.taux5 * min_(f7vv, max5) +
                    P.taux6 * min_(f7vt, max6))


class jeunes(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"jeunes"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, simulation, period):
        period = period.this_year
        jeunes_ind_holder = simulation.compute('jeunes_ind', period)

        return period, self.sum_by_entity(jeunes_ind_holder)


class jeunes_ind(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Crédit d'impôt en faveur des jeunes"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, simulation, period):
        '''
        Crédit d'impôt en faveur des jeunes
        2005-2008

        rfr de l'année où jeune de moins de 26 à travaillé six mois
        cf. http://www3.finances.gouv.fr/calcul_impot/2009/pdf/form-2041-GY.pdf
        Attention seuls certains
        '''
        period = period.this_year
        age = simulation.calculate('age', period)
        nbptr_holder = simulation.compute('nbptr', period)
        rfr_holder = simulation.compute('rfr', period)
        salaire_imposable =  simulation.calculate_add('salaire_imposable', period)
        maries_ou_pacses_holder = simulation.compute('maries_ou_pacses', period)
        elig_creimp_jeunes = simulation.calculate('elig_creimp_jeunes', period)
        _P = simulation.legislation_at(period.start)

        #TODO: vérifier si les jeunes sous le foyer fiscal de leurs parents sont éligibles

        P = _P.impot_revenu.credits_impot.jeunes
        rfr = self.cast_from_entity_to_roles(rfr_holder)
        nbptr = self.cast_from_entity_to_roles(nbptr_holder)
        maries_ou_pacses = self.cast_from_entity_to_roles(maries_ou_pacses_holder)

        elig = (age < P.age) * (rfr < P.rfr_plaf * (maries_ou_pacses * P.rfr_mult + not_(maries_ou_pacses)) + max_(0, nbptr - 2) * .5 *
                P.rfr_maj + (nbptr == 1.5) * P.rfr_maj)
        montant = (
            (P.min <= salaire_imposable) * (salaire_imposable < P.int) * P.montant +
            (P.int <= salaire_imposable) * (salaire_imposable <= P.max) * (P.max - salaire_imposable) * P.taux
            )
        return period, elig_creimp_jeunes * elig * max_(25, montant)  # D'après  le document num. 2041 GY


                                # somme calculée sur formulaire 2041


class mecena(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Mécénat d'entreprise"
    start_date = date(2003, 1, 1)

    def function(self, simulation, period):
        '''
        Mécénat d'entreprise (case 7US)
        2003-
        '''
        period = period.this_year
        f7us = simulation.calculate('f7us', period)

        return period, f7us


class percvm(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt pertes sur cessions de valeurs mobilières"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
        -2010
        '''
        period = period.this_year
        f3vv_end_2010 = simulation.calculate('f3vv_end_2010', period)
        _P = simulation.legislation_at(period.start)

        return period, _P.impot_revenu.credits_impot.percvm.taux * f3vv_end_2010


class preetu(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt pour souscription de prêts étudiants"

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, simulation, period):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2005
        '''
        period = period.this_year
        f7uk = simulation.calculate('f7uk', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.preetu

        return period, P.taux * min_(f7uk, P.max)

    @dated_function(start = date(2006, 1, 1), stop = date(2007, 12, 31))
    def function_20060101_20071231(self, simulation, period):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2006-2007
        '''
        period = period.this_year
        f7uk = simulation.calculate('f7uk', period)
        f7vo = simulation.calculate('f7vo', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.preetu

        max1 = P.max * (1 + f7vo)
        return period, P.taux * min_(f7uk, max1)

    @dated_function(start = date(2008, 1, 1))
    def function_20080101_20151231(self, simulation, period):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2008-
        '''
        period = period.this_year
        f7uk = simulation.calculate('f7uk', period)
        f7vo = simulation.calculate('f7vo', period)
        f7td = simulation.calculate('f7td', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.preetu

        max1 = P.max * f7vo
        return period, P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)


class prlire(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Prélèvement libératoire à restituer (case 2DH)"
    stop_date = date(2013, 12, 31)

    def function(self, simulation, period):
        '''
        Prélèvement libératoire à restituer (case 2DH)
        2002-
        http://www2.impots.gouv.fr/documentation/2013/brochure_ir/index.html#122/z
        '''
        period = period.this_year
        f2dh = simulation.calculate('f2dh', period)
        f2ch = simulation.calculate('f2ch', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        _P = simulation.legislation_at(period.start)

        plaf_resid = max_(_P.impot_revenu.rvcm.abat_assvie * (1 + maries_ou_pacses) - f2ch, 0)
        return period, _P.impot_revenu.credits_impot.prlire.taux * min_(f2dh, plaf_resid)


class quaenv(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale"

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH)
        2005
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wf = simulation.calculate('f7wf', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.quaenv

        n = nb_pac2
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return period, (P.taux_wf * min_(f7wf, max0) +
            P.taux_wg * min_(f7wg, max1) +
            P.taux_wh * min_(f7wh, max2))

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WQ)
        2006-2008
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7wf = simulation.calculate('f7wf', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wq = simulation.calculate('f7wq', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return period, (P.taux_wf * min_(f7wf, max0) +
                    P.taux_wg * min_(f7wg, max1) +
                    P.taux_wh * min_(f7wh, max2) +
                    P.taux_wq * min_(f7wq, max3))

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WK, 7WQ, 7SB, 7SC, 7SD, 7SE)
        2009
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7we = simulation.calculate('f7we', period)
        f7wf = simulation.calculate('f7wf', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wk = simulation.calculate('f7wk', period)
        f7wq = simulation.calculate('f7wq', period)
        f7sb = simulation.calculate('f7sb', period)
        f7sc = simulation.calculate('f7sc', period)
        f7sd = simulation.calculate('f7sd', period)
        f7se = simulation.calculate('f7se', period)
        rfr = simulation.calculate('rfr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.quaenv
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wg)
        max6 = max_(0, max5 - f7sc)
        max7 = max_(0, max6 - f7wh)
        max8 = max_(0, max7 - f7sb)

        return period, or_(not_(f7we), rfr < 45000) * (P.taux_wf * min_(f7wf, max0) +
                    P.taux_se * min_(f7se, max1) +
                    P.taux_wk * min_(f7wk, max2) +
                    P.taux_sd * min_(f7sd, max3) +
                    P.taux_wg * min_(f7wg, max4) +
                    P.taux_sc * min_(f7sc, max5) +
                    P.taux_wh * min_(f7wh, max6) +
                    P.taux_sb * min_(f7sb, max7) +
                    P.taux_wq * min_(f7wq, max8))

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
        2010-2011
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7we = simulation.calculate('f7we', period)
        f7wf = simulation.calculate('f7wf', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wk = simulation.calculate('f7wk', period)
        f7wq = simulation.calculate('f7wq', period)
        f7sb = simulation.calculate('f7sb', period)
        f7sd = simulation.calculate('f7sd', period)
        f7se = simulation.calculate('f7se', period)
        f7sh = simulation.calculate('f7sh', period)
        rfr = simulation.calculate('rfr', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.credits_impot.quaenv
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wh)
        max6 = max_(0, max5 - f7sb)
        max7 = max_(0, max6 - f7wq)
        return period, not_(f7wg) * or_(not_(f7we), (rfr < 45000)) * (
            P.taux_wf * min_(f7wf, max0) +
            P.taux_se * min_(f7se, max1) +
            P.taux_wk * min_(f7wk, max2) +
            P.taux_sd * min_(f7sd, max3) +
            P.taux_wh * min_(f7wh, max4) +
            P.taux_sb * min_(f7sb, max5) +
            P.taux_wq * min_(f7wq, max6) +
            P.taux_sh * min_(f7sh, max7)
            )

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2012
        '''
        period = period.this_year
        f7sd = simulation.calculate('f7sd', period)
        f7se = simulation.calculate('f7se', period)
        f7sf = simulation.calculate('f7sf', period)
        f7sg = simulation.calculate('f7sg', period)
        f7sh = simulation.calculate('f7sh', period)
        f7si = simulation.calculate('f7si', period)
        f7sj = simulation.calculate('f7sj', period)
        f7sk = simulation.calculate('f7sk', period)
        f7sl = simulation.calculate('f7sl', period)
        f7sm = simulation.calculate('f7sm', period)
        f7sn = simulation.calculate('f7sn', period)
        f7so = simulation.calculate('f7so', period)
        f7sp = simulation.calculate('f7sp', period)
        f7sq = simulation.calculate('f7sq', period)
        f7sr = simulation.calculate('f7sr', period)
        f7ss = simulation.calculate('f7ss', period)
        f7tt = simulation.calculate('f7tt', period)
        f7tu = simulation.calculate('f7tu', period)
        f7tv = simulation.calculate('f7tv', period)
        f7tw = simulation.calculate('f7tw', period)
        f7tx = simulation.calculate('f7tx', period)
        f7ty = simulation.calculate('f7ty', period)
        f7st = simulation.calculate('f7st', period)
        f7su = simulation.calculate('f7su', period)
        f7sv = simulation.calculate('f7sv', period)
        f7sw = simulation.calculate('f7sw', period)
        f7sz = simulation.calculate('f7sz', period)
        f7wc = simulation.calculate('f7wc', period)
        f7we = simulation.calculate('f7we', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wk = simulation.calculate('f7wk', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        quaenv_bouquet = simulation.calculate('quaenv_bouquet', period)
        rfr = simulation.calculate('rfr', period)
        P = simulation.legislation_at(period.start).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2
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
        return period, not_(f7wg) * or_(not_(f7we), (rfr < 30000)) * (montant + collectif) + f7sz

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, simulation, period):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        '''
        period = period.this_year
        f7sd = simulation.calculate('f7sd', period)
        f7se = simulation.calculate('f7se', period)
        f7sf = simulation.calculate('f7sf', period)
        f7sg = simulation.calculate('f7sg', period)
        f7sh = simulation.calculate('f7sh', period)
        f7si = simulation.calculate('f7si', period)
        f7sj = simulation.calculate('f7sj', period)
        f7sk = simulation.calculate('f7sk', period)
        f7sl = simulation.calculate('f7sl', period)
        f7sm = simulation.calculate('f7sm', period)
        f7sn = simulation.calculate('f7sn', period)
        f7so = simulation.calculate('f7so', period)
        f7sp = simulation.calculate('f7sp', period)
        f7sq = simulation.calculate('f7sq', period)
        f7sr = simulation.calculate('f7sr', period)
        f7ss = simulation.calculate('f7ss', period)
        f7st = simulation.calculate('f7st', period)
        f7su = simulation.calculate('f7su', period)
        f7sv = simulation.calculate('f7sv', period)
        f7sw = simulation.calculate('f7sw', period)
        f7sz = simulation.calculate('f7sz', period)
        f7wc = simulation.calculate('f7wc', period)
        f7we = simulation.calculate('f7we', period)
        f7wg = simulation.calculate('f7wg', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wk = simulation.calculate('f7wk', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        nb_pac2 = simulation.calculate('nb_pac2', period)
        quaenv_bouquet = simulation.calculate('quaenv_bouquet', period)
        rfr = simulation.calculate('rfr', period)
        P = simulation.legislation_at(period.start).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2
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
        return period, or_(not_(or_(f7we, f7wg)), (rfr < 30000)) * montant + f7sz


class quaenv_bouquet(Variable):
    column = BoolCol(default = False)
    entity = FoyerFiscal
    label = u"quaenv_bouquet"
    start_date = date(2013, 1, 1)

    def function(self, simulation, period):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2013
        '''
        period = period.this_year
        f7sd = simulation.calculate('f7sd', period)
        f7se = simulation.calculate('f7se', period)
        f7sn = simulation.calculate('f7sn', period)
        f7so = simulation.calculate('f7so', period)
        f7sp = simulation.calculate('f7sp', period)
        f7sq = simulation.calculate('f7sq', period)
        f7sr = simulation.calculate('f7sr', period)
        f7ss = simulation.calculate('f7ss', period)
        f7st = simulation.calculate('f7st', period)
        f7ve = simulation.calculate('f7ve', period)
        f7vf = simulation.calculate('f7vf', period)
        f7vg = simulation.calculate('f7vg', period)
        f7wa = simulation.calculate('f7wa', period)
        f7wb = simulation.calculate('f7wb', period)
        f7wc = simulation.calculate('f7wc', period)
        f7wf = simulation.calculate('f7wf', period)
        f7wh = simulation.calculate('f7wh', period)
        f7wq = simulation.calculate('f7wq', period)
        f7ws = simulation.calculate('f7ws', period)
        f7wt = simulation.calculate('f7wt', period)

        t1 = or_(or_(f7wt * f7ws, f7wq), f7wf)
        t2 = or_(f7wc * f7wb, f7wa)
        t3 = or_(f7vg * f7vf, f7ve)
        t4 = or_(f7sn > 0, f7so > 0)
        t5 = or_(f7sr > 0, f7ss > 0)
        t6 = or_(or_(or_(f7st > 0, f7sp > 0), or_(f7sq > 0, f7sd > 0)), f7se > 0)
        bouquet = (t1 + t2 + t3 + t4 + t5 + t6 > 1)
        return period, or_(bouquet, f7wh)


class saldom2(DatedVariable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Crédit d’impôt emploi d’un salarié à domicile"

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, simulation, period):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2007-2008
        '''
        period = period.this_year
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7db = simulation.calculate('f7db', period)
        f7dg = simulation.calculate('f7dg', period)
        f7dl = simulation.calculate('f7dl', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg

        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return period, P.taux * min_(f7db, maxEffectif)

    @dated_function(start = date(2009, 1, 1), stop = date(2013, 12, 31))
    def function_20090101_20131231(self, simulation, period):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2009-2010
        '''
        period = period.this_year
        nb_pac2 = simulation.calculate('nb_pac2', period)
        f7db = simulation.calculate('f7db', period)
        f7dg = simulation.calculate('f7dg', period)
        f7dl = simulation.calculate('f7dl', period)
        f7dq = simulation.calculate('f7dq', period)
        _P = simulation.legislation_at(period.start)

        P = _P.impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg

        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return period, P.taux * min_(f7db, maxEffectif)
