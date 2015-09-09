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

# import logging

from openfisca_core import columns, formulas, reforms
# from openfisca_core.taxscales import MarginalRateTaxScale

from .. import entities


# log = logging.getLogger(__name__)


def brut_to_target(target_name = None, period = None, simulation = None, **input_array_by_name):
    simulation = simulation.clone(debug = simulation.debug, debug_all = simulation.debug_all, trace = simulation.trace)
    simulation.get_or_new_holder(target_name).delete_arrays()
    for variable_name, array in input_array_by_name.iteritems():
        simulation.get_or_new_holder(variable_name).set_array(period, array)
    return simulation.calculate_add(target_name)


def build_reform(tax_benefit_system):
    from scipy.optimize import fsolve

    Reform = reforms.make_reform(
        key = 'inversion_revenus',
        name = u'Inversion des revenus',
        reference = tax_benefit_system,
        )

    Reform.input_variable(
        column = columns.FloatCol,
        entity_class = entities.Individus,
        label = u'Salaire imposable utilisé pour remonter au salaire brut',
        name = 'salaire_imposable_pour_inversion',
        )

    @Reform.formula
    class salaire_de_base(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Salaire brut ou traitement indiciaire brut"
        reference = tax_benefit_system.column_by_name["salaire_de_base"]
        url = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-brut.html"

        def function(self, simulation, period):
            """Calcule le salaire brut à partir du salaire imposable ou sinon du salaire net.

            Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
            Note : le supplément familial de traitement est imposable.
            """
    #        period = period.start.offset('first-of', 'month').period('month')

            # Get value for year and divide below.
            salaire_imposable_pour_inversion = simulation.get_array('salaire_imposable_pour_inversion',
                period.start.offset('first-of', 'year').period('year'))
            if salaire_imposable_pour_inversion is None:
                salaire_net = simulation.get_array('salaire_net', period)
                if salaire_net is not None:
                    # Calcule le salaire brut à partir du salaire net par inversion numérique.
                    if (salaire_net == 0).all():
                        # Quick path to avoid fsolve when using default value of input variables.
                        return period, salaire_net
                    simulation = self.holder.entity.simulation

                    def solve_function(salaire_de_base):
                        return brut_to_target(
                            target_name = 'salaire_net',
                            period = period,
                            salaire_de_base = salaire_de_base,
                            simulation = simulation,
                            ) - salaire_net
                    return period, fsolve(solve_function, salaire_net)

                salaire_imposable_pour_inversion = simulation.calculate_add_divide('salaire_imposable_pour_inversion',
                    period)

            # Calcule le salaire brut à partir du salaire imposable par inversion numérique.
            if (salaire_imposable_pour_inversion == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, salaire_imposable_pour_inversion
            simulation = self.holder.entity.simulation

            def solve_function(salaire_de_base):
                return brut_to_target(
                    target_name = 'salaire_imposable',
                    period = period,
                    salaire_de_base = salaire_de_base,
                    simulation = simulation,
                    ) - salaire_imposable_pour_inversion

            return period, fsolve(solve_function, salaire_imposable_pour_inversion)

    #       TODO: inclure un taux de prime et calculer les primes en même temps que salaire_de_base

    #        # Calcule le salaire brut à partir du salaire imposable.
    #        # Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
    #        # Note : le supplément familial de traitement est imposable.
    #
    #        hsup = simulation.calculate('hsup', period)
    #        type_sal = simulation.calculate('type_sal', period)
    #        P = simulation.legislation_at(period.start)
    #
    #        plafond_securite_sociale = P.cotsoc.gen.plafond_securite_sociale
    #
    #        salarie = P.cotsoc.sal.scale_tax_scales(plafond_securite_sociale)
    #        csg = P.csg.scale_tax_scales(plafond_securite_sociale)
    #
    #        salarie['noncadre'].update(salarie['commun'])
    #        salarie['cadre'].update(salarie['commun'])
    #
    #        # log.info(
    #        #     "Le dictionnaire des barèmes des cotisations salariés des titulaires de l'Etat contient : \n %s",
    #        #     salarie['fonc']["etat"],
    #        #     )
    #
    #        # Salariés du privé
    #
    #        noncadre = salarie['noncadre'].combine_tax_scales()
    #        cadre = salarie['cadre'].combine_tax_scales()
    #
    #        # On ajoute la CSG deductible
    #        noncadre.add_tax_scale(csg['activite']['deductible'])
    #        cadre.add_tax_scale(csg['activite']['deductible'])
    #
    #        nca = noncadre.inverse()
    #        cad = cadre.inverse()
    #        brut_nca = nca.calc(salaire_imposable_pour_inversion)
    #        brut_cad = cad.calc(salaire_imposable_pour_inversion)
    #        salbrut = brut_nca * (type_sal == CAT['prive_non_cadre'])
    #        salbrut += brut_cad * (type_sal == CAT['prive_cadre'])
    #
    #        # public etat
    #        # TODO: modifier la contribution exceptionelle de solidarité
    #        # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
    #        # et en tenant compte des éléments de l'assiette
    #        salarie['fonc']['etat']['excep_solidarite'] = salarie['fonc']['commun']['solidarite']
    #
    #        public_etat = salarie['fonc']['etat']['pension']
    #        # public_colloc = salarie['fonc']["colloc"].combine_tax_scales()  TODO
    #
    #        # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
    #        # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
    #        bareme_csg_titulaire_etat = csg['act']['deduc'].multiply_rates(1 + TAUX_DE_PRIME, inplace = False,
    #            new_name = "csg deduc titutaire etat")
    #        public_etat.add_tax_scale(bareme_csg_titulaire_etat)
    #        bareme_prime = MarginalRateTaxScale(name = "taux de prime")
    #        bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
    #        public_etat.add_tax_scale(bareme_prime)
    #
    #        etat = public_etat.inverse()
    #
    #        # TODO: complete this to deal with the fonctionnaire
    #        # supp_familial_traitement = 0  # TODO: dépend de salbrut
    #        # indemnite_residence = 0  # TODO: fix bug
    #
    #        # print 'salaire_imposable_pour_inversion', salaire_imposable_pour_inversion
    #        brut_etat = etat.calc(salaire_imposable_pour_inversion)
    #        # print 'brut_etat', brut_etat
    #        # print 'impot', public_etat.calc(brut_etat)
    #        # print 'brut_etat', brut_etat
    #        salbrut_etat = (brut_etat)
    #        # TODO: fonctionnaire
    #        # print 'salbrut_etat', salbrut_etat
    #        salbrut += salbrut_etat * (type_sal == CAT['public_titulaire_etat'])
    #
    #        #<NODE desc= "Supplément familial de traitement " shortname="Supp. fam." code= "supp_familial_traitement"/>
    #        #<NODE desc= "Indemnité de résidence" shortname="Ind. rés." code= "indemenite_residence"/>
    #        return period, salbrut + hsup

    @Reform.formula
    class chobrut(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Allocations chômage brutes"
        url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

        def function(self, simulation, period):
            """"Calcule les allocations chômage brutes à partir des allocations imposables ou sinon des allocations nettes.
            """
            # Get value for year and divide below.
            choi = simulation.get_array('choi', period.start.offset('first-of', 'year').period('year'))
            if choi is None:
                chonet = simulation.get_array('chonet', period)
                if chonet is not None:
                    # Calcule les allocations chomage brutes à partir des allocations nettes par inversion numérique.
                    if (chonet == 0).all():
                        # Quick path to avoid fsolve when using default value of input variables.
                        return period, chonet
                    simulation = self.holder.entity.simulation

                    def solve_function(chobrut):
                        return brut_to_target(
                            chobrut = chobrut,
                            target_name = 'chonet',
                            period = period,
                            simulation = simulation,
                            ) - chonet
                    return period, fsolve(solve_function, chonet)

                choi = simulation.calculate_add_divide('choi', period)

            # Calcule les allocations chômage brutes à partir des allocations imposables.
            # taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
            if (choi == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, choi
            simulation = self.holder.entity.simulation

            def solve_function(chobrut):
                return brut_to_target(
                    chobrut = chobrut,
                    # taux_csg_remplacement = taux_csg_remplacement,
                    target_name = 'cho',
                    period = period,
                    simulation = simulation,
                    ) - choi
            return period, fsolve(solve_function, choi)

    @Reform.formula
    class rstbrut(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Pensions de retraite brutes"
        url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

        def function(self, simulation, period):
            """"Calcule les pensions de retraite brutes à partir des pensions imposables ou sinon des pensions nettes.
            """
            # period = period.start.offset('first-of', 'month').period('month')

            # Get value for year and divide below.
            rsti = simulation.get_array('rsti', period.start.offset('first-of', 'year').period('year'))
            if rsti is None:
                rstnet = simulation.get_array('rstnet', period)
                if rstnet is not None:
                    # Calcule les pensions de retraite brutes à partir des pensions nettes par inversion numérique.
                    if (rstnet == 0).all():
                        # Quick path to avoid fsolve when using default value of input variables.
                        return period, rstnet
                    simulation = self.holder.entity.simulation

                    def solve_function(rstbrut):
                        return brut_to_target(
                            target_name = 'rstnet',
                            period = period,
                            rstbrut = rstbrut,
                            simulation = simulation,
                            ) - rstnet
                    return period, fsolve(solve_function, rstnet)

                rsti = simulation.calculate_add_divide('rsti', period)

            # Calcule les pensions de retraite brutes à partir des pensions imposables.
            taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
            if (rsti == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, rsti
            simulation = self.holder.entity.simulation

            def solve_function(rstbrut):
                return brut_to_target(
                    rstbrut = rstbrut,
                    taux_csg_remplacement = taux_csg_remplacement,
                    target_name = 'rst',
                    period = period,
                    simulation = simulation,
                    ) - rsti
            return period, fsolve(solve_function, rsti)

    return Reform()
