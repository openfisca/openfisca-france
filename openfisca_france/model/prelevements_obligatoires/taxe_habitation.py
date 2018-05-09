# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *


class exonere_taxe_habitation(Variable):
    value_type = bool
    default_value = True
    entity = Menage
    label = u"Exonération de la taxe d'habitation"
    reference = "http://vosdroits.service-public.fr/particuliers/F42.xhtml"
    definition_period = YEAR

    def formula(menage, period, parameters):
        """Exonation de la taxe d'habitation
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
        asi_i = menage.members('asi', period, options = [ADD])
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
        elig = ((age >= 60) + (statut_marital == TypesStatutMarital.veuf)) * (isf_tot <= 0) * (rfr < seuil_th) + (asi > 0) + (aspa > 0) + (aah > 0)
        return not_(elig)


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

        return - 0 * not_(exonere_taxe_habitation)
