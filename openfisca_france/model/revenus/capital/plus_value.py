# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

# Gain de levée d'options
# Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
# et les mettre en f1tvm comme pour salaire_imposable
# Il faut aussi le faire en amont dans les tables

# là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
# du coups je n'ai pas changé et j'ai fait un dico comme pour salaire_imposable

class f1tv(Variable):
    cerfa_field = {QUIFOY['vous']: u"1TV",
        QUIFOY['conj']: u"1UV",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans"
    definition_period = YEAR

  # (f1tv,f1uv))

class f1tw(Variable):
    cerfa_field = {QUIFOY['vous']: u"1TW",
        QUIFOY['conj']: u"1UW",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans"
    definition_period = YEAR

  # (f1tw,f1uw))

class f1tx(Variable):
    cerfa_field = {QUIFOY['vous']: u"1TX",
        QUIFOY['conj']: u"1UX",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans"
    definition_period = YEAR

  # (f1tx,f1ux))



class f3si(Variable):
    column = IntCol
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: parmi ces cas créer des valeurs individuelles
#                                    # correspond à autre chose en 2009, vérifier 2011,2010

class f3sa(Variable):
    column = IntCol
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR

  # TODO: n'existe pas en 2013 et 2012 vérifier 2011 et 2010

class f3sf(Variable):
    column = IntCol
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

class f3sd(Variable):
    column = IntCol
    entity = FoyerFiscal
    # start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

class f3vc(Variable):
    cerfa_field = u"3VC"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Produits et plus-values exonérés provenant de structure de capital-risque"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR



class f3vd(Variable):
    cerfa_field = {QUIFOY['vous']: u"3VD",
        QUIFOY['conj']: u"3SD",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR

  # (f3vd, f3sd)

class f3ve(Variable):
    cerfa_field = u"3VE"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %"
    definition_period = YEAR


class f3vf(Variable):
    cerfa_field = {QUIFOY['vous']: u"3VF",
        QUIFOY['conj']: u"3SF",
        }
    column = IntCol(val_type = "monetary")
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
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Distributions par des sociétés de capital-risque taxables à 19 %"
    definition_period = YEAR

  # vérifier pour 2011 et 2010

class f3vi(Variable):
    cerfa_field = {QUIFOY['vous']: u"3VI",
        QUIFOY['conj']: u"3SI",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %"
    definition_period = YEAR

  # (f3vi, f3si )

class f3vm(Variable):
    cerfa_field = u"3VM"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %"
    definition_period = YEAR


class f3vt(Variable):
    cerfa_field = u"3VT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


class f3vj(Variable):
    cerfa_field = {QUIFOY['vous']: u"3VJ",
        QUIFOY['conj']: u"3VK",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Gains imposables sur option dans la catégorie des salaires"
    definition_period = YEAR

  # (f3vj, f3vk )

class f3va(Variable):
    cerfa_field = {QUIFOY['vous']: u"3VA",
        QUIFOY['conj']: u"3VB",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR

  # (f3va, f3vb )))

# Plus values et gains taxables à des taux forfaitaires

class f3vg(Variable):
    cerfa_field = u"3VG"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés"
    definition_period = YEAR


class f3vh(Variable):
    cerfa_field = u"3VH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Perte de l'année de perception des revenus"
    definition_period = YEAR


class f3vu(Variable):
    column = IntCol
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR

  # TODO: vérifier pour 2010 et 2011

class f3vv(Variable):
    cerfa_field = u"3VV"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR

  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

class f3vv_end_2010(Variable):
    cerfa_field = u"3VV"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Pertes ouvrant droit au crédit d’impôt de 19 % "
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f3vz(Variable):
    cerfa_field = u"3VZ"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR

  # TODO: vérifier avant 2012
