# -*- coding: utf-8 -*-

from __future__ import division
import logging
from openfisca_france.model.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)

########################################################################################################################
########################################################################################################################
########## Calcul de la partie du prélèvement forfaitaire unique (PFU) associé à l'impôt sur le revenu       ###########
########## (le reste étant associé aux prélèvements sociaux) ###########################################################
########################################################################################################################
########################################################################################################################

class assurance_vie_pfu_ir_plus8ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 8 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_plus6ans_avant1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 6 ans pour les contrats souscrits avant le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_moins4ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de moins de 4 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_4_8_ans_1990_19970926(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée entre 4 et 8 ans pour les contrats souscrits entre le 1er janvier 1990 et le 26 septembre 1997, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie de plus de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie entre 4 et 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie de moins de 4 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées avant le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie de moins de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées après le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie de plus de 8 ans pour les contrats souscrits après le 26 septembre 1997, dont le produits sont associés aux primes versées après le 27 septembre 2017, et que le bénéficiaire décide de soumettre au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

class assurance_vie_pfu_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie soumis au prélèvement forfaitaire unique au titre de l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period):

        assurance_vie_pfu_ir_plus8ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_1990_19970926', period)
        assurance_vie_pfu_ir_plus6ans_avant1990 = foyer_fiscal('assurance_vie_pfu_ir_plus6ans_avant1990', period)
        assurance_vie_pfu_ir_moins4ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_moins4ans_1990_19970926', period)
        assurance_vie_pfu_ir_4_8_ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_4_8_ans_1990_19970926', period)
        assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927 = foyer_fiscal('assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927', period)
        assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927', period)

        return (
            assurance_vie_pfu_ir_plus8ans_1990_19970926
            + assurance_vie_pfu_ir_plus6ans_avant1990
            + assurance_vie_pfu_ir_moins4ans_1990_19970926
            + assurance_vie_pfu_ir_4_8_ans_1990_19970926
            + assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927
            + assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927
            + assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927
            + assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927
            + assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927
            )

class revenus_capitaux_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus des valeurs et capitaux mobiliers soumis au prélèvement forfaitaire unique (partie impôt sur le revenu)"
    definition_period = MONTH

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Les frais et charges déductibles de la case 2CA ne sont déductibles que si imposition au barème, d'où l'absence de cette case dans cette formualre
        Cf. https://www.impots.gouv.fr/portail/particulier/questions/les-frais-engages-sur-mes-valeurs-mobilieres-sont-ils-deductibles
        Note : on laisse les cases de la déclaration 2042 associées à l'assurance-vie, car en attendant d'avoir le formulaire de l'impôt 2019 sur revenus 2018,
        on réinjecte les montants des variables désaggrégées d'assurance-vie dans ces cases, afin de garder constante la structure des cases
        Notes : cette variable est définie à l'échelle du mois pour être en cohérence avec les variables qu'elle remplace
                (à savoir revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        '''
        year = period.this_year
        f2dh = foyer_fiscal('f2dh', year)
        f2ee = foyer_fiscal('f2ee', year)
        f2dc = foyer_fiscal('f2dc', year)
        f2fu = foyer_fiscal('f2fu', year)
        f2ch = foyer_fiscal('f2ch', year)
        f2ts = foyer_fiscal('f2ts', year)
        f2tr = foyer_fiscal('f2tr', year)
        f2tt = foyer_fiscal('f2tt', year)
        f2fa = foyer_fiscal('f2fa', year)
        f2go = foyer_fiscal('f2go', year)
        majoration_revenus_reputes_distribues = parameters(period).impot_revenu.rvcm.majoration_revenus_reputes_distribues

        return (f2dh + f2ee + f2dc + f2fu + f2ch + f2ts + f2tr + f2tt + f2fa + f2go * majoration_revenus_reputes_distribues) / 12

class plus_values_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Plus-values soumises au prélèvement forfaitaire unique (partie impôt sur le revenu)"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Cette variable fusionne le périmètre des plus-values des anciennes variables de plus_values-values présentes
        dans taxation_plus_values_hors_bareme et dans rev_cat_pv, mais en adaptant les assiettes au PFU
        (notamment, pour les revenus de rev_cat_pv, passage des montants nets à bruts)
        '''
        f3sa = foyer_fiscal('f3sa', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3wb = foyer_fiscal('f3wb', period)

        # Ici, on reprend le champ des plus-values de la variable taxation_plus_values_hors_bareme
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vd_i = foyer_fiscal.members('f3vd', period)
        f3vi_i = foyer_fiscal.members('f3vi', period)
        f3vf_i = foyer_fiscal.members('f3vf', period)
        f3vd = foyer_fiscal.sum(f3vd_i)
        f3vi = foyer_fiscal.sum(f3vi_i)
        f3vf = foyer_fiscal.sum(f3vf_i)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)


        # Notes :
            # 3sg + 3sl : correspond aux abattements associés aux cases 3vg et 3ua (donc, on considère les montants bruts).
            #             En revanche, on n'enlève pas l'abattement fixe en 3va, car il est maintenu, y compris si le contribuable
            #             choisit le PFU. Les conditions on été légèrement modifiées, mais on ne va pas dans ce détail-là. Cf par exemple https://taj-strategie.fr/plf-2018-lecture-definitive-fiscalite-personnes
            # 3WE n'est pas compté, car normalement, il n'est pas dans la base du PFU... A checker ?
            # 3WB : il s'agit des plus-values et créances sans sursis de paiement (pour transfert du domicile fiscal hors de France)
            #       après abattements. Normalement, il faudrait prendre la mesure avant abattement. Les montants avant abattements sont case 3WD. Mais cette case
            #       comprend, en plus des plus-values imposables avant abbattement, celles bénéficiant d'un report d'imposition. HYP : on prend les montants nets.
            # 3WI et 3WJ : les conditions liées au report d'imposition de l'art. 150-0 B ter du CGI ont été remaniées à la marge.
            #              On ne prend pas en compte ces remaniements. Situation résumée dans https://taj-strategie.fr/plf-2018-lecture-definitive-fiscalite-personnes
        return f3sa + f3vg + f3ua + f3sg + f3sl + f3wb + f3sj + f3sk + f3vm + f3vt + f3vd + f3vi + f3vf + f3wi + f3wj + rpns_pvce




class prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu (hors assurance-vie, épargne solidaire et produits venant des états non-coopératifs)"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        P = parameters(period).impot_revenu.prelevement_forfaitaire_unique_ir

        # Revenus des valeurs et capitaux mobiliers hors assurance-vie et hors produits d'épargne solidaire ou des états non-coopératifs
        #   Note : Les revenus d'assurance-vie, de l'épargne solidaire et des produits des états non-coopératifs ont été ajoutés dans les variables f2ee et f2dh (cf. docstring de ces varables pour une explication), d'où le fait qu'on soustrait ici ces variables de revenus_capitaux_prelevement_forfaitaire_unique_ir
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        assurance_vie_pfu_ir = foyer_fiscal('assurance_vie_pfu_ir', period)
        produit_epargne_solidaire = foyer_fiscal('produit_epargne_solidaire', period)
        produit_etats_non_cooperatif = foyer_fiscal('produit_etats_non_cooperatif', period)
        revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs = (
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

        return -assiette_pfu_hors_assurance_vie * P.taux

class prelevement_forfaitaire_unique_ir_sur_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu sur l'assurance-vie"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        P1 = parameters(period).impot_revenu.prelevement_forfaitaire_unique_ir
        P2 = parameters(period).taxation_capital.pfl_av.bons_ou_contrats_de_capitalisation_et_placements_de_meme_nature_assurance_vie_lors_du_denouement_du_contrat
        rvcm = parameters(period).impot_revenu.rvcm

        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        assurance_vie_pfu_ir_plus8ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_1990_19970926', period)
        assurance_vie_pfu_ir_plus6ans_avant1990 = foyer_fiscal('assurance_vie_pfu_ir_plus6ans_avant1990', period)
        assurance_vie_pfu_ir_moins4ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_moins4ans_1990_19970926', period)
        assurance_vie_pfu_ir_4_8_ans_1990_19970926 = foyer_fiscal('assurance_vie_pfu_ir_4_8_ans_1990_19970926', period)
        assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927 = foyer_fiscal('assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927', period)
        assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927 = foyer_fiscal('assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927', period)
        assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927 = foyer_fiscal('assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927', period)

        # Nouveau régime de taxation (produits au titre des primes versées à compter du 26 septembre 1997, pour les contrats souscrits à partir du 26 septembre 1997)
        assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927_apres_abt = max_(assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927 - rvcm.abat_assvie * (1 + maries_ou_pacses), 0)
        pfu_ir_av_nouveau_regime = -(
            (assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927 * P1.taux)
            + (min_(assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927_apres_abt, P1.seuil_taux_reduit_av) * P1.taux_reduit_av)
            + (max_(assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927_apres_abt - P1.seuil_taux_reduit_av, 0) * P1.taux)
            )

        # Ancien régime de taxation (autres produits que ceux mentionnés ci-dessus)
        p_contrat_age_sup_apres_abt = (
            max_(assurance_vie_pfu_ir_plus8ans_1990_19970926 - rvcm.abat_assvie * (1 + maries_ou_pacses), 0)
            + max_(assurance_vie_pfu_ir_plus6ans_avant1990 - rvcm.abat_assvie * (1 + maries_ou_pacses), 0)
            + max_(assurance_vie_pfu_ir_plus8ans_19970926_primes_avant_20170927 - rvcm.abat_assvie * (1 + maries_ou_pacses), 0)
        )
        p_contrat_age_mid = assurance_vie_pfu_ir_4_8_ans_1990_19970926 + assurance_vie_pfu_ir_4_8_ans_19970926_primes_avant_20170927
        p_contrat_age_low = assurance_vie_pfu_ir_moins4ans_1990_19970926 + assurance_vie_pfu_ir_moins4ans_19970926_primes_avant_20170927
        pfu_ir_av_ancien_regime = -(
            (p_contrat_age_low * P2.souscrits_apres_le_1_1_90_et_le_pour_une_duree_de.duree_moins_de_4_ans)
            + (p_contrat_age_mid * P2.souscrits_apres_le_1_1_90_et_le_pour_une_duree_de.duree_4_a_8_ans)
            + (p_contrat_age_sup_apres_abt * P2.souscrits_apres_le_1_1_90_et_le_pour_une_duree_de.duree_8_ans_et_plus_pour_les_produits_acquis_apres_le_01_01_1998_avec_abattement_sur_l_ir_5)
            )

        return pfu_ir_av_nouveau_regime + pfu_ir_av_ancien_regime

class prelevement_forfaitaire_unique_ir_epargne_solidaire_etats_non_cooperatifs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu sur les produits d'épargne solidaire et les produits venant des états non-coopératifs"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        produit_epargne_solidaire = foyer_fiscal('produit_epargne_solidaire', period)
        produit_etats_non_cooperatif = foyer_fiscal('produit_etats_non_cooperatif', period)

        param_pfl = parameters(period).taxation_capital.pfl

        montant = -(
            (param_pfl.produits_epargne_solidaire_partage * produit_epargne_solidaire)
            + (param_pfl.produits_vers_etats_non_cooperatifs * produit_etats_non_cooperatif)
            )

        return montant


class prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs = foyer_fiscal('prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs', period)
        prelevement_forfaitaire_unique_ir_sur_assurance_vie = foyer_fiscal('prelevement_forfaitaire_unique_ir_sur_assurance_vie', period)
        prelevement_forfaitaire_unique_ir_epargne_solidaire_etats_non_cooperatifs = foyer_fiscal('prelevement_forfaitaire_unique_ir_epargne_solidaire_etats_non_cooperatifs', period)

        return (
            prelevement_forfaitaire_unique_ir_hors_assurance_vie_epargne_solidaire_etats_non_cooperatifs
            + prelevement_forfaitaire_unique_ir_sur_assurance_vie
            + prelevement_forfaitaire_unique_ir_epargne_solidaire_etats_non_cooperatifs
            )

