# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *


class UCChequeEnergie(Enum):
    __order__ = 'une_uc une_uc_a_deux_uc plus_de_deux_uc'  # Needed to preserve the enum order in Python 2
    une_uc = u'Une unité de consommation (UC)'
    une_uc_a_deux_uc = u'Une UC à deux UC'
    plus_de_deux_uc = u'Plus de deux UC'


class cheque_energie_unites_consommation(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=LEGIARTI000032497834&cidTexte=LEGITEXT000023983208&dateTexte=20160511"
    label = u"Unités de consommation du ménage pour le calcul du chèque Énergie"
    definition_period = YEAR

    def formula_2018(menage, period, parameters):
        uc = parameters(period).cheque_energie.unites_consommation
        nb_personnes = menage.nb_persons()
        gardes_alternees = menage.sum(menage.members('garde_alternee', period.first_month))

        nb_personnes_ajuste = nb_personnes - 0.5 * gardes_alternees
        return (
            uc.premiere_personne
            + uc.deuxieme_personne * (nb_personnes_ajuste > 1) * (min_(nb_personnes_ajuste, 2) - 1)
            + uc.autres_personnes * (nb_personnes_ajuste > 2) * (nb_personnes_ajuste - 2)
            )


class cheque_energie_eligibilite_logement(Variable):
    entity = Menage
    value_type = bool
    reference = [
        u"Article L124-1 du Code de l'énergie",
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=5AB50D02153C9CB753729850314A2E17.tplgfr29s_1?idArticle=LEGIARTI000031057544&cidTexte=LEGITEXT000023983208&dateTexte=20180314",
        u"Article LO6314-3 du Code général des collectivités territoriales",
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=6A3717E70623B148432581CC8F585C5F.tplgfr31s_1?idArticle=LEGIARTI000006394061&cidTexte=LEGITEXT000006070633&dateTexte=20180316",
        ]
    label = u"Éligibilité du logement occupé au chèque énergie"
    definition_period = MONTH

    def formula_2018(menage, period, parameters):
        statut_occupation_logement = menage('statut_occupation_logement', period)
        residence_saint_martin = menage('residence_saint_martin', period)

        return (
            not_(residence_saint_martin) * (
                + (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)
                + (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble)
                )
            )


class cheque_energie_montant(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichTexteArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=JORFARTI000032496647&cidTexte=JORFTEXT000032496630&dateTexte=20160508&categorieLien=id"
    label = u"Montant du chèque énergie"
    definition_period = YEAR

    def formula_2018(menage, period, parameters):
        baremes = parameters(period).cheque_energie.baremes
        seuils = baremes.thresholds
        montants = baremes.montants

        uc_menage = menage('cheque_energie_unites_consommation', period)
        rfr = menage.personne_de_reference.foyer_fiscal('rfr', period.n_2)

        ressources_par_uc = rfr / uc_menage

        uc = select(
            [uc_menage <= 1, uc_menage < 2, 2 <= uc_menage],
            [UCChequeEnergie.une_uc, UCChequeEnergie.une_uc_a_deux_uc, UCChequeEnergie.plus_de_deux_uc]
            )

        return (
            + (ressources_par_uc < seuils.tranche_une) * montants[uc].tranche_une
            + (seuils.tranche_une <= ressources_par_uc) * (ressources_par_uc < seuils.tranche_deux) * montants[uc].tranche_deux
            + (seuils.tranche_deux <= ressources_par_uc) * (ressources_par_uc < seuils.tranche_trois) * montants[uc].tranche_trois
            )


class cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://chequeenergie.gouv.fr"
    label = u"Montant auquel le ménage peut prétendre au titre du chèque energie"
    definition_period = MONTH

    def formula_2018(menage, period, parameters):
        return menage('cheque_energie_montant', period.this_year) * menage('cheque_energie_eligibilite_logement', period)
