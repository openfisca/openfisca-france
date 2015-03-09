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


from ..base import *  # noqa


build_column('alt', BoolCol(label = u'Enfant en garde alternée'))  # TODO: cerfa_field


build_column('activite', EnumCol(label = u'Activité',
                     enum = Enum([u'Actif occupé',
                                u'Chômeur',
                                u'Étudiant, élève',
                                u'Retraité',
                                u'Autre inactif']), default = 4))


build_column('statmarit', EnumCol(label = u"Statut marital",
                      default = 2,
                      enum = Enum([u"Marié",
                                u"Célibataire",
                                u"Divorcé",
                                u"Veuf",
                                u"Pacsé",
                                u"Jeune veuf"], start = 1)))

build_column('nbN', PeriodSizeIndependentIntCol(cerfa_field = u'N', entity = 'foy',
    label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"))
build_column('nbR', PeriodSizeIndependentIntCol(cerfa_field = u'R', entity = 'foy',
    label = u"Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"))

build_column('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'E', end = date(2012, 12, 31)))
build_column('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)",
                  entity = 'foy',
                  cerfa_field = u'F'))
build_column('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                  entity = 'foy',
                  cerfa_field = u'G'))  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche
build_column('caseH', PeriodSizeIndependentIntCol(label = u"Année de naissance des enfants à charge en garde alternée", entity = 'foy',
                 cerfa_field = u'H'))
# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


build_column('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                  entity = 'foy',
                  cerfa_field = u'K', end = date(2011, 12, 31)))

build_column('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'L'))

build_column('caseN', BoolCol(label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'N'))
build_column('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                  entity = 'foy',
                  cerfa_field = u'P'))
build_column('caseS', BoolCol(label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'S'))

build_column('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'T'))

build_column('caseW', BoolCol(label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'W'))

