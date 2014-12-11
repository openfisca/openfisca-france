# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import logical_not as not_, minimum as min_, maximum as max_

from .base import *


log = logging.getLogger(__name__)


@reference_formula
class rfr_cd(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles entrant dans le revenus fiscal de référence"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, cd_acc75a, cd_doment, cd_eparet, cd_sofipe):
        return cd_acc75a + cd_doment + cd_eparet + cd_sofipe

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class cd1(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles non plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, cd_penali, cd_acc75a, cd_percap, cd_deddiv, cd_doment):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2002
        '''
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment
        return niches1

    @dated_function(start = date(2004, 1, 1), stop = date(2005, 12, 31))
    def function_20040101_20051231(self, cd_penali, cd_acc75a, cd_percap, cd_deddiv, cd_doment, cd_eparet):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2004
        '''
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment + cd_eparet
        return niches1

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, cd_penali, cd_acc75a, cd_percap, cd_deddiv, cd_eparet):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2006
        '''
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_eparet
        return niches1

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, cd_penali, cd_acc75a, cd_deddiv, cd_eparet):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2007
        '''
        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet
        return niches1

    @dated_function(start = date(2009, 1, 1), stop = date(2013, 12, 31))
    def function_20090101_20131231(self, cd_penali, cd_acc75a, cd_deddiv, cd_eparet, cd_grorep):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2009
        '''
        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
        return niches1

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_20140101_20141231(self, cd_penali, cd_acc75a, cd_deddiv, cd_eparet, cd_grorep):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2014
        '''
        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
        # log.error("Charges déductibles to be checked because not defined for %s", 2014)
        return niches1

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')








@reference_formula
class cd2(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, cd_sofipe, cd_cinema):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        niches2 = cd_sofipe + cd_cinema
        return niches2

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, cd_sofipe):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        niches2 = cd_sofipe
        return niches2

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, cd_ecodev):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        niches2 = cd_ecodev
        return niches2

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class rbg_int(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu brut global intermédiaire"

    def function(self, rbg, cd1):
        return max_(rbg - cd1, 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class charges_deduc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, cd1, cd2):
        return cd1 + cd2

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_penali(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_penali"
    url = "http://frederic.anne.free.fr/Cours/ITV.htm"

    def function(self, f6gi, f6gj, f6gp, f6el, f6em, f6gu, penalim =  law.ir.charges_deductibles.penalim):
        '''
        Pensions alimentaires
        '''
        max1 = penalim.max
        taux_jgt_2006 = penalim.taux_jgt_2006
            # TODO: si vous subvenez seul(e) à l'entretien d'un enfant marié ou
            # pacsé ou chargé de famille, quel que soit le nmbre d'enfants du jeune
            # foyer, la déduction est limitée à 2*max
        # S'il habite chez ses parents, max 3359, sinon 5698
        return (min_(f6gi * (1 + taux_jgt_2006), max1) +
                    min_(f6gj * (1 + taux_jgt_2006), max1) +
                    min_(f6el, max1) +
                    min_(f6em, max1) +
                    f6gp * (1 + taux_jgt_2006) + f6gu)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_acc75a(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_acc75a"

    def function(self, f6eu, f6ev, acc75a =  law.ir.charges_deductibles.acc75a):
        '''
        Frais d’accueil sous votre toit d’une personne de plus de 75 ans
        '''
        amax = acc75a.max * max_(1, f6ev)
        return min_(f6eu, amax)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_percap(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_percap"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, f6cb, marpac, _P, percap =  law.ir.charges_deductibles.percap):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        max_cb = percap.max_cb * (1 + marpac)
        return min_(f6cb, max_cb)

    @dated_function(start = date(2003, 1, 1), stop = date(2006, 12, 31))
    def function_20030101_20061231(self, f6cb, f6da, marpac, _P, percap =  law.ir.charges_deductibles.percap):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        max_cb = percap.max_cb * (1 + marpac)
        max_da = percap.max_da * (1 + marpac)
        return min_(min_(f6cb, max_cb) + min_(f6da, max_da), max_da)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')




@reference_formula
class cd_deddiv(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_deddiv"

    def function(self, f6dd):
        '''
        Déductions diverses (case DD)
        '''
        return f6dd

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class cd_doment(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_doment"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, f6eh):
        '''
        Investissements DOM-TOM dans le cadre d’une entreprise (case EH de la
        déclaration n° 2042 complémentaire)
        2002-2005
        '''
        return f6eh

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class cd_eparet(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_eparet"
    start_date = date(2004, 1, 1)

    def function(self, f6ps_holder, f6rs_holder, f6ss_holder):
        '''
        Épargne retraite - PERP, PRÉFON, COREM et CGOS
        2004-
        '''
        f6ps = self.filter_role(f6ps_holder, role = VOUS)
        f6pt = self.filter_role(f6ps_holder, role = CONJ)
        f6pu = self.filter_role(f6ps_holder, role = PAC1)

        f6rs = self.filter_role(f6rs_holder, role = VOUS)
        f6rt = self.filter_role(f6rs_holder, role = CONJ)
        f6ru = self.filter_role(f6rs_holder, role = PAC1)

        f6ss = self.filter_role(f6ss_holder, role = VOUS)
        f6st = self.filter_role(f6ss_holder, role = CONJ)
        f6su = self.filter_role(f6ss_holder, role = PAC1)

        # TODO: En théorie, les plafonds de déductions (ps, pt, pu) sont calculés sur
        # le formulaire 2041 GX
        return ((f6ps == 0) * (f6rs + f6ss) +
                (f6ps != 0) * min_(f6rs + f6ss, f6ps) +
                (f6pt == 0) * (f6rt + f6st) +
                (f6pt != 0) * min_(f6rt + f6st, f6pt) +
                (f6pu == 0) * (f6ru + f6su) +
                (f6pu != 0) * min_(f6ru + f6su, f6pu))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_sofipe(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_sofipe"
    start_date = date(2002, 1, 1)
    stop_date = date(2006, 12, 31)

    def function(self, f6cc, rbg_int, marpac, sofipe =  law.ir.charges_deductibles.sofipe):
        '''
        Souscriptions au capital des SOFIPÊCHE (case CC de la déclaration
        complémentaire)
        2002-2006
        '''
        max1 = min_(sofipe.taux * rbg_int, sofipe.max * (1 + marpac))
        return min_(f6cc, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_cinema(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_cinema"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, f6aa, rbg_int, cinema =  law.ir.charges_deductibles.cinema):
        '''
        Souscriptions en faveur du cinéma ou de l’audiovisuel (case AA de la
        déclaration n° 2042 complémentaire)
        2002-2005
        '''
        max1 = min_(cinema.taux * rbg_int, cinema.max)
        return min_(f6aa, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_ecodev(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_ecodev"
    start_date = date(2007, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, f6eh, rbg_int, ecodev =  law.ir.charges_deductibles.ecodev):
        '''
        Versements sur un compte épargne codéveloppement (case EH de la déclaration
        complémentaire)
        2007-2008
        '''
        max1 = min_(ecodev.taux * rbg_int, ecodev.max)
        return min_(f6eh, max1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cd_grorep(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_grorep"
    start_date = date(2009, 1, 1)

    def function(self, f6cb, f6hj, f6hk, f6hl, grorep =  law.ir.charges_deductibles.grorep):
        '''
        Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
        2009-
        '''
        return min_(f6cb + f6hj + f6hk + f6hl, grorep.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
