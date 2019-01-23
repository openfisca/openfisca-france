# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa

class rente_accident_travail_salaire(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire annuel pour calculer la rente d’accident du travail"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=7392B9902E4B974EAE8783FAF2D69849.tplgfr30s_1?idArticle=LEGIARTI000006750376&cidTexte=LEGITEXT000006073189&dateTexte=20180823"
    definition_period = MONTH

    def formula(individu, period, parameters):
        previous_year = period.start.period('year').offset(-1)

        rente_at = parameters(period).accident_travail.rente

        salaire_net = individu('salaire_net', previous_year, options=[ADD])
        salaire_net_base = max_(rente_at.salaire_net.salaire_minimum, salaire_net)

        return rente_at.salaire_net.salaire_minimum * rente_at.salaire_net.bareme.calc(
            salaire_net_base / rente_at.salaire_net.salaire_minimum)


class rente_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Montant mensuel de la rente d’accident du travail"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rente_at = parameters(period).accident_travail.rente
        taux_incapacite = individu('taux_accident_travail', period)

        taux = rente_at.taux.bareme.calc(taux_incapacite)
        taux_rente_accident_travail = select(
            [taux_incapacite < rente_at.taux.taux_minimum],
            [0], default=taux
        )
        rente_accident_travail_salaire = individu('rente_accident_travail_salaire', period)

        return rente_accident_travail_salaire * taux_rente_accident_travail
