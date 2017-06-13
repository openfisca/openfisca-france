# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa


# Rentes viagères
class f1aw(Variable):
    cerfa_field = u"1AW"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans"
    definition_period = YEAR


class f1bw(Variable):
    cerfa_field = u"1BW"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans"
    definition_period = YEAR


class f1cw(Variable):
    cerfa_field = u"1CW"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans"
    definition_period = YEAR


class f1dw(Variable):
    cerfa_field = u"1DW"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans"
    definition_period = YEAR


# Revenus fonciers
class f4ba(Variable):
    cerfa_field = u"4BA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus fonciers imposables"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        revenus_locatifs = foyer_fiscal.members('revenus_locatifs', period, options = [ADD])
        return foyer_fiscal.sum(revenus_locatifs)



class f4bb(Variable):
    cerfa_field = u"4BB"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficit imputable sur les revenus fonciers"
    definition_period = YEAR


class f4bc(Variable):
    cerfa_field = u"4BC"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficit imputable sur le revenu global"
    definition_period = YEAR


class f4bd(Variable):
    cerfa_field = u"4BD"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits antérieurs non encore imputés"
    definition_period = YEAR


class f4be(Variable):
    cerfa_field = u"4BE"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Micro foncier: recettes brutes sans abattement"
    definition_period = YEAR


# Prime d'assurance loyers impayés
class f4bf(Variable):
    cerfa_field = u"4BF"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Primes d'assurance pour loyers impayés des locations conventionnées"
    definition_period = YEAR


class f4bl(Variable):
    column = IntCol
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR
    # TODO: cf 2010 2011


# Variables utilisées par mes aides
class revenus_locatifs(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenus locatifs"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class valeur_locative_immo_non_loue(Variable):
    column = FloatCol
    entity = Individu
    base_function = requested_period_last_value
    label = u"Valeur locative des biens immobiliers possédés et non loués"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class valeur_locative_terrains_non_loue(Variable):
    column = FloatCol
    entity = Individu
    base_function = requested_period_last_value
    label = u"Valeur locative des terrains possédés et non loués"
    definition_period = MONTH
    set_input = set_input_divide_by_period
