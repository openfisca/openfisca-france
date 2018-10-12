# -*- coding: utf-8 -*-

from numpy.core.defchararray import startswith
from openfisca_france.model.base import *


class TypesEligibiliteANAH(Enum):
    # Needed to preserve the enum order in Python 2
    __order__ = 'a_verifier modestes tres_modeste'
    a_verifier = u"A vérifier"
    modestes = u"Modestes"
    tres_modeste = u"Très modestes"


class eligibilite_anah(Variable):
    value_type = Enum
    possible_values = TypesEligibiliteANAH
    default_value = TypesEligibiliteANAH.a_verifier
    entity = Menage
    label = u"Barème d'éligibilité aux aides ANAH"
    definition_period = YEAR

    def formula(menage, period):
        depcom = menage('depcom', period.first_month)

        departements_idf = [b'75', b'77', b'78', b'91', b'92', b'93', b'94', b'95']
        in_idf = sum([startswith(depcom, departement_idf) for departement_idf in departements_idf])

        rfr_declarants_principaux_du_menage = menage.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) * menage.members.foyer_fiscal('rfr', period.n_2)
        rfr = menage.sum(rfr_declarants_principaux_du_menage)

        nb_members = menage.nb_persons()

        bareme_idf = select(
            [nb_members == 1, nb_members == 2, nb_members == 3, nb_members == 4, nb_members >= 5],
            [select([rfr <= 19875, rfr <= 24194], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 29171, rfr <= 35510], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 35032, rfr <= 42648], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 40905, rfr <= 49799], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 46798 + ((nb_members - 5) * 5882), rfr <= 56970 + ((nb_members - 5) * 7162)], [2, 1], 0)])

        bareme_out = select(
            [nb_members == 1, nb_members == 2, nb_members == 3, nb_members == 4, nb_members >= 5],
            [select([rfr <= 14360, rfr <= 18409], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 21001, rfr <= 26923], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 25257, rfr <= 32377], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 29506, rfr <= 37826], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier),
             select([rfr <= 33774 + ((nb_members - 5) * 4257), rfr <= 43297 + ((nb_members - 5) * 5454)], [TypesEligibiliteANAH.tres_modeste, TypesEligibiliteANAH.modestes], TypesEligibiliteANAH.a_verifier)])

        return where(in_idf, bareme_idf, bareme_out)
