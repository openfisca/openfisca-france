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
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2002 
        """
        acqgpl = foyer_fiscal("acqgpl", period)
        aidper = foyer_fiscal("aidper", period)
        creimp = foyer_fiscal("creimp", period)
        drbail = foyer_fiscal("drbail", period)
        prlire = foyer_fiscal("prlire", period)

        return acqgpl + aidper + creimp + drbail + prlire

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2003 et 2004 
        """
        acqgpl = foyer_fiscal("acqgpl", period)
        aidper = foyer_fiscal("aidper", period)
        creimp = foyer_fiscal("creimp", period)
        drbail = foyer_fiscal("drbail", period)
        prlire = foyer_fiscal("prlire", period)

        return acqgpl + aidper + creimp + drbail + prlire

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2005 et 2006 
        """
        acqgpl = foyer_fiscal("acqgpl", period)
        aidmob = foyer_fiscal("aidmob", period)
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        divide = foyer_fiscal("divide", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        jeunes = foyer_fiscal("jeunes", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)

        return (
            acqgpl
            + aidmob
            + aidper
            + assloy
            + ci_garext
            + creimp
            + divide
            + direpa
            + drbail
            + jeunes
            + preetu
            + prlire
            + quaenv
        )

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2007 
        """
        acqgpl = foyer_fiscal("acqgpl", period)
        aidmob = foyer_fiscal("aidmob", period)
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        divide = foyer_fiscal("divide", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        jeunes = foyer_fiscal("jeunes", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            acqgpl
            + aidmob
            + aidper
            + assloy
            + ci_garext
            + creimp
            + divide
            + direpa
            + drbail
            + inthab
            + jeunes
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2008 
        """
        aidmob = foyer_fiscal("aidmob", period)
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        creimp_exc_2008 = foyer_fiscal("creimp_exc_2008", period)
        divide = foyer_fiscal("divide", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        jeunes = foyer_fiscal("jeunes", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidmob
            + aidper
            + assloy
            + ci_garext
            + creimp
            + creimp_exc_2008
            + divide
            + direpa
            + drbail
            + inthab
            + jeunes
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2009 
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        divide = foyer_fiscal("divide", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + ci_garext
            + creimp
            + divide
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2010 
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        jeunes = foyer_fiscal("jeunes", period)
        percvm = foyer_fiscal("percvm", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + autent
            + ci_garext
            + creimp
            + direpa
            + drbail
            + inthab
            + percvm
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2011 
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + autent
            + ci_garext
            + creimp
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2012 
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        cotsyn = foyer_fiscal("cotsyn", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + autent
            + ci_garext
            + cotsyn
            + creimp
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2013 
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        cotsyn = foyer_fiscal("cotsyn", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + autent
            + ci_garext
            + cotsyn
            + creimp
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus de 2014 à 2016
        """
        aidper = foyer_fiscal("aidper", period)
        assloy = foyer_fiscal("assloy", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        cotsyn = foyer_fiscal("cotsyn", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + assloy
            + autent
            + ci_garext
            + cotsyn
            + creimp
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        """ 
        Crédits d'impôt pour l'impôt sur les revenus depuis 2017
        """
        aidper = foyer_fiscal("aidper", period)
        autent = foyer_fiscal("autent", period)
        ci_garext = foyer_fiscal("ci_garext", period)
        cotsyn = foyer_fiscal("cotsyn", period)
        creimp = foyer_fiscal("creimp", period)
        direpa = foyer_fiscal("direpa", period)
        drbail = foyer_fiscal("drbail", period)
        inthab = foyer_fiscal("inthab", period)
        preetu = foyer_fiscal("preetu", period)
        prlire = foyer_fiscal("prlire", period)
        quaenv = foyer_fiscal("quaenv", period)
        saldom2 = foyer_fiscal("saldom2", period)

        return (
            aidper
            + autent
            + ci_garext
            + cotsyn
            + creimp
            + direpa
            + drbail
            + inthab
            + preetu
            + prlire
            + quaenv
            + saldom2
        )


class nb_pac2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Nombre de personnes à charges (en comptant les enfants en résidence alternée comme une demi personne à charge)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbF = foyer_fiscal("nbF", period)
        nbJ = foyer_fiscal("nbJ", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbH = foyer_fiscal("nbH", period)

        return nbF + nbJ + nbpac_invalideR - nbH / 2


class acqgpl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte"
    end = "2007-12-31"
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        """
        Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
        2002-2007
        """
        f7up = foyer_fiscal("f7up", period)
        f7uq = foyer_fiscal("f7uq", period)
        acqgpl = parameters(period).impot_revenu.credits_impot.acqgpl

        return f7up * acqgpl.mont_up + f7uq * acqgpl.mont_uq


class aidmob(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité"
    end = "2008-12-31"
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        """
        Crédit d'impôt aide à la mobilité
        2005-2008
        """
        f1ar = foyer_fiscal("f1ar", period)
        f1br = foyer_fiscal("f1br", period)
        f1cr = foyer_fiscal("f1cr", period)
        f1dr = foyer_fiscal("f1dr", period)
        f1er = foyer_fiscal("f1er", period)
        montant = parameters(period).impot_revenu.credits_impot.aidmob.montant

        return (f1ar + f1br + f1cr + f1dr + f1er) * montant


class aidper(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de l’aide aux personnes"
    reference = "http://bofip.impots.gouv.fr/bofip/3859-PGP"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2002-2003
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        nbH = foyer_fiscal("nbH", period)
        f7wi = foyer_fiscal("f7wi_2012", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        n = nb_pac_majoration_plafond - nbH / 2
        max0 = (
            P.max * (1 + maries_ou_pacses)
            + P.pac1 * (n >= 1)
            + P.pac2 * (n >= 2)
            + P.pac3 * (max_(n - 2, 0))
            + (
                (n >= 2) * P.pac3 * nbH
                + (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1)) * (nbH >= 1)
                + (n == 0)
                * (
                    P.pac1
                    + (nbH > 1) * P.pac2 * (nbH - 1)
                    + (nbH > 2) * P.pac3 * (nbH - 2)
                )
                * (nbH >= 1)
            )
            / 2
        )

        return P.taux_wi * min_(f7wi, max0)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2004-2005
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        nbH = foyer_fiscal("nbH", period)
        f7wi = foyer_fiscal("f7wi_2012", period)
        f7wj = foyer_fiscal("f7wj", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        n = nb_pac_majoration_plafond - nbH / 2
        max0 = (
            P.max * (1 + maries_ou_pacses)
            + P.pac1 * (n >= 1)
            + P.pac2 * (n >= 2)
            + P.pac3 * (max_(n - 2, 0))
            + (
                (n >= 2) * P.pac3 * nbH
                + (n == 1) * (P.pac2 + (nbH > 1) * P.pac3 * (nbH - 1)) * (nbH >= 1)
                + (n == 0)
                * (
                    P.pac1
                    + (nbH > 1) * P.pac2 * (nbH - 1)
                    + (nbH > 2) * P.pac3 * (nbH - 2)
                )
                * (nbH >= 1)
            )
            / 2
        )

        max1 = max_(0, max0 - f7wj)
        return P.taux_wj * min_(f7wj, max0) + P.taux_wi * min_(f7wi, max1)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ).
        2006-2009
        cf. cerfa 50796
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wi = foyer_fiscal("f7wi_2012", period)
        f7wj = foyer_fiscal("f7wj", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)
        return P.taux_wj * min_(f7wj, max0) + P.taux_wi * min_(f7wi, max1)

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7SF, 7WI, 7WJ, 7WL).
        2010-2011
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7wi = foyer_fiscal("f7wi_2012", period)
        f7wj = foyer_fiscal("f7wj", period)
        f7wl = foyer_fiscal("f7wl", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wl - f7sf)
        max2 = max_(0, max1 - f7wj)
        return (
            P.taux_wl * min_(f7wl + f7sf, max0)
            + P.taux_wj * min_(f7wj, max1)
            + P.taux_wi * min_(f7wi, max2)
        )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL, 7WR).
        2012
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wi = foyer_fiscal("f7wi_2012", period)
        f7wj = foyer_fiscal("f7wj", period)
        f7wl = foyer_fiscal("f7wl", period)
        f7wr = foyer_fiscal("f7wr", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        # On ne contrôle pas que 7WR ne dépasse pas le plafond (dépend du nombre de logements et de la nature des travaux)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)  # f7wj s'impute avant f7wl et f7wi
        max2 = max_(0, max1 - f7wi)  # f7wi s'impute avant f7wl
        return (
            P.taux_wr * f7wr
            + +P.taux_wj * min_(f7wj, max0)
            + P.taux_wi * min_(f7wi, max1)
            + P.taux_wl * (min_(f7wl, max2) + min_(max_(0, f7wl - max2), max00))
        )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2013 - 2015
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wj = foyer_fiscal("f7wj", period)
        f7wl = foyer_fiscal("f7wl", period)
        f7wr = foyer_fiscal("f7wr", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        # On ne contrôle pas que 7WR ne dépasse pas le plafond (dépend du nombre de logements et de la nature des travaux)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)  # f7wj s'impute avant f7wl

        return (
            P.taux_wr * f7wr
            + P.taux_wj * min_(f7wj, max0)
            + P.taux_wl * (min_(f7wl, max1) + min_(max_(0, f7wl - max1), max00))
        )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
        (cases 7WI, 7WJ, 7WL).
        2015 - 
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wj = foyer_fiscal("f7wj", period)
        f7wl = foyer_fiscal("f7wl", period)
        f7wr = foyer_fiscal("f7wr", period)
        P = parameters(period).impot_revenu.credits_impot.aidper

        # On ne contrôle pas que 7WR ne dépasse pas le plafond (dépend du nombre de logements et de la nature des travaux)
        max00 = P.max * (1 + maries_ou_pacses)
        max0 = max00 + P.pac1 * nb_pac_majoration_plafond
        max1 = P.max_wl

        return (
            P.taux_wr * f7wr
            + P.taux_wj * min_(f7wj, max0)
            + P.taux_wl * min_(f7wl, max1)
        )


class assloy(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt primes d’assurance pour loyers impayés"
    reference = "http://bofip.impots.gouv.fr/bofip/844-PGP.html?identifiant=BOI-IR-RICI-320-20120912"
    definition_period = YEAR
    end = "2016-12-31"

    def formula_2005(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
        2005-2016
        """
        f4bf = foyer_fiscal("f4bf", period)
        P = parameters(period).impot_revenu.credits_impot.assloy

        return P.taux * f4bf


class autent(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"autent"
    definition_period = YEAR

    def formula_2009(foyer_fiscal, period, parameters):
        """
        Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
        2009-
        """
        f8uy = foyer_fiscal("f8uy", period)

        return f8uy


class ci_garext(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Frais de garde des enfants à l’extérieur du domicile"
    reference = "http://bofip.impots.gouv.fr/bofip/865-PGP?datePubl=13/04/2013"
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        """
        Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
        2005-
        """
        f7ga = foyer_fiscal("f7ga", period)
        f7gb = foyer_fiscal("f7gb", period)
        f7gc = foyer_fiscal("f7gc", period)
        f7ge = foyer_fiscal("f7ge", period)
        f7gf = foyer_fiscal("f7gf", period)
        f7gg = foyer_fiscal("f7gg", period)
        P = parameters(period).impot_revenu.credits_impot.garext

        max1 = P.plafond
        return P.taux * (
            min_(f7ga, max1)
            + min_(f7gb, max1)
            + min_(f7gc, max1)
            + min_(f7ge, max1 / 2)
            + min_(f7gf, max1 / 2)
            + min_(f7gg, max1 / 2)
        )


class creimp_exc_2008(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt exceptionnel sur les revenus 2008"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Crédit d'impôt exceptionnel sur les revenus 2008
        http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf
        """
        rni = foyer_fiscal("rni", period)
        nbptr = foyer_fiscal("nbptr", period)
        iai = foyer_fiscal("iai", period)
        mohist = foyer_fiscal("mohist", period)
        elig_creimp_exc_2008 = foyer_fiscal("elig_creimp_exc_2008", period)

        # TODO: gérer les DOM-TOM, corriger les formules, inclure 7KA
        rpp = rni / nbptr
        return (
            elig_creimp_exc_2008
            * (mohist < 10700)
            * (rpp <= 12475)
            * around(
                (2 / 3) * min_(12475, iai) * (rpp < 11674)
                + (rpp > 11673) * max_(0, 8317 * (12475 - rpp) / 802)
            )
        )


class creimp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Avoirs fiscaux et crédits d'impôt"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8td_2002_2005 = foyer_fiscal("f8td_2002_2005", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)

        return f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8th

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8td_2002_2005 = foyer_fiscal("f8td_2002_2005", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8td_2002_2005
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
        )

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8td_2002_2005 = foyer_fiscal("f8td_2002_2005", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8td_2002_2005
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
        )

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8td_2002_2005 = foyer_fiscal("f8td_2002_2005", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8we = foyer_fiscal("f8we", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8td_2002_2005
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8we
        )

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8ws = foyer_fiscal("f8ws", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8we
            + f8wr
            + f8ws
            + f8wt
            + f8wu
        )

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8ws = foyer_fiscal("f8ws", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)
        f8wv = foyer_fiscal("f8wv", period)
        f8wx = foyer_fiscal("f8wx", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8wr
            + f8ws
            + f8wt
            + f8wu
            + f8wv
            + f8wx
        )

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8ws = foyer_fiscal("f8ws", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)
        f8wv = foyer_fiscal("f8wv", period)
        f8wx = foyer_fiscal("f8wx", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8wr
            + f8ws
            + f8wt
            + f8wu
            + f8wv
            + f8wx
        )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8ws = foyer_fiscal("f8ws", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)
        f8wv = foyer_fiscal("f8wv", period)
        f8wx = foyer_fiscal("f8wx", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wd
            + f8we
            + f8wr
            + f8ws
            + f8wt
            + f8wu
            + f8wv
            + f8wx
        )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)
        f8wv = foyer_fiscal("f8wv", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wd
            + f8we
            + f8wr
            + f8wt
            + f8wu
            + f8wv
        )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8ts = foyer_fiscal("f8ts", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)
        f8wv = foyer_fiscal("f8wv", period)

        return (
            f2ab
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8ts
            + f8tz
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8we
            + f8wr
            + f8wt
            + f8wu
            + f8wv
        )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f2ck = foyer_fiscal("f2ck", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8tl = foyer_fiscal("f8tl", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8ts = foyer_fiscal("f8ts", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uw = foyer_fiscal("f8uw", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)

        return (
            f2ab
            + f2ck
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tl
            + f8ts
            + f8tz
            + f8uw
            + f8uz
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8we
            + f8wr
            + f8wt
            + f8wu
        )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f2ck = foyer_fiscal("f2ck", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8th = foyer_fiscal("f8th", period)
        f8tl = foyer_fiscal("f8tl", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8ts = foyer_fiscal("f8ts", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uw = foyer_fiscal("f8uw", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)

        f8vm_i = foyer_fiscal.members("f8vm", period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab
            + f2ck
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8th
            + f8to
            - f8tp
            + f8tl
            + f8ts
            + f8tz
            + f8uw
            + f8uz
            + f8vm
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8we
            + f8wr
            + f8wt
            + f8wu
        )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal("f2ab", period)
        f2ck = foyer_fiscal("f2ck", period)
        f8ta = foyer_fiscal("f8ta", period)
        f8tb = foyer_fiscal("f8tb", period)
        f8tc = foyer_fiscal("f8tc", period)
        f8te = foyer_fiscal("f8te", period)
        f8tf = foyer_fiscal("f8tf", period)
        f8tg = foyer_fiscal("f8tg", period)
        f8tl = foyer_fiscal("f8tl", period)
        f8to = foyer_fiscal("f8to", period)
        f8tp = foyer_fiscal("f8tp", period)
        f8ts = foyer_fiscal("f8ts", period)
        f8tz = foyer_fiscal("f8tz", period)
        f8uw = foyer_fiscal("f8uw", period)
        f8uz = foyer_fiscal("f8uz", period)
        f8wa = foyer_fiscal("f8wa", period)
        f8wb = foyer_fiscal("f8wb", period)
        f8wc = foyer_fiscal("f8wc", period)
        f8wd = foyer_fiscal("f8wd", period)
        f8we = foyer_fiscal("f8we", period)
        f8wr = foyer_fiscal("f8wr", period)
        f8wt = foyer_fiscal("f8wt", period)
        f8wu = foyer_fiscal("f8wu", period)

        f8vm_i = foyer_fiscal.members("f8vm", period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab
            + f2ck
            + f8ta
            + f8tb
            + f8tc
            + f8te
            - f8tf
            + f8tg
            + f8to
            - f8tp
            + f8tl
            + f8ts
            + f8tz
            + f8uw
            + f8uz
            + f8vm
            + f8wa
            + f8wb
            + f8wc
            + f8wd
            + f8we
            + f8wr
            + f8wt
            + f8wu
        )

    # TODO : add tax credit 8VM and 8VL (2016)
    # TODO: add tax credit 8TK for all years ?


class direpa(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt directive « épargne »"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt directive « épargne » (case 2BG)
        2006-
        """
        f2bg = foyer_fiscal("f2bg", period)

        return f2bg


class divide(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d'impôt dividendes"
    end = "2009-12-31"
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d'impôt dividendes
        2005-2009
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        f2dc = foyer_fiscal("f2dc", period)
        f2gr = foyer_fiscal("f2gr", period)
        P = parameters(period).impot_revenu.credits_impot.divide

        max1 = P.max * (maries_ou_pacses + 1)
        return min_(P.taux * (f2dc + f2gr), max1)


class drbail(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
        2002-
        """
        f4tq = foyer_fiscal("f4tq", period)
        P = parameters(period).impot_revenu.credits_impot.drbail

        return P.taux * f4tq


class inthab(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt intérêts des emprunts pour l’habitation principale"
    reference = u"http://bofip.impots.gouv.fr/bofip/3863-PGP.html?identifiant=BOI-IR-RICI-350-20120912"
    definition_period = YEAR

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7UH)
        2007
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        f7uh = foyer_fiscal("f7uh", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        return P.taux1 * min_(max0, f7uh)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2008
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        f7vy = foyer_fiscal("f7vy", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        max1 = max_(max0 - f7vy, 0)

        return P.taux1 * min_(f7vy, max0) + P.taux3 * min_(f7vz, max1)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2009
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vy = foyer_fiscal("f7vy", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux1 * min_(f7vy, max1)
            + P.taux3 * min_(f7vz, max2)
        )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2010
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        f7vw = foyer_fiscal("f7vw", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vy = foyer_fiscal("f7vy", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux1 * min_(f7vy, max1)
            + P.taux2 * min_(f7vw, max2)
            + P.taux3 * min_(f7vz, max3)
        )

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        f7vu = foyer_fiscal("f7vu", period)
        f7vw = foyer_fiscal("f7vw", period)
        f7vv = foyer_fiscal("f7vv", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vy = foyer_fiscal("f7vy", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux1 * min_(f7vy, max1)
            + P.taux2 * min_(f7vw, max2)
            + P.taux3 * min_(f7vu, max3)
            + P.taux4 * min_(f7vz, max4)
            + P.taux5 * min_(f7vv, max5)
        )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2012 - 2013
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbpac_invalideI = foyer_fiscal("nbI", period)
        f7vt = foyer_fiscal("f7vt", period)
        f7vu = foyer_fiscal("f7vu", period)
        f7vv = foyer_fiscal("f7vv", period)
        f7vw = foyer_fiscal("f7vw", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vy = foyer_fiscal("f7vy", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
            | (nbpac_invalideI != 0)
        )
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        max6 = max_(max5 - f7vv, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux1 * min_(f7vy, max1)
            + P.taux2 * min_(f7vw, max2)
            + P.taux3 * min_(f7vu, max3)
            + P.taux4 * min_(f7vz, max4)
            + P.taux5 * min_(f7vv, max5)
            + P.taux6 * min_(f7vt, max6)
        )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2014 
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbpac_invalideI = foyer_fiscal("nbI", period)
        f7vt = foyer_fiscal("f7vt", period)
        f7vu = foyer_fiscal("f7vu", period)
        f7vv = foyer_fiscal("f7vv", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
            | (nbpac_invalideI != 0)
        )
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vu, 0)
        max3 = max_(max2 - f7vz, 0)
        max4 = max_(max3 - f7vv, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux3 * min_(f7vu, max1)
            + P.taux4 * min_(f7vz, max2)
            + P.taux5 * min_(f7vv, max3)
            + P.taux6 * min_(f7vt, max4)
        )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2015
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbpac_invalideI = foyer_fiscal("nbI", period)
        f7vt = foyer_fiscal("f7vt", period)
        f7vv = foyer_fiscal("f7vv", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
            | (nbpac_invalideI != 0)
        )
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vz, 0)
        max3 = max_(max2 - f7vv, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux4 * min_(f7vz, max1)
            + P.taux5 * min_(f7vv, max2)
            + P.taux6 * min_(f7vt, max3)
        )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2016
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbpac_invalideI = foyer_fiscal("nbI", period)
        f7vt = foyer_fiscal("f7vt", period)
        f7vx = foyer_fiscal("f7vx", period)
        f7vz = foyer_fiscal("f7vz", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
            | (nbpac_invalideI != 0)
        )
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vz, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux4 * min_(f7vz, max1)
            + P.taux6 * min_(f7vt, max2)
        )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt intérêts des emprunts pour l’habitation principale
        2017
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        invalidite_decl = foyer_fiscal("caseP", period)
        invalidite_conj = foyer_fiscal("caseF", period)
        nbpac_invalideG = foyer_fiscal("nbG", period)
        nbpac_invalideR = foyer_fiscal("nbR", period)
        nbpac_invalideI = foyer_fiscal("nbI", period)
        f7vt = foyer_fiscal("f7vt", period)
        f7vv = foyer_fiscal("f7vv", period)
        f7vx = foyer_fiscal("f7vx", period)
        P = parameters(period).impot_revenu.credits_impot.inthab

        invalide = (
            invalidite_decl
            | invalidite_conj
            | (nbpac_invalideG != 0)
            | (nbpac_invalideR != 0)
            | (nbpac_invalideI != 0)
        )
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = (
            P.max * (maries_ou_pacses + 1) * (1 + invalide)
            + nb_pac_majoration_plafond * P.add
        )
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vv, 0)

        return (
            P.taux1 * min_(f7vx, max0)
            + P.taux5 * min_(f7vv, max1)
            + P.taux6 * min_(f7vt, max2)
        )


class jeunes(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"jeunes"
    end = "2008-12-31"
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        jeunes_ind_i = foyer_fiscal.members("jeunes_ind", period)

        return foyer_fiscal.sum(jeunes_ind_i)


class jeunes_ind(Variable):
    value_type = float
    entity = Individu
    label = u"Crédit d'impôt en faveur des jeunes"
    end = "2008-12-31"
    definition_period = YEAR

    def formula_2005_01_01(individu, period, parameters):
        """
        Crédit d'impôt en faveur des jeunes
        2005-2008

        rfr de l'année où jeune de moins de 26 à travaillé six mois
        cf. http://www3.finances.gouv.fr/calcul_impot/2009/pdf/form-2041-GY.pdf
        Attention seuls certains
        """
        janvier = period.first_month
        age = individu("age", janvier)
        salaire_imposable = individu("salaire_imposable", period, options=[ADD])
        elig_creimp_jeunes = individu("elig_creimp_jeunes", period)
        P = parameters(period).impot_revenu.credits_impot.jeunes

        # TODO: vérifier si les jeunes sous le foyer fiscal de leurs parents sont éligibles

        rfr = individu.foyer_fiscal("rfr", period)
        nbptr = individu.foyer_fiscal("nbptr", period)
        maries_ou_pacses = individu.foyer_fiscal("maries_ou_pacses", period)

        elig = (age < P.age) * (
            rfr
            < P.rfr_plaf * (maries_ou_pacses * P.rfr_mult + not_(maries_ou_pacses))
            + max_(0, nbptr - 2) * .5 * P.rfr_maj
            + (nbptr == 1.5) * P.rfr_maj
        )
        montant = (
            (P.min <= salaire_imposable) * (salaire_imposable < P.int) * P.montant
            + (P.int <= salaire_imposable)
            * (salaire_imposable <= P.max)
            * (P.max - salaire_imposable)
            * P.taux
        )
        return (
            elig_creimp_jeunes * elig * max_(25, montant)
        )  # D'après  le document num. 2041 GY

        # somme calculée sur formulaire 2041


class percvm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt pertes sur cessions de valeurs mobilières"
    end = "2010-12-31"
    definition_period = YEAR

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
        -2010
        """
        f3vv_end_2010 = foyer_fiscal("f3vv_end_2010", period)
        P = parameters(period).impot_revenu.credits_impot.percvm

        return P.taux * f3vv_end_2010


class preetu(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt pour souscription de prêts étudiants"
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2005
        """
        f7uk = foyer_fiscal("f7uk", period)
        P = parameters(period).impot_revenu.credits_impot.preetu

        return P.taux * min_(f7uk, P.max)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2006-2007
        """
        f7uk = foyer_fiscal("f7uk", period)
        f7vo = foyer_fiscal("f7vo", period)
        P = parameters(period).impot_revenu.credits_impot.preetu

        max1 = P.max * (1 + f7vo)
        return P.taux * min_(f7uk, max1)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2008-
        """
        f7uk = foyer_fiscal("f7uk", period)
        f7vo = foyer_fiscal("f7vo", period)
        f7td = foyer_fiscal("f7td", period)
        P = parameters(period).impot_revenu.credits_impot.preetu

        max1 = P.max * f7vo
        return P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)


class prlire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvement libératoire à restituer (case 2DH)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Prélèvement libératoire à restituer (case 2DH)
        2002-
        http://www2.impots.gouv.fr/documentation/2013/brochure_ir/index.html#122/z
        """
        f2dh = foyer_fiscal("f2dh", period)
        f2ch = foyer_fiscal("f2ch", period)
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        P = parameters(period)

        plaf_resid = max_(
            P.impot_revenu.rvcm.abat_assvie * (1 + maries_ou_pacses) - f2ch, 0
        )
        return P.impot_revenu.credits_impot.prlire.taux * min_(f2dh, plaf_resid)


class quaenv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale (2005 - 2014) / de la transition energétique (2014 - ) "
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH)
        2005
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wf = foyer_fiscal("f7wf", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        n = nb_pac_majoration_plafond
        max0 = (
            P.max * (1 + maries_ou_pacses)
            + P.pac1 * (n >= 1)
            + P.pac2 * (n >= 2)
            + P.pac2 * (max_(n - 2, 0))
        )

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_wg * min_(f7wg, max1)
            + P.taux_wh * min_(f7wh, max2)
        )

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WQ)
        2006-2008
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7wf = foyer_fiscal("f7wf", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wq = foyer_fiscal("f7wq", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_wg * min_(f7wg, max1)
            + P.taux_wh * min_(f7wh, max2)
            + P.taux_wq * min_(f7wq, max3)
        )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WK, 7WQ, 7SB, 7SC, 7SD, 7SE)
        2009
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7we = foyer_fiscal("f7we", period)
        f7wf = foyer_fiscal("f7wf", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wk = foyer_fiscal("f7wk", period)
        f7wq = foyer_fiscal("f7wq", period)
        f7sb = foyer_fiscal("f7sb_2011", period)
        f7sc = foyer_fiscal("f7sc_2009", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wg)
        max6 = max_(0, max5 - f7sc)
        max7 = max_(0, max6 - f7wh)
        max8 = max_(0, max7 - f7sb)

        return or_(not_(f7we), rfr < P.max_rfr) * (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_se * min_(f7se, max1)
            + P.taux_wk * min_(f7wk, max2)
            + P.taux_sd * min_(f7sd, max3)
            + P.taux_wg * min_(f7wg, max4)
            + P.taux_sc * min_(f7sc, max5)
            + P.taux_wh * min_(f7wh, max6)
            + P.taux_sb * min_(f7sb, max7)
            + P.taux_wq * min_(f7wq, max8)
        )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
        2010-2011
        """
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7we = foyer_fiscal("f7we", period)
        f7wf = foyer_fiscal("f7wf", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wk = foyer_fiscal("f7wk", period)
        f7wq = foyer_fiscal("f7wq", period)
        f7sb = foyer_fiscal("f7sb_2011", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sh = foyer_fiscal("f7sh", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wh)
        max6 = max_(0, max5 - f7sb)
        max7 = max_(0, max6 - f7wq)
        return (
            not_(f7wg)
            * or_(not_(f7we), (rfr < P.max_rfr))
            * (
                P.taux_wf * min_(f7wf, max0)
                + P.taux_se * min_(f7se, max1)
                + P.taux_wk * min_(f7wk, max2)
                + P.taux_sd * min_(f7sd, max3)
                + P.taux_wh * min_(f7wh, max4)
                + P.taux_sb * min_(f7sb, max5)
                + P.taux_wq * min_(f7wq, max6)
                + P.taux_sh * min_(f7sh, max7)
            )
        )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2012
        """
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sm = foyer_fiscal("f7sm", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7tt = foyer_fiscal("f7tt", period)
        f7tu = foyer_fiscal("f7tu", period)
        f7tv = foyer_fiscal("f7tv", period)
        f7tw = foyer_fiscal("f7tw", period)
        f7tx = foyer_fiscal("f7tx_2012", period)
        f7ty = foyer_fiscal("f7ty_2012", period)
        f7st = foyer_fiscal("f7st", period)
        f7su = foyer_fiscal("f7su", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7sz = foyer_fiscal("f7sz_2015", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7we = foyer_fiscal("f7we", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wk = foyer_fiscal("f7wk", period)
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        quaenv_bouquet = foyer_fiscal("quaenv_bouquet", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        maxi1 = max_(0, max0 - f7ty)
        maxi2 = max_(0, maxi1 - f7tx)
        maxi3 = max_(0, maxi2 - f7tw)
        maxi4 = max_(0, maxi3 - f7tv)
        maxi5 = max_(0, maxi4 - f7tu)
        collectif = (
            P.taux_ty * min_(f7ty, max0)
            + P.taux_tx * min_(f7tx, maxi1)
            + P.taux_tw * min_(f7tw, maxi2)
            + P.taux_tv * min_(f7tv, maxi3)
            + P.taux_tu * min_(f7tu, maxi4)
            + P.taux_tt * min_(f7tt, maxi5)
        )

        max1 = max_(
            0,
            max0
            - quaenv_bouquet * (f7ss + f7st)
            - not_(quaenv_bouquet) * (f7ss + f7st + f7sv),
        )
        max2 = max_(
            0,
            max1
            - quaenv_bouquet * (f7sn + f7sr + f7sq)
            - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr),
        )
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = max_(
            0,
            max3
            - quaenv_bouquet * (f7se)
            - not_(quaenv_bouquet)
            * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp),
        )
        max5 = max_(
            0,
            max4
            - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp)
            - not_(quaenv_bouquet) * (f7sm),
        )
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))
        montant = quaenv_bouquet * (
            P.taux10 * min_(max8, f7sk + f7sl)
            + P.taux11 * min_(max7, f7sm)
            + P.taux15 * min_(max6, f7sf + f7si + f7su + f7sw)
            + P.taux18 * min_(max5, f7sd + f7sj)
            + P.taux23 * min_(max4, f7sg + f7sh + f7so + f7sp)
            + P.taux26 * min_(max3, f7se)
            + P.taux32 * min_(max2, f7sv)
            + P.taux34 * min_(max1, f7sn + f7sr + f7sq)
            + P.taux40 * min_(max0, f7ss + f7st)
        ) + (
            not_(quaenv_bouquet)
            * (
                P.taux32 * min_(max0, f7ss + f7st + f7sv)
                + P.taux26 * min_(max1, f7sn + f7sq + f7sr)
                + P.taux17 * min_(max2, f7se)
                + P.taux15
                * min_(max3, f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)
                + P.taux11 * min_(max4, f7sm)
                + P.taux10 * min_(max5, f7sd + not_(f7wk) * (f7sj + f7sk + f7sl))
            )
        )
        return (
            not_(f7wg) * or_(not_(f7we), (rfr < P.max_rfr)) * (montant + collectif)
            + f7sz
        )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        """
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sm = foyer_fiscal("f7sm", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7su = foyer_fiscal("f7su", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7sz = foyer_fiscal("f7sz_2015", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7we = foyer_fiscal("f7we", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wk = foyer_fiscal("f7wk", period)
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        quaenv_bouquet = foyer_fiscal("quaenv_bouquet", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(
            0,
            max0
            - quaenv_bouquet * (f7ss + f7st)
            - not_(quaenv_bouquet) * (f7ss + f7st + f7sv),
        )
        max2 = max_(
            0,
            max1
            - quaenv_bouquet * (f7sn + f7sr + f7sq)
            - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr),
        )
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = max_(
            0,
            max3
            - quaenv_bouquet * (f7se)
            - not_(quaenv_bouquet)
            * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp),
        )
        max5 = max_(
            0,
            max4
            - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp)
            - not_(quaenv_bouquet) * (f7sm),
        )
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))

        montant = quaenv_bouquet * (
            P.taux10 * min_(max8, f7sk + f7sl)
            + P.taux11 * min_(max7, f7sm)
            + P.taux15 * min_(max6, f7sf + f7si + f7su + f7sw)
            + P.taux18 * min_(max5, f7sd + f7sj)
            + P.taux23 * min_(max4, f7sg + f7sh + f7so + f7sp)
            + P.taux26 * min_(max3, f7se)
            + P.taux32 * min_(max2, f7sv)
            + P.taux34 * min_(max1, f7sn + f7sr + f7sq)
            + P.taux40 * min_(max0, f7ss + f7st)
        ) + not_(quaenv_bouquet) * (
            +P.taux32 * min_(max0, f7ss + f7st + f7sv)
            + P.taux26 * min_(max1, f7sn + f7sq + f7sr)
            + P.taux17 * min_(max2, f7se)
            + P.taux15
            * min_(max3, f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)
            + P.taux11 * min_(max4, f7sm)
            + P.taux10 * min_(max5, f7sd + not_(f7wk) * (f7sj + f7sk + f7sl))
        )
        return (
            or_(not_(or_(f7we, f7wg)), (rfr < P.max_rfr)) * montant + f7sz
        )  # TODO : attention, la condition porte sur le RFR des années passées (N-2 et N-3)

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale (1.1-31.8.2014) et transition energétique (1.9-31.12.2014)
        2014
        """
        f7rg = foyer_fiscal("f7rg", period)
        f7rh = foyer_fiscal("f7rh", period)
        f7ri = foyer_fiscal("f7ri", period)
        f7rj = foyer_fiscal("f7rj", period)
        f7rk = foyer_fiscal("f7rk", period)
        f7rl = foyer_fiscal("f7rl", period)
        f7rn = foyer_fiscal("f7rn", period)
        f7rp = foyer_fiscal("f7rp", period)
        f7rq = foyer_fiscal("f7rq", period)
        f7rr = foyer_fiscal("f7rr", period)
        f7rs = foyer_fiscal("f7rs", period)
        f7rt = foyer_fiscal("f7rt", period)
        f7rv = foyer_fiscal("f7rv", period)
        f7rw = foyer_fiscal("f7rw", period)
        f7rz = foyer_fiscal("f7rz_2015", period)
        f7sa = foyer_fiscal("f7sa", period)
        f7sb = foyer_fiscal("f7sb", period)
        f7sc = foyer_fiscal("f7sc", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7tv = foyer_fiscal("f7tv", period)
        f7tw = foyer_fiscal("f7tw", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7vh = foyer_fiscal("f7vh", period)
        f7wb = foyer_fiscal("f7wb", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7we = foyer_fiscal("f7we", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wk = foyer_fiscal("f7wk", period)
        f7wt = foyer_fiscal("f7wt", period)
        f7wu = foyer_fiscal("f7wu", period)
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac2 = foyer_fiscal("nb_pac2", period)
        quaenv_bouquet = foyer_fiscal("quaenv_bouquet", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        depenses_transition_energetique = (
            f7sa
            + f7sb
            + f7sc
            + f7wb
            + f7rg
            + f7vh
            + f7rh
            + f7ri
            + f7wu
            + f7rj
            + f7rk
            + f7rl
            + f7rn
            + f7rp
            + f7rr
            + f7rs
            + f7rq
            + f7rt
            + f7rv
            + f7rw
            + f7rz
            + f7tv
            + f7tw
        )

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2
        max00 = max_(0, max0 - depenses_transition_energetique)
        max1 = max_(
            0,
            max00
            - quaenv_bouquet
            * (
                f7sd
                + f7se
                + f7wc
                + f7vg
                + f7wt
                + f7sn
                + f7sp
                + f7sr
                + f7ss
                + f7sq
                + f7st
            )
            - not_(quaenv_bouquet) * (max00),
        )

        credit_quaenv = quaenv_bouquet * (
            P.taux25
            * (
                min_(
                    max00,
                    f7sd
                    + f7se
                    + f7wc
                    + f7vg
                    + f7wt
                    + f7sn
                    + f7sp
                    + f7sr
                    + f7ss
                    + f7sq
                    + f7st,
                )
            )
            + P.taux15
            * min_(max1, f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw)
        ) + not_(quaenv_bouquet) * P.taux15 * (
            min_(
                max00,
                f7se
                + f7wc
                + f7vg
                + f7sn
                + f7sp
                + f7sr
                + f7ss
                + f7sq
                + f7st
                + f7sf
                + f7sg
                + f7sh
                + f7si
                + f7sv
                + f7sw
                + f7sd
                + not_(f7wk) * (f7wt + f7sj + f7sk + f7sl),
            )
        )

        # TODO: inclure la condition de non cumul éco-prêt / crédit quaenv si RFR > ... (condition complexifiée à partir de 2014)
        # TODO : inclure la condition de RFR2 (si pas de bouquet les dépenses f7s n'ouvrent aps droit à un crédit sauf si RFR < à un certain seuil)
        # TODO : inclure la condition de bouquet sur 2 périodes (si pas de bouquet avec les dépenses du 1.1 au 31.8, le bouquet peut s'apprécier
        #          sur la base des dépenses faites du 1.1 au 31.12 mais le taux sera de 25% pour la 1ère moitié de l'année et 30% l'autre)

        return P.taux30 * min_(max0, depenses_transition_energetique) + min_(
            max_(0, max0 - depenses_transition_energetique), credit_quaenv
        )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale (1.1-31.8.2014) et transition energétique (1.9.2014-31.12.2015)
        2015
        """
        f7aa = foyer_fiscal("f7aa", period)
        f7ad = foyer_fiscal("f7ad", period)
        f7af = foyer_fiscal("f7af", period)
        f7ah = foyer_fiscal("f7ah", period)
        f7ak = foyer_fiscal("f7ak", period)
        f7al = foyer_fiscal("f7al", period)
        f7am = foyer_fiscal("f7am", period)
        f7an = foyer_fiscal("f7an", period)
        f7aq = foyer_fiscal("f7aq", period)
        f7ar = foyer_fiscal("f7ar", period)
        f7av = foyer_fiscal("f7av", period)
        f7ax = foyer_fiscal("f7ax", period)
        f7ay = foyer_fiscal("f7ay", period)
        f7az = foyer_fiscal("f7az", period)
        f7bb = foyer_fiscal("f7bb", period)
        f7bc = foyer_fiscal("f7bc", period)
        f7bd = foyer_fiscal("f7bd", period)
        f7be = foyer_fiscal("f7be", period)
        f7bf = foyer_fiscal("f7bf", period)
        f7bh = foyer_fiscal("f7bh", period)
        f7bk = foyer_fiscal("f7bk", period)
        f7bl = foyer_fiscal("f7bl", period)
        f7rg = foyer_fiscal("f7rg", period)
        f7rh = foyer_fiscal("f7rh", period)
        f7ri = foyer_fiscal("f7ri", period)
        f7rj = foyer_fiscal("f7rj", period)
        f7rk = foyer_fiscal("f7rk", period)
        f7rl = foyer_fiscal("f7rl", period)
        f7rn = foyer_fiscal("f7rn", period)
        f7rp = foyer_fiscal("f7rp", period)
        f7rq = foyer_fiscal("f7rq", period)
        f7rr = foyer_fiscal("f7rr", period)
        f7rs = foyer_fiscal("f7rs", period)
        f7rt = foyer_fiscal("f7rt", period)
        f7ru = foyer_fiscal("f7ru", period)
        f7rv = foyer_fiscal("f7rv", period)
        f7rw = foyer_fiscal("f7rw", period)
        f7rz = foyer_fiscal("f7rz_2015", period)
        f7sa = foyer_fiscal("f7sa", period)
        f7sb = foyer_fiscal("f7sb", period)
        f7sc = foyer_fiscal("f7sc", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sm = foyer_fiscal("f7sm", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7su = foyer_fiscal("f7su", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7sz = foyer_fiscal("f7sz_2015", period)
        f7ta = foyer_fiscal("f7ta", period)
        f7tb = foyer_fiscal("f7tb", period)
        f7tc = foyer_fiscal("f7tc", period)
        f7tn = foyer_fiscal("f7tn", period)
        f7tp = foyer_fiscal("f7tp", period)
        f7tq = foyer_fiscal("f7tq", period)
        f7tr = foyer_fiscal("f7tr", period)
        f7ts = foyer_fiscal("f7ts", period)
        f7tt = foyer_fiscal("f7tt", period)
        f7tv = foyer_fiscal("f7tv", period)
        f7tw = foyer_fiscal("f7tw", period)
        f7tx = foyer_fiscal("f7tx_2015", period)
        f7ty = foyer_fiscal("f7ty_2015", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7vh = foyer_fiscal("f7vh", period)
        f7vi = foyer_fiscal("f7vi", period)
        f7vk = foyer_fiscal("f7vk", period)
        f7vl = foyer_fiscal("f7vl", period)
        f7wb = foyer_fiscal("f7wb", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7we = foyer_fiscal("f7we", period)
        f7wg = foyer_fiscal("f7wg", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wi = foyer_fiscal("f7wi", period)
        f7wk = foyer_fiscal("f7wk", period)
        f7wt = foyer_fiscal("f7wt", period)
        f7wu = foyer_fiscal("f7wu", period)
        f7wv = foyer_fiscal("f7wv", period)
        f7ww = foyer_fiscal("f7ww", period)
        f7xb = foyer_fiscal("f7xb", period)
        f7xc = foyer_fiscal("f7xc", period)
        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac2 = foyer_fiscal("nb_pac2", period)
        quaenv_bouquet = foyer_fiscal("quaenv_bouquet", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        depenses_transition_energetique_bouquet_2ans_2014_part2 = (
            f7sa
            + f7sb
            + f7sc
            + f7wb
            + f7rg
            + f7vh
            + f7rh
            + f7ri
            + f7wu
            + f7rj
            + f7rk
            + f7rl
            + f7rn
            + f7rp
            + f7rr
            + f7rs
            + f7rq
            + f7rt
            + f7rv
            + f7rw
            + f7rz
            + f7tv
            + f7tw
        )
        depenses_transition_energetique_bouquet_2ans_2015 = (
            f7ta
            + f7tb
            + f7tc
            + f7xb
            + f7xc
            + f7wh
            + f7wi
            + f7vi
            + f7wv
            + f7ww
            + f7vk
            + f7vl
            + f7tn
            + f7tp
            + f7tr
            + f7ts
            + f7tq
            + f7tt
            + f7tx
            + f7ty
            + f7ru
            + f7su
            + f7sm
            + f7so
            + f7sz
        )
        depenses_transition_energetique_2015 = (
            f7aa
            + f7ad
            + f7af
            + f7ah
            + f7ak
            + f7al
            + f7am
            + f7an
            + f7aq
            + f7ar
            + f7av
            + f7ax
            + f7ay
            + f7az
            + f7bb
            + f7bc
            + f7bd
            + f7be
            + f7bf
            + f7bh
            + f7bk
            + f7bl
        )
        depenses_transition_energetique = (
            depenses_transition_energetique_bouquet_2ans_2014_part2 * quaenv_bouquet
            + depenses_transition_energetique_bouquet_2ans_2015
            + depenses_transition_energetique_2015
        )

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2
        max00 = max_(0, max0 - depenses_transition_energetique)
        max1 = max_(
            0,
            max00
            - quaenv_bouquet
            * (
                f7sd
                + f7se
                + f7wc
                + f7vg
                + f7wt
                + f7sn
                + f7sp
                + f7sr
                + f7ss
                + f7sq
                + f7st
            )
            - not_(quaenv_bouquet) * (max00),
        )
        credit_quaenv_bouquet_2ans = quaenv_bouquet * (
            P.taux25
            * (
                min_(
                    max00,
                    f7sd
                    + f7se
                    + f7wc
                    + f7vg
                    + f7wt
                    + f7sn
                    + f7sp
                    + f7sr
                    + f7ss
                    + f7sq
                    + f7st,
                )
            )
            + P.taux15
            * min_(max1, f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw)
        )

        # TODO: inclure la condition de non cumul éco-prêt / crédit quaenv si RFR > ... (condition complexifiée à partir de 2014)

        return P.taux30 * min_(max0, depenses_transition_energetique) + min_(
            max_(0, max0 - depenses_transition_energetique), credit_quaenv_bouquet_2ans
        )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2016
        """
        f7aa = foyer_fiscal("f7aa", period)
        f7ad = foyer_fiscal("f7ad", period)
        f7af = foyer_fiscal("f7af", period)
        f7ah = foyer_fiscal("f7ah", period)
        f7ak = foyer_fiscal("f7ak", period)
        f7al = foyer_fiscal("f7al", period)
        f7am = foyer_fiscal("f7am", period)
        f7an = foyer_fiscal("f7an", period)
        f7aq = foyer_fiscal("f7aq", period)
        f7ar = foyer_fiscal("f7ar", period)
        f7av = foyer_fiscal("f7av", period)
        f7ax = foyer_fiscal("f7ax", period)
        f7ay = foyer_fiscal("f7ay", period)
        f7az = foyer_fiscal("f7az", period)
        f7bb = foyer_fiscal("f7bb", period)
        f7bc = foyer_fiscal("f7bc", period)
        f7bd = foyer_fiscal("f7bd", period)
        f7be = foyer_fiscal("f7be", period)
        f7bf = foyer_fiscal("f7bf", period)
        f7bh = foyer_fiscal("f7bh", period)
        f7bk = foyer_fiscal("f7bk", period)
        f7bl = foyer_fiscal("f7bl", period)
        f7bm = foyer_fiscal("f7bm", period)
        f7cb = foyer_fiscal("f7cb", period)
        f7we = foyer_fiscal("f7we", period)
        f7wg = foyer_fiscal("f7wg", period)

        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        nb_pac2 = foyer_fiscal("nb_pac2", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        depenses_transition_energetique = (
            f7aa
            + f7ad
            + f7af
            + f7ah
            + f7ak
            + f7al
            + f7am
            + f7an
            + f7aq
            + f7ar
            + f7av
            + f7ax
            + f7ay
            + f7az
            + f7bb
            + f7bc
            + f7bd
            + f7be
            + f7bf
            + f7bh
            + f7bk
            + f7bl
            + f7bm
            + f7cb
        )

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        # TODO: inclure la condition de non cumul éco-prêt / crédit quaenv si RFR > ... (condition complexifiée à partir de 2014)

        return P.taux30 * min_(max0, depenses_transition_energetique)

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        """
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2017
        """
        f7ad = foyer_fiscal("f7ad", period)
        f7af = foyer_fiscal("f7af", period)
        f7ah = foyer_fiscal("f7ah", period)
        f7ak = foyer_fiscal("f7ak", period)
        f7al = foyer_fiscal("f7al", period)
        f7am = foyer_fiscal("f7am", period)
        f7an = foyer_fiscal("f7an", period)
        f7aq = foyer_fiscal("f7aq", period)
        f7ar = foyer_fiscal("f7ar", period)
        f7av = foyer_fiscal("f7av", period)
        f7ax = foyer_fiscal("f7ax", period)
        f7ay = foyer_fiscal("f7ay", period)
        f7az = foyer_fiscal("f7az", period)
        f7bb = foyer_fiscal("f7bb", period)
        f7bc = foyer_fiscal("f7bc", period)
        f7bd = foyer_fiscal("f7bd", period)
        f7be = foyer_fiscal("f7be", period)
        f7bf = foyer_fiscal("f7bf", period)
        f7bh = foyer_fiscal("f7bh", period)
        f7bk = foyer_fiscal("f7bk", period)
        f7bl = foyer_fiscal("f7bl", period)
        f7cb = foyer_fiscal("f7cb", period)

        maries_ou_pacses = foyer_fiscal("maries_ou_pacses", period)
        personnes_a_charge = foyer_fiscal("nb_pac2", period)
        rfr = foyer_fiscal("rfr", period)
        P = parameters(period).impot_revenu.credits_impot.quaenv

        depenses_transition_energetique = (
            f7ad
            + f7af
            + f7ah
            + f7ak
            + f7al
            + f7am
            + f7an
            + f7aq
            + f7ar
            + f7av
            + f7ax
            + f7ay
            + f7az
            + f7bb
            + f7bc
            + f7bd
            + f7be
            + f7bf
            + f7bh
            + f7bk
            + f7bl
            + f7cb
        )

        plafond_depenses_energetiques = (
            P.max * (1 + maries_ou_pacses) + P.pac1 * personnes_a_charge
        )

        return P.taux30 * min_(
            plafond_depenses_energetiques, depenses_transition_energetique
        )


class quaenv_bouquet(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"Indicateur de réalisation d'un bouquet de travaux, dans le cadre du crédit d'impôt en faveur de la qualité environnementale"
    definition_period = YEAR
    reference = "http://bofip.impots.gouv.fr/bofip/3883-PGP.html?identifiant=BOI-IR-RICI-280-20170807"
    end = "2015-12-31"

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        """
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2012
        """
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7ve = foyer_fiscal("f7ve", period)
        f7vf = foyer_fiscal("f7vf", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7wa = foyer_fiscal("f7wa", period)
        f7wb = foyer_fiscal("f7wb", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7wf = foyer_fiscal("f7wf", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wq = foyer_fiscal("f7wq", period)
        f7ws = foyer_fiscal("f7ws", period)
        f7wt = foyer_fiscal("f7wt", period)

        t1 = ((f7wt * f7ws + f7wq + f7wf) > 0) * 1
        t2 = ((f7wc * f7wb + f7wa) > 0) * 1
        t3 = ((f7vg * f7vf + f7ve) > 0) * 1
        t4 = ((f7sn + f7so) > 0) * 1
        t5 = ((f7sr + f7ss) > 0) * 1
        t6 = ((f7st + f7sp + f7sq + f7sd + f7se) > 0) * 1
        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (f7wh == 1)
        return bouquet

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2013
        """
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7so = foyer_fiscal("f7so", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wt = foyer_fiscal("f7wt", period)

        t1 = f7wt
        t2 = f7wc
        t3 = f7vg
        t4 = ((f7sn + f7so) > 0) * 1
        t5 = ((f7sr + f7ss) > 0) * 1
        t6 = ((f7st + f7sp + f7sq + f7sd + f7se) > 0) * 1
        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (f7wh == 1)
        return bouquet

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        """
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2014
        """
        f7rn = foyer_fiscal("f7rn", period)
        f7rp = foyer_fiscal("f7rp", period)
        f7rq = foyer_fiscal("f7rq", period)
        f7rr = foyer_fiscal("f7rr", period)
        f7rs = foyer_fiscal("f7rs", period)
        f7rt = foyer_fiscal("f7rt", period)
        f7sa = foyer_fiscal("f7sa", period)
        f7sb = foyer_fiscal("f7sb", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7vh = foyer_fiscal("f7vh", period)
        f7wb = foyer_fiscal("f7wb", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7wt = foyer_fiscal("f7wt", period)
        f7wu = foyer_fiscal("f7wu", period)

        depense_2014_eligible = (
            f7sd
            + f7se
            + f7wc
            + f7vg
            + f7wt
            + f7sn
            + f7sp
            + f7sr
            + f7ss
            + f7sq
            + f7st
            + f7sf
            + f7sg
            + f7sh
            + f7si
            + f7sj
            + f7sk
            + f7sl
            + f7sv
            + f7sw
        )
        t1 = ((f7wt + f7wu) > 0) * 1
        t2 = ((f7wc + f7wb) > 0) * 1
        t3 = ((f7vg + f7vh) > 0) * 1
        t4 = ((f7sn + f7rn) > 0) * 1
        t5 = ((f7sr + f7rr + f7ss + f7rs) > 0) * 1
        t6 = (
            (f7sd + f7sa + f7se + f7sb + f7sp + f7rp + f7sq + f7rq + f7st + f7rt) > 0
        ) * 1

        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (depense_2014_eligible > 0)
        return bouquet

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        """
        Les dépenses de travaux dépendent d'un bouquet de travaux (sur 2 ans)
        2015
        """
        f7rn = foyer_fiscal("f7rn", period)
        f7rp = foyer_fiscal("f7rp", period)
        f7rq = foyer_fiscal("f7rq", period)
        f7rr = foyer_fiscal("f7rr", period)
        f7rs = foyer_fiscal("f7rs", period)
        f7rt = foyer_fiscal("f7rt", period)
        f7sa = foyer_fiscal("f7sa", period)
        f7sb = foyer_fiscal("f7sb", period)
        f7sd = foyer_fiscal("f7sd", period)
        f7se = foyer_fiscal("f7se", period)
        f7sf = foyer_fiscal("f7sf", period)
        f7sg = foyer_fiscal("f7sg", period)
        f7sh = foyer_fiscal("f7sh", period)
        f7si = foyer_fiscal("f7si", period)
        f7sj = foyer_fiscal("f7sj", period)
        f7sk = foyer_fiscal("f7sk", period)
        f7sl = foyer_fiscal("f7sl", period)
        f7sn = foyer_fiscal("f7sn", period)
        f7sp = foyer_fiscal("f7sp", period)
        f7sq = foyer_fiscal("f7sq", period)
        f7sr = foyer_fiscal("f7sr", period)
        f7ss = foyer_fiscal("f7ss", period)
        f7st = foyer_fiscal("f7st", period)
        f7sv = foyer_fiscal("f7sv", period)
        f7sw = foyer_fiscal("f7sw", period)
        f7ta = foyer_fiscal("f7ta", period)
        f7tb = foyer_fiscal("f7tb", period)
        f7tn = foyer_fiscal("f7tn", period)
        f7tp = foyer_fiscal("f7tp", period)
        f7tq = foyer_fiscal("f7tq", period)
        f7tr = foyer_fiscal("f7tr", period)
        f7ts = foyer_fiscal("f7ts", period)
        f7tt = foyer_fiscal("f7tt", period)
        f7vg = foyer_fiscal("f7vg", period)
        f7vh = foyer_fiscal("f7vh", period)
        f7wb = foyer_fiscal("f7wb", period)
        f7wc = foyer_fiscal("f7wc", period)
        f7wh = foyer_fiscal("f7wh", period)
        f7wt = foyer_fiscal("f7wt", period)
        f7wu = foyer_fiscal("f7wu", period)
        f7wv = foyer_fiscal("f7wv", period)
        f7xb = foyer_fiscal("f7xb", period)

        depense_2014_eligible = (
            f7sd
            + f7se
            + f7wc
            + f7vg
            + f7wt
            + f7sn
            + f7sp
            + f7sr
            + f7ss
            + f7sq
            + f7st
            + f7sf
            + f7sg
            + f7sh
            + f7si
            + f7sj
            + f7sk
            + f7sl
            + f7sv
            + f7sw
        )
        depense_2015_eligible = (
            f7ta + f7tb + f7xb + f7wh + f7wv + f7tn + f7tp + f7tr + f7ts + f7tq + f7tt
        )

        t1 = ((f7wt + f7wu + f7wv) > 0) * 1
        t2 = ((f7wc + f7wb + f7xb) > 0) * 1
        t3 = ((f7vg + f7vh + f7wh) > 0) * 1
        t4 = ((f7sn + f7rn + f7tn) > 0) * 1
        t5 = ((f7sr + f7rr + f7tr + f7ss + f7rs + f7ts) > 0) * 1
        t6 = (
            (
                f7sd
                + f7sa
                + f7ta
                + f7se
                + f7sb
                + f7tb
                + f7sp
                + f7rp
                + f7tp
                + f7sq
                + f7rq
                + f7tq
                + f7st
                + f7rt
                + f7tt
            )
            > 0
        ) * 1

        bouquet = (
            ((t1 + t2 + t3 + t4 + t5 + t6) > 1)
            * (depense_2014_eligible > 0)
            * (depense_2015_eligible > 0)
        )
        return bouquet


class saldom2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Crédit d’impôt emploi d’un salarié à domicile"
    definition_period = YEAR

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2007-2008
        """
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7db = foyer_fiscal("f7db", period)
        f7dg = foyer_fiscal("f7dg", period)
        f7dl = foyer_fiscal("f7dl", period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        nbpacmin = nb_pac_majoration_plafond + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2009-
        """
        nb_pac_majoration_plafond = foyer_fiscal("nb_pac2", period)
        f7db = foyer_fiscal("f7db", period)
        f7dg = foyer_fiscal("f7dg", period)
        f7dl = foyer_fiscal("f7dl", period)
        f7dq = foyer_fiscal("f7dq", period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        annee1 = f7dq
        nbpacmin = nb_pac_majoration_plafond + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_premiere_annee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_premiere_annee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid

        return P.taux * min_(f7db, maxEffectif)
