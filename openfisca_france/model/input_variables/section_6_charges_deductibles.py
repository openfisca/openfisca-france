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

from openfisca_core.columns import IntCol, PeriodSizeIndependentIntCol

from ..base import build_column_couple, column_by_name, QUIFOY


column_by_name.update(collections.OrderedDict((

    # Csg déductible
    build_column_couple('f6de', IntCol(entity = 'foy',
                    label = u"CSG déductible calculée sur les revenus du patrimoine",
                    val_type = "monetary",
                    cerfa_field = u'6DE')),

    # Pensions alimentaires
    build_column_couple('f6gi', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GI')),

    build_column_couple('f6gj', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GJ')),

    build_column_couple('f6el', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant",
                    val_type = "monetary",
                    start = datetime.date(2006, 1, 1),
                    cerfa_field = u'6EL')),

    build_column_couple('f6em', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant",
                    val_type = "monetary",
                    start = datetime.date(2006, 1, 1),
                    cerfa_field = u'6EM')),

    build_column_couple('f6gp', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)",
                    val_type = "monetary",
                    cerfa_field = u'6GP')),

    build_column_couple('f6gu', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées (mineurs, ascendants)",
                    start = datetime.date(2006, 1, 1),
                    val_type = "monetary",
                    cerfa_field = u'6GU')),

    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    build_column_couple('f6eu', IntCol(entity = 'foy',
                    label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin",
                    val_type = "monetary",
                    cerfa_field = u'6EU')),

    build_column_couple('f6ev', PeriodSizeIndependentIntCol(entity = 'foy',
                    label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit",
                    cerfa_field = u'6EV')),

    # Déductions diverses
    build_column_couple('f6dd', IntCol(entity = 'foy',
                    label = u"Déductions diverses",
                    val_type = "monetary",
                    cerfa_field = u'6DD')),

    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    build_column_couple('f6ps', IntCol(entity = 'ind',
                    label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6PS",
                                   QUIFOY['conj']: u"6PT",
                                   QUIFOY['pac1']: u"6PU",
                                   })),  # (f6ps, f6pt, f6pu)

    build_column_couple('f6rs', IntCol(entity = 'ind',
                    label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6RS",
                                   QUIFOY['conj']: u"6RT",
                                   QUIFOY['pac1']: u"6RU",
                                   })),  # (f6rs, f6rt, f6ru))),

    build_column_couple('f6ss', IntCol(entity = 'ind',
                    label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6SS",
                                   QUIFOY['conj']: u"6ST",
                                   QUIFOY['pac1']: u"6SU",
                                   })),  # (f6ss, f6st, f6su))),

    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    build_column_couple('f6aa', IntCol(entity = 'foy',
                    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel",
                    val_type = "monetary",
                    start = datetime.date(2005, 1, 1),
                    end = datetime.date(2006, 12, 31),
                    cerfa_field = u'6AA')),  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

    # Souscriptions au capital des SOFIPÊCHE
    build_column_couple('f6cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des SOFIPÊCHE",
                    val_type = "monetary",
                    cerfa_field = u'CC',
                    start = datetime.date(2005, 1, 1),
                    end = datetime.date(2005, 12, 31))),  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


    # Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
    # ou Versements sur un compte épargne codéveloppement
    build_column_couple('f6eh', IntCol(entity = 'foy',
                    label = u"",
                    val_type = "monetary",
                    start = datetime.date(2005, 1, 1),
                    end = datetime.date(2005, 12, 31),
                    cerfa_field = u'EH')),  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

    # Pertes en capital consécutives à la souscription au capital de sociétés
    # nouvelles ou de sociétés en difficulté
    build_column_couple('f6da', IntCol(entity = 'foy',
                    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté",
                    val_type = "monetary",
                    start = datetime.date(2005, 1, 1),
                    end = datetime.date(2005, 12, 31),
                    cerfa_field = u'DA')),


    # Dépenses de grosses réparations effectuées par les nus propriétaires
    build_column_couple('f6cb', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)",
                    val_type = "monetary",
                    start = datetime.date(2009, 1, 1),
                    cerfa_field = u'6CB')),
                                           # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

    build_column_couple('f6hj', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = datetime.date(2010, 1, 1),
                    cerfa_field = u'6HJ')),

    build_column_couple('f6hk', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = datetime.date(2011, 1, 1),
                    cerfa_field = u'6HK')),

    build_column_couple('f6hl', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = datetime.date(2012, 1, 1),
                    cerfa_field = u'6HL')),

    build_column_couple('f6hm', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = datetime.date(2013, 1, 1),
                    cerfa_field = u'6HM')),

    # Sommes à rajouter au revenu imposable
    build_column_couple('f6gh', IntCol(entity = 'foy',
                    label = u"Sommes à ajouter au revenu imposable",
                    val_type = "monetary",
                    cerfa_field = u'6GH')),

    # Deficits antérieurs
    build_column_couple('f6fa', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6",
                    val_type = "monetary",
                    cerfa_field = u'6FA')),

    build_column_couple('f6fb', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'6FB')),

    build_column_couple('f6fc', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'6FC')),

    build_column_couple('f6fd', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'6FD')),

    build_column_couple('f6fe', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'6FE')),

    build_column_couple('f6fl', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'6FL')),

    )))
