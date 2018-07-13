class assurance_vie_pl_non_anonyme_plus8ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 8 ans pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR

class assurance_vie_pl_non_anonyme_plus6ans_avant1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée d'au moins 6 ans pour les contrats souscrits précédemment, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR

class assurance_vie_pl_non_anonyme_moins4ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de moins de 4 ans, pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR

class assurance_vie_pl_non_anonyme_4_8_ans_depuis1990(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie d'une durée de 4 à 8 ans, pour les contrats souscrits depuis le 1er janvier 1990, et que le bénéficiaire décide de soumettre au prélèvement libératoire"
    definition_period = YEAR

class assurance_vie_pl_anonyme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits des bons ou contrats de capitalisation et d'assurance vie lorsque le bénéficiaire ne révèle pas son identité et son domicile fiscal, et qu'il décide de soumettre ces produits au prélèvement libératoire"
    definition_period = YEAR

class produit_epargne_solidaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produit d'épargne solidaire"
    definition_period = YEAR

class produit_etats_non_cooperatif(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits de placement à revenus fixe ou de contrats de capitalisation et d'assurance-vie versés à un bénéficiaire résidant dans un état non-coopératif"
    definition_period = YEAR

class prelevement_forfaitaire_liberatoire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prelèvement forfaitaire libératoire sur les revenus du capital"
    reference = "art. 125-0 A du Code Général des Impôts"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Prelèvement forfaitaire libératoire (PFL) sur les revenus du capital
        Notes :
          (1) On ne prend en compte le PFL qu'à partir de 2013. Or, il existait avant.
              Il était codé sous la variable imp_lib, mais avec des erreurs
              (application d'un unique taux à la case 2EE). On ne rperend pas tout.
          (2) Cette variable ne comprend pas la taxation forfaitaire à 24% associée
              à la base f2fa, qui est prise en compte via la variable tax_rvcm_forfaitaire,
              qui est incluse dans irpp. Cette taxaiton à 24% est certes forfaitaire,
              mais apparemment pas à la source. Elle serait calculée au moment de l'irpp,
              d'où mle fait de l'inclure dans la variable IRPP.
        '''
        ... Doit-on donner une date de fin à cette formule, en fonction de la nature de la réforme du PFU ?

        assurance_vie_pl_non_anonyme_plus8ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_plus8ans_depuis1990', period)
        assurance_vie_pl_non_anonyme_plus6ans_avant1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_plus6ans_avant1990', period)
        assurance_vie_pl_non_anonyme_moins4ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_moins4ans_depuis1990', period)
        assurance_vie_pl_non_anonyme_4_8_ans_depuis1990 = foyer_fiscal('assurance_vie_pl_non_anonyme_4_8_ans_depuis1990', period)
        assurance_vie_pl_anonyme = foyer_fiscal('assurance_vie_pl_anonyme', period)
        produit_epargne_solidaire = foyer_fiscal('produit_epargne_solidaire', period)
        produit_etats_non_cooperatif = foyer_fiscal('produit_etats_non_cooperatif', period)

        param_pfl_av = parameters(period).taxation_capital.pfl_av
        param_pfl = parameters(period).taxation_capital.pfl

        pfl = (
            (param_pfl_av.8_ans_et_plus_pour_les_produits_acquis_apres_le_01_01_1998_avec_abattement_sur_l_ir_5
            * assurance_vie_pl_non_anonyme_plus8ans_depuis1990)
            + (param_pfl_av.6_ans_et_plus_pour_les_produits_acquis_apres_le_01_01_1998_avec_abattement_sur_l_ir_5
            * assurance_vie_pl_non_anonyme_plus6ans_avant1990)
            + (param_pfl_av.moins_de_4_ans
            * assurance_vie_pl_non_anonyme_moins4ans_depuis1990)
            + (param_pfl_av.4_a_8_ans
            * assurance_vie_pl_non_anonyme_4_8_ans_depuis1990)
            + (param_pfl_av.avec_anonymat
            * assurance_vie_pl_anonyme)
            + (param_pfl.produits_epargne_solidaire_partage
            * produit_epargne_solidaire)
            + (param_pfl.produits_vers_etats_non_cooperatifs
            * produit_etats_non_cooperatif)
            )

        return pfl


