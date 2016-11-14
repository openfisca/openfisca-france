# -*- coding: utf-8 -*-

from __future__ import division

# import logging

from openfisca_core import columns, reforms
# from openfisca_core.taxscales import MarginalRateTaxScale

from .. import entities


# log = logging.getLogger(__name__)


def brut_to_target(target_name = None, period = None, simulation = None, **input_array_by_name):
    simulation = simulation.clone(debug = simulation.debug, debug_all = simulation.debug_all, trace = simulation.trace)
    simulation.get_or_new_holder(target_name).delete_arrays()
    for variable_name, array in input_array_by_name.iteritems():
        simulation.get_or_new_holder(variable_name).put_in_cache(array, period)
    return simulation.calculate_add(target_name)


def build_reform(tax_benefit_system):
    from scipy.optimize import fsolve

    Reform = reforms.make_reform(
        key = 'inversion_revenus',
        name = u'Inversion des revenus',
        reference = tax_benefit_system,
        )

    class salaire_imposable_pour_inversion(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u'Salaire imposable utilisé pour remonter au salaire brut'

    class chomage_imposable_pour_inversion(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u'Autres revenus imposables (chômage, préretraite), utilisé pour l’inversion'

    class retraite_imposable_pour_inversion(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u'Pensions, retraites, rentes connues imposables, utilisé pour l’inversion'

    class salaire_de_base(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u"Salaire brut ou traitement indiciaire brut"
        reference = tax_benefit_system.column_by_name["salaire_de_base"]
        url = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-brut.html"

        def function(self, simulation, period):
            """Calcule le salaire brut à partir du salaire imposable ou sinon du salaire net.

            Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
            Note : le supplément familial de traitement est imposable.
            """
    #        period = period.this_month

            # Get value for year and divide below.
            salaire_imposable_pour_inversion = simulation.get_array('salaire_imposable_pour_inversion',
                period.this_year)
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
    #        categorie_salarie = simulation.calculate('categorie_salarie', period)
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
    #        salbrut = brut_nca * (categorie_salarie == CAT['prive_non_cadre'])
    #        salbrut += brut_cad * (categorie_salarie == CAT['prive_cadre'])
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
    #        salbrut += salbrut_etat * (categorie_salarie == CAT['public_titulaire_etat'])
    #
    #        #<NODE desc= "Supplément familial de traitement " shortname="Supp. fam." code= "supp_familial_traitement"/>
    #        #<NODE desc= "Indemnité de résidence" shortname="Ind. rés." code= "indemenite_residence"/>
    #        return period, salbrut + hsup

    class chomage_brut(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u"Allocations chômage brutes"
        url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

        def function(self, simulation, period):
            """"Calcule les allocations chômage brutes à partir des allocations imposables ou sinon des allocations nettes.
            """
            # Get value for year and divide below.
            chomage_imposable_pour_inversion = simulation.get_array(
                'chomage_imposable_pour_inversion', period.this_year)
            if chomage_imposable_pour_inversion is None:
                chomage_net = simulation.get_array('chomage_net', period)
                if chomage_net is not None:
                    # Calcule les allocations chomage brutes à partir des allocations nettes par inversion numérique.
                    if (chomage_net == 0).all():
                        # Quick path to avoid fsolve when using default value of input variables.
                        return period, chomage_net
                    simulation = self.holder.entity.simulation

                    def solve_function(chomage_brut):
                        return brut_to_target(
                            chomage_brut = chomage_brut,
                            target_name = 'chomage_net',
                            period = period,
                            simulation = simulation,
                            ) - chomage_net
                    return period, fsolve(solve_function, chomage_net)

                chomage_imposable_pour_inversion = simulation.calculate_add_divide(
                    'chomage_imposable_pour_inversion', period)

            # Calcule les allocations chômage brutes à partir des allocations imposables.
            # taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
            if (chomage_imposable_pour_inversion == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, chomage_imposable_pour_inversion
            simulation = self.holder.entity.simulation

            def solve_function(chomage_brut):
                return brut_to_target(
                    chomage_brut = chomage_brut,
                    # taux_csg_remplacement = taux_csg_remplacement,
                    target_name = 'chomage_imposable',
                    period = period,
                    simulation = simulation,
                    ) - chomage_imposable_pour_inversion
            return period, fsolve(solve_function, chomage_imposable_pour_inversion)

    class retraite_brute(Reform.Variable):
        column = columns.FloatCol
        entity = entities.Individu
        label = u"Pensions de retraite brutes"
        url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

        def function(self, simulation, period):
            """"Calcule les pensions de retraite brutes à partir des pensions imposables ou sinon des pensions nettes.
            """
            # period = period.this_month

            # Get value for year and divide below.
            retraite_imposable_pour_inversion = simulation.get_array(
                'retraite_imposable_pour_inversion', period.this_year)
            if retraite_imposable_pour_inversion is None:
                retraite_nette = simulation.get_array('retraite_nette', period)
                if retraite_nette is not None:
                    # Calcule les pensions de retraite brutes à partir des pensions nettes par inversion numérique.
                    if (retraite_nette == 0).all():
                        # Quick path to avoid fsolve when using default value of input variables.
                        return period, retraite_nette
                    simulation = self.holder.entity.simulation

                    def solve_function(retraite_brute):
                        return brut_to_target(
                            target_name = 'retraite_nette',
                            period = period,
                            retraite_brute = retraite_brute,
                            simulation = simulation,
                            ) - retraite_nette
                    return period, fsolve(solve_function, retraite_nette)

                retraite_imposable_pour_inversion = simulation.calculate_add_divide(
                    'retraite_imposable_pour_inversion', period)

            # Calcule les pensions de retraite brutes à partir des pensions imposables.
            taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
            if (retraite_imposable_pour_inversion == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, retraite_imposable_pour_inversion
            simulation = self.holder.entity.simulation

            def solve_function(retraite_brute):
                return brut_to_target(
                    retraite_brute = retraite_brute,
                    taux_csg_remplacement = taux_csg_remplacement,
                    target_name = 'retraite_imposable',
                    period = period,
                    simulation = simulation,
                    ) - retraite_imposable_pour_inversion
            return period, fsolve(solve_function, retraite_imposable_pour_inversion)

    return Reform()
