# -*- coding: utf-8 -*-

from openfisca_france.model.base import *

####### Simulation TH de la résidence principale : législation à partir de l'année 2017


class condition_rfr_exoneration_th(Variable):
    value_type = bool
    default_value = False
    entity = FoyerFiscal
    label = u"Condition de revenu fiscal de référence pour l'éxonération à l'échelle du foyer fiscal"
    reference = "BOI-IF-TH-10-50-30"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
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
        ... nb_enfants : mettre Famille. alors que menage.nb_persons : à checker
        nb_enfants = menage.nb_persons(role = Famille.ENFANT)
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
        ... nb_enfants : mettre Famille. alors que menage.nb_persons : à checker
        nb_enfants = menage.nb_persons(role = Famille.ENFANT)
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
        ... nb_enfants : mettre Famille. alors que menage.nb_persons : à checker
        nb_enfants = menage.nb_persons(role = Famille.ENFANT)
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
        ... nb_enfants : mettre Famille. alors que menage.nb_persons : à checker
        nb_enfants = menage.nb_persons(role = Famille.ENFANT)
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


class taxe_habitation_commune_epci_avant_plafonnement(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation de la commune et de l'EPCI avant plafonnement"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        SIREN_EPCI = menage('SIREN_EPCI', period)
        taux_com = P.taux.communes[code_INSEE_commune]
        taux_epci = P.taux.epci[SIREN_EPCI]
        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        return base_nette_th_commune * taux_com + base_nette_th_epci * taux_epci


class taxe_habitation_commune_epci_avant_plafonnement(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation de la commune et de l'EPCI avant plafonnement"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        P = parameters(period).taxation_locale.taxe_habitation
        code_INSEE_commune = menage('code_INSEE_commune', period)
        SIREN_EPCI = menage('SIREN_EPCI', period)
        taux_com = P.taux.communes[code_INSEE_commune]
        taux_epci = P.taux.epci[SIREN_EPCI]
        base_nette_th_commune = menage('base_nette_th_commune', period)
        base_nette_th_epci = menage('base_nette_th_epci', period)
        return base_nette_th_commune * taux_com + base_nette_th_epci * taux_epci


class taxe_habitation(Variable):
    value_type = float
    entity = Menage
    label = u"Taxe d'habitation"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?espId=1&pageId=part_taxe_habitation&impot=TH&sfid=50"
    definition_period = YEAR

    def formula_2017_01_01(menage, period, parameters):
        last_year = period.last_year

        exonere_th = menage('exonere_th', period)
        enfant_a_charge_i = menage.members('enfant_a_charge', period)
        nombre_enfants_a_charge_menage = menage.sum(enfant_a_charge_i)
        nombre_enfants_majeurs_celibataires_sans_enfant = menage('nombre_enfants_majeurs_celibataires_sans_enfant', period)

        rfr_i = menage.members.foyer_fiscal('rfr', last_year)
        rfr = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # noqa F841

        # Variables TODO: à inclure dans la fonction
        valeur_locative_brute = 0
        valeur_locative_moyenne = 0  # déped de la collectivité)

        # Paramètres: à inclure dans parameters.xml
        taux_minimal_2_premiers = .1  # minimun depusi 2011
        majoration_2_premiers = 0
        taux_minimal_3_et_plus = .15
        majoration_3_et_plus = 0

        abattement_general_base_forfaitaire = 0  # si non nul le taux suivant est nul
        taux_abattement_general_base = .1  # entre 1% et 15% depuis 2011

        taux_special_modeste = 0
        seuil_elig_special_modeste = 1.3  # 130 % de la valeur locative moyenne
        seuil_elig_special_modeste_add = .1  # 10% par personne à charge en garde exclusive et 5% en garde altennée

        taux_special_invalide = .1  # 10% si l'abattement est voté est en vigueur

        taux_imposition = .10  # TODO: taux d'imposition voté par les colloc

        # abattements pour l'habitation principale

        #   abattements obligatoires pour charges de famille

        # * les enfants du contribuable, de son conjoint ou les enfants recueillis qui sont pris en compte pour le
        # calcul de l’impôt sur le revenu (2). Ne sont pas concernés ceux pour lesquels le redevable déduit de ses
        # revenus imposables une pension alimentaire ;
        pac_enf = nombre_enfants_a_charge_menage + nombre_enfants_majeurs_celibataires_sans_enfant  # TODO: inclure ceux du conjoint non présent sur la feuille d'impôt ? gestion des gardes alternées

        # * les ascendants du contribuable et ceux de son conjoint remplissant les 3 conditions suivantes :
        # – être âgés de plus de 70 ans ou infirmes (c’est-à-dire ne pouvant subvenir par leur travail aux nécessités
        # de l’existence),
        # – résider avec lui,
        # – et disposer d’un revenu fiscal de référence pour l’année précédente n’excédant pas la limite prévue à
        # l’article 1417-I du CGI (voir page 94).

        pac_asc = 0  # TODO

        taux_2_premiers = taux_minimal_2_premiers + majoration_2_premiers
        taux_3_et_plus = taux_minimal_3_et_plus + majoration_3_et_plus

        abattement_obligatoire = (
            min_(pac_enf + pac_asc, 2)
            * taux_2_premiers
            + max_(pac_enf + pac_asc - 2, 0)
            * taux_3_et_plus
            ) * valeur_locative_moyenne

        #   abattements facultatifs à la base :
        #     abattement faculattif général

        abattement_general = abattement_general_base_forfaitaire + taux_abattement_general_base * valeur_locative_moyenne

        #     abattement facultatif dit spécial en faveur des personnes dont le « revenu fiscal de référence » n’excède pas certaines limites

        # Il est institué à l’initiative des communes et EPCI à fiscalité propre ; il est indépendant de l’abattement géné-
        # ral à la base avec lequel il peut se cumuler. Il ne s’applique pas dans les départements d’outre-mer.
        # Son taux peut être fixé, selon la décision des communes et EPCI à fiscalité propre qui en décident
        # l’application, à une valeur entière comprise entre 1 et 15 % de la valeur locative moyenne des habitations
        # (pour rappel, jusqu’en 2011, les taux pouvaient être fixés à 5 %, 10 % ou 15 %)
        #
        # Pour bénéficier de cet abattement, les contribuables doivent remplir deux conditions :

        abattement_special_modeste = (
            valeur_locative_brute <= ((seuil_elig_special_modeste + seuil_elig_special_modeste_add * (pac_enf + pac_asc)) * valeur_locative_moyenne)
            #       ) * (rfr <= 100  # TODO
            ) * taux_special_modeste * valeur_locative_moyenne

        #     abattement facultatif en faveur des personnes handicapées ou invalides.
        abattement_special_invalide = 0 * taux_special_invalide  # Tous les habitants doivent êtres invalides

        base_nette = valeur_locative_brute - (abattement_obligatoire + abattement_general + abattement_special_modeste + abattement_special_invalide)

        cotisation_brute = base_nette * taux_imposition  # noqa F841

        # Frais de gestion
        #     FRAIS DE GESTION DE LA
        # FISCALITÉ DIRECTE LOCALE (art. 1641 du CGI)
        # En contrepartie des frais de confection des
        # rôles et de dégrèvement qu’il prend à sa
        # charge, l’État perçoit une somme égale à :
        # - 3 %
        # (1) des cotisations perçues au profit
        # des communes et EPCI à fiscalité propre,
        # ramenée à 1 % pour les locaux meublés
        # affectés à l’habitation principale ;
        # - 8 % (2) des cotisations perçues au profit
        # des syndicats de communes ;
        # - 9 % (2) des cotisations perçues au profit
        # des établissements publics bénéficiaires de
        # taxes spéciales d’équipement (TSE).
        # (1) Dont frais de dégrèvement et de non-valeurs : 2 %.
        # (2) Dont frais de dégrèvement et de non-valeurs : 3,6 %.
        frais_gestion = 0  # noqa F841

        # Prélèvement pour base élevée et sur les résidences secondaires
        # TODO
        prelevement_residence_secondaire = 0  # noqa F841

        return - 0 * not_(exonere_th)
