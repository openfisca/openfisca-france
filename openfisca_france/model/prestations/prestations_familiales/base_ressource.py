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

from numpy import int32, logical_not as not_, logical_or as or_, zeros


from ...base import *  # noqa analysis:ignore


@reference_formula
class smic55(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Indicatrice d'autonomie financière vis-à-vis des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salaire_net = simulation.calculate_add('salaire_net', period.start.period('month', 6).offset(-6))
        _P = simulation.legislation_at(period.start)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees

        # Oui on compare du salaire net avec un bout du SMIC brut ...
        return period, salaire_net / 6 >= (_P.fam.af.seuil_rev_taux * smic_mensuel_brut)


@reference_formula
class pfam_enfant_a_charge(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Enfant considéré à charge au sens des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        smic55 = simulation.calculate('smic55', period)
        age = simulation.calculate('age', period)
        rempli_obligation_scolaire = simulation.calculate('rempli_obligation_scolaire', period)

        pfam = simulation.legislation_at(period.start).fam

        condition_enfant = ((age >= pfam.enfants.age_minimal) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.enfants.age_limite) * not_(smic55)

        return period, or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


@reference_formula
class pfam_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ressources de l'individu prises en compte dans le cadre des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        br_pf_i = simulation.calculate('br_pf_i', period)
        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        pfam_enfant_a_charge = simulation.calculate('pfam_enfant_a_charge', period)

        return period, or_(not_(est_enfant_dans_famille), pfam_enfant_a_charge) * br_pf_i


@reference_formula
class br_pf_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Base ressource individuelle des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        annee_fiscale_n_2 = period.start.offset('first-of', 'year').period('year').offset(-2)

        tspr = simulation.calculate('tspr', annee_fiscale_n_2)
        hsup = simulation.calculate('hsup', annee_fiscale_n_2)
        rpns = simulation.calculate('rpns', annee_fiscale_n_2)

        return period, tspr + hsup + rpns


@reference_formula
class biact(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice de biactivité"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        annee_fiscale_n_2 = period.start.offset('first-of', 'year').period('year').offset(-2)

        br_pf_i_holder = simulation.compute('br_pf_i', period)
        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])

        pfam = simulation.legislation_at(annee_fiscale_n_2.start).fam
        seuil_rev = 12 * pfam.af.bmaf

        return period, (br_pf_i[CHEF] >= seuil_rev) & (br_pf_i[PART] >= seuil_rev)


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
        rev_cap_lib_holder = simulation.compute_add('rev_cap_lib', period)
        rev_cat_rvcm_holder = simulation.compute('rev_cat_rvcm', period)
        # div = simulation.calculate('div', period)  # TODO why is this variable not used ?
        abat_spe_holder = simulation.compute('abat_spe', period)
        glo = simulation.calculate('glo', period)
        fon_holder = simulation.compute('fon', period)
        # Quand rev_coll est calculé sur une année glissante, pensions_alimentaires_versees_declarant1 est calculé sur l'année légale
        # correspondante.
        pensions_alimentaires_versees_declarant1 = simulation.calculate('pensions_alimentaires_versees_declarant1', period.offset('first-of'))
        f7ga_holder = simulation.compute('f7ga', period)
        f7gb_holder = simulation.compute('f7gb', period)
        f7gc_holder = simulation.compute('f7gc', period)
        rev_cat_pv_holder = simulation.compute('rev_cat_pv', period)

        # TODO: ajouter les revenus de l'étranger etr*0.9
        # pensions_alimentaires_versees_declarant1 is negative since it is paid by the declaree
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
        rev_cat_rvcm = self.cast_from_entity_to_role(rev_cat_rvcm_holder, role = VOUS)
        abat_spe = self.cast_from_entity_to_role(abat_spe_holder, role = VOUS)
        fon = self.cast_from_entity_to_role(fon_holder, role = VOUS)
        f7ga = self.cast_from_entity_to_role(f7ga_holder, role = VOUS)
        f7gb = self.cast_from_entity_to_role(f7gb_holder, role = VOUS)
        f7gc = self.cast_from_entity_to_role(f7gc_holder, role = VOUS)
        rev_cat_pv = self.cast_from_entity_to_role(rev_cat_pv_holder, role = VOUS)

        return period, (rto_net_declarant1 + rev_cap_lib + rev_cat_rvcm + fon + glo + pensions_alimentaires_versees_declarant1 - f7ga - f7gb
            - f7gc - abat_spe + rev_cat_pv)


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
        period = period.start.offset('first-of', 'month').period('month')
        # period_legacy = period.start.offset('first-of', 'month').period('year')
        annee_fiscale_n_2 = period.start.offset('first-of', 'year').period('year').offset(-2)

        pfam_ressources_i_holder = simulation.compute('pfam_ressources_i', period)
        rev_coll_holder = simulation.compute('rev_coll', annee_fiscale_n_2)

        br_pf_i_total = self.sum_by_entity(pfam_ressources_i_holder)
        rev_coll = self.split_by_roles(rev_coll_holder, roles = [CHEF, PART])

        br_pf = br_pf_i_total + rev_coll[CHEF] + rev_coll[PART]
        return period, br_pf


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
        if res is None:
            res = zeros(len(age), dtype = int32)
        res += (ag1 <= age) & (age <= ag2) & not_(smic55[key])
    return res


def age_en_mois_benjamin(ages_en_mois):
    '''
    Renvoie un vecteur (une entree pour chaque famille) avec l'age du benjamin.  # TODO check age_en_mois > 0
    '''
    age_en_mois_benjamin = 12 * 9999
    for age_en_mois in ages_en_mois.itervalues():
        isbenjamin = (age_en_mois < age_en_mois_benjamin) & (age_en_mois != -9999)
        age_en_mois_benjamin = isbenjamin * age_en_mois + not_(isbenjamin) * age_en_mois_benjamin
    return age_en_mois_benjamin
