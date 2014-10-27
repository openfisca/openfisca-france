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


from openfisca_core.columns import FloatCol

from ..base import build_column


build_column('indemnites_journalieres_maternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de maternité"))
build_column('indemnites_journalieres_paternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de paternité"))
build_column('indemnites_journalieres_adoption', FloatCol(entity = 'ind', label = u"Indemnités journalières d'adoption"))
build_column('indemnites_journalieres_maladie', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie"))
build_column('indemnites_journalieres_accident_travail', FloatCol(entity = 'ind', label = u"Indemnités journalières d'accident du travail"))
build_column('indemnites_journalieres_maladie_professionnelle', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie professionnelle"))
build_column('indemnites_chomage_partiel', FloatCol(entity = 'ind', label = u"Indemnités de chômage partiel"))
build_column('allocation_aide_retour_emploi', FloatCol(entity = 'ind', label = u"Allocation d'aide au retour à l'emploi"))
build_column('allocation_securisation_professionnelle', FloatCol(entity = 'ind', label = u"Allocation de sécurisation professionnelle"))
build_column('prime_forfaitaire_mensuelle_reprise_activite', FloatCol(entity = 'ind', label = u"Prime forfaitaire mensuelle pour la reprise d'activité"))
build_column('indemnites_volontariat', FloatCol(entity = 'ind', label = u"Indemnités de volontariat"))
build_column('dedommagement_victime_amiante', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante"))
build_column('prestation_compensatoire', FloatCol(entity = 'ind', label = u"Dédommagement versé aux victimes de l'amiante"))
build_column('aah', FloatCol(entity = 'ind', label = u"Allocation de l'adulte handicapé"))
build_column('caah', FloatCol(entity = 'ind', label = u"Complément de l'allocation de l'adulte handicapé"))
build_column('gains_exceptionnels', FloatCol(entity = 'ind', label = u"Gains exceptionnels"))
build_column('pensions_invalidite', FloatCol(entity = 'ind', label = u"Pensions d'invalidité"))
build_column('bourse_enseignement_sup', FloatCol(entity = 'ind', label = u"Bourse de l'enseignement supérieur"))
build_column('bourse_recherche', FloatCol(entity = 'ind', label = u"Bourse de recherche"))
build_column('retraite_combattant', FloatCol(entity = 'ind', label = u"Retraite du combattant"))
build_column('revenus_stage_formation_pro', FloatCol(entity = 'ind', label = u"Revenus de stage de formation professionnelle"))
