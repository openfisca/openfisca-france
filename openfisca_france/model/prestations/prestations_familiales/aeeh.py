# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa


class aeeh_niveau_handicap(Variable):
    column = IntCol
    entity = Individu
    label = u"Catégorie de handicap prise en compte pour l'AEEH"
    definition_period = MONTH


class aeeh(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocation d'éducation de l'enfant handicapé"
    url = "http://vosdroits.service-public.fr/particuliers/N14808.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2003_01_01(self, simulation, period):
        '''
        Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)
        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.
        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit
        son activité professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        '''
        janvier = period.this_year.first_month
        age_holder = simulation.compute('age', janvier)
        handicap_holder = simulation.compute('handicap', janvier)
        isole = not_(simulation.calculate('en_couple', janvier))
        niveau_handicap_holder = simulation.compute('aeeh_niveau_handicap', period)
        prestations_familiales = simulation.legislation_at(period.start).prestations.prestations_familiales

        age = self.split_by_roles(age_holder, roles = ENFS)
        niveau_handicap = self.split_by_roles(niveau_handicap_holder, roles = ENFS)
        handicap = self.split_by_roles(handicap_holder, roles = ENFS)

        if period.start.year >= 2006:
            base = prestations_familiales.aeeh.base
            cpl = prestations_familiales.aeeh.complement_d_allocation
            maj = prestations_familiales.aeeh.majoration_pour_parent_isole
        else:
            base = prestations_familiales.aes.base
            cpl = prestations_familiales.aes.complement_d_allocation
            cpl['6e_categorie_1'] = cpl['6e_categorie_2']
            maj = dict()
            for categorie in range(2, 7):
                maj['{}e_categorie'.format(categorie)] = 0

        aeeh = 0
        for enfant in age.iterkeys():
            enfhand = handicap[enfant] * (age[enfant] < prestations_familiales.aeeh.age) / 12
            categ = niveau_handicap[enfant]
            aeeh += enfhand * (
                prestations_familiales.af.bmaf * (
                    base +
                    cpl['1ere_categorie'] * (categ == 1) +
                    (categ == 2) * (cpl['1ere_categorie'] + maj['2e_categorie'] * isole) +
                    (categ == 3) * (cpl['2e_categorie'] + maj['3e_categorie'] * isole) +
                    (categ == 4) * (cpl['3e_categorie'] + maj['4e_categorie'] * isole) +
                    (categ == 5) * (cpl['4e_categorie'] + maj['5e_categorie'] * isole) +
                    (categ == 6) * (maj['6e_categorie'] * isole)
                    ) +
                (categ == 6) * cpl['6e_categorie_1']
                )

    # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
    # versement des prestations familiales.
    # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
    # complément ni avec la majoration de parent isolé.
    # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
    # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
    # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
    # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumis à la CRDS
        return aeeh
