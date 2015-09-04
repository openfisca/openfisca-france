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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import logging

from numpy import maximum as max_, minimum as min_


from ....base import *  # noqa analysis:ignore
from .base import montant_csg_crds


log = logging.getLogger(__name__)


build_column(
    'taux_csg_remplacement',
    EnumCol(
        label = u"Taux retenu sur la CSG des revenus de remplacment",
        entity = 'ind',
        enum = Enum([
            u"Non renseigné/non pertinent",
            u"Exonéré",
            u"Taux réduit",
            u"Taux plein",
            ]),
        default = 3,
        ),
    )


############################################################################
# # Allocations chômage
############################################################################


@reference_formula
class csg_deductible_chomage(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        csg_imposable_chomage = simulation.calculate('csg_imposable_chomage', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)
        montant_csg = montant_csg_crds(
            base_avec_abattement = chobrut,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = law.csg.chomage.deductible,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = law.csg.chomage.min_exo * nbh_travail * law.cotsoc.gen.smic_h_b
        csg_deductible_chomage = max_(
            - montant_csg - max_(cho_seuil_exo - (chobrut + csg_imposable_chomage + montant_csg), 0),
            0,
            )

        return period, - csg_deductible_chomage


@reference_formula
class csg_imposable_chomage(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_avec_abattement = chobrut,
            law_node = law.csg.chomage.imposable,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = law.csg.chomage.min_exo * nbh_travail * law.cotsoc.gen.smic_h_b
        csg_imposable_chomage = max_(- montant_csg - max_(cho_seuil_exo - (chobrut + montant_csg), 0), 0)
        return period, - csg_imposable_chomage


@reference_formula
class crds_chomage(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les allocations chômage"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        csg_deductible_chomage = simulation.calculate('csg_deductible_chomage', period)
        csg_imposable_chomage = simulation.calculate('csg_imposable_chomage', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        smic_h_b = law.cotsoc.gen.smic_h_b
        # salaire_mensuel_reference = chobrut / .7
        # heures_mensuelles = min_(salaire_mensuel_reference / smic_h_b, 35 * 52 / 12)  # TODO: depuis 2001 mais avant ?
        heures_mensuelles = 35 * 52 / 12
        cho_seuil_exo = law.csg.chomage.min_exo * heures_mensuelles * smic_h_b

        montant_crds = montant_csg_crds(
            base_avec_abattement = chobrut,
            law_node = law.crds.activite,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (2 <= taux_csg_remplacement)

        crds_chomage = max_(
            -montant_crds - max_(
                cho_seuil_exo - (chobrut + csg_imposable_chomage + csg_deductible_chomage + montant_crds), 0
                ), 0
            )
        return period, -crds_chomage


@reference_formula
class cho(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage imposables"
    set_input = set_input_divide_by_period
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm"

    def function(self, simulation, period):
        period = period
        chobrut = simulation.calculate('chobrut', period)
        csg_deductible_chomage = simulation.calculate_add('csg_deductible_chomage', period)

        return period, chobrut + csg_deductible_chomage


@reference_formula
class chonet(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    def function(self, simulation, period):
        period = period
        cho = simulation.calculate('cho', period)
        csg_imposable_chomage = simulation.calculate_add('csg_imposable_chomage', period)
        crds_chomage = simulation.calculate_add('crds_chomage', period)

        return period, cho + csg_imposable_chomage + crds_chomage


############################################################################
# # Pensions
############################################################################

@reference_formula
class csg_deductible_retraite(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = rstbrut,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = law.csg.retraite.deductible,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


@reference_formula
class csg_imposable_retraite(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = rstbrut,
            law_node = law.csg.retraite.imposable,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


@reference_formula
class crds_retraite(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les pensions de retraite"
    url = u"http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            base_sans_abattement = rstbrut,
            law_node = law.crds.retraite,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (taux_csg_remplacement == 1)
        return period, montant_crds


@reference_formula
class casa(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle de solidarité et d'autonomie"
    url = u"http://www.service-public.fr/actualites/002691.html"

    @dated_function(date(2013, 4, 1))
    def function_2013(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        rfr_holder = simulation.compute('rfr', period.start.offset('first-of', 'year').offset(-2, 'year').period('year'))
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        rfr = self.cast_from_entity_to_roles(rfr_holder)

        casa = (taux_csg_remplacement == 3) * law.prelsoc.add_ret * rstbrut * (rfr > 13900)
        # TODO: insert in parameters file and deal with nombre de part fiscales

        return period, - casa


@reference_formula
class rst(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite imposables"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/F415.xhtml"

    def function(self, simulation, period):
        period = period
        rstbrut = simulation.calculate_add('rstbrut', period)
        csg_deductible_retraite = simulation.calculate_add('csg_deductible_retraite', period)

        return period, rstbrut + csg_deductible_retraite


@reference_formula
class rstnet(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    # def function(self, rst, csg_imposable_retraite, crds_retraite, casa):
    # return rst + csg_imposable_retraite + crds_retraite + casa
    def function(self, simulation, period):
        period = period
        rst = simulation.calculate('rst', period)
        csg_imposable_retraite = simulation.calculate_add('csg_imposable_retraite', period)
        crds_retraite = simulation.calculate_add('crds_retraite', period)

        return period, rst + csg_imposable_retraite + crds_retraite


@reference_formula
class crds_pfam(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"CRDS sur les prestations familiales)"
    url = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"

    def function(self, simulation, period):
        '''
        Renvoie la CRDS des prestations familiales
        '''
        period = period
        af = simulation.calculate_add('af', period)
        cf = simulation.calculate_add('cf', period)
        asf = simulation.calculate_add('asf', period)
        ars = simulation.calculate('ars', period)
        paje = simulation.calculate_add('paje', period)
        ape = simulation.calculate_add('ape', period)
        apje = simulation.calculate_add('apje', period)
        _P = simulation.legislation_at(period.start)

        return period, -(af + cf + asf + ars + paje + ape + apje) * _P.fam.af.crds
