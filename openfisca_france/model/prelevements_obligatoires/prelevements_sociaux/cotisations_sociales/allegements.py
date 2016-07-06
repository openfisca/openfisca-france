# -*- coding: utf-8 -*-

from __future__ import division

from functools import partial
import logging

from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, logical_and as and_,
    maximum as max_, minimum as min_, round as round_, timedelta64
)
from datetime import datetime

from openfisca_core import periods

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.assets.holidays import holidays

log = logging.getLogger(__name__)


class assiette_allegement(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des allègements de cotisations sociales employeur"

    def function(self, simulation, period):
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        period = period
        # TODO vérifier changement d'assiette
        return period, assiette_cotisations_sociales * (
            (categorie_salarie == CAT['prive_non_cadre']) | (categorie_salarie == CAT['prive_cadre'])
            )


class coefficient_proratisation(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Coefficient de proratisation du salaire notamment pour le calcul du SMIC"

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
        busday_count = partial(original_busday_count, holidays=holidays)  # @holidays : jours feriés français

        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1,
                                                                                     'D')  # busday ignores the last day

        jours_ouvres_ce_mois = busday_count(
            debut_mois,
            fin_mois,
            weekmask='1111100'
        )

        mois_incomplet = or_(contrat_de_travail_debut > debut_mois, contrat_de_travail_fin < fin_mois)
        # jours travaillables sur l'intersection du contrat de travail et du mois en cours
        jours_ouvres_ce_mois_incomplet = busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois),
            weekmask='1111100'
        )

        duree_legale_mensuelle = 35 * 52 / 12  # ~151,67

        heures_temps_plein = switch(heures_duree_collective_entreprise,
                                    {0: duree_legale_mensuelle, 1: heures_duree_collective_entreprise})

        jours_absence = heures_non_remunerees_volume / 7

        coefficient_proratisation_temps_partiel = heures_remunerees_volume / heures_temps_plein
        coefficient_proratisation_forfait_jours = forfait_jours_remuneres_volume / 218

        # temps plein
        coefficient = switch(
            contrat_de_travail,
            {  # temps plein
                0: ((jours_ouvres_ce_mois_incomplet - jours_absence) /
                    jours_ouvres_ce_mois
                    ),
                # temps partiel
                # (en l'absence du détail pour chaque jour de la semaine ou chaque semaine du mois)
                1: coefficient_proratisation_temps_partiel * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_temps_partiel - jours_absence) /
                    (jours_ouvres_ce_mois * coefficient_proratisation_temps_partiel + 1e-16)
                ),
                5: coefficient_proratisation_forfait_jours * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_forfait_jours - jours_absence) /
                    (jours_ouvres_ce_mois * coefficient_proratisation_forfait_jours + 1e-16)
                )
            })

        #      Forfait en heures
        # coefficient = (contrat_de_travail >= 2) * (contrat_de_travail <= 3) * (
        #     forfait_heures_remunerees_volume / 45.7 * 52 / 12
        #     ) +
        return period, coefficient


class credit_impot_competitivite_emploi(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Crédit d'imôt pour la compétitivité et l'emploi"

    @dated_function(date(2013, 1, 1))
    def function_2013_(self, simulation, period):
        period = period.this_month
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        jeune_entreprise_innovante = simulation.calculate('jeune_entreprise_innovante', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        stagiaire = simulation.calculate('stagiaire', period)
        cotsoc = simulation.legislation_at(period.start).cotsoc
        taux_cice = taux_exo_cice(assiette_allegement, smic_proratise, cotsoc)
        credit_impot_competitivite_emploi = taux_cice * assiette_allegement
        non_cumul = not_(stagiaire)
        association = simulation.calculate('entreprise_est_association_non_lucrative', period)

        return period, credit_impot_competitivite_emploi * non_cumul * not_(association)


class aide_premier_salarie(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Aide à l'embauche d'un premier salarié"

    @dated_function(start=date(2015, 6, 9))
    def function(self, simulation, period):
        period = period.this_month
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        apprenti = simulation.calculate('apprenti', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        coefficient_proratisation = simulation.calculate('coefficient_proratisation', period)

        # Cette aide est temporaire.
        # TODO : Si toutefois elle est reconduite et modifiée pour 2017, les dates et le montant seront à
        # implémenter comme des params xml.

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64("2015-06-09"),
            contrat_de_travail_debut <= datetime64("2016-12-31")
        )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée
            contrat_de_travail_duree == 0,
            # durée déterminée supérieure à 1 an
            and_(
                contrat_de_travail_duree == 1,  # CDD
                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
                # Initialement, la condition était d'un contrat >= 12 mois,
                # pour les demandes transmises jusqu'au 26 janvier.
            )
        )

        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut
        eligible = \
            (effectif_entreprise == 1) * not_(apprenti) * eligible_contrat * eligible_duree * eligible_date

        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # TODO comment implémenter la condition "premier employé" ? L'effectif est insuffisant en cas de rupture
        # d'un premier contrat
        # Condition : l’entreprise n’a pas conclu de contrat de travail avec un salarié,
        # au-delà de la période d’essai, dans les 12 mois précédant la nouvelle
        # embauche.

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester
        return period, eligible * (montant_max / 24) * coefficient_proratisation


class aide_embauche_pme(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Aide à l'embauche d'un salarié pour les PME"
    url = u"http://travail-emploi.gouv.fr/grands-dossiers/embauchepme"

    @dated_function(start=date(2016, 1, 18))
    def function(self, simulation, period):
        period = period.this_month
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        apprenti = simulation.calculate('apprenti', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        coefficient_proratisation = simulation.calculate('coefficient_proratisation', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)

        # Cette aide est temporaire.
        # Si toutefois elle est reconduite et modifiée pour 2017, les dates et le montant seront à implémenter comme
        # des params xml.

        # jusqu’à 1,3 fois le Smic
        eligible_salaire = salaire_de_base <= (1.3 * smic_proratise)

        # pour les PME
        eligible_effectif = effectif_entreprise < 250

        # non cumulable avec l'aide pour la première embauche
        # qui est identique, si ce n'est qu'elle couvre tous les salaires
        non_cumulee = effectif_entreprise > 1

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64("2016-01-18"),
            contrat_de_travail_debut <= datetime64("2016-12-31")
        )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée
            contrat_de_travail_duree == 0,
            # durée déterminée supérieure à 1 an
            and_(
                # CDD
                contrat_de_travail_duree == 1,
                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
            )
        )

        # Valable 2 ans seulement
        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut

        eligible = (
            eligible_salaire * eligible_effectif * non_cumulee * eligible_contrat * eligible_duree *
            eligible_date * not_(apprenti)
        )
        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester
        return period, eligible * (montant_max / 24) * coefficient_proratisation


class smic_proratise(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"SMIC proratisé (mensuel)"

    def function(self, simulation, period):
        period = period.this_month
        coefficient_proratisation = simulation.calculate('coefficient_proratisation', period)
        smic_horaire_brut = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
        smic_proratise = coefficient_proratisation * smic_horaire_brut * 35 * 52 / 12

        return period, smic_proratise


class allegement_fillon(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges employeur sur les bas et moyens salaires (dit allègement Fillon)"

    # Attention : cet allègement a des règles de cumul spécifiques

    @dated_function(date(2005, 7, 1))
    def function(self, simulation, period):
        period = period.this_month
        stagiaire = simulation.calculate('stagiaire', period)
        apprenti = simulation.calculate('apprenti', period)
        allegement_mode_recouvrement = simulation.calculate('allegement_fillon_mode_recouvrement', period)

        # switch on 3 possible payment options
        allegement = switch_on_allegement_mode(
            simulation, period,
            allegement_mode_recouvrement,
            self.__class__.__name__,
        )

        return period, allegement * not_(stagiaire) * not_(apprenti)


def compute_allegement_fillon(simulation, period):
    """
        Exonération Fillon
        http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    """
    assiette = simulation.calculate_add('assiette_allegement', period)
    smic_proratise = simulation.calculate_add('smic_proratise', period)
    taille_entreprise = simulation.calculate('taille_entreprise', period)
    majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
    # Calcul du taux
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.
    Pf = simulation.legislation_at(period.start).cotsoc.exo_bas_sal.fillon
    seuil = Pf.seuil
    tx_max = (Pf.tx_max * not_(majoration) + Pf.tx_max2 * majoration)
    if seuil <= 1:
        return 0
    ratio_smic_salaire = smic_proratise / (assiette + 1e-16)
    # règle d'arrondi: 4 décimales au dix-millième le plus proche
    taux_fillon = round_(tx_max * min_(1, max_(seuil * ratio_smic_salaire - 1, 0) / (seuil - 1)), 4)

    # Montant de l'allegment
    return taux_fillon * assiette


class allegement_cotisation_allocations_familiales(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de la cotisation d'allocationos familiales sur les bas et moyens salaires"
    url = u"https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/la-cotisation-dallocations-famil/la-reduction-du-taux-de-la-cotis.html"

    @dated_function(date(2015, 1, 1))
    def function(self, simulation, period):
        period = period.this_month
        stagiaire = simulation.calculate('stagiaire', period)
        apprenti = simulation.calculate('apprenti', period)
        allegement_mode_recouvrement = \
            simulation.calculate('allegement_cotisation_allocations_familiales_mode_recouvrement', period)

        # switch on 3 possible payment options
        allegement = switch_on_allegement_mode(
            simulation, period,
            allegement_mode_recouvrement,
            self.__class__.__name__,
        )

        return period, allegement * not_(stagiaire) * not_(apprenti)


def compute_allegement_cotisation_allocations_familiales(simulation, period):
    """
        La réduction du taux de la cotisation d’allocations familiales
    """
    assiette = simulation.calculate_add('assiette_allegement', period)
    smic_proratise = simulation.calculate_add('smic_proratise', period)
    taille_entreprise = simulation.calculate('taille_entreprise', period)

    law = simulation.legislation_at(period.start).cotsoc.exo_bas_sal.allegement_cotisation_allocations_familiales

    ratio_smic_salaire = assiette / smic_proratise

    # Montant de l'allegment
    return (ratio_smic_salaire < law.seuil) * law.taux * assiette


###############################
#  Helper functions and classes
###############################


def switch_on_allegement_mode(simulation, period, mode_recouvrement, variable_name):
    """
        Switch on 3 possible payment options for allegements

        Name of the computation method specific to the allegement
        should precisely be the variable name prefixed with 'compute_'
    """
    compute_function = globals()['compute_' + variable_name]
    return switch(
        mode_recouvrement,
        {
            0: compute_allegement_annuel(simulation, period, variable_name, compute_function),
            1: compute_allegement_anticipe(simulation, period, variable_name, compute_function),
            2: compute_allegement_progressif(simulation, period, variable_name, compute_function),
        },
    )


def compute_allegement_annuel(simulation, period, variable_name, compute_function):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_function(simulation, period.this_year)


def compute_allegement_anticipe(simulation, period, variable_name, compute_function):
    if period.start.month < 12:
        return compute_function(simulation, period.this_month)
    if period.start.month == 12:
        cumul = simulation.calculate_add(
            variable_name,
            period.start.offset('first-of', 'year').period('month', 11), max_nb_cycles=1)
        return compute_function(
            simulation, period.this_year
        ) - cumul


def compute_allegement_progressif(simulation, period, variable_name, compute_function):
    if period.start.month == 1:
        return compute_function(simulation, period.this_month)

    if period.start.month > 1:
        up_to_this_month = period.start.offset('first-of', 'year').period('month', period.start.month)
        up_to_previous_month = period.start.offset('first-of', 'year').period('month', period.start.month - 1)
        cumul = simulation.calculate_add(variable_name, up_to_previous_month, max_nb_cycles=1)
        return compute_function(simulation, up_to_this_month) - cumul


def taux_exo_cice(assiette_allegement, smic_proratise, P):
    Pc = P.exo_bas_sal.cice
    taux_cice = ((assiette_allegement / (smic_proratise + 1e-16)) <= Pc.max) * Pc.taux
    return taux_cice
