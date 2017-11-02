# -*- coding: utf-8 -*-

from enum import Enum
from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage


class TypesStatutOccupationLogement(Enum):
    non_renseigne = u"Non renseigné"
    primo_accedant = u"Accédant à la propriété"
    proprietaire = u"Propriétaire (non accédant) du logement"
    locataire_hlm = u"Locataire d'un logement HLM"
    locataire_vide = u"Locataire ou sous-locataire d'un logement loué vide non-HLM"
    locataire_meuble = u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel"
    loge_gratuitement = u"Logé gratuitement par des parents, des amis ou l'employeur"
    locataire_foyer = u"Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)"
    sans_domicile = u"Sans domicile stable"


class TypeTailleEntreprise(Enum):
    non_pertinent = u"Non pertinent"
    moins_de_10 = u"Moins de 10 salariés"
    de_10_a_19 = u"De 10 à 19 salariés"
    de_20_a_249 = u"De 20 à 249 salariés"
    plus_de_250 = u"Plus de 250 salariés"


class TypesZoneApl(Enum) :
    non_renseigne = u"Non renseigné"
    zone_1 = u"Zone 1"
    zone_2 = u"Zone 2"
    zone_3 = u"Zone 3"


class TypesCategorieSalarie(Enum):
    prive_non_cadre = u'prive_non_cadre'
    prive_cadre = u'prive_cadre'
    public_titulaire_etat = u'public_titulaire_etat'
    public_titulaire_militaire = u'public_titulaire_militaire'
    public_titulaire_territoriale = u'public_titulaire_territoriale'
    public_titulaire_hospitaliere = u'public_titulaire_hospitaliere'
    public_non_titulaire = u'public_non_titulaire'
    non_pertinent = u'non_pertinent'


class TypesActivite(Enum):
    actif = u'Actif occupé'
    chomeur = u'Chômeur'
    etudiant = u'Étudiant, élève'
    retraite = u'Retraité'
    inactif = u'Autre, inactif'


class TypesStatutMarital(Enum):
    non_renseigne = u'Non renseigné'
    marie = u'Marié'
    celibataire = u'Celibataire'
    divorce = u'Divorcé'
    veuf = u'Veuf'
    pacse = u'Pacsé'
    jeune_veuf = u'Jeune veuf'


class TypesContratDeTravail(Enum):
    temps_plein = u"temps_plein"
    temps_partiel = u"temps_partiel"
    forfait_heures_semaines = u"forfait_heures_semaines"
    forfait_heures_mois = u"forfait_heures_mois"
    forfait_heures_annee = u"forfait_heures_annee"
    forfait_jours_annee = u"forfait_jours_annee"
    sans_objet = u"sans_objet"


class CATEGORIE_SALARIE(Enum):
    prive_non_cadre = u'prive_non_cadre',
    prive_cadre = u'prive_cadre',
    public_titulaire_etat = u'public_titulaire_etat',
    public_titulaire_militaire = u'public_titulaire_militaire',
    public_titulaire_territoriale = u'public_titulaire_territoriale',
    public_titulaire_hospitaliere = u'public_titulaire_hospitaliere',
    public_non_titulaire = u'public_non_titulaire',
    non_pertinent = u'non_pertinent',


class enum_tns_type_activite(Enum):
    achat_revente = u'achat_revente'
    bic = u'bic'
    bnc = u'bnc'


class TypesRSANonCalculable(Enum):
    non_renseigne = u"Non Renseigne"
    tns = u"tns"
    conjoint_tns = u"conjoint_tns"


class TypesAAHNonCalculable(Enum):
    non_renseigne = u"Non renseigné"
    intervention_CDAPH_necessaire = u"intervention_CDAPH_necessaire"


class TypeAideLogementNonCalculable(Enum):
    non_renseigne = u"Non renseigné"
    primo_accedant = u"Primo accedant"
    locataire_foyer = u"Locataire foyer"


class TypeTauxCSGRemplacement(Enum):
    non_renseigne = u"Non renseigné/non pertinent"
    exonere = u"Exonéré"
    taux_reduit = u"Taux réduit"
    taux_plein = u"Taux plein"


class TypesExpositionAccident(Enum):
    faible = u"Faible"
    moyen = u"Moyen"
    eleve = u"Élevé"
    tres_eleve = u"Très élevé"


class TypesExpositionPenibilite(Enum):
    nulle = u"Nulle, pas d'exposition de l'employé à un facteur de pénibilité"
    simple = u"Simple, exposition à un seul facteur de pénibilité"
    multiple = u"Multiple, exposition à plusieurs facteurs de pénibilité"


class TypesAllegementFillonModeRecouvrement(Enum):
    fin_d_annee = u"fin_d_annee"
    anticipe = u"anticipe_regularisation_fin_de_periode"
    progressif = u"progressif"


class TypesAllegementCotisationAllocationsFamilialesModeRecouvrement(Enum):
    fin_d_annee = u"fin_d_annee"
    anticipe = u"anticipe_regularisation_fin_de_periode"
    progressif = u"progressif"


class TypesEligibiliteANAH(Enum):
    a_verifier = u"A vérifier"
    modestes = u"Modestes"
    tres_modeste = u"Très modestes"


class TypesGir(Enum):
    non_defini = u"Non défini"
    gir_1 = u"Gir 1"
    gir_2 = u"Gir 2"
    gir_3 = u"Gir 3"
    gir_4 = u"Gir 4"
    gir_5 = u"Gir 5"
    gir_6 = u"Gir 6"


class TypesScolarite(Enum):
    inconnue = u"Inconnue"
    college = u"Collège"
    lycee = u"Lycée"


class TypesCotisationSocialeModeRecouvrement(Enum):
    mensuel = u"Mensuel avec régularisation en fin d'année"
    annuel = u"Annuel"


class TypesContratDeTravailDuree(Enum):
    cdi = u"CDI"
    cdd = u"CDD"

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
