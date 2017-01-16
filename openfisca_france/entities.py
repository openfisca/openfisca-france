# -*- coding: utf-8 -*-

from openfisca_core.entities import build_entity

Famille = build_entity(
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

Individu = build_entity(
    key = "individu",
    plural = "individus",
    label = u'Individu',
    is_person = True
    )

FoyerFiscal = build_entity(
    key = "foyer_fiscal",
    plural = "foyers_fiscaux",
    label = u'Déclaration d’impôts',
    roles = [
        {
            'key': 'declarant',
            'plural': 'declarants',
            'label': u'Déclarants',
            'subroles': ['declarant_principal', 'conjoint'],
            },
        {
            'key': 'personne_a_charge',
            'plural': 'personnes_a_charge',
            'label': u'Personnes à charge'
            },
        ]
    )

Menage = build_entity(
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
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': u'Autres'
            }
        ]
    )

entities = [Individu, Famille, FoyerFiscal, Menage]
