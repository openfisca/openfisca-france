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


from ...base import *  # noqa


# Dons à des organismes établis en France
build_column('f7ud', IntCol(entity = 'foy',
                label = u"Dons à des organismes d'aide aux personnes en difficulté",
                val_type = "monetary",
                cerfa_field = u'7UD'))

build_column('f7uf', IntCol(entity = 'foy',
                label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général",
                val_type = "monetary",
                cerfa_field = u'7UF')) # début/fin ?

build_column('f7xs', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5",
                val_type = "monetary",
                cerfa_field = u'7XS'))

build_column('f7xt', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'7XT'))

build_column('f7xu', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'7XU'))

build_column('f7xw', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'7XW'))

build_column('f7xy', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7XY'))

build_column('f7va', IntCol(entity = 'foy',
                label = u"Dons à des organismes d'aides aux personnes établis dans un Etat européen",
                val_type = "monetary",
                cerfa_field = u'7VA',
                start = date(2011, 1, 1)))

build_column('f7vc', IntCol(entity = 'foy',
                label = u"Dons à des autres organismes établis dans un Etat européen",
                val_type = "monetary",
                cerfa_field = u'7VC',
                start = date(2011, 1, 1)))  # f7va, f7vc 2011 ou 2013 ?

# Cotisations syndicales des salariées et pensionnés
build_column('f7ac', IntCol(entity = 'ind',
                label = u"Cotisations syndicales des salariées et pensionnés",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"7AC",
                               QUIFOY['conj']: u"7AE",
                               QUIFOY['pac1']: u"7AG",
                               }))  # f7ac, f7ae, f7ag

# Salarié à domicile
build_column('f7db', IntCol(entity = 'foy',
                label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'7DB'))

build_column('f7df', IntCol(entity = 'foy',
                label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7DF'))

build_column('f7dq', BoolCol(entity = 'foy',
                 label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés",
                 start = date(2009, 1, 1),
                 cerfa_field = u'7DQ'))

build_column('f7dg', BoolCol(entity = 'foy',
                 label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés",
                 cerfa_field = u'7DG'))

build_column('f7dl', IntCol(entity = 'foy',
                label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés",
                cerfa_field = u'7DL'))

# Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
build_column('f7uh_2007', IntCol(entity = 'foy',
                label = u"Intérêts payés la première année de remboursement du prêt pour l'habitation principale",
                val_type = "monetary",
                cerfa_field = u'7UH',
                start = date(2007, 1, 1),
                end = date(2007, 12, 31)))

build_column('f7vy', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7VY'))

build_column('f7vz', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7VZ'))

build_column('f7vx', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011",
                val_type = "monetary",
                cerfa_field = u'7VX'))

build_column('f7vw', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7VW'))

build_column('f7vv', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7VV'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

build_column('f7vu', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7VU'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

build_column('f7vt', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7VT'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

# Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
build_column('f7cd', IntCol(entity = 'foy',
                label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne",
                val_type = "monetary",
                cerfa_field = u'7CD'))

build_column('f7ce', IntCol(entity = 'foy',
                label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne",
                val_type = "monetary",
                cerfa_field = u'7CE'))

# Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
build_column('f7ga', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GA'))

build_column('f7gb', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GB'))

build_column('f7gc', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GC'))

build_column('f7ge', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GE'))

build_column('f7gf', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GF'))

build_column('f7gg', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GG'))

# Nombre d'enfants à charge poursuivant leurs études
build_column('f7ea', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études au collège",
                cerfa_field = u'7EA'))

build_column('f7eb', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège",
                cerfa_field = u'7EB'))

build_column('f7ec', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études au lycée",
                cerfa_field = u'7EC'))

build_column('f7ed', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée",
                cerfa_field = u'7ED'))

build_column('f7ef', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur",
                cerfa_field = u'7EF'))

build_column('f7eg', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur",
                cerfa_field = u'7EG'))

# Intérêts des prêts étudiants
build_column('f7td', IntCol(entity = 'foy',
                label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7TD'))

build_column('f7vo', PeriodSizeIndependentIntCol(entity = 'foy',
                label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés",
                start = date(2006, 1, 1),
                cerfa_field = u'7VO'))

build_column('f7uk', IntCol(entity = 'foy',
                label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7UK'))

# Primes de rente survie, contrats d'épargne handicap
build_column('f7gz', IntCol(entity = 'foy',
                label = u"Primes de rente survie, contrats d'épargne handicap",
                val_type = "monetary",
                cerfa_field = u'7GZ'))

# Prestations compensatoires
build_column('f7wm', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Capital fixé en substitution de rente",
                val_type = "monetary",
                cerfa_field = u'7WM'))

build_column('f7wn', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7WN'))

build_column('f7wo', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué",
                val_type = "monetary",
                cerfa_field = u'7WO'))

build_column('f7wp', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'7WP'))

# Dépenses en faveur de la qualité environnementale de l'habitation principale
build_column('f7we', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés",
                start = date(2009, 1, 1),
                cerfa_field = u'7WE'))

build_column('f7wg', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1",
                val_type = "monetary",
                cerfa_field = u'7WG',
                start = date(2012, 1, 1)))

build_column('f7wa', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs avant le 03/04/2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WA'))

build_column('f7wb', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs à compter du 04/04/2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WB'))

build_column('f7wc', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique sur plus de la moitié de la surface des murs extérieurs",
                start = date(2012, 1, 1),
                cerfa_field = u'7WC'))

build_column('f7ve', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture avant le 04/04/2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7VE'))

build_column('f7vf', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture à compter du 04/04/2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7VF'))

build_column('f7vg', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de toute la toiture",
                start = date(2012, 1, 1),
                cerfa_field = u'7VG'))

build_column('f7sg', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des murs (acquisitionn et pose)",
                start = date(2012, 1, 1),
                cerfa_field = u'7SG'))

build_column('f7sj', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des parois vitrées",
                start = date(2012, 1, 1),
                cerfa_field = u'7SJ'))

build_column('f7sk', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Volets isolants",
                start = date(2012, 1, 1),
                cerfa_field = u'7SK'))

build_column('f7sl', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Portes d'entrées donnant sur l'extérieur",
                start = date(2012, 1, 1),
                cerfa_field = u'7SL'))

build_column('f7sm', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de production d'électricité utilisant l'énergie radiative du soleil",
                start = date(2012, 1, 1),
                cerfa_field = u'7SM'))

build_column('f7sn', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent",
                start = date(2012, 1, 1),
                cerfa_field = u'7SN'))

build_column('f7so', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent",
                start = date(2012, 1, 1),
                cerfa_field = u'7SO'))

build_column('f7sp', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur",
                start = date(2012, 1, 1),
                cerfa_field = u'7SP'))

build_column('f7sq', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur",
                start = date(2012, 1, 1),
                cerfa_field = u'7SQ'))

build_column('f7sr', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques)",
                start = date(2012, 1, 1),
                cerfa_field = u'7SR'))

build_column('f7ss', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires",
                start = date(2012, 1, 1),
                cerfa_field = u'7SS'))

build_column('f7st', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (éolien, hydraulique)",
                start = date(2012, 1, 1),
                cerfa_field = u'7ST'))

build_column('f7su', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de récupération et de traitement des eaux pluviales",
                start = date(2012, 1, 1),
                cerfa_field = u'7SU'))

build_column('f7sv', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Diagnostic de performance énergétique",
                start = date(2012, 1, 1),
                cerfa_field = u'7SV'))

build_column('f7sw', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de raccordement à un réseau de chaleur",
                start = date(2012, 1, 1),
                cerfa_field = u'7SW'))

              # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                # TODO vérifier pour les années précédentes
# TODO: CHECK
# Intérêts d'emprunts
#     build_column('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')) # cf pour quelle année
#
build_column('f7wq', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées du 01/01/2012 au 03/04/2012",
                start = date(2010, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WQ'))

build_column('f7ws', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolations des parois vitrées à compter du 04/04/2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WS'))

build_column('f7wt', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement ",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WT'))

build_column('f7wu', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets avant 2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WU'))

build_column('f7wv', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets en 2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WV'))

build_column('f7ww', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes avant 2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WW'))

build_column('f7wx', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes en 2012",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7WX'))

build_column('f7wh', BoolCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus",
                start = date(2013, 1, 1),
                cerfa_field = u'7WH'))

build_column('f7wk', BoolCol(entity = 'foy',
                 label = u"Votre habitation principale est une maison individuelle",
                 start = date(2009, 1, 1),
                 cerfa_field = u'7WK'))

build_column('f7wf', BoolCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1",
                end = date(2013, 12, 31),
                cerfa_field = u'7WF'))

# Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
build_column('f7wi', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction",
                val_type = "monetary",
                cerfa_field = u'7WI',
                end = date(2012, 12, 31)))

build_column('f7wj', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées",
                val_type = "monetary",
                cerfa_field = u'7WJ'))

build_column('f7wl', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7WL'))

build_column('f7wr', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans des habitations données en location : travaux de prévention des risques technologiques",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7WR'))

# Investissements dans les DOM-TOM dans le cadre d'une entrepise
build_column('f7ur', IntCol(entity = 'foy',
                label = u"Investissements réalisés en n-1, total réduction d’impôt",
                val_type = "monetary",
                cerfa_field = u'7UR',
                end = date(2008, 12, 31)))

build_column('f7oz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6",
                val_type = "monetary",
                cerfa_field = u'7OZ',
                end = date(2011, 12, 31)))  # TODO: vérifier les années antérieures

build_column('f7pz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7PZ',
                end = date(2013, 12, 31)))

build_column('f7qz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7QZ',
                end = date(2012, 12, 31)))

build_column('f7rz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3",
                val_type = "monetary",
                cerfa_field = u'7RZ',
                end = date(2010, 12, 31)))

build_column('f7qv', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010, nvestissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%",
                val_type = "monetary",
                cerfa_field = u'7QV',
                end = date(2011, 12, 31)))

build_column('f7qo', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 50%",
                val_type = "monetary",
                cerfa_field = u'7QO',
                end = date(2009, 12, 31)))

build_column('f7qp', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 60%",
                val_type = "monetary",
                cerfa_field = u'7QP',
                end = date(2009, 12, 31)))

build_column('f7pa', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'7PA',
                end = date(2011, 12, 31)))

build_column('f7pb', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'7PB',
                end = date(2011, 12, 31)))

build_column('f7pc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée",
                val_type = "monetary",
                cerfa_field = u'7PC',
                end = date(2011, 12, 31)))

build_column('f7pd', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011",
                val_type = "monetary",
                cerfa_field = u'7PD',
                end = date(2011, 12, 31)))

build_column('f7qe', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%",
                val_type = "monetary",
                cerfa_field = u'7QE',
                end = date(2009, 12, 31)))

build_column('f7pe', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'7PE',
                end = date(2011, 12, 31)))

build_column('f7pf', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'7PF',
                end = date(2011, 12, 31)))

build_column('f7pg', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée",
                val_type = "monetary",
                cerfa_field = u'7PG',
                end = date(2011, 12, 31)))

build_column('f7ph', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011",
                val_type = "monetary",
                cerfa_field = u'7PH',
                end = date(2011, 12, 31)))

build_column('f7pi', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'7PI',
                end = date(2011, 12, 31)))

build_column('f7pj', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'7PJ',
                end = date(2011, 12, 31)))

build_column('f7pk', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt calculée",
                val_type = "monetary",
                cerfa_field = u'7PK',
                end = date(2011, 12, 31)))

build_column('f7pl', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011",
                val_type = "monetary",
                cerfa_field = u'7PL',
                end = date(2011, 12, 31)))

build_column('f7pm', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%",
                cerfa_field = u'7PM',
                end = date(2013, 12, 31)))

build_column('f7pn', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %",
                cerfa_field = u'7PN',
                end = date(2013, 12, 31)))

build_column('f7po', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %",
                cerfa_field = u'7PO',
                end = date(2013, 12, 31)))

build_column('f7pp', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise",
                cerfa_field = u'7PP',
                end = date(2013, 12, 31)))

build_column('f7pq', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7PQ',
                end = date(2013, 12, 31)))

build_column('f7pr', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7PR',
                end = date(2013, 12, 31)))

build_column('f7ps', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %",
                cerfa_field = u'7PS',
                end = date(2013, 12, 31)))

build_column('f7pt', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %",
                cerfa_field = u'7PT',
                end = date(2013, 12, 31)))

build_column('f7pu', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise",
                cerfa_field = u'7PU',
                end = date(2013, 12, 31)))

build_column('f7pv', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7PV',
                end = date(2013, 12, 31)))

build_column('f7pw', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7PW',
                end = date(2013, 12, 31)))

build_column('f7px', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt  à hauteur de 52,63 %",
                cerfa_field = u'7PX',
                end = date(2013, 12, 31)))

build_column('f7py', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %",
                cerfa_field = u'7PY',
                start = date(2012, 1, 1)))

build_column('f7rg', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise",
                cerfa_field = u'7RG',
                start = date(2012, 1, 1)))

build_column('f7rh', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7RH',
                start = date(2012, 1, 1)))

build_column('f7ri', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7RI',
                start = date(2012, 1, 1)))

build_column('f7rj', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %",
                cerfa_field = u'7RJ',
                start = date(2012, 1, 1)))

build_column('f7rk', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %",
                cerfa_field = u'7RK',
                start = date(2012, 1, 1)))

build_column('f7rl', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %",
                cerfa_field = u'7RL',
                start = date(2012, 1, 1)))

build_column('f7rm', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise",
                cerfa_field = u'7RM',
                start = date(2012, 1, 1)))

build_column('f7rn', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7RN',
                start = date(2012, 1, 1)))

build_column('f7ro', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7RO',
                start = date(2012, 1, 1)))

build_column('f7rp', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %",
                cerfa_field = u'7RP',
                start = date(2012, 1, 1)))

build_column('f7rq', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %",
                cerfa_field = u'7RQ',
                start = date(2012, 1, 1)))

build_column('f7rr', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise",
                cerfa_field = u'7RR',
                start = date(2012, 1, 1)))

build_column('f7rs', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7RS',
                start = date(2012, 1, 1)))

build_column('f7rt', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7RT',
                start = date(2012, 1, 1)))

build_column('f7ru', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %",
                cerfa_field = u'7RU',
                start = date(2012, 1, 1)))

build_column('f7rv', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %",
                cerfa_field = u'7RV',
                start = date(2012, 1, 1)))

build_column('f7rw', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise",
                cerfa_field = u'7RW',
                start = date(2012, 1, 1)))

build_column('f7rx', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7RX',
                start = date(2012, 1, 1)))

build_column('f7ry', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7RY',
                start = date(2012, 1, 1)))

build_column('f7nu', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %",
                cerfa_field = u'7NU',
                start = date(2012, 1, 1)))

build_column('f7nv', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %",
                cerfa_field = u'7NV',
                start = date(2012, 1, 1)))

build_column('f7nw', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise",
                cerfa_field = u'7NW',
                start = date(2012, 1, 1)))

build_column('f7nx', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée",
                cerfa_field = u'7NX',
                start = date(2012, 1, 1)))

build_column('f7ny', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012",
                cerfa_field = u'7NY',
                start = date(2012, 1, 1))) #TODO: 7N* : end ?

build_column('f7mn', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%",
                val_type = "monetary",
                cerfa_field = u'7MN',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7lh', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%",
                val_type = "monetary",
                cerfa_field = u'7LH',
                end = date(2011, 12, 31)))

build_column('f7mb', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%",
                val_type = "monetary",
                cerfa_field = u'7MB',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7kt', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt, Investissements dans votre entreprise",
                val_type = "monetary",
                cerfa_field = u'7KT',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7li', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%",
                val_type = "monetary",
                cerfa_field = u'7LI',
                start = date(2011, 1, 1)))

build_column('f7mc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%",
                val_type = "monetary",
                cerfa_field = u'7MC',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7ku', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements dans votre entreprise",
                val_type = "monetary",
                cerfa_field = u'7KU',
                start = date(2011, 1, 1),
                end = date(2011, 12, 31)))

# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures

build_column('f7sz', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location",
                val_type = "monetary",
                cerfa_field = u'7SZ',
                start = date(2006, 1, 1)))

build_column('fhsa', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSA',
                start = date(2013, 1, 1)))

build_column('fhsb', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HSB',
                start = date(2013, 1, 1)))

build_column('fhsf', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSF',
                start = date(2013, 1, 1)))

build_column('fhsg', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HSG',
                start = date(2013, 1, 1)))

build_column('fhsc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2010",
                val_type = "monetary",
                cerfa_field = u'HSC',
                start = date(2013, 1, 1)))

build_column('fhsh', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2011",
                val_type = "monetary",
                cerfa_field = u'HSH',
                start = date(2013, 1, 1)))

build_column('fhsd', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2010",
                val_type = "monetary",
                cerfa_field = u'HSD',
                start = date(2013, 1, 1)))

build_column('fhsi', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2011",
                val_type = "monetary",
                cerfa_field = u'HSI',
                start = date(2013, 1, 1)))

build_column('fhse', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010",
                val_type = "monetary",
                cerfa_field = u'HSE',
                start = date(2013, 1, 1)))

build_column('fhsj', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011",
                val_type = "monetary",
                cerfa_field = u'HSJ',
                start = date(2013, 1, 1)))

build_column('fhsk', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSK',
                start = date(2013, 1, 1)))

build_column('fhsl', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HSL',
                start = date(2013, 1, 1)))

build_column('fhsp', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSP',
                start = date(2013, 1, 1)))

build_column('fhsq', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HSQ',
                start = date(2013, 1, 1)))

build_column('fhsm', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2010",
                val_type = "monetary",
                cerfa_field = u'HSM',
                start = date(2013, 1, 1)))

build_column('fhsr', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2011",
                val_type = "monetary",
                cerfa_field = u'HSR',
                start = date(2013, 1, 1)))

build_column('fhsn', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2010",
                val_type = "monetary",
                cerfa_field = u'HSN',
                start = date(2013, 1, 1)))

build_column('fhss', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2011",
                val_type = "monetary",
                cerfa_field = u'HSS',
                start = date(2013, 1, 1)))

build_column('fhso', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010",
                val_type = "monetary",
                cerfa_field = u'HSO',
                start = date(2013, 1, 1)))

build_column('fhst', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011",
                val_type = "monetary",
                cerfa_field = u'HST',
                start = date(2013, 1, 1)))

build_column('fhsu', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSU',
                start = date(2013, 1, 1)))

build_column('fhsv', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HSV',
                start = date(2013, 1, 1)))

build_column('fhsw', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise",
                val_type = "monetary",
                cerfa_field = u'HSW',
                start = date(2013, 1, 1)))

build_column('fhsx', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé",
                val_type = "monetary",
                cerfa_field = u'HSX',
                start = date(2013, 1, 1)))

build_column('fhsy', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013",
                val_type = "monetary",
                cerfa_field = u'HS',
                start = date(2013, 1, 1)))

build_column('fhsz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%",
                val_type = "monetary",
                cerfa_field = u'HSZ',
                start = date(2013, 1, 1)))

build_column('fhta', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%",
                val_type = "monetary",
                cerfa_field = u'HTA',
                start = date(2013, 1, 1)))

build_column('fhtb', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise",
                val_type = "monetary",
                cerfa_field = u'HTB',
                start = date(2013, 1, 1)))

build_column('fhtc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé",
                val_type = "monetary",
                cerfa_field = u'HTC',
                start = date(2013, 1, 1)))

build_column('fhtd', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013",
                val_type = "monetary",
                cerfa_field = u'HTD',
                start = date(2013, 1, 1)))

# Aide aux créateurs et repreneurs d'entreprises
build_column('f7fy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                cerfa_field = u'7FY',
                end = date(2011, 12, 31)))

build_column('f7gy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                cerfa_field = u'7GY',
                start = date(2006, 1, 1),
                end = date(2011, 12, 31)))

build_column('f7hy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                cerfa_field = u'7HY',
                start = date(2009, 1, 1),
                end = date(2011, 12, 31)))

build_column('f7ky', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1",
                cerfa_field = u'7KY',
                start = date(2009, 1, 1),
                end = date(2011, 12, 31)))

build_column('f7iy', IntCol(entity = 'foy',
                label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés",
                cerfa_field = u'7IY',
                start = date(2013, 1, 1)))

build_column('f7ly', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                start = date(2010, 1, 1),
                cerfa_field = u'7LY'))  # 2012 et 2013 ok

build_column('f7my', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                cerfa_field = u'7MY',
                start = date(2010, 1, 1)))  # 2012 et 2013 ok

# Travaux de restauration immobilière
build_column('f7ra', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7RA'))  # 2012 et 2013 ok

build_column('f7rb', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7RB'))

build_column('f7rc', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7RC'))

build_column('f7rd', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7RD'))

build_column('f7re', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7RE'))

build_column('f7rf', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7RF'))

build_column('f7sx', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7SX'))

build_column('f7sy', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7SY')) # 2012 et 2013 ok

build_column('f7gw', IntCol(entity = 'foy',
                label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                cerfa_field = u'7GW',
                start = date(2013, 1, 1)))

build_column('f7gx', IntCol(entity = 'foy',
                label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                cerfa_field = u'7GX',
                start = date(2013, 1, 1)))

# Investissements locatifs dans le secteur de touristique
build_column('f7xa', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans un village résidentiel de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XA',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7xb', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans une résidence de tourisme classée ou meublée",
                val_type = "monetary",
                cerfa_field = u'7XB',
                start = date(2011, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7xc', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1",
                val_type = "monetary",
                cerfa_field = u'7XC',
                end = date(2012, 12, 31)))

build_column('f7xd', BoolCol(entity = 'foy',
                 label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                 cerfa_field = u'7XD',
                 start = date(2009, 1, 1),
                 end = date(2012, 12, 31)))

build_column('f7xe', BoolCol(entity = 'foy',
                 label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                 cerfa_field = u'7XE',
                 start = date(2009, 1, 1),
                 end = date(2012, 12, 31)))

build_column('f7xf', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XF'))

build_column('f7xh', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XH',
                end = date(2012, 12, 31)))

build_column('f7xi', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7XI'))

build_column('f7xj', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7XJ'))

build_column('f7xk', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7XK'))

build_column('f7xl', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans",
                val_type = "monetary",
                cerfa_field = u'7XL',
                end = date(2012, 12, 31)))

build_column('f7xm', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XM'))

# TODO: f7xn cf années < à 2011 (possible erreur dans le label pour ces dates, à vérifier)
build_column('f7xn', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XN',
                start = date(2012, 1, 1)))

build_column('f7xo', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7XO'))

build_column('f7xp', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7XP'))

build_column('f7xq', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7XQ'))

build_column('f7xr', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                start = date(2011, 1, 1),
                val_type = "monetary",
                cerfa_field = u'7XR'))

build_column('f7xv', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XV',
                start = date(2012, 1, 1)))

build_column('f7xx', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans un village résidentiel de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XX',
                start = date(2012, 1, 1),
                end = date(2012, 12, 31)))

build_column('f7xz', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans une résidence de tourisme classée ou un meublé tourisme",
                val_type = "monetary",
                cerfa_field = u'7XZ',
                start = date(2012, 1, 1)))

build_column('f7uy', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7UY',
                start = date(2013, 1, 1)))

build_column('f7uz', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7UZ',
                start = date(2013, 1, 1)))

# Souscriptions au capital des PME
build_column('f7cf', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion",
                val_type = "monetary",
                cerfa_field = u'7CF'))

build_column('f7cl', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'7CL'))

build_column('f7cm', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3",
                val_type = "monetary",
                cerfa_field = u'7CM'))

build_column('f7cn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2",
                val_type = "monetary",
                cerfa_field = u'7CN'))

build_column('f7cc', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7CC'))

build_column('f7cq', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1pour les start-up",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7CQ'))

build_column('f7cu', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures",
                val_type = "monetary",
                cerfa_field = u'7CU'))

# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée

build_column('f7gs', IntCol(entity = 'foy',
                label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7GS',
                start = date(2013, 1, 1)))

# Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
build_column('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UA', end = date(2007, 12, 31)))
build_column('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UB', end = date(2007, 12, 31)))

# En 2013 les "7" sont remplacés par des "H" dans les CERFA-FIELDS
# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = date(2011,12,31)))  # vérifier <=2011

build_column('f7uc', IntCol(entity = 'foy',
                label = u"Cotisations pour la défense des forêts contre l'incendie ",
                val_type = "monetary",
                cerfa_field = u'7UC'))

build_column('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UI', end = date(2008, 12, 31)))
build_column('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UJ', end = date(2007, 12, 31)))
build_column('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QB', end = date(2011, 12, 31)))
build_column('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QC', end = date(2011, 12, 31)))
build_column('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QD', end = date(2011, 12, 31)))
build_column('f7qk', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QK', end = date(2009, 12, 31)))
build_column('f7qn', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QN', end = date(2010, 12, 31)))
build_column('f7kg', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7KG', end = date(2010, 12, 31)))
build_column('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QL', end = date(2011, 12, 31)))
build_column('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QT', end = date(2011, 12, 31)))
build_column('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QM', end = date(2011, 12, 31)))
build_column('f7qu', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QU'))
build_column('f7ki', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7KI'))
build_column('f7qj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QJ'))
build_column('f7qw', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QW'))
build_column('f7qx', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QX'))
build_column('f7qf', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QF'))
build_column('f7qg', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QG'))
build_column('f7qh', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QH'))
build_column('f7qi', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QI'))
build_column('f7qq', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QQ'))
build_column('f7qr', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QR'))
build_column('f7qs', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QS'))
build_column('f7mm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7MM', start = date(2010, 1, 1), end = date(2012, 12, 31)))
build_column('f7lg', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7LG', start = date(2010, 1, 1)))
build_column('f7ma', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7MA', start = date(2010, 1, 1)))
build_column('f7ks', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7KS'))
build_column('f7kh', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7KH'))

build_column('f7oa', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009",
                val_type = "monetary",
                cerfa_field = u'7OA',
                start = date(2011, 1, 1)))

build_column('f7ob', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009",
                val_type = "monetary",
                cerfa_field = u'7OB',
                start = date(2011, 1, 1)))

build_column('f7oc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010",
                val_type = "monetary",
                cerfa_field = u'7OC',
                start = date(2011, 1, 1)))

build_column('f7oh', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009",
                val_type = "monetary",
                cerfa_field = u'7OH',
                start = date(2011, 1, 1)))

build_column('f7oi', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009",
                val_type = "monetary",
                cerfa_field = u'7OI',
                start = date(2011, 1, 1)))

build_column('f7oj', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010",
                val_type = "monetary",
                cerfa_field = u'7OJ',
                start = date(2011, 1, 1)))

build_column('f7ok', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Autres investissements",
                val_type = "monetary",
                cerfa_field = u'7OK',
                start = date(2011, 1, 1)))

build_column('f7ol', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009",
                val_type = "monetary",
                cerfa_field = u'7OL',
                start = date(2012, 1, 1)))

build_column('f7om', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009",
                val_type = "monetary",
                cerfa_field = u'7OM',
                start = date(2012, 1, 1)))

build_column('f7on', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010",
                val_type = "monetary",
                cerfa_field = u'7ON',
                start = date(2012, 1, 1)))

build_column('f7oo', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009",
                val_type = "monetary",
                cerfa_field = u'7OO',
                start = date(2012, 1, 1)))

build_column('f7op', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009",
                val_type = "monetary",
                cerfa_field = u'7OP',
                start = date(2012, 1, 1)))

build_column('f7oq', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010",
                val_type = "monetary",
                cerfa_field = u'7OQ',
                start = date(2012, 1, 1)))

build_column('f7or', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011",
                val_type = "monetary",
                cerfa_field = u'7OR',
                start = date(2012, 1, 1)))

build_column('f7os', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009",
                val_type = "monetary",
                cerfa_field = u'7OS',
                start = date(2012, 1, 1)))

build_column('f7ot', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009",
                val_type = "monetary",
                cerfa_field = u'7OT',
                start = date(2012, 1, 1)))

build_column('f7ou', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010",
                val_type = "monetary",
                cerfa_field = u'7OU',
                start = date(2012, 1, 1)))

build_column('f7ov', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011",
                val_type = "monetary",
                cerfa_field = u'7OV',
                start = date(2012, 1, 1)))

build_column('f7ow', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, ",
                val_type = "monetary",
                cerfa_field = u'7OW',
                start = date(2012, 1, 1))) #TODO: 7O* : end ?

build_column('fhod', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés avant le 1.1.2011",
                val_type = "monetary",
                cerfa_field = u'HOD',
                start = date(2013, 1, 1)))

build_column('fhoe', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010",
                val_type = "monetary",
                cerfa_field = u'HOE',
                start = date(2013, 1, 1)))

build_column('fhof', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011",
                val_type = "monetary",
                cerfa_field = u'HOF',
                start = date(2013, 1, 1)))


build_column('fhog', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010",
                val_type = "monetary",
                cerfa_field = u'HOG',
                start = date(2013, 1, 1)))


build_column('fhox', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2011",
                val_type = "monetary",
                cerfa_field = u'HOX',
                start = date(2013, 1, 1)))


build_column('fhoy', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2012",
                val_type = "monetary",
                cerfa_field = u'HOY',
                start = date(2013, 1, 1)))


build_column('fhoz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Autres investissements",
                val_type = "monetary",
                cerfa_field = u'HOZ',
                start = date(2013, 1, 1)))

# Investissements outre-mer dans le logement social

build_column('fhra', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010",
                val_type = "monetary",
                cerfa_field = u'HRA',
                start = date(2013, 1, 1)))

build_column('fhrb', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011",
                val_type = "monetary",
                cerfa_field = u'HRB',
                start = date(2013, 1, 1)))

build_column('fhrc', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2012",
                val_type = "monetary",
                cerfa_field = u'HRC',
                start = date(2013, 1, 1)))

build_column('fhrd', IntCol(entity = 'foy',
                label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Autres investissements",
                val_type = "monetary",
                cerfa_field = u'HRD',
                start = date(2013, 1, 1)))

# Souscription de parts de fonds communs de placement dans l'innovation,
# de fonds d'investissement de proximité
build_column('f7gq', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds communs de placement dans l'innovation",
                val_type = "monetary",
                cerfa_field = u'7GQ'))

build_column('f7fq', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité",
                val_type = "monetary",
                cerfa_field = u'7FQ'))

build_column('f7fm', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'7FM'))

build_column('f7fl', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7FL'))

# Souscriptions au capital de SOFICA
build_column('f7gn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital de SOFICA 36 %",
                val_type = "monetary",
                cerfa_field = u'7GN',
                start = date(2006, 1, 1)))

build_column('f7fn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital de SOFICA 30 %",
                val_type = "monetary",
                cerfa_field = u'7FN',
                start = date(2006, 1, 1)))

# Intérêts d'emprunt pour reprise de société
build_column('f7fh', IntCol(entity = 'foy',
                label = u"Intérêts d'emprunt pour reprise de société",
                val_type = "monetary",
                cerfa_field = u'7FH'))

# Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée))
build_column('f7ff', IntCol(entity = 'foy',
                label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)",
                val_type = "monetary",
                cerfa_field = u'7FF'))

build_column('f7fg', IntCol(entity = 'foy',
                label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations",
                cerfa_field = u'7FG'))

# Travaux de conservation et de restauration d’objets classés monuments historiques
build_column('f7nz', IntCol(entity = 'foy',
                label = u"Travaux de conservation et de restauration d’objets classés monuments historiques",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'7NZ'))

# Dépenses de protection du patrimoine naturel
build_column('f7ka', IntCol(entity = 'foy',
                label = u"Dépenses de protection du patrimoine naturel",
                val_type = "monetary",
                cerfa_field = u'7KA',
                start = date(2010, 1, 1)))

build_column('f7kb', IntCol(entity = 'foy',
                label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                val_type = "monetary",
                cerfa_field = u'7KB',
                start = date(2011, 1, 1)))

build_column('f7kc', IntCol(entity = 'foy',
                label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                val_type = "monetary",
                cerfa_field = u'7KC',
                start = date(2012, 1, 1)))

build_column('f7kd', IntCol(entity = 'foy',
                label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)",
                val_type = "monetary",
                cerfa_field = u'7KD',
                start = date(2013, 1, 1)))

build_column('f7uh', IntCol(entity = 'foy',
                label = u"Dons et cotisations versés aux partis politiques",
                val_type = "monetary",
                cerfa_field = u'7UH',
                start = date(2007, 1, 1))) #TODO: séparer en plusieurs variables (même case pour plusieurs variables selon les années)

# Investissements forestiers
build_column('f7un', IntCol(entity = 'foy',
                label = u"Investissements forestiers: acquisition",
                val_type = "monetary",
                cerfa_field = u'7UN'))

build_column('f7ul', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7UL'))

build_column('f7uu', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7UU'))

build_column('f7uv', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7UV'))

build_column('f7uw', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7UW'))

build_column('f7th', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7TH'))

build_column('f7ux', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7UX'))

build_column('f7tg', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7TG'))

build_column('f7tf', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2011, 1, 1),
                end = date(2013, 12, 31),
                cerfa_field = u'7TF'))

build_column('f7ut', IntCol(entity = 'foy',
                label = u"Investissements forestiers",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7UT'))

# Intérêts pour paiement différé accordé aux agriculteurs
build_column('f7um', IntCol(entity = 'foy',
                label = u"Intérêts pour paiement différé accordé aux agriculteurs",
                val_type = "monetary",
                cerfa_field = u'7UM'))

# Investissements locatifs neufs : Dispositif Scellier:
build_column('f7hj', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7HJ'))

build_column('f7hk', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7HK'))

build_column('f7hn', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HN'))

build_column('f7ho', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HO'))

build_column('f7hl', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HL'))

build_column('f7hm', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HM'))

build_column('f7hr', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HR'))

build_column('f7hs', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7HS'))

build_column('f7la', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2009",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7LA'))

build_column('f7lb', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2010",
                val_type = "monetary",
                cerfa_field = u'7LB',
                start = date(2011, 1, 1)))

build_column('f7lc', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2010",
                val_type = "monetary",
                cerfa_field = u'7LC',
                start = date(2011, 1, 1)))

build_column('f7ld', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2011",
                val_type = "monetary",
                cerfa_field = u'7LD',
                start = date(2012, 1, 1)))

build_column('f7le', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2011",
                val_type = "monetary",
                cerfa_field = u'7LE',
                start = date(2012, 1, 1)))

build_column('f7lf', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011",
                val_type = "monetary",
                cerfa_field = u'7LF',
                start = date(2012, 1, 1)))

build_column('f7ls', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010",
                val_type = "monetary",
                cerfa_field = u'7LS',
                start = date(2013, 1, 1)))

build_column('f7lm', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010",
                val_type = "monetary",
                cerfa_field = u'7LM',
                start = date(2013, 1, 1)))

build_column('f7lz', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Report du solde de réduction d'impôt de l'année 2012",
                val_type = "monetary",
                cerfa_field = u'7LZ',
                start = date(2013, 1, 1)))

build_column('f7mg', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2012 : report du solde de réduction d'impôt de l'année 2012",
                val_type = "monetary",
                cerfa_field = u'7MG',
                start = date(2013, 1, 1)))

build_column('f7na', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7NA',
                start = date(2011, 1, 1)))

build_column('f7nb', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, ",
                val_type = "monetary",
                cerfa_field = u'7NB',
                start = date(2011, 1, 1)))

build_column('f7nc', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7NC',
                start = date(2011, 1, 1)))

build_column('f7nd', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7ND',
                start = date(2011, 1, 1)))

build_column('f7ne', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7NE',
                start = date(2011, 1, 1)))

build_column('f7nf', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, ",
                val_type = "monetary",
                cerfa_field = u'7NF',
                start = date(2011, 1, 1)))

build_column('f7ng', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, ",
                val_type = "monetary",
                cerfa_field = u'7NG',
                start = date(2011, 1, 1)))

build_column('f7nh', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7NH',
                start = date(2011, 1, 1)))

build_column('f7ni', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7NI',
                start = date(2011, 1, 1)))

build_column('f7nj', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7NJ',
                start = date(2011, 1, 1)))

build_column('f7nk', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7NK',
                start = date(2011, 1, 1)))

build_column('f7nl', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7NL',
                start = date(2011, 1, 1)))

build_column('f7nm', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7NM',
                start = date(2011, 1, 1)))

build_column('f7nn', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7NN',
                start = date(2011, 1, 1)))

build_column('f7no', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7NO',
                start = date(2011, 1, 1)))

build_column('f7np', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7NP',
                start = date(2011, 1, 1)))

build_column('f7nq', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7NQ',
                start = date(2011, 1, 1)))

build_column('f7nr', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7NR',
                start = date(2011, 1, 1)))

build_column('f7ns', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7NS',
                start = date(2011, 1, 1)))

build_column('f7nt', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7NT',
                start = date(2011, 1, 1)))

build_column('f7hv', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole",
                val_type = "monetary",
                cerfa_field = u'7HV',
                start = date(2011, 1, 1)))

build_column('f7hw', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM",
                val_type = "monetary",
                cerfa_field = u'7HW',
                start = date(2011, 1, 1)))

build_column('f7hx', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole avec promesse d'achat avant le 1.1.2010",
                val_type = "monetary",
                cerfa_field = u'7HX',
                start = date(2011, 1, 1)))

build_column('f7hz', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM avec promesse d'achat avant le 1.1.2010",
                val_type = "monetary",
                cerfa_field = u'7HZ',
                start = date(2011, 1, 1)))

build_column('f7ht', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques",
                val_type = "monetary",
                cerfa_field = u'7HT',
                start = date(2011, 1, 1)))

build_column('f7hu', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques",
                val_type = "monetary",
                cerfa_field = u'7HU',
                start = date(2011, 1, 1)))

build_column('f7ha', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011",
                val_type = "monetary",
                cerfa_field = u'7HA',
                start = date(2012, 1, 1)))

build_column('f7hb', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011, avec promesse d'achat en 2010",
                val_type = "monetary",
                cerfa_field = u'7HB',
                start = date(2012, 1, 1)))

build_column('f7hg', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7HG',
                start = date(2012, 1, 1)))

build_column('f7hh', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna avec promesse d'achat en 2010",
                val_type = "monetary",
                cerfa_field = u'7HH',
                start = date(2012, 1, 1)))

build_column('f7hd', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, réalisés en 2010, en métropole et dans les DOM-COM",
                val_type = "monetary",
                cerfa_field = u'7HD',
                start = date(2012, 1, 1)))

build_column('f7he', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, en métropole et dans les DOM-COM avec promesse d'achat avant le 1.1.2010",
                val_type = "monetary",
                cerfa_field = u'7HE',
                start = date(2012, 1, 1)))

build_column('f7hf', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, Investissements réalisés en 2009 en métropole et dans les DOM-COM",
                val_type = "monetary",
                cerfa_field = u'7HF',
                start = date(2012, 1, 1)))

build_column('f7ja', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7JA',
                start = date(2012, 1, 1)))

build_column('f7jb', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7JB',
                start = date(2012, 1, 1)))

build_column('f7jd', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7JD',
                start = date(2012, 1, 1)))

build_column('f7je', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, BBC ",
                val_type = "monetary",
                cerfa_field = u'7JE',
                start = date(2012, 1, 1)))

build_column('f7jf', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7JF',
                start = date(2012, 1, 1)))

build_column('f7jg', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7JG',
                start = date(2012, 1, 1)))

build_column('f7jh', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7JH',
                start = date(2012, 1, 1)))

build_column('f7jj', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7JJ',
                start = date(2012, 1, 1)))

build_column('f7jk', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7JK',
                start = date(2012, 1, 1)))

build_column('f7jl', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7JL',
                start = date(2012, 1, 1)))

build_column('f7jm', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7JM',
                start = date(2012, 1, 1)))

build_column('f7jn', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7JN',
                start = date(2012, 1, 1)))

build_column('f7jo', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7JO',
                start = date(2012, 1, 1)))

build_column('f7jp', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7JP',
                start = date(2012, 1, 1)))

build_column('f7jq', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7JQ',
                start = date(2012, 1, 1)))

build_column('f7jr', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7JR',
                start = date(2012, 1, 1)))

build_column('f7gj', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7GJ',
                start = date(2013, 1, 1)))

build_column('f7gk', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2011",
                val_type = "monetary",
                cerfa_field = u'7GK',
                start = date(2013, 1, 1)))

build_column('f7gl', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7GL',
                start = date(2013, 1, 1)))

build_column('f7gp', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2010s",
                val_type = "monetary",
                cerfa_field = u'7GP',
                start = date(2013, 1, 1)))

build_column('f7fa', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, BBC",
                val_type = "monetary",
                cerfa_field = u'7FA',
                start = date(2013, 1, 1)))

build_column('f7fb', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, non-BBC",
                val_type = "monetary",
                cerfa_field = u'7FB',
                start = date(2013, 1, 1)))

build_column('f7fc', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7FC',
                start = date(2013, 1, 1)))

build_column('f7fd', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna",
                val_type = "monetary",
                cerfa_field = u'7FD',
                start = date(2013, 1, 1)))

# Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
build_column('f7ij', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, engagement de réalisation de l'investissement en 2011",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'7IJ'))

build_column('f7il', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, promesse d'achat en 2010",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7IL'))

build_column('f7im', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2010 et achevés en 2012 avec promesse d'achat en 2009",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7IM'))

build_column('f7ik', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Reports de 1/9 de l'investissement réalisé et achevé en 2009",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7IK'))

build_column('f7in', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.1.2011 au 31.3.2011",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IN'))

build_column('f7iv', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.4.2011 au 31.12.2011",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IV'))

build_column('f7iw', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2012",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IW'))

build_column('f7io', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IO'))

build_column('f7ip', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IP'))

build_column('f7ir', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IR'))

build_column('f7iq', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IQ'))

build_column('f7iu', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IU'))

build_column('f7it', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : ",
                val_type = "monetary",
                start = date(2011, 1, 1),
                cerfa_field = u'7IT'))

build_column('f7is', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Report du solde de réduction d'impôt non encore imputé: année  n-4",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7IS'))

build_column('f7ia', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IA'))

build_column('f7ib', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IB'))

build_column('f7ic', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2011 avec promesse d'achat en 2009 ou réalisés en 2009",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IC'))

build_column('f7id', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Engagement de réalisation de l'investissement en 2012",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7ID'))

build_column('f7ie', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Promesse d'achat en 2011",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IE'))

build_column('f7if', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.1.2012 au 31.3.2012, investissement réalisé du 1.1.2012 au 31.3.2012",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IF'))

build_column('f7ig', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.4.2012 au 31.12.2012",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IG'))

build_column('f7ix', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2009; réalisés en 2009 et achevés en 2010; réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report du solde de réduction d'impôt de l'année 2011",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IX'))

build_column('f7ih', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2011",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IH'))

build_column('f7iz', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7IZ'))

build_column('f7jt', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2013",
                val_type = "monetary",
                cerfa_field = u'7JT',
                start = date(2013, 1, 1)))

build_column('f7ju', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2012",
                val_type = "monetary",
                cerfa_field = u'7JU',
                start = date(2013, 1, 1)))

build_column('f7jv', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2012",
                val_type = "monetary",
                cerfa_field = u'7JV',
                start = date(2013, 1, 1)))

build_column('f7jw', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011",
                val_type = "monetary",
                cerfa_field = u'7JW',
                start = date(2013, 1, 1)))

build_column('f7jx', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010",
                val_type = "monetary",
                cerfa_field = u'7JX',
                start = date(2013, 1, 1)))

build_column('f7jy', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009",
                val_type = "monetary",
                cerfa_field = u'7JY',
                start = date(2013, 1, 1)))

build_column('f7jc', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2012",
                val_type = "monetary",
                cerfa_field = u'7JC',
                start = date(2013, 1, 1)))

build_column('f7ji', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d'impôt de l'année 2012",
                val_type = "monetary",
                cerfa_field = u'7JI',
                start = date(2013, 1, 1)))

build_column('f7js', IntCol(entity = 'foy',
                label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d’impôt de l’année 2012",
                val_type = "monetary",
                cerfa_field = u'7JS',
                start = date(2013, 1, 1)))

# Investissements locatifs dans les résidences de tourisme situées dans une zone de
# revitalisation rurale

# """
# réutilisation de cases en 2013
# """

build_column('f7gt', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010",
                val_type = "monetary",
                cerfa_field = u'7GT',
                start = date(2013, 1, 1)))  # vérif <=2012

build_column('f7gu', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009",
                val_type = "monetary",
                cerfa_field = u'7GU',
                start = date(2013, 1, 1)))  # vérif <=2012

build_column('f7gv', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna ",
                val_type = "monetary",
                cerfa_field = u'7GV',
                start = date(2013, 1, 1)))  # vérif <=2012

build_column('f7xg', IntCol(entity = 'foy', label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XG',
                end = date(2012, 12, 1)))  # vérif <=2012

# Crédits d'impôts en f7
# Acquisition de biens culturels
build_column('f7uo', IntCol(entity = 'foy',
                label = u"Acquisition de biens culturels",
                val_type = "monetary",
                cerfa_field = u'7UO'))

# Mécénat d'entreprise
build_column('f7us', IntCol(entity = 'foy',
                label = u"Réduction d'impôt mécénat d'entreprise",
                val_type = "monetary",
                cerfa_field = u'7US'))

# Crédits d’impôt pour dépenses en faveur de la qualité environnementale

build_column('f7sb', IntCol(entity = 'foy',
               label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %",
               val_type = "monetary",
               cerfa_field = u'7SB',
               start = date(2009, 1, 1),
               end = date(2011, 12, 31)))

build_column('f7sc', IntCol(entity = 'foy',
               label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale",
               val_type = "monetary",
               cerfa_field = u'7SC',
               start = date(2009, 1, 1),
               end = date(2009, 12, 1)))
# """
# réutilisation de case pour 2013
# """

build_column('f7sd', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation",
                val_type = "monetary",
                cerfa_field = u'7SD',
                start = date(2009, 1, 1)))

build_column('f7se', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz",
                val_type = "monetary",
                cerfa_field = u'7SE',
                start = date(2009, 1, 1)))

build_column('f7sh', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)",
                val_type = "monetary",
                cerfa_field = u'7SH',
                start = date(2010, 1, 1)))
# ('f7wg', IntCol() déjà disponible

# Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???

build_column('f7up', IntCol(entity = 'foy',
                label = u"Crédit d'impôt pour investissements forestiers: travaux",
                val_type = "monetary",
                cerfa_field = u'7UP',
                start = date(2009, 1, 1)))

build_column('f7uq', IntCol(entity = 'foy',
                label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion",
                val_type = "monetary",
                cerfa_field = u'7UQ',
                start = date(2009, 1, 1)))

# Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
build_column('f1ar', BoolCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité : le déclarant déménage à plus de 200 km pour son emploi",
                cerfa_field = u'1AR',
                end = date(2080, 12, 31)))
#TODO: QUIFOY
build_column('f1br', BoolCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité : le conjoint déménage à plus de 200 km pour son emploi",
                cerfa_field = u'1BR',
                end = date(2008, 12, 31)))

build_column('f1cr', BoolCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité : la 1ère personne à charge déménage à plus de 200 km pour son emploi",
                cerfa_field = u'1CR',
                end = date(2008, 12, 31)))

build_column('f1dr', BoolCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité : la 2è personne à charge déménage à plus de 200 km pour son emploi",
                cerfa_field = u'1DR',
                end = date(2008, 12, 31)))

build_column('f1er', BoolCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité : la 3è personne à charge déménage à plus de 200 km pour son emploi",
                cerfa_field = u'1ER',
                end = date(2006, 12, 31)))

# Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
build_column('f4tq', IntCol(entity = 'foy',
                label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail",
                val_type = "monetary",
                cerfa_field = u'4TQ'))  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                       # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                       # soumis à la taxe additionnelle au droit de bail

# Crédits d’impôt pour dépenses en faveur de l’aide aux personnes

build_column('f7sf', IntCol(entity = 'foy',
                label = u"Crédit de travaux en faveur d'aides aux personnes pour des logements en location (avant 2012 ) / Appareils de régulation du chauffage, matériaux de calorifugeage (après 2011)",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7SF'))

build_column('f7si', IntCol(entity = 'foy',
                label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'7SI'))

build_column('f7te', IntCol(entity = 'foy',
                label = u"Dépenses d'investissement forestier",
                val_type = "monetary",
                start = date(2010, 1, 1),
                cerfa_field = u'7TE'))

build_column('f7tu', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TU'))

build_column('f7tt', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TT'))

build_column('f7tv', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TV'))

build_column('f7tx', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TX'))

build_column('f7ty', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TY'))

build_column('f7tw', IntCol(entity = 'foy',
                label = u"Dépenses de travaux dans l'habitation principale",
                val_type = "monetary",
                start = date(2012, 1, 1),
                end = date(2012, 12, 31),
                cerfa_field = u'7TW'))

# Réduction d'impôts sur les investissements locatifs intermédiaires (loi Duflot)

build_column('f7gh', IntCol(entity = 'foy',
                label = u"Investissements locatifs intermédiaires en métropole",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7GH'))

build_column('f7gi', IntCol(entity = 'foy',
                label = u"Investissements locatifs intermédiaires outre-mer",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'7GI'))


# section 8

build_column('f8tc', IntCol(entity = 'foy',
                label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))",  # différence de label entre les années à voir
                val_type = "monetary",
                end = date(2008, 12, 31),
                cerfa_field = u'8TC'))

build_column('f8tb', IntCol(entity = 'foy',
                label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)",  # TODO: différence de label entre les années à voir
                val_type = "monetary",
                cerfa_field = u'8TB'))

build_column('f8te', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé",
                val_type = "monetary",
                cerfa_field = u'8TE'))

build_column('f8tf', IntCol(entity = 'foy',
                label = u"Reprises de réductions ou de crédits d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TF'))

build_column('f8tg', IntCol(entity = 'foy',
                label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse",
                val_type = "monetary",
                cerfa_field = u'8TG'))

build_column('f8tl', IntCol(entity = 'foy',
                label = u"Crédit d'impôt compétitivité emploi (CICE), entreprises bénéficiant de la restitution immédiate",
                val_type = "monetary",
                cerfa_field = u'8TL'))

build_column('f8to', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures",
                val_type = "monetary",
                cerfa_field = u'8TO'))

build_column('f8tp', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TP'))

build_column('f8ts', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, crédit d'impôt",
                val_type = "monetary",
                start = date(2012, 1, 1),
                cerfa_field = u'8TS'))

build_column('f8uz', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Famille",
                val_type = "monetary",
                cerfa_field = u'8UZ'))

build_column('f8uw', IntCol(entity = 'foy',
                label = u"Crédit d'impôt compétitivité emploi (CICE), autres entreprises",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'8UW'))

build_column('f8tz', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Apprentissage",
                val_type = "monetary",
                cerfa_field = u'8TZ'))

build_column('f8wa', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique",
                val_type = "monetary",
                cerfa_field = u'8WA'))

build_column('f8wb', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale",
                val_type = "monetary",
                cerfa_field = u'8WB'))

build_column('f8wc__2008', IntCol(entity = 'foy',
                 label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies",
                 val_type = "monetary",
                 cerfa_field = u'8WC',
                 end = date(2008, 12, 31)))

build_column('f8wc', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Prêts sans intérêt",
                val_type = "monetary",
                cerfa_field = u'8WC',
                start = date(2012, 1, 1)))

build_column('f8wd', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'8WD'))

build_column('f8we', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Intéressement",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'8WE'))

build_column('f8wr', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'8WR'))

build_column('f8ws', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes",
                val_type = "monetary",
                cerfa_field = u'8WS',
                start = date(2006, 1, 1),
                end = date(2009, 12, 31)))  # verif<=2012

build_column('f8wt', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'8WT'))

build_column('f8wu', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'8WU'))

build_column('f8wv', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac",
                val_type = "monetary",
                cerfa_field = u'8WV',
                start = date(2007, 1, 1),
                end = date(2012, 12, 31)))  # verif<=2012

build_column('f8wx', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise",
                val_type = "monetary",
                cerfa_field = u'8WX',
                start = date(2007, 1, 1),
                end = date(2009, 12, 31)))  # verif<=2012

build_column('elig_creimp_exc_2008', IntCol(entity = 'foy', #TODO: coder http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf B.12
                default = 1,
                label = u"Éligibilité au crédit d'impôt exceptionnel sur les revenus 2008",
                val_type = 'monetary',
                start = date(2008, 1, 1),
                end = date(2008, 12, 31)))

build_column('elig_creimp_jeunes', BoolCol(entity = "ind", label = u"Éligible au crédit d'impôt jeunes",
                    start = date(2005, 1, 1),
                    end = date(2008, 1, 1))) #Sert à savoir si son secteur d'activité permet au jeune de bénéficier du crédit impôts jeunes
