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


"""Variables apparaissant dans la feuille de déclaration de patrimoine soumis à l'ISF"""


import collections

from openfisca_core.columns import IntCol

from ..base import build_column_couple, column_by_name


column_by_name.update(collections.OrderedDict((
## Immeubles bâtis
    build_column_couple('b1ab', IntCol(entity = 'foy', label = u"Valeur de la résidence principale avant abattement", val_type = "monetary")),
    build_column_couple('b1ac', IntCol(entity = 'foy', label = u"Valeur des autres immeubles avant abattement", val_type = "monetary")),
## non bâtis
    build_column_couple('b1bc', IntCol(entity = 'foy', label = u"Immeubles non bâtis : bois, fôrets et parts de groupements forestiers", val_type = "monetary")),
    build_column_couple('b1be', IntCol(entity = 'foy', label = u"Immeubles non bâtis : biens ruraux loués à long termes", val_type = "monetary")),
    build_column_couple('b1bh', IntCol(entity = 'foy', label = u"Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type = "monetary")),
    build_column_couple('b1bk', IntCol(entity = 'foy', label = u"Immeubles non bâtis : autres biens", val_type = "monetary")),

## droits sociaux- valeurs mobilières-liquidités- autres meubles
    build_column_couple('b1cl', IntCol(entity = 'foy', label = u"Parts et actions détenues par les salariés et mandataires sociaux", val_type = "monetary")),
    build_column_couple('b1cb', IntCol(entity = 'foy', label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type = "monetary")),
    build_column_couple('b1cd', IntCol(entity = 'foy', label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type = "monetary")),
    build_column_couple('b1ce', IntCol(entity = 'foy', label = u"Autres valeurs mobilières", val_type = "monetary")),
    build_column_couple('b1cf', IntCol(entity = 'foy', label = u"Liquidités", val_type = "monetary")),
    build_column_couple('b1cg', IntCol(entity = 'foy', label = u"Autres biens meubles", val_type = "monetary")),

    build_column_couple('b1co', IntCol(entity = 'foy', label = u"Autres biens meubles : contrats d'assurance-vie", val_type = "monetary")),

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réductions
    build_column_couple('b2gh', IntCol(entity = 'foy', label = u"Total du passif et autres déductions", val_type = "monetary")),

## réductions
    build_column_couple('b2mt', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    build_column_couple('b2ne', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    build_column_couple('b2mv', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings" , val_type = "monetary")),
    build_column_couple('b2nf', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings", val_type = "monetary")),
    build_column_couple('b2mx', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FIP", val_type = "monetary")),
    build_column_couple('b2na', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type = "monetary")),
    build_column_couple('b2nc', IntCol(entity = 'foy', label = u"Réductions pour dons à certains organismes d'intérêt général", val_type = "monetary")),

##  montant impôt acquitté hors de France
    build_column_couple('b4rs', IntCol(entity = 'foy', label = u"Montant de l'impôt acquitté hors de France", val_type = "monetary")),

## BOUCLIER FISCAL

    build_column_couple('rev_or', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('rev_exo', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    build_column_couple('tax_fonc', IntCol(entity = 'foy', label = u"Taxe foncière", val_type = "monetary")),
    build_column_couple('restit_imp', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('etr', IntCol()),

    )))
