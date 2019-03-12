# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class taux_capacite_travail(Variable):
    value_type = float
    default_value = 1.0
    entity = Individu
    label = u"Taux de capacité de travail, appréciée par la commission des droits et de l'autonomie des personnes handicapées (CDAPH)"
    definition_period = MONTH


class taux_incapacite(Variable):
    value_type = float
    entity = Individu
    label = u"Taux d'incapacité"
    definition_period = MONTH
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=BD54F4B28313142C87FC8B96013E0441.tplgfr44s_1?idArticle=LEGIARTI000023097719&cidTexte=LEGITEXT000006073189&dateTexte=20190312"
    documentation = "Taux d'incapacité retenu pour l'Allocation Adulte Handicapé (AAH)."
