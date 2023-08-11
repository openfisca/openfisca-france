from openfisca_core.model_api import *
from openfisca_france.entities import Famille, FoyerFiscal, Individu, Menage  # noqa F401


AGE_INT_MINIMUM = -9999


# Enums commonly used through the legislation


class TypesNiveauDiplome(Enum):
    # répertoire national des certifications professionnelles
    # https://fr.wikipedia.org/wiki/Liste_des_diplômes_en_France#Nomenclature_des_niveaux_de_diplômes
    # https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037964754/
    __order__ = 'non_renseigne niveau_1 niveau_2 niveau_3 niveau_4 niveau_5 niveau_6 niveau_7 niveau_8'
    non_renseigne = 'Non renseigné'
    niveau_1 = 'Niveau 1 - École maternelle'
    niveau_2 = 'Niveau 2 - École élémentaire'
    niveau_3 = 'Niveau 3 - CAP, DNP, CFG'
    niveau_4 = 'Niveau 4 - Baccalauréat'
    niveau_5 = 'Niveau 5 - Bac+2 BTS, CPGE'
    niveau_6 = 'Niveau 6 - Bac+3 Licence, BUT'
    niveau_7 = 'Niveau 7 - Bac+5 Master'
    niveau_8 = 'Niveau 8 - Bac+8 Doctorat'


class TypesMention(Enum):
    # Mentions délivrées aux candidats à l'issue d'épreuves d'enseignement.
    # https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037875563/2021-04-02
    __order__ = 'non_renseignee mention_assez_bien mention_bien mention_tres_bien mention_tres_bien_felicitations_jury'
    non_renseignee = 'Non renseignée'
    mention_assez_bien = 'Mention assez bien'  # [12, 14[
    mention_bien = 'Mention bien'  # [14, 16[
    mention_tres_bien = 'Mention très bien'  # [16, 18[
    mention_tres_bien_felicitations_jury = 'Mention très bien avec félicitations du jury'  # 18+


class TypesActivite(Enum):
    __order__ = 'actif chomeur etudiant retraite inactif'
    actif = 'Actif occupé'
    chomeur = 'Chômeur'
    etudiant = 'Étudiant, élève'
    retraite = 'Retraité'
    inactif = 'Autre, inactif'


class TypesSecteurActivite(Enum):
    __order__ = 'non_renseigne agricole non_agricole'
    non_renseigne = 'Non renseigné'
    agricole = 'Agricole'
    non_agricole = 'Non agricole'


class TypesCategorieNonSalarie(Enum):
    __order__ = 'non_pertinent artisan commercant profession_liberale'  # Needed to preserve the enum order in Python 2
    non_pertinent = "Non pertinent (l'individu n'est pas un travailleur indépendant)"
    artisan = 'Artisan'
    commercant = 'Commerçant'
    profession_liberale = 'Profession libérale'


class TypesCategorieSalarie(Enum):
    __order__ = 'prive_non_cadre prive_cadre public_titulaire_etat public_titulaire_militaire public_titulaire_territoriale public_titulaire_hospitaliere public_non_titulaire non_pertinent'  # Needed to preserve the enum order in Python 2
    prive_non_cadre = 'Non cadre du secteur privé'
    prive_cadre = 'Cadre du secteur privé'
    public_titulaire_etat = "Titulaire de la fonction publique d'État"
    public_titulaire_militaire = 'Titulaire de la fonction publique militaire'
    public_titulaire_territoriale = 'Titulaire de la fonction publique territoriale'
    public_titulaire_hospitaliere = 'Titulaire de la fonction publique hospitalière'
    public_non_titulaire = 'Agent non-titulaire de la fonction publique'  # Les agents non titulaires, c’est-à-dire titulaires d’aucun grade de la fonction publique, peuvent être des contractuels, des vacataires, des auxiliaires, des emplois aidés…Les assistants maternels et familiaux sont eux aussi des non-titulaires.
    non_pertinent = 'Non pertinent'


class TypesStatutMarital(Enum):
    # La mention jeune_veuf indique que la personne est devenue veuve dans l'année.
    __order__ = 'non_renseigne marie celibataire divorce veuf pacse jeune_veuf'  # Needed to preserve the enum order in Python 2
    non_renseigne = 'Non renseigné'
    marie = 'Marié'
    celibataire = 'Célibataire'
    divorce = 'Divorcé'
    veuf = 'Veuf'
    pacse = 'Pacsé'
    jeune_veuf = 'Veuf d’un conjoint décédé dans l’année'


class TypesStatutOccupationLogement(Enum):
    __order__ = 'non_renseigne primo_accedant proprietaire locataire_hlm locataire_vide locataire_meuble loge_gratuitement locataire_foyer sans_domicile'  # Needed to preserve the enum order in Python 2
    non_renseigne = 'Non renseigné'
    primo_accedant = 'Accédant à la propriété'
    proprietaire = 'Propriétaire (non accédant) du logement'
    locataire_hlm = "Locataire d'un logement HLM"
    locataire_vide = "Locataire ou sous-locataire d'un logement loué vide non-HLM"
    locataire_meuble = "Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel"
    loge_gratuitement = "Logé gratuitement par des parents, des amis ou l'employeur"
    locataire_foyer = "Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)"
    sans_domicile = 'Sans domicile stable'


# Taux de prime moyen de la fonction publique
TAUX_DE_PRIME = 0.195  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute
