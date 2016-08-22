# -*- coding: utf-8 -*-

from __future__ import division

from numpy import (floor, logical_and as and_, logical_not as not_, logical_or as or_, maximum as max_, minimum as min_, select, where)

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf, age_en_mois_benjamin


class api(DatedVariable):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation de parent isolé"
    url = u"http://fr.wikipedia.org/wiki/Allocation_de_parent_isol%C3%A9",

    @dated_function(stop = date(2009, 5, 31))
    def function__2009(self, simulation, period):
        """
        Allocation de parent isolé
        """
        period = period.this_month
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        age_holder = simulation.compute('age', period)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period)
        isole = not_(simulation.calculate('en_couple', period))
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        rsa_base_ressources = simulation.calculate('rsa_base_ressources', period)
        af_majoration = simulation.calculate('af_majoration', period)
        rsa = simulation.calculate('rsa', period)
        af = simulation.legislation_at(period.start).fam.af
        api = simulation.legislation_at(period.start).minim.api

        age = self.split_by_roles(age_holder, roles = ENFS)
        age_en_mois = self.split_by_roles(age_en_mois_holder, roles = ENFS)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
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
        eligib = isole * ((enceinte != 0) | (nb_enf(age, autonomie_financiere, 0, api.age - 1) > 0)) * condition

        # moins de 20 ans avant inclusion dans rsa
        # moins de 25 ans après inclusion dans rsa
        api1 = eligib * af.bmaf * (api.base + api.enf_sup * nb_enf(age, autonomie_financiere, af.age1, api.age_pac - 1))
        rsa = (api.age_pac >= 25)  # dummy passage au rsa majoré
        br_api = rsa_base_ressources + af_majoration * not_(rsa)
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

class psa(DatedVariable):
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
        period = period.this_month
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

class rmi(DatedVariable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu Minimum d'Insertion"

    @dated_function(start = date(1988, 12, 1), stop = date(2009, 5, 31))
    def function(self, simulation, period):
        period = period.this_month
        activite = simulation.calculate('activite', period)
        rsa_base_ressources = simulation.calculate('rsa_base_ressources', period)
        rsa_socle = simulation.calculate('rsa_socle', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)

        return period, (activite != 0) * (activite != 2) * (activite != 3) * (
            max_(0, rsa_socle - rsa_forfait_logement - rsa_base_ressources))
        # TODO: Migré lors de la mensualisation. Probablement faux

class rsa_activite(DatedVariable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Familles
    label = u"Revenu de solidarité active - activité"
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1),)
    def function_2009(self, simulation, period):
        '''
        Calcule le montant du RSA activité
        Note: le partage en moitié est un point de législation, pas un choix arbitraire
        '''
        period = period
        rsa = simulation.calculate_add('rsa', period)
        rmi = simulation.calculate_add('rmi', period)

        return period, max_(rsa - rmi, 0)

class rsa_activite_individu(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu de solidarité active - activité au niveau de l'individu"
    start_date = date(2009, 6, 1)

    @dated_function(start = date(2009, 6, 1), stop = date(2015, 12, 31))
    def function_2009_(self, simulation, period):
        period = period   # TODO: rentre dans le calcul de la PPE check period !!!
        rsa_activite_holder = simulation.compute('rsa_activite', period)
        en_couple_holder = simulation.compute('en_couple', period)
        maries_holder = simulation.compute('maries', period)
        quifam = simulation.calculate('quifam', period)

        en_couple = self.cast_from_entity_to_roles(en_couple_holder)
        maries = self.cast_from_entity_to_roles(maries_holder)
        rsa_activite = self.cast_from_entity_to_roles(rsa_activite_holder)

        conj = or_(en_couple, maries)

        rsa_activite_i = self.zeros()

        chef_filter = quifam == 0
        rsa_activite_i[chef_filter] = rsa_activite[chef_filter] / (1 + conj[chef_filter])
        partenaire_filter = quifam == 1
        rsa_activite_i[partenaire_filter] = rsa_activite[partenaire_filter] * conj[partenaire_filter] / 2
        return period, rsa_activite_i
