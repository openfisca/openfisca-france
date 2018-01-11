# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage

# Enums used through the legislation
# The __order__ is only necessary because of Python 2

class TypesAAHNonCalculable(Enum):
    __order__ = 'calculable intervention_CDAPH_necessaire'
    calculable = u"Calculable"
    intervention_CDAPH_necessaire = u"intervention_CDAPH_necessaire"


class TypesActivite(Enum):
    __order__ = 'actif chomeur etudiant retraite inactif'
    actif = u'Actif occupé'
    chomeur = u'Chômeur'
    etudiant = u'Étudiant, élève'
    retraite = u'Retraité'
    inactif = u'Autre, inactif'


class TypesAideLogementNonCalculable(Enum):
    __order__ = 'calculable locataire_foyer'
    calculable = u"Calculable"
    locataire_foyer = u"Non calculable (Locataire foyer)"

class TypesAllegementCotisationAllocationsFamilialesModeRecouvrement(Enum):
    __order__ = 'fin_d_annee anticipe progressif'
    fin_d_annee = u"fin_d_annee"
    anticipe = u"anticipe_regularisation_fin_de_periode"
    progressif = u"progressif"

# TODO: Merge with the previous one ?
class TypesAllegementFillonModeRecouvrement(Enum):
    __order__ = 'fin_d_annee anticipe progressif'
    fin_d_annee = u"fin_d_annee"
    anticipe = u"anticipe_regularisation_fin_de_periode"
    progressif = u"progressif"


class TypesCategorieSalarie(Enum):
    __order__ = 'prive_non_cadre prive_cadre public_titulaire_etat public_titulaire_militaire public_titulaire_territoriale public_titulaire_hospitaliere public_non_titulaire non_pertinent'
    prive_non_cadre = u'prive_non_cadre'
    prive_cadre = u'prive_cadre'
    public_titulaire_etat = u'public_titulaire_etat'
    public_titulaire_militaire = u'public_titulaire_militaire'
    public_titulaire_territoriale = u'public_titulaire_territoriale'
    public_titulaire_hospitaliere = u'public_titulaire_hospitaliere'
    public_non_titulaire = u'public_non_titulaire'
    non_pertinent = u'non_pertinent'


class TypesContratDeTravail(Enum):
    __order__ = 'temps_plein temps_partiel forfait_heures_semaines forfait_heures_mois forfait_heures_annee forfait_jours_annee sans_objet'
    temps_plein = u"temps_plein"
    temps_partiel = u"temps_partiel"
    forfait_heures_semaines = u"forfait_heures_semaines"
    forfait_heures_mois = u"forfait_heures_mois"
    forfait_heures_annee = u"forfait_heures_annee"
    forfait_jours_annee = u"forfait_jours_annee"
    sans_objet = u"sans_objet"


class TypesContratDeTravailDuree(Enum):
    __order__ = 'cdi cdd'
    cdi = u"CDI"
    cdd = u"CDD"


class TypesTauxCSGRemplacement(Enum):
    __order__ = 'non_renseigne exonere taux_reduit taux_plein'
    non_renseigne = u"Non renseigné/non pertinent"
    exonere = u"Exonéré"
    taux_reduit = u"Taux réduit"
    taux_plein = u"Taux plein"


class TypesCotisationSocialeModeRecouvrement(Enum):
    __order__ = 'mensuel annuel mensuel_strict'
    mensuel = u"Mensuel avec régularisation en fin d'année"
    annuel = u"Annuel"
    mensuel_strict = u"Mensuel strict"


class TypesEligibiliteANAH(Enum):
    __order__ = 'a_verifier modestes tres_modeste'
    a_verifier = u"A vérifier"
    modestes = u"Modestes"
    tres_modeste = u"Très modestes"


class TypesExpositionAccident(Enum):
    __order__ = 'faible moyen eleve tres_eleve'
    faible = u"Faible"
    moyen = u"Moyen"
    eleve = u"Élevé"
    tres_eleve = u"Très élevé"


class TypesExpositionPenibilite(Enum):
    __order__ = 'nulle simple multiple'
    nulle = u"Nulle, pas d'exposition de l'employé à un facteur de pénibilité"
    simple = u"Simple, exposition à un seul facteur de pénibilité"
    multiple = u"Multiple, exposition à plusieurs facteurs de pénibilité"


class TypesGir(Enum):
    __order__ = 'gir_1 gir_2 gir_3 gir_4 gir_5 gir_6'
    non_defini = u"Non défini"
    gir_1 = u"Gir 1"
    gir_2 = u"Gir 2"
    gir_3 = u"Gir 3"
    gir_4 = u"Gir 4"
    gir_5 = u"Gir 5"
    gir_6 = u"Gir 6"


class TypesRSANonCalculable(Enum):
    __order__ = 'calculable tns conjoint_tns'
    calculable = u"Calculable"
    tns = u"tns"
    conjoint_tns = u"conjoint_tns"


class TypesScolarite(Enum):
    __order__ = 'inconnue college lycee'
    inconnue = u"Inconnue"
    college = u"Collège"
    lycee = u"Lycée"


class TypesStatutMarital(Enum):
    __order__ = 'non_renseigne marie celibataire divorce veuf pacse jeune_veuf'
    non_renseigne = u'Non renseigné'
    marie = u'Marié'
    celibataire = u'Celibataire'
    divorce = u'Divorcé'
    veuf = u'Veuf'
    pacse = u'Pacsé'
    jeune_veuf = u'Jeune veuf'


class TypesStatutOccupationLogement(Enum):
    __order__ = 'non_renseigne primo_accedant proprietaire locataire_hlm locataire_vide locataire_meuble loge_gratuitement locataire_foyer sans_domicile'
    non_renseigne = u"Non renseigné"
    primo_accedant = u"Accédant à la propriété"
    proprietaire = u"Propriétaire (non accédant) du logement"
    locataire_hlm = u"Locataire d'un logement HLM"
    locataire_vide = u"Locataire ou sous-locataire d'un logement loué vide non-HLM"
    locataire_meuble = u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel"
    loge_gratuitement = u"Logé gratuitement par des parents, des amis ou l'employeur"
    locataire_foyer = u"Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)"
    sans_domicile = u"Sans domicile stable"


class TypesTailleEntreprise(Enum):
    __order__ = 'non_pertinent moins_de_10 de_10_a_19 de_20_a_249 plus_de_250'
    non_pertinent = u"Non pertinent"
    moins_de_10 = u"Moins de 10 salariés"
    de_10_a_19 = u"De 10 à 19 salariés"
    de_20_a_249 = u"De 20 à 249 salariés"
    plus_de_250 = u"Plus de 250 salariés"


class TypesTnsTypeActivite(Enum):
    __order__ = 'achat_revente bic bnc'
    achat_revente = u'achat_revente'
    bic = u'bic'
    bnc = u'bnc'


class TypesZoneApl(Enum):
    __order__ = 'non_renseigne zone_1 zone_2 zone_3'
    non_renseigne = u"Non renseigné"
    zone_1 = u"Zone 1"
    zone_2 = u"Zone 2"
    zone_3 = u"Zone 3"

TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute

# Legacy roles. To be removed when they are not used by formulas anymore.
class QUIFAM(Enum):
    __order__ = 'chef part enf1 enf2 enf3 enf4 enf5 enf6 enf7 enf8 enf9'
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
    __order__ = 'vous conj pac1 pac2 pac3 pac4 pac5 pac6 pac7 pac8 pac9'
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
    __order__ = 'pref cref enf1 enf2 enf3 enf4 enf5 enf6 enf7 enf8 enf9'
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
