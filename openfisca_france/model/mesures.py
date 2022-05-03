from openfisca_france.model.base import *


class unites_consommation(Variable):
    value_type = float
    entity = Menage
    label = "Unités de consommation du ménage, selon l'échelle de l'INSEE"
    reference = 'https://insee.fr/fr/metadonnees/definition/c1802'
    definition_period = YEAR

    def formula(menage, period, parameters):
        age_individu = menage.members('age', period.first_month)
        uc_individu = 0.5 * (age_individu >= 14) + 0.3 * (age_individu < 14)
        return 0.5 + menage.sum(uc_individu)  # 1 uc pour la personne de référence


class type_menage(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Menage
    label = 'Type de ménage'
    definition_period = YEAR

    def formula(menage, period):
        '''
        Type de menage
        TODO: prendre les enfants du ménage et non ceux de la famille
        Attention : des erreurs peuvent subsister quand ménage et famille ne coincide pas (cas des ménages complexes)
        '''

        af_nbenf = menage.personne_de_reference.famille('af_nbenf', period.first_month)
        isole = not_(menage.personne_de_reference.famille('en_couple', period.first_month))

        return (
            0 * (isole * (af_nbenf == 0))  # Célibataire
            + 1 * (not_(isole) * (af_nbenf == 0))  # Couple sans enfants
            + 2 * (not_(isole) * (af_nbenf == 1))  # Couple un enfant
            + 3 * (not_(isole) * (af_nbenf == 2))  # Couple deux enfants
            + 4 * (not_(isole) * (af_nbenf == 3))  # Couple trois enfants et plus
            + 5 * (isole * (af_nbenf == 1))  # Famille monoparentale un enfant
            + 6 * (isole * (af_nbenf == 2))  # Famille monoparentale deux enfants
            + 7 * (isole * (af_nbenf == 3))
            )  # Famille monoparentale trois enfants et plus


class revenu_disponible(Variable):
    value_type = float
    entity = Menage
    label = 'Revenu disponible du ménage'
    reference = 'http://fr.wikipedia.org/wiki/Revenu_disponible'
    definition_period = YEAR

    def formula(menage, period, parameters):
        pensions_nettes_i = menage.members('pensions_nettes', period)
        revenus_nets_du_capital_i = menage.members('revenus_nets_du_capital', period)
        revenus_nets_du_travail_i = menage.members('revenus_nets_du_travail', period)
        pensions_nettes = menage.sum(pensions_nettes_i)
        revenus_nets_du_capital = menage.sum(revenus_nets_du_capital_i)
        revenus_nets_du_travail = menage.sum(revenus_nets_du_travail_i)

        impots_directs = menage('impots_directs', period)

        # On prend en compte les PPE touchés par un foyer fiscal dont le déclarant principal est dans le ménage
        ppe_i = menage.members.foyer_fiscal('ppe', period)  # PPE du foyer fiscal auquel appartient chaque membre du ménage
        ppe = menage.sum(ppe_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # On somme seulement pour les déclarants principaux

        # On prend en compte les prestations sociales touchées par une famille dont le demandeur est dans le ménage
        prestations_sociales_i = menage.members.famille('prestations_sociales', period)  # PF de la famille auquel appartient chaque membre du ménage
        prestations_sociales = menage.sum(prestations_sociales_i, role = Famille.DEMANDEUR)  # On somme seulement pour les demandeurs

        return (
            revenus_nets_du_travail
            + impots_directs
            + pensions_nettes
            + ppe
            + prestations_sociales
            + revenus_nets_du_capital
            )


class niveau_de_vie(Variable):
    value_type = float
    entity = Menage
    label = 'Niveau de vie du ménage'
    definition_period = YEAR

    def formula(menage, period):
        revenu_disponible = menage('revenu_disponible', period)
        uc = menage('unites_consommation', period)
        return revenu_disponible / uc


class revenus_nets_du_travail(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus nets du travail (salariés et non salariés)'
    reference = 'http://fr.wikipedia.org/wiki/Revenu_du_travail'
    definition_period = YEAR

    def formula(individu, period):
        # Salariés
        salaire_net = individu('salaire_net', period, options = [ADD])
        # Non salariés
        revenu_non_salarie = individu('rpns_imposables', period, options = [ADD])
        csg_imposable_non_salarie = individu('csg_imposable_non_salarie', period)
        crds_non_salarie = individu('crds_non_salarie', period)
        revenu_non_salarie_net = (
            revenu_non_salarie
            + csg_imposable_non_salarie
            + crds_non_salarie
            )
        return salaire_net + revenu_non_salarie_net


class pensions_nettes(Variable):
    value_type = float
    entity = Individu
    label = 'Pensions et revenus de remplacement'
    reference = 'http://fr.wikipedia.org/wiki/Rente'
    definition_period = YEAR

    def formula(individu, period):
        chomage_net = individu('chomage_net', period, options = [ADD])
        retraite_nette = individu('retraite_nette', period, options = [ADD])
        pensions_alimentaires_percues = individu('pensions_alimentaires_percues', period, options = [ADD])
        pensions_invalidite = individu('pensions_invalidite', period, options = [ADD])

        # Revenus du foyer fiscal, que l'on projette uniquement sur le 1er déclarant
        foyer_fiscal = individu.foyer_fiscal
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        rente_viagere_titre_onereux = foyer_fiscal('rente_viagere_titre_onereux', period, options = [ADD])
        pen_foyer_fiscal = pensions_alimentaires_versees + rente_viagere_titre_onereux
        pen_foyer_fiscal_projetees = pen_foyer_fiscal * (individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL))

        return (
            chomage_net
            + retraite_nette
            + pensions_alimentaires_percues
            + pensions_invalidite
            + pen_foyer_fiscal_projetees
            )


class plus_values_base_large(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Montant des plus-values utilisé pour le montant total de revenus du capital'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        La CSG sur plus-values n'est pas calculée sur toutes les plus-values : cf. docstring de la variable v1_assiette_csg_plus_values
        Donc, il existe certaines plus-values pour lesquelles on calcul l'impôt sur le revenu (imposition au barème ou forfaitaire),
        mais pour lesquelles on n'a pas de prélèvements sociaux
        Cette variable est l'assiette de plus-values pour lesquelles au moins un prélèvement est calculé. On l'utilise dans le
        calcul du revenu disponible, afin de n'oublier aucun revenu. Elle vaut la somme de assiette_csg_plus_values et rfr_plus_values_hors_rni,
        où l'on enlève les cases communes entre ces deux variables, et où l'on ajoute les variables présentes dans 'revenu_categoriel_plus_values', mais pas présente
        dans assiette_csg_plus_values
        Attention, on n'ajoute pas en revanche 3SA car de notre compréhension, il s'agit de plus-values qui avaient bénéficié
        de reports d'imposition, report qui a expiré. Ce qui veut dire que ces revenus n'avaient pas été imposés lors de leur
        réalisation (ils le sont maintenant), mais avaient été comptés dans le RFR. Donc, il s'agit de revenus qui ne font pas parti
        du revenu courant de cette année.
        Attention : pour les variables de 'revenu_categoriel_plus_values' ajoutées, elles peuvent représenter des montants nets, alors qu'il faudrait le brut. Améliorer ce point
        '''

        v1_assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)
        v2_rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)

        f3vg = foyer_fiscal('f3vg', period)
        f3we = foyer_fiscal('f3we', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3vt = foyer_fiscal('f3vt', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        intersection_v1_v2 = f3vg + f3we + f3vz + rpns_pvce + f3vt

        return v1_assiette_csg_plus_values + v2_rfr_plus_values_hors_rni - intersection_v1_v2

    def formula_2013_01_01(foyer_fiscal, period):
        '''
        Cf. docstring période précédente
        '''

        v1_assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)
        v2_rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)

        f3we = foyer_fiscal('f3we', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3vl = foyer_fiscal('f3vl', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3vt = foyer_fiscal('f3vt', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        intersection_v1_v2 = f3we + f3vz + rpns_pvce + f3vt
        ajouts_de_rev_cat_pv = f3vl + f3wb

        return v1_assiette_csg_plus_values + v2_rfr_plus_values_hors_rni - intersection_v1_v2 + ajouts_de_rev_cat_pv

    def formula_2014_01_01(foyer_fiscal, period):
        '''
        Cf. docstring période précédente
        '''

        v1_assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)
        v2_rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)

        f3we = foyer_fiscal('f3we', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3vt = foyer_fiscal('f3vt', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        intersection_v1_v2 = f3we + f3vz + rpns_pvce + f3vt
        ajouts_de_rev_cat_pv = f3wb

        return v1_assiette_csg_plus_values + v2_rfr_plus_values_hors_rni - intersection_v1_v2 + ajouts_de_rev_cat_pv

    def formula_2017_01_01(foyer_fiscal, period):
        '''
        Cf. docstring période précédente
        '''

        v1_assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)
        v2_rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)

        f3we = foyer_fiscal('f3we', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3pi = foyer_fiscal('f3pi', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        intersection_v1_v2 = f3we + f3vz + rpns_pvce + f3vt + f3pi
        ajouts_de_rev_cat_pv = f3wb

        return v1_assiette_csg_plus_values + v2_rfr_plus_values_hors_rni - intersection_v1_v2 + ajouts_de_rev_cat_pv

    def formula_2018_01_01(foyer_fiscal, period):
        '''
        Cf. docstring période précédente
        Pour 2018 et 2019, assiette_csg_plus_values est inclus dans rfr_plus_values_hors_rni
        '''
        f3wb = foyer_fiscal('f3wb', period)

        rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)
        ajouts_de_rev_cat_pv = f3wb

        return rfr_plus_values_hors_rni + ajouts_de_rev_cat_pv


class revenus_nets_du_capital(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus du capital nets de prélèvements sociaux'
    reference = 'http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital'
    definition_period = YEAR

    def formula(individu, period):
        '''
        Attention : les formules des calculs des prélèvements sociaux sur revenus du capital avant 2013 n'ont pas été verifiées et sont susceptibles de contenir des erreurs
        Note : On part de l'assiette CSG sur les revenus du capital (avec base élargie pour les plus-values), à partir de
        laquelle on fait les deux modifications ci-dessous :
            (1) On enlève les rentes viagères à titre onéreux, qui sont dans cette
                assiette CSG, mais sont déjà dans la variable pensions_nettes pour
                le calcul du revenu disponible. De plus, le concept de rente foncière
                retenu dans cette assiette était le montant après abattement, n'ayant
                pas de fondement économique
                Par conséquent, vu qu'on retranche la CSG sur les revenus du capital,
                qui contient dans sa base les rentes viagèes à titre onéreux, cette variable
                peut être négative
            (2) On change de concept de plus-values (cf. docstring de la variable plus_values_base_large pour mieux comprendre)
        Cette variable est définie au niveau individuel : on projette les revenus du foyer fiscal
        sur le déclarant principal
        '''

        foyer_fiscal = individu.foyer_fiscal
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)
        plus_values_base_large = foyer_fiscal('plus_values_base_large', period)
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)

        revenus_du_capital_cap_avant_prelevements_sociaux = (
            assiette_csg_revenus_capital
            - assiette_csg_plus_values
            + plus_values_base_large
            - rente_viagere_titre_onereux_net
            )

        prelevements_sociaux_revenus_capital = foyer_fiscal('prelevements_sociaux_revenus_capital', period)

        revenus_foyer_fiscal = (
            revenus_du_capital_cap_avant_prelevements_sociaux
            + prelevements_sociaux_revenus_capital
            )
        revenus_foyer_fiscal_projetes = revenus_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return revenus_foyer_fiscal_projetes


class revenus_fonciers_bruts_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Revenus fonciers du ménage après déficits mais avant abattements'
    definition_period = YEAR

    def formula_2013_01_01(menage, period):
        '''
        Il s'agit des bénéfices (ou déficits) fonciers de l'année courante,
        sans abattement. Il s'agit d'une notion davantage économique.
        Cette variable n'est relative qu'à l'activité foncière de l'année.
        C'est pourquoi on ne prend pas en compte la case 4BD, qui
        correspond à des déficits des années antérieures non encore imputés
        au titre de l'impôt sur le revenu
        Formule vérifiée pour les feuilles d'impôts à partir des revenus 2013,
        d'où le fait que la formule commence à cette date-là
        '''
        f4ba_i = menage.members.foyer_fiscal('f4ba', period)
        f4be_i = menage.members.foyer_fiscal('f4be', period)
        f4bb_i = menage.members.foyer_fiscal('f4bb', period)
        f4bc_i = menage.members.foyer_fiscal('f4bc', period)

        f4ba = menage.sum(f4ba_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        f4be = menage.sum(f4be_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        f4bb = menage.sum(f4bb_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        f4bc = menage.sum(f4bc_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        return f4ba + f4be - f4bb - f4bc


class revenus_travail_super_bruts_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Revenus du travail super bruts du ménage'
    definition_period = YEAR

    def formula(menage, period):
        '''
        Revenus du travail super bruts du ménage :
        avant CSG-CRDS, cotisations salariales et patronales
        '''
        salaire_net_i = menage.members('salaire_net', period, options = [ADD])
        rpns_i = menage.members('rpns_imposables', period)
        csg_imposable_salaire_i = menage.members('csg_imposable_salaire', period, options = [ADD])
        csg_deductible_salaire_i = menage.members('csg_deductible_salaire', period, options = [ADD])
        csg_deductible_non_salarie_i = menage.members('csg_deductible_non_salarie', period, options = [ADD])
        crds_salaire_i = menage.members('crds_salaire', period, options = [ADD])
        cotisations_employeur_i = menage.members('cotisations_employeur', period, options = [ADD])
        cotisations_salariales_i = menage.members('cotisations_salariales', period, options = [ADD])
        cotisations_non_salarie_i = menage.members('cotisations_non_salarie', period, options = [ADD])

        salaire_net = menage.sum(salaire_net_i)
        rpns = menage.sum(rpns_i)
        csg_imposable_salaire = menage.sum(csg_imposable_salaire_i)
        csg_deductible_salaire = menage.sum(csg_deductible_salaire_i)
        csg_deductible_non_salarie = menage.sum(csg_deductible_non_salarie_i)
        crds_salaire = menage.sum(crds_salaire_i)
        cotisations_employeur = menage.sum(cotisations_employeur_i)
        cotisations_salariales = menage.sum(cotisations_salariales_i)
        cotisations_non_salarie = menage.sum(cotisations_non_salarie_i)

        return (
            salaire_net
            + rpns
            - cotisations_employeur  # On veut ajouter le montant de cotisations. Vu que ce montant est négatif, on met un "moins". Idem pour les autres items ci-dessous
            - cotisations_salariales  # On veut ajouter le montant de cotisations. Vu que ce montant est négatif, on met un "moins". Idem pour les autres items ci-dessous
            - cotisations_non_salarie
            - csg_imposable_salaire
            - csg_deductible_salaire
            - csg_deductible_non_salarie
            - crds_salaire
            )


class revenus_remplacement_pensions_bruts_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Revenus de remplacement et pensions bruts du ménage'
    definition_period = YEAR

    def formula(menage, period):
        '''
        Revenus de remplacement et pensions bruts du ménage : avant CSG et CRDS
        '''
        pensions_nettes_i = menage.members('pensions_nettes', period)
        casa_i = menage.members('casa', period, options = [ADD])
        csg_imposable_chomage_i = menage.members('csg_imposable_chomage', period, options = [ADD])
        csg_deductible_chomage_i = menage.members('csg_deductible_chomage', period, options = [ADD])
        csg_imposable_retraite_i = menage.members('csg_imposable_retraite', period, options = [ADD])
        csg_deductible_retraite_i = menage.members('csg_deductible_retraite', period, options = [ADD])
        crds_chomage_i = menage.members('crds_chomage', period, options = [ADD])
        crds_retraite_i = menage.members('crds_retraite', period, options = [ADD])

        pensions_nettes = menage.sum(pensions_nettes_i)
        casa = menage.sum(casa_i)
        csg_imposable_chomage = menage.sum(csg_imposable_chomage_i)
        csg_deductible_chomage = menage.sum(csg_deductible_chomage_i)
        csg_imposable_retraite = menage.sum(csg_imposable_retraite_i)
        csg_deductible_retraite = menage.sum(csg_deductible_retraite_i)
        crds_chomage = menage.sum(crds_chomage_i)
        crds_retraite = menage.sum(crds_retraite_i)

        return (
            + pensions_nettes
            - casa
            - csg_imposable_chomage  # On veut ajouter le montant de cotisations. Vu que ce montant est négatif, on met un "moins". Idem pour les autres items ci-dessous
            - csg_deductible_chomage
            - csg_imposable_retraite
            - csg_deductible_retraite
            - crds_chomage
            - crds_retraite
            )


class revenus_capitaux_mobiliers_plus_values_bruts_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Revenus bruts des capitaux mobiliers et plus-values du ménage'
    definition_period = YEAR

    def formula(menage, period):
        '''
        Revenus bruts des capitaux mobiliers et plus-values du ménage :
        avant tout abattement et prélèvement social
        '''

        revenus_capitaux_prelevement_forfaitaire_unique_ir_i = menage.members.foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        revenus_capitaux_prelevement_forfaitaire_unique_ir = menage.sum(revenus_capitaux_prelevement_forfaitaire_unique_ir_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        revenus_capitaux_prelevement_bareme_i = menage.members.foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        revenus_capitaux_prelevement_bareme = menage.sum(revenus_capitaux_prelevement_bareme_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        revenus_capitaux_prelevement_liberatoire_i = menage.members.foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        revenus_capitaux_prelevement_liberatoire = menage.sum(revenus_capitaux_prelevement_liberatoire_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        interets_pel_moins_12_ans_cel_i = menage.members('interets_pel_moins_12_ans_cel', period)
        interets_pel_moins_12_ans_cel = menage.sum(interets_pel_moins_12_ans_cel_i)
        assurance_vie_ps_exoneree_irpp_pl_i = menage.members.foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)
        assurance_vie_ps_exoneree_irpp_pl = menage.sum(assurance_vie_ps_exoneree_irpp_pl_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        plus_values_base_large_i = menage.members.foyer_fiscal('plus_values_base_large', period)
        plus_values_base_large = menage.sum(plus_values_base_large_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + revenus_capitaux_prelevement_bareme
            + revenus_capitaux_prelevement_liberatoire
            + interets_pel_moins_12_ans_cel
            + assurance_vie_ps_exoneree_irpp_pl
            + plus_values_base_large
            )


class revenus_super_bruts_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Revenus super bruts du ménage'
    definition_period = YEAR

    def formula(menage, period):

        revenus_travail_super_bruts_menage = menage('revenus_travail_super_bruts_menage', period)
        revenus_remplacement_pensions_bruts_menage = menage('revenus_remplacement_pensions_bruts_menage', period)
        revenus_fonciers_bruts_menage = menage('revenus_fonciers_bruts_menage', period)
        revenus_capitaux_mobiliers_plus_values_bruts_menage = menage('revenus_capitaux_mobiliers_plus_values_bruts_menage', period)

        return (
            revenus_travail_super_bruts_menage
            + revenus_remplacement_pensions_bruts_menage
            + revenus_fonciers_bruts_menage
            + revenus_capitaux_mobiliers_plus_values_bruts_menage
            )


class prelevements_sociaux_menage(Variable):
    value_type = float
    entity = Menage
    label = 'Prélèvements sociaux du ménage (tous revenus, hors prestations)'
    definition_period = YEAR

    def formula(menage, period):
        csg_i = menage.members('csg', period, options = [ADD])
        csg = menage.sum(csg_i)
        crds_hors_presta_i = menage.members('crds_hors_prestations', period, options = [ADD])
        crds_hors_prestations = menage.sum(crds_hors_presta_i)

        prelevements_sociaux_revenus_capital_hors_csg_crds_i = menage.members.foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period, options = [ADD])
        prelevements_sociaux_revenus_capital_hors_csg_crds = menage.sum(prelevements_sociaux_revenus_capital_hors_csg_crds_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            + csg
            + crds_hors_prestations
            + prelevements_sociaux_revenus_capital_hors_csg_crds
            )


class prestations_sociales(Variable):
    value_type = float
    entity = Famille
    label = 'Prestations sociales'
    reference = 'http://fr.wikipedia.org/wiki/Prestation_sociale'
    definition_period = YEAR

    def formula(famille, period):
        '''
        Prestations sociales
        '''
        prestations_familiales = famille('prestations_familiales', period)
        minima_sociaux = famille('minima_sociaux', period)
        aides_logement = famille('aides_logement', period)
        reduction_loyer_solidarite = famille('reduction_loyer_solidarite', period, options = [ADD])
        aide_exceptionnelle_covid = famille('covid_aide_exceptionnelle_famille_montant', period, options =[ADD])
        fse_i = famille.members('covid_aide_exceptionnelle_tpe_montant', period, options = [ADD])
        fse = famille.sum(fse_i)

        return prestations_familiales + minima_sociaux + aides_logement + reduction_loyer_solidarite + aide_exceptionnelle_covid + fse


class prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = 'Prestations familiales'
    reference = 'http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html'
    definition_period = YEAR

    def formula(famille, period):
        af = famille('af', period, options = [ADD])
        cf = famille('cf', period, options = [ADD])
        ars = famille('ars', period)
        aeeh = famille('aeeh', period, options = [ADD])
        aes = famille('aes', period, options = [ADD])
        paje = famille('paje', period, options = [ADD])
        asf = famille('asf', period, options = [ADD])
        crds_pfam = famille('crds_pfam', period)

        return af + cf + ars + aeeh + aes + paje + asf + crds_pfam


class minimum_vieillesse(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Minimum vieillesse (ASI + ASPA)'
    definition_period = YEAR

    def formula(famille, period):
        return famille.sum(famille.members('asi', period, options = [ADD])) + famille('aspa', period, options = [ADD])


class minima_sociaux(Variable):
    value_type = float
    entity = Famille
    label = 'Minima sociaux'
    reference = 'http://fr.wikipedia.org/wiki/Minima_sociaux'
    definition_period = YEAR

    def formula(famille, period, parameters):
        aah_i = famille.members('aah', period, options = [ADD])
        caah_i = famille.members('caah', period, options = [ADD])
        aah = famille.sum(aah_i)
        caah = famille.sum(caah_i)
        aefa = famille('aefa', period)
        api = famille('api', period, options = [ADD])
        ass_i = famille.members('ass', period, options = [ADD])
        ass = famille.sum(ass_i)
        minimum_vieillesse = famille('minimum_vieillesse', period, options = [ADD])
        # Certaines réformes ayant des effets de bords nécessitent que le rsa soit calculé avant la ppa
        rsa = famille('rsa', period, options = [ADD])
        ppa = famille('ppa', period, options = [ADD])
        psa = famille('psa', period, options = [ADD])
        crds_mini = famille('crds_mini', period, options = [ADD])
        garantie_jeunes_i = famille.members('garantie_jeunes', period, options = [ADD])
        garantie_jeunes = famille.sum(garantie_jeunes_i)

        return aah + caah + minimum_vieillesse + rsa + aefa + api + ass + psa + ppa + crds_mini + garantie_jeunes


class aides_logement(Variable):
    value_type = float
    entity = Famille
    label = 'Aides logement nettes'
    reference = 'http://vosdroits.service-public.fr/particuliers/N20360.xhtml'
    definition_period = YEAR

    def formula(famille, period):
        return famille('aide_logement', period, options = [ADD])


class irpp_economique(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Notion économique de l'IRPP"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Cette variable d'IRPP comptabilise dans les montants
        d'imposition les acomptes qui, dans la déclaration fiscale, sont considérés comme des crédits
        d'impôt. Ajouter ces acomptes au montant "administratif" d'impôt correspond donc au "véritable impôt"
        payé en totalité, alors que la variable 'irpp' correspond à une notion administrative.
        Exemple :
        Certains revenus du capital sont soumis à un prélèvement forfaitaire à la source non libératoire,
        faisant office d'acompte. Puis, l'impôt au barème sur ces revenus est calculé, et confronté à l'acompte.
        Cet acompte, est en case 2CK, et considéré comme un crédit d'impôt. Retrancher de l'impôt au barème ce
        crédit permet d'obtenir l'impôt dû suite à la déclaration de revenus, qui correspond à la variable 'irpp'.
        Cette notion est administrative. L'impôt total payé correspond à cette notion administrative, augmentée des acomptes.
        '''
        irpp = foyer_fiscal('irpp', period)
        acomptes_ir = foyer_fiscal('acomptes_ir', period)

        return irpp - acomptes_ir  # Car par convention, irpp est un montant négatif et acomptes_ir un montant positif


class impots_directs(Variable):
    value_type = float
    entity = Menage
    label = 'Impôts directs'
    reference = 'http://fr.wikipedia.org/wiki/Imp%C3%B4t_direct'
    definition_period = YEAR

    def formula(menage, period, parameters):
        '''
        Pour les impôts définis au niveau du foyer fiscal :
        on prend en compte l'impôt des foyers fiscaux dont le déclarant principal est dans le ménage
        '''
        taxe_habitation = menage('taxe_habitation', period)

        irpp_economique_i = menage.members.foyer_fiscal('irpp_economique', period)
        irpp_economique = menage.sum(irpp_economique_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        prelevement_forfaitaire_liberatoire_i = menage.members.foyer_fiscal('prelevement_forfaitaire_liberatoire', period)
        prelevement_forfaitaire_liberatoire = menage.sum(prelevement_forfaitaire_liberatoire_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        prelevement_forfaitaire_unique_ir_i = menage.members.foyer_fiscal('prelevement_forfaitaire_unique_ir', period)
        prelevement_forfaitaire_unique_ir = menage.sum(prelevement_forfaitaire_unique_ir_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        # On comptabilise ir_pv_immo ici directement, et non pas dans la variable 'irpp', car administrativement, cet impôt n'est pas dans l'irpp, et n'est déclaré dans le formulaire 2042C que pour calculer le revenu fiscal de référence. On colle à la définition administrative, afin d'avoir une variable 'irpp' qui soit comparable à l'IR du simulateur en ligne de la DGFiP
        ir_pv_immo_i = menage.members.foyer_fiscal('ir_pv_immo', period)
        ir_pv_immo = menage.sum(ir_pv_immo_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period)
        isf_ifi = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            taxe_habitation
            + irpp_economique
            + prelevement_forfaitaire_liberatoire
            + prelevement_forfaitaire_unique_ir
            + ir_pv_immo
            + isf_ifi
            )
