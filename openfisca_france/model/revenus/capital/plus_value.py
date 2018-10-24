# -*- coding: utf-8 -*-

from openfisca_france.model.base import *

# PLAN :
# 1) Gains taxés comme des salaires
# 2) Autres plus-values (exonérées, au barème, ...)
# 3) Abattements sur plus-values
# 4) Plus-values taxées forfaitairement
# 5) Autres variables


# Gains taxés comme des salaires

class f1tt(Variable):
    cerfa_field = {
        0: u"1TT",
        1: u"1UT",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 28.9.2012"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f1tv(Variable):
    cerfa_field = {
        0: u"1TV",
        1: u"1UV",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans"
    end = '2015-12-31'
    definition_period = YEAR


class f1tw(Variable):
    cerfa_field = {
        0: u"1TW",
        1: u"1UW",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans"
    end = '2015-12-31'
    definition_period = YEAR


class f1tx(Variable):
    cerfa_field = {
        0: u"1TX",
        1: u"1UX",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans"
    end = '2016-12-31'
    definition_period = YEAR


class f1tz(Variable):
    cerfa_field = u"1TZ"
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains d'acquisition d'actions gratuites attribuées sur décision prise à compter du 8.8.2015"
    # start_date = date(2015, 1, 1)
    definition_period = YEAR


class f3vj(Variable):
    cerfa_field = {
        0: u"3VJ",
        1: u"3VK",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains imposables sur option dans la catégorie des salaires"
    definition_period = YEAR


# Autres plus-values

class f3vg(Variable):
    cerfa_field = u"3VG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés"
    definition_period = YEAR


class f3vh(Variable):
    cerfa_field = u"3VH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Moins-value imposable su gains de cession de valeurs mobilières, de droits sociaux et gains assimilés"
    definition_period = YEAR


class f3vv(Variable):
    cerfa_field = u"3VV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé"
    # start_date = date(2013, 1, 1)
    end = '2013-12-31'
    definition_period = YEAR


class f3vz(Variable):
    cerfa_field = u"3VZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class f3vc(Variable):
    cerfa_field = u"3VC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Produits et plus-values exonérés provenant de structure de capital-risque"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class f3vp(Variable):
    cerfa_field = u"3VP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values exonérées de cessions de titres de jeunes entreprises innovantes"
    # start_date = date(2007, 1, 1)
    end = '2013-12-31'
    definition_period = YEAR


class f3vq(Variable):
    cerfa_field = u"3VQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Cessions de titres détenus à l'étranger par les impatriés : plus-values exonérées (50%)"
    definition_period = YEAR


class f3vr(Variable):
    cerfa_field = u"3VR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Cessions de titres détenus à l'étranger par les impatriés : moins-values non imputables (50%)"
    definition_period = YEAR


class f3vy(Variable):
    cerfa_field = u"3VY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values exonérées de cessions de participations supérieures à 25% au sein du groupe familial"
    # start_date = date(2011, 1, 1)
    end = '2013-12-31'
    definition_period = YEAR


class f3ve(Variable):
    cerfa_field = u"3VE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %"
    definition_period = YEAR


class f3tz(Variable):
    cerfa_field = u"3TZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values de cession de titres d'OPC monétaires en report d'imposition, plus-values réalisées du 1.1 au 31.3.2017, plus-values en report d'imposition"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f3sb(Variable):
    cerfa_field = u"3SB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition, dont le report a expiré cette année"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f3wb(Variable):
    cerfa_field = u"3WB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values des individus transférant leur domicile fiscal hors de France; plus-values et créances ne bénéficiant pas du sursis de paiement; plus-values nettes imposables au barème"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f3wd(Variable):
    cerfa_field = u"3WD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values des individus transférant leur domicile fiscal hors de France; plus-values et créances ne bénéficiant pas du sursis de paiement; plus-values de base soumise aux prélèvements sociaux"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f3we(Variable):
    """
    Plus-values en report d'imposition au sens de l'art. 150-0 D bis du CGI :
    Jusqu'aux revenus de 2013 : montants nets réalisés pendant l'année
    Pour les revenus 2014 : complément net de prix perçu pendant l'année (car fin du dispositif)
    Depuis les revenus 2015 : complément brut de prix perçu pendant l'année (l'abattement n'est plus recensé dans les cases 3SG et 3SL)
    """
    cerfa_field = u"3WE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition au sens de l'art. 150-0 D bis du CGI"
    definition_period = YEAR


class f3wn(Variable):
    cerfa_field = u"3WN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année, réalisées à compter du 1.1.2013 : plus-values avant abattement"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f3wp(Variable):
    cerfa_field = u"3WP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année, réalisées à compter du 1.1.2013 : plus-values après abattement"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f3wr(Variable):
    cerfa_field = u"3WR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année, réalisées à compter du 1.1.2013 : impôt sur le revenu"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f3wt(Variable):
    cerfa_field = u"3WT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année, réalisées à compter du 1.1.2013 : contribution exceptionnelle sur les hauts revenus"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# Abattements sur plus-values

class f3va_2014(Variable):
    cerfa_field = u"3VA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattements nets (abattement pour durée de détention renforcé et abattement fixe spécial) appliqués sur des plus-values réalisées par les dirigeants de PME lors de leur départ à la retraite"
    # start_date = date(2006, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class f3va_2016(Variable):
    cerfa_field = {
        0: u"3VA",
        1: u"3VB",
        2: u"3VO",
        3: u"3VP",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Abattements nets (abattement pour durée de détention renforcé et abattement fixe spécial) appliqués sur des plus-values réalisées par les dirigeants de PME lors de leur départ à la retraite"
    # start_date = date(2015, 1, 1)
    end = '2016-12-31'
    definition_period = YEAR


class f3va(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement fixe spécial appliqué sur des plus-values réalisées par les dirigeants de PME lors de leur départ à la retraite"
    # start_date = date(2017, 1, 1)
    definition_period = YEAR


class f3vb(Variable):
    cerfa_field = u"3VB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattements nets (abattement pour durée de détention renforcé et abattement fixe spécial) appliqués sur des moins-values réalisées par les dirigeants de PME lors de leur départ à la retraite"
    # start_date = date(2006, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class f3sg(Variable):
    cerfa_field = u"3SG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention (détention de droit commun à partir de 2015) : appliqué sur des plus-values"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f3sh(Variable):
    cerfa_field = u"3SH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention : appliqué sur des moins-values"
    # start_date = date(2013, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class f3sl(Variable):
    cerfa_field = u"3SL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention renforcée : appliqué sur des plus-values"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f3sm(Variable):
    cerfa_field = u"3SM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention renforcée : appliqué sur des moins-values"
    # start_date = date(2013, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class abattements_plus_values(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    reference = u"http://bofip.impots.gouv.fr/bofip/9540-PGP"
    label = u"Abattements sur plus-values notamment pour durée de détention de droit commun, renforcé, et abattement en cas de départ à la retraite d'un dirigeant de PME (abattement fixe et pour durée de détention)"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sh = foyer_fiscal('f3sh', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3sm = foyer_fiscal('f3sm', period)
        f3va = foyer_fiscal('f3va_2014', period)
        f3vb = foyer_fiscal('f3vb', period)

        return max_(0, f3sg - f3sh) + max_(0, f3sl - f3sm) + f3va - f3vb

    def formula_2015_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3va_i = foyer_fiscal.members('f3va_2016', period)
        f3va = foyer_fiscal.sum(f3va_i)

        return f3sg + f3sl + f3va

    def formula_2017_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3va = foyer_fiscal('f3va', period)

        return f3sg + f3sl + f3va


# Plus values et gains taxables à des taux forfaitaires

class f3vd(Variable):
    """ ATTENTION : à partir des revenus 2015, la case 3SD est supprimée : seule la case 3VD reste et recense les montants à l'échelle du foyer fiscal. Avec le code actuel, le seul problème serait si la case 3SD était réutilisée un jour pour autre chose dans le formulaire, ce qui n'est pas le cas aujourd'hui """
    cerfa_field = {
        0: u"3VD",
        1: u"3SD",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


class f3vi(Variable):
    """ ATTENTION : à partir des revenus 2015, la case 3SI est supprimée : seule la case 3VI reste et recense les montants à l'échelle du foyer fiscal. Avec le code actuel, le seul problème serait si la case 3SI était réutilisée un jour pour autre chose dans le formulaire, ce qui n'est pas le cas aujourd'hui """
    cerfa_field = {
        0: u"3VI",
        1: u"3SI",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %"
    definition_period = YEAR


class f3vf(Variable):
    """ ATTENTION : à partir des revenus 2015, la case 3SF est supprimée : seule la case 3VF reste et recense les montants à l'échelle du foyer fiscal. Avec le code actuel, le seul problème serait si la case 3SF était réutilisée un jour pour autre chose dans le formulaire, ce qui n'est pas le cas aujourd'hui """
    cerfa_field = {
        0: u"3VF",
        1: u"3SF",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %"
    definition_period = YEAR


class f3vm(Variable):
    cerfa_field = u"3VM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f3vt(Variable):
    cerfa_field = u"3VT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f3vl(Variable):
    cerfa_field = u"3VL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Distributions par des sociétés de capital-risque taxables à 19 %"
    end = '2013-12-31'
    definition_period = YEAR


class f3sa(Variable):
    cerfa_field = u"3SA"
    value_type = int
    entity = FoyerFiscal
    label = u"Plus-values de cessions de titres réalisées par un entrepreneur, taxables à 19%"
    # start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f3sj(Variable):
    cerfa_field = u"3SJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Gains de cession de bons de souscription de parts de créateur d'entreprise : gains taxables à 19%"
    definition_period = YEAR


class f3sk(Variable):
    cerfa_field = u"3SK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Gains de cession de bons de souscription de parts de créateur d'entreprise : gains taxables à 30%"
    definition_period = YEAR


class f3wi(Variable):
    cerfa_field = u"3WI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année : réalisées du 14.11.2012 au 31.12.2012 et taxables à 24%"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f3wj(Variable):
    cerfa_field = u"3WJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values en report d'imposition dont le report a expiré cette année : réalisées du 14.11.2012 au 31.12.2012 et taxables à 19%"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# Autres variables

class f3vv_end_2010(Variable):
    cerfa_field = u"3VV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Pertes ouvrant droit au crédit d’impôt de 19 % "
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f3ua(Variable):
    cerfa_field = u"3UA"
    label = u"Plus-values bénéficiant de l'abattement pour durée de détention renforcé et plus-values réalisées par les dirigeants de PME lors de leur départ à la retraite : plus-values après abattements"
    value_type = float
    entity = FoyerFiscal
    # start_date = date(2017, 1, 1) NB : Cette case existait avant 2017, mais les montants qui y étaient indiqués étaient également indiqués case 3VG
    definition_period = YEAR
