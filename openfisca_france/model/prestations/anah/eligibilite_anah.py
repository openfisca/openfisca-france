# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

class rfr_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"RFR d'un individu dans un ménage"
    definition_period = YEAR

    def function(individu, period):
        return individu.has_role(FoyerFiscal.DECLARANT) * individu.foyer_fiscal('rfr', period)

class eligibilite_anah(Variable):
    column = EnumCol(
        enum = Enum([
            u"Très modestes",
            u"Modestes",
            u"A vérifier"
        ])
    )
    entity = Menage
    label = u"Barème d'éligibilité aux aides ANAH"
    definition_period = YEAR

    def function(menage, period):
        departement = menage('depcom',period.first_month).astype(int) / 1000
        in_idf = (departement == 75) + (departement == 77) +
                 (departement == 78) + (departement == 91) +
                 (departement == 92) + (departement == 93) +
                 (departement == 94) + (departement == 95)

        nb_members = menage.nb_persons()

        rfr_individu = menage.members('rfr_individu', period)
        rfr = menage.sum(rfr_individu)

        bareme_idf = select(
            [nb_members==1,nb_members==2,nb_members==3,nb_members==4,nb_members>=5],
            [select([rfr <= 19875,rfr <= 24194, rfr>0],[0,1,2]),
             select([rfr <= 29171,rfr <= 35510, rfr>0],[0,1,2]),
             select([rfr <= 35032,rfr <= 42648, rfr>0],[0,1,2]),
             select([rfr <= 40905,rfr <= 49799, rfr>0],[0,1,2]),
             select([rfr <= 46798+((nb_members-5)*5882),rfr <= 56970+((nb_members-5)*7162), rfr>0],[0,1,2])])

        bareme_out = select(
            [nb_members==1,nb_members==2,nb_members==3,nb_members==4,nb_members>=5],
            [select([rfr <= 14360,rfr <= 18409, rfr>0],[0,1,2]),
             select([rfr <= 21001,rfr <= 26923, rfr>0],[0,1,2]),
             select([rfr <= 25257,rfr <= 32377, rfr>0],[0,1,2]),
             select([rfr <= 29506,rfr <= 37826, rfr>0],[0,1,2]),
             select([rfr <= 33774+((nb_members-5)*4257),rfr <= 43297+((nb_members-5)*5454), rfr>0],[0,1,2])])

        return where(in_idf,bareme_idf,bareme_out)
