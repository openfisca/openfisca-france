# -*- coding: utf-8 -*-

from __future__ import division

from functools import partial
import logging

from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, logical_and as and_,
    maximum as max_, minimum as min_, timedelta64
    )

from ....base import *  # noqa analysis:ignore
from .....assets.holidays import holidays


log = logging.getLogger(__name__)


class coefficient_proratisation(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Coefficient de proratisation pour le calcul du SMIC et du plafond de la Sécurité sociale"

    def function(self, simulation, period):
        #  * Tous les calculs sont faits sur le mois *

        # Les types de contrats gérés
        contrat_de_travail = simulation.calculate('contrat_de_travail', period)
        # [ temps_plein
        #   temps_partiel
        #   forfait_heures_semaines
        #   forfait_heures_mois
        #   forfait_heures_annee
        #   forfait_jours_annee ]

        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)

        # Volume des heures rémunérées à un forfait heures
        forfait_heures_remunerees_volume = simulation.calculate('forfait_heures_remunerees_volume', period)
        # Volume des heures rémunérées à forfait jours
        forfait_jours_remuneres_volume = simulation.calculate('forfait_jours_remuneres_volume', period)
        heures_duree_collective_entreprise = simulation.calculate('heures_duree_collective_entreprise', period)
        # Volume des heures rémunérées contractuellement (heures/mois, temps partiel)
        heures_remunerees_volume = simulation.calculate('heures_remunerees_volume', period)
        # Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)
        heures_non_remunerees_volume = simulation.calculate('heures_non_remunerees_volume', period)

        # Décompte des jours en début et fin de contrat
        # http://www.gestiondelapaie.com/flux-paie/?1029-la-bonne-premiere-paye

        # Méthode numpy de calcul des jours travaillés
        # @holidays : jours feriés français
        busday_count = partial(original_busday_count, holidays = holidays)

        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1, 'D') # busday ignores the last day

        mois_incomplet = or_(contrat_de_travail_debut > debut_mois, contrat_de_travail_fin < fin_mois)
        # jours travaillés sur l'intersection du contrat de travail et du mois en cours
        jours_travailles_ce_mois = busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois)
            )

        duree_legale_mensuelle = 35 * 52 / 12  # ~151,67

        heures_temps_plein = (
            (heures_duree_collective_entreprise == 0) * duree_legale_mensuelle + heures_duree_collective_entreprise
            )
        # heures remunerees avant conges sans soldes/ijss
        heures_remunerees_volume = (
            # Salariés à temps plein
            (contrat_de_travail == 0) * (
                heures_temps_plein * not_(mois_incomplet) +  # par défaut 151.67
                jours_travailles_ce_mois * 7 * mois_incomplet  # TODO: 7 = heures / jours
                ) +
            # Salariés sans convention de forfait à temps partiel
            (contrat_de_travail == 1) * heures_remunerees_volume
            )

        heures_realisees = heures_remunerees_volume - heures_non_remunerees_volume

        coefficient = (
            # Salariés à temps plein
            (contrat_de_travail == 0) * heures_realisees / heures_temps_plein +
            # Salariés à temps partiel : plafond proratisé en fonction du ratio durée travaillée / durée du temps plein
            #   Salariés sans convention de forfait à temps partiel
            (contrat_de_travail == 1) * heures_realisees / heures_temps_plein +
            #   Salariés avec convention de forfait
            #      Forfait en heures
            (contrat_de_travail >= 2) * (contrat_de_travail <= 3) * (
                forfait_heures_remunerees_volume / 45.7 * 52 / 12
                ) +
            #      Forfait en jours
            (contrat_de_travail == 4) * forfait_jours_remuneres_volume / 218
            )
        return period, coefficient