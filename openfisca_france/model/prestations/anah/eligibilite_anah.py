# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

class eligibilite_anah(Variable):
    column = EnumCol(
        enum = Enum([
            u"A vérifier",
            u"Modestes",
            u"Très modestes"
        ])
    )
    entity = Menage
    label = u"Barème d'éligibilité aux aides ANAH"
    definition_period = YEAR

    def formula(menage, period):
        # depcom est le code INSEE de la localité, les deux premiers chiffres sont le département
        # le reste de la division entière par 1000 donne ces deux chiffres sans manipulation de chaînes
        departement = menage('depcom', period.first_month).astype(int) / 1000

        departements_idf = [75, 77, 78, 91, 92, 93, 94, 95]
        in_idf = sum([departement == departement_idf for departement_idf in departements_idf])

        rfr_declarants_principaux_du_menage = menage.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) * menage.members.foyer_fiscal('rfr', period.n_2)
        rfr = menage.sum(rfr_declarants_principaux_du_menage)

        nb_members = menage.nb_persons()

        bareme_idf = select(
            [nb_members == 1, nb_members == 2, nb_members == 3, nb_members == 4, nb_members >= 5],
            [select([rfr <= 19875, rfr <= 24194], [2, 1], 0),
             select([rfr <= 29171, rfr <= 35510], [2, 1], 0),
             select([rfr <= 35032, rfr <= 42648], [2, 1], 0),
             select([rfr <= 40905, rfr <= 49799], [2, 1], 0),
             select([rfr <= 46798 + ((nb_members - 5) * 5882), rfr <= 56970 + ((nb_members - 5) * 7162)], [2, 1], 0)])

        bareme_out = select(
            [nb_members == 1, nb_members == 2, nb_members == 3, nb_members == 4, nb_members >= 5],
            [select([rfr <= 14360, rfr <= 18409], [2, 1], 0),
             select([rfr <= 21001, rfr <= 26923], [2, 1], 0),
             select([rfr <= 25257, rfr <= 32377], [2, 1], 0),
             select([rfr <= 29506, rfr <= 37826], [2, 1], 0),
             select([rfr <= 33774 + ((nb_members - 5) * 4257), rfr <= 43297 + ((nb_members - 5) * 5454)], [2, 1], 0)])

        return where(in_idf, bareme_idf, bareme_out)
