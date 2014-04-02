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

import collections
import datetime

from openfisca_core.columns import BoolCol, DateCol, EnumCol, FloatCol, IntCol, StrCol


from base import build_column_couple

column_by_name = collections.OrderedDict((
    # RVCM
    # revenus au prélèvement libératoire
    build_column_couple('f2da', IntCol(label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DA', end = datetime.date(2012, 12, 31))),  # à vérifier sur la nouvelle déclaration des revenus 2013

    build_column_couple('f2dh', IntCol(label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DH')),

    build_column_couple('f2ee', IntCol(label = u"Autres produits de placement soumis aux prélèvements libératoires",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2EE')),

    # revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
    build_column_couple('f2dc', IntCol(entity = 'foy',
                    label = u"Revenus des actions et parts donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2DC')),

    build_column_couple('f2fu', IntCol(entity = 'foy',
                    label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2FU')),
    build_column_couple('f2ch', IntCol(entity = 'foy',
                    label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2CH')),

    #  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
    build_column_couple('f2ts', IntCol(entity = 'foy', label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TS')),
    build_column_couple('f2go', IntCol(entity = 'foy',
                    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2GO')),
    build_column_couple('f2tr', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TR')),


    # Autres revenus des valeurs et capitaux mobiliers
    build_column_couple('f2cg', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2CG')),

    build_column_couple('f2bh', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2BH')),

    build_column_couple('f2ca', IntCol(entity = 'foy',
                    label = u"Frais et charges déductibles",
                    val_type = "monetary",
                    cerfa_field = u'2CA')),

    build_column_couple('f2ck', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé",
                    val_type = "monetary",
                    cerfa_field = u'2CK',
                    start = datetime.date(2013, 1, 1))),  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

    build_column_couple('f2ab', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt sur valeurs étrangères",
                    val_type = "monetary",
                    cerfa_field = u'2AB')),

    build_column_couple('f2bg', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables",
                    val_type = "monetary",
                    cerfa_field = u'2BG',
                    start = datetime.date(2012, 1, 1))),  # TODO: nouvelle case à créer où c'est nécessaire
                                     # TODO: vérifier existence avant 2012

    build_column_couple('f2aa', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AA')),

    build_column_couple('f2al', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AL')),

    build_column_couple('f2am', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AM')),

    build_column_couple('f2an', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AN',
                    start = datetime.date(2010, 1, 1))),

    build_column_couple('f2aq', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AQ',
                    start = datetime.date(2011, 1, 1))),

    build_column_couple('f2ar', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AR',
                    start = datetime.date(2012, 1, 1))),

# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
#
    build_column_couple('f2as', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2012", val_type = "monetary", end = datetime.date(2011, 12, 31))),  # TODO: vérifier existence <=2011

    build_column_couple('f2dm', IntCol(entity = 'foy',
                    label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %",
                    val_type = "monetary",
                    cerfa_field = u'2DM',
                    start = datetime.date(2012, 1, 1))),  # TODO: nouvelle case à utiliser où c'est nécessaire
                                     # TODO: vérifier existence avant 2012

    build_column_couple('f2gr', IntCol(entity = 'foy',
                    label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)",
                    val_type = "monetary",
                    cerfa_field = u'2GR',
                    start = datetime.date(2009, 1, 1),
                    end = datetime.date(2009, 12, 31))),  # TODO: vérifier existence à partir de 2011

    ))
