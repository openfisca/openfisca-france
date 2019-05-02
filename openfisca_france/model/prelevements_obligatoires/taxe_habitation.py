# -*- coding: utf-8 -*-

from numpy import logical_and as and_
from openfisca_france.model.base import *

####### Simulation TH de la résidence principale : législation à partir de l'année 2017


class condition_rfr_exoneration_th(Variable):
    value_type = bool
    default_value = False
    entity = FoyerFiscal
    label = u"Condition de revenu fiscal de référence pour l'éxonération à l'échelle du foyer fiscal"
    reference = "BOI-IF-TH-10-50-30"
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Pour l'exonération de la taxe d'habitation et l'abattement pour condition modeste, en cas de ménages à foyers
        fiscaux multiples, la condition relative au revenu fiscal de référence doit être respectée pour tous les foyers
        fiscaux du ménage, d'où cette variable intermédiaire
        '''
        P = parameters(period).taxation_locale.taxe_habitation
        rfr = foyer_fiscal('rfr', period.last_year)
        nbptr = foyer_fiscal('nbptr', period.last_year)
        seuil_th = P.exon_plaf_rfr_1 + P.exon_plaf_rfr_supp * max_(0, (nbptr - 1) * 2)
        return (rfr < seuil_th)


class exonere_th(Variable):
    value_type = bool
    default_value = False
    entity = Menage
    label = u"Exonération de la taxe d'habitation"
    reference = "http://vosdroits.service-public.fr/particuliers/F42.xhtml"
    definition_period = YEAR

    def formula_2017_01_01(menage, period):
        '''
        Hypothèses :
            (1) pour la condition de plus de 60 ans ou veuf, on regarde seulement la personne de référence du ménage
            (2) pour la condition relative à l'ASPA l'ASI et l'AAH, on fait la somme de ces prestations à l'échelle du ménage
            (3) pour la condition relative à l'ISF-IFI, on fait la somme de ces impôts à l'échelle du ménage
        '''
        janvier = period.first_month

        age = menage.personne_de_reference('age', janvier)
        statut_marital = menage.personne_de_reference('statut_marital', janvier)

        aah_i = menage.members('aah', period, options = [ADD])
        asi_i = menage.members('asi', period, options = [ADD])
        aspa_i = menage.members.famille('aspa', period, options = [ADD])
        aah = menage.sum(aah_i)
        asi = menage.sum(asi_i)
        aspa = menage.sum(aspa_i)

        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)

        exon_avant_condition_rfr = ((age >= 60) + (statut_marital == TypesStatutMarital.veuf)) * (isf_ifi == 0) + (asi > 0) + (aspa > 0) + (aah > 0)
        exon = exon_avant_condition_rfr * condition_rfr_exoneration_th
        return exon


class valeur_locative_cadastrale_brute(Variable):
    value_type = float
    entity = Menage
    label = u"Valeur locative cadastrale utilisée pour les impôts locaux, avant abattements"
    reference = "art. 1496 du CGI"
    definition_period = YEAR

class code_INSEE_commune(Variable):
    value_type = str
    max_length = 5
    entity = Menage
    label = u"Code INSEE de la commune de résidence du ménage"
    definition_period = YEAR

class SIREN_EPCI(Variable):
    value_type = str
    max_length = 9
    entity = Menage
    label = u"Numéro SIREN de l'EPCI de résidence du ménage"
    definition_period = YEAR

class abattement_charge_famille_th_commune(Variable):
    value_type = float
    entity = Menage
    label = u"Abattement obligatoire pour charges de famille - TH de la commune"
    reference = "art. 1411 du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Dans les personnes à charge :
            (1) on ne compte pas les ascendants de plus de 70 ans ou infirmes, ayant un
                revenu fiscal de référence inférieur à un certain seuil.
            (2) on ne prend pas en compte les gardes en résidence alternée qui font qu'une personne à charge ne compte
                que pour 0.5 au lieu de 1.
        '''
        enfant_i = menage.members.has_role(Famille.ENFANT)
        nb_enfants = menage.sum(enfant_i)
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        quotite_abattement_pac_1_2_com = P.quotite_abattement_pac_1_2.communes[code_INSEE_commune]
        quotite_abattement_pac_3_plus_com = P.quotite_abattement_pac_3_plus.communes[code_INSEE_commune]
        return (
            quotite_abattement_pac_1_2_com * min_(nb_enfants, 2)
            + quotite_abattement_pac_3_plus_com * max_(nb_enfants - 2, 0)
            )

class abattement_charge_famille_th_epci(Variable):
    value_type = float
    entity = Menage
    label = u"Abattement obligatoire pour charges de famille - TH de l'EPCI"
    reference = "art. 1411 du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Dans les personnes à charge :
            (1) on ne compte pas les ascendants de plus de 70 ans ou infirmes, ayant un
                revenu fiscal de référence inférieur à un certain seuil.
            (2) on ne prend pas en compte les gardes en résidence alternée qui font qu'une personne à charge ne compte
                que pour 0.5 au lieu de 1.
        '''
        enfant_i = menage.members.has_role(Famille.ENFANT)
        nb_enfants = menage.sum(enfant_i)
        P = parameters(period).taxation_locale.taxe_habitation
        SIREN_EPCI = menage('SIREN_EPCI', period)
        quotite_abattement_pac_1_2_epci = P.quotite_abattement_pac_1_2.epci[SIREN_EPCI]
        quotite_abattement_pac_3_plus_epci = P.quotite_abattement_pac_3_plus.epci[SIREN_EPCI]
        return (
            quotite_abattement_pac_1_2_epci * min_(nb_enfants, 2)
            + quotite_abattement_pac_3_plus_epci * max_(nb_enfants - 2, 0)
            )

class abattement_personnes_condition_modeste_th_commune(Variable):
    value_type = float
    entity = Menage
    label = u"Abattement pour personnes de condition modeste - TH de la commune"
    reference = "3. du II. de l'art. 1411 du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Pour le nombre de personnes à charge, on ne prend pas en compte les gardes en résidence alternée qui font
        qu'une personne à charge ne compte que pour 0.5 au lieu de 1.
        '''
        enfant_i = menage.members.has_role(Famille.ENFANT)
        nb_enfants = menage.sum(enfant_i)
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        quotite_abattement_condition_modeste_com = P.quotite_abattement_condition_modeste.communes[code_INSEE_commune]
        valeur_locative_moyenne_com = P.valeur_locative_moyenne.communes[code_INSEE_commune]
        taux_plafond_general = P.seuil_valeur_locative_abattement_condition_modeste
        maj_taux_plafond_par_pac = P.maj_seuil_valeur_locative_abattement_condition_modeste
        valeur_locative_max = (taux_plafond_general + maj_taux_plafond_par_pac * nb_enfants) * valeur_locative_moyenne_com
        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)
        elig = condition_rfr_exoneration_th * not_(exonere_th) * (valeur_locative_cadastrale_brute <= valeur_locative_max)

        return elig * quotite_abattement_condition_modeste_com


class abattement_personnes_condition_modeste_th_epci(Variable):
    value_type = float
    entity = Menage
    label = u"Abattement pour personnes de condition modeste - TH de l'EPCI"
    reference = "3. du II. de l'art. 1411 du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Pour le nombre de personnes à charge, on ne prend pas en compte les gardes en résidence alternée qui font
        qu'une personne à charge ne compte que pour 0.5 au lieu de 1.
        '''
        enfant_i = menage.members.has_role(Famille.ENFANT)
        nb_enfants = menage.sum(enfant_i)
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        P = parameters(period).taxation_locale.taxe_habitation
        SIREN_EPCI = menage('SIREN_EPCI', period)
        quotite_abattement_condition_modeste_epci = P.quotite_abattement_condition_modeste.epci[SIREN_EPCI]
        valeur_locative_moyenne_epci = P.valeur_locative_moyenne.epci[SIREN_EPCI]
        taux_plafond_general = P.seuil_valeur_locative_abattement_condition_modeste
        maj_taux_plafond_par_pac = P.maj_seuil_valeur_locative_abattement_condition_modeste
        valeur_locative_max = (taux_plafond_general + maj_taux_plafond_par_pac * nb_enfants) * valeur_locative_moyenne_epci
        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)
        elig = condition_rfr_exoneration_th * not_(exonere_th) * (valeur_locative_cadastrale_brute <= valeur_locative_max)

        return elig * quotite_abattement_condition_modeste_epci


class base_nette_th_commune(Variable):
    value_type = float
    entity = Menage
    label = u"Base nette - TH de la commune"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Note : on ne prend pas en compte l'abattement en faveur des personnes handicapées
        '''
        P = parameters(period).taxation_locale.taxe_habitation
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        abattement_charge_famille_th_commune = menage('abattement_charge_famille_th_commune', period)
        abattement_personnes_condition_modeste_th_commune = menage('abattement_personnes_condition_modeste_th_commune', period)
        code_INSEE_commune = menage('code_INSEE_commune', period)
        quotite_abattement_general_a_la_base_com = P.quotite_abattement_general_a_la_base.communes[code_INSEE_commune]
        base_brute_moins_abattements = (
            valeur_locative_cadastrale_brute
            - abattement_charge_famille_th_commune
            - abattement_personnes_condition_modeste_th_commune
            - quotite_abattement_general_a_la_base_com
            )
        return max_(base_brute_moins_abattements, 0)


class base_nette_th_epci(Variable):
    value_type = float
    entity = Menage
    label = u"Base nette - TH de l'EPCI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Note : on ne prend pas en compte l'abattement en faveur des personnes handicapées
        '''
        P = parameters(period).taxation_locale.taxe_habitation
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        abattement_charge_famille_th_epci = menage('abattement_charge_famille_th_epci', period)
        abattement_personnes_condition_modeste_th_epci = menage('abattement_personnes_condition_modeste_th_epci', period)
        SIREN_EPCI = menage('SIREN_EPCI', period)
        quotite_abattement_general_a_la_base_epci = P.quotite_abattement_general_a_la_base.epci[SIREN_EPCI]
        base_brute_moins_abattements = (
            valeur_locative_cadastrale_brute
            - abattement_charge_famille_th_epci
            - abattement_personnes_condition_modeste_th_epci
            - quotite_abattement_general_a_la_base_epci
            )
        return max_(base_brute_moins_abattements, 0)


class taxe_habitation_commune_epci_avant_degrevement(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation de la commune et de l'EPCI avant dégrèvement"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        SIREN_EPCI = menage('SIREN_EPCI', period)
        taux_com = P.taux.communes[code_INSEE_commune]
        taux_epci = P.taux.epci[SIREN_EPCI]
        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        exonere_th = menage('exonere_th', period)
        return (base_nette_th_commune * taux_com + base_nette_th_epci * taux_epci) * not_(exonere_th)


class plafond_taxe_habitation_eligibilite(Variable):
    value_type = bool
    entity = Menage
    label = u"Eligibilité au plafond de la taxe d'habitation en fonction du revenu fiscal de référence"
    reference = "art. 1414 A du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        P_plaf = parameters(period).taxation_locale.taxe_habitation.plafonnement
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi_menage = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        seuil_rfr = P_plaf.plaf_rfr_1ere_part + P_plaf.plaf_rfr_1ere_demi_part_supp * (min_(max_(nbptr_menage - 1, 0), 0.5)) / 0.5 + P_plaf.plaf_rfr_autres_demi_parts_supp * (max_(nbptr_menage - 1.5, 0)) / 0.5
        return (rfr_menage <= seuil_rfr) * (isf_ifi_menage == 0)


class plafond_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = u"Plafond de la taxe d'habitation en fonction du revenu fiscal de référence"
    reference = "art. 1414 A du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        plafond_taxe_habitation_eligibilite = menage('plafond_taxe_habitation_eligibilite', period)
        P_plaf = parameters(period).taxation_locale.taxe_habitation.plafonnement
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        abattement = P_plaf.abattement_rfr_1ere_part + P_plaf.abattement_rfr_4_1eres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 2)) / 0.5 + P_plaf.abattement_rfr_autres_demi_parts_supp * (max_(nbptr_menage - 3, 0)) / 0.5
        return (rfr_menage - abattement) * P_plaf.taux_plafonnement_revenu * plafond_taxe_habitation_eligibilite


class degrevement_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = u"Dégrèvement de la taxe d'habitation"
    reference = "art. 1414 A du CGI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        plafond_taxe_habitation_eligibilite = menage('plafond_taxe_habitation_eligibilite', period)
        plafond_taxe_habitation = menage('plafond_taxe_habitation', period)
        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        base_reduction_degrevement = min_(base_nette_th_commune, base_nette_th_epci)
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        SIREN_EPCI = menage('SIREN_EPCI', period)
        taux_com = P.taux.communes[code_INSEE_commune]
        taux_epci = P.taux.epci[SIREN_EPCI]
        ecart_avec_2000 = period.start.offset('first-of', 'year').year - 2000
        annee_2000 = period.start.offset('first-of', 'year').period('year').offset(-ecart_avec_2000)
        P_2000 = parameters(annee_2000).taxation_locale.taxe_habitation
        taux_com_2000 = P_2000.taux.communes[code_INSEE_commune]
        taux_epci_2000 = P_2000.taux.epci[SIREN_EPCI]
        assert and_(taux_com_2000 is not None, taux_epci_2000 is not None) # Mais quid des variations d'appartenance d'une commune donnée à un EPCI ?
        reduction_degrevement = base_reduction_degrevement * (taux_com + taux_epci - (taux_com_2000 + taux_epci_2000) * P.plafonnement.coeff_multiplicateur_taux_2000)
        reduction_degrevement = reduction_degrevement * (reduction_degrevement > P.plafonnement.valeur_minimale_reduction_degrevement)
        degrevement = (
            taxe_habitation_commune_epci_avant_degrevement
            - plafond_taxe_habitation
            - reduction_degrevement
            )
        return max_(degrevement, 0) * plafond_taxe_habitation_eligibilite

class taxe_habitation_commune_epci(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation de la commune et de l'EPCI, frais de gestion inclus"
    reference = "https://www.service-public.fr/particuliers/vosdroits/F42"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        degrevement_taxe_habitation = menage('degrevement_taxe_habitation', period)
        P = parameters(period).taxation_locale.taxe_habitation
        taux_frais_assiette = P.frais_assiette
        montant = max_(taxe_habitation_commune_epci_avant_degrevement - degrevement_taxe_habitation, 0)
        return - montant * (1 + taux_frais_assiette)
