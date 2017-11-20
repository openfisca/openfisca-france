# -*- coding: utf-8 -*-

from enum import Enum
from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage

class CATEGORIE_SALARIE(Enum):
    prive_non_cadre = u'prive_non_cadre',
    prive_cadre = u'prive_cadre',
    public_titulaire_etat = u'public_titulaire_etat',
    public_titulaire_militaire = u'public_titulaire_militaire',
    public_titulaire_territoriale = u'public_titulaire_territoriale',
    public_titulaire_hospitaliere = u'public_titulaire_hospitaliere',
    public_non_titulaire = u'public_non_titulaire',
    non_pertinent = u'non_pertinent',


TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute

# Legacy roles. To be removed when they are not used by formulas anymore.
class QUIFAM(Enum):
    chef = u'chef',
    part = u'part',
    enf1 = u'enf1',
    enf2 = u'enf2',
    enf3 = u'enf3',
    enf4 = u'enf4',
    enf5 = u'enf5',
    enf6 = u'enf6',
    enf7 = u'enf7',
    enf8 = u'enf8',
    enf9 = u'enf9',

class QUIFOY(Enum):
    vous = u'vous',
    conj = u'conj',
    pac1 = u'pac1',
    pac2 = u'pac2',
    pac3 = u'pac3',
    pac4 = u'pac4',
    pac5 = u'pac5',
    pac6 = u'pac6',
    pac7 = u'pac7',
    pac8 = u'pac8',
    pac9 = u'pac9',

class QUIMEN(Enum):
    pref = u'pref',
    cref = u'cref',
    enf1 = u'enf1',
    enf2 = u'enf2',
    enf3 = u'enf3',
    enf4 = u'enf4',
    enf5 = u'enf5',
    enf6 = u'enf6',
    enf7 = u'enf7',
    enf8 = u'enf8',
    enf9 = u'enf9',

CHEF = QUIFAM.chef
CONJ = QUIFOY.conj
CREF = QUIMEN.cref
ENFS = [
    QUIFAM.enf1, QUIFAM.enf2, QUIFAM.enf3, QUIFAM.enf4, QUIFAM.enf5, QUIFAM.enf6, QUIFAM.enf7,
    QUIFAM.enf8, QUIFAM.enf9,
    ]
PAC1 = QUIFOY.pac1
PAC2 = QUIFOY.pac2
PAC3 = QUIFOY.pac3
PART = QUIFAM.part
PREF = QUIMEN.pref
VOUS = QUIFOY.vous
