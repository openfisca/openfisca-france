import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)


class assurance_vie_pl_non_anonyme_plus8ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 8 ans pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR


class assurance_vie_pl_non_anonyme_plus6ans_avant1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 6 ans pour les contrats souscrits précédemment, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR


class assurance_vie_pl_non_anonyme_moins4ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de moins de 4 ans, pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR


class assurance_vie_pl_non_anonyme_4_8_ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de 4 à 8 ans, pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR


class assurance_vie_pl_anonyme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits des bons ou contrats de capitalisation et d'assurance vie lorsque le bénéficiaire ne révèle pas son identité et son domicile fiscal, et qu'il décide de soumettre ces produits au prélèvement libératoire"
    definition_period = YEAR


class prelevement_forfaitaire_liberatoire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prelèvement forfaitaire libératoire sur les revenus du capital'
    reference = [
        'Article 125-0 A du Code général des impôts',
        'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006308140'
        ]
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        f2dh = foyer_fiscal('f2dh', period)
        f2ee = foyer_fiscal('f2ee', period)
        param_pfl_av = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_assurance_vie.bons_contrats_placements
        param_pfl = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_taux_fixe

        return -(
            f2dh * param_pfl_av.apres_le_1_1_90.duree_8_ans_et_produits_apres_1998
            + f2ee * param_pfl.autres_produits_de_placement_a_revenu_fixe.courus_entre_le_1_1_95_et_apres
            )

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        f2da = foyer_fiscal('f2da', period)
        f2dh = foyer_fiscal('f2dh', period)
        f2ee = foyer_fiscal('f2ee', period)
        param_pfl_av = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_assurance_vie.bons_contrats_placements
        param_pfl = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_taux_fixe

        return -(
            f2da * param_pfl.dividendes
            + f2ee * param_pfl.autres_produits_de_placement_a_revenu_fixe.courus_entre_le_1_1_95_et_apres
            + f2dh * param_pfl_av.apres_le_1_1_90.duree_8_ans_et_produits_apres_1998
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Prelèvement forfaitaire libératoire (PFL) sur les revenus du capital
        Notes :
          (1) La formule avant 2013 provient de l'ancienne variable 'imp_lib'.
              A priori, cette ancienne formule n'est pas entièrement correcte (application d'un taux unique à la case 2EE par exemple) et mériterait d'être corrigée.
          (2) Cette variable ne comprend pas la taxation forfaitaire à 24% associée
              à la base f2fa, qui est prise en compte via la variable tax_rvcm_forfaitaire,
              qui est incluse dans impot_revenu_restant_a_payer. Cette taxaiton à 24% est certes forfaitaire,
              mais apparemment pas à la source. Elle serait calculée au moment de l'impot_revenu_restant_a_payer,
              d'où le fait de l'inclure dans la variable impot_revenu_restant_a_payer.
        '''

        assurance_vie_pl_non_anonyme_plus8ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_plus8ans_depuis1990', period)
        assurance_vie_pl_non_anonyme_plus6ans_avant1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_plus6ans_avant1990', period)
        assurance_vie_pl_non_anonyme_moins4ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_moins4ans_depuis1990', period)
        assurance_vie_pl_non_anonyme_4_8_ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_4_8_ans_depuis1990', period)
        assurance_vie_pl_anonyme = foyer_fiscal('assurance_vie_pl_anonyme', period)
        produit_epargne_solidaire = foyer_fiscal('produit_epargne_solidaire', period)
        produit_etats_non_cooperatif = foyer_fiscal('produit_etats_non_cooperatif', period)

        param_pfl_av = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_assurance_vie.bons_contrats_placements
        param_pfl = parameters(period).taxation_capital.prelevement_forfaitaire.liberatoire_taux_fixe

        pfl = -(
            (param_pfl_av.apres_le_1_1_90.duree_8_ans_et_produits_apres_1998
            * assurance_vie_pl_non_anonyme_plus8ans_depuis1990)
            + (param_pfl_av.entre_1_1_83_et_31_12_89.six_ans_produits_apres_98
            * assurance_vie_pl_non_anonyme_plus6ans_avant1990)
            + (param_pfl_av.apres_le_1_1_90.duree_moins_de_4_ans
            * assurance_vie_pl_non_anonyme_moins4ans_depuis1990)
            + (param_pfl_av.apres_le_1_1_90.duree_4_a_8_ans
            * assurance_vie_pl_non_anonyme_4_8_ans_depuis1990)
            + (param_pfl_av.avec_anonymat
            * assurance_vie_pl_anonyme)
            + (param_pfl.produits_epargne_solidaire_partage
            * produit_epargne_solidaire)
            + (param_pfl_av.produits_vers_etats_non_cooperatifs
            * produit_etats_non_cooperatif)
            )

        return pfl
