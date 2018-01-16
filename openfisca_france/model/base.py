# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage

# Enums commonly used through the legislation

class TypesActivite(Enum):
    __order__ = 'actif chomeur etudiant retraite inactif'  # Needed to preserve the enum order in Python 2
    actif = u'Actif occupé'
    chomeur = u'Chômeur'
    etudiant = u'Étudiant, élève'
    retraite = u'Retraité'
    inactif = u'Autre, inactif'


class TypesCategorieSalarie(Enum):
    __order__ = 'prive_non_cadre prive_cadre public_titulaire_etat public_titulaire_militaire public_titulaire_territoriale public_titulaire_hospitaliere public_non_titulaire non_pertinent'  # Needed to preserve the enum order in Python 2
    prive_non_cadre = u'prive_non_cadre'
    prive_cadre = u'prive_cadre'
    public_titulaire_etat = u'public_titulaire_etat'
    public_titulaire_militaire = u'public_titulaire_militaire'
    public_titulaire_territoriale = u'public_titulaire_territoriale'
    public_titulaire_hospitaliere = u'public_titulaire_hospitaliere'
    public_non_titulaire = u'public_non_titulaire'
    non_pertinent = u'non_pertinent'


class TypesStatutMarital(Enum):
    __order__ = 'non_renseigne marie celibataire divorce veuf pacse jeune_veuf'  # Needed to preserve the enum order in Python 2
    non_renseigne = u'Non renseigné'
    marie = u'Marié'
    celibataire = u'Celibataire'
    divorce = u'Divorcé'
    veuf = u'Veuf'
    pacse = u'Pacsé'
    jeune_veuf = u'Jeune veuf'


class TypesStatutOccupationLogement(Enum):
    __order__ = 'non_renseigne primo_accedant proprietaire locataire_hlm locataire_vide locataire_meuble loge_gratuitement locataire_foyer sans_domicile'  # Needed to preserve the enum order in Python 2
    non_renseigne = u"Non renseigné"
    primo_accedant = u"Accédant à la propriété"
    proprietaire = u"Propriétaire (non accédant) du logement"
    locataire_hlm = u"Locataire d'un logement HLM"
    locataire_vide = u"Locataire ou sous-locataire d'un logement loué vide non-HLM"
    locataire_meuble = u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel"
    loge_gratuitement = u"Logé gratuitement par des parents, des amis ou l'employeur"
    locataire_foyer = u"Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)"
    sans_domicile = u"Sans domicile stable"


TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute

# Legacy roles. To be removed when they are not used by formulas anymore.
class QUIFAM(Enum):
    __order__ = 'chef part enf1 enf2 enf3 enf4 enf5 enf6 enf7 enf8 enf9'  # Needed to preserve the enum order in Python 2
    chef = 0
    part = 1
    enf1 = 2
    enf2 = 3
    enf3 = 4
    enf4 = 5
    enf5 = 6
    enf6 = 7
    enf7 = 8
    enf8 = 9
    enf9 = 10

class QUIFOY(Enum):
    __order__ = 'vous conj pac1 pac2 pac3 pac4 pac5 pac6 pac7 pac8 pac9'  # Needed to preserve the enum order in Python 2
    vous = 0
    conj = 1
    pac1 = 2
    pac2 = 3
    pac3 = 4
    pac4 = 5
    pac5 = 6
    pac6 = 7
    pac7 = 8
    pac8 = 9
    pac9 = 10

class QUIMEN(Enum):
    __order__ = 'pref cref enf1 enf2 enf3 enf4 enf5 enf6 enf7 enf8 enf9'  # Needed to preserve the enum order in Python 2
    pref = 0
    cref = 1
    enf1 = 2
    enf2 = 3
    enf3 = 4
    enf4 = 5
    enf5 = 6
    enf6 = 7
    enf7 = 8
    enf8 = 9
    enf9 = 10

CHEF = QUIFAM.chef.value
CONJ = QUIFOY.conj.value
CREF = QUIMEN.cref.value
ENFS = [
    QUIFAM.enf1.value, QUIFAM.enf2.value, QUIFAM.enf3.value, QUIFAM.enf4.value, QUIFAM.enf5.value, QUIFAM.enf6.value, QUIFAM.enf7.value,
    QUIFAM.enf8.value, QUIFAM.enf9.value,
    ]
PAC1 = QUIFOY.pac1.value
PAC2 = QUIFOY.pac2.value
PAC3 = QUIFOY.pac3.value
PART = QUIFAM.part.value
PREF = QUIMEN.pref.value
VOUS = QUIFOY.vous.value
