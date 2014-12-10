# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import int32, logical_not as not_, zeros

from .base import *


@reference_formula
class nb_par(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Familles
    label = u"Nombre de parents"

    def function(self, quifam_holder):
        '''
        Nombre d'adultes (parents) dans la famille
        'fam'
        '''
        quifam = self.filter_role(quifam_holder, role = PART)

        return 1 + 1 * (quifam == 1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class maries(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"maries"

    def function(self, statmarit_holder):
        '''
        couple = 1 si couple marié sinon 0 TODO faire un choix avec couple ?
        '''
        statmarit = self.filter_role(statmarit_holder, role = CHEF)

        return statmarit == 1

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class concub(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de vie en couple"

    def function(self, nb_par):
        '''
        concub = 1 si vie en couple TODO pas très heureux
        '''
        # TODO: concub n'est pas égal à 1 pour les conjoints
        return nb_par == 2

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class isol(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"isol"

    def function(self, nb_par):
        '''
        Parent (s'il y a lieu) isolé
        '''
        return nb_par == 1

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class etu(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Indicatrice individuelle étudiant"

    def function(self, activite):
        '''
        Indicatrice individuelle etudiant
        '''
        return activite == 2

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class smic55(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Indicatrice individuelle d'un salaire supérieur à 55% du smic"

    def function(self, salbrut, _P = law):
        nbh_travaillees = 151.67
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees
        return salbrut >= _P.fam.af.seuil_rev_taux * smic_mensuel_brut

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class br_pf_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Base ressource individuele des prestations familiales"

    def function(self, tspr, hsup, rpns):
        '''
        Base ressource individuelle des prestations familiales
        'ind'
        '''
        return tspr + hsup + rpns

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class biact(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de biactivité"

    def function(self, br_pf_i_holder, _P):
        '''
        Indicatrice de biactivité des adultes de la famille
        '''
        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])

        seuil_rev = 12 * _P.fam.af.bmaf_n_2
        biact = (br_pf_i[CHEF] >= seuil_rev) & (br_pf_i[PART] >= seuil_rev)
        return biact

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class div(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"div"

    def function(self, rpns_pvce, rpns_pvct, rpns_mvct, rpns_mvlt, f3vc_holder, f3ve_holder, f3vg_holder, f3vh_holder, f3vl_holder, f3vm_holder):
        f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
        f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
        f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
        f3vh = self.cast_from_entity_to_role(f3vh_holder, role = VOUS)
        f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
        f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)

        return f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class rev_coll(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_coll"

    def function(self, rto_net_declarant1, rev_cap_lib_holder, rev_cat_rvcm_holder, div, abat_spe_holder, glo, fon_holder, alv_declarant1, f7ga_holder, f7gb_holder, f7gc_holder, rev_cat_pv_holder):
        '''
        Revenus collectifs
        '''
        # TODO: ajouter les revenus de l'étranger etr*0.9
        # alv_declarant1 is negative since it is paid by the declaree
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
        rev_cat_rvcm = self.cast_from_entity_to_role(rev_cat_rvcm_holder, role = VOUS)
        abat_spe = self.cast_from_entity_to_role(abat_spe_holder, role = VOUS)
        fon = self.cast_from_entity_to_role(fon_holder, role = VOUS)
        f7ga = self.cast_from_entity_to_role(f7ga_holder, role = VOUS)
        f7gb = self.cast_from_entity_to_role(f7gb_holder, role = VOUS)
        f7gc = self.cast_from_entity_to_role(f7gc_holder, role = VOUS)
        rev_cat_pv = self.cast_from_entity_to_role(rev_cat_pv_holder, role = VOUS)

        return (rto_net_declarant1 + rev_cap_lib + rev_cat_rvcm + fon + glo + alv_declarant1 - f7ga - f7gb - f7gc - abat_spe
            + rev_cat_pv)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class br_pf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Base ressource des prestations familiales"

    def function(self, br_pf_i_holder, rev_coll_holder):
        '''
        Base ressource des prestations familiales de la famille
        'fam'
        '''
        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
        rev_coll = self.split_by_roles(rev_coll_holder, roles = [CHEF, PART])

        br_pf = br_pf_i[CHEF] + br_pf_i[PART] + rev_coll[CHEF] + rev_coll[PART]
        return br_pf

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class crds_pfam(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"CRDS (prestations familiales)"
    url = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"

    def function(self, af, cf, asf, ars, paje, ape, apje, _P):
        '''
        Renvoie la CRDS des prestations familiales
        '''
        return -(af + cf + asf + ars + paje + ape + apje) * _P.fam.af.crds

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



############################################################################
# Helper functions
############################################################################

def nb_enf(ages, smic55, ag1, ag2):
    """
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    """
#        Les allocations sont dues à compter du mois civil qui suit la naissance
#        ag1==0 ou suivant les anniversaires ag1>0.
#        Un enfant est reconnu à charge pour le versement des prestations
#        jusqu'au mois précédant son age limite supérieur (ag2 + 1) mais
#        le versement à lieu en début de mois suivant
    res = None
    for key, age in ages.iteritems():
        if res is None: res = zeros(len(age), dtype = int32)
        res += ((ag1 <= age) & (age <= ag2)) * not_(smic55[key])
    return res


def age_aine(ages, smic55, ag1, ag2):
    '''
    renvoi un vecteur avec l'âge de l'ainé (au sens des allocations
    familiales) de chaque famille
    '''
    ageaine = -9999
    for key, age in ages.iteritems():
        ispacaf = ((ag1 <= age) & (age <= ag2)) * not_(smic55[key])
        isaine = ispacaf & (age > ageaine)
        ageaine = isaine * age + not_(isaine) * ageaine
    return ageaine


def age_en_mois_benjamin(agems):
    '''
    renvoi un vecteur (une entree pour chaque famille) avec l'age du benjamin.  # TODO check agem > 0
    '''
    agem_benjamin = 12 * 9999
    for agem in agems.itervalues():
        isbenjamin = (agem < agem_benjamin) & (agem != -9999)
        agem_benjamin = isbenjamin * agem + not_(isbenjamin) * agem_benjamin
    return agem_benjamin
