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

from numpy import (maximum as max_, logical_not as not_, logical_or as or_)
from openfisca_core.accessors import law

from ..input_variables.base import QUIFAM, QUIFOY

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


def _chomeur(choi, activite):
  '''
  Indicatrice de chômage
  '''
  return or_(choi > 0, activite == 1)

def _ass_elig_i(chomeur):
  '''
  Éligibilité individuelle à l'ASS
  '''
  return chomeur

def _ass(self, br_pf, ass_elig_i_holder, concub, ass_params = law.minim.ass):
    '''
    Allocation de solidarité spécifique

    L’Allocation de Solidarité Spécifique (ASS) est une allocation versée aux
    personnes ayant épuisé leurs droits à bénéficier de l'assurance chômage.

    Le prétendant doit avoir épuisé ses droits à l’assurance chômage.
    Il doit être inscrit comme demandeur d’emploi et justifier de recherches actives.
    Il doit être apte à travailler.
    Il doit justifier de 5 ans d’activité salariée au cours des 10 ans précédant le chômage.
    À partir de 60 ans, il doit répondre à des conditions particulières.
     TODO majo ass et base ressource

    Les ressources prises en compte pour apprécier ces plafonds, comprennent l'allocation de solidarité elle-même ainsi que les autres ressources de l'intéressé, et de son conjoint, partenaire pacsé ou concubin, soumises à impôt sur le revenu.
    Ne sont pas prises en compte, pour déterminer le droit à ASS :
      l'allocation d'assurance chômage précédemment perçue,
      les prestations familiales,
      l'allocation de logement,
      la majoration de l'ASS,
      la prime forfaitaire mensuelle de retour à l'emploi,
      la pension alimentaire ou la prestation compensatoire due par l'intéressé.


    Conditions de versement de l'ASS majorée
        Pour les allocataires admis au bénéfice de l'ASS majorée ( avant le 1er janvier 2004) , le montant de l'ASS majorée est fixé à 22,07 € par jour.
        Pour mémoire, jusqu'au 31 décembre 2003, pouvaient bénéficier de l'ASS majorée, les allocataires :
        âgés de 55 ans ou plus et justifiant d'au moins 20 ans d'activité salariée,
        ou âgés de 57 ans et demi ou plus et justifiant de 10 ans d'activité salariée,
        ou justifiant d'au moins 160 trimestres de cotisation retraite.
    '''
    ass_elig_i = self.split_by_roles(ass_elig_i_holder, roles = [CHEF, PART])

    majo = 0
    cond_act_prec_suff = True # Transformer en variable d'entrée
    elig = or_(ass_elig_i[CHEF], ass_elig_i[PART])
    plafond_mensuel = ass_params.plaf_seul * not_(concub) + ass_params.plaf_coup * concub
    plafond = plafond_mensuel * 12
    montant_mensuel = 30 * (ass_params.montant_plein * not_(majo) + majo * ass_params.montant_maj)
    revenus = br_pf + 12 * montant_mensuel  # TODO check base ressources
    ass = elig * (12 * montant_mensuel * (revenus <= plafond)
              + (revenus > plafond) * max_(plafond + 12 * montant_mensuel - revenus, 0))

    return ass  # annualisé