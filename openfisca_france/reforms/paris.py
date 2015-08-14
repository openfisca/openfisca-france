# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public Licensegk

# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import copy
import logging

from openfisca_core import columns, formulas, reforms
from numpy import vectorize, absolute as abs_, minimum as min_, maximum as max_


from .. import entities
from ..model.prelevements_obligatoires.impot_revenu import ir


log = logging.getLogger(__name__)


def build_reform(tax_benefit_system):
    # reform_legislation_subtree = {
    #     "@type": "Node",
    #     "description": "Intégration au revenu imposable des allocations familiales",
    #     "children": {
    #         "imposition": {
    #             "@type": "Parameter",
    #             "description": "Indicatrice d'imposition",
    #             "format": "boolean",
    #             "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': True}],
    #         },
    #     },
    # }
    reform_legislation_json = copy.deepcopy(tax_benefit_system.legislation_json)
    # reform_legislation_json['children']['allocations_familiales_imposables'] = reform_legislation_subtree
    # This validates the modified legislation JSON. But the operation is slow so it is commented. Use in development.
    # from openfisca_core import conv, legislations
    # conv.check(legislations.validate_legislation_json)(reform_legislation_json)

    Reform = reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u'Réforme test',
        reference = tax_benefit_system,
    )

    @Reform.formula
    class paris_logement_familles_elig(formulas.SimpleFormulaColumn):
        column = columns.BoolCol
        label = u"Eligibilité à Paris-Logement-Familles"
        entity_class = entities.Familles

        def function(self, simulation, period):
            parisien = simulation.calculate('parisien', period)
            statut_occupation = simulation.calculate('statut_occupation', period)
            charge_logement = (
                (statut_occupation == 1) +
                (statut_occupation == 2) +
                (statut_occupation == 3) +
                (statut_occupation == 4) +
                (statut_occupation == 5) +
                (statut_occupation == 7)
            )

            result = parisien * charge_logement

            return period, result

    @Reform.formula
    class paris_logement_familles_br_i(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        label = u"Base de ressources individuelle pour Paris Logement Famille"
        entity_class = entities.Individus

        def function(self, simulation, period):
            salaire_net = simulation.calculate('salaire_net', period)
            chonet = simulation.calculate('chonet', period)
            rstnet = simulation.calculate('rstnet', period)
            pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
            pensions_alimentaires_versees_individu = simulation.calculate('pensions_alimentaires_versees_individu', period)
            rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_i', period)
            indemnites_journalieres_imposables = simulation.calculate('indemnites_journalieres_imposables', period)
            indemnites_stage = simulation.calculate('indemnites_stage', period)
            revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', period)
            allocation_securisation_professionnelle = simulation.calculate('allocation_securisation_professionnelle', period)
            prestation_compensatoire = simulation.calculate('prestation_compensatoire', period)
            pensions_invalidite = simulation.calculate('pensions_invalidite', period)
            indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', period)
            bourse_recherche = simulation.calculate('bourse_recherche', period)
            gains_exceptionnels = simulation.calculate('gains_exceptionnels', period)
            tns_total_revenus_net = simulation.calculate_add('tns_total_revenus_net', period)

            result = (
                salaire_net + indemnites_chomage_partiel + indemnites_stage + chonet + rstnet +
                pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
                rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
                indemnites_journalieres_imposables + prestation_compensatoire +
                pensions_invalidite + bourse_recherche + gains_exceptionnels + tns_total_revenus_net +
                revenus_stage_formation_pro
            )

            return period, result

    @Reform.formula
    class paris_logement_familles_br(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        label = u"Base de ressource pour Paris Logement Famille"
        entity_class = entities.Familles

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            paris_logement_familles_br_i_holder = simulation.compute('paris_logement_familles_br_i', period)
            paris_logement_familles_br = self.sum_by_entity(paris_logement_familles_br_i_holder)
            result = paris_logement_familles_br

            return period, result

    @Reform.formula
    class plf_enfant_handicape(formulas.SimpleFormulaColumn):
        column = columns.BoolCol
        label = u"Enfant handicapé au sens de la mairie de Paris"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')

            invalide = simulation.calculate('invalide', period)
            plf_enfant = simulation.calculate('plf_enfant', period)

            return period, plf_enfant * invalide

    @Reform.formula
    class plf_enfant(formulas.SimpleFormulaColumn):
        column = columns.BoolCol
        label = u"Enfant pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
            enfant_place = simulation.calculate('enfant_place', period)
            a_charge_fiscale = simulation.calculate('a_charge_fiscale', period)

            return period, est_enfant_dans_famille * (1 - enfant_place) * a_charge_fiscale

    @Reform.formula
    class plf_enfant_garde_alternee(formulas.SimpleFormulaColumn):
        column = columns.BoolCol
        label = u"Enfant en garde alternée pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            alt = simulation.calculate('alt', period)
            plf_enfant = simulation.calculate('plf_enfant', period)

            return period, alt * plf_enfant

    @Reform.formula
    class plf_enfant_handicape_garde_alternee(formulas.SimpleFormulaColumn):
        column = columns.BoolCol
        label = u"Enfant handicapé en garde alternée pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            alt = simulation.calculate('alt', period)
            plf_enfant_handicape = simulation.calculate('plf_enfant_handicape', period)

            return period, alt * plf_enfant_handicape

    @Reform.formula
    class plf_handicap(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        entity_class = entities.Familles
        label = u"Allocation Paris-Logement-Familles en cas d'enfant handicapé"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            plf_enfant_handicape = simulation.compute('plf_enfant_handicape', period)
            plf_enfant_handicape_garde_alternee = simulation.compute('plf_enfant_handicape_garde_alternee', period)
            br = simulation.calculate('paris_logement_familles_br', period)

            nb_enf_handicape = self.sum_by_entity(plf_enfant_handicape)
            nb_enf_handicape_garde_alternee = self.sum_by_entity(plf_enfant_handicape_garde_alternee)

            P = simulation.legislation_at(period.start).aides_locales.paris.paris_logement_familles
            plafond = P.plafond_haut_3enf
            montant = P.montant_haut_3enf

            plf_handicap = (nb_enf_handicape > 0) * (br <= plafond) * montant

            # Si tous les enfants handicapés sont en garde alternée
            garde_alternee = nb_enf_handicape - nb_enf_handicape_garde_alternee == 0
            deduction_garde_alternee = garde_alternee * 0.5 * plf_handicap

            plf_handicap = plf_handicap - deduction_garde_alternee

            return period, plf_handicap

    @Reform.formula
    class paris_logement_familles(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        label = u"Allocation Paris Logement Familles"
        entity_class = entities.Familles
        url = "http://www.paris.fr/pratique/toutes-les-aides-et-allocations/aides-sociales/paris-logement-familles-prestation-ville-de-paris/rub_9737_stand_88805_port_24193"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            elig = simulation.calculate('paris_logement_familles_elig', period)
            br = simulation.calculate('paris_logement_familles_br', period)
            plf_enfant = simulation.compute('plf_enfant', period)
            nbenf = self.sum_by_entity(plf_enfant)
            plf_enfant_garde_alternee = simulation.compute('plf_enfant_garde_alternee', period)
            nbenf_garde_alternee = self.sum_by_entity(plf_enfant_garde_alternee)
            plf_handicap = simulation.calculate('plf_handicap', period)
            loyer = simulation.calculate('loyer', period) + simulation.calculate('charges_locatives', period)
            P = simulation.legislation_at(period.start).aides_locales.paris.paris_logement_familles

            ressources_sous_plaf_bas = (br <= P.plafond_bas_3enf)
            ressources_sous_plaf_haut = (br <= P.plafond_haut_3enf) * (br > P.plafond_bas_3enf)
            montant_base_3enfs = (nbenf >= 3) * (
                ressources_sous_plaf_bas * P.montant_haut_3enf +
                ressources_sous_plaf_haut * P.montant_bas_3enf
            )
            montant_enf_sup = (
                ressources_sous_plaf_bas * P.montant_haut_enf_sup +
                ressources_sous_plaf_haut * P.montant_bas_enf_sup
            )
            montant_3enfs = montant_base_3enfs + montant_enf_sup * max_(nbenf - 3, 0)
            montant_2enfs = (nbenf == 2) * (br <= P.plafond_2enf) * P.montant_2enf

            plf = montant_2enfs + montant_3enfs

            deduction_garde_alternee = (nbenf_garde_alternee > 0) * (
                (nbenf - nbenf_garde_alternee < 3) * 0.5 * plf +
                (nbenf - nbenf_garde_alternee >= 3) * nbenf_garde_alternee * 0.5 * montant_enf_sup
            )

            plf = plf - deduction_garde_alternee

            plf = max_(plf, plf_handicap)
            plf = elig * plf
            plf = min_(plf, loyer)

            return period, plf

    return Reform()
