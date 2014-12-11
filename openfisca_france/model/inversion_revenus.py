# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

import logging

from numpy import logical_not as not_
from scipy.optimize import fsolve

from openfisca_core.accessors import law
from openfisca_core.taxscales import MarginalRateTaxScale, TaxScalesTree, combine_tax_scales, scale_tax_scales


from .base import FloatCol, Individus, reference_formula, select_function, SelectFormulaColumn
from .cotisations_sociales.remplacement import exo_csg_chom
from .base import CAT, TAUX_DE_PRIME


log = logging.getLogger(__name__)


# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont en CG et BH en 2010

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup

# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés) salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)      salaire total 0,55%
# TODO: accident du travail ?


def brut_to_net(input = None, output_name = None, period = None, simulation = None, **input_array_by_name):
    simulation = simulation.clone(debug = simulation.debug, debug_all = simulation.debug_all)
    simulation.get_holder(output_name).delete_arrays()
    for variable_name, array in input_array_by_name.iteritems():
        simulation.get_or_new_holder(variable_name).set_array(period, array)
    return simulation.calculate(output_name)


############################################################################
# Salaires
############################################################################


# def primes_from_salbrut(salbrut, type_sal):
#     return salbrut * TAUX_DE_PRIME * (type_sal >= 2)


@reference_formula
class salbrut(SelectFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire brut ou traitement indiciaire brut"
    url = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-brut.html"

    @select_function('sali')
    def salbrut_from_sali(self, sali, hsup, type_sal, P = law):
        """Calcule le salaire brut à partir du salaire imposable.

        Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
        Note : le supplément familial de traitement est imposable.
        """
        plaf_ss = P.cotsoc.gen.plaf_ss

        salarie = scale_tax_scales(TaxScalesTree('sal', P.cotsoc.sal), plaf_ss)
        csg = scale_tax_scales(TaxScalesTree('csg', P.csg), plaf_ss)

        salarie['noncadre'].update(salarie['commun'])
        salarie['cadre'].update(salarie['commun'])

        # log.info("Le dictionnaire des barèmes des cotisations salariés des titulaires de l'Etat contient : \n %s",
        #     salarie['fonc']["etat"])

        # Salariés du privé

        noncadre = combine_tax_scales(salarie['noncadre'])
        cadre = combine_tax_scales(salarie['cadre'])

        # On ajoute la CSG deductible
        noncadre.add_tax_scale(csg['act']['deduc'])
        cadre.add_tax_scale(csg['act']['deduc'])

        nca = noncadre.inverse()
        cad = cadre.inverse()
        brut_nca = nca.calc(sali)
        brut_cad = cad.calc(sali)
        salbrut = brut_nca * (type_sal == CAT['prive_non_cadre'])
        salbrut += brut_cad * (type_sal == CAT['prive_cadre'])

        # public etat
        # TODO: modifier la contribution exceptionelle de solidarité
        # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
        # et en tenant compte des éléments de l'assiette
        salarie['fonc']['etat']['excep_solidarite'] = salarie['fonc']['commun']['solidarite']

        public_etat = salarie['fonc']['etat']['pension']
        # public_colloc = combine_tax_scales(salarie['fonc']["colloc"]) TODO:

        # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
        # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
        bareme_csg_titulaire_etat = (csg['act']['deduc']).multiply_rates(1 + TAUX_DE_PRIME, inplace = False,
            new_name = "csg deduc titutaire etat")
        public_etat.add_tax_scale(bareme_csg_titulaire_etat)
        bareme_prime = MarginalRateTaxScale(name = "taux de prime")
        bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
        public_etat.add_tax_scale(bareme_prime)

        etat = public_etat.inverse()

        # TODO: complete this to deal with the fonctionnaire
        # supp_familial_traitement = 0  # TODO: dépend de salbrut
        # indemnite_residence = 0  # TODO: fix bug

        # print 'sali', sali
        brut_etat = etat.calc(sali)
        # print 'brut_etat', brut_etat
        # print 'impot', public_etat.calc(brut_etat)
        # print 'brut_etat', brut_etat
        salbrut_etat = (brut_etat)
        # TODO: fonctionnaire
        # print 'salbrut_etat', salbrut_etat
        salbrut += salbrut_etat * (type_sal == CAT['public_titulaire_etat'])

        # <NODE desc= "Supplément familial de traitement " shortname="Supp. fam." code= "supp_familial_traitement"/>
        # <NODE desc= "Indemnité de résidence" shortname="Ind. rés." code= "indemenite_residence"/>
        return salbrut + hsup

    @select_function('salnet')
    def num_salbrut_from_salnet(self, period, salnet):
        """Calcule les salaires bruts à partir des salaires nets par inversion numérique."""
        if (salnet == 0).all():
            # Quick path to avoid fsolve when using default value of input variables.
            return salnet
        simulation = self.holder.entity.simulation
        function = lambda salbrut: brut_to_net(
            output_name = 'salnet',
            period = period,
            salbrut = salbrut,
            simulation = simulation,
            ) - salnet
        return fsolve(function, salnet)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


############################################################################
# Allocations chômage
############################################################################


@reference_formula
class chobrut(SelectFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage brutes"
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    @select_function('choi')
    def chobrut_from_choi(self, choi, csg_rempl, P = law):
        """Calcule les allocations chômage brute à partir des allocations imposables."""
        csg = scale_tax_scales(TaxScalesTree('csg', P.csg.chom), P.cotsoc.gen.plaf_ss)
        taux_plein = csg['plein']['deduc']
        taux_reduit = csg['reduit']['deduc']

        chom_plein = taux_plein.inverse()
        chom_reduit = taux_reduit.inverse()
        chobrut = (csg_rempl == 1) * choi + (csg_rempl == 2) * chom_reduit.calc(choi) \
            + (csg_rempl == 3) * chom_plein.calc(choi)
        isexo = exo_csg_chom(chobrut, csg_rempl, P)
        chobrut = not_(isexo) * chobrut + (isexo) * choi

        return chobrut

    @select_function('chonet')
    def num_chobrut_from_chonet(self, chonet, period):
        """Calcule les allocations chomage brutes à partir des allocations nettes par inversion numérique."""
        if (chonet == 0).all():
            # Quick path to avoid fsolve when using default value of input variables.
            return chonet
        simulation = self.holder.entity.simulation
        function = lambda chobrut: brut_to_net(
            chobrut = chobrut,
            output_name = 'chonet',
            period = period,
            simulation = simulation,
            ) - chonet
        return fsolve(function, chonet)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


############################################################################
# Pensions
############################################################################


@reference_formula
class rstbrut(SelectFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite brutes"
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    @select_function('rsti')
    def rstbrut_from_rsti(self, rsti, csg_rempl, P = law.csg.retraite):
        """Calcule les pensions de retraites brutes à partir des pensions imposables."""
        rst_plein = P.plein.deduc.inverse()
        rst_reduit = P.reduit.deduc.inverse()
        rstbrut = (csg_rempl == 2) * rst_reduit.calc(rsti) + (csg_rempl == 3) * rst_plein.calc(rsti)
        return rstbrut

    @select_function('rstnet')
    def num_rstbrut_from_rstnet(self, period, rstnet):
        """Calcule les pensions brutes à partir des pensions nettes par inversion numérique."""
        if (rstnet == 0).all():
            # Quick path to avoid fsolve when using default value of input variables.
            return rstnet
        simulation = self.holder.entity.simulation
        function = lambda rstbrut: brut_to_net(
            output_name = 'rstnet',
            period = period,
            rstbrut = rstbrut,
            simulation = simulation,
            ) - rstnet
        return fsolve(function, rstnet)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')
