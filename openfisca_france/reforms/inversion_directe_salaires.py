# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_core.reforms import Reform
from openfisca_core.taxscales import MarginalRateTaxScale


TAUX_DE_PRIME = .10


class salaire_imposable_pour_inversion(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire imposable utilisé pour remonter au salaire brut'
    definition_period = MONTH


class salaire_de_base(Variable):
    definition_period = MONTH

    def formula(individu, period, parameters):
        """Calcule le salaire brut à partir du salaire imposable par inversion du barème
        de cotisations sociales correspondant à la catégorie à laquelle appartient le salarié.
        """
        # Get value for year and divide below.
        salaire_imposable_pour_inversion = individu('salaire_imposable_pour_inversion',
            period.start.offset('first-of', 'year').period('year'))

        # Calcule le salaire brut à partir du salaire imposable.
        # Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
        # Note : le supplément familial de traitement est imposable.

        hsup = individu('hsup', period)
        categorie_salarie = individu('categorie_salarie', period)
        P = parameters(period)

        salarie = P.cotsoc.cotisations_salarie
        plafond_securite_sociale_annuel = P.cotsoc.gen.plafond_securite_sociale * 12
        taux_csg = parameters(period).prelevements_sociaux.contributions.csg.activite.deductible.taux * (1 - .0175)
        csg = MarginalRateTaxScale(name = 'csg')
        csg.add_bracket(0, taux_csg)

#            cat = None
#            if (categorie_salarie == 0).all():
#                cat = 'prive_non_cadre'
#            elif (categorie_salarie == 1).all():
#                cat = 'prive_cadre'
#            elif (categorie_salarie == 2).all():
#                cat = 'public_titulaire_etat'
#            if cat is not None:
#                for name, bareme in salarie[cat].items():
#                    print name, bareme

        prive_non_cadre = salarie['prive_non_cadre'].combine_tax_scales().scale_tax_scales(
            plafond_securite_sociale_annuel)
        prive_cadre = salarie['prive_cadre'].combine_tax_scales().scale_tax_scales(plafond_securite_sociale_annuel)
        # On ajoute la CSG deductible
        prive_non_cadre.add_tax_scale(csg)
        prive_cadre.add_tax_scale(csg)

        salaire_de_base = (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            * prive_non_cadre.inverse().calc(salaire_imposable_pour_inversion)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            * prive_cadre.inverse().calc(salaire_imposable_pour_inversion)
            )

        return salaire_de_base + hsup


class traitement_indiciaire_brut(Variable):
    definition_period = MONTH

    def formula(individu, period, parameters):
        """Calcule le tratement indiciaire brut à partir du salaire imposable.
        """
        # Get value for year and divide below.
        salaire_imposable_pour_inversion = individu('salaire_imposable_pour_inversion',
            period.start.offset('first-of', 'year').period('year'))

        # Calcule le salaire brut à partir du salaire imposable par inversion numérique.
#            if salaire_imposable_pour_inversion == 0 or (salaire_imposable_pour_inversion == 0).all():
#                # Quick path to avoid fsolve when using default value of input variables.
#                return salaire_imposable_pour_inversion

        # Calcule le salaire brut à partir du salaire imposable.
        # Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
        # Note : le supplément familial de traitement est imposable.
        categorie_salarie = individu('categorie_salarie', period)
        P = parameters(period)
        taux_csg = parameters(period).prelevements_sociaux.contributions.csg.activite.deductible.taux * (1 - .0175)
        csg = MarginalRateTaxScale(name = 'csg')
        csg.add_bracket(0, taux_csg)

        salarie = P.cotsoc.cotisations_salarie
#            cat = None
#            if (categorie_salarie == 2).all():
#                cat = 'public_titulaire_etat'
#            if cat is not None:
#                for name, bareme in salarie[cat].items():
#                    print name, bareme

        # public etat
        # TODO: modifier la contribution exceptionelle de solidarité
        # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
        # et en tenant compte des éléments de l'assiette
        # salarie['fonc']['etat']['excep_solidarite'] = salarie['fonc']['commun']['solidarite']

        public_titulaire_etat = salarie['public_titulaire_etat']  # .copy()
        public_titulaire_etat['rafp'].multiply_rates(TAUX_DE_PRIME, inplace = True)
        public_titulaire_etat = salarie['public_titulaire_etat'].combine_tax_scales()

        # public_titulaire_territoriale = salarie['public_titulaire_territoriale'].combine_tax_scales()
        # public_titulaire_hospitaliere = salarie['public_titulaire_hospitaliere'].combine_tax_scales()
        # public_non_titulaire = salarie['public_non_titulaire'].combine_tax_scales()

        # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
        # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
        bareme_csg_public_titulaire_etat = csg.multiply_rates(
            1 + TAUX_DE_PRIME, inplace = False, new_name = "csg deduc titutaire etat")
        public_titulaire_etat.add_tax_scale(bareme_csg_public_titulaire_etat)
        bareme_prime = MarginalRateTaxScale(name = "taux de prime")
        bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
        public_titulaire_etat.add_tax_scale(bareme_prime)

        traitement_indiciaire_brut = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            * public_titulaire_etat.inverse().calc(salaire_imposable_pour_inversion)
            )

        # TODO: complete this to deal with the fonctionnaire
        # supplement_familial_traitement = 0  # TODO: dépend de salbrut
        # indemnite_residence = 0  # TODO: fix bug
        return traitement_indiciaire_brut


class primes_fonction_publique(Variable):
    definition_period = MONTH

    def formula(individu, period, parameters):
        """Calcule les primes.
        """
        # Get value for year and divide below.
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut',
            period.start.offset('first-of', 'year').period('year'))

        return TAUX_DE_PRIME * traitement_indiciaire_brut


class inversion_directe_salaires(Reform):
    key = 'inversion_directe_salaires'
    name = 'Inversion des revenus'

    def apply(self):
        self.add_variable(salaire_imposable_pour_inversion)
        for variable in [traitement_indiciaire_brut, primes_fonction_publique, salaire_de_base]:
            self.update_variable(variable)
