# -*- coding: utf-8 -*-

from __future__ import division

import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'allocations_familiales_imposables.yaml')
    reform_parameters_subtree = load_parameter_file(name='allocations_familiales_imposables', file_path=file_path)
    parameters.add_child('allocations_familiales_imposables', reform_parameters_subtree)
    return parameters


class allocations_familiales_imposables(Reform):
    name = u'Allocations familiales imposables'

    class rbg(Variable):
        label = u"Nouveau revenu brut global intégrant les allocations familiales"
        definition_period = YEAR

        def formula(foyer_fiscal, period, parameters):
            allocations_familiales_imposables = foyer_fiscal('allocations_familiales_imposables', period, options = [ADD])
            deficit_ante = foyer_fiscal('deficit_ante', period)
            f6gh = foyer_fiscal('f6gh', period)

            nacc_pvce_i = foyer_fiscal.members('nacc_pvce', period)
            nbic_impm_i = foyer_fiscal.members('nbic_impm', period)

            rev_cat = foyer_fiscal('rev_cat', period)
            cga = parameters(period).impot_revenu.rpns.cga_taux2

            nacc_pvce = foyer_fiscal.sum(nacc_pvce_i)
            return max_(
                0,
                allocations_familiales_imposables + rev_cat + f6gh +
                (foyer_fiscal.sum(nbic_impm_i) + nacc_pvce) * (1 + cga) - deficit_ante
                )

    class rfr(Variable):
        label = u"Nouveau revenu fiscal de référence intégrant les allocations familiales"
        definition_period = YEAR

        def formula(foyer_fiscal, period, parameters):
            allocations_familiales_imposables = foyer_fiscal('allocations_familiales_imposables')
            abattement_net_duree_detention_retraite_dirigeant_pme = foyer_fiscal('abattement_net_duree_detention_retraite_dirigeant_pme')
            f3vi_holder = foyer_fiscal.members('f3vi')
            f3vz = foyer_fiscal('f3vz')
            rfr_cd = foyer_fiscal('rfr_cd')
            rni = foyer_fiscal('rni')
            rpns_exon_holder = foyer_fiscal.members('rpns_exon')
            rfr_rvcm_abattements_a_reintegrer = foyer_fiscal('rfr_rvcm_abattements_a_reintegrer') # Supprimée en 2018
            revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD]) # Supprimée en 2018
            revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD]) # Existe à partir de 2018
            microentreprise = foyer_fiscal('microentreprise')

            f3vi = foyer_fiscal.sum(f3vi_holder)
            rpns_exon = foyer_fiscal.sum(rpns_exon_holder)

            return (
                max_(0, rni - allocations_familiales_imposables) +
                rfr_cd + rfr_rvcm_abattements_a_reintegrer + revenus_capitaux_prelevement_liberatoire + revenus_capitaux_prelevement_forfaitaire_unique_ir + f3vi + rpns_exon + abattement_net_duree_detention_retraite_dirigeant_pme + f3vz + microentreprise
                )

            # TO CHECK : f3vb after 2015 (abattements sur moins-values = interdits)


    class allocations_familiales_imposables(Variable):
        value_type = float
        entity = FoyerFiscal
        label = u"Allocations familiales imposables"
        definition_period = YEAR

        def formula(foyer_fiscal, period, parameters):
            imposition = parameters(period).allocations_familiales_imposables.imposition
            af = foyer_fiscal.declarant_principal.famille('af', period, options = [ADD])

            return af * imposition

    def apply(self):
        self.update_variable(self.rbg)
        self.update_variable(self.rfr)
        self.add_variable(self.allocations_familiales_imposables)
        self.modify_parameters(modifier_function = modify_parameters)
