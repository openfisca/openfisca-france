from openfisca_france.model.base import *


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = "Date de naissance"
    definition_period = ETERNITY


class majeur(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est considéré comme majeur"
    definition_period = MONTH

    def formula(individu, period, parameters):
        majeur = individu('age', period) >= parameters(period).marche_travail.age_majorite
        mineur_emancipe = individu('mineur_emancipe', period)

        return majeur + mineur_emancipe


class mineur_emancipe(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "L'individu est émancipé"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class adoption(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant adopté"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class garde_alternee(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant en garde alternée"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class plus_haut_diplome_niveau(Variable):
    value_type = Enum
    default_value = TypesNiveauDiplome.non_renseigne
    possible_values = TypesNiveauDiplome  # defined in model/base.py
    entity = Individu
    label = "Plus haut niveau de diplôme obtenu"
    definition_period = MONTH


class plus_haut_diplome_date_obtention(Variable):
    value_type = date
    default_value = date.max
    entity = Individu
    label = "Date d'obtention du diplôme de plus haut niveau"
    definition_period = MONTH


class alternant(Variable):
    value_type = bool
    label = "En formation en alternance"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.service-public.fr/particuliers/vosdroits/N11240"


class niveau_diplome_formation(Variable):
    value_type = Enum
    default_value = TypesNiveauDiplome.non_renseigne
    possible_values = TypesNiveauDiplome  # defined in model/base.py
    entity = Individu
    label = "Niveau du diplôme en cours de préparation"
    definition_period = MONTH


class activite(Variable):
    value_type = Enum
    default_value = TypesActivite.inactif
    possible_values = TypesActivite  # defined in model/base.py
    entity = Individu
    label = "Activité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class enceinte(Variable):
    value_type = bool
    entity = Individu
    label = "Est enceinte"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class statut_marital(Variable):
    value_type = Enum
    possible_values = TypesStatutMarital  # defined in model/base.py
    default_value = TypesStatutMarital.celibataire
    entity = Individu
    label = "Statut marital"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        # Par défault, on considère que deux adultes dans un foyer fiscal sont PACSÉS
        deux_adultes = individu.foyer_fiscal.nb_persons(FoyerFiscal.DECLARANT) >= 2
        return where(deux_adultes, TypesStatutMarital.pacse, TypesStatutMarital.celibataire)


class nbN(Variable):
    cerfa_field = "N"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = "Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"
    definition_period = YEAR


class nbR(Variable):
    cerfa_field = "R"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = "Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"
    definition_period = YEAR


class caseE(Variable):
    cerfa_field = "E"
    value_type = bool
    entity = FoyerFiscal
    label = "Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul"
    end = '2012-12-31'
    definition_period = YEAR


class caseF(Variable):
    cerfa_field = "F"
    value_type = bool
    entity = FoyerFiscal
    label = "Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)"
    definition_period = YEAR


class caseG(Variable):
    cerfa_field = "G"
    value_type = bool
    entity = FoyerFiscal
    label = "Titulaire d'une pension de veuve de guerre"
    definition_period = YEAR
    # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case
    # que l'on remplt et l'autre une case que l'on coche


class annee_naissance_pac_alterne(Variable):
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = "Année de naissance des enfants à charge en garde alternée"
    definition_period = YEAR
    # Il s'agit de l'année de naissance associé aux PAC déclarés dans nbH. Il peut y avoir plusieurs années de naissance si nbH>1. On ne le prend pas en compte


class caseK(Variable):
    cerfa_field = "K"
    value_type = bool
    entity = FoyerFiscal
    label = "Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre"
    end = '2011-12-31'
    definition_period = YEAR


class caseL(Variable):
    cerfa_field = "L"
    value_type = bool
    entity = FoyerFiscal
    label = "Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul (définition depuis 2009) - Un au moins de vos enfants à charge ou rattaché est issu du mariage avec votre conjoint décédé (définition avant 2008)"
    definition_period = YEAR


class caseN(Variable):
    cerfa_field = "N"
    value_type = bool
    entity = FoyerFiscal
    label = "Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus"
    definition_period = YEAR


class caseP(Variable):
    cerfa_field = "P"
    value_type = bool
    entity = FoyerFiscal
    label = "Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%"
    definition_period = YEAR


class caseS(Variable):
    cerfa_field = "S"
    value_type = bool
    entity = FoyerFiscal
    label = "Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"
    definition_period = YEAR


class caseT(Variable):
    cerfa_field = "T"
    value_type = bool
    entity = FoyerFiscal
    label = "Vous êtes parent isolé au 1er janvier de l'année de perception des revenus"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # TODO: Set definition_period as YEAR and change the suggestion process (scenarios.py)


class caseW(Variable):
    cerfa_field = "W"
    value_type = bool
    entity = FoyerFiscal
    label = "Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"
    definition_period = YEAR


class handicap(Variable):
    value_type = bool
    entity = Individu
    label = "Individu en situation de handicap"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class invalidite(Variable):
    value_type = bool
    entity = Individu
    label = "Individu titulaire d'une carte d'invalidité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nb_parents(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = "Nombre d'adultes (parents) dans la famille"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        # Note : Cette variable est « instantanée » : quelle que soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.

        return famille.nb_persons(role = Famille.PARENT)


class maries(Variable):
    value_type = bool
    entity = Famille
    label = "maries"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        # Note : Cette variable est « instantanée » : quelle que soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        statut_marital = famille.members('statut_marital', period)
        individu_marie = (statut_marital == TypesStatutMarital.marie)

        return famille.any(individu_marie, role = Famille.PARENT)


class en_couple(Variable):
    value_type = bool
    entity = Famille
    label = "Indicatrice de vie en couple"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        # Note : Cette variable est « instantanée » : quelle que soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_parents = famille('nb_parents', period)

        return nb_parents == 2


class est_enfant_dans_famille(Variable):
    value_type = bool
    entity = Individu
    label = "Indique que l'individu est un enfant dans une famille"
    definition_period = ETERNITY

    def formula(individu, period):
        return individu.has_role(Famille.ENFANT)


class etudiant(Variable):
    '''
    L'individu est inscrit·e dans un établissement en vue de la préparation d'un concours ou d'un diplôme de l'enseignement supérieur français : une université, une école de commerce ou d'ingénieur, dans un lycée pour un BTS…
    '''
    value_type = bool
    entity = Individu
    label = "Indique que l'individu dispose du statut étudiant"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.service-public.fr/particuliers/vosdroits/F986"

    def formula(individu, period, parameters):
        # Note : Cette variable est « instantanée » : quelle que soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        activite = individu('activite', period)

        return activite == TypesActivite.etudiant


class rempli_obligation_scolaire(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = "Remplit l'obligation scolaire"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nationalite(Variable):
    value_type = str
    entity = Individu
    default_value = 'FR'
    max_length = 2
    label = "Code ISO de la nationalité de l'individu"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class ressortissant_eee(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = "Individu ressortissant d'un pays membre de l'Espace Économique Européen (EEE)."
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        nationalite = individu('nationalite', period)
        return sum([nationalite == str.encode(etat_membre) for etat_membre in parameters(period).geopolitique.eee])  # TOOPTIMIZE: string encoding into bytes array should be done at load time


class resident_ue(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = "Individu résidant dans pays membre de l'Union européenne (UE)."
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        '''
        La résidence est supposée par la nationalité.
        Si la résidence est déterminée d'une autre manière plus précise, écraser cette variable en la définissant plutôt qu'en la laissant calculer par la nationalité.
        '''
        nationalite = individu('nationalite', period)
        return sum([nationalite == str.encode(etat_membre) for etat_membre in parameters(period).geopolitique.ue])  # TOOPTIMIZE: string encoding into bytes array should be done at load time


class residence_continue_annees(Variable):
    value_type = float
    entity = Individu
    label = "Durée depuis laquelle l'individu réside sur le territoire français de manière régulière et continue (en années)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class duree_possession_titre_sejour(Variable):
    value_type = float
    entity = Individu
    label = "Durée depuis laquelle l'individu possède un titre de séjour (en années)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class enfant_place(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant placé en structure spécialisée ou famille d'accueil"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class RegimeSecuriteSociale(Enum):
    regime_general = "Régime général"
    regime_agricole = "Régime Agricole"
    regime_retraite_fonctionnaires_civils_militaires_etat = "Régime de retraite des fonctionnaires civils et militaires de l’Etat"
    regime_special_fonctionnaires_territoriaux_hospitaliers = "Régime spécial des fonctionnaires territoriaux et hospitaliers"
    fond_special_pensions_ouvriers_etablissements_industriels_etat = "Le Fonds spécial des pensions des ouvriers des établissements industriels de l’Etat (FSPOEIE)"
    regime_special_agents_sncf = "Régime spécial des agents de la SNCF"
    regime_special_agents_ratp = "Régime spécial des agents de la RATP"
    regime_special_industries_electriques_gazieres = "Régime spécial des industries électriques et gazières (CNIEG)"
    autres_regimes = "Autres régimes"
    aucun = "Aucun"


class regime_securite_sociale(Variable):
    value_type = Enum
    possible_values = RegimeSecuriteSociale
    default_value = RegimeSecuriteSociale.aucun
    entity = Individu
    label = "Régime de sécurité sociale"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.securite-sociale.fr/files/live/sites/SSFR/files/medias/CCSS/2020/RAPPORT%20CCSS-Sept%202020.pdf"
