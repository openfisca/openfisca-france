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


from __future__ import division

import logging

from numpy import (logical_not as not_, logical_or as or_, maximum as max_, minimum as min_,
                   zeros)

from openfisca_core.taxscales import scale_tax_scales
from openfisca_core.enumerations import Enum

from ..input_variables.base import QUIFAM, QUIFOY, QUIMEN


log = logging.getLogger(__name__)

CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])


CHEF = QUIFAM['chef']
DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'

PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


def _alleg_plfrss2014_prive(salbrut, sal_h_b, type_sal, taille_entreprise, _P):
    '''
    Allègement de cotisations salariées sur les bas et moyens salaires du secteur privé
    '''
    if _P.datesim.year >= 2015:  # TODO: fix this
        taux = taux_alleg_plfrss2014_prive(sal_h_b, taille_entreprise, _P)
        allegement = (taux * salbrut * (
            (type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre']))
            )
        return allegement
    else:
        return 0 * salbrut


def _alleg_plfrss2014_public(salbrut, type_sal, _P):
    '''
    Allègement de cotisations salariées sur les bas et moyens salaires du secteur public
    '''
    if _P.datesim.year >= 2015:  # TODO: fix this
        taux = taux_exo_alleg_plfrss2014_prive(sal_h_b, _P)
        allegement = (taux * salbrut * (
            (type_sal == CAT['public_titulaire_etat'])
            | (type_sal == CAT['public_titulaire_militaire'])
            | (type_sal == CAT['public_titulaire_territoriale',])
            | (type_sal == CAT['public_non_titulaire',])  # TODO: check this category
            )
        return allegement
    else:
        return 0 * salbrut



############################################################################
# # Helper functions
############################################################################

def alleg_plfrss2014_prive(sal_h_b, taille_entreprise, P):
    '''
    Exonération de cotisations des salariés du secteur privé PLFRSS2014
    http://www.assemblee-nationale.fr/14/projets/pl2044-ei.asp#P139_9932
    '''
    # La divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    smic_h_b = P.gen.smic_h_b
    seuil = P.plfrss2014.exonerations_bas_salaires.prive.seuil
    taux =  P.plfrss2014.exonerations_bas_salaires.prive.taux
    if seuil <= 1:
        return 0
    return (taux * min_(1, max_(seuil * smic_h_b / (sal_h_b + 1e-10) - 1, 0)
                          / (seuil - 1)))


def alleg_plfrss2014_public(salbrut, P):
    '''
    Exonération cotisations des salariés du secteur public PLFRSS2014
    http://www.assemblee-nationale.fr/14/projets/pl2044-ei.asp#P139_9932
    '''
    parametres = P.plfrss2014.exonerations_bas_salaires.public
    alleg = (parametres.taux_1 * (salbrut <= parametres.seuil_1)
        + parametres.taux_2 * ( parametres.seuil_1 < salbrut <= parametres.seuil_2)
    + parametres.taux_10 * ( parametres.seuil_2 < salbrut <= parametres.seuil_3)
    + parametres.taux_10 * ( parametres.seuil_3 < salbrut <= parametres.seuil_4)
    + parametres.taux_10 * ( parametres.seuil_4 < salbrut <= parametres.seuil_5)
    + parametres.taux_10 * ( parametres.seuil_5 < salbrut <= parametres.seuil_6)
    + parametres.taux_10 * ( parametres.seuil_6 < salbrut <= parametres.seuil_7)
    + parametres.taux_10 * ( parametres.seuil_7 < salbrut <= parametres.seuil_8)
    + parametres.taux_10 * ( parametres.seuil_8 < salbrut <= parametres.seuil_9)
    + parametres.taux_10 * ( parametres.seuil_9 < salbrut <= parametres.seuil_10)
    + parametres.taux_11 * (parametres.seuil_10 < salbrut <= parametres.seuil_11)


def reduction_impot_execptionnelle(rfr, nb_adult, nb_part, _P)
    parametres = _P.plfr2014.reduction_impot_exceptionnelle
    plafond = parametres.seuil * nb_adult + (nb_part - nb_adult) * 2 * parametres.majoration_seuil
    montant = parametres.montant_plafond * nb_adult
    reduction = min_(max_(plafond + montant - rfr , 0), montant)
