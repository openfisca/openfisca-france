import os

from openfisca_france.model.base import *

from .. import entities


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'cesthra_invalidite.yaml')
    reform_parameters_subtree = load_parameter_file(name='cesthra', file_path=file_path)
    parameters.add_child('cesthra', reform_parameters_subtree)
    return parameters


class cesthra(Variable):
    value_type = float
    entity = entities.FoyerFiscal
    label = "Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité"
    definition_period = YEAR
    # PLF 2013 (rejeté) : 'taxe à 75%'

    def formula(foyer_fiscal, period, parameters):
        salaire_imposable_i = foyer_fiscal.members('salaire_imposable', period, options = [ADD])
        _cesthra = parameters(period).cesthra

        cesthra_i = max_(salaire_imposable_i - _cesthra.seuil, 0) * _cesthra.taux

        return foyer_fiscal.sum(cesthra_i)


class irpp(Variable):
    label = 'Impôt sur le revenu des personnes physiques (réformée pour intégrer la cesthra)'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        iai = foyer_fiscal('iai', period)
        credits_impot = foyer_fiscal('credits_impot', period)
        acomptes_ir = foyer_fiscal('acomptes_ir', period)
        contribution_exceptionnelle_hauts_revenus = foyer_fiscal('contribution_exceptionnelle_hauts_revenus', period)
        cesthra = foyer_fiscal('cesthra', period = period)
        recouvrement = parameters(period).impot_revenu.calcul_impot_revenu.recouvrement

        pre_result = iai - credits_impot - acomptes_ir + contribution_exceptionnelle_hauts_revenus + cesthra

        return (
            (iai > recouvrement.seuil)
            * ((pre_result < recouvrement.min) * (pre_result > 0) * iai * 0
            + ((pre_result <= 0) + (pre_result >= recouvrement.min)) * (- pre_result))
            + (iai <= recouvrement.seuil) * ((pre_result < 0) * (-pre_result)
            + (pre_result >= 0) * 0 * iai)
            )


class cesthra_invalidee(Reform):
    name = "Contribution execptionnelle sur les très hauts revenus d'activité (invalidée par le CC)"

    def apply(self):
        self.add_variable(cesthra)
        self.update_variable(irpp)
        self.modify_parameters(modifier_function = modify_parameters)
