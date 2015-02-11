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


from __future__ import division


from functools import partial
import logging
from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, maximum as max_,
    minimum as min_, timedelta64
    )


from ..base import *  # noqa


log = logging.getLogger(__name__)


@reference_formula
class remuneration_principale(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Rémunération principale des agents titulaires de la fonction publique"

    def function(self, simulation, period):
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = simulation.calculate('nouvelle_bonification_indiciaire', period)
        type_sal = simulation.calculate('type_sal', period)
        return period, (
            (type_sal >= 2) * (type_sal <= 5) * (
                traitement_indiciaire_brut + nouvelle_bonification_indiciaire
                )
            )


@reference_formula
class assiette_cotisations_sociales_public(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des agents titulaires de la fonction publique"
    # TODO: gestion des heures supplémentaires

    def function(self, simulation, period):
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        type_sal = simulation.calculate('type_sal', period)
        public = (type_sal >= 2)
        titulaire = (type_sal >= 2) * (type_sal <= 5)
        assiette = public * (
            remuneration_principale
#        + not_(titulaire) * (
#                indemnite_residence + primes_fonction_publique
#                )
            )
        return period, assiette


# sft dans assiette csg et RAFP et Cotisation exceptionnelle de solidarité et taxe sur les salaires

# primes dont indemnites de residences idem sft

# avantages en nature contrib exceptionnelle de solidarite, RAFP, CSG, CRDS.