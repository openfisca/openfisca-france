import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)

# Calcul de la partie du prélèvement forfaitaire unique (PFU) associé à l'impôt sur le revenu
# (le reste étant associé aux prélèvements sociaux)


class assurance_vie_pfu_ir_plus8ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 8 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR


class assurance_vie_pfu_ir_plus6ans_avant1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 6 ans pour les contrats souscrits avant le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    reference = 'https://www.legifrance.gouv.fr/affichTexteArticle.do?idArticle=LEGIARTI000036377422&cidTexte=JORFTEXT000036339197'  # Art. 28 (modif art 125 A, 125-0 A, 200 A et art 117 quater du CGI)
    definition_period = YEAR


class assurance_vie_pfu_ir_moins4ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de moins de 4 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    reference = 'https://www.legifrance.gouv.fr/affichTexteArticle.do?idArticle=LEGIARTI000036377422&cidTexte=JORFTEXT000036339197'  # Art. 28 (modif art 125 A, 125-0 A, 200 A et art 117 quater du CGI)
    definition_period = YEAR


class assurance_vie_pfu_ir_4_8_ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée entre 4 et 8 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR


class assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie de plus de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    reference = 'https://www.legifrance.gouv.fr/affichTexteArticle.do?idArticle=LEGIARTI000036377422&cidTexte=JORFTEXT000036339197'  # Art. 28 (modif art 125 A, 125-0 A, 200 A et art 117 quater du CGI)
    definition_period = YEAR


class assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie entre 4 et 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR


class assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie de moins de 4 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    reference = 'https://www.legifrance.gouv.fr/affichTexteArticle.do?idArticle=LEGIARTI000036377422&cidTexte=JORFTEXT000036339197'  # Art. 28 (modif art 125 A, 125-0 A, 200 A et art 117 quater du CGI)
    definition_period = YEAR


class f2zz(Variable):
    cerfa_field = '2ZZ'
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie de moins de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées après le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR
    # start_date = date(2018, 1, 1)


class f2vv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie de plus de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées après le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu; produit correspondant aux primes n'excédant pas 150 000 euros."
    definition_period = YEAR
    # start_date = date(2018, 1, 1)


class f2ww(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie de plus de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées après le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu; produit correspondant aux primes excédant pas 150 000 euros."
    definition_period = YEAR
    # start_date = date(2018, 1, 1)


class assurance_vie_pfu_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie soumis au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period):
        f2zz = foyer_fiscal('f2zz', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)

        return f2zz + f2vv + f2ww


class revenus_capitaux_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus des valeurs et capitaux mobiliers soumis au prélèvement forfaitaire unique (partie impôt sur le revenu)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Note : cette variable est définie à l'échelle du mois pour être en cohérence avec les variables qu'elle remplace
                (à savoir revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        '''
        year = period.this_year
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', year)
        f2dc = foyer_fiscal('f2dc', year)
        f2fu = foyer_fiscal('f2fu', year)
        f2ts = foyer_fiscal('f2ts', year)
        f2tr = foyer_fiscal('f2tr', year)
        f2tt = foyer_fiscal('f2tt', year)
        f2go = foyer_fiscal('f2go', year)

        return (assurance_vie_pfu_ir + f2dc + f2fu + f2ts + f2tr + f2tt + f2go) / 12


class plus_values_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Plus-values soumises au prélèvement forfaitaire unique (partie impôt sur le revenu)'
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000036377422/'
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        f3sb = foyer_fiscal('f3sb', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3va = foyer_fiscal('f3va', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3tj = foyer_fiscal('f3tj', period)

        return f3sb + max_(0, f3ua - f3va) + f3vg + f3tj

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        f3sb = foyer_fiscal('f3sb', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3va = foyer_fiscal('f3va', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3tk = foyer_fiscal('f3tk', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3an = foyer_fiscal('f3an', period)

        return f3sb + max_(0, f3ua - f3va) + f3vg + max_(0, f3tj - f3tk) + f3vt + f3an


class prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu (hors assurance-vie, épargne solidaire et produits venant des états non-coopératifs)"
    reference = [
        'Article 28 de la Loi n° 2017-1837 du 30 décembre 2017 de finances pour 2018 (modifie art. 125 A, 125-0 A, 200 A et art. 117 quater du CGI)',
        'https://www.legifrance.gouv.fr/affichTexteArticle.do?idArticle=LEGIARTI000036377422&cidTexte=JORFTEXT000036339197'
        ]
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        P = parameters(period).taxation_capital.prelevement_forfaitaire.partir_2018

        # Revenus des valeurs et capitaux mobiliers hors assurance-vie et hors produits d'épargne solidaire ou des états non-coopératifs
        #   Note : Les revenus d'assurance-vie, de l'épargne solidaire et des produits des états non-coopératifs ont été ajoutés dans les variables f2ee et f2dh (cf. docstring de ces varables pour une explication), d'où le fait qu'on soustrait ici ces variables de revenus_capitaux_prelevement_forfaitaire_unique_ir
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', period)
        produit_epargne_solidaire = foyer_fiscal('produit_epargne_solidaire', period)
        produit_etats_non_cooperatif = foyer_fiscal('produit_etats_non_cooperatif', period)
        revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs = max_(
            0,
            revenus_capitaux_prelevement_forfaitaire_unique_ir
            - assurance_vie_pfu_ir
            - produit_epargne_solidaire
            - produit_etats_non_cooperatif
            )

        # Intérêts des PEL et CEL, hors intérêts des PEL de plus de 12 ans, qui sont déclarés dans la déclaration de revenus (attention, on ne connait pas le formulaire 2019 des revenus 2018 au moment de faire ce code)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018_i = foyer_fiscal.members('interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018', period)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018 = foyer_fiscal.sum(interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018_i)
        interets_compte_epargne_logement_ouvert_a_partir_de_2018_i = foyer_fiscal.members('interets_compte_epargne_logement_ouvert_a_partir_de_2018', period)
        interets_compte_epargne_logement_ouvert_a_partir_de_2018 = foyer_fiscal.sum(interets_compte_epargne_logement_ouvert_a_partir_de_2018_i)

        # Plus-values
        plus_values_prelevement_forfaitaire_unique_ir = foyer_fiscal('plus_values_prelevement_forfaitaire_unique_ir', period)

        assiette_pfu_hors_assurance_vie = (
            revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs
            + interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018
            + interets_compte_epargne_logement_ouvert_a_partir_de_2018
            + plus_values_prelevement_forfaitaire_unique_ir
            )

        return -assiette_pfu_hors_assurance_vie * P.taux_prelevement_forfaitaire_rev_capital_eligibles_pfu_interets_dividendes_etc


class prelevement_forfaitaire_unique_ir_sur_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu sur l'assurance-vie"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        P1_taux = parameters(period).taxation_capital.prelevement_forfaitaire.partir_2018.taux_prelevement_forfaitaire_rev_capital_eligibles_pfu_interets_dividendes_etc
        P1_taux_reduit_av = parameters(period).taxation_capital.prelevement_forfaitaire.partir_2018.taux_prelevement_produits_assurance_vie_non_eligibles_prelevement_forfaitaire_unique
        P2 = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2zz = foyer_fiscal('f2zz', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)

        abattement_residuel = max_(P2.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses) - f2ch, 0)
        abattement_residuel2 = max_(abattement_residuel - f2vv, 0)
        pfu_ir_sur_assurance_vie = -(
            (f2zz * P1_taux)
            + (max_(f2vv - abattement_residuel, 0) * P1_taux_reduit_av)
            + (max_(f2ww - abattement_residuel2, 0) * P1_taux)
            )

        return pfu_ir_sur_assurance_vie


class prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs = foyer_fiscal('prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs', period)
        prelevement_forfaitaire_unique_ir_sur_assurance_vie = foyer_fiscal('prelevement_forfaitaire_unique_ir_sur_assurance_vie', period)

        return (
            prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs
            + prelevement_forfaitaire_unique_ir_sur_assurance_vie
            )
