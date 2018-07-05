# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

# Gain de levée d'options
# Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
# et les mettre en f1tvm comme pour salaire_imposable
# Il faut aussi le faire en amont dans les tables

# là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
# du coups je n'ai pas changé et j'ai fait un dico comme pour salaire_imposable

class f1tv(Variable):
    cerfa_field = {0: u"1TV",
        1: u"1UV",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans"
    end = '2015-12-31'
    definition_period = YEAR

  # (f1tv,f1uv))

class f1tw(Variable):
    cerfa_field = {0: u"1TW",
        1: u"1UW",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans"
    end = '2015-12-31'
    definition_period = YEAR

  # (f1tw,f1uw))

class f1tx(Variable):
    cerfa_field = {0: u"1TX",
        1: u"1UX",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans"
    end = '2016-12-31'
    definition_period = YEAR

  # (f1tx,f1ux))



class f3si(Variable):
    value_type = int
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: parmi ces cas créer des valeurs individuelles
#                                    # correspond à autre chose en 2009, vérifier 2011,2010

class f3sa(Variable):
    cerfa_field = u"3SA"
    value_type = int
    entity = FoyerFiscal
    label = u"Plus-values de cessions de titres réalisées par un entrepreneur, taxables à 19%"
    # start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f3sf(Variable):
    value_type = int
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

class f3sd(Variable):
    value_type = int
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

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
    definition_period = YEAR


class f3vy(Variable):
    cerfa_field = u"3VY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values exonérées de cessions de participations supérieures à 25% au sein du groupe familial"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class f3vd(Variable):
    cerfa_field = {0: u"3VD",
        1: u"3SD",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR

  # (f3vd, f3sd)

class f3ve(Variable):
    cerfa_field = u"3VE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %"
    definition_period = YEAR


class f3vf(Variable):
    cerfa_field = {0: u"3VF",
        1: u"3SF",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %"
    definition_period = YEAR

  # (f3vf, f3sf)

# comment gérer les cases qui ont le même nom mais qui ne correspondent pas tout à fait à la même chose ?
# peut-ont garder le même nom et l'encadrer par des start-end ? ou avec un truc genre if sur l'année ?(pour ne pas avoir à changer le nom de la variable)
# si on garde le même nom avec des start-end, et si on intégre la variable partout où elle doit être (dans les différents calculs), est-on sûr que lors des calculs les start-end seront bien pris en compte ?
# ça rendra le modéle un peu moins clair parce qu'il y aura le même nom de variable pour des choses différentes et dans des calculs ne se rapportant pas aux mêmes choses,
# mais si les start-end fonctionne ça ne devrait pas avoir d'impact sur les calculs ? qu'en penses-tu ?


class f3vl(Variable):
    cerfa_field = u"3VL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Distributions par des sociétés de capital-risque taxables à 19 %"
    end = '2013-12-31'
    definition_period = YEAR


class f3vi(Variable):
    cerfa_field = {0: u"3VI",
        1: u"3SI",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %"
    definition_period = YEAR

  # (f3vi, f3si )

class f3vm(Variable):
    cerfa_field = u"3VM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %"
    definition_period = YEAR


class f3vt(Variable):
    cerfa_field = u"3VT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f3vj(Variable):
    cerfa_field = {0: u"3VJ",
        1: u"3VK",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Gains imposables sur option dans la catégorie des salaires"
    definition_period = YEAR

  # (f3vj, f3vk )

class f3va(Variable):
    cerfa_field = u"3VA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u""
    # start_date = date(2006, 1, 1)
    definition_period = YEAR

class f3vb(Variable):
    cerfa_field = u"3VB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u""
    # start_date = date(2006, 1, 1)
    definition_period = YEAR

class f3sg(Variable):
    cerfa_field = u"3SG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention : appliqué sur des plus-values"
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


class abattement_net_retraite_dirigeant_pme(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    reference = u"http://bofip.impots.gouv.fr/bofip/2894-PGP"
    label = u"Abattement net pour durée de détention des titres en cas de départ à la retraite d'un dirigeant"
    definition_period = YEAR

    def formula_2006_01_01(foyer_fiscal, period):
        f3va = foyer_fiscal('f3va', period)
        f3vb = foyer_fiscal('f3va', period)

        return f3va - f3vb

class abatnet_duree_detention(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Abattement net pour durée de détention"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sh = foyer_fiscal('f3sh', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3sm = foyer_fiscal('f3sm', period)

        return max_(0, f3sg - f3sh) + max_(0, f3sl - f3sm)

    def formula_2015_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)

        return f3sg + f3sl


class abattement_net_duree_detention(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    reference = u"http://bofip.impots.gouv.fr/bofip/9540-PGP"
    label = u"Abattement net pour durée de détention"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sh = foyer_fiscal('f3sh', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3sm = foyer_fiscal('f3sm', period)

        return max_(0, f3sg - f3sh) + max_(0, f3sl - f3sm)

    def formula_2015_01_01(foyer_fiscal, period):
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)

        return f3sg + f3sl


# Plus values et gains taxables à des taux forfaitaires

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
    label = u"Perte de l'année de perception des revenus"
    definition_period = YEAR


class f3vu(Variable):
    value_type = int
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR

  # TODO: vérifier pour 2010 et 2011

class f3vv(Variable):
    cerfa_field = u"3VV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR

  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

class f3vv_end_2010(Variable):
    cerfa_field = u"3VV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Pertes ouvrant droit au crédit d’impôt de 19 % "
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f3vz(Variable):
    cerfa_field = u"3VZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR

  # TODO: vérifier avant 2012
