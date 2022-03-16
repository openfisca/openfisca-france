import logging

from openfisca_france.model.base import *


log = logging.getLogger(__name__)


# Csg déductible
class f6de(Variable):
    cerfa_field = "6DE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "CSG déductible calculée sur les revenus du patrimoine"
    definition_period = YEAR


# Pensions alimentaires
class f6gi(Variable):
    cerfa_field = "6GI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant"
    definition_period = YEAR


class f6gj(Variable):
    cerfa_field = "6GJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant"
    definition_period = YEAR


class f6el(Variable):
    cerfa_field = "6EL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Autres pensions alimentaires versées à des enfants majeurs: 1er enfant"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class f6em(Variable):
    cerfa_field = "6EM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class f6gp(Variable):
    cerfa_field = "6GP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)"
    definition_period = YEAR


class f6gu(Variable):
    cerfa_field = "6GU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Autres pensions alimentaires versées (mineurs, ascendants)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# Frais d'accueil d'une personne de plus de 75 ans dans le besoin
class f6eu(Variable):
    cerfa_field = "6EU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Frais d'accueil de personnes de plus de 75 ans dans le besoin"
    definition_period = YEAR


class f6ev(Variable):
    cerfa_field = "6EV"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = "Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit"
    definition_period = YEAR


# Déductions diverses
class f6dd(Variable):
    cerfa_field = "6DD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Déductions diverses"
    definition_period = YEAR


# Épargne retraite - PERP, PRÉFON, COREM et CGOS
class f6ps(Variable):
    cerfa_field = {
        0: "6PS",
        1: "6PT",
        2: "6PU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)"
    definition_period = YEAR


class f6rs(Variable):
    cerfa_field = {
        0: "6RS",
        1: "6RT",
        2: "6RU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S"
    definition_period = YEAR


class f6ss(Variable):
    cerfa_field = {
        0: "6SS",
        1: "6ST",
        2: "6SU",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Rachat de cotisations PERP, PREFON, COREM et C.G.O.S"
    definition_period = YEAR


# Souscriptions en faveur du cinéma ou de l’audiovisuel
# TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)
class f6aa(Variable):
    cerfa_field = "6AA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Souscriptions en faveur du cinéma ou de l’audiovisuel"
    # start_date = date(2005, 1, 1)
    end = '2006-12-31'
    definition_period = YEAR


# Souscriptions au capital des SOFIPÊCHE


# ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)
class f6cc(Variable):
    cerfa_field = "CC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Souscriptions au capital des SOFIPÊCHE"
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR


# Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
# ou Versements sur un compte épargne codéveloppement
class f6eh(Variable):
    cerfa_field = "EH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR
# TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)


class f6da(Variable):
    cerfa_field = "DA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté"
    # start_date = date(2005, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR


# Dépenses de grosses réparations effectuées par les nus propriétaires
class f6cb(Variable):
    cerfa_field = "6CB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# TODO: before 2006 was Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

class f6hj(Variable):
    cerfa_field = "6HJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2009"
    # start_date = date(2010, 1, 1)
    definition_period = YEAR


class f6hk(Variable):
    cerfa_field = "6HK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2010"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class f6hl(Variable):
    cerfa_field = "6HL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2011"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f6hm(Variable):
    cerfa_field = "6HM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2012"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f6hn(Variable):
    cerfa_field = "6HN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2013"
    # start_date = date(2014, 1, 1)
    definition_period = YEAR


class f6ho(Variable):
    cerfa_field = "6HO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2014"
    # start_date = date(2015, 1, 1)
    definition_period = YEAR


class f6hp(Variable):
    cerfa_field = "6HP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2015"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f6hq(Variable):
    cerfa_field = "6HQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2016"
    # start_date = date(2017, 1, 1)
    definition_period = YEAR


class f6hr(Variable):
    cerfa_field = "6HR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses de l'année 2017"
    # start_date = date(2018, 1, 1)
    definition_period = YEAR


# Sommes à rajouter au revenu imposable
class f6gh(Variable):
    cerfa_field = "6GH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Sommes à ajouter au revenu imposable"
    definition_period = YEAR


# Deficits antérieurs
class f6fa(Variable):
    cerfa_field = "6FA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6"
    definition_period = YEAR


class f6fb(Variable):
    cerfa_field = "6FB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5"
    definition_period = YEAR


class f6fc(Variable):
    cerfa_field = "6FC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4"
    definition_period = YEAR


class f6fd(Variable):
    cerfa_field = "6FD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3"
    definition_period = YEAR


class f6fe(Variable):
    cerfa_field = "6FE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2"
    definition_period = YEAR


class f6fl(Variable):
    cerfa_field = "6FL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1"
    definition_period = YEAR


class rfr_cd(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Charges déductibles entrant dans le revenus fiscal de référence"
    reference = "Article 1417 du Code Général des Impôts - IV-1°-a)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        cd_eparet = foyer_fiscal('cd_eparet', period)
        cd_sofipe = foyer_fiscal('cd_sofipe', period)

        return cd_eparet + cd_sofipe

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        cd_eparet = foyer_fiscal('cd_eparet', period)

        return cd_eparet


class cd1(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Charges déductibles non plafonnées"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2002
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        pertes_capital_societes_nouvelles = foyer_fiscal('pertes_capital_societes_nouvelles', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_doment = foyer_fiscal('cd_doment', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + pertes_capital_societes_nouvelles + cd_deddiv + cd_doment
        return niches1

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2004
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        pertes_capital_societes_nouvelles = foyer_fiscal('pertes_capital_societes_nouvelles', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_doment = foyer_fiscal('cd_doment', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)

        niches1 = (
            pensions_alimentaires_deduites
            + cd_acc75a
            + pertes_capital_societes_nouvelles
            + cd_deddiv
            + cd_doment
            + cd_eparet
            )

        return niches1

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2006
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        pertes_capital_societes_nouvelles = foyer_fiscal('pertes_capital_societes_nouvelles', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + pertes_capital_societes_nouvelles + cd_deddiv + cd_eparet
        return niches1

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2007
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet
        return niches1

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2009
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)
        grosses_reparations = foyer_fiscal('grosses_reparations', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet + grosses_reparations
        return niches1

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles avant rbg_int pour 2014
        '''
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_acc75a = foyer_fiscal('cd_acc75a', period)
        cd_deddiv = foyer_fiscal('cd_deddiv', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)
        grosses_reparations = foyer_fiscal('grosses_reparations', period)

        niches1 = pensions_alimentaires_deduites + cd_acc75a + cd_deddiv + cd_eparet + grosses_reparations
        # log.error("Charges déductibles to be checked because not defined for %s", 2014)
        return niches1


class cd2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Charges déductibles plafonnées"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR
    end = '2008-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        cd_sofipe = foyer_fiscal('cd_sofipe', period)
        cinema = foyer_fiscal('souscriptions_cinema_audiovisuel', period)

        niches2 = cd_sofipe + cinema
        return niches2

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        cd_sofipe = foyer_fiscal('cd_sofipe', period)

        niches2 = cd_sofipe
        return niches2

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la liste des charges déductibles à intégrer après le rbg_int
        '''
        epargne_codeveloppement = foyer_fiscal('epargne_codeveloppement', period)

        niches2 = epargne_codeveloppement
        return niches2


class rbg_int(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenu brut global intermédiaire"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rbg = foyer_fiscal('rbg', period)
        cd1 = foyer_fiscal('cd1', period)

        return max_(rbg - cd1, 0)


class charges_deduc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Charges déductibles"
    reference = "http://impotsurlerevenu.org/definitions/215-charge-deductible.php"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        cd1 = foyer_fiscal('cd1', period)
        cd2 = foyer_fiscal('cd2', period)

        return cd1 + cd2


class pensions_alimentaires_deduites(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Pensions alimentaires"
    reference = "http://frederic.anne.free.fr/Cours/ITV.htm"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f6gi = foyer_fiscal('f6gi', period)
        f6gj = foyer_fiscal('f6gj', period)
        f6gp = foyer_fiscal('f6gp', period)
        f6el = foyer_fiscal('f6el', period)
        f6em = foyer_fiscal('f6em', period)
        f6gu = foyer_fiscal('f6gu', period)
        penalim = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.pensions_alimentaires

        max1 = penalim.plafond
        taux_jgt_2006 = penalim.taux_jgt_2006
        # TODO: si vous subvenez seul(e) à l'entretien d'un enfant marié ou
        # pacsé ou chargé de famille, quel que soit le nmbre d'enfants du jeune
        # foyer, la déduction est limitée à 2*max
        # S'il habite chez ses parents, max 3359, sinon 5698
        return (
            min_(f6gi * (1 + taux_jgt_2006), max1)
            + min_(f6gj * (1 + taux_jgt_2006), max1)
            + min_(f6el, max1)
            + min_(f6em, max1)
            + f6gp
            * (1 + taux_jgt_2006) + f6gu
            )


class cd_acc75a(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Frais d’accueil sous votre toit d’une personne de plus de 75 ans"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f6eu = foyer_fiscal('f6eu', period)
        f6ev = foyer_fiscal('f6ev', period)
        acc75a = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.accueil_personne_agee
        amax = acc75a.plafond * max_(1, f6ev)
        return min_(f6eu, amax)


class pertes_capital_societes_nouvelles(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté"
    definition_period = YEAR
    end = '2006-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        f6cb = foyer_fiscal('f6cb', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        percap = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.pertes_en_capital_societes_nouvelles
        plafond_cb = percap.plafond_cb * (1 + maries_ou_pacses)
        return min_(f6cb, plafond_cb)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Pertes en capital consécutives à la souscription au capital de sociétés
        nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration
        complémentaire)
        '''
        f6cb = foyer_fiscal('f6cb', period)
        f6da = foyer_fiscal('f6da', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        percap = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.pertes_en_capital_societes_nouvelles
        plafond_cb = percap.plafond_cb * (1 + maries_ou_pacses)
        plafond_da = percap.plafond_da * (1 + maries_ou_pacses)
        return min_(min_(f6cb, plafond_cb) + min_(f6da, plafond_da), plafond_da)


class cd_deddiv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déductions diverses"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f6dd = foyer_fiscal('f6dd', period)

        return f6dd


class cd_doment(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Investissements DOM-TOM dans le cadre d’une entreprise"
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Investissements DOM-TOM dans le cadre d’une entreprise (case EH de la
        déclaration n° 2042 complémentaire)
        '''
        f6eh = foyer_fiscal('f6eh', period)

        return f6eh


class cd_eparet(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Charge déductible au titre de l'épargne retraite (PERP, PRÉFON, COREM et CGOS)"
    definition_period = YEAR

    def formula_2004(foyer_fiscal, period, parameters):
        f6ps_i = foyer_fiscal.members('f6ps', period)
        f6rs_i = foyer_fiscal.members('f6rs', period)
        f6ss_i = foyer_fiscal.members('f6ss', period)

        # TODO: En théorie, les plafonds de déductions (ps, pt, pu) sont calculés sur
        # le formulaire 2041 GX
        return foyer_fiscal.sum(
            where(
                f6ps_i == 0,
                f6rs_i + f6ss_i,
                min_(f6rs_i + f6ss_i, f6ps_i)
                )
            )


class cd_sofipe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Souscriptions au capital des SOFIPÊCHE"
    end = '2006-12-31'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des SOFIPÊCHE (case CC de la déclaration
        complémentaire)
        '''
        f6cc = foyer_fiscal('f6cc', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        sofipeche = parameters(period).impot_revenu.calcul_reductions_impots.sofipeche

        plafond = min_(sofipeche.plafond_pct_rng * rbg_int, sofipeche.plafond * (1 + maries_ou_pacses))
        return min_(f6cc, plafond)


class souscriptions_cinema_audiovisuel(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Souscriptions en faveur du cinéma ou de l’audiovisuel"
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Souscriptions en faveur du cinéma ou de l’audiovisuel (case AA de la
        déclaration n° 2042 complémentaire)
        '''
        f6aa = foyer_fiscal('f6aa', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        cinema = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.cinema

        max1 = min_(cinema.taux * rbg_int, cinema.max)
        return min_(f6aa, max1)


class epargne_codeveloppement(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Versements sur un compte épargne codéveloppement"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2007(foyer_fiscal, period, parameters):
        '''
        Versements sur un compte épargne codéveloppement (case EH de la déclaration
        complémentaire)
        '''
        f6eh = foyer_fiscal('f6eh', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        ecodev = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.compte_epargne_codev

        plafond = min_(ecodev.plafond_pct_rng * rbg_int, ecodev.plafond)
        return min_(f6eh, plafond)


class grosses_reparations(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Dépenses de grosses réparations des nus-propriétaires"
    reference = "http://bofip.impots.gouv.fr/bofip/1852-PGP"
    definition_period = YEAR

    def formula_2009(foyer_fiscal, period, parameters):
        '''
        Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
        '''

        f6cb = foyer_fiscal('f6cb', period)
        plafond_grosses_reparations = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.grosses_reparations.plafond

        return min_(f6cb, plafond_grosses_reparations)

    def formula_2010(foyer_fiscal, period, parameters):
        '''
        Dépenses de grosses réparations des nus-propriétaires
        '''
        f6cb = foyer_fiscal('f6cb', period)
        year = period.start.year

        report_depenses_depuis_2009 = sum(
            foyer_fiscal(case_report, period)
            for case_report in [
                "f6hj",
                "f6hk",
                "f6hl",
                "f6hm",
                "f6hn",
                "f6ho",
                "f6hp",
                "f6hq",
                "f6hr",
                ][0:year - 2009]
            )

        plafond_grosses_reparations = parameters(period).impot_revenu.calcul_revenus_imposables.charges_deductibles.grosses_reparations.plafond
        depenses_courantes = f6cb

        return min_(depenses_courantes + report_depenses_depuis_2009, plafond_grosses_reparations)
