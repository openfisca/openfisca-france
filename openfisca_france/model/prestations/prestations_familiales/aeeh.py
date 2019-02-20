# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class aeeh_niveau_handicap(Variable):
    value_type = int
    entity = Individu
    label = u"Catégorie de handicap prise en compte pour l'AEEH"
    definition_period = MONTH


class aeeh(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation d'éducation de l'enfant handicapé"
    reference = "http://vosdroits.service-public.fr/particuliers/N14808.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2003_01_01(famille, period, parameters):
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
        isole = not_(famille('en_couple', janvier))
        prestations_familiales = parameters(period).prestations.prestations_familiales

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

        age = famille.members('age', janvier)
        handicap = famille.members('handicap', janvier)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)
        # Indicatrice d'isolement pour les indidivus
        isole = famille.project(isole)

        enfant_handicape = handicap * (age < prestations_familiales.aeeh.age)

        montant_par_enfant = enfant_handicape * (
            prestations_familiales.af.bmaf * (
                base
                + (niveau_handicap == 1) * cpl['1ere_categorie']
                + (niveau_handicap == 2) * (cpl['1ere_categorie'] + maj['2e_categorie'] * isole)
                + (niveau_handicap == 3) * (cpl['2e_categorie'] + maj['3e_categorie'] * isole)
                + (niveau_handicap == 4) * (cpl['3e_categorie'] + maj['4e_categorie'] * isole)
                + (niveau_handicap == 5) * (cpl['4e_categorie'] + maj['5e_categorie'] * isole)
                + (niveau_handicap == 6) * (maj['6e_categorie'] * isole)
                ) + (niveau_handicap == 6) * cpl['6e_categorie_1']
            ) / 12

        montant_total = famille.sum(montant_par_enfant, role = Famille.ENFANT)

    # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
    # versement des prestations familiales.
    # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
    # complément ni avec la majoration de parent isolé.
    # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
    # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
    # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
    # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumis à la CRDS
        return montant_total
