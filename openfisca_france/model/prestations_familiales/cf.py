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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (round, floor, maximum as max_, minimum as min_, logical_not as not_, logical_and as and_, logical_or as or_)

from ..base import *
from ..pfam import nb_enf


@reference_formula
class cf_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial avant d'éventuels cumuls"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(self, age_holder, br_pf, isol, biact, smic55_holder, P =  law.fam):
        """
        Complément familial
        Vous avez au moins 3 enfants à charge tous âgés de plus de 3 ans.
        Vos ressources ne dépassent pas certaines limites.
        Vous avez peut-être droit au Complément Familial à partir du mois
        suivant les 3 ans du 3ème, 4ème, etc. enfant.

        # TODO:
        # En théorie, il faut comparer les revenus de l'année n-2 à la bmaf de
        # l'année n-2 pour déterminer l'éligibilité avec le cf_seuil. Il faudrait
        # pouvoir déflater les revenus de l'année courante pour en tenir compte.
        """
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        bmaf = P.af.bmaf
        bmaf2 = P.af.bmaf_n_2
        cf_nbenf = nb_enf(age, smic55, P.cf.age1, P.cf.age2)

        cf_base_n_2 = P.cf.tx * bmaf2
        cf_base = P.cf.tx * bmaf

        cf_plaf_tx = 1 + P.cf.plaf_tx1 * min_(cf_nbenf, 2) + P.cf.plaf_tx2 * max_(cf_nbenf - 2, 0)
        cf_majo = isol | biact
        cf_plaf = P.cf.plaf * cf_plaf_tx + P.cf.plaf_maj * cf_majo
        cf_plaf2 = cf_plaf + 12 * cf_base_n_2

        cf = (cf_nbenf >= 3) * ((br_pf <= cf_plaf) * cf_base +
                                 (br_pf > cf_plaf) * max_(cf_plaf2 - br_pf, 0) / 12.0)
        return 12 * cf

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(self, paje_base_temp, apje_temp, ape_temp, cf_temp):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        cf_brut = (paje_base_temp < cf_temp) * (apje_temp <= cf_temp) * (ape_temp <= cf_temp) * cf_temp
        return round(cf_brut, 2)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
