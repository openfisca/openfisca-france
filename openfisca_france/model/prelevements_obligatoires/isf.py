# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import maximum as max_, minimum as min_

from ..base import *  # noqa analysis:ignore

# Variables apparaissant dans la feuille de déclaration de patrimoine soumis à l'ISF

## Immeubles bâtis
build_column('b1ab', IntCol(entity = 'foy', label = u"Valeur de la résidence principale avant abattement", val_type = "monetary"))
build_column('b1ac', IntCol(entity = 'foy', label = u"Valeur des autres immeubles avant abattement", val_type = "monetary"))

## non bâtis
build_column('b1bc', IntCol(entity = 'foy', label = u"Immeubles non bâtis : bois, fôrets et parts de groupements forestiers", val_type = "monetary"))
build_column('b1be', IntCol(entity = 'foy', label = u"Immeubles non bâtis : biens ruraux loués à long termes", val_type = "monetary"))
build_column('b1bh', IntCol(entity = 'foy', label = u"Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type = "monetary"))
build_column('b1bk', IntCol(entity = 'foy', label = u"Immeubles non bâtis : autres biens", val_type = "monetary"))

## droits sociaux- valeurs mobilières-liquidités- autres meubles
build_column('b1cl', IntCol(entity = 'foy', label = u"Parts et actions détenues par les salariés et mandataires sociaux", val_type = "monetary"))
build_column('b1cb', IntCol(entity = 'foy', label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type = "monetary"))
build_column('b1cd', IntCol(entity = 'foy', label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type = "monetary"))
build_column('b1ce', IntCol(entity = 'foy', label = u"Autres valeurs mobilières", val_type = "monetary"))
build_column('b1cf', IntCol(entity = 'foy', label = u"Liquidités", val_type = "monetary"))
build_column('b1cg', IntCol(entity = 'foy', label = u"Autres biens meubles", val_type = "monetary"))

build_column('b1co', IntCol(entity = 'foy', label = u"Autres biens meubles : contrats d'assurance-vie", val_type = "monetary"))

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réductions
build_column('b2gh', IntCol(entity = 'foy', label = u"Total du passif et autres déductions", val_type = "monetary"))

## réductions
build_column('b2mt', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary"))
build_column('b2ne', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary"))
build_column('b2mv', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings" , val_type = "monetary"))
build_column('b2nf', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings", val_type = "monetary"))
build_column('b2mx', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FIP", val_type = "monetary"))
build_column('b2na', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type = "monetary"))
build_column('b2nc', IntCol(entity = 'foy', label = u"Réductions pour dons à certains organismes d'intérêt général", val_type = "monetary"))

##  montant impôt acquitté hors de France
build_column('b4rs', IntCol(entity = 'foy', label = u"Montant de l'impôt acquitté hors de France", val_type = "monetary"))

## BOUCLIER FISCAL

build_column('rev_or', IntCol(entity = 'foy', label = u"", val_type = "monetary"))
build_column('rev_exo', IntCol(entity = 'foy', label = u"", val_type = "monetary"))

build_column('tax_fonc', IntCol(entity = 'foy', label = u"Taxe foncière", val_type = "monetary"))
build_column('restit_imp', IntCol(entity = 'foy', label = u"", val_type = "monetary"))
build_column('etr', IntCol())


# Calcul de l'impôt de solidarité sur la fortune

# 1 ACTIF BRUT

@reference_formula
class isf_imm_bati(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_imm_bati"

    def function(self, simulation, period):
        '''
        Immeubles bâtis
        '''
        period = period.start.offset('first-of', 'year').period('year')
        b1ab = simulation.calculate('b1ab', period)
        b1ac = simulation.calculate('b1ac', period)
        P = simulation.legislation_at(period.start).isf.res_princ

        return period, (1 - P.taux) * b1ab + b1ac


@reference_formula
class isf_imm_non_bati(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_imm_non_bati"

    def function(self, simulation, period):
        '''
        Immeubles non bâtis
        '''
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class isf_actions_sal(SimpleFormulaColumn):  # # non présent en 2005##
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_actions_sal"
    start_date = date(2006, 1, 1)

    def function(self, simulation, period):
        '''
        Parts ou actions détenues par les salariés et mandataires sociaux
        '''
        period = period.start.offset('first-of', 'year').period('year')
        b1cl = simulation.calculate('b1cl', period)
        P = simulation.legislation_at(period.start).isf.droits_soc

        return period,  b1cl * P.taux1


@reference_formula
class isf_droits_sociaux(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_droits_sociaux"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        isf_actions_sal = simulation.calculate('isf_actions_sal', period)
        b1cb = simulation.calculate('b1cb', period)
        b1cd = simulation.calculate('b1cd', period)
        b1ce = simulation.calculate('b1ce', period)
        b1cf = simulation.calculate('b1cf', period)
        b1cg = simulation.calculate('b1cg', period)
        P = simulation.legislation_at(period.start).isf.droits_soc

        b1cc = b1cb * P.taux2
        return period, isf_actions_sal + b1cc + b1cd + b1ce + b1cf + b1cg


@reference_formula
class ass_isf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ass_isf"

    def function(self, simulation, period):
        # TODO: Gérer les trois option meubles meublants
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class isf_iai(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_iai"

    @dated_function(start = date(2002, 1, 1), stop = date(2010, 12, 31))
    def function_20020101_20101231(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        ass_isf = simulation.calculate('ass_isf', period)
        bareme = simulation.legislation_at(period.start).isf.bareme
        return period, bareme.calc(ass_isf)

    @dated_function(start = date(2011, 1, 1), stop = date(2015, 12, 31))
    def function_20110101_20151231(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        ass_isf = simulation.calculate('ass_isf', period)
        bareme = simulation.legislation_at(period.start).isf.bareme
        ass_isf = (ass_isf >= bareme.rates[1]) * ass_isf
        return period, bareme.calc(ass_isf)


@reference_formula
class isf_avant_reduction(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_avant_reduction"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        isf_iai = simulation.calculate('isf_iai', period)
        decote_isf = simulation.calculate('decote_isf', period)

        return period, isf_iai - decote_isf


@reference_formula
class isf_reduc_pac(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_reduc_pac"

    def function(self, simulation, period):
        '''
        Réductions pour personnes à charges
        '''
        period = period.start.offset('first-of', 'year').period('year')
        nb_pac = simulation.calculate('nb_pac', period)
        nbH = simulation.calculate('nbH', period)
        P = simulation.legislation_at(period.start).isf.reduc_pac

        return period, P.reduc_1 * nb_pac + P.reduc_2 * nbH


@reference_formula
class isf_inv_pme(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_inv_pme"
    start_date = date(2008, 1, 1)

    def function(self, simulation, period):
        '''
        Réductions pour investissements dans les PME
        à partir de 2008!
        '''
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class isf_org_int_gen(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_org_int_gen"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        b2nc = simulation.calculate('b2nc', period)
        P = simulation.legislation_at(period.start).isf.pme

        return period, b2nc * P.taux2


@reference_formula
class isf_avant_plaf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_avant_plaf"

    def function(self, simulation, period):
        '''
        Montant de l'impôt avant plafonnement
        '''
        period = period.start.offset('first-of', 'year').period('year')
        isf_avant_reduction = simulation.calculate('isf_avant_reduction', period)
        isf_inv_pme = simulation.calculate('isf_inv_pme', period)
        isf_org_int_gen = simulation.calculate('isf_org_int_gen', period)
        isf_reduc_pac = simulation.calculate('isf_reduc_pac', period)
        borne_max = simulation.legislation_at(period.start).isf.pme.max

        return period, max_(0, isf_avant_reduction - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)


# # calcul du plafonnement ##
@reference_formula
class tot_impot(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"tot_impot"

    def function(self, simulation, period):
        '''
        Total des impôts dus au titre des revenus et produits (irpp, cehr, pl, prélèvements sociaux) + ISF
        Utilisé pour calculer le montant du plafonnement de l'ISF
        '''
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class revetproduits(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenus et produits perçus (avant abattement)"

    def function(self, simulation, period):
        '''
        Utilisé pour calculer le montant du plafonnement de l'ISF
        Cf.
        http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8342/fichedescriptiveformulaire_8342.pdf
        '''
        period = period.start.offset('first-of', 'year').period('year')
        salcho_imp_holder = simulation.compute('salcho_imp', period)
        pen_net_holder = simulation.compute('pen_net', period)
        rto_net = simulation.calculate('rto_net', period)
        rev_cap_bar = simulation.calculate('rev_cap_bar', period)
        fon = simulation.calculate('fon', period)
        ric_holder = simulation.compute('ric', period)
        rag_holder = simulation.compute('rag', period)
        rpns_exon_holder = simulation.compute('rpns_exon', period)
        rpns_pvct_holder = simulation.compute('rpns_pvct', period)
        rev_cap_lib = simulation.calculate('rev_cap_lib', period)
        imp_lib = simulation.calculate('imp_lib', period)
        P = simulation.legislation_at(period.start).isf.plafonnement

        pen_net = self.sum_by_entity(pen_net_holder)
        rag = self.sum_by_entity(rag_holder)
        ric = self.sum_by_entity(ric_holder)
        rpns_exon = self.sum_by_entity(rpns_exon_holder)
        rpns_pvct = self.sum_by_entity(rpns_pvct_holder)
        salcho_imp = self.sum_by_entity(salcho_imp_holder)

        # rev_cap et imp_lib pour produits soumis à prel libératoire- check TODO:
        # # def rev_exon et rev_etranger dans data? ##
        pt = max_(
            0,
            salcho_imp + pen_net + rto_net + rev_cap_bar + rev_cap_lib + ric + rag + rpns_exon +
            rpns_pvct + imp_lib + fon
            )
        return period, pt * P.taux


@reference_formula
class decote_isf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Décote de l'ISF"
    start_date = date(2013, 1, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        ass_isf = simulation.calculate('ass_isf', period)
        P = simulation.legislation_at(period.start).isf.decote

        elig = (ass_isf >= P.min) & (ass_isf <= P.max)
        LB = P.base - P.taux * ass_isf
        return period, LB * elig


@reference_formula
class isf_apres_plaf(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt sur la fortune après plafonnement"
    # Plafonnement supprimé pour l'année 2012

    @dated_function(start = date(2002, 1, 1), stop = date(2011, 12, 31))
    def function_20020101_20111231(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
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
        period = period.start.offset('first-of', 'year').period('year')
        tot_impot = simulation.calculate('tot_impot', period)
        revetproduits = simulation.calculate('revetproduits', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)

        plafond = max_(0, tot_impot - revetproduits)  # case PU sur la déclaration d'impôt
        return period, max_(isf_avant_plaf - plafond, 0)


@reference_formula
class isf_tot(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"isf_tot"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_isf&espId=1&impot=ISF&sfid=50"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        b4rs = simulation.calculate('b4rs', period)
        isf_avant_plaf = simulation.calculate('isf_avant_plaf', period)
        isf_apres_plaf = simulation.calculate('isf_apres_plaf', period)
        irpp = simulation.calculate('irpp', period)

        return period, min_(-((isf_apres_plaf - b4rs) * ((-irpp) > 0) + (isf_avant_plaf - b4rs) * ((-irpp) <= 0)), 0)


# # BOUCLIER FISCAL ##

# # calcul de l'ensemble des revenus du contribuable ##


# TODO: à reintégrer dans irpp
@reference_formula
class rvcm_plus_abat(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rvcm_plus_abat"

    def function(self, simulation, period):
        '''
        Revenu catégoriel avec abattement de 40% réintégré.
        '''
        period = period.start.offset('first-of', 'year').period('year')
        rev_cat_rvcm = simulation.calculate('rev_cat_rvcm', period)
        rfr_rvcm = simulation.calculate('rfr_rvcm', period)

        return period, rev_cat_rvcm + rfr_rvcm


@reference_formula
class maj_cga_i(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Majoration pour non adhésion à un centre de gestion agréé (pour chaque individu du foyer)"

    # TODO: à reintégrer dans irpp (et vérifier au passage que frag_impo est dans la majo_cga
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class maj_cga(PersonToEntityColumn):
    entity_class = FoyersFiscaux
    label = u"Majoration pour non adhésion à un centre de gestion agréé"
    operation = 'add'
    variable = maj_cga_i


@reference_formula
class bouclier_rev(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_rev"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Total des revenus sur l'année 'n' net de charges
        '''
        period = period.start.offset('first-of', 'year').period('year')
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
        null = 0 * rbg

        deficit_ante = null

        # # Revenus
        frac_rvcm_rfr = 0.7 * rvcm_plus_abat  # TODO: UNUSED ?
        # # revenus distribués?
        # # A majorer de l'abatt de 40% - montant brut en cas de PFL
        # # pour le calcul de droit à restitution : prendre 0.7*montant_brut_rev_dist_soumis_au_barème
        rev_bar = rbg - maj_cga - csg_deduc - deficit_ante

    # # TODO: AJOUTER : indemnités de fonction percus par les élus- revenus soumis à régimes spéciaux

        # Revenu soumis à l'impôt sur le revenu forfaitaire
        rev_lib = rev_cap_lib
        # # AJOUTER plus-values immo et moins values?

        # #Revenus exonérés d'IR réalisés en France et à l'étranger##
    #    rev_exo = primes_pel + primes_cel + rente_pea + int_livrets + plus_values_per
        rev_exo = null

        # # proposer à l'utilisateur des taux de réference- PER, PEA, PEL,...TODO
        # # sommes investis- calculer les plus_values annuelles et prendre en compte pour rev_exo?
        # revenus soumis à la taxe forfaitaire sur les métaux précieux : rev_or

        revenus = rev_bar + rev_lib + rev_exo + rev_or

        # # CHARGES
        # Pension alimentaires
        # Cotisations ou primes versées au titre de l'épargne retraite

        charges = cd_penali + cd_eparet

        return period, revenus - charges


@reference_formula
class bouclier_imp_gen(SimpleFormulaColumn):  # # ajouter CSG- CRDS
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_imp_gen"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
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


@reference_formula
class restitutions(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"restitutions"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Restitutions d'impôt sur le revenu et degrèvements percus en l'année 'n'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        ppe = simulation.calculate('ppe', period)
        restit_imp = simulation.calculate('restit_imp', period)

        return period, ppe + restit_imp


@reference_formula
class bouclier_sumimp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_sumimp"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)

    def function(self, simulation, period):
        '''
        Somme totale des impôts moins restitutions et degrèvements
        '''
        period = period.start.offset('first-of', 'year').period('year')
        bouclier_imp_gen = simulation.calculate('bouclier_imp_gen', period)
        restitutions = simulation.calculate('restitutions', period)

        return period, -bouclier_imp_gen + restitutions


@reference_formula
class bouclier_fiscal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"bouclier_fiscal"
    start_date = date(2006, 1, 1)
    stop_date = date(2010, 12, 31)
    url = "http://fr.wikipedia.org/wiki/Bouclier_fiscal"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        bouclier_sumimp = simulation.calculate('bouclier_sumimp', period)
        bouclier_rev = simulation.calculate('bouclier_rev', period)
        P = simulation.legislation_at(period.start).bouclier_fiscal

        return period, max_(0, bouclier_sumimp - (bouclier_rev * P.taux))
