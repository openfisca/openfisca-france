# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class rente_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Montant mensuel de la rente d’accident du travail"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH
