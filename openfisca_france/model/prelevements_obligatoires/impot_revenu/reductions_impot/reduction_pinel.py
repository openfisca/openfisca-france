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
        2014
        '''
        parameters = parameters(period).impot_revenu.reductions_impots.rpinel

        reduc_invest_real_2014 = _reduc_invest_real_2014(foyer_fiscal, parameters, period)

        return (
            + reduc_invest_real_2014
            + foyer_fiscal('rpinel_report', period)
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2015
        '''
        parameters = parameters(period).impot_revenu.reductions_impots.rpinel

        reduc_invest_real_2014 = _reduc_invest_real_2014(foyer_fiscal, parameters, period)
        reduc_invest_real_2015 = _reduc_invest_real_2015(foyer_fiscal, parameters, period)

        return (
            + reduc_invest_real_2014
            + reduc_invest_real_2015
            + foyer_fiscal('rpinel_report', period)
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2016
        '''
        parameters = parameters(period).impot_revenu.reductions_impots.rpinel

        reduc_invest_real_2014 = _reduc_invest_real_2014(foyer_fiscal, parameters, period)
        reduc_invest_real_2015 = _reduc_invest_real_2015(foyer_fiscal, parameters, period)
        reduc_invest_real_2016 = _reduc_invest_real_2016(foyer_fiscal, parameters, period)

        return (
            + reduc_invest_real_2014
            + reduc_invest_real_2015
            + reduc_invest_real_2016
            + foyer_fiscal('rpinel_report', period)
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2017
        '''
        parameters = parameters(period).impot_revenu.reductions_impots.rpinel

        reduc_invest_real_2014 = _reduc_invest_real_2014(foyer_fiscal, parameters, period)
        reduc_invest_real_2015 = _reduc_invest_real_2015(foyer_fiscal, parameters, period)
        reduc_invest_real_2016 = _reduc_invest_real_2016(foyer_fiscal, parameters, period)
        reduc_invest_real_2017 = _reduc_invest_real_2017(foyer_fiscal, parameters, period)

        return (
            + reduc_invest_real_2014
            + reduc_invest_real_2015
            + reduc_invest_real_2016
            + reduc_invest_real_2017
            + foyer_fiscal('rpinel_report', period)
            )


class rpinel_report(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"asdf1234"
    reference = "https://asdf1234.lex"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        reports = (
            # Depuis 2015
            'f7ai', 'f7bi', 'f7ci', 'f7di',
            # Depuis 2016
            'f7bz', 'f7cz', 'f7dz', 'f7ez',
            # Depuis 2017
            'f7qz', 'f7rz', 'f7sz', 'f7tz',
            )

        return sum_(foyer_fiscal(report, period) for report in reports)


def _reduc_invest_real_2014(foyer_fiscal, parameters, period):
    '''
    TODO: document
    '''
    invest_metropole_2014 = foyer_fiscal('f7ek', period)
    invest_domtom_2014 = foyer_fiscal('f7el', period)
    f7qa = foyer_fiscal('f7qa', period)
    f7qb = foyer_fiscal('f7qb', period)
    f7qc = foyer_fiscal('f7qc', period)
    f7qd = foyer_fiscal('f7qd', period)

    max1 = maximum(0, parameters.seuil - invest_domtom_2014 - f7qd)  # 2014 : plafond commun 'duflot' et 'rpinel'
    max2 = maximum(0, max1 - f7qc)
    max3 = maximum(0, max2 - invest_metropole_2014 - f7qb)

    return (
        + parameters.taux29 * minimum(maximum(0, parameters.seuil - invest_domtom_2014), f7qd) / 9
        + parameters.taux23 * minimum(max1, f7qc) / 6
        + parameters.taux18 * minimum(maximum(0, max2 - invest_metropole_2014), f7qb) / 9
        + parameters.taux12 * minimum(max3, f7qa) / 6
        )


def _reduc_invest_real_2015(foyer_fiscal, parameters, period):
    '''
    TODO: document
    '''
    f7qe = foyer_fiscal('f7qe', period)
    f7qf = foyer_fiscal('f7qf', period)
    f7qg = foyer_fiscal('f7qg', period)
    f7qh = foyer_fiscal('f7qh', period)

    return (
        + parameters.taux29 * minimum(parameters.seuil, f7qh) / 9
        + parameters.taux23 * minimum(maximum(0, parameters.seuil - f7qh), f7qg) / 6
        + parameters.taux18 * minimum(maximum(0, parameters.seuil - f7qh - f7qg), f7qf) / 9
        + parameters.taux12 * minimum(maximum(0, parameters.seuil - f7qh - f7qg - f7qf), f7qe) / 6
        )


def _reduc_invest_real_2016(foyer_fiscal, parameters, period):
    '''
    TODO: document
    '''
    f7qi = foyer_fiscal('f7qi', period)
    f7qj = foyer_fiscal('f7qj', period)
    f7qk = foyer_fiscal('f7qk', period)
    f7ql = foyer_fiscal('f7ql', period)

    return (
        + parameters.taux29 * minimum(parameters.seuil, f7ql) / 9
        + parameters.taux23 * minimum(maximum(0, parameters.seuil - f7ql), f7qk) / 6
        + parameters.taux18 * minimum(maximum(0, parameters.seuil - f7ql - f7qk), f7qj) / 9
        + parameters.taux12 * minimum(maximum(0, parameters.seuil - f7ql - f7qk - f7qj), f7qi) / 6
        )


def _reduc_invest_real_2017(foyer_fiscal, parameters, period):
    '''
    TODO: document
    '''
    f7qm = foyer_fiscal('f7qm', period)
    f7qn = foyer_fiscal('f7qn', period)
    f7qo = foyer_fiscal('f7qo', period)
    f7qp = foyer_fiscal('f7qp', period)

    return (
        + parameters.taux29 * minimum(parameters.seuil, f7qp) / 9
        + parameters.taux23 * minimum(maximum(0, parameters.seuil - f7qp), f7qo) / 6
        + parameters.taux18 * minimum(maximum(0, parameters.seuil - f7qp - f7qo), f7qn) / 9
        + parameters.taux12 * minimum(maximum(0, parameters.seuil - f7qp - f7qo - f7qn), f7qm) / 6
        )
