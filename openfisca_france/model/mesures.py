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

from numpy import floor, logical_not as not_

from .base import *  # noqa analysis:ignore


@reference_formula
class uc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Unités de consommation"

    def function(self, simulation, period):
        '''
        Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
        'men'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        age_en_mois_holder = simulation.compute('age_en_mois', period)

        age_en_mois = self.split_by_roles(age_en_mois_holder)

        uc_adt = 0.5
        uc_enf = 0.3
        uc = 0.5
        for agm in age_en_mois.itervalues():
            age = floor(agm / 12)
            adt = (15 <= age) & (age <= 150)
            enf = (0 <= age) & (age <= 14)
            uc += adt * uc_adt + enf * uc_enf
        return period, uc


@reference_formula
class typ_men(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Menages
    label = u"Type de ménage"

    def function(self, simulation, period):
        '''
        type de menage
        'men'
        TODO: prendre les enfants du ménage et non ceux de la famille
        '''
        period = period.start.offset('first-of', 'year').period('year')
        isol_holder = simulation.compute('isol', period)
        af_nbenf_holder = simulation.compute('af_nbenf', period)

        af_nbenf = self.cast_from_entity_to_role(af_nbenf_holder, role = CHEF)
        af_nbenf = self.sum_by_entity(af_nbenf)
        isol = self.cast_from_entity_to_role(isol_holder, role = CHEF)
        isol = self.sum_by_entity(isol)

        _0_kid = af_nbenf == 0
        _1_kid = af_nbenf == 1
        _2_kid = af_nbenf == 2
        _3_kid = af_nbenf >= 3

        return period, (0 * (isol & _0_kid) +  # Célibataire
                1 * (not_(isol) & _0_kid) +  # Couple sans enfants
                2 * (not_(isol) & _1_kid) +  # Couple un enfant
                3 * (not_(isol) & _2_kid) +  # Couple deux enfants
                4 * (not_(isol) & _3_kid) +  # Couple trois enfants et plus
                5 * (isol & _1_kid) +  # Famille monoparentale un enfant
                6 * (isol & _2_kid) +  # Famille monoparentale deux enfants
                7 * (isol & _3_kid))  # Famille monoparentale trois enfants et plus


@reference_formula
class revdisp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Revenu disponible du ménage"
    url = "http://fr.wikipedia.org/wiki/Revenu_disponible"

    def function(self, simulation, period):
        '''
        Revenu disponible - ménage
        'men'
        '''
        period = period.start.period('year').offset('first-of')
        rev_trav_holder = simulation.compute('rev_trav', period)
        pen_holder = simulation.compute('pen', period)
        rev_cap_holder = simulation.compute('rev_cap', period)
        psoc_holder = simulation.compute('psoc', period)
        ppe_holder = simulation.compute('ppe', period)
        impo = simulation.calculate('impo', period)

        pen = self.sum_by_entity(pen_holder)
        ppe = self.cast_from_entity_to_role(ppe_holder, role = VOUS)
        ppe = self.sum_by_entity(ppe)
        psoc = self.cast_from_entity_to_role(psoc_holder, role = CHEF)
        psoc = self.sum_by_entity(psoc)
        rev_cap = self.sum_by_entity(rev_cap_holder)
        rev_trav = self.sum_by_entity(rev_trav_holder)

        return period, rev_trav + pen + rev_cap + psoc + ppe + impo


@reference_formula
class nivvie(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Niveau de vie du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie du ménage
        'men'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        revdisp = simulation.calculate('revdisp', period)
        uc = simulation.calculate('uc', period)

        return period, revdisp / uc


@reference_formula
class revenu_net_individu(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu net de l'individu"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        pen = simulation.calculate('pen', period)
        rev_cap = simulation.calculate('rev_cap', period)
        rev_trav = simulation.calculate('rev_trav', period)

        return period, pen + rev_cap + rev_trav


@reference_formula
class revnet(PersonToEntityColumn):
    entity_class = Menages
    label = u"Revenu net du ménage"
    operation = 'add'
    url = u"http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php",
    variable = revenu_net_individu


@reference_formula
class nivvie_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Niveau de vie net du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie net du ménage
        'men'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        revnet = simulation.calculate('revnet', period)
        uc = simulation.calculate('uc', period)

        return period, revnet / uc


@reference_formula
class revenu_initial_individu(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu initial de l'individu"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        cotisations_employeur_contributives = simulation.calculate('cotisations_employeur_contributives', period)
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        pen = simulation.calculate('pen', period)
        rev_cap = simulation.calculate('rev_cap', period)
        rev_trav = simulation.calculate('rev_trav', period)

        return period, (rev_trav + pen + rev_cap - cotisations_employeur_contributives -
            cotisations_salariales_contributives)


@reference_formula
class revini(PersonToEntityColumn):
    entity_class = Menages
    label = u"Revenu initial du ménage"
    operation = 'add'
    variable = revenu_initial_individu


@reference_formula
class nivvie_ini(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Niveau de vie initial du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie initial du ménage
        'men'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        revini = simulation.calculate('revini', period)
        uc = simulation.calculate('uc', period)

        return period, revini / uc


def _revprim(rev_trav, cho, rev_cap, cotisations_employeur, cotisations_salariales):
    '''
    Revenu primaire du ménage
    Ensemble des revenus d'activités superbruts avant tout prélèvement
    Il est égale à la valeur ajoutée produite par les résidents
    'men'
    '''
    return rev_trav + rev_cap - cotisations_employeur - cotisations_salariales - cho


@reference_formula
class rev_trav(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Revenus du travail (salariés et non salariés)"
    url = "http://fr.wikipedia.org/wiki/Revenu_du_travail"

    def function(self, simulation, period):
        '''
        Revenu du travail
        '''
        period = period.start.offset('first-of', 'year').period('year')
        rev_sal = simulation.calculate('rev_sal', period)
        rag = simulation.calculate('rag', period)
        ric = simulation.calculate('ric', period)
        rnc = simulation.calculate('rnc', period)

        return period, rev_sal + rag + ric + rnc


@reference_formula
class pen(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Total des pensions et revenus de remplacement"
    url = "http://fr.wikipedia.org/wiki/Rente"

    def function(self, simulation, period):
        '''
        Pensions
        '''
        period = period.start.period('year').offset('first-of')
        chonet = simulation.calculate('chonet', period)
        rstnet = simulation.calculate('rstnet', period)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
        pensions_alimentaires_versees_declarant1 = simulation.calculate(
            'pensions_alimentaires_versees_declarant1', period
            )
        rto_declarant1 = simulation.calculate_add('rto_declarant1', period)

        return period, (chonet + rstnet + pensions_alimentaires_percues + pensions_alimentaires_versees_declarant1 +
                    rto_declarant1)


@reference_formula
class cotsoc_bar_declarant1(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Cotisations sociales sur les revenus du capital imposés au barème"

    def function(self, simulation, period):
        '''
        Cotisations sociales sur les revenus du capital imposés au barème
        '''
        period = period.start.period('year').offset('first-of')
        csg_cap_bar_declarant1 = simulation.calculate('csg_cap_bar_declarant1', period)
        prelsoc_cap_bar_declarant1 = simulation.calculate('prelsoc_cap_bar_declarant1', period)
        crds_cap_bar_declarant1 = simulation.calculate('crds_cap_bar_declarant1', period)

        return period, csg_cap_bar_declarant1 + prelsoc_cap_bar_declarant1 + crds_cap_bar_declarant1


@reference_formula
class cotsoc_lib_declarant1(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire"

    def function(self, simulation, period):
        '''
        Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire
        '''
        period = period.start.offset('first-of', 'year').period('year')
        csg_cap_lib_declarant1 = simulation.calculate('csg_cap_lib_declarant1', period)
        prelsoc_cap_lib_declarant1 = simulation.calculate('prelsoc_cap_lib_declarant1', period)
        crds_cap_lib_declarant1 = simulation.calculate('crds_cap_lib_declarant1', period)

        return period, csg_cap_lib_declarant1 + prelsoc_cap_lib_declarant1 + crds_cap_lib_declarant1


@reference_formula
class rev_cap(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Revenus du patrimoine"
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    def function(self, simulation, period):
        '''
        Revenus du patrimoine
        '''
        period = period.start.offset('first-of', 'year').period('year')
        fon_holder = simulation.compute('fon', period)
        rev_cap_bar_holder = simulation.compute_add('rev_cap_bar', period)
        cotsoc_bar_declarant1 = simulation.calculate('cotsoc_bar_declarant1', period)
        rev_cap_lib_holder = simulation.compute_add('rev_cap_lib', period)
        cotsoc_lib_declarant1 = simulation.calculate('cotsoc_lib_declarant1', period)
        imp_lib_holder = simulation.compute('imp_lib', period)
        rac = simulation.calculate('rac', period)

        fon = self.cast_from_entity_to_role(fon_holder, role = VOUS)
        imp_lib = self.cast_from_entity_to_role(imp_lib_holder, role = VOUS)
        rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

        return period, fon + rev_cap_bar + cotsoc_bar_declarant1 + rev_cap_lib + cotsoc_lib_declarant1 + imp_lib + rac


@reference_formula
class psoc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Total des prestations sociales"
    url = "http://fr.wikipedia.org/wiki/Prestation_sociale"

    def function(self, simulation, period):
        '''
        Prestations sociales
        '''
        period = period.start.offset('first-of', 'year').period('year')
        pfam = simulation.calculate('pfam', period)
        mini = simulation.calculate('mini', period)
        aides_logement = simulation.calculate('aides_logement', period)

        return period, pfam + mini + aides_logement


@reference_formula
class pfam(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Total des prestations familiales"
    url = "http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html"

    def function(self, simulation, period):
        '''
        Prestations familiales
        '''
        period = period.start.offset('first-of', 'year').period('year')
        af = simulation.calculate_add('af', period)
        cf = simulation.calculate_add('cf', period)
        ars = simulation.calculate('ars', period)
        aeeh = simulation.calculate('aeeh', period)
        paje = simulation.calculate_add('paje', period)
        asf = simulation.calculate_add('asf', period)
        crds_pfam = simulation.calculate('crds_pfam', period)

        return period, af + cf + ars + aeeh + paje + asf + crds_pfam


@reference_formula
class mini(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Minima sociaux"
    url = "http://fr.wikipedia.org/wiki/Minima_sociaux"

    def function(self, simulation, period):
        '''
        Minima sociaux
        '''
        period = period.start.offset('first-of', 'year').period('year')
        aspa = simulation.calculate_add('aspa', period)
        aah_holder = simulation.compute_add('aah', period)
        caah_holder = simulation.compute_add('caah', period)
        asi = simulation.calculate_add('asi', period)
        rsa = simulation.calculate_add('rsa', period)
        aefa = simulation.calculate('aefa', period)
        api = simulation.calculate('api', period)
        ass = simulation.calculate_add('ass', period)
        psa = simulation.calculate_add('psa', period)

        aah = self.sum_by_entity(aah_holder)
        caah = self.sum_by_entity(caah_holder)

        return period, aspa + aah + caah + asi + rsa + aefa + api + ass + psa


@reference_formula
class aides_logement(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocations logements"
    url = "http://vosdroits.service-public.fr/particuliers/N20360.xhtml"

    def function(self, simulation, period):
        '''
        Prestations logement
        '''
        period = period.start.offset('first-of', 'year').period('year')
        apl = simulation.calculate_add('apl', period)
        als = simulation.calculate_add('als', period)
        alf = simulation.calculate_add('alf', period)
        crds_logement = simulation.calculate_add('crds_logement', period)

        return period, apl + als + alf + crds_logement


@reference_formula
class impo(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Impôts sur le revenu"
    url = "http://fr.wikipedia.org/wiki/Imp%C3%B4t_direct"

    def function(self, simulation, period):
        '''
        Impôts directs
        '''
        period = period.start.offset('first-of', 'year').period('year')
        irpp_holder = simulation.compute('irpp', period)
        taxe_habitation = simulation.calculate('taxe_habitation', period)

        irpp = self.cast_from_entity_to_role(irpp_holder, role = VOUS)
        irpp = self.sum_by_entity(irpp)

        return period, irpp + taxe_habitation


@reference_formula
class crds(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Total des contributions au remboursement de la dette sociale"

    def function(self, simulation, period):
        """Contribution au remboursement de la dette sociale"""
        period = period.start.offset('first-of', 'year').period('year')
        crds_salaire = simulation.calculate_add('crds_salaire', period)
        crds_retraite = simulation.calculate_add('crds_retraite', period)
        crds_chomage = simulation.calculate_add('crds_chomage', period)
        crds_fon_holder = simulation.compute('crds_fon', period)
        crds_cap_bar_declarant1 = simulation.calculate('crds_cap_bar_declarant1', period)
        crds_cap_lib_declarant1 = simulation.calculate('crds_cap_lib_declarant1', period)
        crds_pfam_holder = simulation.compute('crds_pfam', period)
        crds_logement_holder = simulation.compute_add('crds_logement', period)
        crds_mini_holder = simulation.compute_add('crds_mini', period)
        crds_pv_mo_holder = simulation.compute('crds_pv_mo', period)
        crds_pv_immo_holder = simulation.compute('crds_pv_immo', period)

        crds_fon = self.cast_from_entity_to_role(crds_fon_holder, role = VOUS)
        crds_logement = self.cast_from_entity_to_role(crds_logement_holder, role = CHEF)
        crds_mini = self.cast_from_entity_to_role(crds_mini_holder, role = CHEF)
        crds_pfam = self.cast_from_entity_to_role(crds_pfam_holder, role = CHEF)
        crds_pv_immo = self.cast_from_entity_to_role(crds_pv_immo_holder, role = VOUS)
        crds_pv_mo = self.cast_from_entity_to_role(crds_pv_mo_holder, role = VOUS)

        return period, (crds_salaire + crds_retraite + crds_chomage +
                crds_fon + crds_cap_bar_declarant1 + crds_cap_lib_declarant1 + crds_pv_mo + crds_pv_immo +
                crds_pfam + crds_logement + crds_mini)


@reference_formula
class csg(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Total des contributions sociale généralisée"

    def function(self, simulation, period):
        """Contribution sociale généralisée"""
        period = period.start.offset('first-of', 'year').period('year')
        csg_imposable_salaire = simulation.calculate_add('csg_imposable_salaire', period)
        csg_deductible_salaire = simulation.calculate_add('csg_deductible_salaire', period)
        csg_imposable_chomage = simulation.calculate_add('csg_imposable_chomage', period)
        csg_deductible_chomage = simulation.calculate_add('csg_deductible_chomage', period)
        csg_imposable_retraite = simulation.calculate_add('csg_imposable_retraite', period)
        csg_deductible_retraite = simulation.calculate_add('csg_deductible_retraite', period)
        csg_fon_holder = simulation.compute('csg_fon', period)
        csg_cap_lib_declarant1 = simulation.calculate('csg_cap_lib_declarant1', period)
        csg_cap_bar_declarant1 = simulation.calculate('csg_cap_bar_declarant1', period)
        csg_pv_mo_holder = simulation.compute('csg_pv_mo', period)
        csg_pv_immo_holder = simulation.compute('csg_pv_immo', period)

        csg_fon = self.cast_from_entity_to_role(csg_fon_holder, role = VOUS)
        csg_pv_immo = self.cast_from_entity_to_role(csg_pv_immo_holder, role = VOUS)
        csg_pv_mo = self.cast_from_entity_to_role(csg_pv_mo_holder, role = VOUS)

        return period, (csg_imposable_salaire + csg_deductible_salaire + csg_imposable_chomage +
                csg_deductible_chomage + csg_imposable_retraite + csg_deductible_retraite + csg_fon +
                csg_cap_lib_declarant1 + csg_pv_mo + csg_pv_immo + csg_cap_bar_declarant1)


@reference_formula
class cotsoc_noncontrib(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Cotisations sociales non contributives"

    def function(self, simulation, period):
        '''
        Cotisations sociales non contributives (hors prelsoc_cap_lib, prelsoc_cap_bar)
        '''
        period = period.start.offset('first-of', 'year').period('year')
        cotisations_employeur_non_contributives = simulation.calculate('cotisations_employeur_non_contributives',
            period)
        cotisations_salariales_non_contributives = simulation.calculate('cotisations_salariales_non_contributives',
            period)

        return period, cotisations_employeur_non_contributives + cotisations_salariales_non_contributives


@reference_formula
class prelsoc_cap(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Prélèvements sociaux sur les revenus du capital"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"

    def function(self, simulation, period):
        """
        Prélèvements sociaux sur les revenus du capital
        """
        period = period.start.offset('first-of', 'year').period('year')
        prelsoc_fon_holder = simulation.compute('prelsoc_fon', period)
        prelsoc_cap_lib_declarant1 = simulation.calculate('prelsoc_cap_lib_declarant1', period)
        prelsoc_cap_bar_declarant1 = simulation.calculate('prelsoc_cap_bar_declarant1', period)
        prelsoc_pv_mo_holder = simulation.compute('prelsoc_pv_mo', period)
        prelsoc_pv_immo_holder = simulation.compute('prelsoc_pv_immo', period)

        prelsoc_fon = self.cast_from_entity_to_role(prelsoc_fon_holder, role = VOUS)
        prelsoc_pv_immo = self.cast_from_entity_to_role(prelsoc_pv_immo_holder, role = VOUS)
        prelsoc_pv_mo = self.cast_from_entity_to_role(prelsoc_pv_mo_holder, role = VOUS)

        return period, (prelsoc_fon + prelsoc_cap_lib_declarant1 + prelsoc_cap_bar_declarant1 + prelsoc_pv_mo +
                    prelsoc_pv_immo)


@reference_formula
class check_csk(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"check_csk"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        prelsoc_cap_bar_declarant1_holder = simulation.compute('prelsoc_cap_bar_declarant1', period)
        prelsoc_pv_mo_holder = simulation.compute('prelsoc_pv_mo', period)
        prelsoc_fon_holder = simulation.compute('prelsoc_fon', period)

        prelsoc_cap_bar = self.sum_by_entity(prelsoc_cap_bar_declarant1_holder)
        prelsoc_pv_mo = self.cast_from_entity_to_role(prelsoc_pv_mo_holder, role = CHEF)
        prelsoc_pv_mo = self.sum_by_entity(prelsoc_pv_mo)
        prelsoc_fon = self.cast_from_entity_to_role(prelsoc_fon_holder, role = CHEF)
        prelsoc_fon = self.sum_by_entity(prelsoc_fon)

        return period, prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_fon


@reference_formula
class check_csg(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"check_csg"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        csg_cap_bar_declarant1_holder = simulation.compute('csg_cap_bar_declarant1', period)
        csg_pv_mo_holder = simulation.compute('csg_pv_mo', period)
        csg_fon_holder = simulation.compute('csg_fon', period)

        csg_cap_bar = self.sum_by_entity(csg_cap_bar_declarant1_holder)
        csg_pv_mo = self.cast_from_entity_to_role(csg_pv_mo_holder, role = CHEF)
        csg_pv_mo = self.sum_by_entity(csg_pv_mo)
        csg_fon = self.cast_from_entity_to_role(csg_fon_holder, role = CHEF)
        csg_fon = self.sum_by_entity(csg_fon)

        return period, csg_cap_bar + csg_pv_mo + csg_fon


@reference_formula
class check_crds(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"check_crds"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        crds_cap_bar_declarant1_holder = simulation.compute('crds_cap_bar_declarant1', period)
        crds_pv_mo_holder = simulation.compute('crds_pv_mo', period)
        crds_fon_holder = simulation.compute('crds_fon', period)

        crds_cap_bar = self.sum_by_entity(crds_cap_bar_declarant1_holder)
        crds_pv_mo = self.cast_from_entity_to_role(crds_pv_mo_holder, role = CHEF)
        crds_pv_mo = self.sum_by_entity(crds_pv_mo)
        crds_fon = self.cast_from_entity_to_role(crds_fon_holder, role = CHEF)
        crds_fon = self.sum_by_entity(crds_fon)

        return period, crds_cap_bar + crds_pv_mo + crds_fon
