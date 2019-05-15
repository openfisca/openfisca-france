# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage  # noqa F401

# Enums commonly used through the legislation


class TypesActivite(Enum):
    __order__ = 'actif chomeur etudiant retraite inactif'  # Needed to preserve the enum order in Python 2
    actif = u'Actif occupé'
    chomeur = u'Chômeur'
    etudiant = u'Étudiant, élève'
    retraite = u'Retraité'
    inactif = u'Autre, inactif'


class TypesCategorieNonSalarie(Enum):
    __order__ = 'non_pertinent artisan commercant profession_liberale'  # Needed to preserve the enum order in Python 2
    non_pertinent = u"Non pertinent (l'individu n'est pas un travailleur indépendant)"
    artisan = u'Artisant'
    commercant = u'Commercant'
    profession_liberale = u'Profession libérale'


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


class TypesLieuResidence(Enum):
    non_renseigne = u"Non renseigné"
    metropole = u"Métropole"
    guadeloupe = u"Guadeloupe"
    martinique = u"Martinique"
    guyane = u"Guyane"
    la_reunion = u"La réunion"
    saint_pierre_et_miquelon = u"Saint Pierre et Miquelon"
    mayotte = u"Mayotte"
    saint_bartelemy = u"Saint Bartelemy"
    saint_martin = u"Saint Martin"


# Taux de prime moyen de la fonction publique
TAUX_DE_PRIME = 0.195  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute
