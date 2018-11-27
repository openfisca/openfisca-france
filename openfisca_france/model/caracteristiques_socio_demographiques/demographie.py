# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY


class adoption(Variable):
    value_type = bool
    entity = Individu
    label = u"Enfant adopté"
    definition_period = MONTH


class garde_alternee(Variable):
    value_type = bool
    entity = Individu
    label = u'Enfant en garde alternée'
    base_function = requested_period_last_or_next_value
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class activite(Variable):
    value_type = Enum
    default_value = TypesActivite.inactif
    possible_values = TypesActivite  # defined in model/base.py
    entity = Individu
    label = u"Activité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class enceinte(Variable):
    value_type = bool
    entity = Individu
    label = u"Est enceinte"
    definition_period = MONTH


class statut_marital(Variable):
    value_type = Enum
    possible_values = TypesStatutMarital  # defined in model/base.py
    default_value = TypesStatutMarital.celibataire
    entity = Individu
    label = u"Statut marital"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        # Par défault, on considère que deux adultes dans un foyer fiscal sont PACSÉS
        deux_adultes = individu.foyer_fiscal.nb_persons(FoyerFiscal.DECLARANT) >= 2
        return where(deux_adultes, TypesStatutMarital.pacse, TypesStatutMarital.celibataire)


class nbN(Variable):
    cerfa_field = u"N"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"
    definition_period = YEAR


class nbR(Variable):
    cerfa_field = u"R"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"
    definition_period = YEAR


class caseE(Variable):
    cerfa_field = u"E"
    value_type = bool
    entity = FoyerFiscal
    label = u"Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul"
    end = '2012-12-31'
    definition_period = YEAR


class caseF(Variable):
    cerfa_field = u"F"
    value_type = bool
    entity = FoyerFiscal
    label = u"Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)"
    definition_period = YEAR


class caseG(Variable):
    cerfa_field = u"G"
    value_type = bool
    entity = FoyerFiscal
    label = u"Titulaire d'une pension de veuve de guerre"
    definition_period = YEAR
    # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case
    # que l'on remplt et l'autre une case que l'on coche


class caseH(Variable):
    cerfa_field = u"H"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Année de naissance des enfants à charge en garde alternée"
    definition_period = YEAR


# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


class caseK(Variable):
    cerfa_field = u"K"
    value_type = bool
    entity = FoyerFiscal
    label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre"
    end = '2011-12-31'
    definition_period = YEAR


class caseL(Variable):
    cerfa_field = u"L"
    value_type = bool
    entity = FoyerFiscal
    label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul (définition depuis 2009) - Un au moins de vos enfants à charge ou rattaché est issu du mariage avec votre conjoint décédé (définition avant 2008)"
    definition_period = YEAR


class caseN(Variable):
    cerfa_field = u"N"
    value_type = bool
    entity = FoyerFiscal
    label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus"
    definition_period = YEAR


class caseP(Variable):
    cerfa_field = u"P"
    value_type = bool
    entity = FoyerFiscal
    label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%"
    definition_period = YEAR


class caseS(Variable):
    cerfa_field = u"S"
    value_type = bool
    entity = FoyerFiscal
    label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"
    definition_period = YEAR


class caseT(Variable):
    cerfa_field = u"T"
    value_type = bool
    entity = FoyerFiscal
    label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    # TODO: Set definition_period as YEAR and change the suggestion process (scenarios.py)


class caseW(Variable):
    cerfa_field = u"W"
    value_type = bool
    entity = FoyerFiscal
    label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"
    definition_period = YEAR


class handicap(Variable):
    value_type = bool
    entity = Individu
    label = u"Individu en situation de handicap"
    definition_period = MONTH


class invalidite(Variable):
    value_type = bool
    entity = Individu
    label = u"Individu titulaire d'une carte d'invalidité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nb_parents(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = u"Nombre d'adultes (parents) dans la famille"
    definition_period = MONTH

    def formula(famille, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.

        return famille.nb_persons(role = famille.PARENT)


class maries(Variable):
    value_type = bool
    entity = Famille
    label = u"maries"
    definition_period = MONTH

    def formula(famille, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        statut_marital = famille.members('statut_marital', period)
        individu_marie = (statut_marital == TypesStatutMarital.marie)

        return famille.any(individu_marie, role = famille.PARENT)


class en_couple(Variable):
    value_type = bool
    entity = Famille
    label = u"Indicatrice de vie en couple"
    definition_period = MONTH

    def formula(famille, period, parameters):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_parents = famille('nb_parents', period)

        return nb_parents == 2


class est_enfant_dans_famille(Variable):
    value_type = bool
    entity = Individu
    label = u"Indique que l'individu est un enfant dans une famille"
    definition_period = ETERNITY

    def formula(individu, period):
        return individu.has_role(Famille.ENFANT)


class etudiant(Variable):
    value_type = bool
    entity = Individu
    label = u"Indicatrice individuelle étudiant"
    definition_period = MONTH

    def formula(individu, period, parameters):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        activite = individu('activite', period)

        return activite == TypesActivite.etudiant


class rempli_obligation_scolaire(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = u"Rempli l'obligation scolaire"
    definition_period = MONTH


class ressortissant_eee(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = u"Ressortissant de l'EEE ou de la Suisse."
    definition_period = MONTH


class duree_possession_titre_sejour(Variable):
    value_type = int
    entity = Individu
    label = u"Durée depuis laquelle l'individu possède un titre de séjour (en années)"
    definition_period = MONTH


class enfant_place(Variable):
    value_type = bool
    entity = Individu
    label = u"Enfant placé en structure spécialisée ou famille d'accueil"
    definition_period = MONTH
