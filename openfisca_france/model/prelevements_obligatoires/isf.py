from openfisca_france.model.base import *

# Variables apparaissant dans la feuille de déclaration de patrimoine soumis à l'ISF

# Immeubles bâtis


class b1ab(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Valeur de la résidence principale avant abattement'
    definition_period = YEAR


class b1ac(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Valeur des autres immeubles avant abattement'
    definition_period = YEAR


# non bâtis
class b1bc(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Immeubles non bâtis : bois, fôrets et parts de groupements forestiers'
    definition_period = YEAR


class b1be(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Immeubles non bâtis : biens ruraux loués à long termes'
    definition_period = YEAR


class b1bh(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers'
    definition_period = YEAR


class b1bk(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Immeubles non bâtis : autres biens'
    definition_period = YEAR


# droits sociaux- valeurs mobilières-liquidités- autres meubles
class b1cl(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Parts et actions détenues par les salariés et mandataires sociaux'
    definition_period = YEAR


class b1cb(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Parts et actions de sociétés avec engagement de conservation de 6 ans minimum'
    definition_period = YEAR


class b1cd(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité'
    definition_period = YEAR


class b1ce(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Autres valeurs mobilières'
    definition_period = YEAR


class b1cf(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Liquidités'
    definition_period = YEAR


class b1cg(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Autres biens meubles'
    definition_period = YEAR


class b1co(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Autres biens meubles : contrats d'assurance-vie"
    definition_period = YEAR


#    b1ch
#    b1ci
#    b1cj
#    b1ck


# passifs et autres réductions
class b2gh(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Total du passif et autres déductions'
    definition_period = YEAR


# réductions
class b2mt(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements directs dans une société'
    definition_period = YEAR


class b2ne(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements directs dans une société'
    definition_period = YEAR


class b2mv(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements par sociétés interposées, holdings'
    definition_period = YEAR


class b2nf(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements par sociétés interposées, holdings'
    definition_period = YEAR


class b2mx(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements par le biais de FIP'
    definition_period = YEAR


class b2na(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Réductions pour investissements par le biais de FCPI ou FCPR'
    definition_period = YEAR


class b2nc(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Réductions pour dons à certains organismes d'intérêt général"
    definition_period = YEAR


# montant impôt acquitté hors de France
class b4rs(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Montant de l'impôt acquitté hors de France"
    definition_period = YEAR


# BOUCLIER FISCAL

class rev_or(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class rev_exo(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class tax_fonc(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Taxe foncière'
    definition_period = YEAR


class restit_imp(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class etr(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period


# Calcul de l'impôt de solidarité sur la fortune

# 1 ACTIF BRUT

class isf_ifi_imm_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Base de l'ISF-IFI sur l'immobilier bâti"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        b1ab = foyer_fiscal('b1ab', period)
        b1ac = foyer_fiscal('b1ac', period)
        reduc_exo = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.reduc_exo

        return (1 - reduc_exo.abattement_residence_principale) * b1ab + b1ac

    def formula(foyer_fiscal, period, parameters):
        b1ab = foyer_fiscal('b1ab', period)
        b1ac = foyer_fiscal('b1ac', period)
        reduc_exo = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_exo

        return (1 - reduc_exo.abattement_residence_principale) * b1ab + b1ac


class isf_ifi_imm_non_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Base de l'ISF-IFI sur l'immobilier non-bâti"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        b1bc = foyer_fiscal('b1bc', period)
        b1be = foyer_fiscal('b1be', period)
        b1bh = foyer_fiscal('b1bh', period)
        b1bk = foyer_fiscal('b1bk', period)
        non_bati = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.forfait_mobilier.non_bati

        # forêts
        b1bd = b1bc * non_bati.taux_bois_forets
        # bien ruraux loués à long terme
        b1bf = min_(b1be, non_bati.seuil) * non_bati.taux_biens_ruraux
        b1bg = max_(b1be - non_bati.seuil, 0) * non_bati.taux_forestier_agricole
        # part de groupements forestiers- agricoles fonciers
        b1bi = min_(b1bh, non_bati.seuil) * non_bati.taux_biens_ruraux
        b1bj = max_(b1bh - non_bati.seuil, 0) * non_bati.taux_forestier_agricole
        return b1bd + b1bf + b1bg + b1bi + b1bj + b1bk

    def formula(foyer_fiscal, period, parameters):
        b1bc = foyer_fiscal('b1bc', period)
        b1be = foyer_fiscal('b1be', period)
        b1bh = foyer_fiscal('b1bh', period)
        b1bk = foyer_fiscal('b1bk', period)
        non_bati = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.forfait_mobilier.non_bati

        # forêts
        b1bd = b1bc * non_bati.taux_bois_forets
        # bien ruraux loués à long terme
        b1bf = min_(b1be, non_bati.seuil) * non_bati.taux_biens_ruraux
        b1bg = max_(b1be - non_bati.seuil, 0) * non_bati.taux_forestier_agricole
        # part de groupements forestiers- agricoles fonciers
        b1bi = min_(b1bh, non_bati.seuil) * non_bati.taux_biens_ruraux
        b1bj = max_(b1bh - non_bati.seuil, 0) * non_bati.taux_forestier_agricole
        return b1bd + b1bf + b1bg + b1bi + b1bj + b1bk

# droits sociaux- valeurs mobilières- liquidités- autres meubles


class isf_actions_sal(Variable):  # non présent en 2005
    value_type = float
    entity = FoyerFiscal
    label = 'isf_actions_sal'
    definition_period = YEAR
    end = '2017-12-31'

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Parts ou actions détenues par les salariés et mandataires sociaux
        '''
        b1cl = foyer_fiscal('b1cl', period)
        droits_sociaux = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.droits_sociaux

        return b1cl * droits_sociaux.taux_salaries_mandataires_sociaux


class isf_droits_sociaux(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'isf_droits_sociaux'
    definition_period = YEAR
    end = '2017-12-31'

    def formula(foyer_fiscal, period, parameters):
        isf_actions_sal = foyer_fiscal('isf_actions_sal', period)
        b1cb = foyer_fiscal('b1cb', period)
        b1cd = foyer_fiscal('b1cd', period)
        b1ce = foyer_fiscal('b1ce', period)
        b1cf = foyer_fiscal('b1cf', period)
        b1cg = foyer_fiscal('b1cg', period)
        droits_sociaux = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.droits_sociaux

        b1cc = b1cb * droits_sociaux.taux_actions_conservees_6_ans
        return isf_actions_sal + b1cc + b1cd + b1ce + b1cf + b1cg


class assiette_isf_ifi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Assiette de l'ISF-IFI"
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        # TODO: Gérer les trois option meubles meublants
        isf_ifi_imm_bati = foyer_fiscal('isf_ifi_imm_bati', period)
        isf_ifi_imm_non_bati = foyer_fiscal('isf_ifi_imm_non_bati', period)
        isf_droits_sociaux = foyer_fiscal('isf_droits_sociaux', period)
        b1cg = foyer_fiscal('b1cg', period)
        b2gh = foyer_fiscal('b2gh', period)
        forfait_mobilier = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.forfait_mobilier

        total = isf_ifi_imm_bati + isf_ifi_imm_non_bati + isf_droits_sociaux
        forf_mob = (b1cg != 0) * b1cg + (b1cg == 0) * total * forfait_mobilier.majoration_forfaitaire
        actif_brut = total + forf_mob
        return actif_brut - b2gh

    def formula_1989_01_01(foyer_fiscal, period, parameters):
        # TODO: Gérer les trois option meubles meublants
        isf_ifi_imm_bati = foyer_fiscal('isf_ifi_imm_bati', period)
        isf_ifi_imm_non_bati = foyer_fiscal('isf_ifi_imm_non_bati', period)
        isf_droits_sociaux = foyer_fiscal('isf_droits_sociaux', period)
        b1cg = foyer_fiscal('b1cg', period)
        b2gh = foyer_fiscal('b2gh', period)
        forfait_mobilier = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.forfait_mobilier

        total = isf_ifi_imm_bati + isf_ifi_imm_non_bati + isf_droits_sociaux
        forf_mob = (b1cg != 0) * b1cg + (b1cg == 0) * total * forfait_mobilier.majoration_forfaitaire
        actif_brut = total + forf_mob
        return actif_brut - b2gh

    def formula(foyer_fiscal, period, parameters):
        # TODO: Gérer les trois option meubles meublants
        isf_ifi_imm_bati = foyer_fiscal('isf_ifi_imm_bati', period)
        isf_ifi_imm_non_bati = foyer_fiscal('isf_ifi_imm_non_bati', period)
        isf_droits_sociaux = foyer_fiscal('isf_droits_sociaux', period)
        b1cg = foyer_fiscal('b1cg', period)
        b2gh = foyer_fiscal('b2gh', period)
        forfait_mobilier = parameters(period).taxation_capital.impot_grandes_fortunes_1982_1986.forfait_mobilier

        total = isf_ifi_imm_bati + isf_ifi_imm_non_bati + isf_droits_sociaux
        forf_mob = (b1cg != 0) * b1cg + (b1cg == 0) * total * forfait_mobilier.majoration_forfaitaire
        actif_brut = total + forf_mob
        return actif_brut - b2gh

# Calcul de l'impôt par application du barème


class isf_ifi_iai(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'ISF-IFI avant décote, réductions et plafonnement'
    definition_period = YEAR

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        assiette_isf_ifi = foyer_fiscal('assiette_isf_ifi', period)
        bareme = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.bareme.bareme
        return bareme.calc(assiette_isf_ifi)

    # TODO: Cette formule a seulement été vérifiée jusqu'au 2015-12-31
    def formula_2011_01_01(foyer_fiscal, period, parameters):
        assiette_isf_ifi = foyer_fiscal('assiette_isf_ifi', period)
        bareme = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.bareme.bareme
        assiette_isf_ifi = (assiette_isf_ifi >= bareme.rates[1]) * assiette_isf_ifi
        return bareme.calc(assiette_isf_ifi)

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        assiette_isf_ifi = foyer_fiscal('assiette_isf_ifi', period)
        bareme = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.bareme.bareme
        return bareme.calc(assiette_isf_ifi)


class isf_ifi_avant_reduction(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'ISF-IFI avant réductions et plafonnement'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        isf_ifi_iai = foyer_fiscal('isf_ifi_iai', period)
        decote_isf_ifi = foyer_fiscal('decote_isf_ifi', period)

        return isf_ifi_iai - decote_isf_ifi


class isf_reduc_pac(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'isf_reduc_pac'
    end = '2012-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Réductions pour personnes à charges
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        nbH = foyer_fiscal('nbH', period)
        reduc_exo = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_exo

        return reduc_exo.reduction_enfant_charge * nb_pac + (reduc_exo.reduction_enfant_charge / 2) * nbH


class isf_inv_pme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'isf_inv_pme'
    definition_period = YEAR

    def formula_2008(foyer_fiscal, period, parameters):
        '''
        Réductions pour investissements dans les PME
        à partir de 2008!
        '''
        b2mt = foyer_fiscal('b2mt', period)
        b2ne = foyer_fiscal('b2ne', period)
        b2mv = foyer_fiscal('b2mv', period)
        b2nf = foyer_fiscal('b2nf', period)
        b2mx = foyer_fiscal('b2mx', period)
        b2na = foyer_fiscal('b2na', period)
        reduc_impot = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_impot
        taux_dons = reduc_impot.reduction_dons_certains_organismes_interet_general.taux
        taux_invest_direct = reduc_impot.reduction_investissements_capital_pme.taux_investissement_direct
        taux_fip_fci = reduc_impot.reduction_investissements_dans_fcpi_ou_fip_dans_pme.taux_investissement

        inv_dir_soc = b2mt * taux_dons + b2ne * taux_invest_direct
        holdings = b2mv * taux_dons + b2nf * taux_invest_direct
        fip = b2mx * taux_fip_fci
        fcpi = b2na * taux_fip_fci

        montant_reduc = holdings + fip + fcpi + inv_dir_soc
        plaf = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_impot.plafond_somme_trois_reductions_pme_fcip_fip_pme_dons

        return where(montant_reduc < plaf, montant_reduc, plaf)

    def formula_2018(foyer_fiscal, period, parameters):
        '''
        Réductions pour investissements dans les PME
        à partir de 2008!
        '''
        b2mt = foyer_fiscal('b2mt', period)
        b2ne = foyer_fiscal('b2ne', period)
        b2mv = foyer_fiscal('b2mv', period)
        b2nf = foyer_fiscal('b2nf', period)
        b2mx = foyer_fiscal('b2mx', period)
        b2na = foyer_fiscal('b2na', period)
        reduc_impot = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.reduc_impot
        taux_dons = reduc_impot.reduction_dons_certains_organismes_interet_general.taux
        taux_invest_direct = reduc_impot.reduction_investissements_capital_pme.taux_investissement_direct
        taux_fip_fci = reduc_impot.reduction_investissements_dans_fcpi_ou_fip_dans_pme.taux_investissement

        inv_dir_soc = b2mt * taux_dons + b2ne * taux_invest_direct
        holdings = b2mv * taux_dons + b2nf * taux_invest_direct
        fip = b2mx * taux_fip_fci
        fcpi = b2na * taux_fip_fci

        montant_reduc = holdings + fip + fcpi + inv_dir_soc
        plaf = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.reduc_impot.plafond_somme_trois_reductions_pme_fcip_fip_pme_dons

        return where(montant_reduc < plaf, montant_reduc, plaf)


class isf_org_int_gen(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'isf_org_int_gen'
    definition_period = YEAR

    def formula_2008(foyer_fiscal, period, parameters):
        b2nc = foyer_fiscal('b2nc', period)
        P = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_impot.reduction_dons_certains_organismes_interet_general
        montant = b2nc * P.taux

        return where(montant < P.limite_reduction, montant, P.limite_reduction)

    def formula_2018(foyer_fiscal, period, parameters):
        b2nc = foyer_fiscal('b2nc', period)
        P = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.reduc_impot.reduction_dons_certains_organismes_interet_general
        montant = b2nc * P.taux

        return where(montant < P.limite_reduction, montant, P.limite_reduction)


class isf_ifi_avant_plaf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'ISF-IFI avant plafonnement'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        isf_ifi_avant_reduction = foyer_fiscal('isf_ifi_avant_reduction', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)

        return max_(0, isf_ifi_avant_reduction - isf_reduc_pac)

    def formula_2008(foyer_fiscal, period, parameters):
        isf_ifi_avant_reduction = foyer_fiscal('isf_ifi_avant_reduction', period)
        isf_inv_pme = foyer_fiscal('isf_inv_pme', period)
        isf_org_int_gen = foyer_fiscal('isf_org_int_gen', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)

        return max_(0, isf_ifi_avant_reduction - (isf_inv_pme + isf_org_int_gen) - isf_reduc_pac)

    def formula_2009(foyer_fiscal, period, parameters):
        isf_ifi_avant_reduction = foyer_fiscal('isf_ifi_avant_reduction', period)
        isf_inv_pme = foyer_fiscal('isf_inv_pme', period)
        isf_org_int_gen = foyer_fiscal('isf_org_int_gen', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)
        borne_max = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.reduc_impot.plafond_somme_trois_reductions_pme_fcip_fip_pme_dons

        return max_(0, isf_ifi_avant_reduction - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)

    def formula_2018(foyer_fiscal, period, parameters):
        isf_ifi_avant_reduction = foyer_fiscal('isf_ifi_avant_reduction', period)
        isf_inv_pme = foyer_fiscal('isf_inv_pme', period)
        isf_org_int_gen = foyer_fiscal('isf_org_int_gen', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)
        borne_max = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.reduc_impot.plafond_somme_trois_reductions_pme_fcip_fip_pme_dons

        return max_(0, isf_ifi_avant_reduction - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)


# # calcul du plafonnement ##

class rag(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus agricoles'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=BA&pageId=prof_ba&sfid=50'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Revenus agricoles
        '''
        frag_exon = individu('frag_exon', period)
        frag_impo = individu('frag_impo', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        arag_defi = individu('arag_defi', period)
        nrag_exon = individu('nrag_exon', period)
        nrag_impg = individu('nrag_impg', period)
        nrag_defi = individu('nrag_defi', period)
        nrag_ajag = individu('nrag_ajag', period)

        return (
            frag_exon + frag_impo
            + arag_exon + arag_impg - arag_defi
            + nrag_exon + nrag_impg - nrag_defi
            + nrag_ajag
            )

    def formula_2016_01_01(individu, period, parameters):
        '''
        Revenus agricoles
        '''
        mrag_exon = individu('mrag_exon', period)
        mrag_impo = individu('mrag_impo', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        arag_defi = individu('arag_defi', period)
        nrag_exon = individu('nrag_exon', period)
        nrag_impg = individu('nrag_impg', period)
        nrag_defi = individu('nrag_defi', period)
        nrag_ajag = individu('nrag_ajag', period)

        return (
            mrag_exon + mrag_impo
            + arag_exon + arag_impg - arag_defi
            + nrag_exon + nrag_impg - nrag_defi
            + nrag_ajag
            )


class ric(Variable):
    value_type = float
    entity = Individu
    label = 'Bénéfices industriels et commerciaux'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?pageId=prof_bic&espId=2&impot=BIC&sfid=50'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Bénéfices industriels et commerciaux
        '''
        mbic_exon = individu('mbic_exon', period)
        mbic_impv = individu('mbic_impv', period)
        mbic_imps = individu('mbic_imps', period)
        abic_exon = individu('abic_exon', period)
        nbic_exon = individu('nbic_exon', period)
        abic_impn = individu('abic_impn', period)
        nbic_impn = individu('nbic_impn', period)
        abic_imps = individu('abic_imps', period)
        nbic_imps = individu('nbic_imps', period)
        abic_defn = individu('abic_defn', period)
        nbic_defn = individu('nbic_defn', period)
        abic_defs = individu('abic_defs', period)
        nbic_defs = individu('nbic_defs', period)
        nbic_apch = individu('nbic_apch', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        zbic = (
            mbic_exon + mbic_impv + mbic_imps
            + abic_exon + nbic_exon
            + abic_impn + nbic_impn
            + abic_imps + nbic_imps
            + abic_defn - nbic_defn
            + abic_defs - nbic_defs
            + nbic_apch
            )

        cond = (mbic_impv > 0) & (mbic_imps == 0)
        taux = micro.microentreprise.regime_micro_bnc.marchandises.taux * cond + micro.microentreprise.regime_micro_bnc.services.taux * not_(cond)

        cbic = min_(
            mbic_impv + mbic_imps + mbic_exon,
            max_(
                micro.microentreprise.montant_minimum,
                round_(
                    mbic_impv * micro.microentreprise.regime_micro_bnc.marchandises.taux + mbic_imps * micro.microentreprise.regime_micro_bnc.services.taux + mbic_exon * taux
                    )
                )
            )
        return zbic - cbic


class rac(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus accessoires individuels'
    reference = 'http://vosdroits.service-public.fr/particuliers/F1225.xhtml'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Revenus accessoires individuels
        '''
        macc_exon = individu('macc_exon', period)
        macc_impv = individu('macc_impv', period)
        macc_imps = individu('macc_imps', period)
        aacc_exon = individu('aacc_exon', period)
        aacc_impn = individu('aacc_impn', period)
        aacc_imps = individu('aacc_imps', period)
        aacc_defn = individu('aacc_defn', period)
        aacc_defs = individu('aacc_defs', period)
        nacc_exon = individu('nacc_exon', period)
        nacc_impn = individu('nacc_impn', period)
        nacc_defn = individu('nacc_defn', period)
        alnp_imps = individu('alnp_imps', period)
        mncn_impo = individu('mncn_impo', period)
        cncn_bene = individu('cncn_bene', period)
        cncn_defi = individu('cncn_defi', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        zacc = (
            macc_exon + macc_impv + macc_imps
            + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs
            + nacc_exon + nacc_impn - nacc_defn - alnp_imps
            + mncn_impo + cncn_bene - cncn_defi
            )

    # TODO: aacc_imps aacc_defs
        cond = (macc_impv > 0) & (macc_imps == 0)
        taux = micro.microentreprise.regime_micro_bnc.marchandises.taux * cond + micro.microentreprise.regime_micro_bnc.services.taux * not_(cond)

        cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, max_(micro.microentreprise.montant_minimum, round_(
            macc_impv * micro.microentreprise.regime_micro_bnc.marchandises.taux
            + macc_imps * micro.microentreprise.regime_micro_bnc.services.taux + macc_exon * taux
            + mncn_impo * micro.microentreprise.regime_micro_bnc.taux)))

        return zacc - cacc


class rnc(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus non commerciaux individuels'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&pageId=prof_bnc&impot=BNC&sfid=50'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Revenus non commerciaux individuels
        '''
        mbnc_exon = individu('mbnc_exon', period)
        mbnc_impo = individu('mbnc_impo', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        abnc_impo = individu('abnc_impo', period)
        nbnc_impo = individu('nbnc_impo', period)
        abnc_defi = individu('abnc_defi', period)
        nbnc_defi = individu('nbnc_defi', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro.microentreprise

        zbnc = (
            mbnc_exon + mbnc_impo
            + abnc_exon + nbnc_exon
            + abnc_impo + nbnc_impo
            - abnc_defi - nbnc_defi
            )

        cbnc = min_(
            mbnc_exon + mbnc_impo,
            max_(
                micro.montant_minimum,
                round_((mbnc_exon + mbnc_impo) * micro.regime_micro_bnc.taux)
                )
            )

        return zbnc - cbnc

class total_impots_plafonnement_isf_ifi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Total des impôts dus au titre des revenus et produits (iai, contribution_exceptionnelle_hauts_revenus, prélèvements forfaitaires, prélèvements sociaux) + ISF et IFI. Utilisé pour calculer le montant du plafonnement de l'ISF et de l'IFI."
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        Voir le formulaire 2041-ISF-FCP
        https://www.impots.gouv.fr/portail/formulaire/2041-isf-fcp/fiche-de-calcul-du-plafonnement-isf
        Points à améliorer : impôts payés à l'étranger
        '''
        isf_ifi_avant_plaf = foyer_fiscal('isf_ifi_avant_plaf', period)
        irpp_economique = foyer_fiscal('irpp_economique', period)
        ir_pv_immo = foyer_fiscal('ir_pv_immo', period)
        crds_i = foyer_fiscal.members('crds', period)
        csg_i = foyer_fiscal.members('csg', period)
        crds = foyer_fiscal.sum(crds_i, role = FoyerFiscal.DECLARANT)
        csg = foyer_fiscal.sum(csg_i, role = FoyerFiscal.DECLARANT)
        prelevements_sociaux_revenus_capital_hors_csg_crds = foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period)

        return (
            isf_ifi_avant_plaf
            - irpp_economique
            - ir_pv_immo
            - crds
            - csg
            - prelevements_sociaux_revenus_capital_hors_csg_crds
            )


class revenus_et_produits_plafonnement_isf_ifi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenus et produits perçus, utilisés pour calculer le montant du plafonnement de l'ISF"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Voir le formulaire 2041-ISF-FCP
        https://www.impots.gouv.fr/portail/formulaire/2041-isf-fcp/fiche-de-calcul-du-plafonnement-isf
        Points à améliorer : revenus de l'étranger et revenus exonérés
        '''
        salcho_imp_i = foyer_fiscal.members('revenu_assimile_salaire_apres_abattements', period)
        pen_net_i = foyer_fiscal.members('revenu_assimile_pension_apres_abattements', period)
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)
        revenu_categoriel_foncier = foyer_fiscal('revenu_categoriel_foncier', period)
        ric_i = foyer_fiscal.members('ric', period)
        rag_i = foyer_fiscal.members('rag', period)
        rpns_exon_i = foyer_fiscal.members('rpns_exon', period)
        rpns_pvct_i = foyer_fiscal.members('rpns_pvct', period)
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])  # Existe à partir de 2018
        plus_values_base_large = foyer_fiscal('plus_values_base_large', period)
        assurance_vie_ps_exoneree_irpp_pl = foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)
        interets_pel_cel_non_soumis_IR_i = foyer_fiscal.members('interets_pel_cel_non_soumis_IR', period)
        livret_a_i = foyer_fiscal.members('livret_a', period.last_month)
        taux_livret_a = parameters(period).taxation_capital.epargne.livret_a.taux
        interets_livret_a_i = livret_a_i * taux_livret_a

        revenu_assimile_pension_apres_abattements = foyer_fiscal.sum(pen_net_i)
        rag = foyer_fiscal.sum(rag_i)
        ric = foyer_fiscal.sum(ric_i)
        rpns_exon = foyer_fiscal.sum(rpns_exon_i)
        rpns_pvct = foyer_fiscal.sum(rpns_pvct_i)
        revenu_assimile_salaire_apres_abattements = foyer_fiscal.sum(salcho_imp_i)
        interets_pel_cel_non_soumis_IR = foyer_fiscal.sum(interets_pel_cel_non_soumis_IR_i)
        interets_livret_a = foyer_fiscal.sum(interets_livret_a_i)

        montant = max_(
            0,
            revenu_assimile_salaire_apres_abattements
            + revenu_assimile_pension_apres_abattements
            + rente_viagere_titre_onereux_net
            + revenus_capitaux_prelevement_bareme
            + revenus_capitaux_prelevement_liberatoire
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + ric
            + rag
            + rpns_exon
            + rpns_pvct
            + revenu_categoriel_foncier
            + plus_values_base_large
            + assurance_vie_ps_exoneree_irpp_pl
            + interets_pel_cel_non_soumis_IR
            + interets_livret_a
            )

        return montant


class decote_isf_ifi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Décote de l'ISF-IFI"
    definition_period = YEAR

    def formula_2018(foyer_fiscal, period, parameters):
        assiette_isf_ifi = foyer_fiscal('assiette_isf_ifi', period)
        decote = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.decote

        elig = (assiette_isf_ifi >= decote.borne_inferieure_decote) & (assiette_isf_ifi <= decote.borne_superieure_decote)
        lb = decote.parametre_calcul_decote - decote.taux_decote * assiette_isf_ifi
        return lb * elig

    def formula_2013(foyer_fiscal, period, parameters):
        assiette_isf_ifi = foyer_fiscal('assiette_isf_ifi', period)
        decote = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.decote

        elig = (assiette_isf_ifi >= decote.borne_inferieure_decote) & (assiette_isf_ifi <= decote.borne_superieure_decote)
        lb = decote.parametre_calcul_decote - decote.taux_decote * assiette_isf_ifi
        return lb * elig


class isf_ifi_apres_plaf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'ISF-IFI après plafonnement'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        total_impots_plafonnement_isf_ifi = foyer_fiscal('total_impots_plafonnement_isf_ifi', period)
        revenus_et_produits_plafonnement_isf_ifi = foyer_fiscal('revenus_et_produits_plafonnement_isf_ifi', period)
        isf_ifi_avant_plaf = foyer_fiscal('isf_ifi_avant_plaf', period)
        plaf = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.plaf

        # si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas
        # si entre les deux seuils; l'allègement est limité au 1er seuil
        # si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement
        # est limité à 50% de l'ISF
        plafonnement = max_(total_impots_plafonnement_isf_ifi - revenus_et_produits_plafonnement_isf_ifi, 0)
        limitationplaf = (
            (isf_ifi_avant_plaf <= plaf.plaf.seuil1) * plafonnement
            + (plaf.plaf.seuil1 <= isf_ifi_avant_plaf) * (isf_ifi_avant_plaf <= plaf.plaf.seuil2) * min_(plafonnement, plaf.plaf.seuil1)
            + (isf_ifi_avant_plaf >= plaf.plaf.seuil2) * min_(isf_ifi_avant_plaf * plaf.plafonnement_plafonnement, plafonnement)
            )
        return max_(isf_ifi_avant_plaf - limitationplaf, 0)

    def formula_2012_01_01(foyer_fiscal, period):
        '''
        Plafonnement supprimé pour l'année 2012
        '''
        isf_ifi_avant_plaf = foyer_fiscal('isf_ifi_avant_plaf', period)
        return isf_ifi_avant_plaf

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        total_impots_plafonnement_isf_ifi = foyer_fiscal('total_impots_plafonnement_isf_ifi', period)
        revenus_et_produits_plafonnement_isf_ifi = foyer_fiscal('revenus_et_produits_plafonnement_isf_ifi', period)
        isf_ifi_avant_plaf = foyer_fiscal('isf_ifi_avant_plaf', period)
        plaf = parameters(period).taxation_capital.impot_solidarite_fortune_isf_1989_2017.plaf

        plafond = max_(0, total_impots_plafonnement_isf_ifi - plaf.plafonnement_taux_imposition * revenus_et_produits_plafonnement_isf_ifi)  # case 9PV sur le formulaire 2042C des revenus 2013 aux revenus 2016
        return max_(isf_ifi_avant_plaf - plafond, 0)

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        total_impots_plafonnement_isf_ifi = foyer_fiscal('total_impots_plafonnement_isf_ifi', period)
        revenus_et_produits_plafonnement_isf_ifi = foyer_fiscal('revenus_et_produits_plafonnement_isf_ifi', period)
        isf_ifi_avant_plaf = foyer_fiscal('isf_ifi_avant_plaf', period)
        plaf = parameters(period).taxation_capital.impot_fortune_immobiliere_ifi_partir_2018.plaf

        plafond = max_(0, total_impots_plafonnement_isf_ifi - plaf.plafonnement_taux_imposition * revenus_et_produits_plafonnement_isf_ifi)  # case 9PV sur le formulaire 2042C des revenus 2013 aux revenus 2016
        return max_(isf_ifi_avant_plaf - plafond, 0)


class isf_ifi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Montant d'ISF-IFI"
    reference = 'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000036385039/'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        b4rs = foyer_fiscal('b4rs', period)
        isf_ifi_apres_plaf = foyer_fiscal('isf_ifi_apres_plaf', period)
        return min_(-(isf_ifi_apres_plaf - b4rs), 0)


# BOUCLIER FISCAL

# calcul de l'ensemble des revenus du contribuable

class rag(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus agricoles'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=BA&pageId=prof_ba&sfid=50'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Revenus agricoles
        '''
        frag_exon = individu('frag_exon', period)
        frag_impo = individu('frag_impo', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        arag_defi = individu('arag_defi', period)
        nrag_exon = individu('nrag_exon', period)
        nrag_impg = individu('nrag_impg', period)
        nrag_defi = individu('nrag_defi', period)
        nrag_ajag = individu('nrag_ajag', period)

        return (
            frag_exon + frag_impo
            + arag_exon + arag_impg - arag_defi
            + nrag_exon + nrag_impg - nrag_defi
            + nrag_ajag
            )

    def formula_2016_01_01(individu, period, parameters):
        '''
        Revenus agricoles
        '''
        mrag_exon = individu('mrag_exon', period)
        mrag_impo = individu('mrag_impo', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        arag_defi = individu('arag_defi', period)
        nrag_exon = individu('nrag_exon', period)
        nrag_impg = individu('nrag_impg', period)
        nrag_defi = individu('nrag_defi', period)
        nrag_ajag = individu('nrag_ajag', period)

        return (
            mrag_exon + mrag_impo
            + arag_exon + arag_impg - arag_defi
            + nrag_exon + nrag_impg - nrag_defi
            + nrag_ajag
            )


class ric(Variable):
    value_type = float
    entity = Individu
    label = 'Bénéfices industriels et commerciaux'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?pageId=prof_bic&espId=2&impot=BIC&sfid=50'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Bénéfices industriels et commerciaux
        '''
        mbic_exon = individu('mbic_exon', period)
        mbic_impv = individu('mbic_impv', period)
        mbic_imps = individu('mbic_imps', period)
        abic_exon = individu('abic_exon', period)
        nbic_exon = individu('nbic_exon', period)
        abic_impn = individu('abic_impn', period)
        nbic_impn = individu('nbic_impn', period)
        abic_imps = individu('abic_imps', period)
        nbic_imps = individu('nbic_imps', period)
        abic_defn = individu('abic_defn', period)
        nbic_defn = individu('nbic_defn', period)
        abic_defs = individu('abic_defs', period)
        nbic_defs = individu('nbic_defs', period)
        nbic_apch = individu('nbic_apch', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        zbic = (
            mbic_exon + mbic_impv + mbic_imps
            + abic_exon + nbic_exon
            + abic_impn + nbic_impn
            + abic_imps + nbic_imps
            + abic_defn - nbic_defn
            + abic_defs - nbic_defs
            + nbic_apch
            )

        cond = (mbic_impv > 0) & (mbic_imps == 0)
        taux = micro.microentreprise.regime_micro_bnc.marchandises.taux * cond + micro.microentreprise.regime_micro_bnc.services.taux * not_(cond)

        cbic = min_(
            mbic_impv + mbic_imps + mbic_exon,
            max_(
                micro.microentreprise.montant_minimum,
                round_(
                    mbic_impv * micro.microentreprise.regime_micro_bnc.marchandises.taux + mbic_imps * micro.microentreprise.regime_micro_bnc.services.taux + mbic_exon * taux
                    )
                )
            )
        return zbic - cbic


class rac(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus accessoires individuels'
    reference = 'http://vosdroits.service-public.fr/particuliers/F1225.xhtml'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Revenus accessoires individuels
        '''
        macc_exon = individu('macc_exon', period)
        macc_impv = individu('macc_impv', period)
        macc_imps = individu('macc_imps', period)
        aacc_exon = individu('aacc_exon', period)
        aacc_impn = individu('aacc_impn', period)
        aacc_imps = individu('aacc_imps', period)
        aacc_defn = individu('aacc_defn', period)
        aacc_defs = individu('aacc_defs', period)
        nacc_exon = individu('nacc_exon', period)
        nacc_impn = individu('nacc_impn', period)
        nacc_defn = individu('nacc_defn', period)
        nacc_pres = individu('nacc_pres', period)
        mncn_impo = individu('mncn_impo', period)
        cncn_bene = individu('cncn_bene', period)
        cncn_defi = individu('cncn_defi', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        zacc = (
            macc_exon + macc_impv + macc_imps
            + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs
            + nacc_exon + nacc_impn - nacc_defn + nacc_pres
            + mncn_impo + cncn_bene - cncn_defi
            )

    # TODO: aacc_imps aacc_defs
        cond = (macc_impv > 0) & (macc_imps == 0)
        taux = micro.microentreprise.regime_micro_bnc.marchandises.taux * cond + micro.microentreprise.regime_micro_bnc.services.taux * not_(cond)

        cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, max_(micro.microentreprise.montant_minimum, round_(
            macc_impv * micro.microentreprise.regime_micro_bnc.marchandises.taux
            + macc_imps * micro.microentreprise.regime_micro_bnc.services.taux + macc_exon * taux
            + mncn_impo * micro.microentreprise.regime_micro_bnc.taux)))

        return zacc - cacc


# TODO: à reintégrer dans impot_revenu_restant_a_payer
class rvcm_plus_abat(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'rvcm_plus_abat'
    definition_period = YEAR
    end = '2010-12-31'

    def formula(foyer_fiscal, period, parameters):
        '''
        Revenu catégoriel avec abattement de 40% réintégré.
        '''
        rev_cat_rvcm = foyer_fiscal('revenu_categoriel_capital', period)
        rfr_rvcm_abattements_a_reintegrer = foyer_fiscal('rfr_rvcm_abattements_a_reintegrer', period)

        return rev_cat_rvcm + rfr_rvcm_abattements_a_reintegrer


class maj_cga(Variable):
    value_type = float
    entity = Individu
    label = 'Majoration pour non adhésion à un centre de gestion agréé (pour chaque individu du foyer)'
    definition_period = YEAR

    # TODO: à reintégrer dans impot_revenu_restant_a_payer (et vérifier au passage que frag_impo est dans la majo_cga
    def formula(individu, period, parameters):
        frag_impo = individu('frag_impo', period)
        nrag_impg = individu('nrag_impg', period)
        nbic_impn = individu('nbic_impn', period)
        nbic_imps = individu('nbic_imps', period)
        nbic_defn = individu('nbic_defn', period)
        nbic_defs = individu('nbic_defs', period)
        nacc_impn = individu('nacc_impn', period)
        nlnp_defs = individu('nlnp_defs', period)
        nacc_defn = individu('nacc_defn', period)
        nlnp_imps = individu('nlnp_imps', period)
        nbnc_impo = individu('nbnc_impo', period)
        nbnc_defi = individu('nbnc_defi', period)
        rpns = parameters(period).impot_revenu.calcul_revenus_imposables.rpns

        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

        # C revenus industriels et commerciaux non professionnels
        # (revenus accesoires du foyers en nomenclature INSEE)
        nacc_timp = max_(0, (nacc_impn + nlnp_imps) - (nacc_defn + nlnp_defs))

        # régime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
        nbnc_timp = nbnc_impo - nbnc_defi

        # Totaux
        ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp

        return max_(0, rpns.cga_taux2 * (ntimp + frag_impo))


class bouclier_rev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'bouclier_rev'
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Total des revenus sur l'année 'n' net de charges
        '''
        rbg = foyer_fiscal('rbg', period)
        csg_patrimoine_deductible_ir = foyer_fiscal('csg_patrimoine_deductible_ir', period)
        rvcm_plus_abat = foyer_fiscal('rvcm_plus_abat', period)
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period)
        rev_exo = foyer_fiscal('rev_exo', period)  # noqa F841
        rev_or = foyer_fiscal('rev_or', period)
        pensions_alimentaires_deduites = foyer_fiscal('pensions_alimentaires_deduites', period)
        cd_eparet = foyer_fiscal('cd_eparet', period)

        maj_cga_i = foyer_fiscal.members('maj_cga', period)  # noqa F841
        maj_cga = foyer_fiscal.sum(maj_cga)  # noqa F841

        # TODO: réintégrer les déficits antérieur
        # TODO: intégrer les revenus soumis au prélèvement libératoire
        # deficit_ante =

        # # Revenus
        # TODO: UNUSED ?
        frac_rvcm_rfr = 0.7 * rvcm_plus_abat  # noqa F841
        # # revenus distribués?
        # # A majorer de l'abatt de 40% - montant brut en cas de PFL
        # # pour le calcul de droit à restitution : prendre 0.7*montant_brut_rev_dist_soumis_au_barème
        # rev_bar = rbg - maj_cga - csg_patrimoine_deductible_ir - deficit_ante
        rev_bar = rbg - maj_cga - csg_patrimoine_deductible_ir

    # # TODO: AJOUTER : indemnités de fonction percus par les élus- revenus soumis à régimes spéciaux

        # Revenu soumis à l'impôt sur le revenu forfaitaire
        rev_lib = revenus_capitaux_prelevement_liberatoire
        # TODO: AJOUTER plus-values immo et moins values?

        # Revenus exonérés d'IR réalisés en France et à l'étranger
        # rev_exo = primes_pel + primes_cel + rente_pea + int_livrets + plus_values_per

        # TODO: proposer à l'utilisateur des taux de réference- PER, PEA, PEL,...
        # sommes investis- calculer les plus_values annuelles et prendre en compte pour rev_exo?
        # revenus soumis à la taxe forfaitaire sur les métaux précieux : rev_or

        # revenus = rev_bar + rev_lib + rev_exo + rev_or
        revenus = rev_bar + rev_lib + rev_or

        # # CHARGES
        # Pension alimentaires
        # Cotisations ou primes versées au titre de l'épargne retraite

        charges = pensions_alimentaires_deduites + cd_eparet

        return revenus - charges


class bouclier_imp_gen(Variable):  # # ajouter CSG- CRDS
    value_type = float
    entity = FoyerFiscal
    label = 'bouclier_imp_gen'
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        impot_revenu_restant_a_payer = foyer_fiscal('impot_revenu_restant_a_payer', period)
        tax_fonc = foyer_fiscal('tax_fonc', period)
        isf_ifi = foyer_fiscal('isf_ifi', period)
        csg_deductible_salaire_i = foyer_fiscal.members('csg_deductible_salaire', period)
        csg_imposable_salaire_i = foyer_fiscal.members('csg_imposable_salaire', period)
        crds_salaire_i = foyer_fiscal.members('crds_salaire', period)
        csg_imposable_chomage_i = foyer_fiscal.members('csg_imposable_chomage', period)
        csg_deductible_chomage_i = foyer_fiscal.members('csg_deductible_chomage', period)
        csg_deductible_retraite_i = foyer_fiscal.members('csg_deductible_retraite', period)
        csg_imposable_retraite_i = foyer_fiscal.members('csg_imposable_retraite', period)

        prelevements_sociaux_revenus_capital = foyer_fiscal('prelevements_sociaux_revenus_capital', period)
        crds_salaire = foyer_fiscal.sum(crds_salaire_i)
        csg_deductible_chomage = foyer_fiscal.sum(csg_deductible_chomage_i)
        csg_imposable_chomage = foyer_fiscal.sum(csg_imposable_chomage_i)
        csg_deductible_salaire = foyer_fiscal.sum(csg_deductible_salaire_i)
        csg_imposable_salaire = foyer_fiscal.sum(csg_imposable_salaire_i)
        csg_deductible_retraite = foyer_fiscal.sum(csg_deductible_retraite_i)
        csg_imposable_retraite = foyer_fiscal.sum(csg_imposable_retraite_i)

        taxe_habitation_i = foyer_fiscal.members.menage('taxe_habitation', period)  # noqa F841
        taxe_habitation = foyer_fiscal.sum(taxe_habitation_i, role = Menage.PERSONNE_DE_REFERENCE)

        # # ajouter Prelèvements sources/ libé
        # # ajouter crds rstd
        # # impôt sur les plus-values immo et cession de fonds de commerce
        imp1 = prelevements_sociaux_revenus_capital + csg_deductible_salaire + csg_deductible_chomage + crds_salaire + csg_deductible_retraite
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés sur l'année 'n'
        '''
        imp2 = impot_revenu_restant_a_payer + isf_ifi + taxe_habitation + tax_fonc + csg_imposable_salaire + csg_imposable_chomage + csg_imposable_retraite
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés en 'n-1'
        '''
        return imp1 + imp2


class restitutions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'restitutions'
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Restitutions d'impôt sur le revenu et degrèvements percus en l'année 'n'
        '''
        ppe = foyer_fiscal('ppe', period)
        restit_imp = foyer_fiscal('restit_imp', period)

        return ppe + restit_imp


class bouclier_sumimp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'bouclier_sumimp'
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Somme totale des impôts moins restitutions et degrèvements
        '''
        bouclier_imp_gen = foyer_fiscal('bouclier_imp_gen', period)
        restitutions = foyer_fiscal('restitutions', period)

        return -bouclier_imp_gen + restitutions


class bouclier_fiscal(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'bouclier_fiscal'
    end = '2010-12-31'
    reference = 'http://fr.wikipedia.org/wiki/Bouclier_fiscal'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        bouclier_sumimp = foyer_fiscal('bouclier_sumimp', period)
        bouclier_rev = foyer_fiscal('bouclier_rev', period)
        bouclier_fiscal = parameters(period).impot_revenu.calcul_impot_revenu.bouclier_fiscal

        return max_(0, bouclier_sumimp - (bouclier_rev * bouclier_fiscal.taux))
