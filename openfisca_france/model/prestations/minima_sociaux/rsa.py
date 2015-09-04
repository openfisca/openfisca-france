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

from numpy import (floor, logical_and as and_, logical_not as not_, logical_or as or_, maximum as max_, minimum as min_)

from ...base import *  # noqa analysis:ignore
from ..prestations_familiales.base_ressource import nb_enf, age_en_mois_benjamin


@reference_formula
class aefa(DatedFormulaColumn):
    '''
    Aide exceptionelle de fin d'année (prime de Noël)
    Instituée en 1998
    Apparaît sous le nom de complément de rmi dans les ERF
    Le montant de l’aide mentionnée à l’article 1er versée aux bénéficiaires de l’allocation de solidarité
    spécifique à taux majoré servie aux allocataires âgés de cinquante-cinq ans ou plus justifiant de vingt années
    d’activité salariée, aux allocataires âgés de cinquante-sept ans et demi ou plus justifiant de dix années d’activité
    salariée ainsi qu’aux allocataires justifiant d’au moins 160 trimestres validés dans les régimes d’assurance
    vieillesse ou de périodes reconnues équivalentes est égal à
    Pour bénéficier de la Prime de Noël 2011, vous devez être éligible pour le compte du mois de novembre 2011
    ou au plus de décembre 2011, soit d’une allocation de solidarité spécifique (ASS), de la prime forfaitaire mensuelle
    de reprise d'activité, de l'allocation équivalent retraite (allocataire AER), du revenu de solidarité active
    (Bénéficiaires RSA), de l'allocation de parent isolé (API), du revenu minimum d'insertion (RMI), de l’Allocation
    pour la Création ou la Reprise d'Entreprise (ACCRE-ASS) ou encore allocation chômage.
    '''
    column = FloatCol
    entity_class = Familles
    label = u"Aide exceptionelle de fin d'année (prime de Noël)"
    url = u"http://www.pole-emploi.fr/candidat/aide-exceptionnelle-de-fin-d-annee-dite-prime-de-noel--@/suarticle.jspz?id=70996"  # noqa

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_2009__(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_par = simulation.calculate('nb_par', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate_add('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, smic55, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_par == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_par <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_par = simulation.calculate('nb_par', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, smic55, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_par == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_par <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa += condition * P.forf2008
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function__2008_(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_par = simulation.calculate('nb_par', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, smic55, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_par == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_par <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa


@reference_formula
class api(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation de parent isolé"
    url = u"http://fr.wikipedia.org/wiki/Allocation_de_parent_isol%C3%A9",

    @dated_function(stop = date(2009, 5, 31))
    def function__2009(self, simulation, period):
        """
        Allocation de parent isolé
        """
        period = period.start.offset('first-of', 'month').period('month')
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        isol = simulation.calculate('isol', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        br_rmi = simulation.calculate('br_rmi', period)
        af_majo = simulation.calculate('af_majo', period)
        rsa = simulation.calculate('rsa', period)
        af = simulation.legislation_at(period.start).fam.af
        api = simulation.legislation_at(period.start).minim.api

        age = self.split_by_roles(age_holder, roles = ENFS)
        age_en_mois = self.split_by_roles(age_en_mois_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        # TODO:
        #    Majoration pour isolement
        #    Si vous êtes parent isolé, c’est-à-dire célibataire, divorcé(e), séparé(e) ou veuf(ve) avec des enfants
        #    à charge ou enceinte, le montant forfaitaire garanti est majoré.
        #    Ce montant forfaitaire majoré est accordé à partir du mois au cours duquel survient l'un des événements
        #    suivants :
        #    - déclaration de grossesse,
        #    - naissance d'un enfant,
        #    - prise en charge d'un enfant,
        #    - séparation, veuvage,
        #    - dépôt de la demande si l’événement est antérieur.
        #
        #    Le montant forfaitaire majoré peut être accordé pendant 12 mois, continus ou discontinus, au cours
        #    d’une période de 18 mois suivant l’événement.
        #    Si votre plus jeune enfant à charge a moins de 3 ans, le montant forfaitaire majoré vous est accordé
        #    jusqu'à ses 3 ans.
        benjamin = age_en_mois_benjamin(age_en_mois)
        enceinte = (benjamin < 0) * (benjamin > -6)
        # TODO: quel mois mettre ?
        # TODO: pas complètement exact
        # L'allocataire perçoit l'API :
        # jusqu'�� ce que le plus jeune enfant ait 3 ans,
        # ou pendant 12 mois consécutifs si les enfants sont âgés de plus de 3 ans
        #    et s'il a présenté sa demande dans les 6 mois à partir du moment où il
        #    assure seul la charge de l'enfant.
        # TODO: API courte gens pour les gens qui ont divorcés dans l'année
        # Le droit à l'allocation est réétudié tous les 3 mois.
        # # Calcul de l'année et mois de naissance du benjamin

        condition = (floor(benjamin / 12) <= api.age - 1)
        eligib = isol * ((enceinte != 0) | (nb_enf(age, smic55, 0, api.age - 1) > 0)) * condition

        # moins de 20 ans avant inclusion dans rsa
        # moins de 25 ans après inclusion dans rsa
        api1 = eligib * af.bmaf * (api.base + api.enf_sup * nb_enf(age, smic55, af.age1, api.age_pac - 1))
        rsa = (api.age_pac >= 25)  # dummy passage au rsa majoré
        br_api = br_rmi + af_majo * not_(rsa)
        # On pourrait mensualiser RMI, BRrmi et forfait logement
        api = max_(0, api1 - rsa_forfait_logement / 12 - br_api / 12 - rsa / 12)
        # L'API est exonérée de CRDS
        return period, api  # annualisé
        # TODO API: temps partiel qui modifie la base ressource
        # Cumul
        # Cumul avec un revenu
        # Si l'allocataire reprend une activité ou suit une formation professionnelle rémunérée, les revenus sont
        # cumulables intégralement au cours des 3 premiers mois de reprise d'activité.
        # Du 4e au 12e mois qui suit, le montant de l'allocation varie en fonction de la durée de l'activité
        # ou de la formation.
        # Durée d'activité de 78 heures ou plus par mois ou activité non salariée
        # Lorsque la durée d'activité est de 78 heures minimum par mois, le montant de l'API perçu par l'allocataire est
        # diminué de la totalité du salaire. Tous les revenus d'activité sont pris en compte pour le calcul de l'API,
        # sauf si l'allocataire perçoit des revenus issus d'un contrat insertion-revenu minimum d'activité (CIRMA)
        # ou d'un contrat d'avenir (CAV).
        # L'allocataire peut bénéficier, sous certaines conditions :
        # • de la prime de retour à l'emploi si son activité est d'une durée d'au moins 4 mois consécutifs,
        # sauf s'il effectue un stage de formation professionnelle,
        # • de la prime forfaitaire pendant 9 mois, sauf s'il exerce une activité salariée dans le cadre d'un CIRMA
        # ou d'un CAV.
        # Durée d'activité de moins de 78 heures par mois
        # Lorsque la durée d'activité est inférieure à 78 heures par mois, le montant de l'API perçu par l'allocataire
        # est diminué de la moitié du salaire.
        # Si l'allocataire exerce une activité dans le cadre d'un CIRMA ou d'un CAV, ses revenus d'activité ne sont pas
        # pris en compte pour le calcul de son API.


@reference_formula
class br_rmi(DatedFormulaColumn):
    column = FloatCol
    label = u"Base ressources du Rmi ou du Rsa"
    entity_class = Familles

    @dated_function(stop = date(2009, 5, 31))
    def function_rmi(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        br_rmi_pf = simulation.calculate('br_rmi_pf', period)
        br_rmi_ms = simulation.calculate('br_rmi_ms', period)
        br_rmi_i_holder = simulation.compute('br_rmi_i', period)

        br_rmi_i_total = self.sum_by_entity(br_rmi_i_holder)
        return period, br_rmi_pf + br_rmi_ms + br_rmi_i_total

    @dated_function(start = date(2009, 6, 1))
    def function_rsa(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        br_rmi_pf = simulation.calculate('br_rmi_pf', period)
        br_rmi_ms = simulation.calculate('br_rmi_ms', period)
        br_rmi_i_holder = simulation.compute('br_rmi_i', period)
        ra_rsa_i_holder = simulation.compute('ra_rsa_i', period)

        br_rmi_i_total = self.sum_by_entity(br_rmi_i_holder)
        ra_rsa_i_total = self.sum_by_entity(ra_rsa_i_holder)
        return period, br_rmi_pf + br_rmi_ms + br_rmi_i_total + ra_rsa_i_total


@reference_formula
class br_rmi_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressource individuelle du RSA/RMI (hors revenus d'actvité)"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        three_previous_months = period.start.period('month', 3).offset(-3)

        r = rsa_ressource_calculator(simulation, period)

        # Ressources professionelles
        chonet = r.calcule_ressource('chonet', revenu_pro = True)
        rstnet = r.calcule_ressource('rstnet', revenu_pro = True)

        pensions_alimentaires_percues = r.calcule_ressource('pensions_alimentaires_percues')
        allocation_aide_retour_emploi = r.calcule_ressource('allocation_aide_retour_emploi')
        allocation_securisation_professionnelle = r.calcule_ressource('allocation_securisation_professionnelle')
        prestation_compensatoire = r.calcule_ressource('prestation_compensatoire')
        rto_declarant1 = r.calcule_ressource('rto_declarant1')
        rfon_ms = r.calcule_ressource('rfon_ms')
        div_ms = r.calcule_ressource('div_ms')
        gains_exceptionnels = r.calcule_ressource('gains_exceptionnels')
        dedommagement_victime_amiante = r.calcule_ressource('dedommagement_victime_amiante')
        pensions_invalidite = r.calcule_ressource('pensions_invalidite')
        rsa_base_ressources_patrimoine_i = r.calcule_ressource('rsa_base_ressources_patrimoine_i')

        rev_cap_bar_holder = simulation.compute_add('rev_cap_bar', three_previous_months)
        rev_cap_lib_holder = simulation.compute_add('rev_cap_lib', three_previous_months)
        rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

        result = (
            chonet + rstnet + pensions_alimentaires_percues + rto_declarant1 + rev_cap_bar +
            rev_cap_lib + rfon_ms + div_ms +
            gains_exceptionnels + dedommagement_victime_amiante + pensions_invalidite + allocation_aide_retour_emploi +
            allocation_securisation_professionnelle + prestation_compensatoire +
            rsa_base_ressources_patrimoine_i
        ) / 3

        return period, result


@reference_formula
class br_rmi_ms(SimpleFormulaColumn):
    column = FloatCol
    label = u"Minima sociaux inclus dans la base ressource RSA/RMI"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        three_previous_months = period.start.period('month', 3).offset(-3)
        aspa = simulation.calculate('aspa', period)
        asi = simulation.calculate('asi', period)
        ass = simulation.calculate('ass', period)
        aah_holder = simulation.compute_add('aah', three_previous_months)
        caah_holder = simulation.compute_add('caah', three_previous_months)

        aah = self.sum_by_entity(aah_holder) / 3
        caah = self.sum_by_entity(caah_holder) / 3

        return period, aspa + asi + ass + aah + caah


@reference_formula
class br_rmi_pf(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Prestations familiales inclues dans la base ressource RSA/RMI"

    @dated_function(date(2002, 1, 1), date(2003, 12, 31))
    def function_2002(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_base = simulation.calculate('af_base', period)
        cf = simulation.calculate_divide('cf', period)
        asf = simulation.calculate('asf', period)
        apje = simulation.calculate_divide('apje', period)
        ape = simulation.calculate_divide('ape', period)
        P = simulation.legislation_at(period.start).minim

        return period, P.rmi.pfInBRrmi * (af_base + cf + asf + apje + ape)

    @dated_function(start = date(2004, 1, 1), stop = date(2014, 3, 31))
    def function_2003(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_base = simulation.calculate('af_base', period)
        cf = simulation.calculate_divide('cf', period)
        asf = simulation.calculate_divide('asf', period)
        paje_base = simulation.calculate_divide('paje_base', period)
        paje_clca = simulation.calculate_divide('paje_clca', period)
        paje_prepare = simulation.calculate_divide('paje_prepare', period)
        paje_colca = simulation.calculate_divide('paje_colca', period)
        P = simulation.legislation_at(period.start).minim

        return period, P.rmi.pfInBRrmi * (af_base + cf + asf + paje_base + paje_clca + paje_prepare + paje_colca)

    @dated_function(start = date(2014, 4, 1))
    def function_2014(self, simulation, period):
        # TODO : Neutraliser les ressources de type prestations familiales quand elles sont interrompues
        period = period.start.offset('first-of', 'month').period('month')
        af_base = simulation.calculate('af_base', period)
        cf_non_majore_avant_cumul = simulation.calculate('cf_non_majore_avant_cumul', period)
        cf = simulation.calculate('cf', period)
        rsa_forfait_asf = simulation.calculate('rsa_forfait_asf', period)
        paje_base = simulation.calculate_divide('paje_base', period)
        paje_clca = simulation.calculate_divide('paje_clca', period)
        paje_prepare = simulation.calculate_divide('paje_prepare', period)
        paje_colca = simulation.calculate_divide('paje_colca', period)
        P = simulation.legislation_at(period.start).minim

        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul

        return period, P.rmi.pfInBRrmi * (af_base + rsa_forfait_asf + cf_non_majore + paje_base + paje_clca +
            paje_prepare + paje_colca)


@reference_formula
class crds_mini(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"CRDS versée sur les minimas sociaux"

    @dated_function(start = date(2009, 6, 1))
    def function_2009_(self, simulation, period):
        """
        CRDS sur les minima sociaux
        """
        period = period.start.offset('first-of', 'month').period('month')
        rsa_act = simulation.calculate('rsa_act', period)
        taux_crds = simulation.legislation_at(period.start).fam.af.crds

        return period, - taux_crds * rsa_act


@reference_formula
class div_ms(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        period_declaration = period.start.offset('first-of', 'year').period('year')
        f3vc_holder = simulation.compute('f3vc', period_declaration)
        f3ve_holder = simulation.compute('f3ve', period_declaration)
        f3vg_holder = simulation.compute('f3vg', period_declaration)
        f3vl_holder = simulation.compute('f3vl', period_declaration)
        f3vm_holder = simulation.compute('f3vm', period_declaration)

        f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
        f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
        f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
        f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
        f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)

        return period, (f3vc + f3ve + f3vg + f3vl + f3vm) / 12


@reference_formula
class enceinte_fam(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        period = period
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        enceinte_holder = simulation.compute('enceinte', period)

        age_en_mois_enf = self.split_by_roles(age_en_mois_holder, roles = ENFS)
        enceinte = self.split_by_roles(enceinte_holder, roles = [CHEF, PART])

        benjamin = age_en_mois_benjamin(age_en_mois_enf)
        enceinte_compat = and_(benjamin < 0, benjamin > -6)
        return period, or_(or_(enceinte_compat, enceinte[CHEF]), enceinte[PART])


@reference_formula
class nb_enfant_rsa(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Nombre d'enfants pris en compte pour le calcul du RSA"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rmi = simulation.legislation_at(period.start).minim.rmi
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        age_enf = self.split_by_roles(age_holder, roles = ENFS)
        smic55_enf = self.split_by_roles(smic55_holder, roles = ENFS)
        nbenf = nb_enf(age_enf, smic55_enf, 0, rmi.age_pac)

        return period, nbenf


@reference_formula
class psa(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Prime de solidarité active"
    url = u"http://www.service-public.fr/actualites/001077.html"

    @dated_function(start = date(2009, 4, 1), stop = date(2009, 4, 30))
    def function_2009(self, simulation, period):
        '''
        Prime de solidarité active (exceptionnelle, 200€ versés une fois en avril 2009)
        Versement en avril 2009 d’une prime de solidarité active (Psa) aux familles modestes qui ont bénéficié
        en janvier, février ou mars 2009 du Rmi, de l’Api (du Rsa expérimental, du Cav ou du Rma pour
        les ex-bénéficiaires du Rmi ou de l’Api), de la prime forfaitaire mensuelle au titre du Rmi ou de l’Api
        ou enfin d’une aide au logement (à condition d’exercer une activité professionnelle et
        d’être âgé de plus de 25 ans ou d’avoir au moins un enfant à charge).
        La Psa, prime exceptionnelle, s’élève à 200 euros par foyer bénéficiaire.
        '''
        period = period.start.offset('first-of', 'month').period('month')
        api = simulation.calculate('api', period)
        rsa = simulation.calculate('rsa', period)
        activite_holder = simulation.compute('activite', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        aide_logement = simulation.calculate('aide_logement', period)
        P = simulation.legislation_at(period.start).minim.rmi

        activite = self.split_by_roles(activite_holder, roles = [CHEF, PART])
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        dummy_al = and_(aide_logement > 0, or_(af_nbenf > 0, or_(activite[CHEF] == 0, activite[PART] == 0)))
        condition = (dummy_api + dummy_rmi + dummy_al > 0)
        psa = condition * P.psa
        return period, psa


@reference_formula
class ra_rsa(SimpleFormulaColumn):
    column = FloatCol
    label = u"Revenus d'activité du RSA"
    entity_class = Familles
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        ra_rsa_i_holder = simulation.compute('ra_rsa_i', period)

        ra_rsa = self.sum_by_entity(ra_rsa_i_holder)
        return period, ra_rsa


@reference_formula
class ra_rsa_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Revenus d'activité du Rsa - Individuel"
    entity_class = Individus
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        r = rsa_ressource_calculator(simulation, period)

        salaire_net = r.calcule_ressource('salaire_net', revenu_pro = True)
        indemnites_journalieres = r.calcule_ressource('indemnites_journalieres', revenu_pro = True)
        indemnites_chomage_partiel = r.calcule_ressource('indemnites_chomage_partiel', revenu_pro = True)
        indemnites_volontariat = r.calcule_ressource('indemnites_volontariat', revenu_pro = True)
        revenus_stage_formation_pro = r.calcule_ressource('revenus_stage_formation_pro', revenu_pro = True)
        indemnites_stage = r.calcule_ressource('indemnites_stage', revenu_pro = True)
        bourse_recherche = r.calcule_ressource('bourse_recherche', revenu_pro = True)
        hsup = r.calcule_ressource('hsup', revenu_pro = True)
        etr = r.calcule_ressource('etr', revenu_pro = True)

        # Ressources TNS

        # WARNING : D'après les caisses, le revenu pris en compte pour les AE pour le RSA ne prend en compte que
        # l'abattement standard sur le CA, mais pas les cotisations pour charges sociales. Dans l'attente d'une
        # éventuelle correction, nous implémentons selon leurs instructions. Si changement, il suffira de remplacer le
        # tns_auto_entrepreneur_benefice par tns_auto_entrepreneur_revenus_net
        tns_auto_entrepreneur_revenus_rsa = r.calcule_ressource('tns_auto_entrepreneur_benefice', revenu_pro = True)

        result = (
            salaire_net + indemnites_journalieres + indemnites_chomage_partiel + indemnites_volontariat +
            revenus_stage_formation_pro + indemnites_stage + bourse_recherche + hsup + etr +
            tns_auto_entrepreneur_revenus_rsa
        ) / 3

        return period, result


@reference_formula
class rfon_ms(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus fonciers pour la base ressource du rmi/rsa"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        period_declaration = period.start.offset('first-of', 'year').period('year')
        f4ba_holder = simulation.compute('f4ba', period_declaration)
        f4be_holder = simulation.compute('f4be', period_declaration)

        f4ba = self.cast_from_entity_to_role(f4ba_holder, role = VOUS)
        f4be = self.cast_from_entity_to_role(f4be_holder, role = VOUS)

        return period, (f4ba + f4be) / 12


@reference_formula
class rmi(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu Minimum d'Insertion"

    @dated_function(start = date(1988, 12, 1), stop = date(2009, 5, 31))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        activite = simulation.calculate('activite', period)
        br_rmi = simulation.calculate('br_rmi', period)
        rsa_socle = simulation.calculate('rsa_socle', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)

        return period, (activite != 0) * (activite != 2) * (activite != 3) * (
            max_(0, rsa_socle - rsa_forfait_logement - br_rmi))
        # TODO: Migré lors de la mensualisation. Probablement faux


@reference_formula
class rmi_nbp(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Nombre de personne à charge au sens du Rmi/Rsa"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        nb_par = simulation.calculate('nb_par', period)
        P = simulation.legislation_at(period.start).minim.rmi

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        return period, nb_par + nb_enf(age, smic55, 0, P.age_pac - 1)  # TODO: check limite d'âge in legislation


@reference_formula
class rsa(DatedFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"Revenu de solidarité active"
    entity_class = Familles

    @dated_function(start = date(2009, 06, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rsa_majore = simulation.calculate('rsa_majore', period)
        rsa_non_majore = simulation.calculate('rsa_non_majore', period)
        rsa_non_calculable = simulation.calculate('rsa_non_calculable', period)

        rsa = (1 - rsa_non_calculable) * max_(rsa_majore, rsa_non_majore)

        return period, rsa


@reference_formula
class rsa_act(DatedFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Familles
    label = u"Revenu de solidarité active - activité"
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1))
    def function_2009(self, simulation, period):
        '''
        Calcule le montant du RSA activité
        Note: le partage en moitié est un point de législation, pas un choix arbitraire
        '''
        period = period
        rsa = simulation.calculate('rsa', period)
        rmi = simulation.calculate('rmi', period)

        return period, max_(rsa - rmi, 0)


@reference_formula
class rsa_act_i(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu de solidarité active - activité au niveau de l'individu"
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1))
    def function_2009_(self, simulation, period):
        period = period   # TODO: rentre dans le calcul de la PPE check period !!!
        rsa_act_holder = simulation.compute('rsa_act', period)
        concub_holder = simulation.compute('concub', period)
        maries_holder = simulation.compute('maries', period)
        quifam = simulation.calculate('quifam', period)

        concub = self.cast_from_entity_to_roles(concub_holder)
        maries = self.cast_from_entity_to_roles(maries_holder)
        rsa_act = self.cast_from_entity_to_roles(rsa_act_holder)

        conj = or_(concub, maries)
        rsa_act_i = 0 * quifam  # TODO Generate an array of float for rsa_act_i, add method self.zeros().
        chef_filter = quifam == 0
        rsa_act_i[chef_filter] = rsa_act[chef_filter] / (1 + conj[chef_filter])
        partenaire_filter = quifam == 1
        rsa_act_i[partenaire_filter] = rsa_act[partenaire_filter] * conj[partenaire_filter] / 2
        return period, rsa_act_i


@reference_formula
class rsa_base_ressources_patrimoine_i(DatedFormulaColumn):
    column = FloatCol
    label = u"Base de ressources des revenus du patrimoine du RSA"
    entity_class = Individus
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1))
    def function_2009_(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        interets_epargne_sur_livrets = simulation.calculate('interets_epargne_sur_livrets', period)
        epargne_non_remuneree = simulation.calculate('epargne_non_remuneree', period)
        revenus_capital = simulation.calculate_divide('revenus_capital', period)
        valeur_locative_immo_non_loue = simulation.calculate('valeur_locative_immo_non_loue', period)
        valeur_locative_terrains_non_loue = simulation.calculate('valeur_locative_terrains_non_loue', period)
        revenus_locatifs = simulation.calculate_divide('revenus_locatifs', period)
        rsa = simulation.legislation_at(period.start).minim.rmi

        return period, (
            interets_epargne_sur_livrets / 12 +
            epargne_non_remuneree * rsa.patrimoine.taux_interet_forfaitaire_epargne_non_remunere / 12 +
            revenus_capital +
            valeur_locative_immo_non_loue * rsa.patrimoine.abattement_valeur_locative_immo_non_loue +
            valeur_locative_terrains_non_loue * rsa.patrimoine.abattement_valeur_locative_terrains_non_loue +
            revenus_locatifs
            )


@reference_formula
class rsa_eligibilite(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité au RSA"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        age_parents = self.split_by_roles(age_holder, roles = [CHEF, PART])
        activite_holder = simulation.compute('activite', period)
        activite_parents = self.split_by_roles(activite_holder, roles = [CHEF, PART])
        nb_enfant_rsa = simulation.calculate('nb_enfant_rsa', period)
        rsa_eligibilite_tns = simulation.calculate('rsa_eligibilite_tns', period)
        rmi = simulation.legislation_at(period.start).minim.rmi
        age_min = (nb_enfant_rsa == 0) * rmi.age_pac

        eligib = (
            (age_parents[CHEF] >= age_min) * not_(activite_parents[CHEF] == 2) +
            (age_parents[PART] >= age_min) * not_(activite_parents[PART] == 2)
        )
        eligib = eligib * rsa_eligibilite_tns

        return period, eligib


@reference_formula
class rsa_eligibilite_tns(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité au RSA pour un travailleur non salarié"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        tns_benefice_exploitant_agricole_holder = simulation.compute('tns_benefice_exploitant_agricole', period)
        tns_benefice_exploitant_agricole = self.sum_by_entity(tns_benefice_exploitant_agricole_holder)
        tns_employe_holder = simulation.compute('tns_employe', period)
        tns_employe = self.any_by_roles(tns_employe_holder)
        tns_autres_revenus_chiffre_affaires_holder = simulation.compute('tns_autres_revenus_chiffre_affaires', period)
        tns_autres_revenus_chiffre_affaires = self.split_by_roles(tns_autres_revenus_chiffre_affaires_holder)
        tns_autres_revenus_type_activite_holder = simulation.compute('tns_autres_revenus_type_activite', period)
        tns_autres_revenus_type_activite = self.split_by_roles(tns_autres_revenus_type_activite_holder)

        has_conjoint = simulation.calculate('nb_par', period) > 1
        nb_enfant_rsa = simulation.calculate('nb_enfant_rsa', period)
        P = simulation.legislation_at(period.start)
        P_agr = P.tns.exploitant_agricole
        P_micro = P.ir.rpns.microentreprise
        maj_2p = P_agr.maj_2p
        maj_1e_2ad = P_agr.maj_1e_2ad
        maj_e_sup = P_agr.maj_e_sup

        def eligibilite_agricole(has_conjoint, nb_enfant_rsa, tns_benefice_exploitant_agricole, P_agr):
            plafond_benefice_agricole = P_agr.plafond_rsa * P.cotsoc.gen.smic_h_b
            taux_avec_conjoint = 1 + maj_2p + maj_1e_2ad * (nb_enfant_rsa > 0) + maj_e_sup * max_(nb_enfant_rsa - 1, 0)
            taux_sans_conjoint = 1 + maj_2p * (nb_enfant_rsa > 0) + maj_e_sup * max_(nb_enfant_rsa - 1, 0)
            taux_majoration = has_conjoint * taux_avec_conjoint + (1 - has_conjoint) * taux_sans_conjoint
            plafond_benefice_agricole_majore = taux_majoration * plafond_benefice_agricole

            return tns_benefice_exploitant_agricole < plafond_benefice_agricole_majore

        def eligibilite_chiffre_affaire(ca, type_activite, P_micro):
            plaf_vente = P_micro.vente.max
            plaf_service = P_micro.servi.max

            return ((type_activite == 0) * (ca <= plaf_vente)) + ((type_activite >= 1) * (ca <= plaf_service))

        eligibilite_agricole = eligibilite_agricole(
            has_conjoint, nb_enfant_rsa, tns_benefice_exploitant_agricole, P_agr
            )
        eligibilite_chiffre_affaire = (
            eligibilite_chiffre_affaire(
                tns_autres_revenus_chiffre_affaires[CHEF], tns_autres_revenus_type_activite[CHEF], P_micro
            ) *
            eligibilite_chiffre_affaire(
                tns_autres_revenus_chiffre_affaires[PART], tns_autres_revenus_type_activite[PART], P_micro
            )
        )

        return period, eligibilite_agricole * (1 - tns_employe) * eligibilite_chiffre_affaire


@reference_formula
class rsa_forfait_asf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial forfaitisée pour le RSA"
    start_date = date(2014, 4, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig = simulation.calculate('asf_elig', period)
        rsa_forfait_asf_i_holder = simulation.compute('rsa_forfait_asf_i', period)
        montant = self.sum_by_entity(rsa_forfait_asf_i_holder, roles = ENFS)

        return period, asf_elig * montant


@reference_formula
class rsa_forfait_asf_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"RSA - Montant individuel de forfait ASF"
    start_date = date(2014, 4, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig_i = simulation.calculate('asf_elig_i', period)
        pfam = simulation.legislation_at(period.start).fam
        minim = simulation.legislation_at(period.start).minim

        return period, asf_elig_i * pfam.af.bmaf * minim.rmi.forfait_asf.taux1


@reference_formula
class rsa_forfait_logement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Forfait logement intervenant dans le calcul du Rmi ou du Rsa"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        forf_logement = simulation.legislation_at(period.start).minim.rmi.forfait_logement
        rmi = simulation.legislation_at(period.start).minim.rmi.rmi

        rmi_nbp = simulation.calculate('rmi_nbp', period)
        statut_occupation_holder = simulation.compute('statut_occupation', period)
        aide_logement = simulation.calculate('aide_logement', period)

        statut_occupation = self.cast_from_entity_to_roles(statut_occupation_holder)
        statut_occupation = self.filter_role(statut_occupation, role = CHEF)

        avantage_nature = or_(statut_occupation == 2, statut_occupation == 6)
        avantage_al = aide_logement > 0

        montant_forfait = rmi * (
            (rmi_nbp == 1) * forf_logement.taux1 +
            (rmi_nbp == 2) * forf_logement.taux2 +
            (rmi_nbp >= 3) * forf_logement.taux3
        )

        montant_al = avantage_al * min_(aide_logement, montant_forfait)
        montant_nature = avantage_nature * montant_forfait

        return period, max_(montant_al, montant_nature)


@reference_formula
class rsa_majore(DatedFormulaColumn):
    column = FloatCol
    label = u"Revenu de solidarité active - majoré"
    entity_class = Familles

    @dated_function(start = date(2009, 06, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rsa_socle_majore = simulation.calculate('rsa_socle_majore', period)
        ra_rsa = simulation.calculate('ra_rsa', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        br_rmi = simulation.calculate('br_rmi', period)
        P = simulation.legislation_at(period.start).minim.rmi

        base_normalise = max_(rsa_socle_majore - rsa_forfait_logement - br_rmi + P.pente * ra_rsa, 0)

        return period, base_normalise * (base_normalise >= P.rsa_nv)


@reference_formula
class rsa_majore_eligibilite(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité au RSA majoré pour parent isolé"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        isol = simulation.calculate('isol', period)
        enceinte_fam = simulation.calculate('enceinte_fam', period)
        nbenf = simulation.calculate('nb_enfant_rsa', period)
        rsa_eligibilite_tns = simulation.calculate('rsa_eligibilite_tns', period)
        eligib = isol * (enceinte_fam | (nbenf > 0)) * rsa_eligibilite_tns

        return period, eligib


@reference_formula
class rsa_non_calculable(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum([
            u"",
            u"tns",
            u"conjoint_tns"
        ]),
        default = 0
    )
    entity_class = Familles
    label = u"RSA non calculable pour la Famille (voir rsa_non_calculable_i)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        eligible_rsa = (
            simulation.calculate('rsa_eligibilite', period) +
            simulation.calculate('rsa_majore_eligibilite', period)
            )
        non_calculable_tns_holder = simulation.compute('rsa_non_calculable_tns_i', period)
        non_calculable_tns_parents = self.split_by_roles(non_calculable_tns_holder, roles = [CHEF, PART])
        non_calculable = (
            (non_calculable_tns_parents[CHEF] > 0) * 1 +
            ((1 - non_calculable_tns_parents[CHEF]) * non_calculable_tns_parents[PART] > 0) * 2
            )
        non_calculable = eligible_rsa * non_calculable

        return period, non_calculable


@reference_formula
class rsa_non_calculable_tns_i(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"RSA non calculable du fait de la situation de l'individu. Dans le cas des TNS, l'utilisateur est renvoyé vers son PCG"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', period)
        tns_micro_entreprise_chiffre_affaires = simulation.calculate('tns_micro_entreprise_chiffre_affaires', period)
        tns_autres_revenus = simulation.calculate('tns_autres_revenus', period)

        return period, (
            (tns_benefice_exploitant_agricole > 0) + (tns_micro_entreprise_chiffre_affaires > 0) +
            (tns_autres_revenus > 0)
            )


@reference_formula
class rsa_non_majore(DatedFormulaColumn):
    column = FloatCol
    label = u"Revenu de solidarité active - non majoré"
    entity_class = Familles

    @dated_function(start = date(2009, 06, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rsa_socle = simulation.calculate('rsa_socle', period)
        ra_rsa = simulation.calculate('ra_rsa', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        br_rmi = simulation.calculate('br_rmi', period)
        P = simulation.legislation_at(period.start).minim.rmi

        base_normalise = max_(rsa_socle - rsa_forfait_logement - br_rmi + P.pente * ra_rsa, 0)

        return period, base_normalise * (base_normalise >= P.rsa_nv)


class rsa_ressource_calculator:

    def __init__(self, simulation, period):
        self.period = period
        self.simulation = simulation
        self.three_previous_months = self.period.start.period('month', 3).offset(-3)
        self.last_month = period.start.period('month').offset(-1)
        self.has_ressources_substitution = (
            simulation.calculate('chonet', period) +
            simulation.calculate('indemnites_journalieres', period) +
            simulation.calculate('rstnet', period)  # +
            # simulation.calculate('ass', last_month)
        ) > 0
        self.neutral_max_forfaitaire = 3 * simulation.legislation_at(period.start).minim.rmi.rmi

    def calcule_ressource(self, variable_name, revenu_pro = False):
        ressource_trois_derniers_mois = self.simulation.calculate_add(variable_name, self.three_previous_months)
        ressource_mois_courant = self.simulation.calculate(variable_name, self.period)
        ressource_last_month = self.simulation.calculate(variable_name, self.last_month)

        if revenu_pro:
            condition = (
                (ressource_mois_courant == 0) *
                (ressource_last_month > 0) *
                not_(self.has_ressources_substitution)
            )
            return (1 - condition) * ressource_trois_derniers_mois
        else:
            condition = (
                (ressource_mois_courant == 0) *
                (ressource_last_month > 0)
            )
            return max_(0,
                ressource_trois_derniers_mois - condition * self.neutral_max_forfaitaire)


@reference_formula
class rsa_socle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = "RSA socle"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        nb_par = simulation.calculate('nb_par', period)
        eligib = simulation.calculate('rsa_eligibilite', period)
        nb_enfant_rsa = simulation.calculate('nb_enfant_rsa', period)
        rmi = simulation.legislation_at(period.start).minim.rmi

        nbp = nb_par + nb_enfant_rsa

        taux = (
            1 + (nbp >= 2) * rmi.txp2 +
            (nbp >= 3) * rmi.txp3 +
            (nbp >= 4) * ((nb_par == 1) * rmi.txps + (nb_par != 1) * rmi.txp3) +
            max_(nbp - 4, 0) * rmi.txps
        )
        return period, eligib * rmi.rmi * taux


@reference_formula
class rsa_socle_majore(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Majoration pour parent isolé du Revenu de solidarité active socle"
    start_date = date(2009, 6, 1)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rmi = simulation.legislation_at(period.start).minim.rmi
        eligib = simulation.calculate('rsa_majore_eligibilite', period)
        nbenf = simulation.calculate('nb_enfant_rsa', period)
        taux = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nbenf
        return period, eligib * rmi.rmi * taux
