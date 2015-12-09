# -*- coding: utf-8 -*-

from ..base import *  # noqa


build_column('idmen', IntCol(is_permanent = True, label = u"Identifiant du ménage"))
build_column('idfoy', IntCol(is_permanent = True, label = u"Identifiant du foyer"))
build_column('idfam', IntCol(is_permanent = True, label = u"Identifiant de la famille"))

build_column('quimen', EnumCol(QUIMEN, is_permanent = True))
build_column('quifoy', EnumCol(QUIFOY, is_permanent = True))
build_column('quifam', EnumCol(QUIFAM, is_permanent = True))

build_column('birth', DateCol(default = date(1970, 1, 1), is_permanent = True, label = u"Date de naissance"))


build_column('adoption', BoolCol(entity = "ind", label = u"Enfant adopté"))

build_column('alt', BoolCol(label = u'Enfant en garde alternée'))  # TODO: cerfa_field


build_column('activite', EnumCol(label = u'Activité',
                     enum = Enum([u'Actif occupé',
                                u'Chômeur',
                                u'Étudiant, élève',
                                u'Retraité',
                                u'Autre inactif']), default = 4))


build_column('enceinte', BoolCol(entity = 'ind', label = u"Est enceinte"))


build_column('statmarit', EnumCol(label = u"Statut marital",
                      default = 2,
                      enum = Enum([u"Marié",
                                u"Célibataire",
                                u"Divorcé",
                                u"Veuf",
                                u"Pacsé",
                                u"Jeune veuf"], start = 1)))

build_column('nbN', PeriodSizeIndependentIntCol(cerfa_field = u'N', entity = 'foy',
    label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"))
build_column('nbR', PeriodSizeIndependentIntCol(cerfa_field = u'R', entity = 'foy',
    label = u"Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"))

build_column('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'E', end = date(2012, 12, 31)))
build_column('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)",
                  entity = 'foy',
                  cerfa_field = u'F'))
build_column('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                  entity = 'foy',
                  cerfa_field = u'G'))  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche
build_column('caseH', PeriodSizeIndependentIntCol(label = u"Année de naissance des enfants à charge en garde alternée", entity = 'foy',
                 cerfa_field = u'H'))
# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


build_column('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                  entity = 'foy',
                  cerfa_field = u'K', end = date(2011, 12, 31)))

build_column('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'L'))

build_column('caseN', BoolCol(label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'N'))
build_column('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                  entity = 'foy',
                  cerfa_field = u'P'))
build_column('caseS', BoolCol(label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'S'))

build_column('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'T'))

build_column('caseW', BoolCol(label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'W'))

# pour inv, il faut que tu regardes si tu es d'accord et si c'est bien la bonne case,
# la case P exsite déjà plus bas ligne 339 sous le nom caseP
build_column('invalide', BoolCol(label = u'Invalide'))  # TODO: cerfa_field



class nb_par(Variable):
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


class concub(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de vie en couple"

    def function(self, simulation, period):
        '''
        concub = 1 si vie en couple TODO: pas très heureux
        '''
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_par = simulation.calculate('nb_par', period)

        # TODO: concub n'est pas égal à 1 pour les conjoints
        return period, nb_par == 2


class isol(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Parent (s'il y a lieu) isolé"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_par = simulation.calculate('nb_par', period)

        return period, nb_par == 1


class est_enfant_dans_famille(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Indique qe l'individu est un enfant dans une famille"

    def function(self, simulation, period):
        quifam = simulation.calculate('quifam', period)
        return period, quifam > PART


class etu(Variable):
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
