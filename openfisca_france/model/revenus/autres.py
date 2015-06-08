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


from ..base import *  # noqa analysis:ignore


build_column('pensions_alimentaires_percues', FloatCol(entity = 'ind', label = u"Pensions alimentaires perçues",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AO",
                              QUIFOY['conj']: u"1BO",
                              QUIFOY['pac1']: u"1CO",
                              QUIFOY['pac2']: u"1DO",
                              QUIFOY['pac3']: u"1EO",
                              }))  # (f1ao, f1bo, f1co, f1do, f1eo)
build_column('pensions_alimentaires_percues_decl', BoolCol(label = u"Pension déclarée", default = True))

build_column('pensions_alimentaires_versees_individu', FloatCol(entity = 'ind', label = u"Pensions alimentaires versées pour un individu"))

build_column('gains_exceptionnels', FloatCol(entity = 'ind', label = u"Gains exceptionnels"))

build_column('allocation_aide_retour_emploi', FloatCol(entity = 'ind', label = u"Allocation d'aide au retour à l'emploi"))
build_column('allocation_securisation_professionnelle', FloatCol(entity = 'ind', label = u"Allocation de sécurisation professionnelle"))
build_column('prime_forfaitaire_mensuelle_reprise_activite', FloatCol(entity = 'ind', label = u"Prime forfaitaire mensuelle pour la reprise d'activité"))
build_column('indemnites_volontariat', FloatCol(entity = 'ind', label = u"Indemnités de volontariat"))
build_column('dedommagement_victime_amiante', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante"))
build_column('prestation_compensatoire', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante"))
build_column('pensions_invalidite', FloatCol(entity = 'ind', label = u"Pensions d'invalidité"))
build_column('bourse_enseignement_sup', FloatCol(entity = 'ind', label = u"Bourse de l'enseignement supérieur"))


# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
build_column('f8ta', IntCol(entity = 'foy',
                label = u"Retenue à la source en France ou impôt payé à l'étranger",
                val_type = "monetary",
                cerfa_field = u'8TA'))


build_column('f8th', IntCol(entity = 'foy',
                label = u"Retenue à la source élus locaux",
                val_type = "monetary",
                cerfa_field = u'8TH'))


build_column('f8td_2002_2005', IntCol(entity = 'foy',
                start = date(2002, 1, 1),
                end = date(2005, 12, 31),
                label = u"Contribution exceptionnelle sur les hauts revenus",
                cerfa_field = u'8TD'))

build_column('f8td', BoolCol(entity = 'foy',
                start = date(2011, 1, 1),  # 2011 ou 2013 ?
                end = date(2014, 12, 31),
                label = u"Revenus non imposables dépassent la moitié du RFR",
                cerfa_field = u'8TD'))


build_column('f8ti', IntCol(entity = 'foy',
                label = u"Revenus de l'étranger exonérés d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TK'))

build_column('f8tk', IntCol(entity = 'foy',
                label = u"Revenus de l'étranger imposables",
                val_type = "monetary",
                cerfa_field = u'8TK'))

# Auto-entrepreneur : versements libératoires d’impôt sur le revenu
build_column('f8uy', IntCol(entity = 'foy',
                label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'8UY'))
