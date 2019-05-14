# -*- coding: utf-8 -*-

from openfisca_france.model.base import *

from numpy import ceil


class livret_epargne_populaire_plafond(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    reference = [
        'Article 1417 du Code général des impôts',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=E596249E4FBBDB2A6D14A1D46EEB9451.tplgfr25s_3?idArticle=LEGIARTI000036443079&cidTexte=LEGITEXT000006069577&categorieLien=id&dateTexte=20200101'
        ]

    def formula(individu, period, parameters):
        params = parameters(period).epargne.livret_epargne_populaire
        p_metropole = params.baremes.metropole
        p_mgr = params.baremes.martinique_guadeloupe_la_reunion
        p_guyane = params.baremes.guyane
        p_mayotte = params.baremes.mayotte

        nbptr = individu.foyer_fiscal('nbptr', period.n_2)

        metropole = min_(1, nbptr) * p_metropole.base + 2 * (max_(0, (nbptr - 1))) * p_metropole.demi_part_supplementaire
        mgr = min_(1, nbptr) * p_mgr.base + 2 * (min_(max_(0, nbptr - 1), 0.5) * p_mgr.premiere_demi_part + max_(0, nbptr - 1.5) * p_mgr.demi_part_supplementaire)
        guyane = min_(1, nbptr) * p_guyane.base + 2 * (min_(max_(0, nbptr - 1), 0.5) * p_guyane.premiere_demi_part + max_(0, nbptr - 1.5) * p_guyane.demi_part_supplementaire)
        mayotte = min_(1, nbptr) * p_mayotte.base + 2 * (min_(max_(0, nbptr - 1), 0.5) * p_mayotte.premiere_demi_part + max_(0, nbptr - 1.5) * p_mayotte.demi_part_supplementaire)

        r_mgr = individu.menage('residence_martinique', period) + individu.menage('residence_guadeloupe', period) + individu.menage('residence_reunion', period)
        r_guyane = individu.menage('residence_guyane', period)
        r_mayotte = individu.menage('residence_mayotte', period)
        r_metropole = not_(r_mgr + r_guyane + r_mayotte)

        plafond = (
            + r_metropole * metropole
            + r_mgr * mgr
            + r_guyane * guyane
            + r_mayotte * mayotte
            )

        coef = params.coefficient_multiplicateur
        return ceil(coef * plafond)


class livret_epargne_populaire_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = u"Eligibilité au livret d'épargne populaire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        plafond = individu('livret_epargne_populaire_plafond', period)

        return rfr <= plafond


class livret_epargne_populaire_taux(Variable):
    value_type = float
    entity = Individu
    label = u"Eligibilité au livret d'épargne populaire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        eligibilite = individu('livret_epargne_populaire_eligibilite', period)

        epargne = parameters(period).epargne
        base_livret_a = epargne.livret_a.taux
        majoration = epargne.livret_epargne_populaire.majoration_base_livret_a
        return 100 * eligibilite * (base_livret_a + majoration)
