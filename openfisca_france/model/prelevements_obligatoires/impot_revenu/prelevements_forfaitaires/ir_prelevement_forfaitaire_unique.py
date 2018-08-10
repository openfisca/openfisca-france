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

class revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus des valeurs et capitaux mobiliers soumis au prélèvement forfaitaire unique (partie impôt sur le revenu), hors assurance-vie"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Les frais et charges déductibles de la case 2CA ne sont déductibles que si imposition au barème, d'où l'absence de cette case dans cette formualre
        Cf. https://www.impots.gouv.fr/portail/particulier/questions/les-frais-engages-sur-mes-valeurs-mobilieres-sont-ils-deductibles
        '''
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2tt = foyer_fiscal('f2tt', period)
        f2fa = foyer_fiscal('f2fa', period)
        f2go = foyer_fiscal('f2go', period)
        f2tu = foyer_fiscal('f2tu', period)
        majoration_revenus_reputes_distribues = parameters(period).impot_revenu.rvcm.majoration_revenus_reputes_distribues

        return f2dc + f2fu + f2tr + max_(0, f2tt - f2tu) + f2fa + f2go * majoration_revenus_reputes_distribues

class assurance_vie_prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie soumis au prélèvement forfaitaire unique (partie impôt sur le revenu)"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
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
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie', period)
        assurance_vie_prelevement_forfaitaire_unique_ir = foyer_fiscal('assurance_vie_prelevement_forfaitaire_unique_ir', period)

        return revenus_capitaux_prelevement_forfaitaire_unique_ir_hors_assurance_vie + assurance_vie_prelevement_forfaitaire_unique_ir




class prelevement_forfaitaire_unique_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Partie du prélèvement forfaitaire unique associée à l'impôt sur le revenu"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        ... TO CODE



