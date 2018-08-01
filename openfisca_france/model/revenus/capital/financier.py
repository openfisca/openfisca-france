# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa


# RVCM
# revenus au prélèvement libératoire
class f2da(Variable):
    cerfa_field = u"2DA"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %"
    # start_date = date(2008, 1, 1)
    end = "2012-12-31"
    definition_period = YEAR


class f2dh(Variable):
    cerfa_field = u"2DH"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %"
    definition_period = YEAR


class f2ee(Variable):
    cerfa_field = u"2EE"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Autres produits de placement soumis aux prélèvements libératoires"
    definition_period = YEAR


# revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
class f2dc(Variable):
    cerfa_field = u"2DC"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus des actions et parts donnant droit à abattement"
    definition_period = YEAR


class f2fu(Variable):
    cerfa_field = u"2FU"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement"
    definition_period = YEAR


class f2ch(Variable):
    cerfa_field = u"2CH"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement"
    definition_period = YEAR


#  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
class f2ts(Variable):
    cerfa_field = u"2TS"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)"
    definition_period = YEAR


class f2go(Variable):
    cerfa_field = u"2GO"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)"
    definition_period = YEAR


class f2tr(Variable):
    cerfa_field = u"2TR"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)"
    definition_period = YEAR


# Autres revenus des valeurs et capitaux mobiliers
class f2fa(Variable):
    cerfa_field = u"2FA"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Intérêts et autres produits de placement à revenu fixe n'excédant pas 2000 euros, taxables sur option à 24%"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR


class f2tt(Variable):
    cerfa_field = u"2TT"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Intérêts des prêts participatifs"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f2tu(Variable):
    cerfa_field = u"2TU"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Pertes en capital sur prêts participatifs en 2016"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f2tv(Variable):
    cerfa_field = u"2TV"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Pertes en capital sur prêts participatifs en 2017"
    # start_date = date(2017, 1, 1)
    definition_period = YEAR


class f2cg(Variable):
    cerfa_field = u"2CG"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible"
    definition_period = YEAR


class f2bh(Variable):
    cerfa_field = u"2BH"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f2ca(Variable):
    cerfa_field = u"2CA"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Frais et charges déductibles"
    definition_period = YEAR


class f2ck(Variable):
    cerfa_field = u"2CK"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé"
    # start_date = date(2013, 1, 1)
    definition_period = YEAR
    # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013


class f2ab(Variable):
    cerfa_field = u"2AB"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Crédits d'impôt sur valeurs étrangères"
    definition_period = YEAR


class f2bg(Variable):
    cerfa_field = u"2BG"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = (
        u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables"
    )
    definition_period = YEAR


class f2aa(Variable):
    cerfa_field = u"2AA"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f2al(Variable):
    cerfa_field = u"2AL"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


class f2am(Variable):
    cerfa_field = u"2AM"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class f2an(Variable):
    cerfa_field = u"2AN"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2010, 1, 1)
    definition_period = YEAR


class f2aq(Variable):
    cerfa_field = u"2AQ"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class f2ar(Variable):
    cerfa_field = u"2AR"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
# TODO: vérifier existence <=2011
class f2as(Variable):
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits: année 2012"
    end = "2011-12-31"
    definition_period = YEAR


class f2dm(Variable):
    cerfa_field = u"2DM"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


class f2gr(Variable):
    cerfa_field = u"2GR"
    value_type = int
    unit = "currency"
    entity = FoyerFiscal
    label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)"
    # start_date = date(2005, 1, 1)
    end = "2009-12-31"
    definition_period = YEAR
    # TODO: vérifier existence à partir de 2011


# Utilisés par mes aides. TODO: à consolider
class livret_a(Variable):
    value_type = float
    entity = Individu
    base_function = requested_period_last_value
    label = u"Épargne sur Livret A"
    definition_period = MONTH


class epargne_revenus_non_imposables(Variable):
    value_type = float
    entity = Individu
    base_function = requested_period_last_value
    label = u"Épargne générant des revenus non imposables hors Livret A"
    definition_period = MONTH


class epargne_revenus_imposables(Variable):
    value_type = float
    entity = Individu
    base_function = requested_period_last_value
    label = u"Épargne générant des revenus imposables"
    definition_period = MONTH


class revenus_capitaux_prelevement_bareme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus du capital imposés au barème (montants bruts)"
    set_input = set_input_divide_by_period
    reference = "http://bofip.impots.gouv.fr/bofip/3775-PGP"
    definition_period = MONTH

    def formula(foyer_fiscal, period, parameters):
        year = period.this_year
        f2dc = foyer_fiscal("f2dc", year)
        f2gr = foyer_fiscal("f2gr", year)
        f2ch = foyer_fiscal("f2ch", year)
        f2ts = foyer_fiscal("f2ts", year)
        f2go = foyer_fiscal("f2go", year)
        f2tr = foyer_fiscal("f2tr", year)
        f2fu = foyer_fiscal("f2fu", year)
        avoirs_credits_fiscaux = foyer_fiscal("avoirs_credits_fiscaux", year)
        f2da = foyer_fiscal("f2da", year)
        f2ee = foyer_fiscal("f2ee", year)
        majoration_revenus_reputes_distribues = parameters(
            period
        ).impot_revenu.rvcm.majoration_revenus_reputes_distribues

        return (
            f2dc
            + f2gr
            + f2ch
            + f2ts
            + f2go * majoration_revenus_reputes_distribues
            + f2tr
            + f2fu
            - avoirs_credits_fiscaux
        ) / 12

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        year = period.this_year
        f2dc = foyer_fiscal("f2dc", year)
        f2ch = foyer_fiscal("f2ch", year)
        f2ts = foyer_fiscal("f2ts", year)
        f2go = foyer_fiscal("f2go", year)
        f2tr = foyer_fiscal("f2tr", year)
        f2fu = foyer_fiscal("f2fu", year)
        avoirs_credits_fiscaux = foyer_fiscal("avoirs_credits_fiscaux", year)
        majoration_revenus_reputes_distribues = parameters(
            period
        ).impot_revenu.rvcm.majoration_revenus_reputes_distribues

        return (
            f2dc
            + f2ch
            + f2ts
            + f2go * majoration_revenus_reputes_distribues
            + f2tr
            + f2fu
            - avoirs_credits_fiscaux
        ) / 12


class revenus_capitaux_prelevement_liberatoire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenu du capital imposé au prélèvement libératoire (montants bruts)"
    set_input = set_input_divide_by_period
    reference = "http://bofip.impots.gouv.fr/bofip/3817-PGP"
    definition_period = MONTH

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        f2dh = foyer_fiscal("f2dh", period.this_year)
        f2ee = foyer_fiscal("f2ee", period.this_year)

        return (f2dh + f2ee) / 12

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        f2da = foyer_fiscal("f2da", period.this_year)
        f2dh = foyer_fiscal("f2dh", period.this_year)
        f2ee = foyer_fiscal("f2ee", period.this_year)

        return (f2da + f2dh + f2ee) / 12

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f2dh = foyer_fiscal("f2dh", period.this_year)
        f2ee = foyer_fiscal("f2ee", period.this_year)
        f2fa = foyer_fiscal("f2fa", period.this_year)

        return (f2dh + f2ee + f2fa) / 12


class revenus_capital(Variable):
    value_type = float
    entity = Individu
    label = u"Revenus du capital"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        types_revenus_capital = ["f2dc", "f2ch", "f2ts", "f2tr", "f2da", "f2dh", "f2ee"]
        return sum(
            individu.foyer_fiscal(type_revenu, period, options=[DIVIDE])
            * individu.has_role(individu.foyer_fiscal.DECLARANT_PRINCIPAL)
            for type_revenu in types_revenus_capital
        )
