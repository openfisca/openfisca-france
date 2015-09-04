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


from ...base import *  # noqa analysis:ignore

# Gain de levée d'options
# Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
# et les mettre en f1tvm comme pour salaire_imposable
# Il faut aussi le faire en amont dans les tables

# là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
# du coups je n'ai pas changé et j'ai fait un dico comme pour salaire_imposable

build_column('f1tv', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TV",
                                       QUIFOY['conj']: u"1UV",
                                       }))  # (f1tv,f1uv))

build_column('f1tw', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TW",
                                       QUIFOY['conj']: u"1UW",
                                       }))  # (f1tw,f1uw))

build_column('f1tx', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TX",
                                       QUIFOY['conj']: u"1UX",
                        }))  # (f1tx,f1ux))



build_column('f3si', IntCol(entity = 'foy',
                start = date(2012, 1, 1)))  # TODO: parmi ces cas créer des valeurs individuelles
#                                    # correspond à autre chose en 2009, vérifier 2011,2010

build_column('f3sa', IntCol(entity = 'foy', end = date(2009, 12, 31)))  # TODO: n'existe pas en 2013 et 2012 vérifier 2011 et 2010

build_column('f3sf', IntCol(entity = 'foy',
                start = date(2012, 1, 1)))  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

build_column('f3sd', IntCol(entity = 'foy',
                start = date(2012, 1, 1)))  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

build_column('f3vc', IntCol(entity = 'foy',
                label = u"Produits et plus-values exonérés provenant de structure de capital-risque",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'3VC'))

build_column('f3vd', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"3VD",
                               QUIFOY['conj']: u"3SD",
                               }))  # (f3vd, f3sd)

build_column('f3ve', IntCol(entity = 'foy',
                label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %",
                val_type = "monetary",
                cerfa_field = u'3VE'))
# """
# réutilisation case 3VE en 2013


#    build_column('f3ve', IntCol(entity = 'foy',
#                    label = u"Plus-values de cession de droits sociaux réalisées par des personnes domiciliées dans les DOM",
#                    val_type = "monetary",
#                    cerfa_field = u'3VE',
#                    end =date.datetime (2012, 12, 31)))
# """

build_column('f3vf', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VF",
                               QUIFOY['conj']: u"3SF",
                               }))  # (f3vf, f3sf)

# comment gérer les cases qui ont le même nom mais qui ne correspondent pas tout à fait à la même chose ?
# peut-ont garder le même nom et l'encadrer par des start-end ? ou avec un truc genre if sur l'année ?(pour ne pas avoir à changer le nom de la variable)
# si on garde le même nom avec des start-end, et si on intégre la variable partout où elle doit être (dans les différents calculs), est-on sûr que lors des calculs les start-end seront bien pris en compte ?
# ça rendra le modéle un peu moins clair parce qu'il y aura le même nom de variable pour des choses différentes et dans des calculs ne se rapportant pas aux mêmes choses,
# mais si les start-end fonctionne ça ne devrait pas avoir d'impact sur les calculs ? qu'en penses-tu ?

# ## build_column('f3vl', IntCol(entity = 'foy',
# ##                 label = u"Distributions par des sociétés de capital-risque taxables à 24 %",
# ##                 val_type = "monetary",
# ##                 cerfa_field = u'3VL'
# ##                 start = date(2009, 1, 1),
# ##                 end = date(2009, 12, 31)))#vérifier avant 2009

build_column('f3vl', IntCol(entity = 'foy',
                label = u"Distributions par des sociétés de capital-risque taxables à 19 %",
                val_type = "monetary",
                cerfa_field = u'3VL'))  # vérifier pour 2011 et 2010

build_column('f3vi', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VI",
                               QUIFOY['conj']: u"3SI",
                               }))  # (f3vi, f3si )

build_column('f3vm', IntCol(entity = 'foy',
                label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %",
                val_type = "monetary",
                cerfa_field = u'3VM'))

build_column('f3vt', IntCol(entity = 'foy',
                label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'3VT'))

build_column('f3vj', IntCol(entity = 'ind',
                label = u"Gains imposables sur option dans la catégorie des salaires",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VJ",
                               QUIFOY['conj']: u"3VK",
                               }))  # (f3vj, f3vk )

build_column('f3va', IntCol(entity = 'ind',
                label = u"Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"3VA",
                               QUIFOY['conj']: u"3VB",
                               }))  # (f3va, f3vb )))

# Plus values et gains taxables à des taux forfaitaires

build_column('f3vg', IntCol(entity = 'foy',
                label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés",
                val_type = "monetary",
                cerfa_field = u'3VG'))

build_column('f3vh', IntCol(entity = 'foy',
                label = u"Perte de l'année de perception des revenus",
                val_type = "monetary",
                cerfa_field = u'3VH'))

build_column('f3vu', IntCol(entity = 'foy',
                end = date(2009, 12, 31)))  # TODO: vérifier pour 2010 et 2011

build_column('f3vv', IntCol(entity = 'foy',
    label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé",
    val_type = "monetary",
    start = date(2013, 1, 1),
    cerfa_field = u'3VV'))  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

build_column('f3vv_end_2010', IntCol(entity = 'foy',
    start = date(2010, 1, 1),
    end = date(2010, 12, 31),
    label = u"Pertes ouvrant droit au crédit d’impôt de 19 % ",
    val_type = "monetary",
    cerfa_field = u'3VV'))

build_column('f3vz', IntCol(entity = 'foy',
                 label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles",
                 val_type = "monetary",
                 cerfa_field = u'3VZ',
                 start = date(2011, 1, 1)))  # TODO: vérifier avant 2012
