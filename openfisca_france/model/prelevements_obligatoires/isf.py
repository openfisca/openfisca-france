# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *

# Variables apparaissant dans la feuille de déclaration de patrimoine soumis à l'ISF

# Immeubles bâtis


class b1ab(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Valeur de la résidence principale avant abattement"
    definition_period = YEAR


class b1ac(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Valeur des autres immeubles avant abattement"
    definition_period = YEAR


# non bâtis
class b1bc(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Immeubles non bâtis : bois, fôrets et parts de groupements forestiers"
    definition_period = YEAR


class b1be(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Immeubles non bâtis : biens ruraux loués à long termes"
    definition_period = YEAR


class b1bh(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers"
    definition_period = YEAR


class b1bk(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Immeubles non bâtis : autres biens"
    definition_period = YEAR


# droits sociaux- valeurs mobilières-liquidités- autres meubles
class b1cl(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Parts et actions détenues par les salariés et mandataires sociaux"
    definition_period = YEAR


class b1cb(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum"
    definition_period = YEAR


class b1cd(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité"
    definition_period = YEAR


class b1ce(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres valeurs mobilières"
    definition_period = YEAR


class b1cf(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Liquidités"
    definition_period = YEAR


class b1cg(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres biens meubles"
    definition_period = YEAR


class b1co(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Autres biens meubles : contrats d'assurance-vie"
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
    label = u"Total du passif et autres déductions"
    definition_period = YEAR


# réductions
class b2mt(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements directs dans une société"
    definition_period = YEAR


class b2ne(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements directs dans une société"
    definition_period = YEAR


class b2mv(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements par sociétés interposées, holdings"
    definition_period = YEAR


class b2nf(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements par sociétés interposées, holdings"
    definition_period = YEAR


class b2mx(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements par le biais de FIP"
    definition_period = YEAR


class b2na(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour investissements par le biais de FCPI ou FCPR"
    definition_period = YEAR


class b2nc(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réductions pour dons à certains organismes d'intérêt général"
    definition_period = YEAR


# montant impôt acquitté hors de France
class b4rs(Variable):
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Montant de l'impôt acquitté hors de France"
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
    label = u"Taxe foncière"
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

class isf_imm_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_imm_bati"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Immeubles bâtis
        '''
        b1ab = foyer_fiscal('b1ab', period)
        b1ac = foyer_fiscal('b1ac', period)
        P = parameters(period).taxation_capital.isf.res_princ

        return (1 - P.abattement_sur_residence_principale) * b1ab + b1ac


class isf_imm_non_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_imm_non_bati"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Immeubles non bâtis
        '''
        b1bc = foyer_fiscal('b1bc', period)
        b1be = foyer_fiscal('b1be', period)
        b1bh = foyer_fiscal('b1bh', period)
        b1bk = foyer_fiscal('b1bk', period)
        P = parameters(period).taxation_capital.isf.nonbat

        # forêts
        b1bd = b1bc * P.taux_f
        # bien ruraux loués à long terme
        b1bf = min_(b1be, P.seuil) * P.taux_r1
        b1bg = max_(b1be - P.seuil, 0) * P.taux_r2
        # part de groupements forestiers- agricoles fonciers
        b1bi = min_(b1bh, P.seuil) * P.taux_r1
        b1bj = max_(b1bh - P.seuil, 0) * P.taux_r2
        return b1bd + b1bf + b1bg + b1bi + b1bj + b1bk


# # droits sociaux- valeurs mobilières- liquidités- autres meubles ##


class isf_actions_sal(Variable):  # # non présent en 2005##
    value_type = float
    entity = FoyerFiscal
    label = u"isf_actions_sal"
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Parts ou actions détenues par les salariés et mandataires sociaux
        '''
        b1cl = foyer_fiscal('b1cl', period)
        P = parameters(period).taxation_capital.isf.droits_soc

        return b1cl * P.taux1


class isf_droits_sociaux(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_droits_sociaux"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        isf_actions_sal = foyer_fiscal('isf_actions_sal', period)
        b1cb = foyer_fiscal('b1cb', period)
        b1cd = foyer_fiscal('b1cd', period)
        b1ce = foyer_fiscal('b1ce', period)
        b1cf = foyer_fiscal('b1cf', period)
        b1cg = foyer_fiscal('b1cg', period)
        P = parameters(period).taxation_capital.isf.droits_soc

        b1cc = b1cb * P.taux2
        return isf_actions_sal + b1cc + b1cd + b1ce + b1cf + b1cg


class ass_isf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"ass_isf"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        # TODO: Gérer les trois option meubles meublants
        isf_imm_bati = foyer_fiscal('isf_imm_bati', period)
        isf_imm_non_bati = foyer_fiscal('isf_imm_non_bati', period)
        isf_droits_sociaux = foyer_fiscal('isf_droits_sociaux', period)
        b1cg = foyer_fiscal('b1cg', period)
        b2gh = foyer_fiscal('b2gh', period)
        P = parameters(period).taxation_capital.isf.forf_mob

        total = isf_imm_bati + isf_imm_non_bati + isf_droits_sociaux
        forf_mob = (b1cg != 0) * b1cg + (b1cg == 0) * total * P.taux
        actif_brut = total + forf_mob
        return actif_brut - b2gh


# # calcul de l'impôt par application du barème ##


class isf_iai(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_iai"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        ass_isf = foyer_fiscal('ass_isf', period)
        bareme = parameters(period).taxation_capital.isf.bareme
        return bareme.calc(ass_isf)

    # Cette formule a seulement été vérifiée jusqu'au 2015-12-31
    def formula_2011_01_01(foyer_fiscal, period, parameters):
        ass_isf = foyer_fiscal('ass_isf', period)
        bareme = parameters(period).taxation_capital.isf.bareme
        ass_isf = (ass_isf >= bareme.rates[1]) * ass_isf
        return bareme.calc(ass_isf)


class isf_avant_reduction(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_avant_reduction"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        isf_iai = foyer_fiscal('isf_iai', period)
        decote_isf = foyer_fiscal('decote_isf', period)

        return isf_iai - decote_isf


class isf_reduc_pac(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_reduc_pac"
    end = '2012-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Réductions pour personnes à charges
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        nbH = foyer_fiscal('nbH', period)
        P = parameters(period).taxation_capital.isf.reduc_pac

        return P.reduc_enf_garde * nb_pac + (P.reduc_enf_garde / 2) * nbH


class isf_inv_pme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_inv_pme"
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
        P = parameters(period).taxation_capital.isf.reduc_invest_don

        inv_dir_soc = b2mt * P.taux_don_interet_general + b2ne * P.taux_invest_direct_soc_holding
        holdings = b2mv * P.taux_don_interet_general + b2nf * P.taux_invest_direct_soc_holding
        fip = b2mx * P.taux_invest_direct_soc_holding
        fcpi = b2na * P.taux_invest_direct_soc_holding

        return holdings + fip + fcpi + inv_dir_soc


class isf_org_int_gen(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_org_int_gen"
    definition_period = YEAR

    def formula_2008(foyer_fiscal, period, parameters):
        b2nc = foyer_fiscal('b2nc', period)
        P = parameters(period).taxation_capital.isf.reduc_invest_don

        return b2nc * P.taux_don_interet_general


class isf_avant_plaf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Montant de l'impôt sur la fortune avant plafonnement"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        isf_avant_reduction = foyer_fiscal('isf_avant_reduction', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)

        return max_(0, isf_avant_reduction - isf_reduc_pac)

    def formula_2008(foyer_fiscal, period, parameters):
        isf_avant_reduction = foyer_fiscal('isf_avant_reduction', period)
        isf_inv_pme = foyer_fiscal('isf_inv_pme', period)
        isf_org_int_gen = foyer_fiscal('isf_org_int_gen', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)

        return max_(0, isf_avant_reduction - (isf_inv_pme + isf_org_int_gen) - isf_reduc_pac)

    def formula_2009(foyer_fiscal, period, parameters):
        isf_avant_reduction = foyer_fiscal('isf_avant_reduction', period)
        isf_inv_pme = foyer_fiscal('isf_inv_pme', period)
        isf_org_int_gen = foyer_fiscal('isf_org_int_gen', period)
        isf_reduc_pac = foyer_fiscal('isf_reduc_pac', period)
        borne_max = parameters(period).taxation_capital.isf.reduc_invest_don.max

        return max_(0, isf_avant_reduction - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)


# # calcul du plafonnement ##
class tot_impot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Total des impôts dus au titre des revenus et produits (irpp, cehr, pl, prélèvements sociaux) + ISF. Utilisé pour calculer le montant du plafonnement de l'ISF."
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        irpp = foyer_fiscal('irpp', period)
        isf_avant_plaf = foyer_fiscal('isf_avant_plaf', period)
        crds_i = foyer_fiscal.members('crds', period)
        csg_i = foyer_fiscal.members('csg', period)
        crds = foyer_fiscal.sum(crds_i, role = FoyerFiscal.DECLARANT)
        csg = foyer_fiscal.sum(csg_i, role = FoyerFiscal.DECLARANT)
        prelevements_sociaux_revenus_capital_hors_csg_crds = foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period)

        return (
            - irpp
            + isf_avant_plaf
            - crds
            - csg
            - prelevements_sociaux_revenus_capital_hors_csg_crds
            )

        # TODO: irpp n'est pas suffisant : ajouter ir soumis à taux propor + impôt acquitté à l'étranger
        # + prélèvement libé de l'année passée + montant de la csg


class revetproduits(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Revenus et produits perçus (avant abattement)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Utilisé pour calculer le montant du plafonnement de l'ISF
        Cf.
        http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8342/fichedescriptiveformulaire_8342.pdf
        '''
        salcho_imp_i = foyer_fiscal.members('revenu_assimile_salaire_apres_abattements', period)
        pen_net_i = foyer_fiscal.members('revenu_assimile_pension_apres_abattements', period)
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)
        fon = foyer_fiscal('fon', period)
        ric_i = foyer_fiscal.members('ric', period)
        rag_i = foyer_fiscal.members('rag', period)
        rpns_exon_i = foyer_fiscal.members('rpns_exon', period)
        rpns_pvct_i = foyer_fiscal.members('rpns_pvct', period)
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])  # Supprimée à partir de 2018
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])  # Supprimée à partir de 2018
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])  # Existe à partir de 2018
        prelevement_forfaitaire_liberatoire = foyer_fiscal('prelevement_forfaitaire_liberatoire', period)
        prelevement_forfaitaire_unique_ir = foyer_fiscal('prelevement_forfaitaire_unique_ir', period)
        P = parameters(period).taxation_capital.isf.plafonnement

        revenu_assimile_pension_apres_abattements = foyer_fiscal.sum(pen_net_i)
        rag = foyer_fiscal.sum(rag_i)
        ric = foyer_fiscal.sum(ric_i)
        rpns_exon = foyer_fiscal.sum(rpns_exon_i)
        rpns_pvct = foyer_fiscal.sum(rpns_pvct_i)
        revenu_assimile_salaire_apres_abattements = foyer_fiscal.sum(salcho_imp_i)

        # rev_cap et prelevement_forfaitaire_liberatoire pour produits soumis à prel libératoire- check TODO:
        # # def rev_exon et rev_etranger dans data? ##
        pt = max_(
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
            + prelevement_forfaitaire_liberatoire
            + prelevement_forfaitaire_unique_ir
            + fon
            )

        return pt * P.plafonnement_taux_d_imposition_isf


class decote_isf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Décote de l'ISF"
    definition_period = YEAR

    def formula_2013(foyer_fiscal, period, parameters):
        ass_isf = foyer_fiscal('ass_isf', period)
        P = parameters(period).taxation_capital.isf.decote

        elig = (ass_isf >= P.isf_borne_min_decote) & (ass_isf <= P.isf_borne_sup_decote)
        LB = P.isf_base_decote - P.isf_taux_decote * ass_isf
        return LB * elig


class isf_apres_plaf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Impôt sur la fortune après plafonnement"
    definition_period = YEAR
    # Plafonnement supprimé pour l'année 2012

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        tot_impot = foyer_fiscal('tot_impot', period)
        revetproduits = foyer_fiscal('revetproduits', period)
        isf_avant_plaf = foyer_fiscal('isf_avant_plaf', period)
        P = parameters(period).taxation_capital.isf.plaf

        # si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas
        # si entre les deux seuils; l'allègement est limité au 1er seuil
        # si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement
        #    est limité à 50% de l'ISF
        plafonnement = max_(tot_impot - revetproduits, 0)
        limitationplaf = (
            (isf_avant_plaf <= P.seuil1) * plafonnement
            + (P.seuil1 <= isf_avant_plaf) * (isf_avant_plaf <= P.seuil2) * min_(plafonnement, P.seuil1)
            + (isf_avant_plaf >= P.seuil2) * min_(isf_avant_plaf * P.taux, plafonnement)
            )
        return max_(isf_avant_plaf - limitationplaf, 0)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        isf_avant_plaf = foyer_fiscal('isf_avant_plaf', period)

        # si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas ##
        # si entre les deux seuils; l'allègement est limité au 1er seuil ##
        # si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement
        #    est limité à 50% de l'ISF
        return isf_avant_plaf

    # Cette formule a seulement été vérifiée jusqu'au 2015-12-31
    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Impôt sur la fortune après plafonnement
        """
        tot_impot = foyer_fiscal('tot_impot', period)
        revetproduits = foyer_fiscal('revetproduits', period)
        isf_avant_plaf = foyer_fiscal('isf_avant_plaf', period)

        plafond = max_(0, tot_impot - revetproduits)  # case PU sur la déclaration d'impôt
        return max_(isf_avant_plaf - plafond, 0)


class isf_tot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"isf_tot"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_isf&espId=1&impot=ISF&sfid=50"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        b4rs = foyer_fiscal('b4rs', period)
        isf_avant_plaf = foyer_fiscal('isf_avant_plaf', period)
        isf_apres_plaf = foyer_fiscal('isf_apres_plaf', period)
        irpp = foyer_fiscal('irpp', period)

        return min_(-((isf_apres_plaf - b4rs) * ((-irpp) > 0) + (isf_avant_plaf - b4rs) * ((-irpp) <= 0)), 0)


# # BOUCLIER FISCAL ##

# # calcul de l'ensemble des revenus du contribuable ##


# TODO: à reintégrer dans irpp
class rvcm_plus_abat(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"rvcm_plus_abat"
    definition_period = YEAR
    end = '2010-12-31'

    def formula(foyer_fiscal, period, parameters):
        '''
        Revenu catégoriel avec abattement de 40% réintégré.
        '''
        rev_cat_rvcm = foyer_fiscal('rev_cat_rvcm', period)
        rfr_rvcm_abattements_a_reintegrer = foyer_fiscal('rfr_rvcm_abattements_a_reintegrer', period)

        return rev_cat_rvcm + rfr_rvcm_abattements_a_reintegrer


class maj_cga(Variable):
    value_type = float
    entity = Individu
    label = u"Majoration pour non adhésion à un centre de gestion agréé (pour chaque individu du foyer)"
    definition_period = YEAR

    # TODO: à reintégrer dans irpp (et vérifier au passage que frag_impo est dans la majo_cga
    def formula(individu, period, parameters):
        frag_impo = individu('frag_impo', period)
        nrag_impg = individu('nrag_impg', period)
        nbic_impn = individu('nbic_impn', period)
        nbic_imps = individu('nbic_imps', period)
        nbic_defn = individu('nbic_defn', period)
        nbic_defs = individu('nbic_defs', period)
        nacc_impn = individu('nacc_impn', period)
        nacc_meup = individu('nacc_meup', period)
        nacc_defn = individu('nacc_defn', period)
        nacc_defs = individu('nacc_defs', period)
        nbnc_impo = individu('nbnc_impo', period)
        nbnc_defi = individu('nbnc_defi', period)
        P = parameters(period).impot_revenu.rpns

        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

        # C revenus industriels et commerciaux non professionnels
        # (revenus accesoires du foyers en nomenclature INSEE)
        nacc_timp = max_(0, (nacc_impn + nacc_meup) - (nacc_defn + nacc_defs))

        # régime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
        nbnc_timp = nbnc_impo - nbnc_defi

        # Totaux
        ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp

        return max_(0, P.cga_taux2 * (ntimp + frag_impo))


class bouclier_rev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"bouclier_rev"
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
        # # AJOUTER plus-values immo et moins values?

        # #Revenus exonérés d'IR réalisés en France et à l'étranger##
    #    rev_exo = primes_pel + primes_cel + rente_pea + int_livrets + plus_values_per

        # # proposer à l'utilisateur des taux de réference- PER, PEA, PEL,...TODO
        # # sommes investis- calculer les plus_values annuelles et prendre en compte pour rev_exo?
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
    label = u"bouclier_imp_gen"
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        irpp = foyer_fiscal('irpp', period)
        tax_fonc = foyer_fiscal('tax_fonc', period)
        isf_tot = foyer_fiscal('isf_tot', period)
        csg_deductible_salaire_i = foyer_fiscal.members('csg_deductible_salaire', period)
        csg_imposable_salaire_i = foyer_fiscal.members('csg_imposable_salaire', period)
        crds_salaire_i = foyer_fiscal.members('crds_salaire', period)
        csg_imposable_chomage_i = foyer_fiscal.members('csg_imposable_chomage', period)
        csg_deductible_chomage_i = foyer_fiscal.members('csg_deductible_chomage', period)
        csg_deductible_retraite_i = foyer_fiscal.members('csg_deductible_retraite', period)
        csg_imposable_retraite_i = foyer_fiscal.members('csg_imposable_retraite', period)
        prelevement_forfaitaire_liberatoire = foyer_fiscal('prelevement_forfaitaire_liberatoire', period)

        prelevements_sociaux_revenus_capital = foyer_fiscal('prelevements_sociaux_revenus_capital', period)
        crds_salaire = foyer_fiscal.sum(crds_salaire_i)
        csg_deductible_chomage = foyer_fiscal.sum(csg_deductible_chomage_i)
        csg_imposable_chomage = foyer_fiscal.sum(csg_imposable_chomage_i)
        csg_deductible_salaire = foyer_fiscal.sum(csg_deductible_salaire_i)
        csg_imposable_salaire = foyer_fiscal.sum(csg_imposable_salaire_i)
        csg_deductible_retraite = foyer_fiscal.sum(csg_deductible_retraite_i)
        csg_imposable_retraite = foyer_fiscal.sum(csg_imposable_retraite_i)

        taxe_habitation_i = foyer_fiscal.members.menage('taxe_habitation', period)  # noqa F841
        taxe_habitation = foyer_fiscal.sum(taxe_habitation, role = Menage.PERSONNE_DE_REFERENCE)

        # # ajouter Prelèvements sources/ libé
        # # ajouter crds rstd
        # # impôt sur les plus-values immo et cession de fonds de commerce
        imp1 = prelevements_sociaux_revenus_capital + csg_deductible_salaire + csg_deductible_chomage + crds_salaire + csg_deductible_retraite + prelevement_forfaitaire_liberatoire
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés sur l'année 'n'
        '''
        imp2 = irpp + isf_tot + taxe_habitation + tax_fonc + csg_imposable_salaire + csg_imposable_chomage + csg_imposable_retraite
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés en 'n-1'
        '''
        return imp1 + imp2


class restitutions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"restitutions"
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
    label = u"bouclier_sumimp"
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
    label = u"bouclier_fiscal"
    end = '2010-12-31'
    reference = "http://fr.wikipedia.org/wiki/Bouclier_fiscal"
    definition_period = YEAR

    def formula_2006(foyer_fiscal, period, parameters):
        bouclier_sumimp = foyer_fiscal('bouclier_sumimp', period)
        bouclier_rev = foyer_fiscal('bouclier_rev', period)
        P = parameters(period).bouclier_fiscal

        return max_(0, bouclier_sumimp - (bouclier_rev * P.taux))
