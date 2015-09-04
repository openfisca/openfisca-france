# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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

from numpy import minimum as min_, maximum as max_


from ...base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# Csg déductible
build_column('f6de', IntCol(entity = 'foy',
                label = u"CSG déductible calculée sur les revenus du patrimoine",
                val_type = "monetary",
                cerfa_field = u'6DE'))

# Pensions alimentaires
build_column('f6gi', IntCol(entity = 'foy',
                label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant",
                val_type = "monetary",
                cerfa_field = u'6GI'))

build_column('f6gj', IntCol(entity = 'foy',
                label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant",
                val_type = "monetary",
                cerfa_field = u'6GJ'))

build_column('f6el', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'6EL'))

build_column('f6em', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'6EM'))

build_column('f6gp', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)",
                val_type = "monetary",
                cerfa_field = u'6GP'))

build_column('f6gu', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées (mineurs, ascendants)",
                start = date(2006, 1, 1),
                val_type = "monetary",
                cerfa_field = u'6GU'))

# Frais d'accueil d'une personne de plus de 75 ans dans le besoin
build_column('f6eu', IntCol(entity = 'foy',
                label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin",
                val_type = "monetary",
                cerfa_field = u'6EU'))

build_column('f6ev', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit",
                cerfa_field = u'6EV'))

# Déductions diverses
build_column('f6dd', IntCol(entity = 'foy',
                label = u"Déductions diverses",
                val_type = "monetary",
                cerfa_field = u'6DD'))

# Épargne retraite - PERP, PRÉFON, COREM et CGOS
build_column('f6ps', IntCol(entity = 'ind',
                label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6PS",
                               QUIFOY['conj']: u"6PT",
                               QUIFOY['pac1']: u"6PU",
                               }))  # (f6ps, f6pt, f6pu)

build_column('f6rs', IntCol(entity = 'ind',
                label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6RS",
                               QUIFOY['conj']: u"6RT",
                               QUIFOY['pac1']: u"6RU",
                               }))  # (f6rs, f6rt, f6ru)))

build_column('f6ss', IntCol(entity = 'ind',
                label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6SS",
                               QUIFOY['conj']: u"6ST",
                               QUIFOY['pac1']: u"6SU",
                               }))  # (f6ss, f6st, f6su)))

# Souscriptions en faveur du cinéma ou de l’audiovisuel
build_column('f6aa', IntCol(entity = 'foy',
                label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2006, 12, 31),
                cerfa_field = u'6AA'))  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

# Souscriptions au capital des SOFIPÊCHE
build_column('f6cc', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des SOFIPÊCHE",
                val_type = "monetary",
                cerfa_field = u'CC',
                start = date(2005, 1, 1),
                end = date(2005, 12, 31)))  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


# Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
# ou Versements sur un compte épargne codéveloppement
build_column('f6eh', IntCol(entity = 'foy',
                label = u"",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2005, 12, 31),
                cerfa_field = u'EH'))  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

# Pertes en capital consécutives à la souscription au capital de sociétés
# nouvelles ou de sociétés en difficulté
build_column('f6da', IntCol(entity = 'foy',
                label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2005, 12, 31),
                cerfa_field = u'DA'))


# Dépenses de grosses réparations effectuées par les nus propriétaires
build_column('f6cb', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'6CB'))
                                       # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

build_column('f6hj', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'6HJ'))

build_column('f6hk', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'6HK'))

build_column('f6hl', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'6HL'))

build_column('f6hm', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'6HM'))

# Sommes à rajouter au revenu imposable
build_column('f6gh', IntCol(entity = 'foy',
                label = u"Sommes à ajouter au revenu imposable",
                val_type = "monetary",
                cerfa_field = u'6GH'))

# Deficits antérieurs
build_column('f6fa', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6",
                val_type = "monetary",
                cerfa_field = u'6FA'))

build_column('f6fb', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5",
                val_type = "monetary",
                cerfa_field = u'6FB'))

build_column('f6fc', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'6FC'))

build_column('f6fd', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3",
                val_type = "monetary",
                cerfa_field = u'6FD'))

build_column('f6fe', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2",
                val_type = "monetary",
                cerfa_field = u'6FE'))

build_column('f6fl', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'6FL'))


@reference_formula
class rfr_cd(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles entrant dans le revenus fiscal de référence"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_doment = simulation.calculate('cd_doment', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        return period, cd_acc75a + cd_doment + cd_eparet + cd_sofipe


@reference_formula
class cd1(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles non plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2003, 12, 31))
    def function_20020101_20031231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2002
        '''
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
        cd_penali = simulation.calculate('cd_penali', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_grorep = simulation.calculate('cd_grorep', period)

        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
        # log.error("Charges déductibles to be checked because not defined for %s", 2014)
        return period, niches1


@reference_formula
class cd2(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles plafonnées"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.start.offset('first-of', 'year').period('year')
        cd_sofipe = simulation.calculate('cd_sofipe', period)
        cd_cinema = simulation.calculate('cd_cinema', period)

        niches2 = cd_sofipe + cd_cinema
        return period, niches2

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_20060101_20061231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.start.offset('first-of', 'year').period('year')
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        niches2 = cd_sofipe
        return period, niches2

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_20070101_20081231(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        period = period.start.offset('first-of', 'year').period('year')
        cd_ecodev = simulation.calculate('cd_ecodev', period)

        niches2 = cd_ecodev
        return period, niches2


@reference_formula
class rbg_int(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu brut global intermédiaire"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        rbg = simulation.calculate('rbg', period)
        cd1 = simulation.calculate('cd1', period)

        return period, max_(rbg - cd1, 0)


@reference_formula
class charges_deduc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Charges déductibles"
    url = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        cd1 = simulation.calculate('cd1', period)
        cd2 = simulation.calculate('cd2', period)

        return period, cd1 + cd2


@reference_formula
class cd_penali(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_penali"
    url = "http://frederic.anne.free.fr/Cours/ITV.htm"

    def function(self, simulation, period):
        '''
        Pensions alimentaires
        '''
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class cd_acc75a(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_acc75a"

    def function(self, simulation, period):
        '''
        Frais d’accueil sous votre toit d’une personne de plus de 75 ans
        '''
        period = period.start.offset('first-of', 'year').period('year')
        f6eu = simulation.calculate('f6eu', period)
        f6ev = simulation.calculate('f6ev', period)
        acc75a = simulation.legislation_at(period.start).ir.charges_deductibles.acc75a

        amax = acc75a.max * max_(1, f6ev)
        return period, min_(f6eu, amax)


@reference_formula
class cd_percap(DatedFormulaColumn):
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
        f6cb = simulation.calculate('f6cb', period)
        f6da = simulation.calculate('f6da', period)
        marpac = simulation.calculate('marpac', period)
        percap = simulation.legislation_at(period.start).ir.charges_deductibles.percap

        max_cb = percap.max_cb * (1 + marpac)
        max_da = percap.max_da * (1 + marpac)
        return period, min_(min_(f6cb, max_cb) + min_(f6da, max_da), max_da)


@reference_formula
class cd_deddiv(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_deddiv"

    def function(self, simulation, period):
        '''
        Déductions diverses (case DD)
        '''
        period = period.start.offset('first-of', 'year').period('year')
        f6dd = simulation.calculate('f6dd', period)

        return period, f6dd


@reference_formula
class cd_doment(SimpleFormulaColumn):
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
        period = period.start.offset('first-of', 'year').period('year')
        f6eh = simulation.calculate('f6eh', period)

        return period, f6eh


@reference_formula
class cd_eparet(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_eparet"
    start_date = date(2004, 1, 1)

    def function(self, simulation, period):
        '''
        Épargne retraite - PERP, PRÉFON, COREM et CGOS
        2004-
        '''
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class cd_sofipe(SimpleFormulaColumn):
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
        period = period.start.offset('first-of', 'year').period('year')
        f6cc = simulation.calculate('f6cc', period)
        rbg_int = simulation.calculate('rbg_int', period)
        marpac = simulation.calculate('marpac', period)
        sofipe = simulation.legislation_at(period.start).ir.charges_deductibles.sofipe

        max1 = min_(sofipe.taux * rbg_int, sofipe.max * (1 + marpac))
        return period, min_(f6cc, max1)


@reference_formula
class cd_cinema(SimpleFormulaColumn):
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
        period = period.start.offset('first-of', 'year').period('year')
        f6aa = simulation.calculate('f6aa', period)
        rbg_int = simulation.calculate('rbg_int', period)
        cinema = simulation.legislation_at(period.start).ir.charges_deductibles.cinema

        max1 = min_(cinema.taux * rbg_int, cinema.max)
        return period, min_(f6aa, max1)


@reference_formula
class cd_ecodev(SimpleFormulaColumn):
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
        period = period.start.offset('first-of', 'year').period('year')
        f6eh = simulation.calculate('f6eh', period)
        rbg_int = simulation.calculate('rbg_int', period)
        ecodev = simulation.legislation_at(period.start).ir.charges_deductibles.ecodev

        max1 = min_(ecodev.taux * rbg_int, ecodev.max)
        return period, min_(f6eh, max1)


@reference_formula
class cd_grorep(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cd_grorep"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
        2009-
        '''
        period = period.start.offset('first-of', 'year').period('year')
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        grorep = simulation.legislation_at(period.start).ir.charges_deductibles.grorep

        return period, min_(f6cb + f6hj + f6hk + f6hl, grorep.max)
