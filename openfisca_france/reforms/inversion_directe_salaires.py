# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_core.reforms import Reform
from openfisca_core.taxscales import MarginalRateTaxScale

import logging

log = logging.getLogger(__name__)

TAUX_DE_PRIME = .10


class salaire_imposable_pour_inversion(Variable):
    column = FloatCol
    entity = Individu
    label = u'Salaire imposable utilisé pour remonter au salaire brut'


class salaire_de_base(Variable):

    def function(self, simulation, period):
        """Calcule le salaire brut à partir du salaire imposable par inversion du barème
        de cotisations sociales correspondant à la catégorie à laquelle appartient le salarié.
        """
        # Get value for year and divide below.
        this_year = period.this_year
        salaire_imposable_pour_inversion = simulation.calculate('salaire_imposable_pour_inversion',
            period = this_year)

        # Calcule le salaire brut (salaire de base) à partir du salaire imposable.

        categorie_salarie = simulation.calculate('categorie_salarie', period = this_year)
        contrat_de_travail = simulation.calculate('contrat_de_travail', period = this_year)
        heures_remunerees_volume = simulation.calculate('heures_remunerees_volume', period = this_year)
        hsup = simulation.calculate('hsup', period = this_year)

        P = simulation.legislation_at(period.start)

        salarie = P.cotsoc.cotisations_salarie
        plafond_securite_sociale_annuel = P.cotsoc.gen.plafond_securite_sociale * 12
        csg_deductible = simulation.legislation_at(period.start).prelevements_sociaux.contributions.csg.activite.deductible
        taux_csg = csg_deductible.taux
        taux_abattement = csg_deductible.abattement.rates[0]
        try:
            seuil_abattement = csg_deductible.abattement.thresholds[1]
        except IndexError:  # Pour gérer le fait que l'abattement n'a pas toujours était limité à 4 PSS
            seuil_abattement = None
        csg = MarginalRateTaxScale(name = 'csg')
        csg.add_bracket(0, taux_csg * (1 - taux_abattement))
        if seuil_abattement is not None:
            csg.add_bracket(seuil_abattement, taux_csg)

        target = dict()
        target['prive_non_cadre'] = set(['maladie', 'arrco', 'vieillesse_deplafonnee', 'vieillesse', 'agff', 'assedic'])
        target['prive_cadre'] = set(
            ['maladie', 'arrco', 'vieillesse_deplafonnee', 'agirc', 'cet', 'apec', 'vieillesse', 'agff', 'assedic']
            )

        for categorie in ['prive_non_cadre', 'prive_cadre']:
            baremes_collection = salarie[categorie]
            baremes_to_remove = list()
            for name, bareme in baremes_collection.iteritems():
                if name.endswith('alsace_moselle'):
                    baremes_to_remove.append(name)
            for name in baremes_to_remove:
                del baremes_collection[name]

        for categorie in ['prive_non_cadre', 'prive_cadre']:
            test = set(
                name for name, bareme in salarie[categorie].iteritems()
                if isinstance(bareme, MarginalRateTaxScale)
                )
            assert target[categorie] == test, 'target: {} \n test {}'.format(target[categorie], test)
        del bareme
        # On ajoute la CSG deductible et on proratise par le plafond de la sécurité sociale
        # Pour éviter les divisions 0 /0 dans le switch
        heures_remunerees_volume_avoid_warning = heures_remunerees_volume + (heures_remunerees_volume == 0) * 1e9
        salaire_imposable_proratise = switch(
            contrat_de_travail,
            {
                # temps plein
                0: salaire_imposable_pour_inversion / plafond_securite_sociale_annuel,
                # temps partiel
                1: salaire_imposable_pour_inversion / (
                    (heures_remunerees_volume_avoid_warning / (52 * 35)) * plafond_securite_sociale_annuel
                    ),
                }
            )
        salaire_de_base = 0.0
        for categorie in ['prive_non_cadre', 'prive_cadre']:
            bareme = salarie[categorie].combine_tax_scales()
            bareme.add_tax_scale(csg)
            brut_proratise = bareme.inverse().calc(salaire_imposable_proratise)
            assert np.isfinite(brut_proratise).all()
            brut = plafond_securite_sociale_annuel * switch(
                contrat_de_travail,
                {
                    # temps plein
                    0: brut_proratise,
                    # temps partiel
                    1: brut_proratise * (heures_remunerees_volume / (52 * 35)),
                    }
                )
            salaire_de_base += (
                (categorie_salarie == CATEGORIE_SALARIE[categorie]) * brut
                )
            assert (salaire_de_base > -1e9).all()
            assert (salaire_de_base < 1e9).all()
        # agirc_gmp
        # gmp = P.prelevements_sociaux.gmp
        # salaire_charniere = gmp.salaire_charniere_annuel
        # cotisation_forfaitaire = gmp.cotisation_forfaitaire_mensuelle_en_euros.part_salariale * 12
        # salaire_de_base += (
        #     (categorie_salarie == CATEGORIE_SALARIE['prive_cadre']) *
        #     (salaire_de_base <= salaire_charniere) *
        #     cotisation_forfaitaire
        #     )
        return period, salaire_de_base + hsup

        # public_titulaire_etat = salarie['public_titulaire_etat'] #.copy()
        # public_titulaire_etat['rafp'].multiply_rates(TAUX_DE_PRIME, inplace = True)
        # public_titulaire_etat = salarie['public_titulaire_etat'].combine_tax_scales()

# class traitement_indiciaire_brut(Variable):

#     def function(self, simulation, period):
#         """Calcule le tratement indiciaire brut à partir du salaire imposable.
#         """
#         # Get value for year and divide below.
#         salaire_imposable_pour_inversion = simulation.calculate('salaire_imposable_pour_inversion',
#             period.start.offset('first-of', 'year').period('year'))

#         # Calcule le salaire brut à partir du salaire imposable.
#         # Sauf pour les fonctionnaires où il renvoie le traitement indiciaire brut
#         # Note : le supplément familial de traitement est imposable.
#         categorie_salarie = simulation.calculate('categorie_salarie', period)
#         P = simulation.legislation_at(period.start)
#         taux_csg = simulation.legislation_at(period.start).prelevements_sociaux.contributions.csg.activite.deductible.taux * (1 - .0175)
#         csg = MarginalRateTaxScale(name = 'csg')
#         csg.add_bracket(0, taux_csg)

#         salarie = P.cotsoc.cotisations_salarie

#         # public etat
#         # TODO: modifier la contribution exceptionelle de solidarité
#         # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
#         # et en tenant compte des éléments de l'assiette
#         # salarie['fonc']['etat']['excep_solidarite'] = salarie['fonc']['commun']['solidarite']

#         public_titulaire_etat = salarie['public_titulaire_etat']  # .copy()
#         public_titulaire_etat['rafp'].multiply_rates(TAUX_DE_PRIME, inplace = True)
#         public_titulaire_etat = salarie['public_titulaire_etat'].combine_tax_scales()

#         # public_titulaire_territoriale = salarie['public_titulaire_territoriale'].combine_tax_scales()
#         # public_titulaire_hospitaliere = salarie['public_titulaire_hospitaliere'].combine_tax_scales()
#         # public_non_titulaire = salarie['public_non_titulaire'].combine_tax_scales()

#         # Pour a fonction publique la csg est calculée sur l'ensemble TIB + primes
#         # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
#         bareme_csg_public_titulaire_etat = csg.multiply_rates(
#             1 + TAUX_DE_PRIME, inplace = False, new_name = "csg deduc titutaire etat")
#         public_titulaire_etat.add_tax_scale(bareme_csg_public_titulaire_etat)
#         bareme_prime = MarginalRateTaxScale(name = "taux de prime")
#         bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
#         public_titulaire_etat.add_tax_scale(bareme_prime)
#         traitement_indiciaire_brut = (
#             (categorie_salarie == CATEGORIE_SALARIE['public_titulaire_etat']) *
#             public_titulaire_etat.inverse().calc(salaire_imposable_pour_inversion)
#             )
#         # TODO: complete this to deal with the fonctionnaire
#         # supp_familial_traitement = 0  # TODO: dépend de salbrut
#         # indemnite_residence = 0  # TODO: fix bug
#         return period, traitement_indiciaire_brut


# class primes_fonction_publique(Variable):

#     def function(self, simulation, period):
#         """Calcule les primes.
#         """
#         # Get value for year and divide below.
#         traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut',
#             period.start.offset('first-of', 'year').period('year'))

#         return period, TAUX_DE_PRIME * traitement_indiciaire_brut


class inversion_directe_salaires(Reform):
    key = 'inversion_directe_salaires'
    name = u'Inversion des revenus'

    def apply(self):
        neutralized_variables = [
            'avantage_en_nature',
            'complementaire_sante_employeur',
            'complementaire_sante_salarie',
            'exoneration_cotisations_employeur_apprenti',
            'exoneration_cotisations_employeur_stagiaire',
            'exoneration_cotisations_salariales_apprenti',
            'exoneration_cotisations_salarie_stagiaire',
            'indemnite_fin_contrat',
            'indemnites_compensatrices_conges_payes',
            'nouvelle_bonification_indiciaire',
            'primes_salaires',
            'prevoyance_obligatoire_cadre',
            'reintegration_titre_restaurant_employeur',
            'reintegration_titre_restaurant_employeur',
            'remuneration_apprenti',
            'stage_gratification_reintegration',
            # To reintegrate
            # Revenus
            'agirc_gmp_salarie',
            'ppe_base',
            'supp_familial_traitement',  # Problème de l'autonomie financière
            'traitement_indiciaire_brut',
            ]
        for neutralized_variable in neutralized_variables:
            log.info("Neutralizing {}".format(neutralized_variable))
            self.neutralize_column(neutralized_variable)

        self.add_variable(salaire_imposable_pour_inversion)
        for variable in [salaire_de_base]:  # traitement_indiciaire_brut, primes_fonction_publique,
            self.update_variable(variable)

