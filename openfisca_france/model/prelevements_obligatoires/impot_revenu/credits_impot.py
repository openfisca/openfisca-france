# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import around, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)


class credits_impot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédits d'impôt pour l'impôt sur les revenus"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2002 """
        accult = foyer_fiscal('accult', period)
        acqgpl = foyer_fiscal('acqgpl', period)
        aidper = foyer_fiscal('aidper', period)
        creimp = foyer_fiscal('creimp', period)
        drbail = foyer_fiscal('drbail', period)
        prlire = foyer_fiscal('prlire', period)

        return accult + acqgpl + aidper + creimp + drbail + prlire

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2003 et 2004 """
        accult = foyer_fiscal('accult', period)
        acqgpl = foyer_fiscal('acqgpl', period)
        aidper = foyer_fiscal('aidper', period)
        creimp = foyer_fiscal('creimp', period)
        drbail = foyer_fiscal('drbail', period)
        mecena = foyer_fiscal('mecena', period)
        prlire = foyer_fiscal('prlire', period)

        return accult + acqgpl + aidper + creimp + drbail + mecena + prlire

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2005 et 2006 """
        accult = foyer_fiscal('accult', period)
        acqgpl = foyer_fiscal('acqgpl', period)
        aidmob = foyer_fiscal('aidmob', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        divide = foyer_fiscal('divide', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        jeunes = foyer_fiscal('jeunes', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)

        return (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + jeunes +
                mecena + preetu + prlire + quaenv)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2007 """
        accult = foyer_fiscal('accult', period)
        acqgpl = foyer_fiscal('acqgpl', period)
        aidmob = foyer_fiscal('aidmob', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        divide = foyer_fiscal('divide', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        jeunes = foyer_fiscal('jeunes', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + acqgpl + aidmob + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab +
                jeunes + mecena + preetu + prlire + quaenv + saldom2)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2008 """
        accult = foyer_fiscal('accult', period)
        aidmob = foyer_fiscal('aidmob', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        creimp_exc_2008 = foyer_fiscal('creimp_exc_2008', period)
        divide = foyer_fiscal('divide', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        jeunes = foyer_fiscal('jeunes', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidmob + aidper + assloy + ci_garext + creimp + creimp_exc_2008 + divide + direpa + drbail +
                inthab + jeunes + mecena + preetu + prlire + quaenv + saldom2)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2009 """
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        divide = foyer_fiscal('divide', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + ci_garext + creimp + divide + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2010 """
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        autent = foyer_fiscal('autent', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        jeunes = foyer_fiscal('jeunes', period)
        mecena = foyer_fiscal('mecena', period)
        percvm = foyer_fiscal('percvm', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + percvm +
                preetu + prlire + quaenv + saldom2)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2011 """
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        autent = foyer_fiscal('autent', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        creimp = foyer_fiscal('creimp', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + autent + ci_garext + creimp + direpa + drbail + inthab + mecena + preetu +
                prlire + quaenv + saldom2)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt pour l'impôt sur les revenus de 2012 """
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        autent = foyer_fiscal('autent', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creimp = foyer_fiscal('creimp', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt crédités l'impôt sur les revenus de 2013 """
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        autent = foyer_fiscal('autent', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creimp = foyer_fiscal('creimp', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)

    # Not checked
    def formula_2014_01_01(foyer_fiscal, period, parameters):
        """ Crédits d'impôt crédités l'impôt sur les revenus de 2014 et + (non vérifié)"""
        accult = foyer_fiscal('accult', period)
        aidper = foyer_fiscal('aidper', period)
        assloy = foyer_fiscal('assloy', period)
        autent = foyer_fiscal('autent', period)
        ci_garext = foyer_fiscal('ci_garext', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creimp = foyer_fiscal('creimp', period)
        direpa = foyer_fiscal('direpa', period)
        drbail = foyer_fiscal('drbail', period)
        inthab = foyer_fiscal('inthab', period)
        mecena = foyer_fiscal('mecena', period)
        preetu = foyer_fiscal('preetu', period)
        prlire = foyer_fiscal('prlire', period)
        quaenv = foyer_fiscal('quaenv', period)
        saldom2 = foyer_fiscal('saldom2', period)

        return (accult + aidper + assloy + autent + ci_garext + cotsyn + creimp + direpa + drbail + inthab + mecena +
                preetu + prlire + quaenv + saldom2)


class nb_pac2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"nb_pac2"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbF = foyer_fiscal('nbF', period)
        nbJ = foyer_fiscal('nbJ', period)
        nbR = foyer_fiscal('nbR', period)
        nbH = foyer_fiscal('nbH', period)

        return nbF + nbJ + nbR - nbH / 2


class accult(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Acquisition de biens culturels"
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Acquisition de biens culturels (case 7UO)
        2002-
        '''
        f7uo = foyer_fiscal('f7uo', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.accult
        return P.taux * f7uo


class acqgpl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte"
    end = '2007-12-31'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
        2002-2007
        '''
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        acqgpl = parameters(period).impot_revenu.credits_impot.acqgpl

        return f7up * acqgpl.mont_up + f7uq * acqgpl.mont_uq


class aidmob(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt aide à la mobilité
        2005-2008
        '''
        f1ar = foyer_fiscal('f1ar', period)
        f1br = foyer_fiscal('f1br', period)
        f1cr = foyer_fiscal('f1cr', period)
        f1dr = foyer_fiscal('f1dr', period)
        f1er = foyer_fiscal('f1er', period)
        _P = parameters(period)

        return (f1ar + f1br + f1cr + f1dr + f1er) * _P.impot_revenu.credits_impot.aidmob.montant


class aidper(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de l’aide aux personnes"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2002-2003
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        nbH = foyer_fiscal('nbH', period)
        f7wi = foyer_fiscal('f7wi', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper

        n = nb_pac2 - nbH / 2
        max0 = (P.max * (1 + maries_ou_pacses) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        return P.taux_wi * min_(f7wi, max0)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2004-2005
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        nbH = foyer_fiscal('nbH', period)
        f7wi = foyer_fiscal('f7wi', period)
        f7wj = foyer_fiscal('f7wj', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper

        n = nb_pac2 - nbH/2
        max0 = (P.max * (1 + maries_ou_pacses) +
            P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac3 * (max_(n - 2, 0)) +
            ((n >= 2) * P.pac3 * nbH +
            (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1) ) * (nbH >= 1) +
            (n == 0) * (P.pac1 + (nbH > 1) * P.pac2 * (nbH - 1) + (nbH > 2) * P.pac3 * (nbH - 2)) * (nbH >= 1)) / 2)

        max1 = max_(0, max0 - f7wj)
        return (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2006-2009
        cf. cerfa 50796
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wi = foyer_fiscal('f7wi', period)
        f7wj = foyer_fiscal('f7wj', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wj)
        return (P.taux_wj * min_(f7wj, max0) +
                    P.taux_wi * min_(f7wi, max1))

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7SF, 7WI, 7WJ, 7WL).
        2010-2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7sf = foyer_fiscal('f7sf', period)
        f7wi = foyer_fiscal('f7wi', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        _P = parameters(period)


        P = _P.impot_revenu.credits_impot.aidper
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wl - f7sf)
        max2 = max_(0, max1 - f7wj)
        return P.taux_wl * min_(f7wl+f7sf, max0) + P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL, 7WR).
        2012
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wi = foyer_fiscal('f7wi', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements (7sa) et de la nature des
        #travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0,f7wl-max00))
        max2 = max_(0, max1 - f7wj)
        return (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) +
                P.taux_wj * min_(f7wj, max1)  + P.taux_wi * min_(f7wi, max2))

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements et de la nature des
        # travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0, f7wl - max00))

        return (P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) + P.taux_wj *
                min_(f7wj, max1))

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2014 et supérieurs non vérifiée
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.aidper
        # On ne contrôle pas que 7WR ne dépasse pas le plafond (ça dépend du nombre de logements et de la nature des
        # travaux, c'est un peu le bordel)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac2
        max1 = max_(0, max0 - max_(0, f7wl - max00))

        return (
            P.taux_wr * f7wr + P.taux_wl * min_(f7wl, max00) + P.taux_wl * max_(f7wl - max00, 0) +
            P.taux_wj * min_(f7wj, max1)
            )


class assloy(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt primes d’assurance pour loyers impayés"
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
        2005-
        '''
        f4bf = foyer_fiscal('f4bf', period)
        _P = parameters(period)

        return _P.impot_revenu.credits_impot.assloy.taux * f4bf


class autent(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"autent"
    definition_period = YEAR

    def formula_2009(foyer_fiscal, period, parameters):
        '''
        Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
        2009-
        '''
        f8uy = foyer_fiscal('f8uy', period)

        return f8uy


class ci_garext(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Frais de garde des enfants à l’extérieur du domicile"
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
        2005-
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        f7ge = foyer_fiscal('f7ge', period)
        f7gf = foyer_fiscal('f7gf', period)
        f7gg = foyer_fiscal('f7gg', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.garext
        max1 = P.plafond
        return P.taux * (min_(f7ga, max1) +
                              min_(f7gb, max1) +
                              min_(f7gc, max1) +
                              min_(f7ge, max1 / 2) +
                              min_(f7gf, max1 / 2) +
                              min_(f7gg, max1 / 2))


class creimp_exc_2008(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt exceptionnel sur les revenus 2008"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt exceptionnel sur les revenus 2008
        http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf
        '''
        rni = foyer_fiscal('rni', period)
        nbptr = foyer_fiscal('nbptr', period)
        iai = foyer_fiscal('iai', period)
        mohist = foyer_fiscal('mohist', period)
        elig_creimp_exc_2008 = foyer_fiscal('elig_creimp_exc_2008', period)

        #TODO: gérer les DOM-TOM, corriger les formules, inclure 7KA
        rpp = rni / nbptr
        return (elig_creimp_exc_2008 * (mohist < 10700) * (rpp <= 12475) * around((2/3) * min_(12475, iai) * (rpp < 11674) +
                (rpp > 11673) * max_(0, 8317 * (12475 - rpp) / 802)))


class creimp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Avoirs fiscaux et crédits d'impôt"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8we = foyer_fiscal('f8we', period)

        return  (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa +
                f8wb + f8wc + f8we)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8we + f8wr + f8ws + f8wt + f8wu)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return  (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc +
                f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return  (f2ab + f8ta + f8tb + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
                f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)

        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd +
        f8we + f8wr + f8wt + f8wu + f8wv)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)

        return (f2ab + f8ta + f8tb + f8tc +f8te - f8tf + f8tg + f8th + f8to - f8tp + f8ts + f8tz + f8uz + f8wa + f8wb +
                f8wd + f8we + f8wr + f8wt + f8wu + f8wv)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f2ck = foyer_fiscal('f2ck', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8th = foyer_fiscal('f8th', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        return (f2ab + f2ck + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8tl + f8ts + f8tz + f8uw +
                f8uz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8wt + f8wu)


class direpa(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt directive « épargne »"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt directive « épargne » (case 2BG)
        2006-
        '''
        f2bg = foyer_fiscal('f2bg', period)

        return f2bg


class divide(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt dividendes"
    end = '2009-12-31'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt dividendes
        2005-2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2gr = foyer_fiscal('f2gr', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.divide

        max1 = P.max * (maries_ou_pacses + 1)
        return min_(P.taux * (f2dc + f2gr), max1)


class drbail(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
        2002-
        '''
        f4tq = foyer_fiscal('f4tq', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.drbail
        return P.taux * f4tq


class inthab(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt intérêts des emprunts pour l’habitation principale"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7UH)
        2007
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7uh = foyer_fiscal('f7uh', period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add
        return P.taux1 * min_(max0, f7uh)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vy, 0)
        return (P.taux1 * min_(f7vy, max0) +
                    P.taux3 * min_(f7vz, max1))

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux3 * min_(f7vz, max2))

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        return (P.taux1 * min_(f7vx, max0) +
                    P.taux1 * min_(f7vy, max1) +
                    P.taux2 * min_(f7vw, max2) +
                    P.taux3 * min_(f7vz, max3))

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7vu = foyer_fiscal('f7vu', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

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

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        caseP = foyer_fiscal('caseP', period)
        caseF = foyer_fiscal('caseF', period)
        nbG = foyer_fiscal('nbG', period)
        nbR = foyer_fiscal('nbR', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vu = foyer_fiscal('f7vu', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.inthab

        invalide = caseP | caseF | (nbG != 0) | (nbR != 0)
        max0 = P.max * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac2 * P.add

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


class jeunes(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"jeunes"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        jeunes_ind_i = foyer_fiscal.members('jeunes_ind', period)

        return foyer_fiscal.sum(jeunes_ind_i)


class jeunes_ind(Variable):
    value_type = float
    entity = Individu
    label = u"Crédit d'impôt en faveur des jeunes"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005_01_01(individu, period, parameters):
        '''
        Crédit d'impôt en faveur des jeunes
        2005-2008

        rfr de l'année où jeune de moins de 26 à travaillé six mois
        cf. http://www3.finances.gouv.fr/calcul_impot/2009/pdf/form-2041-GY.pdf
        Attention seuls certains
        '''
        janvier = period.first_month
        age = individu('age', janvier)
        salaire_imposable = individu('salaire_imposable', period, options = [ADD])
        elig_creimp_jeunes = individu('elig_creimp_jeunes', period)
        P = parameters(period).impot_revenu.credits_impot.jeunes

        #TODO: vérifier si les jeunes sous le foyer fiscal de leurs parents sont éligibles

        rfr = individu.foyer_fiscal('rfr', period)
        nbptr = individu.foyer_fiscal('nbptr', period)
        maries_ou_pacses = individu.foyer_fiscal('maries_ou_pacses', period)

        elig = (age < P.age) * (rfr < P.rfr_plaf * (maries_ou_pacses * P.rfr_mult + not_(maries_ou_pacses)) + max_(0, nbptr - 2) * .5 *
                P.rfr_maj + (nbptr == 1.5) * P.rfr_maj)
        montant = (
            (P.min <= salaire_imposable) * (salaire_imposable < P.int) * P.montant +
            (P.int <= salaire_imposable) * (salaire_imposable <= P.max) * (P.max - salaire_imposable) * P.taux
            )
        return elig_creimp_jeunes * elig * max_(25, montant)  # D'après  le document num. 2041 GY


                                # somme calculée sur formulaire 2041


class mecena(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Mécénat d'entreprise"
    definition_period = YEAR

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Mécénat d'entreprise (case 7US)
        2003-
        '''
        f7us = foyer_fiscal('f7us', period)

        return f7us


class percvm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt pertes sur cessions de valeurs mobilières"
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
        -2010
        '''
        f3vv_end_2010 = foyer_fiscal('f3vv_end_2010', period)
        _P = parameters(period)

        return _P.impot_revenu.credits_impot.percvm.taux * f3vv_end_2010


class preetu(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt pour souscription de prêts étudiants"
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2005
        '''
        f7uk = foyer_fiscal('f7uk', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.preetu

        return P.taux * min_(f7uk, P.max)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2006-2007
        '''
        f7uk = foyer_fiscal('f7uk', period)
        f7vo = foyer_fiscal('f7vo', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.preetu

        max1 = P.max * (1 + f7vo)
        return P.taux * min_(f7uk, max1)

    # Cette formule a seulement été vérifiée jusqu'au 2015-12-31
    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2008-
        '''
        f7uk = foyer_fiscal('f7uk', period)
        f7vo = foyer_fiscal('f7vo', period)
        f7td = foyer_fiscal('f7td', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.preetu

        max1 = P.max * f7vo
        return P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)


class prlire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvement libératoire à restituer (case 2DH)"
    end = '2013-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Prélèvement libératoire à restituer (case 2DH)
        2002-
        http://www2.impots.gouv.fr/documentation/2013/brochure_ir/index.html#122/z
        '''
        f2dh = foyer_fiscal('f2dh', period)
        f2ch = foyer_fiscal('f2ch', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        _P = parameters(period)

        plaf_resid = max_(_P.impot_revenu.rvcm.abat_assvie * (1 + maries_ou_pacses) - f2ch, 0)
        return _P.impot_revenu.credits_impot.prlire.taux * min_(f2dh, plaf_resid)


class quaenv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH)
        2005
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wf = foyer_fiscal('f7wf', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.quaenv

        n = nb_pac2
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return (P.taux_wf * min_(f7wf, max0) +
            P.taux_wg * min_(f7wg, max1) +
            P.taux_wh * min_(f7wh, max2))

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WQ)
        2006-2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7wf = foyer_fiscal('f7wf', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wq = foyer_fiscal('f7wq', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return (P.taux_wf * min_(f7wf, max0) +
                    P.taux_wg * min_(f7wg, max1) +
                    P.taux_wh * min_(f7wh, max2) +
                    P.taux_wq * min_(f7wq, max3))

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WK, 7WQ, 7SB, 7SC, 7SD, 7SE)
        2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7we = foyer_fiscal('f7we', period)
        f7wf = foyer_fiscal('f7wf', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7sb = foyer_fiscal('f7sb', period)
        f7sc = foyer_fiscal('f7sc', period)
        f7sd = foyer_fiscal('f7sd', period)
        f7se = foyer_fiscal('f7se', period)
        rfr = foyer_fiscal('rfr', period)
        _P = parameters(period)

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

        return or_(not_(f7we), rfr < 45000) * (P.taux_wf * min_(f7wf, max0) +
                    P.taux_se * min_(f7se, max1) +
                    P.taux_wk * min_(f7wk, max2) +
                    P.taux_sd * min_(f7sd, max3) +
                    P.taux_wg * min_(f7wg, max4) +
                    P.taux_sc * min_(f7sc, max5) +
                    P.taux_wh * min_(f7wh, max6) +
                    P.taux_sb * min_(f7sb, max7) +
                    P.taux_wq * min_(f7wq, max8))

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
        2010-2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7we = foyer_fiscal('f7we', period)
        f7wf = foyer_fiscal('f7wf', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7sb = foyer_fiscal('f7sb', period)
        f7sd = foyer_fiscal('f7sd', period)
        f7se = foyer_fiscal('f7se', period)
        f7sh = foyer_fiscal('f7sh', period)
        rfr = foyer_fiscal('rfr', period)
        _P = parameters(period)

        P = _P.impot_revenu.credits_impot.quaenv
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

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
            P.taux_sh * min_(f7sh, max7)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2012
        '''
        f7sd = foyer_fiscal('f7sd', period)
        f7se = foyer_fiscal('f7se', period)
        f7sf = foyer_fiscal('f7sf', period)
        f7sg = foyer_fiscal('f7sg', period)
        f7sh = foyer_fiscal('f7sh', period)
        f7si = foyer_fiscal('f7si', period)
        f7sj = foyer_fiscal('f7sj', period)
        f7sk = foyer_fiscal('f7sk', period)
        f7sl = foyer_fiscal('f7sl', period)
        f7sm = foyer_fiscal('f7sm', period)
        f7sn = foyer_fiscal('f7sn', period)
        f7so = foyer_fiscal('f7so', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq', period)
        f7sr = foyer_fiscal('f7sr', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7tt = foyer_fiscal('f7tt', period)
        f7tu = foyer_fiscal('f7tu', period)
        f7tv = foyer_fiscal('f7tv', period)
        f7tw = foyer_fiscal('f7tw', period)
        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)
        f7st = foyer_fiscal('f7st', period)
        f7su = foyer_fiscal('f7su', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7sz = foyer_fiscal('f7sz', period)
        f7wc = foyer_fiscal('f7wc', period)
        f7we = foyer_fiscal('f7we', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

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
        return not_(f7wg) * or_(not_(f7we), (rfr < 30000)) * (montant + collectif) + f7sz

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        '''
        f7sd = foyer_fiscal('f7sd', period)
        f7se = foyer_fiscal('f7se', period)
        f7sf = foyer_fiscal('f7sf', period)
        f7sg = foyer_fiscal('f7sg', period)
        f7sh = foyer_fiscal('f7sh', period)
        f7si = foyer_fiscal('f7si', period)
        f7sj = foyer_fiscal('f7sj', period)
        f7sk = foyer_fiscal('f7sk', period)
        f7sl = foyer_fiscal('f7sl', period)
        f7sm = foyer_fiscal('f7sm', period)
        f7sn = foyer_fiscal('f7sn', period)
        f7so = foyer_fiscal('f7so', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq', period)
        f7sr = foyer_fiscal('f7sr', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7su = foyer_fiscal('f7su', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7sz = foyer_fiscal('f7sz', period)
        f7wc = foyer_fiscal('f7wc', period)
        f7we = foyer_fiscal('f7we', period)
        f7wg = foyer_fiscal('f7wg', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

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
        return or_(not_(or_(f7we, f7wg)), (rfr < 30000)) * montant + f7sz


class quaenv_bouquet(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"quaenv_bouquet"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2013
        '''
        f7sd = foyer_fiscal('f7sd', period)
        f7se = foyer_fiscal('f7se', period)
        f7sn = foyer_fiscal('f7sn', period)
        f7so = foyer_fiscal('f7so', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq', period)
        f7sr = foyer_fiscal('f7sr', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7ve = foyer_fiscal('f7ve', period)
        f7vf = foyer_fiscal('f7vf', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7wa = foyer_fiscal('f7wa', period)
        f7wb = foyer_fiscal('f7wb', period)
        f7wc = foyer_fiscal('f7wc', period)
        f7wf = foyer_fiscal('f7wf', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7ws = foyer_fiscal('f7ws', period)
        f7wt = foyer_fiscal('f7wt', period)

        t1 = or_(or_(f7wt * f7ws, f7wq), f7wf)
        t2 = or_(f7wc * f7wb, f7wa)
        t3 = or_(f7vg * f7vf, f7ve)
        t4 = or_(f7sn > 0, f7so > 0)
        t5 = or_(f7sr > 0, f7ss > 0)
        t6 = or_(or_(or_(f7st > 0, f7sp > 0), or_(f7sq > 0, f7sd > 0)), f7se > 0)
        bouquet = (t1 + t2 + t3 + t4 + t5 + t6 > 1)
        return or_(bouquet, f7wh)


class saldom2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt emploi d’un salarié à domicile"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2007-2008
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7dg = foyer_fiscal('f7dg', period)
        f7dl = foyer_fiscal('f7dl', period)
        _P = parameters(period)

        P = _P.impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg

        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2009-2010
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7dg = foyer_fiscal('f7dg', period)
        f7dl = foyer_fiscal('f7dl', period)
        f7dq = foyer_fiscal('f7dq', period)
        _P = parameters(period)

        P = _P.impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg

        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)
