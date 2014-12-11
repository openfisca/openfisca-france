# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import logical_not as not_
from openfisca_core.taxscales import TaxScalesTree, scale_tax_scales

from ..base import *


log = logging.getLogger(__name__)


# Exonération de CSG et de CRDS sur les revenus du chômage
# et des préretraites si cela abaisse ces revenus sous le smic brut
# TODO: mettre un trigger pour l'éxonération
#       des revenus du chômage sous un smic


############################################################################
# # Allocations chômage
############################################################################

def exo_csg_chom(chobrut, csg_rempl, _P):
    '''
    Indicatrice d'exonération de la CSG sur les revenus du chômage sans exo
    '''
    chonet_sans_exo = (
        chobrut +
        csgchod_sans_exo(chobrut, csg_rempl, _P) +
        csgchoi_sans_exo(chobrut, csg_rempl, _P) +
        crdscho_sans_exo(chobrut, csg_rempl, _P)
        )
    nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
    cho_seuil_exo = _P.csg.chom.min_exo * nbh_travail * _P.cotsoc.gen.smic_h_b
    return (chonet_sans_exo <= cho_seuil_exo)


def csgchod_sans_exo(chobrut, csg_rempl, _P):
    '''
    CSG déductible sur les allocations chômage sans exo
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    csg = scale_tax_scales(TaxScalesTree('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['deduc'].calc(chobrut)
    taux_reduit = csg['reduit']['deduc'].calc(chobrut)
    csgchod = (csg_rempl == 2) * taux_reduit + (csg_rempl == 3) * taux_plein
    return -csgchod


def csgchoi_sans_exo(chobrut, csg_rempl, _P):
    '''
    CSG imposable sur les allocations chômage sans exo
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    csg = scale_tax_scales(TaxScalesTree('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['impos'].calc(chobrut)
    taux_reduit = csg['reduit']['impos'].calc(chobrut)
    csgchoi = (csg_rempl == 2) * taux_reduit + (csg_rempl == 3) * taux_plein
    return -csgchoi


def crdscho_sans_exo(chobrut, csg_rempl, _P):
    '''
    CRDS sur les allocations chômage sans exo
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    crds = scale_tax_scales(_P.crds.act, plaf_ss)
    # TODO: Assiette crds éq pour les salariés et les chômeurs en 2014 mais check before
    return -crds.calc(chobrut) * (2 <= csg_rempl)


@reference_formula
class csgchod(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, chobrut, csg_rempl, P = law):
        isexo = exo_csg_chom(chobrut, csg_rempl, P)
        csgchod = csgchod_sans_exo(chobrut, csg_rempl, P) * not_(isexo)
        return csgchod

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class csgchoi(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, chobrut, csg_rempl, P = law):
        isexo = exo_csg_chom(chobrut, csg_rempl, P)
        csgchoi = csgchoi_sans_exo(chobrut, csg_rempl, P) * not_(isexo)
        return csgchoi

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class crdscho(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les allocations chômage"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"

    def function(self, chobrut, csg_rempl, P = law):
        isexo = exo_csg_chom(chobrut, csg_rempl, P)
        crdscho = crdscho_sans_exo(chobrut, csg_rempl, P) * not_(isexo)
        return crdscho

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class cho(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage imposables"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm"

    def function(self, chobrut, csgchod):
        return chobrut + csgchod

    def get_output_period(self, period):
        return period


@reference_formula
class chonet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage nettes"
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    def function(self, cho, csgchoi, crdscho):
        return cho + csgchoi + crdscho

    def get_output_period(self, period):
        return period


############################################################################
# # Pensions
############################################################################

@reference_formula
class csgrstd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"

    def function(self, rstbrut, csg_rempl, P = law):
        plaf_ss = P.cotsoc.gen.plaf_ss
        csg = scale_tax_scales(TaxScalesTree('csg', P.csg.retraite), plaf_ss)
        taux_plein = csg['plein']['deduc'].calc(rstbrut)
        taux_reduit = csg['reduit']['deduc'].calc(rstbrut)
        csgrstd = (csg_rempl == 3) * taux_plein + (csg_rempl == 2) * taux_reduit
        return -csgrstd

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class csgrsti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"

    def function(self, rstbrut, csg_rempl, P = law):
        plaf_ss = P.cotsoc.gen.plaf_ss
        csg = scale_tax_scales(TaxScalesTree('csg', P.csg.retraite), plaf_ss)
        taux_plein = csg['plein']['impos'].calc(rstbrut)
        taux_reduit = csg['reduit']['impos'].calc(rstbrut)
        csgrsti = (csg_rempl == 3) * taux_plein + (csg_rempl == 2) * taux_reduit
        return -csgrsti

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class crdsrst(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les pensions de retraite"
    url = u"http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"

    def function(self, rstbrut, csg_rempl, P = law):
        plaf_ss = P.cotsoc.gen.plaf_ss
        crds = scale_tax_scales(TaxScalesTree('crds', P.crds.rst), plaf_ss)
        isexo = (csg_rempl == 1)
        return -crds['rst'].calc(rstbrut) * not_(isexo)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class casa(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle de solidarité et d'autonomie"
    url = u"http://www.service-public.fr/actualites/002691.html"

    @dated_function(date(2013, 4, 1))
    def function_2013(self, rstbrut, irpp_holder, csg_rempl, P = law):
        # TODO: replace irpp by irpp_n_2
        # TODO: utiliser la bonne période pour irpp_holder

        irpp = self.cast_from_entity_to_roles(irpp_holder)
        casa = (csg_rempl == 3) * P.prelsoc.add_ret * rstbrut * (irpp > P.ir.recouvrement.seuil)

        return - casa

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class rst(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite imposables"
    url = u"http://vosdroits.service-public.fr/particuliers/F415.xhtml"

    def function(self, rstbrut, csgrstd):
        return rstbrut + csgrstd

    def get_output_period(self, period):
        return period


@reference_formula
class rstnet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite nettes"
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    # def function(self, rst, csgrsti, crdsrst, casa):
    # return rst + csgrsti + crdsrst + casa
    def function(self, rst, csgrsti, crdsrst):
        return rst + csgrsti + crdsrst

    def get_output_period(self, period):
        return period
