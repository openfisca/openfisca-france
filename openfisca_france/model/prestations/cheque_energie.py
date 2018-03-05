# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore

class unites_consommation_cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=LEGIARTI000032497834&cidTexte=LEGITEXT000023983208&dateTexte=20160511"
    label = u"Unités de consommation du ménage pour le calcul du chèque Énergie"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        uc = parameters(period).cheque_energie.unites_consommation
        nb_persons = menage.nb_persons()
        gardes_alternee = menage.sum(menage.members('garde_alternee', period.first_month))

        adj_nb = nb_persons - 0.5 * gardes_alternee

        return uc.premiere_personne + uc.deuxieme_personne * (adj_nb > 1) * (adj_nb - 1) + uc.autres_personnes * (adj_nb > 2) * (adj_nb - 2)


class montant_cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichTexteArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=JORFARTI000032496647&cidTexte=JORFTEXT000032496630&dateTexte=20160508&categorieLien=id"
    label = u"Montant du chèque énergie"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        baremes = parameters(period).cheque_energie.baremes
        th = baremes.thresholds
        montants = baremes.montants

        uc = menage('unites_consommation_cheque_energie', period)
        rfr = menage.personne_de_reference.foyer_fiscal('rfr', period.n_2)

        base = rfr / uc

        return (
            + (     uc <= 1) * ((base < th.un) * montants.une_uc.un + (th.un <= base < th.deux) * montants.une_uc.deux + (th.deux <= base < th.trois) * montants.une_uc.trois)
            + (1 <  uc <  2) * ((base < th.un) * montants.une_uc_a_deux_uc.un + (th.un <= base < th.deux) * montants.une_uc_a_deux_uc.deux + (th.deux <= base < th.trois) * montants.une_uc_a_deux_uc.trois)
            + (2 <= uc     ) * ((base < th.un) * montants.plus_de_deux_uc.un + (th.un <= base < th.deux) * montants.plus_de_deux_uc.deux + (th.deux <= base < th.trois) * montants.plus_de_deux_uc.trois)
            )


class cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://chequeenergie.gouv.fr"
    label = u"Chèque énergie"
    definition_period = MONTH

    def formula_2017(menage, period, parameters):
        return menage('montant_cheque_energie', period.this_year)
