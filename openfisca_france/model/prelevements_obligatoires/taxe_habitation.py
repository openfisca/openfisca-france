# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore


class exonere_taxe_habitation(Variable):
    value_type = bool
    default_value = True
    entity = Menage
    label = u"Exonération de la taxe d'habitation"
    reference = "http://vosdroits.service-public.fr/particuliers/F42.xhtml"
    definition_period = YEAR

    def formula(menage, period, parameters):
        """Exonation de la taxe d'habitation

        'men'

        Eligibilité:
        - âgé de plus de 60 ans, non soumis à l'impôt de solidarité sur la fortune (ISF) en n-1
        - veuf quel que soit votre âge et non soumis à l'impôt de solidarité sur la fortune (ISF) n-1
        - titulaire de l'allocation de solidarité aux personnes âgées (Aspa)  ou de l'allocation supplémentaire d'invalidité (Asi),
        bénéficiaire de l'allocation aux adultes handicapés (AAH),
        atteint d'une infirmité ou d'une invalidité vous empêchant de subvenir à vos besoins par votre travail.
        """
        janvier = period.first_month

        P = parameters(period).cotsoc.gen

        age = menage.personne_de_reference('age', janvier)
        statut_marital = menage.personne_de_reference('statut_marital', janvier)

        aah_i = menage.members('aah', period, options = [ADD])
        asi_i = menage.members.famille('asi', period, options = [ADD])
        aspa_i = menage.members.famille('aspa', period, options = [ADD])
        aah = menage.sum(aah_i)
        asi = menage.sum(asi_i)
        aspa = menage.sum(aspa_i)

        isf_tot_i = menage.members.foyer_fiscal('isf_tot', period)
        isf_tot = menage.sum(isf_tot_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        nbptr_i = menage.members.foyer_fiscal('nbptr', period)
        nbptr = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # TODO: Beurk

        rfr_i = menage.members.foyer_fiscal('rfr', period)
        rfr = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)


        seuil_th = P.plaf_th_1 + P.plaf_th_supp * (max_(0, (nbptr - 1) / 2))
        elig = ((age >= 60) + (statut_marital == 4)) * (isf_tot <= 0) * (rfr < seuil_th) + (asi > 0) + (aspa > 0) + (aah > 0)
        return not_(elig)


class cotisation_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = u"Cotisation taxe d'habitation"
    definition_period = YEAR
    set_input = set_input_divide_by_period


class taux_degrevement_taxe_habitation(Variable):
    value_type = float
    default_value = 1
    entity = Menage
    label = u"Taux du degreveemnt de la taxe d'habitation"
    reference = "PLF 2018 article 3"
    definition_period = YEAR
    def formula(menage, period, parameters):
        """Degrevement de la taxe d'habitation
    
        'men'
    
        Eligibilité:
        - avoir moins de 27 000 euros de RFR pour un célibataire + 8000 pour les deux demi parts suivantes et 6000 par demi part au dela
        - un dispositif de lissage permet d'éviter les effets de seuil : entre 27 000 et 28 000 euros de RFR pour un celibataire, le taux du degrevement diminue lineairement avec le RFR.
        """
        janvier = period.first_month
    
        P = parameters(period).th
    
        statut_marital = menage.personne_de_reference('statut_marital', janvier)
    
        nbptr_i = menage.members.foyer_fiscal('nbptr', period)
        nbptr = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # TODO: Beurk
    
        rfr_i = menage.members.foyer_fiscal('rfr', period)
        rfr = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
    
        seuil_degrevement_1 = P.degrevement.plafonds.plaf_degrevement_th_1 + P.degrevement.plafonds.plaf_degrevement_sup_th_1 * 2*min_(max_(0, (nbptr - 1)),1) + P.degrevement.plafonds.plaf_degrevement_sup2_th_1 * 2*max_(0, (nbptr - 2))
        seuil_degrevement_2 = P.degrevement.plafonds.plaf_degrevement_th_2 + P.degrevement.plafonds.plaf_degrevement_sup_th_2 * 2*min_(max_(0, (nbptr - 1)),1) + P.degrevement.plafonds.plaf_degrevement_sup2_th_2 * 2*max_(0, (nbptr - 2))
            
        taux_lissage = max_(min_((seuil_degrevement_2-rfr)/(seuil_degrevement_2-seuil_degrevement_1),1),0)
          
        abattement = P.degrevement.taux*taux_lissage
        
        return (abattement)


class taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?espId=1&pageId=part_taxe_habitation&impot=TH&sfid=50"
    definition_period = YEAR

    def formula(menage, period, parameters):
        last_year = period.last_year

        exonere_taxe_habitation = menage('exonere_taxe_habitation', period)

        enfant_a_charge_i = menage.members('enfant_a_charge', period)
        nombre_enfants_a_charge_menage = menage.sum(enfant_a_charge_i)
        nombre_enfants_majeurs_celibataires_sans_enfant = menage('nombre_enfants_majeurs_celibataires_sans_enfant', period)

        rfr_i = menage.members.foyer_fiscal('rfr', last_year)
        rfr = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        taux_degrevement = menage('taux_degrevement_taxe_habitation', period)
        th = menage('cotisation_taxe_habitation',period)

        return th*(1-taux_degrevement)*(exonere_taxe_habitation)
