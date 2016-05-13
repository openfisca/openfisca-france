# -*- coding: utf-8 -*-

from ..base import *  # noqa


class idmen(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Identifiant du ménage"


class idfoy(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Identifiant du foyer"


class idfam(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Identifiant de la famille"



class quimen(Variable):
    column = EnumCol(enum = QUIMEN)
    entity_class = Individus
    is_permanent = True


class quifoy(Variable):
    column = EnumCol(enum = QUIFOY)
    entity_class = Individus
    is_permanent = True


class quifam(Variable):
    column = EnumCol(enum = QUIFAM)
    entity_class = Individus
    is_permanent = True



class date_naissance(Variable):
    column = DateCol(default = date(1970, 1, 1))
    entity_class = Individus
    is_permanent = True
    label = u"Date de naissance"




class adoption(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant adopté"



class garde_alternee(Variable):
    column = BoolCol
    entity_class = Individus
    label = u'Enfant en garde alternée'
    base_function = requested_period_last_or_next_value

class activite(Variable):
    column = EnumCol(
        default = 4,
        enum = Enum([u'Actif occupé',
            u'Chômeur',
            u'Étudiant, élève',
            u'Retraité',
            u'Autre inactif']),
        )
    entity_class = Individus
    label = u"Activité"




class enceinte(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Est enceinte"




class statmarit(Variable):
    column = EnumCol(
        default = 2,
        enum = Enum([u"Marié",
            u"Célibataire",
            u"Divorcé",
            u"Veuf",
            u"Pacsé",
            u"Jeune veuf"], start = 1),
        )
    entity_class = Individus
    label = u"Statut marital"



class nbN(Variable):
    cerfa_field = u"N"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"


class nbR(Variable):
    cerfa_field = u"R"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"



class caseE(Variable):
    cerfa_field = u"E"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul"
    stop_date = date(2012, 12, 31)


class caseF(Variable):
    cerfa_field = u"F"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)"


class caseG(Variable):
    cerfa_field = u"G"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Titulaire d'une pension de veuve de guerre"

  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche
class caseH(Variable):
    cerfa_field = u"H"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Année de naissance des enfants à charge en garde alternée"


# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


class caseK(Variable):
    cerfa_field = u"K"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre"
    stop_date = date(2011, 12, 31)



class caseL(Variable):
    cerfa_field = u"L"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul"



class caseN(Variable):
    cerfa_field = u"N"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus"


class caseP(Variable):
    cerfa_field = u"P"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%"


class caseS(Variable):
    cerfa_field = u"S"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"



class caseT(Variable):
    cerfa_field = u"T"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus"



class caseW(Variable):
    cerfa_field = u"W"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre"



class handicap(Variable):
    column = BoolCol
    entity_class = Individus
    label= u"Individu en situation de handicap"

class invalidite(Variable):
  column = BoolCol
  entity_class = Individus
  label=u"Individu titulaire d'une carte d'invalidité"

class nb_parents(Variable):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Familles
    label = u"Nombre d'adultes (parents) dans la famille"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        quifam_holder = simulation.compute('quifam', period)

        quifam = self.filter_role(quifam_holder, role = PART)

        return period, 1 + 1 * (quifam == PART)


class maries(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"maries"

    def function(self, simulation, period):
        """couple = 1 si couple marié sinon 0 TODO: faire un choix avec couple ?"""
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        statmarit_holder = simulation.compute('statmarit', period)

        statmarit = self.filter_role(statmarit_holder, role = CHEF)

        return period, statmarit == 1


class en_couple(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Indicatrice de vie en couple"

    def function(self, simulation, period):
        '''
        en_couple = 1 si vie en couple TODO: pas très heureux
        '''
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_parents = simulation.calculate('nb_parents', period)

        return period, nb_parents == 2


class est_enfant_dans_famille(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Indique qe l'individu est un enfant dans une famille"

    def function(self, simulation, period):
        quifam = simulation.calculate('quifam', period)
        return period, quifam > PART


class etudiant(Variable):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Indicatrice individuelle étudiant"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        activite = simulation.calculate('activite', period)

        return period, activite == 2

class rempli_obligation_scolaire(Variable):
    column = BoolCol(default = True)
    entity_class = Individus
    label = u"Rempli l'obligation scolaire"

class ressortissant_eee(Variable):
    column = BoolCol(default = True)
    entity_class = Individus
    label = u"Ressortissant de l'EEE ou de la Suisse."

class duree_possession_titre_sejour(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Durée depuis laquelle l'individu possède un titre de séjour (en années)"
