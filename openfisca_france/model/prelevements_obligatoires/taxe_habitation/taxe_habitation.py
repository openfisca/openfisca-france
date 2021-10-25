from openfisca_france.model.base import *


# Simulation TH de la résidence principale : législation à partir de l'année 2017


class valeur_locative_cadastrale_brute(Variable):
    value_type = float
    entity = Menage
    label = "Valeur locative cadastrale utilisée pour les impôts locaux, avant abattements"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000034111395&cidTexte=LEGITEXT000006069577&dateTexte=20170302"
    definition_period = YEAR


class condition_rfr_exoneration_th(Variable):
    value_type = bool
    default_value = False
    entity = FoyerFiscal
    label = "Condition de revenu fiscal de référence pour l'éxonération à l'échelle du foyer fiscal"
    reference = "http://bofip.impots.gouv.fr/bofip/5934-PGP.html"
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
        seuil_th = P.exon_plaf_rfr.premiere_part + P.exon_plaf_rfr.demi_part_supp * max_(0, (nbptr - 1) * 2)
        return (rfr < seuil_th)


class exonere_taxe_habitation(Variable):
    value_type = bool
    default_value = False
    entity = Menage
    label = "Exonération de la taxe d'habitation"
    reference = "http://vosdroits.service-public.fr/particuliers/F42.xhtml"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Hypothèses :
            (1) pour la condition de plus de 60 ans ou veuf, on regarde seulement la personne de référence du ménage
            (2) pour la condition relative à l'ASPA l'ASI et l'AAH, on fait la somme de ces prestations à l'échelle du ménage
            (3) pour la condition relative à l'ISF-IFI, on fait la somme de ces impôts à l'échelle du ménage
            (4) on ne prend pas en compte les prolongements temporaires d'exonération pour certains contribuables
                ayant perdu l'éligibilité à l'éxonération (I bis de l'art. 1414 du CGI)
        '''
        janvier = period.first_month

        age_personne_de_reference = menage.personne_de_reference('age', janvier)
        age_conjoint = menage.conjoint('age', janvier)
        statut_marital = menage.personne_de_reference('statut_marital', janvier)

        aah_i = menage.members('aah', period, options = [ADD])
        asi_i = menage.members('asi', period, options = [ADD])
        aspa_i = menage.members.famille('aspa', period, options = [ADD])
        aah = menage.sum(aah_i)
        asi = menage.sum(asi_i)
        aspa = menage.sum(aspa_i, role = Famille.DEMANDEUR)

        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)

        P = parameters(period).taxation_locale.taxe_habitation

        exon_non_soumis_a_condition_rfr = (asi > 0) + (aspa > 0)
        exon_soumis_a_condition_rfr = ((age_personne_de_reference >= P.exon_age_min) + (age_conjoint >= P.exon_age_min) + (statut_marital == TypesStatutMarital.veuf)) * (isf_ifi == 0) + (aah > 0)
        exon = exon_non_soumis_a_condition_rfr + exon_soumis_a_condition_rfr * condition_rfr_exoneration_th
        return exon


class abattement_charge_famille_th_commune(Variable):
    value_type = float
    entity = Menage
    label = "Abattement obligatoire pour charges de famille - TH de la commune"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000033220348&dateTexte=&categorieLien=id"
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
        abt_pac_1_2_th_commune = menage('abt_pac_1_2_th_commune', period)
        abt_pac_3pl_th_commune = menage('abt_pac_3pl_th_commune', period)
        return (
            abt_pac_1_2_th_commune * min_(nb_enfants, 2)
            + abt_pac_3pl_th_commune * max_(nb_enfants - 2, 0)
            )


class abattement_charge_famille_th_epci(Variable):
    value_type = float
    entity = Menage
    label = "Abattement obligatoire pour charges de famille - TH de l'EPCI"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000033220348&dateTexte=&categorieLien=id"
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
        abt_pac_1_2_th_epci = menage('abt_pac_1_2_th_epci', period)
        abt_pac_3pl_th_epci = menage('abt_pac_3pl_th_epci', period)
        return (
            abt_pac_1_2_th_epci * min_(nb_enfants, 2)
            + abt_pac_3pl_th_epci * max_(nb_enfants - 2, 0)
            )


class abattement_personnes_condition_modeste_th_commune(Variable):
    value_type = float
    entity = Menage
    label = "Abattement pour personnes de condition modeste - TH de la commune"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000033220348&dateTexte=&categorieLien=id"
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
        abt_condition_modeste_th_commune = menage('abt_condition_modeste_th_commune', period)
        valeur_locative_moyenne_th_commune = menage('valeur_locative_moyenne_th_commune', period)
        taux_plafond_general = P.seuil_valeur_locative_abattement_condition_modeste
        maj_taux_plafond_par_pac = P.maj_seuil_valeur_locative_abattement_condition_modeste
        valeur_locative_max = (taux_plafond_general + maj_taux_plafond_par_pac * nb_enfants) * valeur_locative_moyenne_th_commune
        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)
        exonere_taxe_habitation = menage('exonere_taxe_habitation', period)
        elig = condition_rfr_exoneration_th * not_(exonere_taxe_habitation) * (valeur_locative_cadastrale_brute <= valeur_locative_max)

        return elig * abt_condition_modeste_th_commune


class abattement_personnes_condition_modeste_th_epci(Variable):
    value_type = float
    entity = Menage
    label = "Abattement pour personnes de condition modeste - TH de l'EPCI"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000033220348&dateTexte=&categorieLien=id"
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
        abt_condition_modeste_th_epci = menage('abt_condition_modeste_th_epci', period)
        valeur_locative_moyenne_th_epci = menage('valeur_locative_moyenne_th_epci', period)
        taux_plafond_general = P.seuil_valeur_locative_abattement_condition_modeste
        maj_taux_plafond_par_pac = P.maj_seuil_valeur_locative_abattement_condition_modeste
        valeur_locative_max = (taux_plafond_general + maj_taux_plafond_par_pac * nb_enfants) * valeur_locative_moyenne_th_epci
        condition_rfr_exoneration_th_i = menage.members.foyer_fiscal('condition_rfr_exoneration_th', period)
        condition_rfr_exoneration_th = menage.all(condition_rfr_exoneration_th_i)
        exonere_taxe_habitation = menage('exonere_taxe_habitation', period)
        elig = condition_rfr_exoneration_th * not_(exonere_taxe_habitation) * (valeur_locative_cadastrale_brute <= valeur_locative_max)

        return elig * abt_condition_modeste_th_epci


class base_nette_th_commune(Variable):
    value_type = float
    entity = Menage
    label = "Base nette - TH de la commune"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Notes :
            (1) on ne prend pas en compte l'abattement en faveur des personnes handicapées
            (2) on ne prend pas en compte les abattements temporaires pour certains contribuables
                ayant perdu l'éligibilité à l'éxonération (I bis de l'art. 1414 du CGI)
        '''
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        abattement_charge_famille_th_commune = menage('abattement_charge_famille_th_commune', period)
        abattement_personnes_condition_modeste_th_commune = menage('abattement_personnes_condition_modeste_th_commune', period)
        abt_general_base_th_commune = menage('abt_general_base_th_commune', period)
        base_brute_moins_abattements = (
            valeur_locative_cadastrale_brute
            - abattement_charge_famille_th_commune
            - abattement_personnes_condition_modeste_th_commune
            - abt_general_base_th_commune
            )
        return max_(base_brute_moins_abattements, 0)


class base_nette_th_epci(Variable):
    value_type = float
    entity = Menage
    label = "Base nette - TH de l'EPCI"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        '''
        Notes :
            (1) on ne prend pas en compte l'abattement en faveur des personnes handicapées
            (2) on ne prend pas en compte les abattements temporaires pour certains contribuables
                ayant perdu l'éligibilité à l'éxonération (I bis de l'art. 1414 du CGI)
        '''
        valeur_locative_cadastrale_brute = menage('valeur_locative_cadastrale_brute', period)
        abattement_charge_famille_th_epci = menage('abattement_charge_famille_th_epci', period)
        abattement_personnes_condition_modeste_th_epci = menage('abattement_personnes_condition_modeste_th_epci', period)
        abt_general_base_th_epci = menage('abt_general_base_th_epci', period)
        base_brute_moins_abattements = (
            valeur_locative_cadastrale_brute
            - abattement_charge_famille_th_epci
            - abattement_personnes_condition_modeste_th_epci
            - abt_general_base_th_epci
            )
        return max_(base_brute_moins_abattements, 0)


class taxe_habitation_commune_epci_avant_degrevement(Variable):
    value_type = float
    entity = Menage
    label = "Taxe d'habitation de la commune et de l'EPCI avant dégrèvement (frais de gestion inclus)"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        taux_th_commune = menage('taux_th_commune', period)
        taux_th_epci = menage('taux_th_epci', period)
        # Attention, si (taux_th_commune + taux_th_epci == 0), alors
        # il n'y a pas de taux de taxe d'habitation défini pour le depcom indiqué.

        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        exonere_taxe_habitation = menage('exonere_taxe_habitation', period)
        P = parameters(period).taxation_locale.taxe_habitation
        taux_frais_assiette = P.frais_assiette
        return (base_nette_th_commune * taux_th_commune + base_nette_th_epci * taux_th_epci) * not_(exonere_taxe_habitation) * (1 + taux_frais_assiette)


class plafond_taxe_habitation_eligibilite(Variable):
    value_type = bool
    entity = Menage
    label = "Eligibilité au plafond de la taxe d'habitation en fonction du revenu fiscal de référence"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000006312070&dateTexte=&categorieLien=cid"
    definition_period = YEAR
    end = '2019-12-31'

    def formula_2017_01_01(menage, period, parameters):
        P_plaf = parameters(period).taxation_locale.taxe_habitation.plafonnement
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi_menage = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        seuil_rfr = P_plaf.plaf_rfr.premiere_part + P_plaf.plaf_rfr.premiere_demi_part_supp * (min_(max_(nbptr_menage - 1, 0), 0.5)) / 0.5 + P_plaf.plaf_rfr.autres_demi_parts_supp * (max_(nbptr_menage - 1.5, 0)) / 0.5
        return (rfr_menage <= seuil_rfr) * (isf_ifi_menage == 0)


class plafond_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = "Plafond de la taxe d'habitation en fonction du revenu fiscal de référence"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000006312070&dateTexte=&categorieLien=cid"
    definition_period = YEAR
    end = '2019-12-31'

    def formula_2017_01_01(menage, period, parameters):
        plafond_taxe_habitation_eligibilite = menage('plafond_taxe_habitation_eligibilite', period)
        P_plaf = parameters(period).taxation_locale.taxe_habitation.plafonnement
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        abattement = P_plaf.abattement_rfr.premiere_part + P_plaf.abattement_rfr.quatre_premieres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 2)) / 0.5 + P_plaf.abattement_rfr.autres_demi_parts_supp * (max_(nbptr_menage - 3, 0)) / 0.5
        return max_(rfr_menage - abattement, 0) * P_plaf.taux_plafonnement_revenu * plafond_taxe_habitation_eligibilite


class degrevement_plafonnement_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = "Dégrèvement de la taxe d'habitation au titre du plafonnement"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006069577&idArticle=LEGIARTI000006312070&dateTexte=&categorieLien=cid"
    definition_period = YEAR
    end = '2019-12-31'

    def formula_2017_01_01(menage, period, parameters):
        '''
        Notes :
            (1) On ne prend pas en compte la majoration du dégrèvement pour les cas spécifiques où le montant
                de taxe résulte exclusivement de la réduction du dégrèvement dépendant des hausses de taux
                depuis 2000 (3. du III. de l'art 1414 A du CGI)
            (2) Pour la réduction du dégrèvement, on ne prend pas en compte les cas où les abattements du
                département en 2010 étaient plus avantageux que les abattements de la commune ou de l'EPCI
                en 2018 (a. du 1. du III. de l'art 1414 A du CGI)
        '''
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        plafond_taxe_habitation_eligibilite = menage('plafond_taxe_habitation_eligibilite', period)
        plafond_taxe_habitation = menage('plafond_taxe_habitation', period)
        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        base_reduction_degrevement = min_(base_nette_th_commune, base_nette_th_epci)

        taux_th_commune = menage('taux_th_commune', period)
        taux_th_epci = menage('taux_th_epci', period)
        ecart_avec_2000 = period.start.offset('first-of', 'year').year - 2000
        annee_2000 = period.start.offset('first-of', 'year').period('year').offset(-ecart_avec_2000)
        taux_th_commune_2000 = menage('taux_th_commune', annee_2000)
        taux_th_epci_2000 = menage('taux_th_epci', annee_2000)

        P = parameters(period).taxation_locale.taxe_habitation
        reduction_degrevement = base_reduction_degrevement * (taux_th_commune + taux_th_epci - (taux_th_commune_2000 + taux_th_epci_2000) * P.plafonnement.coeff_multiplicateur_taux_2000)
        reduction_degrevement = reduction_degrevement * (reduction_degrevement > P.plafonnement.valeur_minimale_reduction_degrevement)

        # Les taux de taxe d'habitation de l'année 2000 utilisés pour la réduction du plafonnement
        # ne sont pas disponibles pour cette commune. Nous mettons donc cette réduction à zéro.
        reduction_degrevement = where(
            taux_th_commune_2000 + taux_th_epci_2000 == 0,
            0,
            reduction_degrevement,
            )

        degrevement = (
            taxe_habitation_commune_epci_avant_degrevement
            - plafond_taxe_habitation
            - reduction_degrevement
            )
        return max_(degrevement, 0) * plafond_taxe_habitation_eligibilite


class taxe_habitation_commune_epci_apres_degrevement_plafonnement(Variable):
    value_type = float
    entity = Menage
    label = "Taxe d'habitation de la commune et de l'EPCI après dégrèvement pour plafonnement"
    definition_period = YEAR
    end = '2019-12-31'

    def formula_2017_01_01(menage, period, parameters):
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        degrevement_plafonnement_taxe_habitation = menage('degrevement_plafonnement_taxe_habitation', period)
        return max_(taxe_habitation_commune_epci_avant_degrevement - degrevement_plafonnement_taxe_habitation, 0)


class degrevement_office_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = "Dégrèvement d'office de la taxe d'habitation"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=268AD735F5C69F94FB6756E3125BF0A0.tplgfr43s_1?idArticle=LEGIARTI000036441815&cidTexte=LEGITEXT000006069577&dateTexte=20190513&categorieLien=id&oldAction=&nbResultRech="
    definition_period = YEAR

    def formula_2018_01_01(menage, period, parameters):
        '''
        Note Importante : on ne prend pas en compte l'exclusion de ce dégrèvement des hausses de taux et d'abattements depuis 2018.
        Dans les faits :
            - si les variations de taux de taxation et d'abattements votés par les communes et EPCI depuis 2017
              entrainent une baisse ou une non variation de la taxe d'habitation, le dégrèvement s'applique au
              montant de taxe d'habitation avec taux et abattements actualisés;
            - si ces variations entrainent une hausse de la taxe d'habitation, le dégrèvement d'office est
              appliqué à la taxe d'habitation qui aurait été payée en N (avec N>=2018) avec les taux de taxation
              et d'abattements votés par les communes et EPCI en 2017.
        Dans ce code, on suppose qu'on est toujours dans le premier cas.
        '''

        # Calcul de l'éligibilité en fonction du revenu fiscal de référence et de la perception de l'ISF-IFI
        P_degrev = parameters(period).taxation_locale.taxe_habitation.degrevement_d_office
        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi_menage = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        plafond_rfr_degrev = P_degrev.plaf_rfr_degrev.premiere_part + P_degrev.plaf_rfr_degrev.deux_premieres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 1)) / 0.5 + P_degrev.plaf_rfr_degrev.autres_demi_parts_supp * (max_(nbptr_menage - 2, 0)) / 0.5
        plafond_rfr_degrev_degressif = P_degrev.plaf_rfr_degrev_degressif.premiere_part + P_degrev.plaf_rfr_degrev_degressif.deux_premieres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 1)) / 0.5 + P_degrev.plaf_rfr_degrev_degressif.autres_demi_parts_supp * (max_(nbptr_menage - 2, 0)) / 0.5
        elig_degrev = (isf_ifi_menage == 0) * (rfr_menage <= plafond_rfr_degrev)
        elig_degrev_degressif = (isf_ifi_menage == 0) * (elig_degrev == 0) * (rfr_menage <= plafond_rfr_degrev_degressif)

        # Calcul du dégrèvement
        taxe_habitation_commune_epci_apres_degrevement_plafonnement = menage('taxe_habitation_commune_epci_apres_degrevement_plafonnement', period)
        degrev = P_degrev.taux_inf_plaf * taxe_habitation_commune_epci_apres_degrevement_plafonnement
        degrev_degressif = degrev * max_((plafond_rfr_degrev_degressif - rfr_menage) / (plafond_rfr_degrev_degressif - plafond_rfr_degrev), 0)

        return degrev * elig_degrev + degrev_degressif * elig_degrev_degressif

    def formula_2020_01_01(menage, period, parameters):
        '''
        Différence par rapport à la formule précédente : le taux de plafonnement est appliqué à taxe_habitation_commune_epci_avant_degrevement
        (au lieu de taxe_habitation_commune_epci_apres_degrevement_plafonnement)
        '''

        # Calcul de l'éligibilité en fonction du revenu fiscal de référence et de la perception de l'ISF-IFI
        P_degrev = parameters(period).taxation_locale.taxe_habitation.degrevement_d_office
        isf_ifi_i = menage.members.foyer_fiscal('isf_ifi', period.last_year)
        isf_ifi_menage = menage.sum(isf_ifi_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        rfr_i = menage.members.foyer_fiscal('rfr', period.last_year)
        rfr_menage = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        nbptr_i = menage.members.foyer_fiscal('nbptr', period.last_year)
        nbptr_menage = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
        plafond_rfr_degrev = P_degrev.plaf_rfr_degrev.premiere_part + P_degrev.plaf_rfr_degrev.deux_premieres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 1)) / 0.5 + P_degrev.plaf_rfr_degrev.autres_demi_parts_supp * (max_(nbptr_menage - 2, 0)) / 0.5
        plafond_rfr_degrev_degressif = P_degrev.plaf_rfr_degrev_degressif.premiere_part + P_degrev.plaf_rfr_degrev_degressif.deux_premieres_demi_parts_supp * (min_(max_(nbptr_menage - 1, 0), 1)) / 0.5 + P_degrev.plaf_rfr_degrev_degressif.autres_demi_parts_supp * (max_(nbptr_menage - 2, 0)) / 0.5
        elig_degrev = (isf_ifi_menage == 0) * (rfr_menage <= plafond_rfr_degrev)
        elig_degrev_degressif = (isf_ifi_menage == 0) * (elig_degrev == 0) * (rfr_menage <= plafond_rfr_degrev_degressif)
        elig_degrev_sup_plaf = (elig_degrev == 0)

        # Calcul du dégrèvement
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        degrev = P_degrev.taux_inf_plaf * taxe_habitation_commune_epci_avant_degrevement
        degrev_degressif = degrev * max_((plafond_rfr_degrev_degressif - rfr_menage) / (plafond_rfr_degrev_degressif - plafond_rfr_degrev), 0)
        degrev_sup_plaf = P_degrev.taux_sup_plaf * max_(taxe_habitation_commune_epci_avant_degrevement - degrev_degressif, 0)

        return degrev * elig_degrev + degrev_degressif * elig_degrev_degressif + degrev_sup_plaf * elig_degrev_sup_plaf


class prelevement_base_imposition_elevee_taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = "Prélevement sur base d'imposition élevée sur l'habitation principale"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=81889AAB5AC742D99144BC27CE3D7C31.tplgfr32s_3?idArticle=LEGIARTI000036443853&cidTexte=LEGITEXT000006069577&categorieLien=id&dateTexte=20171231"
    definition_period = YEAR
    end = '2021-12-31'

    def formula_2017_01_01(menage, period, parameters):

        P = parameters(period).taxation_locale.taxe_habitation.prelevement_base_imposition_elevee
        exonere_taxe_habitation = menage('exonere_taxe_habitation', period)
        degrevement_plafonnement_taxe_habitation = menage('degrevement_plafonnement_taxe_habitation', period)
        degrevement_office_taxe_habitation = menage('degrevement_office_taxe_habitation', period)
        base_nette_th_commune = menage('base_nette_th_commune', period)

        non_exonere_non_degreve = not_(exonere_taxe_habitation) * (degrevement_plafonnement_taxe_habitation == 0) * (degrevement_office_taxe_habitation == 0)
        condition_base_nette = (base_nette_th_commune > P.seuil_base_nette_habitation_principale)

        return non_exonere_non_degreve * condition_base_nette * base_nette_th_commune * P.taux_habitation_principale


class taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = "Taxe d'habitation de la commune et de l'EPCI (Établissement Public de Coopération Intercommunale), frais de gestion inclus"
    reference = "https://www.service-public.fr/particuliers/vosdroits/F42"
    definition_period = YEAR

    def formula_2017_01_01(menage, period):
        taxe_habitation_commune_epci_apres_degrevement_plafonnement = menage('taxe_habitation_commune_epci_apres_degrevement_plafonnement', period)
        degrevement_office_taxe_habitation = menage('degrevement_office_taxe_habitation', period)
        prelevement_base_imposition_elevee_taxe_habitation = menage('prelevement_base_imposition_elevee_taxe_habitation', period)
        return - max_(taxe_habitation_commune_epci_apres_degrevement_plafonnement - degrevement_office_taxe_habitation, 0) - prelevement_base_imposition_elevee_taxe_habitation

    def formula_2020_01_01(menage, period):
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        degrevement_office_taxe_habitation = menage('degrevement_office_taxe_habitation', period)
        prelevement_base_imposition_elevee_taxe_habitation = menage('prelevement_base_imposition_elevee_taxe_habitation', period)
        return - max_(taxe_habitation_commune_epci_avant_degrevement - degrevement_office_taxe_habitation, 0) - prelevement_base_imposition_elevee_taxe_habitation

    def formula_2021_01_01(menage, period):
        taxe_habitation_commune_epci_avant_degrevement = menage('taxe_habitation_commune_epci_avant_degrevement', period)
        degrevement_office_taxe_habitation = menage('degrevement_office_taxe_habitation', period)
        return - max_(taxe_habitation_commune_epci_avant_degrevement - degrevement_office_taxe_habitation, 0)
