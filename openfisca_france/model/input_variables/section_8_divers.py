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


from ..base import *  # noqa


# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
build_column('f8ta', IntCol(entity = 'foy',
                label = u"Retenue à la source en France ou impôt payé à l'étranger",
                val_type = "monetary",
                cerfa_field = u'8TA'))

build_column('f8tb', IntCol(entity = 'foy',
                label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)",  # TODO: différence de label entre les années à voir
                val_type = "monetary",
                cerfa_field = u'8TB'))

build_column('f8tf', IntCol(entity = 'foy',
                label = u"Reprises de réductions ou de crédits d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TF'))

build_column('f8tg', IntCol(entity = 'foy',
                label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse",
                val_type = "monetary",
                cerfa_field = u'8TG'))

build_column('f8th', IntCol(entity = 'foy',
                label = u"Retenue à la source élus locaux",
                val_type = "monetary",
                cerfa_field = u'8TH'))

build_column('f8tc', IntCol(entity = 'foy',
                label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))",  # différence de label entre les années à voir
                val_type = "monetary",
                end = date(2008, 12, 31),
                cerfa_field = u'8TC'))

build_column('f8td_2002_2005', IntCol(entity = 'foy',
                start = date(2002, 1, 1),
                end = date(2005, 12, 31),
                label = u"Contribution exceptionnelle sur les hauts revenus",
                cerfa_field = u'8TD'))

build_column('f8td', BoolCol(entity = 'foy',
                start = date(2011, 1, 1), # 2011 ou 2013 ?
                end = date(2014, 12, 31),
                label = u"Revenus non imposables dépassent la moitié du RFR",
                cerfa_field = u'8TD'))

build_column('f8te', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé",
                val_type = "monetary",
                cerfa_field = u'8TE'))

build_column('f8ti', IntCol(entity = 'foy',
                label = u"Revenus de l'étranger exonérés d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TK'))

build_column('f8tk', IntCol(entity = 'foy',
                label = u"Revenus de l'étranger imposables",
                val_type = "monetary",
                cerfa_field = u'8TK'))

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
# Auto-entrepreneur : versements libératoires d’impôt sur le revenu
build_column('f8uy', IntCol(entity = 'foy',
                label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'8UY'))
