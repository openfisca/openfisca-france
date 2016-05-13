# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import minimum as min_, maximum as max_


from ...base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# Csg déductible
class f6de(Variable):
    cerfa_field = u"6DE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"CSG déductible calculée sur les revenus du patrimoine"



# Pensions alimentaires
class f6gi(Variable):
    cerfa_field = u"6GI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant"



class f6gj(Variable):
    cerfa_field = u"6GJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant"



class f6el(Variable):
    cerfa_field = u"6EL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant"
    start_date = date(2006, 1, 1)



class f6em(Variable):
    cerfa_field = u"6EM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant"
    start_date = date(2006, 1, 1)



class f6gp(Variable):
    cerfa_field = u"6GP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)"



class f6gu(Variable):
    cerfa_field = u"6GU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres pensions alimentaires versées (mineurs, ascendants)"
    start_date = date(2006, 1, 1)



# Frais d'accueil d'une personne de plus de 75 ans dans le besoin
class f6eu(Variable):
    cerfa_field = u"6EU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin"



class f6ev(Variable):
    cerfa_field = u"6EV"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit"



# Déductions diverses
class f6dd(Variable):
    cerfa_field = u"6DD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Déductions diverses"



# Épargne retraite - PERP, PRÉFON, COREM et CGOS
class f6ps(Variable):
    cerfa_field = {QUIFOY['vous']: u"6PS",
        QUIFOY['conj']: u"6PT",
        QUIFOY['pac1']: u"6PU",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)"

  # (f6ps, f6pt, f6pu)

class f6rs(Variable):
    cerfa_field = {QUIFOY['vous']: u"6RS",
        QUIFOY['conj']: u"6RT",
        QUIFOY['pac1']: u"6RU",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S"

  # (f6rs, f6rt, f6ru)))

class f6ss(Variable):
    cerfa_field = {QUIFOY['vous']: u"6SS",
        QUIFOY['conj']: u"6ST",
        QUIFOY['pac1']: u"6SU",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S"

  # (f6ss, f6st, f6su)))

# Souscriptions en faveur du cinéma ou de l’audiovisuel
class f6aa(Variable):
    cerfa_field = u"6AA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel"
    start_date = date(2005, 1, 1)
    stop_date = date(2006, 12, 31)

  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

# Souscriptions au capital des SOFIPÊCHE
class f6cc(Variable):
    cerfa_field = u"CC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des SOFIPÊCHE"
    start_date = date(2005, 1, 1)
    stop_date = date(2005, 12, 31)

  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


# Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
# ou Versements sur un compte épargne codéveloppement
class f6eh(Variable):
    cerfa_field = u"EH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    start_date = date(2005, 1, 1)
    stop_date = date(2005, 12, 31)

  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

# Pertes en capital consécutives à la souscription au capital de sociétés
# nouvelles ou de sociétés en difficulté
class f6da(Variable):
    cerfa_field = u"DA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté"
    start_date = date(2005, 1, 1)
    stop_date = date(2005, 12, 31)




# Dépenses de grosses réparations effectuées par les nus propriétaires
class f6cb(Variable):
    cerfa_field = u"6CB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)"
    start_date = date(2009, 1, 1)


                                       # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

class f6hj(Variable):
    cerfa_field = u"6HJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    start_date = date(2010, 1, 1)



class f6hk(Variable):
    cerfa_field = u"6HK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    start_date = date(2011, 1, 1)



class f6hl(Variable):
    cerfa_field = u"6HL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    start_date = date(2012, 1, 1)



class f6hm(Variable):
    cerfa_field = u"6HM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    start_date = date(2013, 1, 1)



# Sommes à rajouter au revenu imposable
class f6gh(Variable):
    cerfa_field = u"6GH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Sommes à ajouter au revenu imposable"



# Deficits antérieurs
class f6fa(Variable):
    cerfa_field = u"6FA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6"



class f6fb(Variable):
    cerfa_field = u"6FB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5"



class f6fc(Variable):
    cerfa_field = u"6FC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4"



class f6fd(Variable):
    cerfa_field = u"6FD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3"



class f6fe(Variable):
    cerfa_field = u"6FE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2"



class f6fl(Variable):
    cerfa_field = u"6FL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1"




class rfr_cd(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles entrant dans le revenus fiscal de référence"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, simulation, period):
        period = period.this_year
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_doment = simulation.calculate('cd_doment', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        return period, cd_acc75a + cd_doment + cd_eparet + cd_sofipe


class cd1(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles non plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2002
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_percap = simulation.calculate('cd_percap', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_doment = simulation.calculate('cd_doment', period)

        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment
        return period, niches1

    @dated_function(start = date(2004, 1, 1), stop = date(2005, 12, 31))
    def function_20040101_20051231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2004
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_percap = simulation.calculate('cd_percap', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_doment = simulation.calculate('cd_doment', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment + cd_eparet
        return period, niches1

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2006
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_percap = simulation.calculate('cd_percap', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_eparet
        return period, niches1

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2007
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet
        return period, niches1

    @dated_function(start = date(2009, 1, 1), stop = date(2013, 12, 31))
    def function_20090101_20131231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2009
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_grorep = simulation.calculate('cd_grorep', period)

        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
        return period, niches1

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_20140101_20141231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2014
        '''
        period = period.this_year
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_grorep = simulation.calculate('cd_grorep', period)

        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
        # log.error("Charges déductibles to be checked because not defined for %s", 2014)
        return period, niches1


class cd2(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.this_year
        cd_sofipe = simulation.calculate('cd_sofipe', period)
        cd_cinema = simulation.calculate('cd_cinema', period)

        niches2 = cd_sofipe + cd_cinema
        return period, niches2

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.this_year
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        niches2 = cd_sofipe
        return period, niches2

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.this_year
        cd_ecodev = simulation.calculate('cd_ecodev', period)

        niches2 = cd_ecodev
        return period, niches2


class rbg_int(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu brut global intermédiaire"

    def function(self, simulation, period):
        period = period.this_year
        rbg = simulation.calculate('rbg', period)
        cd1 = simulation.calculate('cd1', period)

        return period, max_(rbg - cd1, 0)


class charges_deduc(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, simulation, period):
        period = period.this_year
        cd1 = simulation.calculate('cd1', period)
        cd2 = simulation.calculate('cd2', period)

        return period, cd1 + cd2


class cd_penali(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_penali"
    url = "http://frederic.anne.free.fr/Cours/ITV.htm"

    def function(self, simulation, period):
        '''
        Pensions alimentaires
        '''
        period = period.this_year
        f6gi = simulation.calculate('f6gi', period)
        f6gj = simulation.calculate('f6gj', period)
        f6gp = simulation.calculate('f6gp', period)
        f6el = simulation.calculate('f6el', period)
        f6em = simulation.calculate('f6em', period)
        f6gu = simulation.calculate('f6gu', period)
        penalim = simulation.legislation_at(period.start).ir.charges_deductibles.penalim

        max1 = penalim.max
        taux_jgt_2006 = penalim.taux_jgt_2006
        # TODO: si vous subvenez seul(e) à l'entretien d'un enfant marié ou
        # pacsé ou chargé de famille, quel que soit le nmbre d'enfants du jeune
        # foyer, la déduction est limitée à 2*max
        # S'il habite chez ses parents, max 3359, sinon 5698
        return period, (min_(f6gi * (1 + taux_jgt_2006), max1) +
                    min_(f6gj * (1 + taux_jgt_2006), max1) +
                    min_(f6el, max1) +
                    min_(f6em, max1) +
                    f6gp * (1 + taux_jgt_2006) + f6gu)


class cd_acc75a(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_acc75a"

    def function(self, simulation, period):
        '''
        Frais d’accueil sous votre toit d’une personne de plus de 75 ans
        '''
        period = period.this_year
        f6eu = simulation.calculate('f6eu', period)
        f6ev = simulation.calculate('f6ev', period)
        acc75a = simulation.legislation_at(period.start).ir.charges_deductibles.acc75a

        amax = acc75a.max * max_(1, f6ev)
        return period, min_(f6eu, amax)


class cd_percap(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_percap"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, simulation, period):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        period = period.this_year
        f6cb = simulation.calculate('f6cb', period)
        marpac = simulation.calculate('marpac', period)
        percap = simulation.legislation_at(period.start).ir.charges_deductibles.percap

        max_cb = percap.max_cb * (1 + marpac)
        return period, min_(f6cb, max_cb)

    @dated_function(start = date(2003, 1, 1), stop = date(2006, 12, 31))
    def function_20030101_20061231(self, simulation, period):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        period = period.this_year
        f6cb = simulation.calculate('f6cb', period)
        f6da = simulation.calculate('f6da', period)
        marpac = simulation.calculate('marpac', period)
        percap = simulation.legislation_at(period.start).ir.charges_deductibles.percap

        max_cb = percap.max_cb * (1 + marpac)
        max_da = percap.max_da * (1 + marpac)
        return period, min_(min_(f6cb, max_cb) + min_(f6da, max_da), max_da)


class cd_deddiv(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_deddiv"

    def function(self, simulation, period):
        '''
        Déductions diverses (case DD)
        '''
        period = period.this_year
        f6dd = simulation.calculate('f6dd', period)

        return period, f6dd


class cd_doment(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_doment"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, simulation, period):
        '''
        Investissements DOM-TOM dans le cadre d’une entreprise (case EH de la
        déclaration n° 2042 complémentaire)
        2002-2005
        '''
        period = period.this_year
        f6eh = simulation.calculate('f6eh', period)

        return period, f6eh


class cd_eparet(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_eparet"
    start_date = date(2004, 1, 1)

    def function(self, simulation, period):
        '''
        Épargne retraite - PERP, PRÉFON, COREM et CGOS
        2004-
        '''
        period = period.this_year
        f6ps_holder = simulation.compute('f6ps', period)
        f6rs_holder = simulation.compute('f6rs', period)
        f6ss_holder = simulation.compute('f6ss', period)

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
        return period, ((f6ps == 0) * (f6rs + f6ss) +
                (f6ps != 0) * min_(f6rs + f6ss, f6ps) +
                (f6pt == 0) * (f6rt + f6st) +
                (f6pt != 0) * min_(f6rt + f6st, f6pt) +
                (f6pu == 0) * (f6ru + f6su) +
                (f6pu != 0) * min_(f6ru + f6su, f6pu))


class cd_sofipe(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_sofipe"
    start_date = date(2002, 1, 1)
    stop_date = date(2006, 12, 31)

    def function(self, simulation, period):
        '''
        Souscriptions au capital des SOFIPÊCHE (case CC de la déclaration
        complémentaire)
        2002-2006
        '''
        period = period.this_year
        f6cc = simulation.calculate('f6cc', period)
        rbg_int = simulation.calculate('rbg_int', period)
        marpac = simulation.calculate('marpac', period)
        sofipe = simulation.legislation_at(period.start).ir.charges_deductibles.sofipe

        max1 = min_(sofipe.taux * rbg_int, sofipe.max * (1 + marpac))
        return period, min_(f6cc, max1)


class cd_cinema(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_cinema"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, simulation, period):
        '''
        Souscriptions en faveur du cinéma ou de l’audiovisuel (case AA de la
        déclaration n° 2042 complémentaire)
        2002-2005
        '''
        period = period.this_year
        f6aa = simulation.calculate('f6aa', period)
        rbg_int = simulation.calculate('rbg_int', period)
        cinema = simulation.legislation_at(period.start).ir.charges_deductibles.cinema

        max1 = min_(cinema.taux * rbg_int, cinema.max)
        return period, min_(f6aa, max1)


class cd_ecodev(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_ecodev"
    start_date = date(2007, 1, 1)
    stop_date = date(2008, 12, 31)

    def function(self, simulation, period):
        '''
        Versements sur un compte épargne codéveloppement (case EH de la déclaration
        complémentaire)
        2007-2008
        '''
        period = period.this_year
        f6eh = simulation.calculate('f6eh', period)
        rbg_int = simulation.calculate('rbg_int', period)
        ecodev = simulation.legislation_at(period.start).ir.charges_deductibles.ecodev

        max1 = min_(ecodev.taux * rbg_int, ecodev.max)
        return period, min_(f6eh, max1)


class cd_grorep(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_grorep"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
        2009-
        '''
        period = period.this_year
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        grorep = simulation.legislation_at(period.start).ir.charges_deductibles.grorep

        return period, min_(f6cb + f6hj + f6hk + f6hl, grorep.max)
