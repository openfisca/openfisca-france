# -*- coding: utf-8 -*-

from __future__ import division


import datetime
import os
import numpy as np

#%%
import logging


from numpy import maximum as max_, minimum as min_, where


from openfisca_core import periods
from openfisca_core.parameters import load_parameter_file
from openfisca_core.columns import FloatCol
from openfisca_core.reforms import Reform
from openfisca_france.model.base import *
from ..cache import tax_benefit_system


log = logging.getLogger(__name__)

parameter_file = os.path.join(os.path.dirname(__file__), 'assets', 'prestation_unifiee.yaml')

def create_fusion_rsa_apl_progressive(socle = 600):

    class fusion_rsa_apl_progressive(Reform):
        name = u'Fusion RSA-APL progressif'

        def apply(self):

            class prestation_unifiee(Variable):
                value_type = float
                label = u"Prestation unifiée"
                entity = Famille
                definition_period = MONTH

                def formula(famille, period, parameters):
                    rsa_eligibilite = famille('rsa_eligibilite', period)
                    rsa_socle_non_majore = famille('rsa_socle', period)
                    rsa_socle_majore = famille('rsa_socle_majore', period)
                    rsa_socle = max_(rsa_socle_non_majore, rsa_socle_majore)
                    rsa_revenu_activite = famille('rsa_revenu_activite', period)
                    rsa_base_ressources = famille('rsa_base_ressources', period)
                    parameters_rsa = parameters(period).prestations.minima_sociaux.rsa
                    parameters_prestation_unifiee = parameters(period).prestation_unifiee
                    # loyer_imputes = famille('loyer_imputes')
                    zone_apl = famille.demandeur.menage('zone_apl', period)
                    seuil_non_versement = parameters_rsa.rsa_nv
                    premiere_pente = parameters_prestation_unifiee.pente
                    montant_de_base = parameters_rsa.montant_de_base_du_rsa
                    revenu_inflexion = parameters_prestation_unifiee.revenu_inflexion * (rsa_socle / montant_de_base)
                    revenu_sortie = parameters_prestation_unifiee.revenu_sortie * (rsa_socle / montant_de_base)
                    seconde_pente = where(
                        rsa_eligibilite,
                        (
                            (revenu_sortie - (rsa_socle + premiere_pente * revenu_inflexion)) /
                            (revenu_sortie - revenu_inflexion)
                            ),
                        0,
                        )  # deals with denominator being zero and producing nans !
                    majoration_zone_apl = (
                        (zone_apl == 1) * parameters_prestation_unifiee.majoration_zone_1 +
                        (zone_apl == 2) * parameters_prestation_unifiee.majoration_zone_2
                        ) * (rsa_socle / montant_de_base)

                    montant = rsa_eligibilite * (
                        rsa_socle +
                        majoration_zone_apl +
                        premiere_pente * min_(rsa_revenu_activite, revenu_inflexion) +
                        seconde_pente * max_(rsa_revenu_activite - revenu_inflexion, 0) -
                        rsa_base_ressources  # - loyer_imputes
                        )

                    variable_by_name = dict(
                        zone_apl = zone_apl,
                        seuil_non_versement = seuil_non_versement,
                        premiere_pente = premiere_pente,
                        montant_de_base= montant_de_base,
                        revenu_inflexion = revenu_inflexion,
                        revenu_sortie = revenu_sortie,
                        seconde_pente = seconde_pente,
                        montant = montant
                        )
                    for name, variable in variable_by_name.iteritems():
                        if np.isnan(np.sum(variable)):
                            print name

                    return montant * (montant >= seuil_non_versement)

            class minima_sociaux(Variable):
                value_type = float
                entity = Famille
                label = u"Minima sociaux"
                reference = "http://fr.wikipedia.org/wiki/Minima_sociaux"
                definition_period = YEAR

                def formula(self, simulation, period):
                    aah_holder = simulation.compute_add('aah', period)
                    caah_holder = simulation.compute_add('caah', period)
                    aefa = simulation.calculate('aefa', period)
                    api = simulation.calculate('api', period)
                    ass = simulation.calculate_add('ass', period)
                    minimum_vieillesse = simulation.calculate_add('minimum_vieillesse', period)
                    ppa = simulation.calculate_add('ppa', period)
                    psa = simulation.calculate_add('psa', period)
                    rsa = simulation.calculate_add('rsa', period)
                    prestation_unifiee = simulation.calculate_add('prestation_unifiee', period)
                    aah = self.sum_by_entity(aah_holder)
                    caah = self.sum_by_entity(caah_holder)

                    return aah + caah + minimum_vieillesse + rsa + aefa + api + ass + psa + ppa + prestation_unifiee

            def reform_modify_parameters(reference_parameters_copy):
                period = periods.period(2012)
                reference_parameters_copy.prestations.minima_sociaux.rsa.montant_de_base_du_rsa.update(
                    period = period, value = socle)

                parameters_subtree = load_parameter_file(name = 'prestation_unifiee', file_path = parameter_file)
                reference_parameters_copy.add_child('prestation_unifiee', parameters_subtree)

                return reference_parameters_copy

            neutralized_variables = [
                'apl',
                'als',
                'alf',
                'aefa',
                'ppe_brute',
                'ppe',
                'rsa',
                ]
            for neutralized_variable in neutralized_variables:
                self.neutralize_variable(neutralized_variable)

            self.add_variable(prestation_unifiee)
            self.update_variable(minima_sociaux)
            self.modify_parameters(modifier_function = reform_modify_parameters)

    return fusion_rsa_apl_progressive


def test():
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    reform = create_fusion_rsa_apl_progressive(socle = 600)
    reform_tax_benefit_system = reform(tax_benefit_system)
    year = 2012
    scenario = reform_tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_de_base',
                ),
            ],
        period = periods.period(year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(
            loyer = 1000,
            ),
        )
