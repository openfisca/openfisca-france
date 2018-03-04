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
        nb_persons = menage.nb_persons()
        gardes_alternee = menage.sum(menage.members('garde_alternee', period.first_month))

        adj_nb = nb_persons - 0.5 * gardes_alternee

        return 1 + 0.5 * (adj_nb > 1) * (adj_nb - 1) + 0.3 * (adj_nb > 2) * (adj_nb - 2)


class montant_cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichTexteArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=JORFARTI000032496647&cidTexte=JORFTEXT000032496630&dateTexte=20160508&categorieLien=id"
    label = u"Montant du chèque énergie"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        uc = menage('unites_consommation_cheque_energie', period)
        rfr = menage.personne_de_reference.foyer_fiscal('rfr', period.n_2)

        base = rfr / uc

        return (
            + (uc <= 1)    * ((base < 5600) * 144 + (5600 <= base < 6700) *  96 + (6700 <= base < 7700) * 48)
            + (1 < uc < 2) * ((base < 5600) * 190 + (5600 <= base < 6700) * 126 + (6700 <= base < 7700) * 63)
            + (2 <= uc)    * ((base < 5600) * 227 + (5600 <= base < 6700) * 152 + (6700 <= base < 7700) * 76)
            )
