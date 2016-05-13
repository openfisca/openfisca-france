# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_, minimum as min_

from ..base import *  # noqa analysis:ignore

# Variables apparaissant dans la feuille de déclaration de patrimoine soumis à l'ISF

## Immeubles bâtis
class b1ab(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Valeur de la résidence principale avant abattement"


class b1ac(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Valeur des autres immeubles avant abattement"



## non bâtis
class b1bc(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Immeubles non bâtis : bois, fôrets et parts de groupements forestiers"


class b1be(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Immeubles non bâtis : biens ruraux loués à long termes"


class b1bh(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers"


class b1bk(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Immeubles non bâtis : autres biens"



## droits sociaux- valeurs mobilières-liquidités- autres meubles
class b1cl(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Parts et actions détenues par les salariés et mandataires sociaux"


class b1cb(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum"


class b1cd(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité"


class b1ce(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres valeurs mobilières"


class b1cf(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Liquidités"


class b1cg(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres biens meubles"



class b1co(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Autres biens meubles : contrats d'assurance-vie"



#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réductions
class b2gh(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Total du passif et autres déductions"



## réductions
class b2mt(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements directs dans une société"


class b2ne(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements directs dans une société"


class b2mv(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements par sociétés interposées, holdings"


class b2nf(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements par sociétés interposées, holdings"


class b2mx(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements par le biais de FIP"


class b2na(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour investissements par le biais de FCPI ou FCPR"


class b2nc(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réductions pour dons à certains organismes d'intérêt général"



##  montant impôt acquitté hors de France
class b4rs(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Montant de l'impôt acquitté hors de France"



## BOUCLIER FISCAL

class rev_or(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class rev_exo(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux



class tax_fonc(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Taxe foncière"


class restit_imp(Variable):
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class etr(Variable):
    column = IntCol
    entity_class = Individus




# Calcul de l'impôt de solidarité sur la fortune

# 1 ACTIF BRUT

class isf_imm_bati(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_imm_bati"

    def function(self, simulation, period):
        '''
        Immeubles bâtis
        '''
        period = period.this_year
        b1ab = simulation.calculate('b1ab', period)
        b1ac = simulation.calculate('b1ac', period)
        P = simulation.legislation_at(period.start).isf.res_princ

        return period, (1 - P.taux) * b1ab + b1ac


class isf_imm_non_bati(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_imm_non_bati"

    def function(self, simulation, period):
        '''
        Immeubles non bâtis
        '''
        period = period.this_year
        b1bc = simulation.calculate('b1bc', period)
        b1be = simulation.calculate('b1be', period)
        b1bh = simulation.calculate('b1bh', period)
        b1bk = simulation.calculate('b1bk', period)
        P = simulation.legislation_at(period.start).isf.nonbat

        # forêts
        b1bd = b1bc * P.taux_f
        # bien ruraux loués à long terme
        b1bf = min_(b1be, P.seuil) * P.taux_r1
        b1bg = max_(b1be - P.seuil, 0) * P.taux_r2
        # part de groupements forestiers- agricoles fonciers
        b1bi = min_(b1bh, P.seuil) * P.taux_r1
        b1bj = max_(b1bh - P.seuil, 0) * P.taux_r2
        return period, b1bd + b1bf + b1bg + b1bi + b1bj + b1bk


# # droits sociaux- valeurs mobilières- liquidités- autres meubles ##


class isf_actions_sal(Variable):  # # non présent en 2005##
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_actions_sal"
    start_date = date(2006, 1, 1)

    def function(self, simulation, period):
        '''
        Parts ou actions détenues par les salariés et mandataires sociaux
        '''
        period = period.this_year
        b1cl = simulation.calculate('b1cl', period)
        P = simulation.legislation_at(period.start).isf.droits_soc

        return period,  b1cl * P.taux1


class isf_droits_sociaux(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_droits_sociaux"

    def function(self, simulation, period):
        period = period.this_year
        isf_actions_sal = simulation.calculate('isf_actions_sal', period)
        b1cb = simulation.calculate('b1cb', period)
        b1cd = simulation.calculate('b1cd', period)
        b1ce = simulation.calculate('b1ce', period)
        b1cf = simulation.calculate('b1cf', period)
        b1cg = simulation.calculate('b1cg', period)
        P = simulation.legislation_at(period.start).isf.droits_soc

        b1cc = b1cb * P.taux2
        return period, isf_actions_sal + b1cc + b1cd + b1ce + b1cf + b1cg


class ass_isf(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ass_isf"

    def function(self, simulation, period):
        # TODO: Gérer les trois option meubles meublants
        period = period.this_year
        isf_imm_bati = simulation.calculate('isf_imm_bati', period)
        isf_imm_non_bati = simulation.calculate('isf_imm_non_bati', period)
        isf_droits_sociaux = simulation.calculate('isf_droits_sociaux', period)
        b1cg = simulation.calculate('b1cg', period)
        b2gh = simulation.calculate('b2gh', period)
        P = simulation.legislation_at(period.start).isf.forf_mob

        total = isf_imm_bati + isf_imm_non_bati + isf_droits_sociaux
        forf_mob = (b1cg != 0) * b1cg + (b1cg == 0) * total * P.taux
        actif_brut = total + forf_mob
        return period, actif_brut - b2gh


# # calcul de l'impôt par application du barème ##


class isf_iai(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_iai"

    @dated_function(start = date(2002, 1, 1), stop = date(2010, 12, 31))
    def function_20020101_20101231(self, simulation, period):
        period = period.this_year
        ass_isf = simulation.calculate('ass_isf', period)
        bareme = simulation.legislation_at(period.start).isf.bareme
        return period, bareme.calc(ass_isf)

    @dated_function(start = date(2011, 1, 1), stop = date(2015, 12, 31))
    def function_20110101_20151231(self, simulation, period):
        period = period.this_year
        ass_isf = simulation.calculate('ass_isf', period)
        bareme = simulation.legislation_at(period.start).isf.bareme
        ass_isf = (ass_isf >= bareme.rates[1]) * ass_isf
        return period, bareme.calc(ass_isf)


class isf_avant_reduction(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_avant_reduction"

    def function(self, simulation, period):
        period = period.this_year
        isf_iai = simulation.calculate('isf_iai', period)
        decote_isf = simulation.calculate('decote_isf', period)

        return period, isf_iai - decote_isf


class isf_reduc_pac(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_reduc_pac"

    def function(self, simulation, period):
        '''
        Réductions pour personnes à charges
        '''
        period = period.this_year
        nb_pac = simulation.calculate('nb_pac', period)
        nbH = simulation.calculate('nbH', period)
        P = simulation.legislation_at(period.start).isf.reduc_pac

        return period, P.reduc_1 * nb_pac + P.reduc_2 * nbH


class isf_inv_pme(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_inv_pme"
    start_date = date(2008, 1, 1)

    def function(self, simulation, period):
        '''
        Réductions pour investissements dans les PME
        à partir de 2008!
        '''
        period = period.this_year
        b2mt = simulation.calculate('b2mt', period)
        b2ne = simulation.calculate('b2ne', period)
        b2mv = simulation.calculate('b2mv', period)
        b2nf = simulation.calculate('b2nf', period)
        b2mx = simulation.calculate('b2mx', period)
        b2na = simulation.calculate('b2na', period)
        P = simulation.legislation_at(period.start).isf.pme

        inv_dir_soc = b2mt * P.taux2 + b2ne * P.taux1
        holdings = b2mv * P.taux2 + b2nf * P.taux1
        fip = b2mx * P.taux1
        fcpi = b2na * P.taux1
        return period, holdings + fip + fcpi + inv_dir_soc


class isf_org_int_gen(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_org_int_gen"

    def function(self, simulation, period):
        period = period.this_year
        b2nc = simulation.calculate('b2nc', period)
        P = simulation.legislation_at(period.start).isf.pme

        return period, b2nc * P.taux2


class isf_avant_plaf(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_avant_plaf"

    def function(self, simulation, period):
        '''
        Montant de l'impôt avant plafonnement
        '''
        period = period.this_year
        isf_avant_reduction = simulation.calculate('isf_avant_reduction', period)
        isf_inv_pme = simulation.calculate('isf_inv_pme', period)
        isf_org_int_gen = simulation.calculate('isf_org_int_gen', period)
        isf_reduc_pac = simulation.calculate('isf_reduc_pac', period)
        borne_max = simulation.legislation_at(period.start).isf.pme.max

        return period, max_(0, isf_avant_reduction - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)


# # calcul du plafonnement ##
class tot_impot(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"tot_impot"

    def function(self, simulation, period):
        '''
        Total des impôts dus au titre des revenus et produits (irpp, cehr, pl, prélèvements sociaux) + ISF
        Utilisé pour calculer le montant du plafonnement de l'ISF
        '''
        period = period.this_year
        irpp = simulation.calculate('irpp', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)
        crds_holder = simulation.compute('crds', period)
        csg_holder = simulation.compute('csg', period)
        prelsoc_cap_holder = simulation.compute('prelsoc_cap', period)

        crds = self.split_by_roles(crds_holder, roles = [VOUS, CONJ])
        csg = self.split_by_roles(csg_holder, roles = [VOUS, CONJ])
        prelsoc_cap = self.split_by_roles(prelsoc_cap_holder, roles = [VOUS, CONJ])

        return period, (-irpp + isf_avant_plaf -
            (crds[VOUS] + crds[CONJ]) - (csg[VOUS] + csg[CONJ]) - (prelsoc_cap[VOUS] + prelsoc_cap[CONJ])
            )

        # TODO: irpp n'est pas suffisant : ajouter ir soumis à taux propor + impôt acquitté à l'étranger
        # + prélèvement libé de l'année passée + montant de la csg


class revetproduits(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenus et produits perçus (avant abattement)"

    def function(self, simulation, period):
        '''
        Utilisé pour calculer le montant du plafonnement de l'ISF
        Cf.
        http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8342/fichedescriptiveformulaire_8342.pdf
        '''
        period = period.this_year
        salcho_imp_holder = simulation.compute('revenu_assimile_salaire_apres_abattements', period)
        pen_net_holder = simulation.compute('revenu_assimile_pension_apres_abattements', period)
        retraite_titre_onereux_net = simulation.calculate('retraite_titre_onereux_net', period)
        rev_cap_bar = simulation.calculate('rev_cap_bar', period)
        fon = simulation.calculate('fon', period)
        ric_holder = simulation.compute('ric', period)
        rag_holder = simulation.compute('rag', period)
        rpns_exon_holder = simulation.compute('rpns_exon', period)
        rpns_pvct_holder = simulation.compute('rpns_pvct', period)
        rev_cap_lib = simulation.calculate('rev_cap_lib', period)
        imp_lib = simulation.calculate('imp_lib', period)
        P = simulation.legislation_at(period.start).isf.plafonnement

        revenu_assimile_pension_apres_abattements = self.sum_by_entity(pen_net_holder)
        rag = self.sum_by_entity(rag_holder)
        ric = self.sum_by_entity(ric_holder)
        rpns_exon = self.sum_by_entity(rpns_exon_holder)
        rpns_pvct = self.sum_by_entity(rpns_pvct_holder)
        revenu_assimile_salaire_apres_abattements = self.sum_by_entity(salcho_imp_holder)

        # rev_cap et imp_lib pour produits soumis à prel libératoire- check TODO:
        # # def rev_exon et rev_etranger dans data? ##
        pt = max_(
            0,
            revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements + retraite_titre_onereux_net + rev_cap_bar + rev_cap_lib + ric + rag + rpns_exon +
            rpns_pvct + imp_lib + fon
            )
        return period, pt * P.taux


class decote_isf(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Décote de l'ISF"
    start_date = date(2013, 1, 1)

    def function(self, simulation, period):
        period = period.this_year
        ass_isf = simulation.calculate('ass_isf', period)
        P = simulation.legislation_at(period.start).isf.decote

        elig = (ass_isf >= P.min) & (ass_isf <= P.max)
        LB = P.base - P.taux * ass_isf
        return period, LB * elig


class isf_apres_plaf(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt sur la fortune après plafonnement"
    # Plafonnement supprimé pour l'année 2012

    @dated_function(start = date(2002, 1, 1), stop = date(2011, 12, 31))
    def function_20020101_20111231(self, simulation, period):
        period = period.this_year
        tot_impot = simulation.calculate('tot_impot', period)
        revetproduits = simulation.calculate('revetproduits', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)
        P = simulation.legislation_at(period.start).isf.plaf

        # si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas
        # si entre les deux seuils; l'allègement est limité au 1er seuil
        # si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement
        #    est limité à 50% de l'ISF
        plafonnement = max_(tot_impot - revetproduits, 0)
        limitationplaf = (
            (isf_avant_plaf <= P.seuil1) * plafonnement +
            (P.seuil1 <= isf_avant_plaf) * (isf_avant_plaf <= P.seuil2) * min_(plafonnement, P.seuil1) +
            (isf_avant_plaf >= P.seuil2) * min_(isf_avant_plaf * P.taux, plafonnement)
            )
        return period, max_(isf_avant_plaf - limitationplaf, 0)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):
        period = period.this_year
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)

        # si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas ##
        # si entre les deux seuils; l'allègement est limité au 1er seuil ##
        # si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement
        #    est limité à 50% de l'ISF
        return period, isf_avant_plaf

    @dated_function(start = date(2013, 1, 1), stop = date(2015, 12, 31))
    def function_20130101_20151231(self, simulation, period):
        """
        Impôt sur la fortune après plafonnement
        """
        period = period.this_year
        tot_impot = simulation.calculate('tot_impot', period)
        revetproduits = simulation.calculate('revetproduits', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)

        plafond = max_(0, tot_impot - revetproduits)  # case PU sur la déclaration d'impôt
        return period, max_(isf_avant_plaf - plafond, 0)


class isf_tot(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_tot"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_isf&espId=1&impot=ISF&sfid=50"

    def function(self, simulation, period):
        period = period.this_year
        b4rs = simulation.calculate('b4rs', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)
        isf_apres_plaf = simulation.calculate('isf_apres_plaf', period)
        irpp = simulation.calculate('irpp', period)

        return period, min_(-((isf_apres_plaf - b4rs) * ((-irpp) > 0) + (isf_avant_plaf - b4rs) * ((-irpp) <= 0)), 0)


# # BOUCLIER FISCAL ##

# # calcul de l'ensemble des revenus du contribuable ##


# TODO: à reintégrer dans irpp
class rvcm_plus_abat(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rvcm_plus_abat"

    def function(self, simulation, period):
        '''
        Revenu catégoriel avec abattement de 40% réintégré.
        '''
        period = period.this_year
        rev_cat_rvcm = simulation.calculate('rev_cat_rvcm', period)
        rfr_rvcm = simulation.calculate('rfr_rvcm', period)

        return period, rev_cat_rvcm + rfr_rvcm


class maj_cga_individu(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Majoration pour non adhésion à un centre de gestion agréé (pour chaque individu du foyer)"

    # TODO: à reintégrer dans irpp (et vérifier au passage que frag_impo est dans la majo_cga
    def function(self, simulation, period):
        period = period.this_year
        frag_impo = simulation.calculate('frag_impo', period)
        nrag_impg = simulation.calculate('nrag_impg', period)
        nbic_impn = simulation.calculate('nbic_impn', period)
        nbic_imps = simulation.calculate('nbic_imps', period)
        nbic_defn = simulation.calculate('nbic_defn', period)
        nbic_defs = simulation.calculate('nbic_defs', period)
        nacc_impn = simulation.calculate('nacc_impn', period)
        nacc_meup = simulation.calculate('nacc_meup', period)
        nacc_defn = simulation.calculate('nacc_defn', period)
        nacc_defs = simulation.calculate('nacc_defs', period)
        nbnc_impo = simulation.calculate('nbnc_impo', period)
        nbnc_defi = simulation.calculate('nbnc_defi', period)
        P = simulation.legislation_at(period.start).ir.rpns

        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

        # C revenus industriels et commerciaux non professionnels
        # (revenus accesoires du foyers en nomenclature INSEE)
        nacc_timp = max_(0, (nacc_impn + nacc_meup) - (nacc_defn + nacc_defs))

        # régime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
        nbnc_timp = nbnc_impo - nbnc_defi

        # Totaux
        ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp

        return period, max_(0, P.cga_taux2 * (ntimp + frag_impo))


class maj_cga(PersonToEntityColumn):
    entity_class = FoyersFiscaux
    label = u"Majoration pour non adhésion à un centre de gestion agréé"
    operation = 'add'
    variable = maj_cga_individu


class bouclier_rev(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_rev"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Total des revenus sur l'année 'n' net de charges
        '''
        period = period.this_year
        rbg = simulation.calculate('rbg', period)
        maj_cga = simulation.calculate('maj_cga', period)
        csg_deduc = simulation.calculate('csg_deduc', period)
        rvcm_plus_abat = simulation.calculate('rvcm_plus_abat', period)
        rev_cap_lib = simulation.calculate('rev_cap_lib', period)
        rev_exo = simulation.calculate('rev_exo', period)
        rev_or = simulation.calculate('rev_or', period)
        cd_penali = simulation.calculate('cd_penali', period)
        cd_eparet = simulation.calculate('cd_eparet', period)


        # TODO: réintégrer les déficits antérieur
        # TODO: intégrer les revenus soumis au prélèvement libératoire
        # deficit_ante =

        # # Revenus
        frac_rvcm_rfr = 0.7 * rvcm_plus_abat  # TODO: UNUSED ?
        # # revenus distribués?
        # # A majorer de l'abatt de 40% - montant brut en cas de PFL
        # # pour le calcul de droit à restitution : prendre 0.7*montant_brut_rev_dist_soumis_au_barème
        # rev_bar = rbg - maj_cga - csg_deduc - deficit_ante
        rev_bar = rbg - maj_cga - csg_deduc

    # # TODO: AJOUTER : indemnités de fonction percus par les élus- revenus soumis à régimes spéciaux

        # Revenu soumis à l'impôt sur le revenu forfaitaire
        rev_lib = rev_cap_lib
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

        charges = cd_penali + cd_eparet

        return period, revenus - charges


class bouclier_imp_gen(Variable):  # # ajouter CSG- CRDS
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_imp_gen"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        period = period.this_year
        irpp = simulation.calculate('irpp', period)
        taxe_habitation_holder = simulation.compute('taxe_habitation', period)
        tax_fonc = simulation.calculate('tax_fonc', period)
        isf_tot = simulation.calculate('isf_tot', period)
        cotsoc_lib_declarant1_holder = simulation.compute('cotsoc_lib_declarant1', period)
        cotsoc_bar_declarant1_holder = simulation.compute('cotsoc_bar_declarant1', period)
        csg_deductible_salaire_holder = simulation.compute('csg_deductible_salaire', period)
        csg_imposable_salaire_holder = simulation.compute('csg_imposable_salaire', period)
        crds_salaire_holder = simulation.compute('crds_salaire', period)
        csg_imposable_chomage_holder = simulation.compute('csg_imposable_chomage', period)
        csg_deductible_chomage_holder = simulation.compute('csg_deductible_chomage', period)
        csg_deductible_retraite_holder = simulation.compute('csg_deductible_retraite', period)
        csg_imposable_retraite_holder = simulation.compute('csg_imposable_retraite', period)
        imp_lib = simulation.calculate('imp_lib', period)

        cotsoc_bar = self.sum_by_entity(cotsoc_bar_declarant1_holder)
        cotsoc_lib = self.sum_by_entity(cotsoc_lib_declarant1_holder)
        crds_salaire = self.sum_by_entity(crds_salaire_holder)
        csg_deductible_chomage = self.sum_by_entity(csg_deductible_chomage_holder)
        csg_imposable_chomage = self.sum_by_entity(csg_imposable_chomage_holder)
        csg_deductible_salaire = self.sum_by_entity(csg_deductible_salaire_holder)
        csg_imposable_salaire = self.sum_by_entity(csg_imposable_salaire_holder)
        csg_deductible_retraite = self.sum_by_entity(csg_deductible_retraite_holder)
        csg_imposable_retraite = self.sum_by_entity(csg_imposable_retraite_holder)
        taxe_habitation = self.cast_from_entity_to_role(taxe_habitation_holder, role = PREF)
        taxe_habitation = self.sum_by_entity(taxe_habitation)

        # # ajouter Prelèvements sources/ libé
        # # ajouter crds rstd
        # # impôt sur les plus-values immo et cession de fonds de commerce
        imp1 = cotsoc_lib + cotsoc_bar + csg_deductible_salaire + csg_deductible_chomage + crds_salaire + csg_deductible_retraite + imp_lib
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés sur l'année 'n'
        '''
        imp2 = irpp + isf_tot + taxe_habitation + tax_fonc + csg_imposable_salaire + csg_imposable_chomage + csg_imposable_retraite
        '''
        Impôts payés en l'année 'n' au titre des revenus réalisés en 'n-1'
        '''
        return period, imp1 + imp2


class restitutions(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"restitutions"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Restitutions d'impôt sur le revenu et degrèvements percus en l'année 'n'
        '''
        period = period.this_year
        ppe = simulation.calculate('ppe', period)
        restit_imp = simulation.calculate('restit_imp', period)

        return period, ppe + restit_imp


class bouclier_sumimp(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_sumimp"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Somme totale des impôts moins restitutions et degrèvements
        '''
        period = period.this_year
        bouclier_imp_gen = simulation.calculate('bouclier_imp_gen', period)
        restitutions = simulation.calculate('restitutions', period)

        return period, -bouclier_imp_gen + restitutions


class bouclier_fiscal(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_fiscal"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)
    url = "http://fr.wikipedia.org/wiki/Bouclier_fiscal"

    def function(self, simulation, period):
        period = period.this_year
        bouclier_sumimp = simulation.calculate('bouclier_sumimp', period)
        bouclier_rev = simulation.calculate('bouclier_rev', period)
        P = simulation.legislation_at(period.start).bouclier_fiscal

        return period, max_(0, bouclier_sumimp - (bouclier_rev * P.taux))
