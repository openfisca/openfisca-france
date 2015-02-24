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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import int32, logical_not as not_, zeros
from numpy.core.defchararray import startswith

from .base import *  # noqa


@reference_formula
class residence_guadeloupe(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '971')


@reference_formula
class residence_martinique(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '972')


@reference_formula
class residence_guyane(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '973')


@reference_formula
class residence_reunion(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '974')


@reference_formula
class residence_mayotte(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '976')


@reference_formula
class nb_par(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Familles
    label = u"Nombre d'adultes (parents) dans la famille"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        quifam_holder = simulation.compute('quifam', period)

        quifam = self.filter_role(quifam_holder, role = PART)

        return period, 1 + 1 * (quifam == PART)


@reference_formula
class maries(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"maries"

    def function(self, simulation, period):
        """couple = 1 si couple marié sinon 0 TODO faire un choix avec couple ?"""
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        statmarit_holder = simulation.compute('statmarit', period)

        statmarit = self.filter_role(statmarit_holder, role = CHEF)

        return period, statmarit == 1


@reference_formula
class concub(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de vie en couple"

    def function(self, simulation, period):
        '''
        concub = 1 si vie en couple TODO pas très heureux
        '''
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_par = simulation.calculate('nb_par', period)

        # TODO: concub n'est pas égal à 1 pour les conjoints
        return period, nb_par == 2


@reference_formula
class isol(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Parent (s'il y a lieu) isolé"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        nb_par = simulation.calculate('nb_par', period)

        return period, nb_par == 1


@reference_formula
class etu(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Indicatrice individuelle étudiant"

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        activite = simulation.calculate('activite', period)

        return period, activite == 2


@reference_formula
class smic55(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Indicatrice individuelle d'un salaire supérieur à 55% du smic"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        _P = simulation.legislation_at(period.start)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees
        return period, salaire_de_base >= _P.fam.af.seuil_rev_taux * smic_mensuel_brut


@reference_formula
class br_pf_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Base ressource individuelle des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        tspr = simulation.calculate('tspr', period)
        hsup = simulation.calculate('hsup', period)
        rpns = simulation.calculate('rpns', period)

        return period, tspr + hsup + rpns


@reference_formula
class biact(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de biactivité"

    def function(self, simulation, period):
        '''
        Indicatrice de biactivité des adultes de la famille
        '''
        period = period.start.offset('first-of', 'month').period('year')
        br_pf_i_holder = simulation.compute('br_pf_i', period)
        _P = simulation.legislation_at(period.start)

        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])

        seuil_rev = 12 * _P.fam.af.bmaf_n_2
        biact = (br_pf_i[CHEF] >= seuil_rev) & (br_pf_i[PART] >= seuil_rev)
        return period, biact


@reference_formula
class div(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"div"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        rpns_pvce = simulation.calculate('rpns_pvce', period)
        rpns_pvct = simulation.calculate('rpns_pvct', period)
        rpns_mvct = simulation.calculate('rpns_mvct', period)
        rpns_mvlt = simulation.calculate('rpns_mvlt', period)
        f3vc_holder = simulation.compute('f3vc', period)
        f3ve_holder = simulation.compute('f3ve', period)
        f3vg_holder = simulation.compute('f3vg', period)
        f3vh_holder = simulation.compute('f3vh', period)
        f3vl_holder = simulation.compute('f3vl', period)
        f3vm_holder = simulation.compute('f3vm', period)

        f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
        f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
        f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
        f3vh = self.cast_from_entity_to_role(f3vh_holder, role = VOUS)
        f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
        f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)

        return period, f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt


@reference_formula
class rev_coll(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Revenus collectifs"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        # Quand rev_coll est calculé sur une année glissante, rto_net_declarant1 est calculé sur l'année légale
        # correspondante.
        rto_net_declarant1 = simulation.calculate('rto_net_declarant1', period.offset('first-of'))
        rev_cap_lib_holder = simulation.compute('rev_cap_lib', period)
        rev_cat_rvcm_holder = simulation.compute('rev_cat_rvcm', period)
        div = simulation.calculate('div', period)
        abat_spe_holder = simulation.compute('abat_spe', period)
        glo = simulation.calculate('glo', period)
        fon_holder = simulation.compute('fon', period)
        # Quand rev_coll est calculé sur une année glissante, alv_declarant1 est calculé sur l'année légale
        # correspondante.
        alv_declarant1 = simulation.calculate('alv_declarant1', period.offset('first-of'))
        f7ga_holder = simulation.compute('f7ga', period)
        f7gb_holder = simulation.compute('f7gb', period)
        f7gc_holder = simulation.compute('f7gc', period)
        rev_cat_pv_holder = simulation.compute('rev_cat_pv', period)

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

        return period, (rto_net_declarant1 + rev_cap_lib + rev_cat_rvcm + fon + glo + alv_declarant1 - f7ga - f7gb - f7gc - abat_spe
            + rev_cat_pv)


@reference_formula
class br_pf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Base ressource des prestations familiales"

    def function(self, simulation, period):
        '''
        Base ressource des prestations familiales de la famille
        'fam'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        br_pf_i_holder = simulation.compute('br_pf_i', period)
        rev_coll_holder = simulation.compute('rev_coll', period)

        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
        rev_coll = self.split_by_roles(rev_coll_holder, roles = [CHEF, PART])

        br_pf = br_pf_i[CHEF] + br_pf_i[PART] + rev_coll[CHEF] + rev_coll[PART]
        return period, br_pf


@reference_formula
class crds_pfam(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"CRDS (prestations familiales)"
    url = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"

    def function(self, simulation, period):
        '''
        Renvoie la CRDS des prestations familiales
        '''
        period = period.start.offset('first-of', 'month').period('year')
        af = simulation.calculate_add('af', period)
        cf = simulation.calculate('cf', period)
        asf = simulation.calculate('asf', period)
        ars = simulation.calculate('ars', period)
        paje = simulation.calculate('paje', period)
        ape = simulation.calculate('ape', period)
        apje = simulation.calculate('apje', period)
        _P = simulation.legislation_at(period.start)

        return period, -(af + cf + asf + ars + paje + ape + apje) * _P.fam.af.crds


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
        res += (ag1 <= age) & (age <= ag2) & not_(smic55[key])
    return res


def age_aine(ages, smic55, ag1, ag2):
    '''
    Renvoie un vecteur avec l'âge de l'ainé (au sens des allocations
    familiales) de chaque famille
    '''
    ageaine = -9999
    for key, age in ages.iteritems():
        ispacaf = (ag1 <= age) & (age <= ag2) & not_(smic55[key])
        isaine = ispacaf & (age > ageaine)
        ageaine = isaine * age + not_(isaine) * ageaine
    return ageaine


def age_en_mois_benjamin(agems):
    '''
    Renvoie un vecteur (une entree pour chaque famille) avec l'age du benjamin.  # TODO check agem > 0
    '''
    agem_benjamin = 12 * 9999
    for agem in agems.itervalues():
        isbenjamin = (agem < agem_benjamin) & (agem != -9999)
        agem_benjamin = isbenjamin * agem + not_(isbenjamin) * agem_benjamin
    return agem_benjamin
