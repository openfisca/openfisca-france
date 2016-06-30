# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_

from ...base import *  # noqa analysis:ignore
from .base_ressource import nb_enf


class ars(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de rentrée scolaire"
    url = "http://vosdroits.service-public.fr/particuliers/F1878.xhtml"

    def function(self, simulation, period):
        '''
        Allocation de rentrée scolaire brute de CRDS
        '''
        period_br = period.this_year
        period = period.start.offset('first-of', 'year').offset(9, 'month').period('month')
        age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period)
        base_ressources = simulation.calculate('prestations_familiales_base_ressources', period_br.this_month)
        P = simulation.legislation_at(period.start).prestations.prestations_familiales
        # TODO: convention sur la mensualisation
        # On tient compte du fait qu'en cas de léger dépassement du plafond, une allocation dégressive
        # (appelée allocation différentielle), calculée en fonction des revenus, peut être versée.
        age = self.split_by_roles(age_holder, roles = ENFS)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)

        bmaf = P.af.bmaf
        # On doit prendre l'âge en septembre
        enf_05 = nb_enf(age, autonomie_financiere, P.ars.age_entree_primaire - 1, P.ars.age_entree_primaire - 1)  # 5 ans et 6 ans avant le 31 décembre
        # enf_05 = 0
        # Un enfant scolarisé qui n'a pas encore atteint l'âge de 6 ans
        # avant le 1er février 2012 peut donner droit à l'ARS à condition qu'il
        # soit inscrit à l'école primaire. Il faudra alors présenter un
        # certificat de scolarité.
        enf_primaire = enf_05 + nb_enf(age, autonomie_financiere, P.ars.age_entree_primaire, P.ars.age_entree_college - 1)
        enf_college = nb_enf(age, autonomie_financiere, P.ars.age_entree_college, P.ars.age_entree_lycee - 1)
        enf_lycee = nb_enf(age, autonomie_financiere, P.ars.age_entree_lycee, P.ars.age_sortie_lycee)

        arsnbenf = enf_primaire + enf_college + enf_lycee

        # Plafond en fonction du nb d'enfants A CHARGE (Cf. article R543)
        ars_plaf_res = P.ars.plafond_ressources * (1 + af_nbenf * P.ars.majoration_par_enf_supp)
        arsbase = bmaf * (
            P.ars.taux_6_10 * enf_primaire +
            P.ars.taux_11_14 * enf_college +
            P.ars.taux_15_17 * enf_lycee
            )
        # Forme de l'ARS  en fonction des enfants a*n - (rev-plaf)/n
        # ars_diff = (ars_plaf_res + arsbase - base_ressources) / arsnbenf
        ars = (arsnbenf > 0) * max_(0, arsbase - max_(0, (base_ressources - ars_plaf_res) / max_(1, arsnbenf)))

        return period_br, ars * (ars >= P.ars.montant_seuil_non_versement)
