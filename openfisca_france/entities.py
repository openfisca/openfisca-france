from openfisca_core.entities import build_entity

Famille = build_entity(
    key = 'famille',
    plural = 'familles',
    label = 'Famille',
    roles = [
        {
            'key': 'parent',
            'plural': 'parents',
            'label': 'Parents',
            'subroles': ['demandeur', 'conjoint']
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': 'Enfants'
            }
        ]
    )

Individu = build_entity(
    key = 'individu',
    plural = 'individus',
    label = 'Individu',
    is_person = True
    )

FoyerFiscal = build_entity(
    key = 'foyer_fiscal',
    plural = 'foyers_fiscaux',
    label = 'Déclaration d’impôts',
    doc = '''
    Le foyer fiscal désigne l'ensemble des personnes inscrites sur une même déclaration de revenus.
    Il peut y avoir plusieurs foyers fiscaux dans un seul ménage : par exemple, un couple non marié où chacun remplit
    sa propre déclaration de revenus compte pour deux foyers fiscaux.
    Voir https://www.insee.fr/fr/metadonnees/definition/c1735.
    ''',
    roles = [
        {
            'key': 'declarant',
            'plural': 'declarants',
            'label': 'Déclarants',
            'subroles': ['declarant_principal', 'conjoint'],
            },
        {
            'key': 'personne_a_charge',
            'plural': 'personnes_a_charge',
            'label': 'Personnes à charge'
            },
        ]
    )

Menage = build_entity(
    key = 'menage',
    plural = 'menages',
    label = 'Logement principal',
    doc = '''
    Un ménage, au sens statistique du terme, désigne l'ensemble des occupants d'un même logement sans que ces personnes
    soient nécessairement unies par des liens de parenté (en cas de cohabitation, par exemple).
    Un ménage peut être composé d'une seule personne.
    Le niveau de vie ainsi que la pauvreté sont calculés au niveau d'un ménage.
    Voir https://www.insee.fr/fr/metadonnees/definition/c1879.
    ''',
    roles = [
        {
            'key': 'personne_de_reference',
            'label': 'Personne de référence',
            'max': 1
            },
        {
            'key': 'conjoint',
            'label': 'Conjoint',
            'max': 1
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': 'Enfants',
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': 'Autres'
            }
        ]
    )

entities = [Individu, Famille, FoyerFiscal, Menage]
