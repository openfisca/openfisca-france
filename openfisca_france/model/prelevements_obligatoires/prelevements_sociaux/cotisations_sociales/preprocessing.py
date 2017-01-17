# -*- coding: utf-8 -*-

from __future__ import division

import collections
import copy
import logging


from openfisca_france.model.base import *  # noqa


DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(node_json):
    """Construit le dictionnaire de barèmes des cotisations employeur à partir de node_json['children']['cotsoc'][
        'children']['pat']"""
    pat = copy.deepcopy(node_json['children']['cotsoc']['children']['pat'])
    commun = pat['children'].pop('commun')

    for bareme in ['apprentissage', 'apprentissage_add', 'apprentissage_alsace_moselle']:
        commun['children'][bareme] = commun['children']['apprentissage_node']['children'][bareme]
    del commun['children']['apprentissage_node']

    commun['children']['formprof_09'] = commun['children']['formprof_node']['children']['formprof_09']
    commun['children']['formprof_1019'] = commun['children']['formprof_node']['children']['formprof_1019']
    commun['children']['formprof_20'] = commun['children']['formprof_node']['children']['formprof_20']
    del commun['children']['formprof_node']

    commun['children']['construction'] = commun['children']['construction_node']['children']['construction_20']
    del commun['children']['construction_node']

    pat['children']['noncadre']['children'].update(commun['children'])
    pat['children']['cadre']['children'].update(commun['children'])
    pat['children']['fonc']['children']['contract']['children'].update(commun['children'])

    # Renaming
    pat['children']['prive_non_cadre'] = pat['children'].pop('noncadre')
    pat['children']['prive_cadre'] = pat['children'].pop('cadre')

    # Rework commun to deal with public employees
    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "assedic", "chomfg", "construction", "maladie", "formprof_09",
                "formprof_1019", "formprof_20", "vieillesse_deplafonnee", "vieillesse_plafonnee"]:
        del commun['children'][var]

    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "formprof_09", "formprof_1019", "formprof_20", "chomfg",
                "construction", "assedic"]:
        del pat['children']['fonc']['children']['contract']['children'][var]

    pat['children']['fonc']['children']['etat']['children'].update(commun['children'])
    pat['children']['fonc']['children']['colloc']['children'].update(commun['children'])

    pat['children']['etat_t'] = pat['children']['fonc']['children']['etat']
    pat['children']['colloc_t'] = pat['children']['fonc']['children']['colloc']
    pat['children']['contract'] = pat['children']['fonc']['children']['contract']

    for var in ['etat', 'colloc', 'contract']:
        del pat['children']['fonc']['children'][var]

    # Renaming
    pat['children']['public_titulaire_etat'] = pat['children'].pop('etat_t')
    # del pat['children']['public_titulaire_etat']['children']['rafp']

    pat['children']['public_titulaire_territoriale'] = pat['children'].pop('colloc_t')

    pat['children']['public_titulaire_hospitaliere'] = copy.deepcopy(pat['children']['public_titulaire_territoriale'])
    for category in ['territoriale', 'hospitaliere']:
        for name, bareme in pat['children']['public_titulaire_' + category]['children'][category]['children'].iteritems(
                ):
            pat['children']['public_titulaire_{}'.format(category)]['children'][name] = bareme

    for category in ['territoriale', 'hospitaliere']:
        del pat['children']['public_titulaire_territoriale']['children'][category]
        del pat['children']['public_titulaire_hospitaliere']['children'][category]

    pat['children']['public_non_titulaire'] = pat['children'].pop('contract')

    return pat


def build_sal(node_json):
    '''
    à partir des informations contenues dans node_json['children']['cotsoc']['children']['sal']
    Construit le dictionnaire de barèmes des cotisations salariales
    '''
    sal = copy.deepcopy(node_json['children']['cotsoc']['children']['sal'])
    sal['children']['noncadre']['children'].update(sal['children']['commun']['children'])
    sal['children']['cadre']['children'].update(sal['children']['commun']['children'])

    # Renaming
    sal['children']['prive_non_cadre'] = sal['children'].pop('noncadre')
    sal['children']['prive_cadre'] = sal['children'].pop('cadre')
    sal['children']['public_titulaire_etat'] = sal['children']['fonc']['children']['etat']

    sal['children']['public_titulaire_territoriale'] = sal['children']['fonc']['children']['colloc']
    sal['children']['public_titulaire_hospitaliere'] = sal['children']['fonc']['children']['colloc']
    sal['children']['public_non_titulaire'] = sal['children']['fonc']['children']['contract']

    for type_sal_category in (
            'public_titulaire_etat',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire',
            ):
        sal['children'][type_sal_category]['children']['excep_solidarite'] = sal['children']['fonc']['children'][
            'commun']['children']['solidarite']

    sal['children']['public_non_titulaire']['children'].update(sal['children']['commun']['children'])
    del sal['children']['public_non_titulaire']['children']['assedic']

    # Cleaning
    del sal['children']['commun']
    del sal['children']['fonc']['children']['etat']
    del sal['children']['fonc']['children']['colloc']
    del sal['children']['fonc']['children']['contract']

    return sal


def preprocess_legislation(legislation_json):
    '''
    Preprocess the legislation parameters to build the cotisations sociales taxscales (barèmes)
    '''
    sal = build_sal(legislation_json)
    pat = build_pat(legislation_json)

    cotsoc = legislation_json["children"]["cotsoc"]
    cotsoc["children"]["cotisations_employeur"] = collections.OrderedDict((
        (u'@type', u'Node'),
        (u'children', collections.OrderedDict()),
        ))
    cotsoc["children"]["cotisations_salarie"] = collections.OrderedDict((
        (u'@type', u'Node'),
        (u'children', collections.OrderedDict()),
        ))

    for cotisation_name, baremes in (
            ('cotisations_employeur', pat['children']),
            ('cotisations_salarie', sal['children']),
            ):
        for category, bareme in baremes.iteritems():
            if category in CATEGORIE_SALARIE._nums:
                cotsoc['children'][cotisation_name]['children'][category] = bareme

    return legislation_json
