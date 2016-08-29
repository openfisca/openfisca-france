# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf

class aefa(DatedVariable):
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
        period = period.this_year
        age_holder = simulation.compute('age', period)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_parents = simulation.calculate('nb_parents', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate_add('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, autonomie_financiere, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_parents == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_parents <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        period = period.this_year
        age_holder = simulation.compute('age', period)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_parents = simulation.calculate('nb_parents', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, autonomie_financiere, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_parents == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_parents <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa += condition * P.forf2008
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function__2008_(self, simulation, period):
        period = period.this_year
        age_holder = simulation.compute('age', period)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period, accept_other_period = True)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_parents = simulation.calculate('nb_parents', period)
        ass = simulation.calculate_add('ass', period)
        aer_holder = simulation.compute('aer', period)
        api = simulation.calculate_add('api', period)
        rsa = simulation.calculate('rsa', period)
        P = simulation.legislation_at(period.start).minim.aefa
        af = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        aer = self.sum_by_entity(aer_holder)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
        dummy_ass = ass > 0
        dummy_aer = aer > 0
        dummy_api = api > 0
        dummy_rmi = rsa > 0
        maj = 0  # TODO
        condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(age, autonomie_financiere, af.age1, af.age3)
        else:
            nbPAC = af_nbenf
        # TODO check nombre de PAC pour une famille
        aefa = condition * P.mon_seul * (
            1 + (nb_parents == 2) * P.tx_2p +
            nbPAC * P.tx_supp * (nb_parents <= 2) +
            nbPAC * P.tx_3pac * max_(nbPAC - 2, 0)
            )
        aefa_maj = P.mon_seul * maj
        aefa = max_(aefa_maj, aefa)
        return period, aefa
