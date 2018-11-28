# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class reduction_loyer_solidarite_plafond_ressources(Variable):
    value_type = float
    entity = Famille
    label = u"Plafond de ressources pour le calcul de la réduction du loyer de solidarité"
    reference = [
        u"https://www.anil.org/aj-reduction-loyer-solidarite-rls-apl/",
        u"https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036650010&dateTexte=&categorieLien=id",
        u"https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036650026&dateTexte=&categorieLien=id"
        ]
    definition_period = MONTH

    def formula(famille, period, parameters):
        rls = parameters(period).prestations.reduction_loyer_solidarite
        personnes_a_charge_al = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        zone_apl = famille.demandeur.menage('zone_apl', period)

        plafond_ressources = rls.plafond_ressources.par_zone[zone_apl]

        plafond_personne_seule = plafond_ressources.personnes_seules
        plafond_couple = plafond_ressources.couples
        plafond_1pac = plafond_ressources.famille_1pac
        plafond_2pac = plafond_ressources.famille_2pac
        plafond_3pac = plafond_ressources.famille_3pac
        plafond_4pac = plafond_ressources.famille_4pac
        plafond_5pac = plafond_ressources.famille_5pac
        plafond_6pac = plafond_ressources.famille_6pac
        plafond_famille = plafond_ressources.famille_6pac + (personnes_a_charge_al > 6) * (personnes_a_charge_al - 6) * plafond_ressources.majoration_par_pac_supp

        return select(
            [
                not_(couple) * (personnes_a_charge_al == 0),
                couple * (personnes_a_charge_al == 0),
                personnes_a_charge_al == 1,
                personnes_a_charge_al == 2,
                personnes_a_charge_al == 3,
                personnes_a_charge_al == 4,
                personnes_a_charge_al == 5,
                personnes_a_charge_al == 6,
                ],
            [
                plafond_personne_seule,
                plafond_couple,
                plafond_1pac,
                plafond_2pac,
                plafond_3pac,
                plafond_4pac,
                plafond_5pac,
                plafond_6pac
                ],
            default = plafond_famille
            )


class reduction_loyer_solidarite_montant(Variable):
    value_type = float
    entity = Famille
    label = u"Montant de la réduction du loyer de solidarité"
    reference = u"https://www.legifrance.gouv.fr/eli/arrete/2018/2/27/TERL1801551A/jo/article_2"
    definition_period = MONTH

    def formula(famille, period, parameters):
        rls = parameters(period).prestations.reduction_loyer_solidarite
        personnes_a_charge_al = famille('al_nb_personnes_a_charge', period)
        couple = famille('al_couple', period)
        zone_apl = famille.demandeur.menage('zone_apl', period)

        montant = rls.montant.par_zone[zone_apl]

        montant_personne_seule = montant.personnes_seules
        montant_couple = montant.couples
        montant_1pac = montant.famille_1pac
        montant_famille = montant.famille_1pac + (personnes_a_charge_al > 1) * (personnes_a_charge_al - 1) * montant.majoration_par_pac_supp

        return select(
            [
                not_(couple) * (personnes_a_charge_al == 0),
                couple * (personnes_a_charge_al == 0),
                personnes_a_charge_al == 1
                ],
            [
                montant_personne_seule,
                montant_couple,
                montant_1pac
                ],
            default = montant_famille
            )


class reduction_loyer_solidarite(Variable):
    value_type = float
    entity = Famille
    label = u"Réduction du loyer de solidarité effectivement versée"
    reference = [
        u"https://www.anil.org/aj-reduction-loyer-solidarite-rls-apl/",
        u"https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036650010&dateTexte=&categorieLien=id",
        u"https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036650026&dateTexte=&categorieLien=id"
        ]
    definition_period = MONTH

    def formula_2018_01_01(famille, period):
        # les ressources renvoyés sont recombiné pour donner une valeur annuelle
        # necessité de diviser par 12 pour comparer au plafond mensuel
        ressources = famille('aide_logement_base_ressources', period) / 12
        plafond = famille('reduction_loyer_solidarite_plafond_ressources', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        logement_conventionne = famille.demandeur.menage('logement_conventionne', period)
        locataire_foyer = statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer

        eligible = (ressources < plafond) * logement_conventionne * not_(locataire_foyer)
        montant = famille('reduction_loyer_solidarite_montant', period)
        return eligible * montant
