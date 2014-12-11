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

from numpy import minimum as min_, maximum as max_, logical_not as not_, ones, size, around

from .base import *


log = logging.getLogger(__name__)


@reference_formula
class reductions(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"reductions"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, adhcga, assvie, cappme, cotsyn, dfppce, daepad, doment, domlog, donapd, ecpess, garext, intemp, invfor, invrev, ip_net, prcomp, rsceha, saldom, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2002
        '''
        total_reductions = (adhcga + assvie + cappme + cotsyn + dfppce + daepad + doment + domlog + donapd + ecpess +
                garext + intemp + invfor + invrev + prcomp + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2003, 1, 1), stop = date(2004, 12, 31))
    def function_20030101_20041231(self, adhcga, assvie, cappme, cotsyn, dfppce, daepad, doment, domlog, donapd, ecpess, garext, intemp, invfor, invrev, ip_net, prcomp, repsoc, rsceha, saldom, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2003 et 2004
        '''
        total_reductions = (adhcga + assvie + cappme + cotsyn + dfppce + daepad + doment + domlog + donapd + ecpess +
                garext + intemp + invfor + invrev + prcomp + repsoc + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, adhcga, cappme, cotsyn, daepad, dfppce, doment, domlog, donapd, ecpess, intagr, intcon, invfor, invlst, ip_net, prcomp, repsoc, rsceha, saldom, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2005
        '''
        total_reductions = (adhcga + cappme + cotsyn + daepad + dfppce + doment + domlog + donapd + ecpess + intagr +
                intcon + invfor + invlst + prcomp + repsoc + rsceha + saldom + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, donapd, ecpess, intagr, invfor, invlst, ip_net, prcomp, repsoc, rsceha, saldom, sofica, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2006
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, donapd, ecpess, intagr, invfor, invlst, ip_net, prcomp, repsoc, rsceha, saldom, sofica, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2007
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)
    
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, donapd, ecpess, intagr, invfor, invlst, ip_net, mohist, prcomp, repsoc, rsceha, saldom, sofica, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2008
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        ecpess + intagr + invfor + invlst + mohist + prcomp + repsoc + rsceha + saldom + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, domsoc, donapd, ecodev, ecpess, intagr, invfor, invlst, ip_net, locmeu, mohist, prcomp, repsoc, resimm, rsceha, saldom, scelli, sofica, sofipe, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2009
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecodev + ecpess + intagr + invfor + invlst + locmeu + mohist + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, domsoc, donapd, ecpess, intagr, invfor, invlst, ip_net, locmeu, mohist, patnat, prcomp, repsoc, resimm, rsceha, saldom, scelli, sofica, sofipe, spfcpi):  # TODO: check (sees checked) and report in Niches.xls
        # TODO: check (sees checked) and report in Niches.xls
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2010
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)  # TODO: check (sees checked) and report in Niches.xls
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, adhcga, cappme, cotsyn, creaen, daepad, deffor, dfppce, doment, domlog, domsoc, donapd, ecpess, intagr, invfor, invlst, ip_net, locmeu, mohist, patnat, prcomp, repsoc, resimm, rsceha, saldom, scelli, sofica, sofipe, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2011
        '''
        total_reductions = (adhcga + cappme + cotsyn + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + sofipe + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, adhcga, cappme, creaen, daepad, deffor, dfppce, doment, domlog, domsoc, donapd, ecpess, intagr, invfor, invlst, ip_net, locmeu, mohist, patnat, prcomp, repsoc, resimm, rsceha, saldom, scelli, sofica, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2012
        '''
        total_reductions = (adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + domsoc +
        donapd + ecpess + intagr + invfor + invlst + locmeu + mohist + patnat + prcomp + repsoc + resimm + rsceha +
        saldom + scelli + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 1, 1))
    def function_20130101_20130101(self, accult, adhcga, cappme, creaen, daepad, deffor, dfppce, doment, domlog, donapd, duflot, ecpess, garext, intagr, invfor, invlst, ip_net, locmeu, mecena, mohist, patnat, prcomp, repsoc, resimm, rsceha, saldom, scelli, sofica, spfcpi):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2013
        '''
        total_reductions = (accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + donapd +
        duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist +
        patnat + prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi)
        return min_(ip_net, total_reductions)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

























#pour tous les dfppce:
    # : note de bas de page
    # TODO: plafonnement pour parti politiques depuis 2012 P.ir.reductions_impots.dfppce.max_niv


@reference_formula
class adhcga(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"adhcga"

    def function(self, f7ff, f7fg, P =  law.ir.reductions_impots.adhcga):
        '''
        Frais de comptabilité et d'adhésion à un CGA ou AA
        2002-
        '''
        return min_(f7ff, P.max * f7fg)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class assvie(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"assvie"
    start_date = date(2002, 1, 1)
    stop_date = date(2004, 12, 31)

    def function(self, nb_pac, f7gw, f7gx, f7gy, P =  law.ir.reductions_impots.assvie):
        '''
        Assurance-vie (cases GW, GX et GY de la 2042)
        2002-2004
        '''
        max1 = P.max + nb_pac * P.pac
        return P.taux * min_(f7gw + f7gx + f7gy, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cappme(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cappme"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, marpac, f7cf, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2002
        '''
        base = f7cf
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(base, seuil)

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_20030101_20031231(self, marpac, f7cf, f7cl, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2003
        '''
        base = f7cf + f7cl
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(base, seuil)

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_20040101_20041231(self, marpac, f7cf, f7cl, f7cm, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2004
        '''
        base = f7cf + f7cl + f7cm
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(base, seuil)

    @dated_function(start = date(2005, 1, 1), stop = date(2008, 12, 31))
    def function_20050101_20081231(self, marpac, f7cf, f7cl, f7cm, f7cn, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2005-2008
        '''
        base = f7cf + f7cl + f7cm + f7cn
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(base, seuil)

    @dated_function(start = date(2009, 1, 1), stop = date(2010, 12, 31))
    def function_20090101_20101231(self, marpac, f7cf, f7cl, f7cm, f7cn, f7cu, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2009-2010
        '''
        base = f7cf + f7cl + f7cm + f7cn + f7cu
        seuil = P.seuil * (marpac + 1)
        seuil = P.seuil_tpe * (marpac + 1) * (f7cu > 0) + P.seuil * (marpac + 1) * (f7cu <= 0)
        return P.taux * min_(base, seuil)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, marpac, f7cf, f7cl, f7cm, f7cn, f7cq, f7cu, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2011
        '''
        base = f7cl + f7cm + f7cn + f7cq
        seuil = P.seuil_tpe * (marpac + 1) * (f7cu > 0) + P.seuil * (marpac + 1) * (f7cu <= 0)
        max0 = max_(seuil - base, 0)
        return max_(P.taux25 * min_(base, seuil), P.taux * min_(max0, f7cf + f7cu))

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, marpac, f7cf, f7cl, f7cm, f7cn, f7cq, f7cu, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2012 cf. 2041 GR
        '''
        #TODO: gérer les changements de situation familiale
        base = f7cl + f7cm + f7cn
        seuil1 = P.seuil * (marpac + 1)
        seuil2 = max_(0, P.seuil_tpe * (marpac + 1) - min_(base, seuil1) - min_(f7cq, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (marpac + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)
        return P.taux25 * min_(base, seuil1) + P.taux * min_(f7cq, seuil1) + P.taux18 * (min_(f7cf, seuil3) +
                mini(f7cu, seuil2, seuil1))

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, marpac, f7cc, f7cf, f7cl, f7cm, f7cn, f7cq, f7cu, _P, P =  law.ir.reductions_impots.cappme):
        '''
        Souscriptions au capital des PME
        2013
        '''
        base = f7cl + f7cm
        seuil1 = P.seuil * (marpac + 1)
        seuil2 = max_(0, P.seuil_tpe * (marpac + 1) - min_(base, seuil1) - min_(f7cn, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (marpac + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)
        return P.taux25 * min_(base, seuil1) + P.taux22 * min_(f7cn, seuil1) + P.taux18 * (min_(f7cf + f7cc, seuil3) +
                min_(f7cu + f7cq, seuil2))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')











#TODO: vérifier l'existence du "max_"





@reference_formula
class cotsyn(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cotsyn"

    def function(self, f7ac_holder, sal_holder, cho_holder, rst_holder, P =  law.ir.reductions_impots.cotsyn):
        # becomes a credit d'impot in 2012
            # TODO: change f7ac and use split_by_roles
        '''
        Cotisations syndicales (2002-20131
        '''
        f7ac = self.filter_role(f7ac_holder, role = VOUS)
        f7ae = self.filter_role(f7ac_holder, role = CONJ)
        f7ag = self.filter_role(f7ac_holder, role = PAC1)

        cho = self.split_by_roles(cho_holder)
        rst = self.split_by_roles(rst_holder)
        sal = self.split_by_roles(sal_holder)

        tx = P.seuil

        salv, salc, salp = sal[VOUS], sal[CONJ], sal[PAC1]
        chov, choc, chop = cho[VOUS], cho[CONJ], cho[PAC1]
        rstv, rstc, rstp = rst[VOUS], rst[CONJ], rst[PAC1]
        maxv = (salv + chov + rstv) * tx
        maxc = (salc + choc + rstc) * tx
        maxp = (salp + chop + rstp) * tx

        return P.taux * (min_(f7ac, maxv) + min_(f7ae, maxc) + min_(f7ag, maxp))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class creaen(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"creaen"

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, f7fy, f7gy, _P, P =  law.ir.reductions_impots.creaen):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2006-2008
        '''
        return (P.base * f7fy + P.hand * f7gy)

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f7fy, f7gy, f7jy, f7hy, f7ky, f7iy, _P, P =  law.ir.reductions_impots.creaen):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2009
        '''
        return (P.base * ((f7jy + f7fy) + f7hy / 2) +
                    P.hand * ((f7ky + f7gy) + f7iy / 2))

    @dated_function(start = date(2010, 1, 1), stop = date(2011, 12, 31))
    def function_20100101_20111231(self, f7fy, f7gy, f7jy, f7hy, f7ky, f7iy, f7ly, f7my, _P, P =  law.ir.reductions_impots.creaen):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2010-2011
        '''
        return (P.base * ((f7jy + f7fy) + (f7hy + f7ly) / 2) +
                    P.hand * ((f7ky + f7gy) + (f7iy + f7my) / 2))

    @dated_function(start = date(2012, 1, 1), stop = date(2014, 12, 31))
    def function_20120101_20141231(self, f7ly, f7my, _P, P =  law.ir.reductions_impots.creaen):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2012-
        '''
        return (P.base * (f7ly / 2) +
                    P.hand * (f7my / 2))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')









@reference_formula
class deffor(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"deffor"
    start_date = date(2006, 1, 1)

    def function(self, f7uc, P =  law.ir.reductions_impots.deffor):
        '''
        Défense des forêts contre l'incendie
        2006-
        '''
        return P.taux * min_(f7uc, P.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class daepad(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"daepad"

    def function(self, f7cd, f7ce, P =  law.ir.reductions_impots.daepad):
        '''
        Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
        ?-
        '''
        return P.taux * (min_(f7cd, P.max) + min_(f7ce, P.max))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class dfppce(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"dfppce"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, rbg_int, f7uf, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_20040101_20041231(self, rbg_int, f7uf, f7xs, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf + f7xs
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, rbg_int, f7uf, f7xs, f7xt, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf + f7xs + f7xt
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, rbg_int, f7uf, f7xs, f7xt, f7xu, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf + f7xs + f7xt + f7xu
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf + f7xs + f7xt + f7xu + f7xw
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2008, 1, 1), stop = date(2010, 12, 31))
    def function_20080101_20101231(self, rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, _P, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        base = f7uf + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, f7vc, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, f7vc, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        base = min_(P.max_niv, f7uf) + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, rbg_int, f7uf, f7uh, f7xs, f7xt, f7xu, f7xw, f7xy, f7vc, P =  law.ir.reductions_impots.dfppce):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        base = min_(P.max_niv, f7uf + f7uh) + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.max * rbg_int
        return P.taux * min_(base, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')













    # TODO: note de bas de page
    #       Introduire plus de détails dans la déclaration pour séparer les dons aux partis poitiques
    #       et aux candidats des autres dons





# Outre-mer : TODO: plafonnement, cf. 2041-GE 2042-IOM
@reference_formula
class doment(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"doment"

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_20050101_20051231(self, f7ur, f7oz, f7pz, f7qz, f7rz):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return  f7ur + f7oz + f7pz + f7qz + f7rz

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, f7ur, f7oz, f7pz, f7qz, f7rz, f7sz):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return  f7ur + f7oz + f7pz + f7qz + f7rz + f7sz

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f7oz, f7pz, f7qz, f7rz, f7sz, f7qe, f7qf, f7qg, f7qh, f7qi, f7qj):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return  f7oz + f7pz + f7qz + f7rz + f7sz + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, f7oz, f7pz, f7qz, f7rz, f7qe, f7qf, f7qg, f7qh, f7qi, f7qj, f7qo, f7qp, f7qq, f7qr, f7qs, f7mm, f7ma, f7lg, f7ks, f7ls):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return (f7oz + f7pz + f7qz + f7rz + f7qe + f7qf + f7qg + f7qh + f7qi + f7qj + f7qo + f7qp + f7qq + f7qr + f7qs +
                    f7mm + f7ma + f7lg + f7ks + f7ls)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7ks, f7kt, f7ku, f7lg, f7lh, f7li, f7mm, f7ma, f7mb, f7mc, f7mn, f7oz, f7pa, f7pb, f7pd, f7pe, f7pf, f7ph, f7pi, f7pj, f7pl, f7pz, f7qz, f7qe, f7qf, f7qg, f7qh, f7qi, f7qo, f7qp, f7qq, f7qr, f7qv):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return (f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7mb + f7mn + f7mc + f7mm + f7ma +  f7oz + f7pa + f7pb + f7pd +
                    f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pz + f7qz + f7qf + f7qg + f7qh + f7qi + f7qo +
                    f7qp + f7qq + f7qr + f7qe + f7qv)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7ks, f7kt, f7ku, f7lg, f7lh, f7li, f7ma, f7mb, f7mc, f7mm, f7mn, f7nu, f7nv, f7nw, f7ny, f7pa, f7pb, f7pd, f7pe, f7pf, f7ph, f7pi, f7pj, f7pl, f7pm, f7pn, f7po, f7pp, f7pr, f7ps, f7pt, f7pu, f7pw, f7px, f7py, f7pz, f7qe, f7qf, f7qg, f7qi, f7qo, f7qp, f7qr, f7qv, f7qz, f7rg, f7ri, f7rj, f7rk, f7rl, f7rm, f7ro, f7rp, f7rq, f7rr, f7rt, f7ru, f7rv, f7rw, f7rx, f7ry):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return (f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7ma + f7mb + f7mc + f7mm + f7mn +  f7pz + f7nu + f7nv + f7nw +
                    f7ny + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi + f7pj + f7pl + f7pm + f7pn + f7po + f7pp + f7pr +
                    f7ps + f7pt + f7pu + f7pw + f7px + f7py + f7qe + f7qf + f7qg + f7qi + f7qo + f7qp + f7qr + f7qv + f7qz +
                    f7rg + f7ri + f7rj + f7rk + f7rl + f7rm + f7ro + f7rp + f7rq + f7rr + f7rt + f7ru + f7rv + f7rw)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, fhsa, fhsb, fhsf, fhsg, fhsc, fhsh, fhse, fhsj, fhsk, fhsl, fhsp, fhsq, fhsm, fhsr, fhso, fhst, fhsu, fhsv, fhsw, fhsz, fhta, fhtb, fhtd, f7ks, f7kt, f7ku, f7lg, f7lh, f7li, f7ma, f7mb, f7mc, f7mm, f7mn, f7nu, f7nv, f7nw, f7ny, f7pa, f7pb, f7pd, f7pe, f7pf, f7ph, f7pi, f7pj, f7pl, f7pm, f7pn, f7po, f7pp, f7pr, f7ps, f7pt, f7pu, f7pw, f7px, f7py, f7qe, f7qf, f7qg, f7qi, f7qo, f7qp, f7qr, f7qv, f7qz, f7rg, f7ri, f7rj, f7rk, f7rl, f7rm, f7ro, f7rp, f7rq, f7rr, f7rt, f7ru, f7rv, f7rw, f7ry):
        '''
        Investissements dans les DOM-TOM dans le cadre d'une entrepise.
        '''
        return (fhsa + fhsb + fhsf + fhsg + fhsc + fhsh + fhse + fhsj + fhsk + fhsl + fhsp + fhsq + fhsm + fhsr + fhso +
                    fhst + fhsu + fhsv + fhsw + fhsz + fhta + fhtb + fhtd + f7ks + f7kt + f7ku + f7lg + f7lh + f7li + f7ma +
                    f7mb + f7mc + f7mm + f7mn + f7nu + f7nv + f7nw + f7ny + f7pa + f7pb + f7pd + f7pe + f7pf + f7ph + f7pi +
                    f7pj + f7pl + f7pm + f7pn + f7po + f7pp + f7pr + f7ps + f7pt + f7pu + f7pw + f7px + f7py + f7qe + f7qf +
                    f7qg + f7qi + f7qo + f7qp + f7qr + f7qv + f7qz + f7rg + f7ri + f7rj + f7rk + f7rl + f7rm + f7ro + f7rp +
                    f7rq + f7rr + f7rt + f7ru + f7rv + f7rw)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



#TODO: vérifier pour 2002
#TODO: pb 7ul 2005-2009 (ITRED = 0 au lieu de 20€ (forfaitaire), dû à ça : Cochez [7UL] si vous déclarez en ligne pour
#la première fois vos revenus 2008 et si vous utilisez un moyen automatique de paiement (prélèvement mensuel ou à
#l'échéance ou paiement par voie électronique))









#TODO: vérifier les dates des variables de doment et domsoc (y sont-elles encore en 2013 par ex ?)

@reference_formula
class domlog(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"domlog"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, f7ua, f7ub, f7uc, f7uj, _P, P =  law.ir.reductions_impots.domlog):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2002
        '''
        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc)

    @dated_function(start = date(2003, 1, 1), stop = date(2004, 12, 31))
    def function_20030101_20041231(self, f7ua, f7ub, f7uc, f7ui, f7uj, _P, P =  law.ir.reductions_impots.domlog):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2003-2004
        '''
        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub + f7uc) + f7ui

    @dated_function(start = date(2005, 1, 1), stop = date(2007, 12, 31))
    def function_20050101_20071231(self, f7ua, f7ub, f7uc, f7ui, f7uj, _P, P =  law.ir.reductions_impots.domlog):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2005-2007
        '''
        return P.taux1 * f7uj + P.taux2 * (f7ua + f7ub) + f7ui

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_20080101_20081231(self, f7ui):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2008
        '''
        return f7ui

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f7qb, f7qc, f7qd, f7qk):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2009
        '''
        return f7qb + f7qc + f7qd + f7qk / 2

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, f7qb, f7qc, f7qd, f7ql, f7qt, f7qm):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2010
        TODO: Plafonnement sur la notice
        '''
        return f7qb + f7qc + f7qd + f7ql + f7qt + f7qm

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7qb, f7qc, f7qd, f7ql, f7qm, f7qt, f7oa, f7ob, f7oc, f7oh, f7oi, f7oj, f7ok):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2011
        TODO: Plafonnement sur la notice
        '''
        return f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7qb, f7qc, f7qd, f7ql, f7qm, f7qt, f7oa, f7ob, f7oc, f7oh, f7oi, f7oj, f7ok, f7ol, f7om, f7on, f7oo, f7op, f7oq, f7or, f7os, f7ot, f7ou, f7ov, f7ow):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2012
        TODO: Plafonnement sur la notice
        '''
        return (f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok + f7ol + f7om +
                    f7on + f7oo + f7op + f7oq + f7or + f7os + f7ot + f7ou + f7ov + f7ow)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, fhod, fhoe, fhof, fhog, fhox, fhoy, fhoz, f7qb, f7qc, f7qd, f7ql, f7qm, f7qt, f7oa, f7ob, f7oc, f7oh, f7oi, f7oj, f7ok, f7ol, f7om, f7on, f7oo, f7op, f7oq, f7or, f7os, f7ot, f7ou, f7ov, f7ow):
        '''
        Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
        2013
        TODO: Plafonnement sur la notice
        '''
        return (f7qb + f7qc + f7qd + f7ql + f7qm + f7qt + f7oa + f7ob + f7oc + f7oh + f7oi + f7oj + f7ok + f7ol + f7om +
                    f7on + f7oo + f7op + f7oq + f7or + f7os + f7ot + f7ou + f7ov + f7ow + fhod + fhoe +
                    fhof + fhog + fhox + fhoy + fhoz)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





#En accord avec la DGFiP mais pas de 7ub et 7uj dans la notice













@reference_formula
class domsoc(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"domsoc"

    @dated_function(start = date(2010, 1, 1), stop = date(2012, 12, 31))
    def function_20100101_20121231(self, f7qn, f7qk, f7qu, f7kg, f7kh, f7ki, f7qj, f7qs, f7qw, f7qx):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2010-
        TODO plafonnement à 15% f7qa / liens avec autres investissments ?
        '''
        return  f7qn + f7qk + f7qu + f7kg + f7kh + f7ki + f7qj + f7qs + f7qw + f7qx

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, fhra, fhrb, fhrc, fhrd, f7qn, f7qk, f7qu, f7kg, f7kh, f7ki, f7qj, f7qs, f7qw, f7qx):
        '''
        Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
        2013
        TODO plafonnement à 15% f7qa / liens avec autres investissments ?
        '''
        return  fhra + fhrb + fhrc + fhrd + f7qn + f7qk + f7qu + f7kg + f7kh + f7ki + f7qj + f7qs + f7qw + f7qx

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class donapd(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"donapd"

    @dated_function(start = date(2002, 1, 1), stop = date(2010, 12, 31))
    def function_20020101_20101231(self, f7ud, P =  law.ir.reductions_impots.donapd):
        '''
        Dons effectués à  des organises d'aide aux personnes en difficulté (2002-2010)
        '''
        return P.taux * min_(f7ud, P.max)

    @dated_function(start = date(2011, 1, 1), stop = date(2013, 12, 31))
    def function_20110101_20131231(self, f7ud, f7va, P =  law.ir.reductions_impots.donapd):
        '''
        Dons effectués à  des organises d'aide aux personnes en difficulté (2011-2013)
        '''
        return P.taux * min_(f7ud + f7va, P.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class duflot(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"duflot"
    start_date = date(2013, 1, 1)

    def function(self, f7gh, f7gi, P =  law.ir.reductions_impots.duflot):
        '''
        Investissements locatifs interméiaires (loi Duflot)
        2013-
        '''
        return min_(P.plafond, P.taux_m * f7gh + P.taux_om * f7gi) / 9

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

#TODO: / 5 dans trois TOM

@reference_formula
class ecodev(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ecodev"
    start_date = date(2009, 1, 1)
    stop_date = date(2009, 12, 31)

    def function(self, f7uh, rbg_int, P =  law.ir.reductions_impots.ecodev):
        '''
        Sommes versées sur un compte épargne codéveloppement (case 7UH)
        2009
        '''
        return min_(f7uh * P.taux, min_(P.base * rbg_int, P.max))  # page3 ligne 18

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ecpess(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ecpess"

    def function(self, f7ea, f7eb, f7ec, f7ed, f7ef, f7eg, P =  law.ir.reductions_impots.ecpess):
        '''
        Réduction d'impôt au titre des enfants à charge poursuivant leurs études secondaires ou supérieures
        '''
        return (P.col * (f7ea + f7eb / 2) +
                P.lyc * (f7ec + f7ed / 2) +
                P.sup * (f7ef + f7eg / 2))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class garext(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"garext"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, f7ga, f7gb, f7gc, _P, P =  law.ir.reductions_impots.garext):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2002
        '''
        max1 = P.max
        return P.taux * (min_(f7ga, max1) + min_(f7gb, max1) + min_(f7gc, max1))

    @dated_function(start = date(2003, 1, 1), stop = date(2005, 12, 31))
    def function_20030101_20051231(self, f7ga, f7gb, f7gc, f7ge, f7gf, f7gg, _P, P =  law.ir.reductions_impots.garext):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2003-2005
        '''
        max1 = P.max
        max2 = P.max / 2
        return P.taux * (min_(f7ga, max1) +
                           min_(f7gb, max1) +
                           min_(f7gc, max1) +
                           min_(f7ge, max2) +
                           min_(f7gf, max2) +
                           min_(f7gg, max2))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class intagr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"intagr"
    start_date = date(2005, 1, 1)

    def function(self, f7um, marpac, P =  law.ir.reductions_impots.intagr):
        '''
        Intérêts pour paiement différé accordé aux agriculteurs
        2005-
        '''
        max1 = P.max * (1 + marpac)
        return P.taux * min_(f7um, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class intcon(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"intcon"
    start_date = date(2004, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, f7uh, P =  law.ir.reductions_impots.intcon):
        '''
        Intérêts des prêts à la consommation (case UH)
        2004-2005
        '''
        max1 = P.max
        return P.taux * min_(f7uh, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class intemp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"intemp"
    start_date = date(2002, 1, 1)
    stop_date = date(2003, 12, 31)

    def function(self, nb_pac, f7wg, P =  law.ir.reductions_impots.intemp):
        '''
        Intérêts d'emprunts
        2002-2003
        '''
        max1 = P.max + P.pac * nb_pac
        return P.taux * min_(f7wg, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class invfor(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"invfor"

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, marpac, f7un, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2002-2005
        '''
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(f7un, seuil)

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, f7un, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2006-2008
        '''
        return P.taux * f7un

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, marpac, f7un, f7up, f7uq, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2009
        '''
        return P.taux * (min_(f7un, P.seuil * (marpac + 1)) + min_(f7up, P.ifortra_seuil * (marpac + 1)) +
                min_(f7uq, P.iforges_seuil * (marpac + 1)))

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, marpac, f7te, f7un, f7up, f7uq, f7uu, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2010
        '''
        return (P.taux * (
            min_(f7un, P.seuil * (marpac + 1)) +
            min_(f7up + f7uu + f7te, P.ifortra_seuil * (marpac + 1)) +
            min_(f7uq, P.iforges_seuil * (marpac + 1))))

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, marpac, f7te, f7tf, f7ul, f7un, f7up, f7uq, f7uu, f7uv, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2011 cf. 2041 GK
        '''
        max0 = max_(0, P.ifortra_seuil * (marpac + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        return (P.taux * (
            min_(f7un, P.seuil * (marpac + 1)) +
            min_(f7up, max1) +
            min_(f7uq, P.iforges_seuil * (marpac + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (marpac + 1)))

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, marpac, f7te, f7tf, f7tg, f7ul, f7un, f7up, f7uq, f7uu, f7uv, f7uw, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2012 cf. 2041 GK
        '''
        max0 = max_(0, P.ifortra_seuil * (marpac + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        max2 = max_(0, max1 - f7tg - f7uw)
        return (P.taux * (
            min_(f7un, P.seuil * (marpac + 1)) +
            min_(f7up, max2) +
            min_(f7uq, P.iforges_seuil * (marpac + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.report11 * min_(f7tg + f7uw, max1) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (marpac + 1)))

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, marpac, f7te, f7tf, f7tg, f7th, f7ul, f7un, f7up, f7uq, f7uu, f7uv, f7uw, f7ux, _P, P =  law.ir.reductions_impots.invfor):
        '''
        Investissements forestiers pour 2013 cf. 2041 GK
        '''
        max0 = max_(0, P.ifortra_seuil * (marpac + 1) - f7ul)
        max1 = max_(0, max0 - f7uu + f7te + f7uv + f7tf)
        max2 = max_(0, max1 - f7tg - f7uw)
        max3 = max_(0, max2 - f7th - f7ux)
        return (P.taux * (
            min_(f7un, P.seuil * (marpac + 1)) +
            min_(f7up, max3) +
            min_(f7uq, P.iforges_seuil * (marpac + 1))) +
            P.report10 * min_(f7uu + f7te + f7uv + f7tf, max0) +
            P.report11 * min_(f7tg + f7uw, max1) +
            P.report12 * min_(f7th + f7ux, max2) +
            P.taux_ass * min_(f7ul, P.ifortra_seuil * (marpac + 1)))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')















@reference_formula
class invlst(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"invlst"

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_20040101_20041231(self, marpac, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, _P, P =  law.ir.reductions_impots.invlst):
        '''
        Investissements locatifs dans le secteur touristique
        2004
        '''
        seuil1 = P.seuil1 * (1 + marpac)
        seuil2 = P.seuil2 * (1 + marpac)
        seuil3 = P.seuil3 * (1 + marpac)
    
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

    @dated_function(start = date(2005, 1, 1), stop = date(2010, 12, 31))
    def function_20050101_20101231(self, marpac, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, _P, P =  law.ir.reductions_impots.invlst):
        '''
        Investissements locatifs dans le secteur touristique
        2005-2010
        '''
        seuil1 = P.seuil1 * (1 + marpac)
        seuil2 = P.seuil2 * (1 + marpac)
        seuil3 = P.seuil3 * (1 + marpac)
    
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

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, marpac, f7xa, f7xb, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, f7xp, f7xq, f7xr, _P, P =  law.ir.reductions_impots.invlst):
        '''
        Investissements locatifs dans le secteur touristique
        2011
        '''
        seuil1 = P.seuil1 * (1 + marpac)
        seuil2 = P.seuil2 * (1 + marpac)
        seuil3 = P.seuil3 * (1 + marpac)
    
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

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, marpac, f7xa, f7xb, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, f7xp, f7xq, f7xr, f7xv, f7xx, f7xz, _P, P =  law.ir.reductions_impots.invlst):
        '''
        Investissements locatifs dans le secteur touristique
        2012
        '''
        seuil1 = P.seuil1 * (1 + marpac)
        seuil2 = P.seuil2 * (1 + marpac)
        seuil3 = P.seuil3 * (1 + marpac)
    
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

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, marpac, f7uy, f7uz, f7xf, f7xi, f7xj, f7xk, f7xm, f7xn, f7xo, f7xp, f7xq, f7xr, f7xv, _P, P =  law.ir.reductions_impots.invlst):
        '''
        Investissements locatifs dans le secteur touristique
        2013
        '''
    
        xi = P.taux_xi * (f7xf + f7xi + f7xp + f7xn + f7uy)
        xj = P.taux_xj * (f7xm + f7xj + f7xq + f7xv + f7uz)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)
    
        return around(xi + xj + xo)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')











@reference_formula
class invrev(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"invrev"
    start_date = date(2002, 1, 1)
    stop_date = date(2003, 12, 31)

    def function(self, marpac, f7gs, f7gt, f7xg, f7gu, f7gv, P =  law.ir.reductions_impots.invrev):
        '''
        Investissements locatifs dans les résidences de tourisme situées dans une zone de
        revitalisation rurale (cases GS, GT, XG, GU et GV)
        2002-2003
        TODO 1/4 codé en dur
        '''
        return (P.taux_gs * min_(f7gs, P.seuil_gs * (1 + marpac)) / 4 +
                 P.taux_gu * min_(f7gu, P.seuil_gu * (1 + marpac)) / 4 +
                 P.taux_xg * min_(f7xg, P.seuil_xg * (1 + marpac)) / 4 +
                 P.taux_gt * f7gt + P.taux_gt * f7gv)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class locmeu(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"locmeu"

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f7ij, P =  law.ir.reductions_impots.locmeu):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2009
        '''
        return P.taux * min_(P.max, f7ij) / 9

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, f7ij, f7ik, f7il, f7im, f7is, P =  law.ir.reductions_impots.locmeu):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2010
        '''
        return ((min_(P.max, max_(f7ij, f7il)) + min_(P.max, f7im)) / 9 + f7ik) * P.taux + f7is

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7ij, f7ik, f7il, f7im, f7in, f7io, f7ip, f7iq, f7ir, f7is, f7it, f7iu, f7iv, f7iw, P =  law.ir.reductions_impots.locmeu):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2011
        '''
        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik, f7ip + f7ir + f7iq) +
            f7is + f7iu + f7it)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7ia, f7ib, f7ic, f7id, f7ie, f7if, f7ig, f7ih, f7ij, f7ik, f7il, f7im, f7in, f7io, f7ip, f7iq, f7ir, f7is, f7it, f7iu, f7iv, f7iw, f7ix, f7iz, P =  law.ir.reductions_impots.locmeu):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2012
        '''
        m18 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                min_(P.max, maxi(f7id, f7ie, f7if, f7ig)) * (P.taux18 * m18 + P.taux11 * not_(m18)) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik + f7ip, f7ir + f7iq) +
            f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iz)

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f7ia, f7ib, f7ic, f7id, f7ie, f7if, f7ig, f7ih, f7ij, f7ik, f7il, f7im, f7in, f7io, f7ip, f7iq, f7ir, f7is, f7it, f7iu, f7iv, f7iw, f7ix, f7iy, f7iz, f7jc, f7ji, f7js, f7jt, f7ju, f7jv, f7jw, f7jx, f7jy, P =  law.ir.reductions_impots.locmeu):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2013
        '''
        m18 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        m20 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        return ((min_(P.max, maxi(f7ij, f7il, f7in, f7iv)) * (P.taux20 * m20 + P.taux18 * not_(m20)) +
                min_(P.max, maxi(f7id, f7ie, f7if, f7ig)) * (P.taux18 * m18 + P.taux11 * not_(m18)) +
                P.taux11 * min_(P.max, f7jt + f7ju) +
                P.taux * (min_(P.max, max_(f7im, f7iw)) + min_(P.max, f7io))) / 9 +
            P.taux * max_(f7ik + f7ip, f7ir + f7iq) +
            f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iy + f7iz + f7jv + f7jw + f7jx + f7jy + f7jc +
                f7ji + f7js)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')













@reference_formula
class mohist(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"mohist"
    start_date = date(2008, 1, 1)

    def function(self, f7nz, P =  law.ir.reductions_impots.mohist):
        '''
        Travaux de conservation et de restauration d’objets classés monuments historiques (case NZ)
        2008-
        '''
        return P.taux * min_(f7nz, P.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class patnat(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"patnat"

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, f7ka, P =  law.ir.reductions_impots.patnat):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA)
        2010
        '''
        max1 = P.max
        return P.taux * min_(f7ka, max1)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7ka, f7kb, P =  law.ir.reductions_impots.patnat):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB)
        2011
        '''
        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7ka, f7kb, f7kc, P =  law.ir.reductions_impots.patnat):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2012
        '''
        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb + f7kc

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f7ka, f7kb, f7kc, f7kd, P =  law.ir.reductions_impots.patnat):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2013
        '''
        max1 = P.max
        return P.taux * min_(f7ka, max1) + f7kb + f7kc + f7kd

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')









@reference_formula
class prcomp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"prcomp"

    def function(self, f7wm, f7wn, f7wo, f7wp, P =  law.ir.reductions_impots.prcomp):
        '''
        Prestations compensatoires
        2002-
        '''
        div = (f7wo == 0) * 1 + f7wo  # Pour éviter les divisions par zéro

        return ((f7wm == 0) * ((f7wn == f7wo) * P.taux * min_(f7wn, P.seuil) +
                                  (f7wn < f7wo) * (f7wo <= P.seuil) * P.taux * f7wn +
                                  max_(0, (f7wn < f7wo) * (f7wo > P.seuil) * P.taux * P.seuil * f7wn / div)) +
                (f7wm != 0) * ((f7wn == f7wm) * (f7wo <= P.seuil) * P.taux * f7wm +
                                  max_(0, (f7wn == f7wm) * (f7wo >= P.seuil) * P.taux * f7wm / div) +
                                  (f7wn > f7wm) * (f7wo <= P.seuil) * P.taux * f7wn +
                                  max_(0, (f7wn > f7wm) * (f7wo >= P.seuil) * P.taux * f7wn / div)) +
                 P.taux * f7wp)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class repsoc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"repsoc"
    start_date = date(2003, 1, 1)

    def function(self, marpac, f7fh, P =  law.ir.reductions_impots.repsoc):
        '''
        Intérèts d'emprunts pour reprises de société
        2003-
        '''
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(f7fh, seuil)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class resimm(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"resimm"

    @dated_function(start = date(2009, 1, 1), stop = date(2010, 12, 31))
    def function_20090101_20101231(self, f7ra, f7rb, P =  law.ir.reductions_impots.resimm):
        '''
        Travaux de restauration immobilière (cases 7RA et 7RB)
        2009-2010
        '''
        max1 = P.max
        max2 = max_(max1 - f7rb, 0)
        return P.taux_rb * min_(f7rb, max1) + P.taux_ra * min_(f7ra, max2)

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7ra, f7rb, f7rc, f7rd, P =  law.ir.reductions_impots.resimm):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD)
        2011
        '''
        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7rc, max3) +
                P.taux_ra * min_(f7ra, max4))

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7ra, f7rb, f7rc, f7rd, f7re, f7rf, P =  law.ir.reductions_impots.resimm):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF)
        2012
        '''
        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7rc + f7rf, max3) +
                P.taux_ra * min_(f7ra, max4) + P.taux_re * min_(f7re, max5))

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f7ra, f7rb, f7rc, f7rd, f7re, f7rf, f7sx, f7sy, P =  law.ir.reductions_impots.resimm):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF, 7SX, 7SY)
        2012
        '''
        max1 = P.max
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7sy - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)
        return (P.taux_rd * min_(f7rd, max1) + P.taux_rb * min_(f7rb, max2) + P.taux_rc * min_(f7sy + f7rf + f7rc, max3) +
                P.taux_ra * min_(f7ra, max4) + P.taux_re * min_(f7re + f7sx, max5))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')









@reference_formula
class rsceha(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rsceha"

    def function(self, nb_pac2, nbR, f7gz, P =  law.ir.reductions_impots.rsceha):
        '''
        Rentes de survie et contrats d'épargne handicap
        2002-
        '''
        max1 = P.seuil1 + (nb_pac2 - nbR) * P.seuil2
        return P.taux * min_(f7gz, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class saldom(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"saldom"

    @dated_function(start = date(2002, 1, 1), stop = date(2004, 12, 31))
    def function_20020101_20041231(self, f7df, f7dg, _P, P =  law.ir.reductions_impots.saldom):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2002-2004
        '''
        isinvalid = f7dg
        max1 = P.max1 * not_(isinvalid) + P.max3 * isinvalid
        return P.taux * min_(f7df, max1)

    @dated_function(start = date(2005, 1, 1), stop = date(2006, 12, 31))
    def function_20050101_20061231(self, nb_pac2, f7df, f7dl, f7dg, _P, P =  law.ir.reductions_impots.saldom):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2005-2006
        '''
        isinvalid = f7dg
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        max1 = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        return P.taux * min_(f7df, max1)

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, nb_pac2, f7db, f7df, f7dl, f7dg, _P, P =  law.ir.reductions_impots.saldom):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2007-2008
        '''
        isinvalid = f7dg
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
        return P.taux * min_(f7df, max1)

    @dated_function(start = date(2009, 1, 1), stop = date(2013, 12, 31))
    def function_20090101_20131231(self, nb_pac2, f7db, f7df, f7dl, f7dq, f7dg, _P, P =  law.ir.reductions_impots.saldom):
        '''
        Sommes versées pour l'emploi d'un salariés à  domicile
        2009-2013
        '''
        isinvalid = f7dg
        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
        return P.taux * min_(f7df, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')









@reference_formula
class scelli(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"scelli"

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_20090101_20091231(self, f7hj, f7hk, P =  law.ir.reductions_impots.scelli):
        '''
        Investissements locatif neufs : Dispositif Scellier (cases 7HJ et 7HK)
        2009
        '''
        return max_(P.taux1 * min_(P.max, f7hj), P.taux2 * min_(P.max, f7hk)) / 9

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_20100101_20101231(self, f7hj, f7hk, f7hn, f7ho, f7hl, f7hm, f7hr, f7hs, f7la, P =  law.ir.reductions_impots.scelli):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2010
        '''
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

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_20110101_20111231(self, f7hj, f7hk, f7hl, f7hm, f7hn, f7ho, f7hr, f7hs, f7ht, f7hu, f7hv, f7hw, f7hx, f7hz, f7la, f7lb, f7lc, f7na, f7nb, f7nc, f7nd, f7ne, f7nf, f7ng, f7nh, f7ni, f7nj, f7nk, f7nl, f7nm, f7nn, f7no, f7np, f7nq, f7nr, f7ns, f7nt, P =  law.ir.reductions_impots.scelli):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2011
        '''
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

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f7ha, f7hb, f7hg, f7hh, f7hd, f7he, f7hf, f7hj, f7hk, f7hl, f7hm, f7hn, f7ho, f7hr, f7hs, f7ht, f7hu, f7hv, f7hw, f7hx, f7hz, f7ja, f7jb, f7jd, f7je, f7jf, f7jg, f7jh, f7jj, f7jk, f7jl, f7jm, f7jn, f7jo, f7jp, f7jq, f7jr, f7la, f7lb, f7lc, f7ld, f7le, f7lf, f7na, f7nb, f7nc, f7nd, f7ne, f7nf, f7ng, f7nh, f7ni, f7nj, f7nk, f7nl, f7nm, f7nn, f7no, f7np, f7nq, f7nr, f7ns, f7nt, P =  law.ir.reductions_impots.scelli):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2012
        '''
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

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, f7fa, f7fb, f7fc, f7fd, f7gj, f7gk, f7gl, f7gp, f7gs, f7gt, f7gu, f7gv, f7gw, f7gx, f7ha, f7hb, f7hg, f7hh, f7hd, f7he, f7hf, f7hj, f7hk, f7hl, f7hm, f7hn, f7ho, f7hr, f7hs, f7ht, f7hu, f7hv, f7hw, f7hx, f7hz, f7ja, f7jb, f7jd, f7je, f7jf, f7jg, f7jh, f7jj, f7jk, f7jl, f7jm, f7jn, f7jo, f7jp, f7jq, f7jr, f7la, f7lb, f7lc, f7ld, f7le, f7lf, f7lm, f7ls, f7lz, f7mg, f7na, f7nb, f7nc, f7nd, f7ne, f7nf, f7ng, f7nh, f7ni, f7nj, f7nk, f7nl, f7nm, f7nn, f7no, f7np, f7nq, f7nr, f7ns, f7nt, P =  law.ir.reductions_impots.scelli):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2013
        '''
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

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')











@reference_formula
class sofica(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"sofica"
    start_date = date(2006, 1, 1)

    def function(self, f7gn, f7fn, rng, P =  law.ir.reductions_impots.sofica):
        '''
        Souscriptions au capital de SOFICA
        2006-
        '''
        max0 = min_(P.taux1 * max_(rng, 0), P.max)
        max1 = max_(0, max0 - f7gn)
        return P.taux2 * min_(f7gn, max0) + P.taux3 * min_(f7fn, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class sofipe(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"sofipe"
    start_date = date(2009, 1, 1)
    stop_date = date(2011, 1, 1)

    def function(self, marpac, rbg_int, f7gs, _P, P =  law.ir.reductions_impots.sofipe):
        """
        Souscription au capital d’une SOFIPECHE (case 7GS)
        2009-2011
        """
        max1 = min_(P.max * (marpac + 1), P.base * rbg_int)  # page3 ligne 18
        return P.taux * min_(f7gs, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class spfcpi(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"spfcpi"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, marpac, f7gq, _P, P =  law.ir.reductions_impots.spfcpi):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2002
        '''
        max1 = P.max * (marpac + 1)
        return P.taux1 * min_(f7gq, max1)

    @dated_function(start = date(2003, 1, 1), stop = date(2006, 12, 31))
    def function_20030101_20061231(self, marpac, f7gq, f7fq, _P, P =  law.ir.reductions_impots.spfcpi):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2003-2006
        '''
        max1 = P.max * (marpac + 1)
        return (P.taux1 * min_(f7gq, max1) + P.taux1 * min_(f7fq, max1))

    @dated_function(start = date(2007, 1, 1), stop = date(2010, 12, 31))
    def function_20070101_20101231(self, marpac, f7gq, f7fq, f7fm, _P, P =  law.ir.reductions_impots.spfcpi):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2007-2010
        '''
        max1 = P.max * (marpac + 1)
        return (P.taux1 * min_(f7gq, max1) +
                    P.taux1 * min_(f7fq, max1) +
                    P.taux2 * min_(f7fm, max1))

    @dated_function(start = date(2011, 1, 1), stop = date(2013, 12, 31))
    def function_20110101_20131231(self, marpac, f7gq, f7fq, f7fm, f7fl, _P, P =  law.ir.reductions_impots.spfcpi):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2011-2013
        '''
        max1 = P.max * (marpac + 1)
        return (P.taux1 * min_(f7gq, max1) + P.taux1 * min_(f7fq, max1) + P.taux2 * min_(f7fm, max1) +
                P.taux3 * min_(f7fl, max1))

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_20140101_20141231(self, f7gq):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2014
        '''
        return f7gq * 0

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')











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
