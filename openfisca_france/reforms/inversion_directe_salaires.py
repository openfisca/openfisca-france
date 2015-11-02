# -*- coding: utf-8 -*-

from __future__ import division

# import logging

from openfisca_core import columns, formulas, reforms
# from openfisca_core.taxscales import MarginalRateTaxScale

from .. import entities


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
            # Get value for year and divide below.
            salaire_imposable_pour_inversion = simulation.get_array('salaire_imposable_pour_inversion',
                period.start.offset('first-of', 'year').period('year'))

            # Calcule le salaire brut à partir du salaire imposable par inversion numérique.
            if (salaire_imposable_pour_inversion == 0).all():
                # Quick path to avoid fsolve when using default value of input variables.
                return period, salaire_imposable_pour_inversion

           # Calcule le salaire brut à partir du salaire imposable.
           # Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
           # Note : le supplément familial de traitement est imposable.

           hsup = simulation.calculate('hsup', period)
           type_sal = simulation.calculate('type_sal', period)
           P = simulation.legislation_at(period.start)

           salarie = P.cotsoc.cotisations_salarie
           csg = P.csg.scale_tax_scales(plafond_securite_sociale)

           # Salariés du privé
           prive_non_cadre = salarie['prive_non_cadre'].combine_tax_scales()
           prive_cadre = salarie['prive_cadre'].combine_tax_scales()

           # On ajoute la CSG deductible
           prive_non_cadre.add_tax_scale(csg['activite']['deductible'])
           prive_cadre.add_tax_scale(csg['activite']['deductible'])

           salaire_de_base = (
               (type_sal == CAT['prive_non_cadre']) * prive_non_cadre.inverse().calc(salaire_imposable_pour_inversion) +
               (type_sal == CAT['prive_cadre']) * prive_cadre.inverse().calc(salaire_imposable_pour_inversion)
               )

           # public etat
           # TODO: modifier la contribution exceptionelle de solidarité
           # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
           # et en tenant compte des éléments de l'assiette
           salarie['fonc']['etat']['excep_solidarite'] = salarie['fonc']['commun']['solidarite']

           public_titulaire_etat = salarie['public_titulaire_etat'].combine_tax_scales()
           public_titulaire_territoriale = salarie['public_titulaire_territoriale'].combine_tax_scales()
           public_titulaire_hospitaliere = salarie['public_titulaire_hospitaliere'].combine_tax_scales()
           public_non_titulaire = salarie['public_non_titulaire'].combine_tax_scales()

           # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
           # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
           bareme_csg_public_titulaire_etat = csg['act']['deduc'].multiply_rates(1 + TAUX_DE_PRIME, inplace = False,
               new_name = "csg deduc titutaire etat")
           public_etat.add_tax_scale(bareme_csg_titulaire_etat)
           bareme_prime = MarginalRateTaxScale(name = "taux de prime")
           bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
           public_titulaire_etat.add_tax_scale(bareme_prime)

           salaire_de_base += (
                (type_sal == CAT['public_titulaire_etat']) *
                public_titulaire_etat.inverse().calc(salaire_imposable_pour_inversion)
                )
           # TODO: complete this to deal with the fonctionnaire
           # supp_familial_traitement = 0  # TODO: dépend de salbrut
           # indemnite_residence = 0  # TODO: fix bug

           return period, salaire_de_base + hsup

    return Reform()
