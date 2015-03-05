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


from . import (  # noqa analysis:ignore
    common,
    input_variables,
    pfam,
    travailleurs_non_salaries,
    th,
    )

from .prelevements_obligatoires.cotisations_sociales import (  # noqa analysis:ignore
    allegements,
    capital,
    # penalites,
    remplacement,
    remuneration_prive,
    remuneration_public,
    travail_fonction_publique,
    travail_prive,
    travail_totaux,
    )

from .prelevements_obligatoires.impot_revenu import (  # noqa analysis:ignore
    charges_deductibles,
    credits_impot,
    ir,
    plus_values_immobilieres,
    reductions_impot,
    )

from .prelevements_obligatoires import(  # noqa analysis:ignore
    isf,
    )

from .prestations import (  # noqa analysis:ignore
    aides_logement,
    education,
    )

from prestations.minima_sociaux import (  # noqa analysis:ignore
    # aah,
    asi_aspa,
    ass,
    cmu,
    rsa,
    )

from prestations.prestations_familiales import (  # noqa analysis:ignore
    aeeh,
    af,
    ars,
    asf,
    paje,
    cf,
    )
