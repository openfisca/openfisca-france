# -*- coding: utf-8 -*-

from numpy import (
    minimum,
    maximum,
    sum as sum_,
    )

from openfisca_france.model.base import (
    FoyerFiscal,
    Variable,
    YEAR,
    )


class rpinel(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Réduction d'impôt en faveur de l'investissement locatif intermédiaire - Dispositif Pinel"
    reference = "http://bofip.impots.gouv.fr/bofip/8425-PGP"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        Depuis 2014
        '''
        return (
            + foyer_fiscal("rpinel_report", period)
            + foyer_fiscal("rpinel_reduc_invest_real", period)
            )


class rpinel_report(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2015_01_01(foyer_fiscal, period):
        reports = (
            # Depuis 2015
            "f7ai", "f7bi", "f7ci", "f7di",
            # Depuis 2016
            "f7bz", "f7cz", "f7dz", "f7ez",
            # Depuis 2017
            "f7qz", "f7rz", "f7sz", "f7tz",
            )

        return sum_(foyer_fiscal(report, period) for report in reports)


class rpinel_reduc_invest_real(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        reductions = (
            "rpinel_reduc_invest_real_taux12",
            "rpinel_reduc_invest_real_taux18",
            "rpinel_reduc_invest_real_taux23",
            "rpinel_reduc_invest_real_taux29",
            )

        return sum_(foyer_fiscal(reduction, period) for reduction in reductions)


class rpinel_reduc_invest_real_taux12(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        rpinel = parameters(period).impot_revenu.reductions_impots.rpinel
        seuil = rpinel.seuil
        taux = rpinel.taux12
        rate = 6

        invest_metropole_2014 = foyer_fiscal("f7ek", period)
        invest_domtom_2014 = foyer_fiscal("f7el", period)
        f7qa = foyer_fiscal("f7qa", period)
        f7qb = foyer_fiscal("f7qb", period)
        f7qc = foyer_fiscal("f7qc", period)
        f7qd = foyer_fiscal("f7qd", period)
        f7qe = foyer_fiscal("f7qe", period)
        f7qf = foyer_fiscal("f7qf", period)
        f7qg = foyer_fiscal("f7qg", period)
        f7qh = foyer_fiscal("f7qh", period)
        f7qi = foyer_fiscal("f7qi", period)
        f7qj = foyer_fiscal("f7qj", period)
        f7qk = foyer_fiscal("f7qk", period)
        f7ql = foyer_fiscal("f7ql", period)
        f7qm = foyer_fiscal("f7qm", period)
        f7qn = foyer_fiscal("f7qn", period)
        f7qo = foyer_fiscal("f7qo", period)
        f7qp = foyer_fiscal("f7qp", period)

        max1 = maximum(0, seuil - invest_domtom_2014 - f7qd)
        max2 = maximum(0, max1 - f7qc)

        reductions = (
            # Depuis 2014
            + minimum(maximum(0, max2 - invest_metropole_2014 - f7qb), f7qa)
            # Depuis 2015
            + minimum(maximum(0, seuil - f7qh - f7qg - f7qf), f7qe)
            # Depuis 2016
            + minimum(maximum(0, seuil - f7ql - f7qk - f7qj), f7qi)
            # Depuis 2017
            + minimum(maximum(0, seuil - f7qp - f7qo - f7qn), f7qm)
            )

        return taux * reductions / rate


class rpinel_reduc_invest_real_taux18(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        rpinel = parameters(period).impot_revenu.reductions_impots.rpinel
        seuil = rpinel.seuil
        taux = rpinel.taux18
        rate = 9

        invest_metropole_2014 = foyer_fiscal("f7ek", period)
        invest_domtom_2014 = foyer_fiscal("f7el", period)
        f7qb = foyer_fiscal("f7qb", period)
        f7qc = foyer_fiscal("f7qc", period)
        f7qd = foyer_fiscal("f7qd", period)
        f7qf = foyer_fiscal("f7qf", period)
        f7qg = foyer_fiscal("f7qg", period)
        f7qh = foyer_fiscal("f7qh", period)
        f7qj = foyer_fiscal("f7qj", period)
        f7qk = foyer_fiscal("f7qk", period)
        f7ql = foyer_fiscal("f7ql", period)
        f7qn = foyer_fiscal("f7qn", period)
        f7qo = foyer_fiscal("f7qo", period)
        f7qp = foyer_fiscal("f7qp", period)

        max1 = maximum(0, seuil - invest_domtom_2014 - f7qd)
        max2 = maximum(0, max1 - f7qc)

        reductions = (
            # Depuis 2014
            + minimum(maximum(0, max2 - invest_metropole_2014), f7qb)  # 2014 : plafond commun 'duflot' et 'rpinel'
            # Depuis 2015
            + minimum(maximum(0, seuil - f7qh - f7qg), f7qf)
            # Depuis 2016
            + minimum(maximum(0, seuil - f7ql - f7qk), f7qj)
            # Depuis 2017
            + minimum(maximum(0, seuil - f7qp - f7qo), f7qn)
            )

        return taux * reductions / rate


class rpinel_reduc_invest_real_taux23(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        rpinel = parameters(period).impot_revenu.reductions_impots.rpinel
        seuil = rpinel.seuil
        taux = rpinel.taux23
        rate = 6

        invest_domtom_2014 = foyer_fiscal("f7el", period)
        f7qc = foyer_fiscal("f7qc", period)
        f7qd = foyer_fiscal("f7qd", period)
        f7qg = foyer_fiscal("f7qg", period)
        f7qh = foyer_fiscal("f7qh", period)
        f7qk = foyer_fiscal("f7qk", period)
        f7ql = foyer_fiscal("f7ql", period)
        f7qo = foyer_fiscal("f7qo", period)
        f7qp = foyer_fiscal("f7qp", period)

        reductions = (
            # Depuis 2014
            + minimum(maximum(0, seuil - invest_domtom_2014 - f7qd), f7qc)  # 2014 : plafond commun 'duflot' et 'rpinel'
            # Depuis 2015
            + minimum(maximum(0, seuil - f7qh), f7qg)
            # Depuis 2016
            + minimum(maximum(0, seuil - f7ql), f7qk)
            # Depuis 2017
            + minimum(maximum(0, seuil - f7qp), f7qo)
            )

        return taux * reductions / rate


class rpinel_reduc_invest_real_taux29(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        rpinel = parameters(period).impot_revenu.reductions_impots.rpinel
        seuil = rpinel.seuil
        taux = rpinel.taux29
        rate = 9

        invest_domtom_2014 = foyer_fiscal("f7el", period)
        f7qd = foyer_fiscal("f7qd", period)
        f7qh = foyer_fiscal("f7qh", period)
        f7ql = foyer_fiscal("f7ql", period)
        f7qp = foyer_fiscal("f7qp", period)

        reductions = (
            # Depuis 2014
            + minimum(maximum(0, seuil - invest_domtom_2014), f7qd)
            # Depuis 2015
            + minimum(seuil, f7qh)
            # Depuis 2016
            + minimum(seuil, f7ql)
            # Depuis 2017
            + minimum(seuil, f7qp)
            )

        return taux * reductions / rate
