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


build_column('coloc', BoolCol(label = u"Vie en colocation"))

build_column('depcom', FixedStrCol(label = u"Code INSEE (depcom) du lieu de résidence", entity = 'men', max_length = 5))


build_column('logement_chambre', BoolCol(label = u"Le logement est considéré comme une chambre"))

build_column('loyer', IntCol(label = u"Loyer mensuel",
                 entity = 'men',
                 val_type = "monetary"))  # Loyer mensuel

build_column(
    'proprietaire_proche_famille',
    BoolCol(
        entity = "fam",
        label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint",
        ),
    )

build_column('statut_occupation', EnumCol(label = u"Statut d'occupation",
               entity = 'men',
               enum = Enum([u"Non renseigné",
                            u"Accédant à la propriété",
                            u"Propriétaire (non accédant) du logement",
                            u"Locataire d'un logement HLM",
                            u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                            u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                            u"Logé gratuitement par des parents, des amis ou l'employeur"])))

