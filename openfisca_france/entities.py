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
    doc = u'''
    Le foyer fiscal désigne l'ensemble des personnes inscrites sur une même déclaration de revenus.
    Il peut y avoir plusieurs foyers fiscaux dans un seul ménage : par exemple, un couple non marié où chacun remplit
    sa propre déclaration de revenus compte pour deux foyers fiscaux.
    Voir https://www.insee.fr/fr/metadonnees/definition/c1735.
    ''',
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
    doc = u'''
    Un ménage, au sens statistique du terme, désigne l'ensemble des occupants d'un même logement sans que ces personnes
    soient nécessairement unies par des liens de parenté (en cas de cohabitation, par exemple).
    Un ménage peut être composé d'une seule personne.
    Le niveau de vie ainsi que la pauvreté sont calculés au niveau d'un ménage.
    Voir https://www.insee.fr/fr/metadonnees/definition/c1879.
    ''',
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
