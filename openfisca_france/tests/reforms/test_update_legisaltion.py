# -*- coding: utf-8 -*-

from __future__ import division


import datetime
import numpy as np

#%%
import logging


from numpy import maximum as max_, minimum as min_, where


from openfisca_core import periods
from openfisca_core.columns import FloatCol
from openfisca_core.reforms import Reform, update_legislation
from openfisca_france.model.base import Famille, Variable
from openfisca_france.tests.base import tax_benefit_system


log = logging.getLogger(__name__)


def create_fusion_rsa_apl_progressive(socle = 600):

    class fusion_rsa_apl_progressive(Reform):
        name = u'Fusion RSA-APL progressif'

        def apply(self):

            class prestation_unifiee(Variable):
                column = FloatCol
                label = u"Prestation unifiée"
                entity = Famille

                def function(famille, period, legislation):
                    period = period.this_month
                    rsa_eligibilite = famille('rsa_eligibilite', period)
                    rsa_socle_non_majore = famille('rsa_socle', period)
                    rsa_socle_majore = famille('rsa_socle_majore', period)
                    rsa_socle = max_(rsa_socle_non_majore, rsa_socle_majore)
                    rsa_revenu_activite = famille('rsa_revenu_activite', period)
                    rsa_base_ressources = famille('rsa_base_ressources', period)
                    legislation_rsa = legislation(period).prestations.minima_sociaux.rsa
                    legislation_prestation_unifiee = legislation(period).prestation_unifiee
                    # loyer_imputes = famille('loyer_imputes')
                    zone_apl = famille.demandeur.menage('zone_apl', period)
                    seuil_non_versement = legislation_rsa.rsa_nv
                    premiere_pente = legislation_prestation_unifiee.pente
                    montant_de_base = legislation_rsa.montant_de_base_du_rsa
                    revenu_inflexion = legislation_prestation_unifiee.revenu_inflexion * (rsa_socle / montant_de_base)
                    revenu_sortie = legislation_prestation_unifiee.revenu_sortie * (rsa_socle / montant_de_base)
                    seconde_pente = where(
                        rsa_eligibilite,
                        (
                            (revenu_sortie - (rsa_socle + premiere_pente * revenu_inflexion)) /
                            (revenu_sortie - revenu_inflexion)
                            ),
                        0,
                        )  # deals with denominator being zero and producing nans !
                    majoration_zone_apl = (
                        (zone_apl == 1) * legislation_prestation_unifiee.majoration_zone_1 +
                        (zone_apl == 2) * legislation_prestation_unifiee.majoration_zone_2
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

                    return period, montant * (montant >= seuil_non_versement)

            class minima_sociaux(Variable):
                column = FloatCol
                entity = Famille
                label = u"Minima sociaux"
                url = "http://fr.wikipedia.org/wiki/Minima_sociaux"

                def function(self, simulation, period):
                    period = period.this_year
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

                    return period, aah + caah + minimum_vieillesse + rsa + aefa + api + ass + psa + ppa + prestation_unifiee

            def reform_modify_legislation_json(reference_legislation_json_copy):
                period = periods.period('year', 2012)
                reference_legislation_json_copy = update_legislation(
                    legislation_json = reference_legislation_json_copy,
                    path = [
                        'children', 'prestations',
                        'children', 'minima_sociaux',
                        'children', 'rsa',
                        'children', 'montant_de_base_du_rsa',
                        'values'
                        ],
                    period = period,
                    # start = period.start,
                    value = socle,
                    )
                reform_legislation_subtree = {
                    "@type": "Node",
                    "description": u"Prestation unifiée",
                    "children": {
                        "majoration_zone_1": {
                            "@type": "Parameter",
                            "description": "Majoration zone 1",
                            "format": "integer",
                            "unit": "currency",
                            "values": [{'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': 53}],
                            },
                        "majoration_zone_2": {
                            "@type": "Parameter",
                            "description": "Majoration zone 2",
                            "format": "integer",
                            "unit": "currency",
                            "values": [{'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': 16}],
                            },
                        "pente": {
                            "@type": "Parameter",
                            "description": "Pente",
                            "format": "float",
                            "values": [{'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': .62}],
                            },
                        "revenu_inflexion": {
                            "@type": "Parameter",
                            "description": "Revenu d'inflexion de la pente",
                            "format": "float",
                            "unit": "currency",
                            "values": [{'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': 1150}],
                            },
                        "revenu_sortie": {
                            "@type": "Parameter",
                            "description": "Revenu de sortie de la prestation",
                            "format": "float",
                            "unit": "currency",
                            "values": [{'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': 1500}],
                            },
                        },
                    }
                reference_legislation_json_copy['children']['prestation_unifiee'] = reform_legislation_subtree
                return reference_legislation_json_copy

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
                self.neutralize_column(neutralized_variable)

            self.add_variable(prestation_unifiee)
            self.update_variable(minima_sociaux)
            self.modify_legislation_json(modifier_function = reform_modify_legislation_json)

    return fusion_rsa_apl_progressive


if __name__ == '__main__':
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
        period = periods.period('year', year),
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
