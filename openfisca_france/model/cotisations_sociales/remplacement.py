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

from numpy import logical_not as not_


from ..base import *  # noqa
from .base import montant_csg_crds


log = logging.getLogger(__name__)


# Exonération de CSG et de CRDS sur les revenus du chômage
# et des préretraites si cela abaisse ces revenus sous le smic brut
# TODO: mettre un trigger pour l'éxonération
#       des revenus du chômage sous un smic


############################################################################
# # Allocations chômage
############################################################################

def exo_csg_chom(chobrut, csg_rempl, law):
    '''
    Indicatrice d'exonération de la CSG sur les revenus du chômage sans exonération
    '''
    chonet_sans_exo = (
        chobrut +
        csgchod_sans_exo(chobrut, csg_rempl, law) +
        csgchoi_sans_exo(chobrut, law) +
        crdscho_sans_exo(chobrut, csg_rempl, law)
        )
    nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
    cho_seuil_exo = law.csg.chomage.min_exo * nbh_travail * law.cotsoc.gen.smic_h_b
    return (chonet_sans_exo <= cho_seuil_exo)


def csgchod_sans_exo(chobrut, csg_rempl, law):
    '''
    CSG déductible sur les allocations chômage sans exonération
    '''
    montant_csg = montant_csg_crds(
        law_node = law.csg.chomage.deductible,
        base_avec_abattement = chobrut,
        indicatrice_taux_plein = (csg_rempl == 3),
        indicatrice_taux_reduit = (csg_rempl == 2),
        plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
        )
    return montant_csg


def csgchoi_sans_exo(chobrut, law):
    '''
    CSG imposable sur les allocations chômage sans exonération
    '''
    montant_csg = montant_csg_crds(
        law_node = law.csg.chomage.imposable,
        base_avec_abattement = chobrut,
        plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
        )
    return montant_csg


def crdscho_sans_exo(chobrut, csg_rempl, law):
    '''
    CRDS sur les allocations chômage sans exonération
    '''
    montant_crds = montant_csg_crds(
        law_node = law.crds.activite,
        base_avec_abattement = chobrut,
        plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
        )
    return montant_crds * (2 <= csg_rempl)


@reference_formula
class csgchod(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)
        isexo = exo_csg_chom(chobrut, csg_rempl, law)
        csgchod = csgchod_sans_exo(chobrut, csg_rempl, law) * not_(isexo)

        return period, csgchod


@reference_formula
class csgchoi(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)
        isexo = exo_csg_chom(chobrut, csg_rempl, law)
        csgchoi = csgchoi_sans_exo(chobrut, law) * not_(isexo)

        return period, csgchoi


@reference_formula
class crdscho(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les allocations chômage"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        chobrut = simulation.calculate('chobrut', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)

        isexo = exo_csg_chom(chobrut, csg_rempl, law)
        crdscho = crdscho_sans_exo(chobrut, csg_rempl, law) * not_(isexo)

        return period, crdscho


@reference_formula
class cho(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage imposables"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm"

    def function(self, simulation, period):
        period = period
        chobrut = simulation.calculate('chobrut', period)
        csgchod = simulation.sum_calculate('csgchod', period)

        return period, chobrut + csgchod


@reference_formula
class chonet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage nettes"
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    def function(self, simulation, period):
        period = period
        cho = simulation.calculate('cho', period)
        csgchoi = simulation.calculate('csgchoi', period)
        crdscho = simulation.calculate('crdscho', period)

        return period, cho + csgchoi + crdscho


############################################################################
# # Pensions
############################################################################

@reference_formula
class csgrstd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            law_node = law.csg.retraite.deductible,
            base_sans_abattement = rstbrut,
            indicatrice_taux_plein = (csg_rempl == 3),
            indicatrice_taux_reduit = (csg_rempl == 2),
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


@reference_formula
class csgrsti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            law_node = law.csg.retraite.imposable,
            base_sans_abattement = rstbrut,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


@reference_formula
class crdsrst(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les pensions de retraite"
    url = u"http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"  # noqa

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rstbrut = simulation.calculate('rstbrut', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            law_node = law.crds.retraite,
            base_sans_abattement = rstbrut,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (csg_rempl == 1)
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
        irpp_holder = simulation.compute('irpp', period)
        csg_rempl = simulation.calculate('csg_rempl', period)
        law = simulation.legislation_at(period.start)

        irpp = self.cast_from_entity_to_roles(irpp_holder)
        casa = (csg_rempl == 3) * law.prelsoc.add_ret * rstbrut * (irpp > law.ir.recouvrement.seuil)

        return period, - casa


@reference_formula
class rst(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite imposables"
    url = u"http://vosdroits.service-public.fr/particuliers/F415.xhtml"

    def function(self, simulation, period):
        period = period
        rstbrut = simulation.calculate('rstbrut', period)
        csgrstd = simulation.sum_calculate('csgrstd', period)

        return period, rstbrut + csgrstd


@reference_formula
class rstnet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite nettes"
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    # def function(self, rst, csgrsti, crdsrst, casa):
    # return rst + csgrsti + crdsrst + casa
    def function(self, simulation, period):
        period = period
        rst = simulation.calculate('rst', period)
        csgrsti = simulation.sum_calculate('csgrsti', period)
        crdsrst = simulation.sum_calculate('crdsrst', period)

        return period, rst + csgrsti + crdsrst
