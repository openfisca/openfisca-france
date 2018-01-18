# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import around

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


class reductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"reductions"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2002
        '''
        adhcga = foyer_fiscal('adhcga', period)
        assvie = foyer_fiscal('assvie', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        dfppce = foyer_fiscal('dfppce', period)
        daepad = foyer_fiscal('daepad', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        garext = foyer_fiscal('garext', period)
        intemp = foyer_fiscal('intemp', period)
        invfor = foyer_fiscal('invfor', period)
        invrev = foyer_fiscal('invrev', period)
        ip_net = foyer_fiscal('ip_net', period)
        prcomp = foyer_fiscal('prcomp', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + assvie + cappme + cotsyn + dfppce + daepad + doment + domlog + donapd + ecpess +
                garext + intemp + invfor + invrev + prcomp + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2003 et 2004
        '''
        adhcga = foyer_fiscal('adhcga', period)
        assvie = foyer_fiscal('assvie', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        dfppce = foyer_fiscal('dfppce', period)
        daepad = foyer_fiscal('daepad', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        garext = foyer_fiscal('garext', period)
        intemp = foyer_fiscal('intemp', period)
        invfor = foyer_fiscal('invfor', period)
        invrev = foyer_fiscal('invrev', period)
        ip_net = foyer_fiscal('ip_net', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + assvie + cappme + cotsyn + dfppce + daepad + doment + domlog + donapd + ecpess +
                garext + intemp + invfor + invrev + prcomp + repsoc + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2005
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        daepad = foyer_fiscal('daepad', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        intcon = foyer_fiscal('intcon', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + daepad + dfppce + doment + domlog + donapd + ecpess + intagr +
                intcon + invfor + invlst + prcomp + repsoc + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2006
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2007
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)

        return min_(ip_net, total_reductions)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2008
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        mohist = foyer_fiscal('mohist', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + mohist + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2009
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        domsoc = foyer_fiscal('domsoc', period)
        donapd = foyer_fiscal('donapd', period)
        ecodev = foyer_fiscal('ecodev', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mohist = foyer_fiscal('mohist', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        sofipe = foyer_fiscal('sofipe', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecodev + ecpess + intagr + invfor + invlst + locmeu + mohist + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)
        return min_(ip_net, total_reductions)

    # TODO: check (sees checked) and report in Niches.xls
    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2010
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        domsoc = foyer_fiscal('domsoc', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mohist = foyer_fiscal('mohist', period)
        patnat = foyer_fiscal('patnat', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        sofipe = foyer_fiscal('sofipe', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)  # TODO: check (sees checked) and report in Niches.xls
        return min_(ip_net, total_reductions)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2011
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        cotsyn = foyer_fiscal('cotsyn', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        domsoc = foyer_fiscal('domsoc', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mohist = foyer_fiscal('mohist', period)
        patnat = foyer_fiscal('patnat', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        sofipe = foyer_fiscal('sofipe', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2012
        '''
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        domsoc = foyer_fiscal('domsoc', period)
        donapd = foyer_fiscal('donapd', period)
        ecpess = foyer_fiscal('ecpess', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mohist = foyer_fiscal('mohist', period)
        patnat = foyer_fiscal('patnat', period)
        prcomp = foyer_fiscal('prcomp', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2013
        '''
        accult = foyer_fiscal('accult', period)
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        duflot = foyer_fiscal('duflot', period)
        ecpess = foyer_fiscal('ecpess', period)
        garext = foyer_fiscal('garext', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mecena = foyer_fiscal('mecena', period)
        mohist = foyer_fiscal('mohist', period)
        patnat = foyer_fiscal('patnat', period)
        prcomp = foyer_fiscal('prcomp', period)
        reduction_impot_exceptionnelle = foyer_fiscal('reduction_impot_exceptionnelle', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist +
        patnat + prcomp + reduction_impot_exceptionnelle + repsoc + resimm + rsceha + saldom + scelli + sofica +
        spfcpi)
        return min_(ip_net, total_reductions)

    # Start date not checked
    def formula_2014(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2014 et + (non vérifiée)
        '''
        accult = foyer_fiscal('accult', period)
        adhcga = foyer_fiscal('adhcga', period)
        cappme = foyer_fiscal('cappme', period)
        creaen = foyer_fiscal('creaen', period)
        daepad = foyer_fiscal('daepad', period)
        deffor = foyer_fiscal('deffor', period)
        dfppce = foyer_fiscal('dfppce', period)
        doment = foyer_fiscal('doment', period)
        domlog = foyer_fiscal('domlog', period)
        donapd = foyer_fiscal('donapd', period)
        duflot = foyer_fiscal('duflot', period)
        ecpess = foyer_fiscal('ecpess', period)
        garext = foyer_fiscal('garext', period)
        intagr = foyer_fiscal('intagr', period)
        invfor = foyer_fiscal('invfor', period)
        invlst = foyer_fiscal('invlst', period)
        ip_net = foyer_fiscal('ip_net', period)
        locmeu = foyer_fiscal('locmeu', period)
        mecena = foyer_fiscal('mecena', period)
        mohist = foyer_fiscal('mohist', period)
        patnat = foyer_fiscal('patnat', period)
        prcomp = foyer_fiscal('prcomp', period)
        reduction_impot_exceptionnelle = foyer_fiscal('reduction_impot_exceptionnelle', period)
        repsoc = foyer_fiscal('repsoc', period)
        resimm = foyer_fiscal('resimm', period)
        rsceha = foyer_fiscal('rsceha', period)
        saldom = foyer_fiscal('saldom', period)
        scelli = foyer_fiscal('scelli', period)
        sofica = foyer_fiscal('sofica', period)
        spfcpi = foyer_fiscal('spfcpi', period)

        total_reductions = (accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist +
        patnat + prcomp + reduction_impot_exceptionnelle + repsoc + resimm + rsceha + saldom + scelli + sofica +
        spfcpi)
        return min_(ip_net, total_reductions)


        # pour tous les dfppce:
        # : note de bas de page
        # TODO: plafonnement pour parti politiques depuis 2012 P.impot_revenu.reductions_impots.dons.max_niv


class adhcga(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"adhcga"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Frais de comptabilité et d'adhésion à un CGA ou AA
        2002-
        '''
        f7ff = foyer_fiscal('f7ff', period)
        f7fg = foyer_fiscal('f7fg', period)
        P = parameters(period).impot_revenu.reductions_impots.adhcga

        return min_(f7ff, P.max * f7fg)


class assvie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"assvie"
    end = '2004-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Assurance-vie (cases GW, GX et GY de la 2042)
        2002-2004
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        f7gw = foyer_fiscal('f7gw', period)
        f7gx = foyer_fiscal('f7gx', period)
        f7gy = foyer_fiscal('f7gy', period)
        P = parameters(period).impot_revenu.reductions_impots.assvie

        max1 = P.max + nb_pac * P.pac
        return P.taux * min_(f7gw + f7gx + f7gy, max1)


class cappme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"cappme"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2002
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cf
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2003
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cf + f7cl
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2004
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cf + f7cl + f7cm
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2005-2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cf + f7cl + f7cm + f7cn
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2009-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cf + f7cl + f7cm + f7cn + f7cu
        seuil = P.seuil * (maries_ou_pacses + 1)
        seuil = P.seuil_tpe * (maries_ou_pacses + 1) * (f7cu > 0) + P.seuil * (maries_ou_pacses + 1) * (f7cu <= 0)
        return P.taux * min_(base, seuil)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cl + f7cm + f7cn + f7cq
        seuil = P.seuil_tpe * (maries_ou_pacses + 1) * (f7cu > 0) + P.seuil * (maries_ou_pacses + 1) * (f7cu <= 0)
        max0 = max_(seuil - base, 0)
        return max_(P.taux25 * min_(base, seuil), P.taux * min_(max0, f7cf + f7cu))

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2012 cf. 2041 GR
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        #TODO: gérer les changements de situation familiale
        base = f7cl + f7cm + f7cn
        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = max_(0, P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)
        return P.taux25 * min_(base, seuil1) + P.taux * min_(f7cq, seuil1) + P.taux18 * (min_(f7cf, seuil3) +
                mini(f7cu, seuil2, seuil1))

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cc = foyer_fiscal('f7cc', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.reductions_impots.cappme

        base = f7cl + f7cm
        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = max_(0, P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cn, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)
        return P.taux25 * min_(base, seuil1) + P.taux22 * min_(f7cn, seuil1) + P.taux18 * (min_(f7cf + f7cc, seuil3) +
                min_(f7cu + f7cq, seuil2))


class cotsyn(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"cotsyn"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Cotisations syndicales (2002-20131
        '''
        f7ac = foyer_fiscal.members('f7ac', period)
        salaire_imposable = foyer_fiscal.members('salaire_imposable', period, options = [ADD])
        chomage_imposable = foyer_fiscal.members('chomage_imposable', period, options = [ADD])
        retraite_imposable = foyer_fiscal.members('retraite_imposable', period, options = [ADD])

        P = parameters(period).impot_revenu.reductions_impots.cotsyn
        tx = P.seuil

        max_imposable = (salaire_imposable + chomage_imposable + retraite_imposable) * tx

        return P.taux * foyer_fiscal.sum(
            min_(f7ac, max_imposable)
            )

class creaen(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"creaen"
    definition_period = YEAR
    end = '2014-12-31'

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2006-2008
        '''
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)
        P = parameters(period).impot_revenu.reductions_impots.creaen

        return (P.base * f7fy + P.hand * f7gy)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2009
        '''
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7hy = foyer_fiscal('f7hy', period)
        f7ky = foyer_fiscal('f7ky', period)
        f7iy = foyer_fiscal('f7iy', period)
        P = parameters(period).impot_revenu.reductions_impots.creaen


        return (P.base * ((f7jy + f7fy) + f7hy / 2) +
                    P.hand * ((f7ky + f7gy) + f7iy / 2))

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2010-2011
        '''
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7hy = foyer_fiscal('f7hy', period)
        f7ky = foyer_fiscal('f7ky', period)
        f7iy = foyer_fiscal('f7iy', period)
        f7ly = foyer_fiscal('f7ly', period)
        f7my = foyer_fiscal('f7my', period)
        P = parameters(period).impot_revenu.reductions_impots.creaen

        return (P.base * ((f7jy + f7fy) + (f7hy + f7ly) / 2) +
                    P.hand * ((f7ky + f7gy) + (f7iy + f7my) / 2))

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2012-
        '''
        f7ly = foyer_fiscal('f7ly', period)
        f7my = foyer_fiscal('f7my', period)
        P = parameters(period).impot_revenu.reductions_impots.creaen

        return (P.base * (f7ly / 2) +
                    P.hand * (f7my / 2))


class deffor(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"deffor"
    definition_period = YEAR

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Défense des forêts contre l'incendie
        2006-
        '''
        f7uc = foyer_fiscal('f7uc', period)
        P = parameters(period).impot_revenu.reductions_impots.deffor

        return P.taux * min_(f7uc, P.max)


class daepad(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"daepad"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
        ?-
        '''
        f7cd = foyer_fiscal('f7cd', period)
        f7ce = foyer_fiscal('f7ce', period)
        P = parameters(period).impot_revenu.reductions_impots.daepad

        return P.taux * (min_(f7cd, P.max) + min_(f7ce, P.max))


class dfppce(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"dfppce"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7xs
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7xs + f7xt
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu + f7xw
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7vc = foyer_fiscal('f7vc', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7vc = foyer_fiscal('f7vc', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = min_(P.max_niv, f7uf) + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        rbg_int = foyer_fiscal('rbg_int', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7uh = foyer_fiscal('f7uh', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7vc = foyer_fiscal('f7vc', period)
        P = parameters(period).impot_revenu.reductions_impots.dons

        base = min_(P.max_niv, f7uf + f7uh) + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.taux_max_dons_partipo * rbg_int
        return P.taux_dons_oeuvres * min_(base, max1)


    # TODO: note de bas de page
    #       Introduire plus de détails dans la déclaration pour séparer les dons aux partis poitiques
    #       et aux candidats des autres dons


# Outre-mer : TODO: plafonnement, cf. 2041-GE 2042-IOM
class doment(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"doment"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7ur = foyer_fiscal('f7ur', period)
        f7oz = foyer_fiscal('f7oz', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rz = foyer_fiscal('f7rz', period)

        return  f7ur + f7oz + f7pz + f7qz + f7rz

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7ur = foyer_fiscal('f7ur', period)
        f7oz = foyer_fiscal('f7oz', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rz = foyer_fiscal('f7rz', period)
        f7sz = foyer_fiscal('f7sz', period)

        return  f7ur + f7oz + f7pz + f7qz + f7rz + f7sz

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7oz = foyer_fiscal('f7oz', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rz = foyer_fiscal('f7rz', period)
        f7sz = foyer_fiscal('f7sz', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qj = foyer_fiscal('f7qj', period)

        return  f7oz + f7pz + f7qz + f7rz + f7sz + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7oz = foyer_fiscal('f7oz', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rz = foyer_fiscal('f7rz', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qj = foyer_fiscal('f7qj', period)
        f7qo = foyer_fiscal('f7qo', period)
        f7qp = foyer_fiscal('f7qp', period)
        f7qq = foyer_fiscal('f7qq', period)
        f7qr = foyer_fiscal('f7qr', period)
        f7qs = foyer_fiscal('f7qs', period)
        f7mm = foyer_fiscal('f7mm', period)
        f7ma = foyer_fiscal('f7ma', period)
        f7lg = foyer_fiscal('f7lg', period)
        f7ks = foyer_fiscal('f7ks', period)
        f7ls = foyer_fiscal('f7ls', period)

        return (f7oz + f7pz + f7qz + f7rz + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj + f7qo + f7qp + f7qq + f7qr + f7qs +
                    f7mm + f7ma + f7lg + f7ks + f7ls)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7ks = foyer_fiscal('f7ks', period)
        f7kt = foyer_fiscal('f7kt', period)
        f7ku = foyer_fiscal('f7ku', period)
        f7lg = foyer_fiscal('f7lg', period)
        f7lh = foyer_fiscal('f7lh', period)
        f7li = foyer_fiscal('f7li', period)
        f7mm = foyer_fiscal('f7mm', period)
        f7ma = foyer_fiscal('f7ma', period)
        f7mb = foyer_fiscal('f7mb', period)
        f7mc = foyer_fiscal('f7mc', period)
        f7mn = foyer_fiscal('f7mn', period)
        f7oz = foyer_fiscal('f7oz', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pd = foyer_fiscal('f7pd', period)
        f7pe = foyer_fiscal('f7pe', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qo = foyer_fiscal('f7qo', period)
        f7qp = foyer_fiscal('f7qp', period)
        f7qq = foyer_fiscal('f7qq', period)
        f7qr = foyer_fiscal('f7qr', period)
        f7qv = foyer_fiscal('f7qv', period)

        return (f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7mb + f7mn + f7mc + f7mm + f7ma +  f7oz + f7pa + f7pb + f7pd +
                    f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pz + f7qz + f7qf + f7qg + f7qh + f7qi + f7qo +
                    f7qp + f7qq + f7qr + f7qe + f7qv)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        f7ks = foyer_fiscal('f7ks', period)
        f7kt = foyer_fiscal('f7kt', period)
        f7ku = foyer_fiscal('f7ku', period)
        f7lg = foyer_fiscal('f7lg', period)
        f7lh = foyer_fiscal('f7lh', period)
        f7li = foyer_fiscal('f7li', period)
        f7ma = foyer_fiscal('f7ma', period)
        f7mb = foyer_fiscal('f7mb', period)
        f7mc = foyer_fiscal('f7mc', period)
        f7mm = foyer_fiscal('f7mm', period)
        f7mn = foyer_fiscal('f7mn', period)
        f7nu = foyer_fiscal('f7nu', period)
        f7nv = foyer_fiscal('f7nv', period)
        f7nw = foyer_fiscal('f7nw', period)
        f7ny = foyer_fiscal('f7ny', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pd = foyer_fiscal('f7pd', period)
        f7pe = foyer_fiscal('f7pe', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)
        f7pp = foyer_fiscal('f7pp', period)
        f7pr = foyer_fiscal('f7pr', period)
        f7ps = foyer_fiscal('f7ps', period)
        f7pt = foyer_fiscal('f7pt', period)
        f7pu = foyer_fiscal('f7pu', period)
        f7pw = foyer_fiscal('f7pw', period)
        f7px = foyer_fiscal('f7px', period)
        f7py = foyer_fiscal('f7py', period)
        f7pz = foyer_fiscal('f7pz', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qo = foyer_fiscal('f7qo', period)
        f7qp = foyer_fiscal('f7qp', period)
        f7qr = foyer_fiscal('f7qr', period)
        f7qv = foyer_fiscal('f7qv', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rg = foyer_fiscal('f7rg', period)
        f7ri = foyer_fiscal('f7ri', period)
        f7rj = foyer_fiscal('f7rj', period)
        f7rk = foyer_fiscal('f7rk', period)
        f7rl = foyer_fiscal('f7rl', period)
        f7rm = foyer_fiscal('f7rm', period)
        f7ro = foyer_fiscal('f7ro', period)
        f7rp = foyer_fiscal('f7rp', period)
        f7rq = foyer_fiscal('f7rq', period)
        f7rr = foyer_fiscal('f7rr', period)
        f7rt = foyer_fiscal('f7rt', period)
        f7ru = foyer_fiscal('f7ru', period)
        f7rv = foyer_fiscal('f7rv', period)
        f7rw = foyer_fiscal('f7rw', period)
        f7rx = foyer_fiscal('f7rx', period)
        f7ry = foyer_fiscal('f7ry', period)

        return (f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7ma + f7mb + f7mc + f7mm + f7mn +  f7pz + f7nu + f7nv + f7nw +
                    f7ny + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pm + f7pn + f7po + f7pp + f7pr +
                    f7ps + f7pt + f7pu + f7pw + f7px + f7py + f7qe + f7qf + f7qg + f7qi + f7qo + f7qp + f7qr + f7qv + f7qz +
                    f7rg + f7ri + f7rj + f7rk + f7rl + f7rm + f7ro + f7rp + f7rq + f7rr + f7rt + f7ru + f7rv + f7rw)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        fhsa = foyer_fiscal('fhsa', period)
        fhsb = foyer_fiscal('fhsb', period)
        fhsf = foyer_fiscal('fhsf', period)
        fhsg = foyer_fiscal('fhsg', period)
        fhsc = foyer_fiscal('fhsc', period)
        fhsh = foyer_fiscal('fhsh', period)
        fhse = foyer_fiscal('fhse', period)
        fhsj = foyer_fiscal('fhsj', period)
        fhsk = foyer_fiscal('fhsk', period)
        fhsl = foyer_fiscal('fhsl', period)
        fhsp = foyer_fiscal('fhsp', period)
        fhsq = foyer_fiscal('fhsq', period)
        fhsm = foyer_fiscal('fhsm', period)
        fhsr = foyer_fiscal('fhsr', period)
        fhso = foyer_fiscal('fhso', period)
        fhst = foyer_fiscal('fhst', period)
        fhsu = foyer_fiscal('fhsu', period)
        fhsv = foyer_fiscal('fhsv', period)
        fhsw = foyer_fiscal('fhsw', period)
        fhsz = foyer_fiscal('fhsz', period)
        fhta = foyer_fiscal('fhta', period)
        fhtb = foyer_fiscal('fhtb', period)
        fhtd = foyer_fiscal('fhtd', period)
        f7ks = foyer_fiscal('f7ks', period)
        f7kt = foyer_fiscal('f7kt', period)
        f7ku = foyer_fiscal('f7ku', period)
        f7lg = foyer_fiscal('f7lg', period)
        f7lh = foyer_fiscal('f7lh', period)
        f7li = foyer_fiscal('f7li', period)
        f7ma = foyer_fiscal('f7ma', period)
        f7mb = foyer_fiscal('f7mb', period)
        f7mc = foyer_fiscal('f7mc', period)
        f7mm = foyer_fiscal('f7mm', period)
        f7mn = foyer_fiscal('f7mn', period)
        f7nu = foyer_fiscal('f7nu', period)
        f7nv = foyer_fiscal('f7nv', period)
        f7nw = foyer_fiscal('f7nw', period)
        f7ny = foyer_fiscal('f7ny', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pd = foyer_fiscal('f7pd', period)
        f7pe = foyer_fiscal('f7pe', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)
        f7pp = foyer_fiscal('f7pp', period)
        f7pr = foyer_fiscal('f7pr', period)
        f7ps = foyer_fiscal('f7ps', period)
        f7pt = foyer_fiscal('f7pt', period)
        f7pu = foyer_fiscal('f7pu', period)
        f7pw = foyer_fiscal('f7pw', period)
        f7px = foyer_fiscal('f7px', period)
        f7py = foyer_fiscal('f7py', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qo = foyer_fiscal('f7qo', period)
        f7qp = foyer_fiscal('f7qp', period)
        f7qr = foyer_fiscal('f7qr', period)
        f7qv = foyer_fiscal('f7qv', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rg = foyer_fiscal('f7rg', period)
        f7ri = foyer_fiscal('f7ri', period)
        f7rj = foyer_fiscal('f7rj', period)
        f7rk = foyer_fiscal('f7rk', period)
        f7rl = foyer_fiscal('f7rl', period)
        f7rm = foyer_fiscal('f7rm', period)
        f7ro = foyer_fiscal('f7ro', period)
        f7rp = foyer_fiscal('f7rp', period)
        f7rq = foyer_fiscal('f7rq', period)
        f7rr = foyer_fiscal('f7rr', period)
        f7rt = foyer_fiscal('f7rt', period)
        f7ru = foyer_fiscal('f7ru', period)
        f7rv = foyer_fiscal('f7rv', period)
        f7rw = foyer_fiscal('f7rw', period)
        f7ry = foyer_fiscal('f7ry', period)

        return (fhsa + fhsb + fhsf + fhsg + fhsc + fhsh + fhse + fhsj + fhsk + fhsl + fhsp + fhsq + fhsm + fhsr + fhso +
                    fhst + fhsu + fhsv + fhsw + fhsz + fhta + fhtb + fhtd + f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7ma +
                    f7mb + f7mc + f7mm + f7mn + f7nu + f7nv + f7nw + f7ny + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi +
                    f7pj + f7pl + f7pm + f7pn + f7po + f7pp + f7pr + f7ps + f7pt + f7pu + f7pw + f7px + f7py + f7qe + f7qf +
                    f7qg + f7qi + f7qo + f7qp + f7qr + f7qv + f7qz + f7rg + f7ri + f7rj + f7rk + f7rl + f7rm + f7ro + f7rp +
                    f7rq + f7rr + f7rt + f7ru + f7rv + f7rw)

        # TODO: vérifier pour 2002
        # TODO: pb 7ul 2005-2009 (ITRED = 0 au lieu de 20€ (forfaitaire), dû à ça : Cochez [7UL] si vous déclarez en ligne pour
        # la première fois vos revenus 2008 et si vous utilisez un moyen automatique de paiement (prélèvement mensuel ou à
        # l'échéance ou paiement par voie électronique))


        # TODO: vérifier les dates des variables de doment et domsoc (y sont-elles encore en 2013 par ex ?)

class domlog(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"domlog"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2002
        '''
        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uc = foyer_fiscal('f7uc', period)
        f7uj = foyer_fiscal('f7uj', period)
        P = parameters(period).impot_revenu.reductions_impots.domlog

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2003-2004
        '''
        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uc = foyer_fiscal('f7uc', period)
        f7ui = foyer_fiscal('f7ui', period)
        f7uj = foyer_fiscal('f7uj', period)
        P = parameters(period).impot_revenu.reductions_impots.domlog

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc) + f7ui

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2005-2007
        '''
        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uc = foyer_fiscal('f7uc', period)
        f7ui = foyer_fiscal('f7ui', period)
        f7uj = foyer_fiscal('f7uj', period)
        P = parameters(period).impot_revenu.reductions_impots.domlog

        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub) + f7ui

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2008
        '''
        f7ui = foyer_fiscal('f7ui', period)

        return f7ui

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2009
        '''
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7qk = foyer_fiscal('f7qk', period)

        return f7qb + f7qc + f7qd + f7qk / 2

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2010
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7ql = foyer_fiscal('f7ql', period)
        f7qt = foyer_fiscal('f7qt', period)
        f7qm = foyer_fiscal('f7qm', period)

        return f7qb + f7qc + f7qd + f7ql + f7qt + f7qm

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2011
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7ql = foyer_fiscal('f7ql', period)
        f7qm = foyer_fiscal('f7qm', period)
        f7qt = foyer_fiscal('f7qt', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)

        return f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2012
        TODO: Plafonnement sur la notice
        '''
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7ql = foyer_fiscal('f7ql', period)
        f7qm = foyer_fiscal('f7qm', period)
        f7qt = foyer_fiscal('f7qt', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7op = foyer_fiscal('f7op', period)
        f7oq = foyer_fiscal('f7oq', period)
        f7or = foyer_fiscal('f7or', period)
        f7os = foyer_fiscal('f7os', period)
        f7ot = foyer_fiscal('f7ot', period)
        f7ou = foyer_fiscal('f7ou', period)
        f7ov = foyer_fiscal('f7ov', period)
        f7ow = foyer_fiscal('f7ow', period)

        return (f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok + f7ol + f7om +
                    f7on + f7oo + f7op + f7oq + f7or + f7os + f7ot + f7ou + f7ov + f7ow)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2013
        TODO: Plafonnement sur la notice
        '''
        fhod = foyer_fiscal('fhod', period)
        fhoe = foyer_fiscal('fhoe', period)
        fhof = foyer_fiscal('fhof', period)
        fhog = foyer_fiscal('fhog', period)
        fhox = foyer_fiscal('fhox', period)
        fhoy = foyer_fiscal('fhoy', period)
        fhoz = foyer_fiscal('fhoz', period)
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7ql = foyer_fiscal('f7ql', period)
        f7qm = foyer_fiscal('f7qm', period)
        f7qt = foyer_fiscal('f7qt', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7op = foyer_fiscal('f7op', period)
        f7oq = foyer_fiscal('f7oq', period)
        f7or = foyer_fiscal('f7or', period)
        f7os = foyer_fiscal('f7os', period)
        f7ot = foyer_fiscal('f7ot', period)
        f7ou = foyer_fiscal('f7ou', period)
        f7ov = foyer_fiscal('f7ov', period)
        f7ow = foyer_fiscal('f7ow', period)

        return (f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok + f7ol + f7om +
                    f7on + f7oo + f7op + f7oq + f7or + f7os + f7ot + f7ou + f7ov + f7ow + fhod + fhoe +
                    fhof + fhog + fhox + fhoy + fhoz)


#En accord avec la DGFiP mais pas de 7ub et 7uj dans la notice


class domsoc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"domsoc"
    definition_period = YEAR
    end = '2013-12-31'


    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2010-
        TODO plafonnement à 15% f7qa / liens avec autres investissments ?
        '''
        f7qn = foyer_fiscal('f7qn', period)
        f7qk = foyer_fiscal('f7qk', period)
        f7qu = foyer_fiscal('f7qu', period)
        f7kg = foyer_fiscal('f7kg', period)
        f7kh = foyer_fiscal('f7kh', period)
        f7ki = foyer_fiscal('f7ki', period)
        f7qj = foyer_fiscal('f7qj', period)
        f7qs = foyer_fiscal('f7qs', period)
        f7qw = foyer_fiscal('f7qw', period)
        f7qx = foyer_fiscal('f7qx', period)

        return  f7qn + f7qk + f7qu + f7kg + f7kh + f7ki + f7qj + f7qs + f7qw + f7qx

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2013
        TODO plafonnement à 15% f7qa / liens avec autres investissments ?
        '''
        fhra = foyer_fiscal('fhra', period)
        fhrb = foyer_fiscal('fhrb', period)
        fhrc = foyer_fiscal('fhrc', period)
        fhrd = foyer_fiscal('fhrd', period)
        f7qn = foyer_fiscal('f7qn', period)
        f7qk = foyer_fiscal('f7qk', period)
        f7qu = foyer_fiscal('f7qu', period)
        f7kg = foyer_fiscal('f7kg', period)
        f7kh = foyer_fiscal('f7kh', period)
        f7ki = foyer_fiscal('f7ki', period)
        f7qj = foyer_fiscal('f7qj', period)
        f7qs = foyer_fiscal('f7qs', period)
        f7qw = foyer_fiscal('f7qw', period)
        f7qx = foyer_fiscal('f7qx', period)

        return  fhra + fhrb + fhrc + fhrd + f7qn + f7qk + f7qu + f7kg + f7kh + f7ki + f7qj + f7qs + f7qw + f7qx


class donapd(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"donapd"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Dons effectués à  des organises d'aide aux personnes en difficulté (2002-2010)
        '''
        f7ud = foyer_fiscal('f7ud', period)
        P = parameters(period).impot_revenu.reductions_impots.donapd

        return P.taux * min_(f7ud, P.max)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Dons effectués à  des organises d'aide aux personnes en difficulté (2011-2013)
        '''
        f7ud = foyer_fiscal('f7ud', period)
        f7va = foyer_fiscal('f7va', period)
        P = parameters(period).impot_revenu.reductions_impots.donapd

        return P.taux * min_(f7ud + f7va, P.max)


class duflot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"duflot"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs interméiaires (loi Duflot)
        2013-
        '''
        f7gh = foyer_fiscal('f7gh', period)
        f7gi = foyer_fiscal('f7gi', period)
        P = parameters(period).impot_revenu.reductions_impots.duflot

        return min_(P.plafond, P.taux_m * f7gh + P.taux_om * f7gi) / 9


#TODO: / 5 dans trois TOM

class ecodev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"ecodev"
    end = '2009-12-31'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées sur un compte épargne codéveloppement (case 7UH)
        2009
        '''
        f7uh = foyer_fiscal('f7uh', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        P = parameters(period).impot_revenu.reductions_impots.ecodev

        return min_(f7uh * P.taux, min_(P.taux_plafond * rbg_int, P.plafond_par_personne))  # page3 ligne 18


class ecpess(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"ecpess"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Réduction d'impôt au titre des enfants à charge poursuivant leurs études secondaires ou supérieures
        '''
        f7ea = foyer_fiscal('f7ea', period)
        f7eb = foyer_fiscal('f7eb', period)
        f7ec = foyer_fiscal('f7ec', period)
        f7ed = foyer_fiscal('f7ed', period)
        f7ef = foyer_fiscal('f7ef', period)
        f7eg = foyer_fiscal('f7eg', period)
        P = parameters(period).impot_revenu.reductions_impots.ecpess

        return (P.col * (f7ea + f7eb / 2) +
                P.lyc * (f7ec + f7ed / 2) +
                P.sup * (f7ef + f7eg / 2))


class garext(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"garext"
    definition_period = YEAR
    end = '2005-12-31'


    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2002
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        P = parameters(period).impot_revenu.credits_impot.garext

        max1 = P.plafond
        return P.taux * (min_(f7ga, max1) + min_(f7gb, max1) + min_(f7gc, max1))

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2003-2005
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        f7ge = foyer_fiscal('f7ge', period)
        f7gf = foyer_fiscal('f7gf', period)
        f7gg = foyer_fiscal('f7gg', period)
        P = parameters(period).impot_revenu.credits_impot.garext

        max1 = P.plafond
        max2 = P.plafond / 2
        return P.taux * (min_(f7ga, max1) +
                           min_(f7gb, max1) +
                           min_(f7gc, max1) +
                           min_(f7ge, max2) +
                           min_(f7gf, max2) +
                           min_(f7gg, max2))


class intagr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"intagr"
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts pour paiement différé accordé aux agriculteurs
        2005-
        '''
        f7um = foyer_fiscal('f7um', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        P = parameters(period).impot_revenu.reductions_impots.intagr

        max1 = P.max * (1 + maries_ou_pacses)
        return P.taux * min_(f7um, max1)


class intcon(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"intcon"
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts des prêts à la consommation (case UH)
        2004-2005
        '''
        f7uh = foyer_fiscal('f7uh', period)
        P = parameters(period).impot_revenu.reductions_impots.intcon

        max1 = P.max
        return P.taux * min_(f7uh, max1)


class intemp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"intemp"
    end = '2003-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts d'emprunts
        2002-2003
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        f7wg = foyer_fiscal('f7wg', period)
        P = parameters(period).impot_revenu.reductions_impots.intemp

        max1 = P.max + P.pac * nb_pac
        return P.taux * min_(f7wg, max1)


class invfor(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"invfor"
    definition_period = YEAR
    end = '2013-12-31'


    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2002-2005
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7un = foyer_fiscal('f7un', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(f7un, seuil)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2006-2008
        '''
        f7un = foyer_fiscal('f7un', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        return P.taux * f7un

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        return P.taux * (min_(f7un, P.seuil * (maries_ou_pacses + 1)) + min_(f7up, P.ifortra_seuil * (maries_ou_pacses + 1)) +
                min_(f7uq, P.iforges_seuil * (maries_ou_pacses + 1)))

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        return (P.taux * (
            min_(f7un, P.seuil * (maries_ou_pacses + 1)) +
            min_(f7up + f7uu + f7te, P.ifortra_seuil * (maries_ou_pacses + 1)) +
            min_(f7uq, P.iforges_seuil * (maries_ou_pacses + 1))))

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2011 cf. 2041 GK
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu', period)
        f7uv = foyer_fiscal('f7uv', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        max0 = max_(0, P.ifortra_seuil * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        return (P.taux * (
            min_(f7un, P.seuil * (maries_ou_pacses + 1)) +
            min_(f7up, max1) +
            min_(f7uq, P.iforges_seuil * (maries_ou_pacses + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (maries_ou_pacses + 1)))

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2012 cf. 2041 GK
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu', period)
        f7uv = foyer_fiscal('f7uv', period)
        f7uw = foyer_fiscal('f7uw', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        max0 = max_(0, P.ifortra_seuil * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        max2 = max_(0, max1 - f7tg - f7uw)
        return (P.taux * (
            min_(f7un, P.seuil * (maries_ou_pacses + 1)) +
            min_(f7up, max2) +
            min_(f7uq, P.iforges_seuil * (maries_ou_pacses + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.report11 * min_(f7tg + f7uw, max1) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (maries_ou_pacses + 1)))

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2013 cf. 2041 GK
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7th = foyer_fiscal('f7th', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu', period)
        f7uv = foyer_fiscal('f7uv', period)
        f7uw = foyer_fiscal('f7uw', period)
        f7ux = foyer_fiscal('f7ux', period)
        P = parameters(period).impot_revenu.reductions_impots.invfor

        max0 = max_(0, P.ifortra_seuil * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        max2 = max_(0, max1 - f7tg - f7uw)
        max3 = max_(0, max2 - f7th - f7ux)
        return (P.taux * (
            min_(f7un, P.seuil * (maries_ou_pacses + 1)) +
            min_(f7up, max3) +
            min_(f7uq, P.iforges_seuil * (maries_ou_pacses + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.report11 * min_(f7tg + f7uw, max1) +
            P.report12 * min_(f7th + f7ux, max2) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (maries_ou_pacses + 1)))


class invlst(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"invlst"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2004
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xc = foyer_fiscal('f7xc', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh', period)
        f7xi = foyer_fiscal('f7xi', period)
        f7xj = foyer_fiscal('f7xj', period)
        f7xk = foyer_fiscal('f7xk', period)
        f7xl = foyer_fiscal('f7xl', period)
        f7xm = foyer_fiscal('f7xm', period)
        f7xn = foyer_fiscal('f7xn', period)
        f7xo = foyer_fiscal('f7xo', period)
        P = parameters(period).impot_revenu.reductions_impots.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)
        seuil3 = P.seuil3 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 4)
        xd = P.taux_xd * f7xd
        xe = P.taux_xe * min_(f7xe, seuil1 / 6)
        xf = P.taux_xf * f7xf
        xg = P.taux_xg * min_(f7xg, seuil2)
        xh = P.taux_xh * min_(f7xh, seuil3)
        xi = P.taux_xi * min_(f7xi, seuil1 / 4)
        xj = P.taux_xj * f7xj
        xk = P.taux_xk * f7xk
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xm = P.taux_xm * f7xm
        xn = P.taux_xn * min_(f7xn, seuil1 / 6)
        xo = P.taux_xo * f7xo

        return around(xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2005-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xc = foyer_fiscal('f7xc', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh', period)
        f7xi = foyer_fiscal('f7xi', period)
        f7xj = foyer_fiscal('f7xj', period)
        f7xk = foyer_fiscal('f7xk', period)
        f7xl = foyer_fiscal('f7xl', period)
        f7xm = foyer_fiscal('f7xm', period)
        f7xn = foyer_fiscal('f7xn', period)
        f7xo = foyer_fiscal('f7xo', period)
        P = parameters(period).impot_revenu.reductions_impots.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)
        seuil3 = P.seuil3 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xd = P.taux_xd * f7xd
        xe = P.taux_xe * min_(f7xe, seuil1 / 6)
        xf = P.taux_xf * f7xf
        xg = P.taux_xg * min_(f7xg, seuil2)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xg)
        xi = P.taux_xi * f7xi
        xj = P.taux_xj * f7xj
        xk = P.taux_xk * f7xk
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xm = P.taux_xm * f7xm
        xn = P.taux_xn * min_(f7xn, seuil1 / 6)
        xo = P.taux_xo * f7xo

        return around(xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xa = foyer_fiscal('f7xa', period)
        f7xb = foyer_fiscal('f7xb', period)
        f7xc = foyer_fiscal('f7xc', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh', period)
        f7xi = foyer_fiscal('f7xi', period)
        f7xj = foyer_fiscal('f7xj', period)
        f7xk = foyer_fiscal('f7xk', period)
        f7xl = foyer_fiscal('f7xl', period)
        f7xm = foyer_fiscal('f7xm', period)
        f7xn = foyer_fiscal('f7xn', period)
        f7xo = foyer_fiscal('f7xo', period)
        f7xp = foyer_fiscal('f7xp', period)
        f7xq = foyer_fiscal('f7xq', period)
        f7xr = foyer_fiscal('f7xr', period)
        P = parameters(period).impot_revenu.reductions_impots.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)
        seuil3 = P.seuil3 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xa = P.taux_xa * min_(f7xa, seuil2)
        xg = P.taux_xg * min_(f7xg, seuil2 - f7xa)
        xb = P.taux_xb * min_(f7xb, seuil2 - f7xa - f7xg)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xa - f7xg - f7xb)
        xi = P.taux_xi * (f7xf + f7xi + f7xp)
        xj = P.taux_xj * (f7xm + f7xj + f7xq)
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xc + xa + xg + xb + xh + xi + xj + xl + xo)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2012
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xa = foyer_fiscal('f7xa', period)
        f7xb = foyer_fiscal('f7xb', period)
        f7xc = foyer_fiscal('f7xc', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh', period)
        f7xi = foyer_fiscal('f7xi', period)
        f7xj = foyer_fiscal('f7xj', period)
        f7xk = foyer_fiscal('f7xk', period)
        f7xl = foyer_fiscal('f7xl', period)
        f7xm = foyer_fiscal('f7xm', period)
        f7xn = foyer_fiscal('f7xn', period)
        f7xo = foyer_fiscal('f7xo', period)
        f7xp = foyer_fiscal('f7xp', period)
        f7xq = foyer_fiscal('f7xq', period)
        f7xr = foyer_fiscal('f7xr', period)
        f7xv = foyer_fiscal('f7xv', period)
        f7xx = foyer_fiscal('f7xx', period)
        f7xz = foyer_fiscal('f7xz', period)
        P = parameters(period).impot_revenu.reductions_impots.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)
        seuil3 = P.seuil3 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xa = P.taux_xa * min_(f7xa, seuil2)
        xg = P.taux_xg * min_(f7xg, seuil2 - f7xa)
        xx = P.taux_xx * min_(f7xx, seuil2 - f7xa - f7xg)
        xb = P.taux_xb * min_(f7xb, seuil2 - f7xa - f7xg - f7xx)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xa - f7xg - f7xb - f7xx)
        xz = P.taux_xz * min_(f7xz, seuil2 - f7xa - f7xg - f7xb - f7xx - f7xh)
        xi = P.taux_xi * (f7xf + f7xi + f7xp + f7xn)
        xj = P.taux_xj * (f7xm + f7xj + f7xq + f7xv)
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xc + xa + xg + xx + xb + xz + xh + xi + xj + xl + xo)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7uy = foyer_fiscal('f7uy', period)
        f7uz = foyer_fiscal('f7uz', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xi = foyer_fiscal('f7xi', period)
        f7xj = foyer_fiscal('f7xj', period)
        f7xk = foyer_fiscal('f7xk', period)
        f7xm = foyer_fiscal('f7xm', period)
        f7xn = foyer_fiscal('f7xn', period)
        f7xo = foyer_fiscal('f7xo', period)
        f7xp = foyer_fiscal('f7xp', period)
        f7xq = foyer_fiscal('f7xq', period)
        f7xr = foyer_fiscal('f7xr', period)
        f7xv = foyer_fiscal('f7xv', period)
        P = parameters(period).impot_revenu.reductions_impots.invlst

        xi = P.taux_xi * (f7xf + f7xi + f7xp + f7xn + f7uy)
        xj = P.taux_xj * (f7xm + f7xj + f7xq + f7xv + f7uz)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xi + xj + xo)


class invrev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"invrev"
    end = '2003-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans les résidences de tourisme situées dans une zone de
        revitalisation rurale (cases GS, GT, XG, GU et GV)
        2002-2003
        TODO 1/4 codé en dur
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gs = foyer_fiscal('f7gs', period)
        f7gt = foyer_fiscal('f7gt', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7gu = foyer_fiscal('f7gu', period)
        f7gv = foyer_fiscal('f7gv', period)
        P = parameters(period).impot_revenu.reductions_impots.invrev

        return (P.taux_gs * min_(f7gs, P.seuil_gs * (1 + maries_ou_pacses)) / 4 +
                 P.taux_gu * min_(f7gu, P.seuil_gu * (1 + maries_ou_pacses)) / 4 +
                 P.taux_xg * min_(f7xg, P.seuil_xg * (1 + maries_ou_pacses)) / 4 +
                 P.taux_gt * f7gt + P.taux_gt * f7gv)


class locmeu(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"locmeu"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2009
        '''
        f7ij = foyer_fiscal('f7ij', period)
        P = parameters(period).impot_revenu.reductions_impots.locmeu

        return P.taux * min_(P.max, f7ij) / 9

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2010
        '''
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7is = foyer_fiscal('f7is', period)
        P = parameters(period).impot_revenu.reductions_impots.locmeu

        return ((min_(P.max, max_(f7ij, f7il)) + min_(P.max, f7im)) / 9 + f7ik) * P.taux + f7is

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2011
        '''
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io', period)
        f7ip = foyer_fiscal('f7ip', period)
        f7iq = foyer_fiscal('f7iq', period)
        f7ir = foyer_fiscal('f7ir', period)
        f7is = foyer_fiscal('f7is', period)
        f7it = foyer_fiscal('f7it', period)
        f7iu = foyer_fiscal('f7iu', period)
        f7iv = foyer_fiscal('f7iv', period)
        f7iw = foyer_fiscal('f7iw', period)
        P = parameters(period).impot_revenu.reductions_impots.locmeu

        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik, f7ip + f7ir + f7iq) +
            f7is + f7iu + f7it)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2012
        '''
        f7ia = foyer_fiscal('f7ia', period)
        f7ib = foyer_fiscal('f7ib', period)
        f7ic = foyer_fiscal('f7ic', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie', period)
        f7if = foyer_fiscal('f7if', period)
        f7ig = foyer_fiscal('f7ig', period)
        f7ih = foyer_fiscal('f7ih', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io', period)
        f7ip = foyer_fiscal('f7ip', period)
        f7iq = foyer_fiscal('f7iq', period)
        f7ir = foyer_fiscal('f7ir', period)
        f7is = foyer_fiscal('f7is', period)
        f7it = foyer_fiscal('f7it', period)
        f7iu = foyer_fiscal('f7iu', period)
        f7iv = foyer_fiscal('f7iv', period)
        f7iw = foyer_fiscal('f7iw', period)
        f7ix = foyer_fiscal('f7ix', period)
        f7iz = foyer_fiscal('f7iz', period)
        P = parameters(period).impot_revenu.reductions_impots.locmeu

        m18 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                min_(P.max, maxi(f7id, f7ie, f7if, f7ig)) * (P.taux18 * m18 + P.taux11 * not_(m18)) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik + f7ip, f7ir + f7iq) +
            f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iz)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2013
        '''
        f7ia = foyer_fiscal('f7ia', period)
        f7ib = foyer_fiscal('f7ib', period)
        f7ic = foyer_fiscal('f7ic', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie', period)
        f7if = foyer_fiscal('f7if', period)
        f7ig = foyer_fiscal('f7ig', period)
        f7ih = foyer_fiscal('f7ih', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io', period)
        f7ip = foyer_fiscal('f7ip', period)
        f7iq = foyer_fiscal('f7iq', period)
        f7ir = foyer_fiscal('f7ir', period)
        f7is = foyer_fiscal('f7is', period)
        f7it = foyer_fiscal('f7it', period)
        f7iu = foyer_fiscal('f7iu', period)
        f7iv = foyer_fiscal('f7iv', period)
        f7iw = foyer_fiscal('f7iw', period)
        f7ix = foyer_fiscal('f7ix', period)
        f7iy = foyer_fiscal('f7iy', period)
        f7iz = foyer_fiscal('f7iz', period)
        f7jc = foyer_fiscal('f7jc', period)
        f7ji = foyer_fiscal('f7ji', period)
        f7js = foyer_fiscal('f7js', period)
        f7jt = foyer_fiscal('f7jt', period)
        f7ju = foyer_fiscal('f7ju', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        P = parameters(period).impot_revenu.reductions_impots.locmeu

        m18 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                min_(P.max, maxi(f7id, f7ie, f7if, f7ig)) * (P.taux18 * m18 + P.taux11 * not_(m18)) +
                P.taux11 * min_(P.max, f7jt + f7ju) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik + f7ip, f7ir + f7iq) +
            f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iy + f7iz + f7jv + f7jw + f7jx + f7jy + f7jc +
                f7ji + f7js)


class mohist(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"mohist"
    definition_period = YEAR

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de conservation et de restauration d’objets classés monuments historiques (case NZ)
        2008-
        '''
        f7nz = foyer_fiscal('f7nz', period)
        P = parameters(period).impot_revenu.reductions_impots.mohist

        return P.taux * min_(f7nz, P.max)


class patnat(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"patnat"
    definition_period = YEAR
    end = '2013-12-31'

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA)
        2010
        '''
        f7ka = foyer_fiscal('f7ka', period)
        P = parameters(period).impot_revenu.reductions_impots.patnat

        max1 = P.max
        return P.taux * min_(f7ka, max1)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB)
        2011
        '''
        f7ka = foyer_fiscal('f7ka', period)
        f7kb = foyer_fiscal('f7kb', period)
        P = parameters(period).impot_revenu.reductions_impots.patnat

        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2012
        '''
        f7ka = foyer_fiscal('f7ka', period)
        f7kb = foyer_fiscal('f7kb', period)
        f7kc = foyer_fiscal('f7kc', period)
        P = parameters(period).impot_revenu.reductions_impots.patnat

        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb + f7kc

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2013
        '''
        f7ka = foyer_fiscal('f7ka', period)
        f7kb = foyer_fiscal('f7kb', period)
        f7kc = foyer_fiscal('f7kc', period)
        f7kd = foyer_fiscal('f7kd', period)
        P = parameters(period).impot_revenu.reductions_impots.patnat

        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb + f7kc + f7kd


class prcomp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prestations compensatoires"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Prestations compensatoires
        '''
        f7wm = foyer_fiscal('f7wm', period)
        f7wn = foyer_fiscal('f7wn', period)
        f7wo = foyer_fiscal('f7wo', period)
        f7wp = foyer_fiscal('f7wp', period)
        P = parameters(period).impot_revenu.reductions_impots.prcomp

        div = (f7wo == 0) * 1 + f7wo  # Pour éviter les divisions par zéro

        return (
            (f7wm == 0) * (
                (f7wn == f7wo) * P.taux * min_(f7wn, P.seuil) +
                (f7wn < f7wo) * (f7wo <= P.seuil) * P.taux * f7wn +
                max_(0, (f7wn < f7wo) * (f7wo > P.seuil) * P.taux * P.seuil * f7wn / div)
                ) +
            (f7wm != 0) * (
                (f7wn == f7wm) * (f7wo <= P.seuil) * P.taux * f7wm +
                max_(0, (f7wn == f7wm) * (f7wo >= P.seuil) * P.taux * f7wm / div) +
                (f7wn > f7wm) * (f7wo <= P.seuil) * P.taux * f7wn +
                max_(0, (f7wn > f7wm) * (f7wo >= P.seuil) * P.taux * f7wn / div)
                ) +
            P.taux * f7wp
            )


class reduction_impot_exceptionnelle(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Réduction d'impôt exceptionnelle"
    end = '2013-12-31'
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        nb_adult = foyer_fiscal('nb_adult', period)
        nbptr = foyer_fiscal('nbptr', period)
        rfr = foyer_fiscal('rfr', period)
        params = parameters(period).impot_revenu.reductions_impots.reduction_impot_exceptionnelle
        plafond = params.seuil * nb_adult + (nbptr - nb_adult) * 2 * params.majoration_seuil
        montant = params.montant_plafond * nb_adult
        return min_(max_(plafond + montant - rfr, 0), montant)


class repsoc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"repsoc"
    definition_period = YEAR

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Intérèts d'emprunts pour reprises de société
        2003-
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7fh = foyer_fiscal('f7fh', period)
        P = parameters(period).impot_revenu.reductions_impots.repsoc

        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(f7fh, seuil)


class resimm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"resimm"
    definition_period = YEAR
    end = '2013-12-31'


    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA et 7RB)
        2009-2010
        '''
        f7ra = foyer_fiscal('f7ra', period)
        f7rb = foyer_fiscal('f7rb', period)
        P = parameters(period).impot_revenu.reductions_impots.resimm

        max1 = P.max
        max2 = max_(max1 - f7rb, 0)
        return P.taux_rb * min_(f7rb, max1) + P.taux_ra * min_(f7ra, max2)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD)
        2011
        '''
        f7ra = foyer_fiscal('f7ra', period)
        f7rb = foyer_fiscal('f7rb', period)
        f7rc = foyer_fiscal('f7rc', period)
        f7rd = foyer_fiscal('f7rd', period)
        P = parameters(period).impot_revenu.reductions_impots.resimm

        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7rc, max3) +
                P.taux_ra * min_(f7ra, max4))

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF)
        2012
        '''
        f7ra = foyer_fiscal('f7ra', period)
        f7rb = foyer_fiscal('f7rb', period)
        f7rc = foyer_fiscal('f7rc', period)
        f7rd = foyer_fiscal('f7rd', period)
        f7re = foyer_fiscal('f7re', period)
        f7rf = foyer_fiscal('f7rf', period)
        P = parameters(period).impot_revenu.reductions_impots.resimm

        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7rc + f7rf, max3) +
                P.taux_ra * min_(f7ra, max4) + P.taux_re * min_(f7re, max5))

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF, 7SX, 7SY)
        2012
        '''
        f7ra = foyer_fiscal('f7ra', period)
        f7rb = foyer_fiscal('f7rb', period)
        f7rc = foyer_fiscal('f7rc', period)
        f7rd = foyer_fiscal('f7rd', period)
        f7re = foyer_fiscal('f7re', period)
        f7rf = foyer_fiscal('f7rf', period)
        f7sx = foyer_fiscal('f7sx', period)
        f7sy = foyer_fiscal('f7sy', period)
        P = parameters(period).impot_revenu.reductions_impots.resimm

        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7sy - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7sy + f7rf + f7rc, max3) +
                P.taux_ra * min_(f7ra, max4) + P.taux_re * min_(f7re + f7sx, max5))


class rsceha(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"rsceha"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Rentes de survie et contrats d'épargne handicap
        2002-
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        nbR = foyer_fiscal('nbR', period)
        f7gz = foyer_fiscal('f7gz', period)
        P = parameters(period).impot_revenu.reductions_impots.rsceha

        max1 = P.seuil1 + (nb_pac2 - nbR) * P.seuil2
        return P.taux * min_(f7gz, max1)


class saldom(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"saldom"
    definition_period = YEAR
    end = '2013-12-31'


    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2002-2004
        '''
        f7df = foyer_fiscal('f7df', period)
        f7dg = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        max1 = P.max1 * not_(isinvalid) + P.max3 * isinvalid
        return P.taux * min_(f7df, max1)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2005-2006
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        f7dg = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        max1 = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        return P.taux * min_(f7df, max1)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2007-2008
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        f7dg = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
        return P.taux * min_(f7df, max1)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2009-2013
        '''
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        f7dq = foyer_fiscal('f7dq', period)
        f7dg = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.reductions_impots.salarie_domicile

        isinvalid = f7dg
        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
        return P.taux * min_(f7df, max1)


class scelli(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"scelli"
    definition_period = YEAR
    end = '2013-12-31'


    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier (cases 7HJ et 7HK)
        2009
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        P = parameters(period).impot_revenu.reductions_impots.scelli

        return max_(P.taux1 * min_(P.max, f7hj), P.taux2 * min_(P.max, f7hk)) / 9

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2010
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho', period)
        f7hl = foyer_fiscal('f7hl', period)
        f7hm = foyer_fiscal('f7hm', period)
        f7hr = foyer_fiscal('f7hr', period)
        f7hs = foyer_fiscal('f7hs', period)
        f7la = foyer_fiscal('f7la', period)
        P = parameters(period).impot_revenu.reductions_impots.scelli

        return (max_(
                    max_(P.taux1 * min_(P.max, f7hj),
                    P.taux2 * min_(P.max, f7hk)),
                    max_(P.taux1 * min_(P.max, f7hn),
                    P.taux2 * min_(P.max, f7ho))) / 9 +
                max_(
                    P.taux1 * min_(P.max, f7hl),
                    P.taux2 * min_(P.max, f7hm)) / 9 +
                max_(P.taux1 * f7hr, P.taux2 * f7hs) +
                f7la)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2011
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl', period)
        f7hm = foyer_fiscal('f7hm', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho', period)
        f7hr = foyer_fiscal('f7hr', period)
        f7hs = foyer_fiscal('f7hs', period)
        f7ht = foyer_fiscal('f7ht', period)
        f7hu = foyer_fiscal('f7hu', period)
        f7hv = foyer_fiscal('f7hv', period)
        f7hw = foyer_fiscal('f7hw', period)
        f7hx = foyer_fiscal('f7hx', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7na = foyer_fiscal('f7na', period)
        f7nb = foyer_fiscal('f7nb', period)
        f7nc = foyer_fiscal('f7nc', period)
        f7nd = foyer_fiscal('f7nd', period)
        f7ne = foyer_fiscal('f7ne', period)
        f7nf = foyer_fiscal('f7nf', period)
        f7ng = foyer_fiscal('f7ng', period)
        f7nh = foyer_fiscal('f7nh', period)
        f7ni = foyer_fiscal('f7ni', period)
        f7nj = foyer_fiscal('f7nj', period)
        f7nk = foyer_fiscal('f7nk', period)
        f7nl = foyer_fiscal('f7nl', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.reductions_impots.scelli

        return (min_(P.max, maxi(
                    P.taux13 * max_(f7nf, f7nj) / 9,
                    P.taux15 * max_(f7ng, f7ni) / 9,
                    P.taux22 * max_(f7na, f7ne) / 9,
                    P.taux1 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
                    P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
                    P.taux2 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5))) +
                min_(P.max, maxi(
                    P.taux1 * max_(f7hj, f7hn),
                    P.taux2 * max_(f7hk, f7ho))) / 9 +
                min_(P.max, max_(P.taux1 * f7hl, P.taux2 * f7hm)) / 9 +
                min_(P.max, maxi(P.taux1 * f7hv, P.taux1 * f7hx, P.taux2 * f7hw, P.taux2 * f7hz)) +
                min_(P.max, max_(P.taux1 * f7ht, P.taux2 * f7hu)) +
                min_(P.max, max_(P.taux1 * f7hr, P.taux2 * f7hs)) +
                f7la + f7lb + f7lc
                )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2012
        '''
        f7ha = foyer_fiscal('f7ha', period)
        f7hb = foyer_fiscal('f7hb', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7he = foyer_fiscal('f7he', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl', period)
        f7hm = foyer_fiscal('f7hm', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho', period)
        f7hr = foyer_fiscal('f7hr', period)
        f7hs = foyer_fiscal('f7hs', period)
        f7ht = foyer_fiscal('f7ht', period)
        f7hu = foyer_fiscal('f7hu', period)
        f7hv = foyer_fiscal('f7hv', period)
        f7hw = foyer_fiscal('f7hw', period)
        f7hx = foyer_fiscal('f7hx', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja', period)
        f7jb = foyer_fiscal('f7jb', period)
        f7jd = foyer_fiscal('f7jd', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm', period)
        f7jn = foyer_fiscal('f7jn', period)
        f7jo = foyer_fiscal('f7jo', period)
        f7jp = foyer_fiscal('f7jp', period)
        f7jq = foyer_fiscal('f7jq', period)
        f7jr = foyer_fiscal('f7jr', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7na = foyer_fiscal('f7na', period)
        f7nb = foyer_fiscal('f7nb', period)
        f7nc = foyer_fiscal('f7nc', period)
        f7nd = foyer_fiscal('f7nd', period)
        f7ne = foyer_fiscal('f7ne', period)
        f7nf = foyer_fiscal('f7nf', period)
        f7ng = foyer_fiscal('f7ng', period)
        f7nh = foyer_fiscal('f7nh', period)
        f7ni = foyer_fiscal('f7ni', period)
        f7nj = foyer_fiscal('f7nj', period)
        f7nk = foyer_fiscal('f7nk', period)
        f7nl = foyer_fiscal('f7nl', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.reductions_impots.scelli

        return (min_(P.max, maxi(
                    P.taux13 * max_(f7nf, f7nj) / 9,
                    P.taux15 * max_(f7ng, f7ni) / 9,
                    P.taux22 * max_(f7na, f7ne) / 9,
                    P.taux1 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
                    P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
                    P.taux2 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5))) +
                min_(P.max, maxi(
                    P.taux1 * max_(f7hj, f7hn),
                    P.taux2 * max_(f7hk, f7ho))) / 9 +
                min_(P.max, max_(P.taux1 * f7hl, P.taux2 * f7hm)) / 9 +
                min_(P.max, maxi(P.taux1 * f7hv, P.taux1 * f7hx, P.taux2 * f7hw, P.taux2 * f7hz)) +
                min_(P.max, max_(P.taux1 * f7ht, P.taux2 * f7hu)) +
                min_(P.max, max_(P.taux1 * f7hr, P.taux2 * f7hs)) +
                f7la + f7lb + f7lc + f7ld + f7le + f7lf +
                f7ha + f7hb + f7hg + f7hh + f7hd + f7he + f7hf +
                min_(P.max, maxi(
                    P.taux6 * max_(f7jf, f7jj) / 9,
                    P.taux13 * maxi(f7ja, f7je, f7jg, f7jh) / 9,
                    P.taux22 * maxi(f7jb, f7jd) / 9,
                    P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5),
                    P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5)))
                )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2013
        '''
        f7fa = foyer_fiscal('f7fa', period)
        f7fb = foyer_fiscal('f7fb', period)
        f7fc = foyer_fiscal('f7fc', period)
        f7fd = foyer_fiscal('f7fd', period)
        f7gj = foyer_fiscal('f7gj', period)
        f7gk = foyer_fiscal('f7gk', period)
        f7gl = foyer_fiscal('f7gl', period)
        f7gp = foyer_fiscal('f7gp', period)
        f7gs = foyer_fiscal('f7gs', period)
        f7gt = foyer_fiscal('f7gt', period)
        f7gu = foyer_fiscal('f7gu', period)
        f7gv = foyer_fiscal('f7gv', period)
        f7gw = foyer_fiscal('f7gw', period)
        f7gx = foyer_fiscal('f7gx', period)
        f7ha = foyer_fiscal('f7ha', period)
        f7hb = foyer_fiscal('f7hb', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7he = foyer_fiscal('f7he', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl', period)
        f7hm = foyer_fiscal('f7hm', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho', period)
        f7hr = foyer_fiscal('f7hr', period)
        f7hs = foyer_fiscal('f7hs', period)
        f7ht = foyer_fiscal('f7ht', period)
        f7hu = foyer_fiscal('f7hu', period)
        f7hv = foyer_fiscal('f7hv', period)
        f7hw = foyer_fiscal('f7hw', period)
        f7hx = foyer_fiscal('f7hx', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja', period)
        f7jb = foyer_fiscal('f7jb', period)
        f7jd = foyer_fiscal('f7jd', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm', period)
        f7jn = foyer_fiscal('f7jn', period)
        f7jo = foyer_fiscal('f7jo', period)
        f7jp = foyer_fiscal('f7jp', period)
        f7jq = foyer_fiscal('f7jq', period)
        f7jr = foyer_fiscal('f7jr', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7lm = foyer_fiscal('f7lm', period)
        f7ls = foyer_fiscal('f7ls', period)
        f7lz = foyer_fiscal('f7lz', period)
        f7mg = foyer_fiscal('f7mg', period)
        f7na = foyer_fiscal('f7na', period)
        f7nb = foyer_fiscal('f7nb', period)
        f7nc = foyer_fiscal('f7nc', period)
        f7nd = foyer_fiscal('f7nd', period)
        f7ne = foyer_fiscal('f7ne', period)
        f7nf = foyer_fiscal('f7nf', period)
        f7ng = foyer_fiscal('f7ng', period)
        f7nh = foyer_fiscal('f7nh', period)
        f7ni = foyer_fiscal('f7ni', period)
        f7nj = foyer_fiscal('f7nj', period)
        f7nk = foyer_fiscal('f7nk', period)
        f7nl = foyer_fiscal('f7nl', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.reductions_impots.scelli

        return (min_(P.max, maxi(
                    P.taux13 * max_(f7nf, f7nj) / 9,
                    P.taux15 * max_(f7ng, f7ni) / 9,
                    P.taux22 * max_(f7na, f7ne) / 9,
                    P.taux1 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
                    P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
                    P.taux2 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5))) +
                min_(P.max, maxi(
                    P.taux1 * max_(f7hj, f7hn),
                    P.taux2 * max_(f7hk, f7ho))) / 9 +
                min_(P.max, max_(P.taux1 * f7hl, P.taux2 * f7hm)) / 9 +
                min_(P.max, maxi(P.taux1 * f7hv, P.taux1 * f7hx, P.taux2 * f7hw, P.taux2 * f7hz)) +
                min_(P.max, max_(P.taux1 * f7ht, P.taux2 * f7hu)) +
                min_(P.max, max_(P.taux1 * f7hr, P.taux2 * f7hs)) +
                min_(P.max, maxi(
                    P.taux6 * maxi(f7jf, f7jj, f7fb) / 9,
                    P.taux13 * maxi(f7ja, f7je, f7jg, f7jh, f7fa) / 9,
                    P.taux22 * maxi(f7jb, f7jd) / 9,
                    P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5, f7fc / 9, f7fd / 5),
                    P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5))) +
                f7la + f7lb + f7lc + f7ld + f7le + f7lf + f7lm + f7ls + f7lz + f7mg +
                f7ha + f7hb + f7hg + f7hh + f7hd + f7he + f7hf +
                f7gj + f7gk + f7gl + f7gp + f7gs + f7gt + f7gu + f7gv + f7gx + f7gw
                )


class sofica(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"sofica"
    definition_period = YEAR

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital de SOFICA
        2006-
        '''
        f7gn = foyer_fiscal('f7gn', period)
        f7fn = foyer_fiscal('f7fn', period)
        rng = foyer_fiscal('rng', period)
        P = parameters(period).impot_revenu.reductions_impots.sofica

        max0 = min_(P.taux1 * max_(rng, 0), P.max)
        max1 = max_(0, max0 - f7gn)
        return P.taux2 * min_(f7gn, max0) + P.taux3 * min_(f7fn, max1)


class sofipe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"sofipe"
    end = '2011-01-01'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Souscription au capital d’une SOFIPECHE (case 7GS)
        2009-2011
        """
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        f7gs = foyer_fiscal('f7gs', period)
        P = parameters(period).impot_revenu.reductions_impots.sofipe

        max1 = min_(P.max * (maries_ou_pacses + 1), P.base * rbg_int)  # page3 ligne 18
        return P.taux * min_(f7gs, max1)


class spfcpi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"spfcpi"
    definition_period = YEAR
    end = '2014-12-31'


    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2002
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        P = parameters(period).impot_revenu.reductions_impots.spfcpi

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return P.taux1 * min_(f7gq, max1)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2003-2006
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        P = parameters(period).impot_revenu.reductions_impots.spfcpi

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return (P.taux1 * min_(f7gq, max1) + P.taux1 * min_(f7fq, max1))

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2007-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7fm = foyer_fiscal('f7fm', period)
        P = parameters(period).impot_revenu.reductions_impots.spfcpi

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return (P.taux1 * min_(f7gq, max1) +
                    P.taux1 * min_(f7fq, max1) +
                    P.taux2 * min_(f7fm, max1))

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2011-2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7fm = foyer_fiscal('f7fm', period)
        f7fl = foyer_fiscal('f7fl', period)
        P = parameters(period).impot_revenu.reductions_impots.spfcpi

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return (P.taux1 * min_(f7gq, max1) + P.taux1 * min_(f7fq, max1) + P.taux2 * min_(f7fm, max1) +
                P.taux3 * min_(f7fl, max1))

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2014
        '''
        f7gq = foyer_fiscal('f7gq', period)

        return f7gq * 0


def mini(a, b, *args):
    if not args:
        return min_(a, b)
    else:
        return min_(a, mini(b, *args))


def maxi(a, b, *args):
    if not args:
        return max_(a, b)
    else:
        return max_(a, maxi(b, *args))
