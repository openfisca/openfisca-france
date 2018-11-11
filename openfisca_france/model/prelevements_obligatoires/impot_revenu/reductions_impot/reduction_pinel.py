# -*- coding: utf-8 -*-

from numpy import minimum as min_, maximum as max_

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
        invest_metropole_2014 = foyer_fiscal('f7ek', period)
        invest_domtom_2014 = foyer_fiscal('f7el', period)
        f7qa = foyer_fiscal('f7qa', period)
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        P = parameters(period).impot_revenu.reductions_impots.rpinel

        max1 = max_(0, P.seuil - invest_domtom_2014 - f7qd)  # 2014 : plafond commun 'duflot' et 'rpinel'
        max2 = max_(0, max1 - f7qc)
        max3 = max_(0, max2 - invest_metropole_2014 - f7qb)

        return (
            P.taux29 * min_(max_(0, P.seuil - invest_domtom_2014), f7qd) / 9
            + P.taux23 * min_(max1, f7qc) / 6
            + P.taux18 * min_(max_(0, max2 - invest_metropole_2014), f7qb) / 9
            + P.taux12 * min_(max3, f7qa) / 6
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2015
        '''
        f7ai = foyer_fiscal('f7ai', period)
        f7bi = foyer_fiscal('f7bi', period)
        f7ci = foyer_fiscal('f7ci', period)
        f7di = foyer_fiscal('f7di', period)
        invest_metropole_2014 = foyer_fiscal('f7ek', period)
        invest_domtom_2014 = foyer_fiscal('f7el', period)
        f7qa = foyer_fiscal('f7qa', period)
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        P = parameters(period).impot_revenu.reductions_impots.rpinel

        max1 = max_(0, P.seuil - invest_domtom_2014 - f7qd)  # 2014 : plafond commun 'duflot' et 'rpinel'
        max2 = max_(0, max1 - f7qc)
        max3 = max_(0, max2 - invest_metropole_2014 - f7qb)

        reduc_invest_real_2014 = (
            P.taux29 * min_(max_(0, P.seuil - invest_domtom_2014), f7qd) / 9
            + P.taux23 * min_(max1, f7qc) / 6
            + P.taux18 * min_(max_(0, max2 - invest_metropole_2014), f7qb) / 9
            + P.taux12 * min_(max3, f7qa) / 6
            )

        reduc_invest_real_2015 = (
            P.taux29 * min_(P.seuil, f7qh) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7qh), f7qg) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7qh - f7qg), f7qf) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7qh - f7qg - f7qf), f7qe) / 6
            )

        report = f7ai + f7bi + f7ci + f7di

        return reduc_invest_real_2014 + reduc_invest_real_2015 + report

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2016
        '''
        f7ai = foyer_fiscal('f7ai', period)
        f7bi = foyer_fiscal('f7bi', period)
        f7bz = foyer_fiscal('f7bz', period)
        f7ci = foyer_fiscal('f7ci', period)
        f7cz = foyer_fiscal('f7cz', period)
        f7di = foyer_fiscal('f7di', period)
        f7dz = foyer_fiscal('f7dz', period)
        invest_metropole_2014 = foyer_fiscal('f7ek', period)
        invest_domtom_2014 = foyer_fiscal('f7el', period)
        f7ez = foyer_fiscal('f7ez', period)
        f7qa = foyer_fiscal('f7qa', period)
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qj = foyer_fiscal('f7qj', period)
        f7qk = foyer_fiscal('f7qk', period)
        f7ql = foyer_fiscal('f7ql', period)
        P = parameters(period).impot_revenu.reductions_impots.rpinel

        max1 = max_(0, P.seuil - invest_domtom_2014 - f7qd)  # 2014 : plafond commun 'duflot' et 'rpinel'
        max2 = max_(0, max1 - f7qc)
        max3 = max_(0, max2 - invest_metropole_2014 - f7qb)

        reduc_invest_real_2014 = (
            P.taux29 * min_(max_(0, P.seuil - invest_domtom_2014), f7qd) / 9
            + P.taux23 * min_(max1, f7qc) / 6
            + P.taux18 * min_(max_(0, max2 - invest_metropole_2014), f7qb) / 9
            + P.taux12 * min_(max3, f7qa) / 6
            )

        reduc_invest_real_2015 = (
            P.taux29 * min_(P.seuil, f7qh) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7qh), f7qg) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7qh - f7qg), f7qf) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7qh - f7qg - f7qf), f7qe) / 6
            )

        reduc_invest_real_2016 = (
            P.taux29 * min_(P.seuil, f7ql) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7ql), f7qk) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7ql - f7qk), f7qj) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7ql - f7qk - f7qj), f7qi) / 6
            )

        report = f7ai + f7bi + f7ci + f7di + f7bz + f7cz + f7dz + f7ez

        return reduc_invest_real_2014 + reduc_invest_real_2015 + reduc_invest_real_2016 + report

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        2017
        '''
        f7ai = foyer_fiscal('f7ai', period)
        f7bi = foyer_fiscal('f7bi', period)
        f7bz = foyer_fiscal('f7bz', period)
        f7ci = foyer_fiscal('f7ci', period)
        f7cz = foyer_fiscal('f7cz', period)
        f7di = foyer_fiscal('f7di', period)
        f7dz = foyer_fiscal('f7dz', period)
        invest_metropole_2014 = foyer_fiscal('f7ek', period)
        invest_domtom_2014 = foyer_fiscal('f7el', period)
        f7ez = foyer_fiscal('f7ez', period)
        f7qa = foyer_fiscal('f7qa', period)
        f7qb = foyer_fiscal('f7qb', period)
        f7qc = foyer_fiscal('f7qc', period)
        f7qd = foyer_fiscal('f7qd', period)
        f7qe = foyer_fiscal('f7qe', period)
        f7qf = foyer_fiscal('f7qf', period)
        f7qg = foyer_fiscal('f7qg', period)
        f7qh = foyer_fiscal('f7qh', period)
        f7qi = foyer_fiscal('f7qi', period)
        f7qj = foyer_fiscal('f7qj', period)
        f7qk = foyer_fiscal('f7qk', period)
        f7ql = foyer_fiscal('f7ql', period)
        f7qm = foyer_fiscal('f7qm', period)
        f7qn = foyer_fiscal('f7qn', period)
        f7qo = foyer_fiscal('f7qo', period)
        f7qp = foyer_fiscal('f7qp', period)
        f7qz = foyer_fiscal('f7qz', period)
        f7rz = foyer_fiscal('f7rz', period)
        f7sz = foyer_fiscal('f7sz', period)
        f7tz = foyer_fiscal('f7tz', period)

        P = parameters(period).impot_revenu.reductions_impots.rpinel

        max1 = max_(0, P.seuil - invest_domtom_2014 - f7qd)  # 2014 : plafond commun 'duflot' et 'rpinel'
        max2 = max_(0, max1 - f7qc)
        max3 = max_(0, max2 - invest_metropole_2014 - f7qb)

        reduc_invest_real_2014 = (
            P.taux29 * min_(max_(0, P.seuil - invest_domtom_2014), f7qd) / 9
            + P.taux23 * min_(max1, f7qc) / 6
            + P.taux18 * min_(max_(0, max2 - invest_metropole_2014), f7qb) / 9
            + P.taux12 * min_(max3, f7qa) / 6
            )

        reduc_invest_real_2015 = (
            P.taux29 * min_(P.seuil, f7qh) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7qh), f7qg) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7qh - f7qg), f7qf) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7qh - f7qg - f7qf), f7qe) / 6
            )

        reduc_invest_real_2016 = (
            P.taux29 * min_(P.seuil, f7ql) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7ql), f7qk) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7ql - f7qk), f7qj) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7ql - f7qk - f7qj), f7qi) / 6
            )

        reduc_invest_real_2017 = (
            P.taux29 * min_(P.seuil, f7qp) / 9
            + P.taux23 * min_(max_(0, P.seuil - f7qp), f7qo) / 6
            + P.taux18 * min_(max_(0, P.seuil - f7qp - f7qo), f7qn) / 9
            + P.taux12 * min_(max_(0, P.seuil - f7qp - f7qo - f7qn), f7qm) / 6
            )

        report = f7ai + f7bi + f7ci + f7di + f7bz + f7cz + f7dz + f7ez + f7qz + f7rz + f7sz + f7tz

        return (
            reduc_invest_real_2014
            + reduc_invest_real_2015
            + reduc_invest_real_2016
            + reduc_invest_real_2017
            + report
            )
