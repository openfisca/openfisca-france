import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)

# Calcul de la partie du prélèvement forfaitaire unique (PFU) associé à l'impôt sur le revenu
# (le reste étant associé aux prélèvements sociaux)


class f2op(Variable):
    cerfa_field = '2OP'
    value_type = bool
    entity = FoyerFiscal
    label = 'Le foyer fiscal choisit l imposition au barème plutôt que le pfu si il coche la case 2op'
    definition_period = YEAR


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
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f2zz = foyer_fiscal('f2zz', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)

        result = where(imposition_au_bareme, 0, f2zz + f2vv + f2ww)

        return result


class revenus_capitaux_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus des valeurs et capitaux mobiliers soumis au prélèvement forfaitaire unique (partie impôt sur le revenu)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    unit = 'currency'

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Note : cette variable est définie à l'échelle du mois pour être en cohérence avec les variables qu'elle remplace
                (à savoir revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        '''
        year = period.this_year
        imposition_au_bareme = foyer_fiscal('f2op', year)
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', year)
        f2dc = foyer_fiscal('f2dc', year)
        f2fu = foyer_fiscal('f2fu', year)
        f2ts = foyer_fiscal('f2ts', year)
        f2tr = foyer_fiscal('f2tr', year)
        f2tt = foyer_fiscal('f2tt', year)
        f2go = foyer_fiscal('f2go', year)

        result = where(imposition_au_bareme, 0, assurance_vie_pfu_ir + f2dc + f2fu + f2ts + f2tr + f2tt + f2go)

        return result / 12

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Note : cette variable est définie à l'échelle du mois pour être en cohérence avec les variables qu'elle remplace
                (à savoir revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        Brochure pratique revenus 2019 page 123 et 340: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2020/accueil.htm
        Nouvelle variable 'Intérêts imposables des obligations remboursables en actions détenues dans le PEA-PME' (2tq) qui est éligible au pfu. Ces revenus étaient comptés dans la variable 2tr auparavant.
        '''
        year = period.this_year
        imposition_au_bareme = foyer_fiscal('f2op', year)
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', year)
        f2dc = foyer_fiscal('f2dc', year)
        f2fu = foyer_fiscal('f2fu', year)
        f2ts = foyer_fiscal('f2ts', year)
        f2tr = foyer_fiscal('f2tr', year)
        f2tt = foyer_fiscal('f2tt', year)
        f2go = foyer_fiscal('f2go', year)
        f2tq = foyer_fiscal('f2tq', year)

        result = where(imposition_au_bareme, 0, assurance_vie_pfu_ir + f2dc + f2fu + f2ts + f2tr + f2tt + f2go + f2tq)

        return result / 12

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Note : cette variable est définie à l'échelle du mois pour être en cohérence avec les variables qu'elle remplace
                (à savoir revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)

        Nouvelle variable 'Produits des plans d’épargne retraite – sortie en capital' (2tz) qui est éligible au pfu. Ces revenus étaient comptés dans la variable 2tr auparavant.
        Source: Brochure pratique revenus 2020 pages 119, 132 et 364: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2021/accueil.htm

        A compter de l’imposition des revenus de 2020, le montant des revenus 2GO est multiplié par un coefficient de 1,25 pour le calcul de l’impôt sur le revenu quelles que
        soient les modalités d’imposition de ces revenus (prélèvement forfaitaire unique de 12,8% ou option pour le barème progressif). Jusqu'en 2019, ce coefficient ne s'appliquait qu'en
        cas d'option pour le barème progressif.
        Sources:
            - Brochure pratique revenus 2020 page 130: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2021/accueil.htm
            - Brochure pratique revenus 2019 page 120: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2020/accueil.htm
        '''
        year = period.this_year
        imposition_au_bareme = foyer_fiscal('f2op', year)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', year)
        f2dc = foyer_fiscal('f2dc', year)
        f2fu = foyer_fiscal('f2fu', year)
        f2ts = foyer_fiscal('f2ts', year)
        f2tr = foyer_fiscal('f2tr', year)
        f2tt = foyer_fiscal('f2tt', year)
        f2go = foyer_fiscal('f2go', year)
        f2tq = foyer_fiscal('f2tq', year)
        f2tz = foyer_fiscal('f2tz', year)

        result = where(imposition_au_bareme, 0, assurance_vie_pfu_ir + f2dc + f2fu + f2ts + f2tr + f2tt + f2go * P.majoration_revenus_reputes_distribues + f2tq + f2tz)

        return result / 12


class plus_values_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Plus-values soumises au prélèvement forfaitaire unique (partie impôt sur le revenu)'
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000036377422/'
    definition_period = YEAR
    unit = 'currency'

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f3sb = foyer_fiscal('f3sb', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3va = foyer_fiscal('f3va', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3tj = foyer_fiscal('f3tj', period)

        result = where(imposition_au_bareme, 0, f3sb + max_(0, f3ua - f3va) + f3vg + f3tj)

        return result

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f3sb = foyer_fiscal('f3sb', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3va = foyer_fiscal('f3va', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3tk = foyer_fiscal('f3tk', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3an = foyer_fiscal('f3an', period)  # Actifs numériques toujours soumis au pfu, pas d'option d'imposition au barème

        pre_result = where(imposition_au_bareme, 0, f3sb + max_(0, f3ua - f3va) + f3vg + max_(0, f3tj - f3tk) + f3vt)

        return f3an + pre_result


class prelevement_forfaitaire_unique_ir_hors_assurance_vie(Variable):
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

        # Revenus des valeurs et capitaux mobiliers hors assurance-vie
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', period)
        revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie = (
            revenus_capitaux_prelevement_forfaitaire_unique_ir
            - assurance_vie_pfu_ir
            )

        # Plus-values
        plus_values_prelevement_forfaitaire_unique_ir = foyer_fiscal('plus_values_prelevement_forfaitaire_unique_ir', period)

        assiette_pfu_hors_assurance_vie = (
            revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie
            + plus_values_prelevement_forfaitaire_unique_ir
            )

        return assiette_pfu_hors_assurance_vie * P.taux_prelevement_forfaitaire_rev_capital_eligibles_pfu_interets_dividendes_etc


class prelevement_forfaitaire_unique_ir_sur_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu sur l'assurance-vie"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)
        jeune_veuf = foyer_fiscal('jeune_veuf', period)

        parameters_taux = parameters(period).taxation_capital.prelevement_forfaitaire.partir_2018.taux_prelevement_forfaitaire_rev_capital_eligibles_pfu_interets_dividendes_etc
        parameters_taux_reduit_av = parameters(period).taxation_capital.prelevement_forfaitaire.partir_2018.taux_prelevement_produits_assurance_vie_non_eligibles_prelevement_forfaitaire_unique
        parameters_rvcm = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm
        abattement_assurance_vie = parameters_rvcm.produits_assurances_vies_assimiles.abattement_couple * maries_ou_pacses + parameters_rvcm.produits_assurances_vies_assimiles.abattement_celib * (celibataire_ou_divorce | veuf | jeune_veuf)

        imposition_au_bareme = foyer_fiscal('f2op', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2zz = foyer_fiscal('f2zz', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)

        abattement_residuel = max_(abattement_assurance_vie - f2ch, 0)
        abattement_residuel2 = max_(abattement_residuel - f2vv, 0)
        pfu_ir_sur_assurance_vie = where(imposition_au_bareme, 0,
            (f2zz * parameters_taux)
            + (max_(f2vv - abattement_residuel, 0) * parameters_taux_reduit_av)
            # Ce calcul avec le taux réduit ne semble pas prendre en compte le montant maximal des versements qui est de 150 000 euros et semble disponible dans ce paramètre : seuil_primes_applique_eligibilite_produits_assurance_vie_prelevement_forfaitaire_unique
            + (max_(f2ww - abattement_residuel2, 0) * parameters_taux)
            )

        return pfu_ir_sur_assurance_vie


class prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        prelevement_forfaitaire_unique_ir_hors_assurance_vie = foyer_fiscal('prelevement_forfaitaire_unique_ir_hors_assurance_vie', period)
        prelevement_forfaitaire_unique_ir_sur_assurance_vie = foyer_fiscal('prelevement_forfaitaire_unique_ir_sur_assurance_vie', period)

        return (
            prelevement_forfaitaire_unique_ir_hors_assurance_vie
            + prelevement_forfaitaire_unique_ir_sur_assurance_vie
            )
