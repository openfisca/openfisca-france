# -*- coding: utf-8 -*-
from __future__ import division

from numpy import absolute as abs_, minimum as min_, maximum as max_, where

from ....base import *  # noqa analysis:ignore

class paris_logement_familles_elig(Variable):
    column = BoolCol
    label = u"Eligibilité à Paris-Logement-Familles"
    entity_class = Familles

    def function(self, simulation, period):
        parisien = simulation.calculate('parisien', period)
        statut_occupation = simulation.calculate('statut_occupation_famille', period)
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


class plf_handicap(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation Paris-Logement-Familles en cas d'enfant handicapé"

    def function(self, simulation, period):
        period = period.this_month
        paris_enfant_handicape = simulation.compute('paris_enfant_handicape', period)
        paris_enfant_handicape_garde_alternee = simulation.compute('paris_enfant_handicape_garde_alternee', period)
        br = simulation.calculate('paris_base_ressources_commun', period)
        P = simulation.legislation_at(period.start).paris.paris_logement_familles

        nb_enfant = simulation.calculate('paris_nb_enfants', period)
        nb_enf_handicape = self.sum_by_entity(paris_enfant_handicape)
        nb_enf_handicape_garde_alternee = self.sum_by_entity(paris_enfant_handicape_garde_alternee)

        plafond = simulation.legislation_at(period.start).paris.paris_logement_familles.plafond_haut_3enf
        montant = simulation.legislation_at(period.start).paris.paris_logement_familles.montant_haut_3enf

        plf_handicap = (nb_enf_handicape > 0) * (br <= plafond) * montant

        # Si tous les enfants handicapés sont en garde alternée
        garde_alternee = (nb_enf_handicape - nb_enf_handicape_garde_alternee) == 0
        deduction_garde_alternee = garde_alternee * 0.5 * plf_handicap

        # S'il a plus de 3 enfants
        supa3_enfant = where(nb_enfant > 3, nb_enfant - 3, 0)
        suppl_enfant = where(supa3_enfant > 0, P.montant_haut_enf_sup * supa3_enfant, 0)

        plf_handicap = plf_handicap + suppl_enfant

        plf_handicap = plf_handicap - deduction_garde_alternee
        print plf_handicap
        return period, plf_handicap

class paris_logement_familles(Variable):
    column = FloatCol
    label = u"Allocation Paris Logement Familles"
    entity_class = Familles
    url = "http://www.paris.fr/pratique/toutes-les-aides-et-allocations/aides-sociales/paris-logement-familles-prestation-ville-de-paris/rub_9737_stand_88805_port_24193"  # noqa

    def function(self, simulation, period):
        period = period.this_month
        elig = simulation.calculate('paris_logement_familles_elig', period)
        br = simulation.calculate('paris_base_ressources_commun', period)
        paris_enfant = simulation.compute('paris_enfant', period)
        nbenf = self.sum_by_entity(paris_enfant)
        paris_enfant_garde_alternee = simulation.compute('paris_enfant_garde_alternee', period)
        nbenf_garde_alternee = self.sum_by_entity(paris_enfant_garde_alternee)
        plf_handicap = simulation.calculate('plf_handicap', period)
        loyer = simulation.calculate('loyer', period) + simulation.calculate('charges_locatives', period)
        P = simulation.legislation_at(period.start).paris.paris_logement_familles

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
