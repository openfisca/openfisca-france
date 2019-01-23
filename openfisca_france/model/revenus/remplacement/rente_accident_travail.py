# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa

class taux_rente_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Rente d’accident du travail "
    reference = ""
    definition_period = MONTH

    def formula(individu, period):
        taux_incapacite = individu('taux_accident_travail', period)
        return select([taux_incapacite < 10, taux_incapacite < 50, taux_incapacite >= 50],
                      [0, (taux_incapacite / 2) / 100, ((50 / 2) + ((taux_incapacite - 50) * 1.5)) / 100],
                      )


class rente_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Montant mensuel de la rente d’accident du travail"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rent_at = parameters(period).cotsoc
        taux_rente_accident_travail = individu('taux_rente_accident_travail', period)
        previous_year = period.start.period('year').offset(-1)
        salaire_annuel = individu('salaire_net', previous_year, options = [ADD])
        rente_salaire_minimum = rent_at.rent_at.rente_salaire_minimum
        salaire_annuel = select(
            [salaire_annuel <= (rente_salaire_minimum * 2), salaire_annuel <= (rente_salaire_minimum * 8),
             salaire_annuel > (rente_salaire_minimum * 8)],
            [salaire_annuel, rente_salaire_minimum * 2 + (salaire_annuel - rente_salaire_minimum * 2)/3, 0],
        )

        return taux_rente_accident_travail * salaire_annuel

