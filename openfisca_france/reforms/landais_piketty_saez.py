# -*- coding: utf-8 -*-


# TODO switch to to average tax rates


"""Impôt Landais, Piketty, Saez"""

from __future__ import division

import os

from openfisca_france.model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


class assiette_csg(Variable):
    value_type = float
    entity = Individu
    label = u"Assiette de la CSG"
    definition_period = YEAR

    def formula(individu, period, parameters):
        salaire_de_base = individu('salaire_de_base', period, options = [ADD])
        chomage_brut = individu('chomage_brut', period, options = [ADD])
        retraite_brute = individu('retraite_brute', period, options = [ADD])
        rev_cap_bar = individu.foyer_fiscal('rev_cap_bar', period, options = [ADD]) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        rev_cap_lib = individu.foyer_fiscal('rev_cap_lib', period, options = [ADD]) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        return salaire_de_base + chomage_brut + retraite_brute + rev_cap_bar + rev_cap_lib


class impot_revenu_lps(Variable):
    value_type = float
    entity = Individu
    label = u"Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par Landais, Piketty et Saez"
    definition_period = YEAR

    def formula(individu, period, parameters):
        janvier = period.first_month

        nbF = individu.foyer_fiscal('nbF', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        nbH = individu.foyer_fiscal('nbH', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        nbEnf = (nbF + nbH / 2)
        lps = parameters(period).landais_piketty_saez
        ae = nbEnf * lps.abatt_enfant
        re = nbEnf * lps.reduc_enfant
        ce = nbEnf * lps.credit_enfant
        statut_marital = individu('statut_marital', period = janvier)
        couple = (statut_marital == TypesStatutMarital.marie) | (statut_marital == TypesStatutMarital.pacse)
        ac = couple * lps.abatt_conj
        rc = couple * lps.reduc_conj
        assiette_csg = individu('assiette_csg', period)
        return -max_(0, lps.bareme.calc(max_(assiette_csg - ae - ac, 0)) - re - rc) + ce


class revenu_disponible(Variable):
    value_type = float
    entity = Menage
    label = u"Revenu disponible du ménage"
    reference = u"http://fr.wikipedia.org/wiki/Revenu_disponible"
    definition_period = YEAR

    def formula(menage, period, parameters):
        impot_revenu_lps_i = menage.members('impot_revenu_lps', period)
        impot_revenu_lps = menage.sum(impot_revenu_lps_i)
        pen_i = menage.members('pensions', period)
        pen = menage.sum(pen_i)
        prestations_sociales_i = menage.members.famille('prestations_sociales', period) * menage.members.has_role(Famille.DEMANDEUR)
        prestations_sociales = menage.sum(prestations_sociales_i)
        revenus_du_capital_i = menage.members('revenus_du_capital', period)
        revenus_du_capital = menage.sum(revenus_du_capital_i)
        revenus_du_travail_i = menage.members('revenus_du_travail', period)
        revenus_du_travail = menage.sum(revenus_du_travail_i)

        return revenus_du_travail + pen + revenus_du_capital + impot_revenu_lps + prestations_sociales


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'landais_piketty_saez.yaml')
    reform_parameters_subtree = load_parameter_file(name='landais_piketty_saez', file_path=file_path)
    parameters.add_child('landais_piketty_saez', reform_parameters_subtree)
    return parameters


class landais_piketty_saez(Reform):
    name = u'Landais Piketty Saez'

    def apply(self):
        for variable in [assiette_csg, impot_revenu_lps, revenu_disponible]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = modify_parameters)
