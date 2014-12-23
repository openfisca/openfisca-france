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

import copy
import logging


from openfisca_core.taxscales import TaxScalesTree  #, scale_tax_scales
from openfisca_core.legislations import CompactNode

from ..base import *  # noqa


DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(_P):
    """Construit le dictionnaire de barèmes des cotisations patronales à partir de _P.cotsoc.pat"""
    pat = TaxScalesTree('pat', _P.cotsoc.pat)

    for bareme in ['apprentissage', 'apprentissage_add']:
        pat['commun'][bareme] = pat['commun']['apprentissage_node'][bareme]
    del pat['commun']['apprentissage_node']

    pat['commun']['formprof_09'] = pat['commun']['formprof_node']['formprof_09']
    pat['commun']['formprof_1019'] = pat['commun']['formprof_node']['formprof_1019']
    pat['commun']['formprof_20'] = pat['commun']['formprof_node']['formprof_20']
    del pat['commun']['formprof_node']

    pat['commun']['construction'] = pat['commun']['construction_node']['construction_20']
    del pat['commun']['construction_node']

    pat['noncadre'].update(pat['commun'])
    pat['cadre'].update(pat['commun'])
    pat['fonc']['contract'].update(pat['commun'])

    # Renaiming
    pat['prive_non_cadre'] = pat.pop('noncadre')
    pat['prive_cadre'] = pat.pop('cadre')

    # Rework commun to deal with public employees
    for var in ["apprentissage", "apprentissage_add", "assedic", "chomfg", "construction", "maladie", "formprof_09",
                "formprof_1019", "formprof_20", "vieillessedeplaf", "vieillesseplaf"]:
        del pat['commun'][var]

    for var in ["apprentissage", "apprentissage_add", "formprof_09", "formprof_1019", "formprof_20", "chomfg",
                "construction", "assedic"]:
        del pat['fonc']['contract'][var]

    pat['fonc']['etat'].update(pat['commun'])
    pat['fonc']['colloc'].update(pat['commun'])
    del pat['commun']

    pat['etat_t'] = pat['fonc']['etat']
    pat['colloc_t'] = pat['fonc']['colloc']
    pat['contract'] = pat['fonc']['contract']

    for var in ['etat', 'colloc', 'contract']:
        del pat['fonc'][var]

    # Renaming
    pat['public_titulaire_etat'] = pat.pop('etat_t')
    # del pat['public_titulaire_etat']['rafp']

    pat['public_titulaire_territoriale'] = pat.pop('colloc_t')

    pat['public_titulaire_hospitaliere'] = copy.deepcopy(pat['public_titulaire_territoriale'])
    for category in ['territoriale', 'hospitaliere']:
        for name, bareme in pat['public_titulaire_' + category][category].iteritems():
            pat['public_titulaire_{}'.format(category)][name] = bareme

    for category in ['territoriale', 'hospitaliere']:
        del pat['public_titulaire_territoriale'][category]
        del pat['public_titulaire_hospitaliere'][category]

    pat['public_non_titulaire'] = pat.pop('contract')

    return pat


def build_sal(_P):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    à partir des informations contenues dans P.cotsoc.sal
    '''
    sal = TaxScalesTree('sal', _P.cotsoc.sal)
    sal['noncadre'].update(sal['commun'])
    sal['cadre'].update(sal['commun'])

    # Renaiming
    sal['prive_non_cadre'] = sal.pop('noncadre')
    sal['prive_cadre'] = sal.pop('cadre')
    sal['public_titulaire_etat'] = sal['fonc']['etat']

    sal['public_titulaire_territoriale'] = sal['fonc']['colloc']
    sal['public_titulaire_hospitaliere'] = sal['fonc']['colloc']
    sal['public_non_titulaire'] = sal['fonc']['contract']

    for type_sal_category in (
            'public_titulaire_etat',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire',
            ):
        sal[type_sal_category]['excep_solidarite'] = sal['fonc']['commun']['solidarite']

    sal['public_non_titulaire'].update(sal['commun'])
    del sal['public_non_titulaire']['arrco']
    del sal['public_non_titulaire']['assedic']

    # Cleaning
    del sal['commun']
    del sal['fonc']['etat']
    del sal['fonc']['colloc']
    del sal['fonc']['contract']

    return sal


def preprocess_compact_legislation(compact_legislation):
    '''
    Preprocess the legislation parameters to build the cotisations sociales taxscales (barèmes)
    '''
    sal = build_sal(compact_legislation)
    pat = build_pat(compact_legislation)

    compact_legislation.cotsoc.cotisations_employeur = CompactNode()
    compact_legislation.cotsoc.cotisations_salarie = CompactNode()
    cotsoc_dict = compact_legislation.cotsoc.__dict__
    for cotisation_name, bareme_dict in (('cotisations_employeur', pat), ('cotisations_salarie', sal)):
        for category, bareme in bareme_dict.iteritems():
            if category in CAT._nums:
                cotsoc_dict[cotisation_name].__dict__[category] = bareme
