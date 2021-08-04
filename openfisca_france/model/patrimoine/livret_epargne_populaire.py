from openfisca_france.model.base import Individu, Variable, min_, max_, not_, MONTH, set_input_dispatch_by_period, set_input_divide_by_period
from numpy import ceil


class livret_epargne_populaire_plafond(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article L221-15 du code monétaire et financier',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=5ADBC3914320B781FBF13FBA821C392E.tplgfr25s_3?idArticle=LEGIARTI000028447486&cidTexte=LEGITEXT000006072026&dateTexte=20190515',
        'Article 1417 du Code général des impôts',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=E596249E4FBBDB2A6D14A1D46EEB9451.tplgfr25s_3?idArticle=LEGIARTI000036443079&cidTexte=LEGITEXT000006069577&categorieLien=id&dateTexte=20200101'
        ]

    def formula(individu, period, parameters):
        params = parameters(period).epargne.livret_epargne_populaire
        residence = individu.menage('residence', period)
        bareme = params.baremes[residence]

        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        plafond = min_(1, nbptr) * bareme.valeur_de_base + 2 * (min_(max_(0, nbptr - 1), 0.5) * bareme.premiere_demi_part + max_(0, nbptr - 1.5) * bareme.demi_part_supplementaire)

        coef = params.coefficient_multiplicateur

        return ceil(coef * plafond)


class livret_epargne_populaire_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité au livret d'épargne populaire"
    reference = "https://www.service-public.fr/particuliers/vosdroits/F2367"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        plafond = individu('livret_epargne_populaire_plafond', period)
        independent = not_(individu('enfant_a_charge', period.this_year))

        return independent * (rfr <= plafond)


class livret_epargne_populaire_taux(Variable):
    value_type = float
    entity = Individu
    label = "Eligibilité au livret d'épargne populaire"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        eligibilite = individu('livret_epargne_populaire_eligibilite', period)

        epargne = parameters(period).epargne
        base_livret_a = epargne.livret_a.taux
        majoration = epargne.livret_epargne_populaire.majoration_base_livret_a
        return 100 * eligibilite * (base_livret_a + majoration)
