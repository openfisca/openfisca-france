# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa

from numpy import logical_not as not_

class aeeh_niveau_handicap(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Catégorie de handicap prise en compte pour l'AEEH"

class aeeh(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation d'éducation de l'enfant handicapé"
    url = "http://vosdroits.service-public.fr/particuliers/N14808.xhtml"

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_20020101_20021231(self, simulation, period):
        '''
        Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.

        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
        professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period)
        handicap_holder = simulation.compute('handicap', period)
        niveau_handicap_holder = simulation.compute('aeeh_niveau_handicap', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        niveau_handicap = self.split_by_roles(niveau_handicap_holder, roles = ENFS)
        handicap = self.split_by_roles(handicap_holder, roles = ENFS)

        aeeh = 0
        for enfant in age.iterkeys():
            enfhand = handicap[enfant] * (age[enfant] < P.aeeh.age) / 12
            categ = niveau_handicap[enfant]
            aeeh += 0 * enfhand  # TODO:

    # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
    # versement des prestations familiales.
    # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
    # complément ni avec la majoration de parent isolé.
    # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
    # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
    # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
    # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumis à la CRDS
        return period, 12 * aeeh  # annualisé

    @dated_function(start = date(2003, 1, 1), stop = date(2015, 12, 31))
    def function_20030101_20151231(self, simulation, period):
        '''
        Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.

        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
        professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period)
        handicap_holder = simulation.compute('handicap', period)
        isole = not_(simulation.calculate('en_couple', period))
        niveau_handicap_holder = simulation.compute('aeeh_niveau_handicap', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        niveau_handicap = self.split_by_roles(niveau_handicap_holder, roles = ENFS)
        handicap = self.split_by_roles(handicap_holder, roles = ENFS)

        aeeh = 0
        for enfant in age.iterkeys():
            enfhand = handicap[enfant] * (age[enfant] < P.aeeh.age) / 12
            categ = niveau_handicap[enfant]
            aeeh += enfhand * (P.af.bmaf * (P.aeeh.base +
                                  P.aeeh.cpl1 * (categ == 1) +
                                  (categ == 2) * (P.aeeh.cpl2 + P.aeeh.maj2 * isole) +
                                  (categ == 3) * (P.aeeh.cpl3 + P.aeeh.maj3 * isole) +
                                  (categ == 4) * (P.aeeh.cpl4 + P.aeeh.maj4 * isole) +
                                  (categ == 5) * (P.aeeh.cpl5 + P.aeeh.maj5 * isole) +
                                  (categ == 6) * (P.aeeh.maj6 * isole)) +
                                  (categ == 6) * P.aeeh.cpl6)

    # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
    # versement des prestations familiales.
    # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
    # complément ni avec la majoration de parent isolé.
    # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
    # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
    # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
    # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumis à la CRDS
        return period, 12 * aeeh  # annualisé
