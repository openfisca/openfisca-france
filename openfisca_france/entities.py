# -*- coding: utf-8 -*-

import collections
import itertools

from openfisca_core.entities import build_entity

Familles = build_entity(
    key = "famille",
    plural = "familles",
    label = u'Famille',
    roles = [
        {
            'key': 'parent',
            'plural': 'parents',
            'label': u'Parents',
            'subroles': ['demandeur', 'conjoint']
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': u'Enfants'
            }
        ]
    )

Individus = build_entity(
    key = "individu",
    plural = "individus",
    label = u'Individu',
    is_person = True
    )

FoyersFiscaux = build_entity(
    key = "foyer_fiscal",
    plural = "foyers_fiscaux",
    label = u'Déclaration d’impôts',
    roles = [
        {
            'key': 'declarant',
            'plural': 'declarants',
            'label': u'Déclarants',
            'subroles': ['declarant_principal', 'conjoint']
            },
        {
            'key': 'personne_a_charge',
            'plural': 'personnes_a_charge',
            'label': u'Personnes à charge'
            },
        ]
    )

Menages = build_entity(
    key = "menage",
    plural = "menages",
    label = u'Logement principal',
    roles = [
        {
            'key': 'personne_de_reference',
            'label': u'Personne de référence',
            'max': 1
            },
        {
            'key': 'conjoint',
            'label': u'Conjoint',
            'max': 1
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': u'Enfants',
            'max': 2
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': u'Autres'
            }
        ]
    )

entities = [Individus, Familles, FoyersFiscaux, Menages]
