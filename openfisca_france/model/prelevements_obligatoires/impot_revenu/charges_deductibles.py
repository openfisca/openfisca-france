# -*- coding: utf-8 -*-

from __future__ import division

import logging

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# Csg déductible
class f6de(Variable):
    cerfa_field = u"6DE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"CSG déductible calculée sur les revenus du patrimoine"
    definition_period = YEAR


# Pensions alimentaires
class f6gi(Variable):
    cerfa_field = u"6GI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant"
    definition_period = YEAR


class f6gj(Variable):
    cerfa_field = u"6GJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant"
    definition_period = YEAR


class f6el(Variable):
    cerfa_field = u"6EL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class f6em(Variable):
    cerfa_field = u"6EM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class f6gp(Variable):
    cerfa_field = u"6GP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)"
    definition_period = YEAR


class f6gu(Variable):
    cerfa_field = u"6GU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres pensions alimentaires versées (mineurs, ascendants)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# Frais d'accueil d'une personne de plus de 75 ans dans le besoin
class f6eu(Variable):
    cerfa_field = u"6EU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin"
    definition_period = YEAR


class f6ev(Variable):
    cerfa_field = u"6EV"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit"
    definition_period = YEAR


# Déductions diverses
class f6dd(Variable):
    cerfa_field = u"6DD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déductions diverses"
    definition_period = YEAR


# Épargne retraite - PERP, PRÉFON, COREM et CGOS
class f6ps(Variable):
    cerfa_field = {QUIFOY['vous']: u"6PS",
        QUIFOY['conj']: u"6PT",
        QUIFOY['pac1']: u"6PU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)"
    definition_period = YEAR


class f6rs(Variable):
    cerfa_field = {QUIFOY['vous']: u"6RS",
        QUIFOY['conj']: u"6RT",
        QUIFOY['pac1']: u"6RU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S"
    definition_period = YEAR


class f6ss(Variable):
    cerfa_field = {QUIFOY['vous']: u"6SS",
        QUIFOY['conj']: u"6ST",
        QUIFOY['pac1']: u"6SU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S"
    definition_period = YEAR


# Souscriptions en faveur du cinéma ou de l’audiovisuel
class f6aa(Variable):
    cerfa_field = u"6AA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel"
    # start_date = date(2005, 1, 1)
    end = '2006-12-31'
    definition_period = YEAR

  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

# Souscriptions au capital des SOFIPÊCHE
class f6cc(Variable):
    cerfa_field = u"CC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des SOFIPÊCHE"
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR

  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


# Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
# ou Versements sur un compte épargne codéveloppement
class f6eh(Variable):
    cerfa_field = u"EH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR
# TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)


class f6da(Variable):
    cerfa_field = u"DA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté"
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR


# Dépenses de grosses réparations effectuées par les nus propriétaires
class f6cb(Variable):
    cerfa_field = u"6CB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# TODO: before 2006 was Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

class f6hj(Variable):
    cerfa_field = u"6HJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2010, 1, 1)
    definition_period = YEAR


class f6hk(Variable):
    cerfa_field = u"6HK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class f6hl(Variable):
    cerfa_field = u"6HL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f6hm(Variable):
    cerfa_field = u"6HM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR

class f6hn(Variable):
    cerfa_field = u"6HN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2014, 1, 1)
    definition_period = YEAR

class f6ho(Variable):
    cerfa_field = u"6HO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2015, 1, 1)
    definition_period = YEAR

class f6hp(Variable):
    cerfa_field = u"6HP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# Sommes à rajouter au revenu imposable
class f6gh(Variable):
    cerfa_field = u"6GH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Sommes à ajouter au revenu imposable"
    definition_period = YEAR


# Deficits antérieurs
class f6fa(Variable):
    cerfa_field = u"6FA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6"
    definition_period = YEAR


class f6fb(Variable):
    cerfa_field = u"6FB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5"
    definition_period = YEAR


class f6fc(Variable):
    cerfa_field = u"6FC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4"
    definition_period = YEAR


class f6fd(Variable):
    cerfa_field = u"6FD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3"
    definition_period = YEAR


class f6fe(Variable):
    cerfa_field = u"6FE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2"
    definition_period = YEAR


class f6fl(Variable):
    cerfa_field = u"6FL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1"
    definition_period = YEAR


class rfr_cd(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Charges déductibles entrant dans le revenus fiscal de référence"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR

    def formula(self, simulation, period):
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_doment = simulation.calculate('cd_doment', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        return cd_acc75a + cd_doment + cd_eparet + cd_sofipe


class cd1(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Charges déductibles non plafonnées"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR
    end = '2016-12-31'

    def formula_2002_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2002
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        pertes_capital_societes_nouvelles = simulation.calculate('pertes_capital_societes_nouvelles', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_doment = simulation.calculate('cd_doment', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + pertes_capital_societes_nouvelles + cd_deddiv + cd_doment
        return niches1

    def formula_2004_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2004
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        pertes_capital_societes_nouvelles = simulation.calculate('pertes_capital_societes_nouvelles', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_doment = simulation.calculate('cd_doment', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = (pensions_alimentaires_deduites + cd_acc75a + pertes_capital_societes_nouvelles +
                   cd_deddiv + cd_doment + cd_eparet)
        return niches1

    def formula_2006_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2006
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        pertes_capital_societes_nouvelles = simulation.calculate('pertes_capital_societes_nouvelles', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + pertes_capital_societes_nouvelles + cd_deddiv + cd_eparet
        return niches1

    def formula_2007_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2007
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet
        return niches1

    def formula_2009_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2009
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        grosses_reparations = simulation.calculate('grosses_reparations', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet + grosses_reparations
        return niches1

    def formula_2014_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2014
        '''
        pensions_alimentaires_deduites = simulation.calculate('pensions_alimentaires_deduites', period)
        cd_acc75a = simulation.calculate('cd_acc75a', period)
        cd_deddiv = simulation.calculate('cd_deddiv', period)
        cd_eparet = simulation.calculate('cd_eparet', period)
        grosses_reparations = simulation.calculate('grosses_reparations', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet + grosses_reparations
        # log.error("Charges déductibles to be checked because not defined for %s", 2014)
        return niches1


class cd2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Charges déductibles plafonnées"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR
    end = '2008-12-31'

    def formula_2002_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        cd_sofipe = simulation.calculate('cd_sofipe', period)
        cinema = simulation.calculate('souscriptions_cinema_audiovisuel', period)

        niches2 = cd_sofipe + cinema
        return niches2

    def formula_2006_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        cd_sofipe = simulation.calculate('cd_sofipe', period)

        niches2 = cd_sofipe
        return niches2

    def formula_2007_01_01(self, simulation, period):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        epargne_codeveloppement = simulation.calculate('epargne_codeveloppement', period)

        niches2 = epargne_codeveloppement
        return niches2


class rbg_int(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu brut global intermédiaire"
    definition_period = YEAR

    def formula(self, simulation, period):
        rbg = simulation.calculate('rbg', period)
        cd1 = simulation.calculate('cd1', period)

        return max_(rbg - cd1, 0)


class charges_deduc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Charges déductibles"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR

    def formula(self, simulation, period):
        cd1 = simulation.calculate('cd1', period)
        cd2 = simulation.calculate('cd2', period)

        return cd1 + cd2


class pensions_alimentaires_deduites(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Pensions alimentaires"
    reference = "http://frederic.anne.free.fr/Cours/ITV.htm"
    definition_period = YEAR

    def formula(self, simulation, period):
        f6gi = simulation.calculate('f6gi', period)
        f6gj = simulation.calculate('f6gj', period)
        f6gp = simulation.calculate('f6gp', period)
        f6el = simulation.calculate('f6el', period)
        f6em = simulation.calculate('f6em', period)
        f6gu = simulation.calculate('f6gu', period)
        penalim = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.pensions_alimentaires

        max1 = penalim.plafond
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


class cd_acc75a(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Frais d’accueil sous votre toit d’une personne de plus de 75 ans"
    definition_period = YEAR

    def formula(self, simulation, period):
        f6eu = simulation.calculate('f6eu', period)
        f6ev = simulation.calculate('f6ev', period)
        acc75a = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.accueil_personne_agee
        amax = acc75a.plafond * max_(1, f6ev)
        return min_(f6eu, amax)


class pertes_capital_societes_nouvelles(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté"
    definition_period = YEAR
    end = '2006-12-31'

    def formula_2002_01_01(self, simulation, period):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        f6cb = simulation.calculate('f6cb', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        percap = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.pertes_en_capital_societes_nouvelles
        plafond_cb = percap.plafond_cb * (1 + maries_ou_pacses)
        return min_(f6cb, plafond_cb)

    def formula_2003_01_01(self, simulation, period):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6da = simulation.calculate('f6da', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        percap = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.pertes_en_capital_societes_nouvelles
        plafond_cb = percap.plafond_cb * (1 + maries_ou_pacses)
        plafond_da = percap.plafond_da * (1 + maries_ou_pacses)
        return min_(min_(f6cb, plafond_cb) + min_(f6da, plafond_da), plafond_da)


class cd_deddiv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Déductions diverses"
    definition_period = YEAR

    def formula(self, simulation, period):
        f6dd = simulation.calculate('f6dd', period)

        return f6dd


class cd_doment(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Investissements DOM-TOM dans le cadre d’une entreprise"
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2002(self, simulation, period):
        '''
        Investissements DOM-TOM dans le cadre d’une entreprise (case EH de la
        déclaration n° 2042 complémentaire)
        '''
        f6eh = simulation.calculate('f6eh', period)

        return f6eh


class cd_eparet(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Charge déductible au titre de l'épargne retraite (PERP, PRÉFON, COREM et CGOS)"
    definition_period = YEAR

    def formula_2004(self, simulation, period):
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
        return ((f6ps == 0) * (f6rs + f6ss) +
                (f6ps != 0) * min_(f6rs + f6ss, f6ps) +
                (f6pt == 0) * (f6rt + f6st) +
                (f6pt != 0) * min_(f6rt + f6st, f6pt) +
                (f6pu == 0) * (f6ru + f6su) +
                (f6pu != 0) * min_(f6ru + f6su, f6pu))


class cd_sofipe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Souscriptions au capital des SOFIPÊCHE"
    end = '2006-12-31'
    definition_period = YEAR

    def formula_2002(self, simulation, period):
        '''
        Souscriptions au capital des SOFIPÊCHE (case CC de la déclaration
        complémentaire)
        '''
        f6cc = simulation.calculate('f6cc', period)
        rbg_int = simulation.calculate('rbg_int', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        sofipeche = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.sofipeche

        plafond = min_(sofipeche.plafond_pct_rng * rbg_int, sofipeche.plafond * (1 + maries_ou_pacses))
        return min_(f6cc, plafond)


class souscriptions_cinema_audiovisuel(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel"
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2002(self, simulation, period):
        '''
        Souscriptions en faveur du cinéma ou de l’audiovisuel (case AA de la
        déclaration n° 2042 complémentaire)
        '''
        f6aa = simulation.calculate('f6aa', period)
        rbg_int = simulation.calculate('rbg_int', period)
        cinema = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.cinema

        max1 = min_(cinema.taux * rbg_int, cinema.max)
        return min_(f6aa, max1)


class epargne_codeveloppement(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Versements sur un compte épargne codéveloppement"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2007(self, simulation, period):
        '''
        Versements sur un compte épargne codéveloppement (case EH de la déclaration
        complémentaire)
        '''
        f6eh = simulation.calculate('f6eh', period)
        rbg_int = simulation.calculate('rbg_int', period)
        ecodev = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.compte_epargne_codev

        plafond = min_(ecodev.plafond_pct_rng * rbg_int, ecodev.plafond)
        return min_(f6eh, plafond)


class grosses_reparations(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Dépenses de grosses réparations des nus-propriétaires"
    definition_period = YEAR

    def formula_2009(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
        '''
        f6cb = simulation.calculate('f6cb', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb, grorep.plafond)

    def formula_2010(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj, grorep.plafond)

    def formula_2011(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk, grorep.plafond)

    def formula_2012(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk + f6hl, grorep.plafond)

    def formula_2013(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        f6hm = simulation.calculate('f6hm', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk + f6hl + f6hm, grorep.plafond)


    def formula_2014(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        f6hm = simulation.calculate('f6hm', period)
        f6hn = simulation.calculate('f6hn', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk + f6hl + f6hm + f6hn, grorep.plafond)

    def formula_2015(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        f6hm = simulation.calculate('f6hm', period)
        f6hn = simulation.calculate('f6hn', period)
        f6ho = simulation.calculate('f6ho', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk + f6hl + f6hm + f6hn + f6ho, grorep.plafond)

    def formula_2016(self, simulation, period):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = simulation.calculate('f6cb', period)
        f6hj = simulation.calculate('f6hj', period)
        f6hk = simulation.calculate('f6hk', period)
        f6hl = simulation.calculate('f6hl', period)
        f6hm = simulation.calculate('f6hm', period)
        f6hn = simulation.calculate('f6hn', period)
        f6ho = simulation.calculate('f6ho', period)
        f6hp = simulation.calculate('f6hp', period)
        grorep = simulation.parameters_at(period.start).impot_revenu.charges_deductibles.grosses_reparations

        return min_(f6cb + f6hj + f6hk + f6hl + f6hm + f6hn + f6ho + f6hp, grorep.plafond)
