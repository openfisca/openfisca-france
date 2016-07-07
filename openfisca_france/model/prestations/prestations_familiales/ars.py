# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


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
        P = simulation.legislation_at(period.start).fam
        # TODO: convention sur la mensualisation
        # On tient compte du fait qu'en cas de léger dépassement du plafond, une allocation dégressive
        # (appelée allocation différentielle), calculée en fonction des revenus, peut être versée.
        age = self.split_by_roles(age_holder, roles = ENFS)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)

        bmaf = P.af.bmaf
        # On doit prendre l'âge en septembre
        enf_05 = nb_enf(age, autonomie_financiere, P.ars.agep - 1, P.ars.agep - 1)  # 5 ans et 6 ans avant le 31 décembre
        # enf_05 = 0
        # Un enfant scolarisé qui n'a pas encore atteint l'âge de 6 ans
        # avant le 1er février 2012 peut donner droit à l'ARS à condition qu'il
        # soit inscrit à l'école primaire. Il faudra alors présenter un
        # certificat de scolarité.
        enf_primaire = enf_05 + nb_enf(age, autonomie_financiere, P.ars.agep, P.ars.agec - 1)
        enf_college = nb_enf(age, autonomie_financiere, P.ars.agec, P.ars.agel - 1)
        enf_lycee = nb_enf(age, autonomie_financiere, P.ars.agel, P.ars.ages)

        arsnbenf = enf_primaire + enf_college + enf_lycee

        # Plafond en fonction du nb d'enfants A CHARGE (Cf. article R543)
        ars_plaf_res = P.ars.plaf * (1 + af_nbenf * P.ars.plaf_enf_supp)
        arsbase = bmaf * (P.ars.tx0610 * enf_primaire +
                         P.ars.tx1114 * enf_college +
                         P.ars.tx1518 * enf_lycee)
        # Forme de l'ARS  en fonction des enfants a*n - (rev-plaf)/n
        # ars_diff = (ars_plaf_res + arsbase - base_ressources) / arsnbenf
        ars = (arsnbenf > 0) * max_(0, arsbase - max_(0, (base_ressources - ars_plaf_res) / max_(1, arsnbenf)))
        # Calcul net de crds : ars_net = (P.ars.enf0610 * enf_primaire + P.ars.enf1114 * enf_college + P.ars.enf1518 * enf_lycee)

        return period_br, ars * (ars >= P.ars.seuil_nv)
