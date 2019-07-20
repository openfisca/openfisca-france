# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class aefa(Variable):
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
    value_type = float
    entity = Famille
    label = "Aide exceptionelle de fin d'année (prime de Noël)"
    reference = "https://www.service-public.fr/particuliers/vosdroits/F1325"
    definition_period = YEAR

    def formula_2002_01_01(famille, period, parameters):
        rsa = famille('rsa', period, options = [ADD])
        ass_i = famille.members('ass', period, options = [ADD])
        ass = famille.sum(ass_i)
        api = famille('api', period, options = [ADD])
        aer_i = famille.members('aer', period, options = [ADD])
        aer = famille.sum(aer_i)
        condition = (ass > 0) + (aer > 0) + (api > 0) + (rsa > 0)
        condition_majoration = rsa > 0

        af = parameters(period).prestations.prestations_familiales.af
        janvier = period.first_month
        af_nbenf = famille('af_nbenf', janvier)
        nb_parents = famille('nb_parents', janvier)
        if hasattr(af, "age3"):
            nbPAC = nb_enf(famille, janvier, af.age1, af.age3)
        else:
            nbPAC = af_nbenf

        aefa = parameters(period).prestations.minima_sociaux.aefa

        # TODO check nombre de PAC pour une famille
        majoration = 1 + (condition_majoration * (
            (nb_parents == 2) * aefa.tx_2p
            + nbPAC * aefa.tx_supp * (nb_parents <= 2)
            + nbPAC * aefa.tx_3pac * max_(nbPAC - 2, 0)
            ))

        montant_aefa = aefa.mon_seul * majoration
        montant_aefa += aefa.prime_exceptionnelle

        return condition * montant_aefa
