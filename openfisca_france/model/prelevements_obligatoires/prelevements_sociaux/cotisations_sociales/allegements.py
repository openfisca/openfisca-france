import logging

from numpy import busday_count, datetime64, logical_or as or_, logical_and as and_, timedelta64

from openfisca_core.periods import Period
from openfisca_core.dates import date

from openfisca_france.model.base import *

log = logging.getLogger(__name__)


class assiette_allegement(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette des allègements de cotisations sociales employeur'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period, options = [ADD])
        categorie_salarie = individu('categorie_salarie', period)
        # TODO vérifier changement d'assiette
        return assiette_cotisations_sociales * (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre) | (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            )


class coefficient_proratisation(Variable):
    value_type = float
    entity = Individu
    label = 'Coefficient de proratisation du salaire notamment pour le calcul du Smic'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        #  * Tous les calculs sont faits sur le mois *

        # Les types de contrats gérés
        contrat_de_travail = individu('contrat_de_travail', period)
        TypesContratDeTravail = contrat_de_travail.possible_values
        # [ temps_plein
        #   temps_partiel
        #   forfait_heures_semaines
        #   forfait_heures_mois
        #   forfait_heures_annee
        #   forfait_jours_annee ]

        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)

        # Volume des heures rémunérées à un forfait heures
        forfait_heures_remunerees_volume = individu('forfait_heures_remunerees_volume', period)  # noqa F841
        # Volume des heures rémunérées à forfait jours
        forfait_jours_remuneres_volume = individu('forfait_jours_remuneres_volume', period)
        heures_duree_collective_entreprise = individu('heures_duree_collective_entreprise', period)
        # Volume des heures rémunérées contractuellement (heures/mois, temps partiel)
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        # Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)
        heures_non_remunerees_volume = individu('heures_non_remunerees_volume', period)

        # Décompte des jours en début et fin de contrat
        # http://www.gestiondelapaie.com/flux-paie/?1029-la-bonne-premiere-paye

        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1,
                                                                                     'D')  # busday ignores the last day

        jours_ouvres_ce_mois = busday_count(
            debut_mois,
            fin_mois,
            weekmask='1111100'
            )

        # jours travaillables sur l'intersection du contrat de travail et du mois en cours
        jours_ouvres_ce_mois_incomplet = busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois),
            weekmask='1111100'
            )

        duree_legale_mensuelle = parameters(period).marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel

        heures_temps_plein = where(heures_duree_collective_entreprise,
                                   heures_duree_collective_entreprise,
                                   duree_legale_mensuelle
                                   )

        jours_absence = heures_non_remunerees_volume / 7

        coefficient_proratisation_temps_partiel = heures_remunerees_volume / heures_temps_plein
        coefficient_proratisation_forfait_jours = forfait_jours_remuneres_volume / 218

        # temps plein
        coefficient = switch(
            contrat_de_travail,
            {  # temps plein
                TypesContratDeTravail.temps_plein: (
                    (jours_ouvres_ce_mois_incomplet - jours_absence)
                    / jours_ouvres_ce_mois
                    ),

                # temps partiel
                # (en l'absence du détail pour chaque jour de la semaine ou chaque semaine du mois)
                TypesContratDeTravail.temps_partiel: coefficient_proratisation_temps_partiel * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_temps_partiel - jours_absence)
                    / (jours_ouvres_ce_mois * coefficient_proratisation_temps_partiel + 1e-16)
                    ),

                TypesContratDeTravail.forfait_jours_annee: coefficient_proratisation_forfait_jours * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_forfait_jours - jours_absence)
                    / (jours_ouvres_ce_mois * coefficient_proratisation_forfait_jours + 1e-16)
                    )
                }
            )

        #      Forfait en heures
        # coefficient = (contrat_de_travail >= 2) * (contrat_de_travail <= 3) * (
        #     forfait_heures_remunerees_volume / 45.7 * 52 / 12
        #     ) +
        return (jours_ouvres_ce_mois_incomplet > 0) * coefficient


class credit_impot_competitivite_emploi(Variable):
    value_type = float
    entity = Individu
    label = "Crédit d'impôt pour la compétitivité et l'emploi (CICE)"
    end = '2018-12-31'
    definition_period = MONTH
    calculate_output = calculate_output_add
    set_input = set_input_divide_by_period
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037992483'

    def formula_2013_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        jeune_entreprise_innovante = individu('jeune_entreprise_innovante', period)  # noqa F841
        smic_proratise = individu('smic_proratise', period)
        stagiaire = individu('stagiaire', period)
        taux_cice = taux_exo_cice(assiette_allegement, smic_proratise, parameters(period).prelevements_sociaux.reductions_cotisations_sociales.cice)
        credit_impot_competitivite_emploi = taux_cice * assiette_allegement
        non_cumul = not_(stagiaire)
        association = individu('entreprise_est_association_non_lucrative', period)

        return credit_impot_competitivite_emploi * non_cumul * not_(association)


class aide_premier_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l'embauche du premier salarié"
    definition_period = MONTH
    calculate_output = calculate_output_add
    set_input = set_input_divide_by_period

    def formula_2015_06_09(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        apprenti = individu('apprenti', period)
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        coefficient_proratisation = individu('coefficient_proratisation', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)

        # Cette aide est temporaire.
        # TODO : Si toutefois elle est reconduite et modifiée pour 2017, les dates et le montant seront à
        # implémenter comme des params xml.

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64('2015-06-09'),
            contrat_de_travail_debut <= datetime64('2016-12-31')
            )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée

            contrat_de_travail_type == TypesContrat.cdi,
            # durée déterminée supérieure à 1 an
            and_(contrat_de_travail_type == TypesContrat.cdd,

                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
                # Initialement, la condition était d'un contrat >= 12 mois,
                # pour les demandes transmises jusqu'au 26 janvier.
                 )
            )

        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut
        eligible =\
            (effectif_entreprise == 1) * not_(apprenti) * eligible_contrat * eligible_duree * eligible_date

        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # non cumul avec le dispositif Jeune Entreprise Innovante (JEI)
        non_cumulee = not_(exoneration_cotisations_employeur_jei)

        # TODO comment implémenter la condition "premier employé" ? L'effectif est insuffisant en cas de rupture
        # d'un premier contrat
        # Condition : l’entreprise n’a pas conclu de contrat de travail avec un salarié,
        # au-delà de la période d’essai, dans les 12 mois précédant la nouvelle
        # embauche.

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester
        return eligible * (montant_max / 24) * coefficient_proratisation * non_cumulee


class aide_embauche_pme(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l'embauche TPE/PME"
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000031909980/'
    definition_period = MONTH
    calculate_output = calculate_output_add
    set_input = set_input_divide_by_period

    def formula_2016_01_18(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        apprenti = individu('apprenti', period)
        contrat_de_travail_type = individu('contrat_de_travail_type', period)
        TypesContrat = contrat_de_travail_type.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        coefficient_proratisation = individu('coefficient_proratisation', period)
        smic_proratise = individu('smic_proratise', period)
        salaire_de_base = individu('salaire_de_base', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)
        aide_premier_salarie = individu('aide_premier_salarie', period)

        # Cette aide est temporaire.
        # Si toutefois elle est reconduite et modifiée, les dates et le montant seront à implémenter comme
        # des params xml.

        # jusqu’à 1,3 fois le Smic
        eligible_salaire = salaire_de_base <= (1.3 * smic_proratise)

        # pour les PME
        eligible_effectif = effectif_entreprise < 250

        non_cumulee = and_(
            # non cumulable avec l'aide pour la première embauche
            # qui est identique, si ce n'est qu'elle couvre tous les salaires
            aide_premier_salarie == 0,
            # non cumul avec le dispositif Jeune Entreprise Innovante (JEI)
            not_(exoneration_cotisations_employeur_jei)
            )

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64('2016-01-18'),
            contrat_de_travail_debut <= datetime64('2017-06-30')
            )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée
            contrat_de_travail_type == TypesContrat.cdi,
            # durée déterminée supérieure à 1 an
            and_(
                # CDD
                contrat_de_travail_type == TypesContrat.cdd,
                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
                )
            )

        # Valable 2 ans seulement
        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut

        eligible = (
            eligible_salaire
            * eligible_effectif
            * non_cumulee
            * eligible_contrat
            * eligible_duree
            * eligible_date
            * not_(apprenti)
            )

        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester

        return eligible * (montant_max / 24) * coefficient_proratisation


class smic_proratise(Variable):
    value_type = float
    entity = Individu
    label = 'Smic proratisé (mensuel)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        coefficient_proratisation = individu('coefficient_proratisation', period)
        parameters = parameters(period)
        smic_horaire_brut = parameters.marche_travail.salaire_minimum.smic.smic_b_horaire
        nbh_travail = parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel

        smic_proratise = coefficient_proratisation * smic_horaire_brut * nbh_travail

        return smic_proratise


class allegement_general(Variable):
    value_type = float
    entity = Individu
    label = 'Réduction générale des cotisations patronales (dite réduction Fillon)'
    reference = 'https://www.service-public.fr/professionnels-entreprises/vosdroits/F24542'
    definition_period = MONTH
    calculate_output = calculate_output_add
    set_input = set_input_divide_by_period

    # Attention : cet allègement a des règles de cumul spécifiques

    def formula_2005_07_01(individu, period, parameters):
        stagiaire = individu('stagiaire', period)
        apprenti = individu('apprenti', period)
        allegement_mode_recouvrement = individu('allegement_general_mode_recouvrement', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)
        exoneration_cotisations_employeur_tode = individu('exoneration_cotisations_employeur_tode', period)
        non_cumulee = not_(exoneration_cotisations_employeur_jei + exoneration_cotisations_employeur_tode)

        # Inlined logic from switch_on_allegement_mode:
        # variable_name is 'allegement_general'
        # compute_function becomes compute_allegement_general
        local_compute_function = compute_allegement_general
        TypesAllegementModeRecouvrement = allegement_mode_recouvrement.possible_values
        recouvrement_fin_annee = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
        recouvrement_anticipe = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
        recouvrement_progressif = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

        # Fully inlined logic for allegement calculation
        # local_compute_function (compute_allegement_general) is now inlined below

        TypesAllegementModeRecouvrement = allegement_mode_recouvrement.possible_values
        recouvrement_fin_annee = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
        recouvrement_anticipe = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
        recouvrement_progressif = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

        allegement_annuel_value = 0.0
        if recouvrement_fin_annee:
            if period.start.month == 12:
                sum_val_annuel = 0.0
                for sub_period_ann in period.this_year.get_subperiods(MONTH):
                    calc_assiette_ann = individu('assiette_allegement', sub_period_ann)
                    calc_smic_proratise_ann = individu('smic_proratise', sub_period_ann)
                    calc_effectif_entreprise_ann = individu('effectif_entreprise', sub_period_ann)
                    calc_allegement_general_params_ann = parameters(sub_period_ann).prelevements_sociaux.reductions_cotisations_sociales.allegement_general
                    calc_seuil_ann = 0.0
                    calc_tx_max_ann = 0.0
                    current_period_start_date_ann = sub_period_ann.start.date
                    if date(2003, 7, 1) <= current_period_start_date_ann <= date(2005, 6, 30):
                        calc_seuil_ann = calc_allegement_general_params_ann.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
                        calc_tx_max_ann = calc_allegement_general_params_ann.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
                    elif date(2005, 7, 1) <= current_period_start_date_ann <= date(2019, 12, 31):
                        calc_seuil_ann = calc_allegement_general_params_ann.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_ann = (calc_effectif_entreprise_ann < 20)
                        calc_tx_max_ann = (
                            calc_allegement_general_params_ann.ensemble_des_entreprises.entreprises_de_20_salaries_et_plus * not_(calc_petite_entreprise_ann)
                            + calc_allegement_general_params_ann.ensemble_des_entreprises.entreprises_de_moins_de_20_salaries * calc_petite_entreprise_ann)
                    else:
                        calc_seuil_ann = calc_allegement_general_params_ann.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_ann = (calc_effectif_entreprise_ann < 50)
                        calc_tx_max_ann = (
                            calc_allegement_general_params_ann.ensemble_des_entreprises.entreprises_de_50_salaries_et_plus * not_(calc_petite_entreprise_ann)
                            + calc_allegement_general_params_ann.ensemble_des_entreprises.entreprises_de_moins_de_50_salaries * calc_petite_entreprise_ann)
                    computed_value_for_this_call_ann = 0.0
                    if calc_seuil_ann <= 1:
                        computed_value_for_this_call_ann = 0.0
                    else:
                        calc_ratio_smic_salaire_ann = calc_smic_proratise_ann / (calc_assiette_ann + 1e-16)
                        calc_taux_allegement_general_ann = round_(calc_tx_max_ann * min_(1, max_(calc_seuil_ann * calc_ratio_smic_salaire_ann - 1, 0) / (calc_seuil_ann - 1)), 4)
                        computed_value_for_this_call_ann = calc_taux_allegement_general_ann * calc_assiette_ann
                    sum_val_annuel += computed_value_for_this_call_ann
                allegement_annuel_value = sum_val_annuel

        allegement_anticipe_value = 0.0
        if recouvrement_anticipe:
            if period.start.month < 12:
                current_period_ant_direct = period.first_month
                calc_assiette_ant_direct = individu('assiette_allegement', current_period_ant_direct)
                calc_smic_proratise_ant_direct = individu('smic_proratise', current_period_ant_direct)
                calc_effectif_entreprise_ant_direct = individu('effectif_entreprise', current_period_ant_direct)
                calc_allegement_general_params_ant_direct = parameters(current_period_ant_direct).prelevements_sociaux.reductions_cotisations_sociales.allegement_general
                calc_seuil_ant_direct = 0.0
                calc_tx_max_ant_direct = 0.0
                current_period_start_date_ant_direct = current_period_ant_direct.start.date
                if date(2003, 7, 1) <= current_period_start_date_ant_direct <= date(2005, 6, 30):
                    calc_seuil_ant_direct = calc_allegement_general_params_ant_direct.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
                    calc_tx_max_ant_direct = calc_allegement_general_params_ant_direct.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
                elif date(2005, 7, 1) <= current_period_start_date_ant_direct <= date(2019, 12, 31):
                    calc_seuil_ant_direct = calc_allegement_general_params_ant_direct.ensemble_des_entreprises.plafond
                    calc_petite_entreprise_ant_direct = (calc_effectif_entreprise_ant_direct < 20)
                    calc_tx_max_ant_direct = (
                        calc_allegement_general_params_ant_direct.ensemble_des_entreprises.entreprises_de_20_salaries_et_plus * not_(calc_petite_entreprise_ant_direct)
                        + calc_allegement_general_params_ant_direct.ensemble_des_entreprises.entreprises_de_moins_de_20_salaries * calc_petite_entreprise_ant_direct)
                else:
                    calc_seuil_ant_direct = calc_allegement_general_params_ant_direct.ensemble_des_entreprises.plafond
                    calc_petite_entreprise_ant_direct = (calc_effectif_entreprise_ant_direct < 50)
                    calc_tx_max_ant_direct = (
                        calc_allegement_general_params_ant_direct.ensemble_des_entreprises.entreprises_de_50_salaries_et_plus * not_(calc_petite_entreprise_ant_direct)
                        + calc_allegement_general_params_ant_direct.ensemble_des_entreprises.entreprises_de_moins_de_50_salaries * calc_petite_entreprise_ant_direct)
                computed_value_for_this_call_ant_direct = 0.0
                if calc_seuil_ant_direct <= 1:
                    computed_value_for_this_call_ant_direct = 0.0
                else:
                    calc_ratio_smic_salaire_ant_direct = calc_smic_proratise_ant_direct / (calc_assiette_ant_direct + 1e-16)
                    calc_taux_allegement_general_ant_direct = round_(calc_tx_max_ant_direct * min_(1, max_(calc_seuil_ant_direct * calc_ratio_smic_salaire_ant_direct - 1, 0) / (calc_seuil_ant_direct - 1)), 4)
                    computed_value_for_this_call_ant_direct = calc_taux_allegement_general_ant_direct * calc_assiette_ant_direct
                allegement_anticipe_value = computed_value_for_this_call_ant_direct
            elif period.start.month == 12:
                cumul_anticipe = individu('allegement_general', Period(('month', period.start.offset('first-of', 'year'), 11)), options = [ADD])
                sum_val_ant_sum = 0.0
                for sub_period_ant_sum in period.this_year.get_subperiods(MONTH):
                    calc_assiette_ant_sum = individu('assiette_allegement', sub_period_ant_sum)
                    calc_smic_proratise_ant_sum = individu('smic_proratise', sub_period_ant_sum)
                    calc_effectif_entreprise_ant_sum = individu('effectif_entreprise', sub_period_ant_sum)
                    calc_allegement_general_params_ant_sum = parameters(sub_period_ant_sum).prelevements_sociaux.reductions_cotisations_sociales.allegement_general
                    calc_seuil_ant_sum = 0.0
                    calc_tx_max_ant_sum = 0.0
                    current_period_start_date_ant_sum = sub_period_ant_sum.start.date
                    if date(2003, 7, 1) <= current_period_start_date_ant_sum <= date(2005, 6, 30):
                        calc_seuil_ant_sum = calc_allegement_general_params_ant_sum.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
                        calc_tx_max_ant_sum = calc_allegement_general_params_ant_sum.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
                    elif date(2005, 7, 1) <= current_period_start_date_ant_sum <= date(2019, 12, 31):
                        calc_seuil_ant_sum = calc_allegement_general_params_ant_sum.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_ant_sum = (calc_effectif_entreprise_ant_sum < 20)
                        calc_tx_max_ant_sum = (
                            calc_allegement_general_params_ant_sum.ensemble_des_entreprises.entreprises_de_20_salaries_et_plus * not_(calc_petite_entreprise_ant_sum)
                            + calc_allegement_general_params_ant_sum.ensemble_des_entreprises.entreprises_de_moins_de_20_salaries * calc_petite_entreprise_ant_sum)
                    else:
                        calc_seuil_ant_sum = calc_allegement_general_params_ant_sum.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_ant_sum = (calc_effectif_entreprise_ant_sum < 50)
                        calc_tx_max_ant_sum = (
                            calc_allegement_general_params_ant_sum.ensemble_des_entreprises.entreprises_de_50_salaries_et_plus * not_(calc_petite_entreprise_ant_sum)
                            + calc_allegement_general_params_ant_sum.ensemble_des_entreprises.entreprises_de_moins_de_50_salaries * calc_petite_entreprise_ant_sum)
                    computed_value_for_this_call_ant_sum = 0.0
                    if calc_seuil_ant_sum <= 1:
                        computed_value_for_this_call_ant_sum = 0.0
                    else:
                        calc_ratio_smic_salaire_ant_sum = calc_smic_proratise_ant_sum / (calc_assiette_ant_sum + 1e-16)
                        calc_taux_allegement_general_ant_sum = round_(calc_tx_max_ant_sum * min_(1, max_(calc_seuil_ant_sum * calc_ratio_smic_salaire_ant_sum - 1, 0) / (calc_seuil_ant_sum - 1)), 4)
                        computed_value_for_this_call_ant_sum = calc_taux_allegement_general_ant_sum * calc_assiette_ant_sum
                    sum_val_ant_sum += computed_value_for_this_call_ant_sum
                allegement_anticipe_value = sum_val_ant_sum - cumul_anticipe

        allegement_progressif_value = 0.0
        if recouvrement_progressif:
            if period.start.month == 1:
                current_period_prog_direct = period.first_month
                calc_assiette_prog_direct = individu('assiette_allegement', current_period_prog_direct)
                calc_smic_proratise_prog_direct = individu('smic_proratise', current_period_prog_direct)
                calc_effectif_entreprise_prog_direct = individu('effectif_entreprise', current_period_prog_direct)
                calc_allegement_general_params_prog_direct = parameters(current_period_prog_direct).prelevements_sociaux.reductions_cotisations_sociales.allegement_general
                calc_seuil_prog_direct = 0.0
                calc_tx_max_prog_direct = 0.0
                current_period_start_date_prog_direct = current_period_prog_direct.start.date
                if date(2003, 7, 1) <= current_period_start_date_prog_direct <= date(2005, 6, 30):
                    calc_seuil_prog_direct = calc_allegement_general_params_prog_direct.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
                    calc_tx_max_prog_direct = calc_allegement_general_params_prog_direct.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
                elif date(2005, 7, 1) <= current_period_start_date_prog_direct <= date(2019, 12, 31):
                    calc_seuil_prog_direct = calc_allegement_general_params_prog_direct.ensemble_des_entreprises.plafond
                    calc_petite_entreprise_prog_direct = (calc_effectif_entreprise_prog_direct < 20)
                    calc_tx_max_prog_direct = (
                        calc_allegement_general_params_prog_direct.ensemble_des_entreprises.entreprises_de_20_salaries_et_plus * not_(calc_petite_entreprise_prog_direct)
                        + calc_allegement_general_params_prog_direct.ensemble_des_entreprises.entreprises_de_moins_de_20_salaries * calc_petite_entreprise_prog_direct)
                else:
                    calc_seuil_prog_direct = calc_allegement_general_params_prog_direct.ensemble_des_entreprises.plafond
                    calc_petite_entreprise_prog_direct = (calc_effectif_entreprise_prog_direct < 50)
                    calc_tx_max_prog_direct = (
                        calc_allegement_general_params_prog_direct.ensemble_des_entreprises.entreprises_de_50_salaries_et_plus * not_(calc_petite_entreprise_prog_direct)
                        + calc_allegement_general_params_prog_direct.ensemble_des_entreprises.entreprises_de_moins_de_50_salaries * calc_petite_entreprise_prog_direct)
                computed_value_for_this_call_prog_direct = 0.0
                if calc_seuil_prog_direct <= 1:
                    computed_value_for_this_call_prog_direct = 0.0
                else:
                    calc_ratio_smic_salaire_prog_direct = calc_smic_proratise_prog_direct / (calc_assiette_prog_direct + 1e-16)
                    calc_taux_allegement_general_prog_direct = round_(calc_tx_max_prog_direct * min_(1, max_(calc_seuil_prog_direct * calc_ratio_smic_salaire_prog_direct - 1, 0) / (calc_seuil_prog_direct - 1)), 4)
                    computed_value_for_this_call_prog_direct = calc_taux_allegement_general_prog_direct * calc_assiette_prog_direct
                allegement_progressif_value = computed_value_for_this_call_prog_direct
            elif period.start.month > 1:
                up_to_this_month = Period(('month', period.start.offset('first-of', 'year'), period.start.month))
                up_to_previous_month = Period(('month', period.start.offset('first-of', 'year'), period.start.month - 1))
                cumul_progressif = individu('allegement_general', up_to_previous_month, options = [ADD])
                sum_val_prog_sum = 0.0
                for sub_period_prog_sum in up_to_this_month.get_subperiods(MONTH):
                    calc_assiette_prog_sum = individu('assiette_allegement', sub_period_prog_sum)
                    calc_smic_proratise_prog_sum = individu('smic_proratise', sub_period_prog_sum)
                    calc_effectif_entreprise_prog_sum = individu('effectif_entreprise', sub_period_prog_sum)
                    calc_allegement_general_params_prog_sum = parameters(sub_period_prog_sum).prelevements_sociaux.reductions_cotisations_sociales.allegement_general
                    calc_seuil_prog_sum = 0.0
                    calc_tx_max_prog_sum = 0.0
                    current_period_start_date_prog_sum = sub_period_prog_sum.start.date
                    if date(2003, 7, 1) <= current_period_start_date_prog_sum <= date(2005, 6, 30):
                        calc_seuil_prog_sum = calc_allegement_general_params_prog_sum.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
                        calc_tx_max_prog_sum = calc_allegement_general_params_prog_sum.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
                    elif date(2005, 7, 1) <= current_period_start_date_prog_sum <= date(2019, 12, 31):
                        calc_seuil_prog_sum = calc_allegement_general_params_prog_sum.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_prog_sum = (calc_effectif_entreprise_prog_sum < 20)
                        calc_tx_max_prog_sum = (
                            calc_allegement_general_params_prog_sum.ensemble_des_entreprises.entreprises_de_20_salaries_et_plus * not_(calc_petite_entreprise_prog_sum)
                            + calc_allegement_general_params_prog_sum.ensemble_des_entreprises.entreprises_de_moins_de_20_salaries * calc_petite_entreprise_prog_sum)
                    else:
                        calc_seuil_prog_sum = calc_allegement_general_params_prog_sum.ensemble_des_entreprises.plafond
                        calc_petite_entreprise_prog_sum = (calc_effectif_entreprise_prog_sum < 50)
                        calc_tx_max_prog_sum = (
                            calc_allegement_general_params_prog_sum.ensemble_des_entreprises.entreprises_de_50_salaries_et_plus * not_(calc_petite_entreprise_prog_sum)
                            + calc_allegement_general_params_prog_sum.ensemble_des_entreprises.entreprises_de_moins_de_50_salaries * calc_petite_entreprise_prog_sum)
                    computed_value_for_this_call_prog_sum = 0.0
                    if calc_seuil_prog_sum <= 1:
                        computed_value_for_this_call_prog_sum = 0.0
                    else:
                        calc_ratio_smic_salaire_prog_sum = calc_smic_proratise_prog_sum / (calc_assiette_prog_sum + 1e-16)
                        calc_taux_allegement_general_prog_sum = round_(calc_tx_max_prog_sum * min_(1, max_(calc_seuil_prog_sum * calc_ratio_smic_salaire_prog_sum - 1, 0) / (calc_seuil_prog_sum - 1)), 4)
                        computed_value_for_this_call_prog_sum = calc_taux_allegement_general_prog_sum * calc_assiette_prog_sum
                    sum_val_prog_sum += computed_value_for_this_call_prog_sum
                allegement_progressif_value = sum_val_prog_sum - cumul_progressif

        allegement = (
            (recouvrement_fin_annee * allegement_annuel_value)
            + (recouvrement_anticipe * allegement_anticipe_value)
            + (recouvrement_progressif * allegement_progressif_value)
            )

        return allegement * not_(stagiaire) * not_(apprenti) * non_cumulee

        return allegement * not_(stagiaire) * not_(apprenti) * non_cumulee

class allegement_cotisation_allocations_familiales(Variable):
    value_type = float
    label = "Allègement des cotisations d'allocations familiales sur les bas et moyens salaires"
    entity = Individu
    reference = 'https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/la-cotisation-dallocations-famil/la-reduction-du-taux-de-la-cotis.html'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_01_01(individu, period, parameters):
        allegement_cotisation_allocations_familiales_base = individu('allegement_cotisation_allocations_familiales_base', period)
        # Si l'employeur fait le choix de la TO-DE alors celle-ci remplace l'allègement de cotisation des allocations familiales.
        choix_exoneration_cotisations_employeur_agricole = individu('choix_exoneration_cotisations_employeur_agricole', period)
        return allegement_cotisation_allocations_familiales_base * not_(choix_exoneration_cotisations_employeur_agricole)


class allegement_cotisation_allocations_familiales_base(Variable):
    value_type = float
    label = "Allègement des cotisations d'allocations familiales sur les bas et moyens salaires"
    entity = Individu
    reference = 'https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/la-cotisation-dallocations-famil/la-reduction-du-taux-de-la-cotis.html'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_01_01(individu, period, parameters):
        stagiaire = individu('stagiaire', period)
        apprenti = individu('apprenti', period)
        allegement_mode_recouvrement =\
            individu('allegement_cotisation_allocations_familiales_mode_recouvrement', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)

        non_cumulee = not_(exoneration_cotisations_employeur_jei)

        # Fully inlined logic for allegement_cotisation_allocations_familiales_base
        TypesAllegementModeRecouvrement = allegement_mode_recouvrement.possible_values
        recouvrement_fin_annee = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
        recouvrement_anticipe = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
        recouvrement_progressif = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

        allegement_annuel_value = 0.0
        if recouvrement_fin_annee:
            if period.start.month == 12:
                sum_val_annuel_caf = 0.0
                for sub_period_ann_caf in period.this_year.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_allocations_familiales_base for annuel
                    calc_assiette_ann_caf = individu('assiette_allegement', sub_period_ann_caf)
                    calc_smic_proratise_ann_caf = individu('smic_proratise', sub_period_ann_caf)
                    calc_law_ann_caf = parameters(sub_period_ann_caf).prelevements_sociaux.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales
                    calc_taux_reduction_ann_caf = calc_law_ann_caf.reduction
                    calc_plafond_reduction_ann_caf = 0.0
                    if sub_period_ann_caf.start.year < 2024:
                        calc_plafond_reduction_ann_caf = calc_law_ann_caf.plafond_smic * calc_smic_proratise_ann_caf
                    else:
                        calc_coefficient_proratisation_ann_caf = individu('coefficient_proratisation', sub_period_ann_caf)
                        calc_parameters_smic_2023_12_ann_caf = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_ann_caf = calc_parameters_smic_2023_12_ann_caf.smic_b_horaire
                        calc_nbh_travail_2023_12_ann_caf = calc_parameters_smic_2023_12_ann_caf.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_ann_caf = calc_coefficient_proratisation_ann_caf * calc_smic_horaire_brut_2023_12_ann_caf * calc_nbh_travail_2023_12_ann_caf
                        calc_plafond_reduction_ann_caf = max_(calc_law_ann_caf.plafond_smic_courant * calc_smic_proratise_ann_caf, calc_law_ann_caf.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ann_caf)
                    computed_value_ann_caf = (calc_assiette_ann_caf < calc_plafond_reduction_ann_caf) * calc_taux_reduction_ann_caf * calc_assiette_ann_caf
                    sum_val_annuel_caf += computed_value_ann_caf
                    # END INLINE
                allegement_annuel_value = sum_val_annuel_caf

        allegement_anticipe_value = 0.0
        if recouvrement_anticipe:
            if period.start.month < 12:
                current_period_ant_direct_caf = period.first_month
                # BEGIN INLINE compute_allegement_cotisation_allocations_familiales_base for anticipe (direct)
                calc_assiette_ant_direct_caf = individu('assiette_allegement', current_period_ant_direct_caf)
                calc_smic_proratise_ant_direct_caf = individu('smic_proratise', current_period_ant_direct_caf)
                calc_law_ant_direct_caf = parameters(current_period_ant_direct_caf).prelevements_sociaux.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales
                calc_taux_reduction_ant_direct_caf = calc_law_ant_direct_caf.reduction
                calc_plafond_reduction_ant_direct_caf = 0.0
                if current_period_ant_direct_caf.start.year < 2024:
                    calc_plafond_reduction_ant_direct_caf = calc_law_ant_direct_caf.plafond_smic * calc_smic_proratise_ant_direct_caf
                else:
                    calc_coefficient_proratisation_ant_direct_caf = individu('coefficient_proratisation', current_period_ant_direct_caf)
                    calc_parameters_smic_2023_12_ant_direct_caf = parameters('2023-12').marche_travail.salaire_minimum.smic
                    calc_smic_horaire_brut_2023_12_ant_direct_caf = calc_parameters_smic_2023_12_ant_direct_caf.smic_b_horaire
                    calc_nbh_travail_2023_12_ant_direct_caf = calc_parameters_smic_2023_12_ant_direct_caf.nb_heures_travail_mensuel
                    calc_smic_proratise_2O23_12_ant_direct_caf = calc_coefficient_proratisation_ant_direct_caf * calc_smic_horaire_brut_2023_12_ant_direct_caf * calc_nbh_travail_2023_12_ant_direct_caf
                    calc_plafond_reduction_ant_direct_caf = max_(calc_law_ant_direct_caf.plafond_smic_courant * calc_smic_proratise_ant_direct_caf, calc_law_ant_direct_caf.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ant_direct_caf)
                allegement_anticipe_value = (calc_assiette_ant_direct_caf < calc_plafond_reduction_ant_direct_caf) * calc_taux_reduction_ant_direct_caf * calc_assiette_ant_direct_caf
                # END INLINE
            elif period.start.month == 12:
                cumul_anticipe_caf = individu('allegement_cotisation_allocations_familiales_base', Period(('month', period.start.offset('first-of', 'year'), 11)), options=[ADD])
                sum_val_ant_sum_caf = 0.0
                for sub_period_ant_sum_caf in period.this_year.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_allocations_familiales_base for anticipe (sum)
                    calc_assiette_ant_sum_caf = individu('assiette_allegement', sub_period_ant_sum_caf)
                    calc_smic_proratise_ant_sum_caf = individu('smic_proratise', sub_period_ant_sum_caf)
                    calc_law_ant_sum_caf = parameters(sub_period_ant_sum_caf).prelevements_sociaux.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales
                    calc_taux_reduction_ant_sum_caf = calc_law_ant_sum_caf.reduction
                    calc_plafond_reduction_ant_sum_caf = 0.0
                    if sub_period_ant_sum_caf.start.year < 2024:
                        calc_plafond_reduction_ant_sum_caf = calc_law_ant_sum_caf.plafond_smic * calc_smic_proratise_ant_sum_caf
                    else:
                        calc_coefficient_proratisation_ant_sum_caf = individu('coefficient_proratisation', sub_period_ant_sum_caf)
                        calc_parameters_smic_2023_12_ant_sum_caf = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_ant_sum_caf = calc_parameters_smic_2023_12_ant_sum_caf.smic_b_horaire
                        calc_nbh_travail_2023_12_ant_sum_caf = calc_parameters_smic_2023_12_ant_sum_caf.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_ant_sum_caf = calc_coefficient_proratisation_ant_sum_caf * calc_smic_horaire_brut_2023_12_ant_sum_caf * calc_nbh_travail_2023_12_ant_sum_caf
                        calc_plafond_reduction_ant_sum_caf = max_(calc_law_ant_sum_caf.plafond_smic_courant * calc_smic_proratise_ant_sum_caf, calc_law_ant_sum_caf.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ant_sum_caf)
                    computed_value_ant_sum_caf = (calc_assiette_ant_sum_caf < calc_plafond_reduction_ant_sum_caf) * calc_taux_reduction_ant_sum_caf * calc_assiette_ant_sum_caf
                    sum_val_ant_sum_caf += computed_value_ant_sum_caf
                    # END INLINE
                allegement_anticipe_value = sum_val_ant_sum_caf - cumul_anticipe_caf

        allegement_progressif_value = 0.0
        if recouvrement_progressif:
            if period.start.month == 1:
                current_period_prog_direct_caf = period.first_month
                # BEGIN INLINE compute_allegement_cotisation_allocations_familiales_base for progressif (direct)
                calc_assiette_prog_direct_caf = individu('assiette_allegement', current_period_prog_direct_caf)
                calc_smic_proratise_prog_direct_caf = individu('smic_proratise', current_period_prog_direct_caf)
                calc_law_prog_direct_caf = parameters(current_period_prog_direct_caf).prelevements_sociaux.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales
                calc_taux_reduction_prog_direct_caf = calc_law_prog_direct_caf.reduction
                calc_plafond_reduction_prog_direct_caf = 0.0
                if current_period_prog_direct_caf.start.year < 2024:
                    calc_plafond_reduction_prog_direct_caf = calc_law_prog_direct_caf.plafond_smic * calc_smic_proratise_prog_direct_caf
                else:
                    calc_coefficient_proratisation_prog_direct_caf = individu('coefficient_proratisation', current_period_prog_direct_caf)
                    calc_parameters_smic_2023_12_prog_direct_caf = parameters('2023-12').marche_travail.salaire_minimum.smic
                    calc_smic_horaire_brut_2023_12_prog_direct_caf = calc_parameters_smic_2023_12_prog_direct_caf.smic_b_horaire
                    calc_nbh_travail_2023_12_prog_direct_caf = calc_parameters_smic_2023_12_prog_direct_caf.nb_heures_travail_mensuel
                    calc_smic_proratise_2O23_12_prog_direct_caf = calc_coefficient_proratisation_prog_direct_caf * calc_smic_horaire_brut_2023_12_prog_direct_caf * calc_nbh_travail_2023_12_prog_direct_caf
                    calc_plafond_reduction_prog_direct_caf = max_(calc_law_prog_direct_caf.plafond_smic_courant * calc_smic_proratise_prog_direct_caf, calc_law_prog_direct_caf.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_prog_direct_caf)
                allegement_progressif_value = (calc_assiette_prog_direct_caf < calc_plafond_reduction_prog_direct_caf) * calc_taux_reduction_prog_direct_caf * calc_assiette_prog_direct_caf
                # END INLINE
            elif period.start.month > 1:
                up_to_this_month_caf = Period(('month', period.start.offset('first-of', 'year'), period.start.month))
                up_to_previous_month_caf = Period(('month', period.start.offset('first-of', 'year'), period.start.month - 1))
                cumul_progressif_caf = individu('allegement_cotisation_allocations_familiales_base', up_to_previous_month_caf, options=[ADD])
                sum_val_prog_sum_caf = 0.0
                for sub_period_prog_sum_caf in up_to_this_month_caf.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_allocations_familiales_base for progressif (sum)
                    calc_assiette_prog_sum_caf = individu('assiette_allegement', sub_period_prog_sum_caf)
                    calc_smic_proratise_prog_sum_caf = individu('smic_proratise', sub_period_prog_sum_caf)
                    calc_law_prog_sum_caf = parameters(sub_period_prog_sum_caf).prelevements_sociaux.reductions_cotisations_sociales.allegement_cotisation_allocations_familiales
                    calc_taux_reduction_prog_sum_caf = calc_law_prog_sum_caf.reduction
                    calc_plafond_reduction_prog_sum_caf = 0.0
                    if sub_period_prog_sum_caf.start.year < 2024:
                        calc_plafond_reduction_prog_sum_caf = calc_law_prog_sum_caf.plafond_smic * calc_smic_proratise_prog_sum_caf
                    else:
                        calc_coefficient_proratisation_prog_sum_caf = individu('coefficient_proratisation', sub_period_prog_sum_caf)
                        calc_parameters_smic_2023_12_prog_sum_caf = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_prog_sum_caf = calc_parameters_smic_2023_12_prog_sum_caf.smic_b_horaire
                        calc_nbh_travail_2023_12_prog_sum_caf = calc_parameters_smic_2023_12_prog_sum_caf.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_prog_sum_caf = calc_coefficient_proratisation_prog_sum_caf * calc_smic_horaire_brut_2023_12_prog_sum_caf * calc_nbh_travail_2023_12_prog_sum_caf
                        calc_plafond_reduction_prog_sum_caf = max_(calc_law_prog_sum_caf.plafond_smic_courant * calc_smic_proratise_prog_sum_caf, calc_law_prog_sum_caf.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_prog_sum_caf)
                    computed_value_prog_sum_caf = (calc_assiette_prog_sum_caf < calc_plafond_reduction_prog_sum_caf) * calc_taux_reduction_prog_sum_caf * calc_assiette_prog_sum_caf
                    sum_val_prog_sum_caf += computed_value_prog_sum_caf
                    # END INLINE
                allegement_progressif_value = sum_val_prog_sum_caf - cumul_progressif_caf

        allegement = (
            (recouvrement_fin_annee * allegement_annuel_value)
            + (recouvrement_anticipe * allegement_anticipe_value)
            + (recouvrement_progressif * allegement_progressif_value)
            )

        return allegement * not_(stagiaire) * not_(apprenti) * non_cumulee

class allegement_cotisation_maladie(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = 'Allègement des cotisations employeur d’assurance maladie sur les bas et moyens salaires (Ex-CICE)'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037947559'

    def formula_2019_01_01(individu, period, parameters):
        allegement_cotisation_maladie_base = individu('allegement_cotisation_maladie_base', period)
        # Si l'employeur fait le choix de la TO-DE alors celle-ci remplace l'allègement de cotisation maladie.
        choix_exoneration_cotisations_employeur_agricole = individu('choix_exoneration_cotisations_employeur_agricole', period)
        return allegement_cotisation_maladie_base * not_(choix_exoneration_cotisations_employeur_agricole)


class allegement_cotisation_maladie_base(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = 'Allègement des cotisations employeur d’assurance maladie sur les bas et moyens salaires (Ex-CICE)'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037947559'

    def formula_2019_01_01(individu, period, parameters):
        # propose 3 modes de paiement possibles
        allegement_mode_recouvrement = individu('allegement_cotisation_maladie_mode_recouvrement', period)

        # Fully inlined logic for allegement_cotisation_maladie_base
        TypesAllegementModeRecouvrement = allegement_mode_recouvrement.possible_values
        recouvrement_fin_annee = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
        recouvrement_anticipe = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
        recouvrement_progressif = (allegement_mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

        allegement_annuel_value = 0.0
        if recouvrement_fin_annee:
            if period.start.month == 12:
                sum_val_annuel_maladie = 0.0
                for sub_period_ann_maladie in period.this_year.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_maladie_base for annuel
                    calc_allegement_mmid_ann_maladie = parameters(sub_period_ann_maladie).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid
                    calc_assiette_allegement_ann_maladie = individu('assiette_allegement', sub_period_ann_maladie)
                    calc_smic_proratise_ann_maladie = individu('smic_proratise', sub_period_ann_maladie)
                    calc_plafond_allegement_mmid_ann_maladie = 0.0
                    if sub_period_ann_maladie.start.year < 2024:
                        calc_plafond_allegement_mmid_ann_maladie = calc_allegement_mmid_ann_maladie.plafond * calc_smic_proratise_ann_maladie
                    else:
                        calc_coefficient_proratisation_ann_maladie = individu('coefficient_proratisation', sub_period_ann_maladie)
                        calc_parameters_smic_2023_12_ann_maladie = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_ann_maladie = calc_parameters_smic_2023_12_ann_maladie.smic_b_horaire
                        calc_nbh_travail_2023_12_ann_maladie = calc_parameters_smic_2023_12_ann_maladie.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_ann_maladie = calc_coefficient_proratisation_ann_maladie * calc_smic_horaire_brut_2023_12_ann_maladie * calc_nbh_travail_2023_12_ann_maladie
                        calc_plafond_allegement_mmid_ann_maladie = max_(calc_allegement_mmid_ann_maladie.plafond_smic_courant * calc_smic_proratise_ann_maladie, calc_allegement_mmid_ann_maladie.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ann_maladie)
                    calc_sous_plafond_ann_maladie = calc_assiette_allegement_ann_maladie <= calc_plafond_allegement_mmid_ann_maladie
                    computed_value_ann_maladie = calc_sous_plafond_ann_maladie * calc_allegement_mmid_ann_maladie.taux * calc_assiette_allegement_ann_maladie
                    sum_val_annuel_maladie += computed_value_ann_maladie
                    # END INLINE
                allegement_annuel_value = sum_val_annuel_maladie

        allegement_anticipe_value = 0.0
        if recouvrement_anticipe:
            if period.start.month < 12:
                current_period_ant_direct_maladie = period.first_month
                # BEGIN INLINE compute_allegement_cotisation_maladie_base for anticipe (direct)
                calc_allegement_mmid_ant_direct_maladie = parameters(current_period_ant_direct_maladie).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid
                calc_assiette_allegement_ant_direct_maladie = individu('assiette_allegement', current_period_ant_direct_maladie)
                calc_smic_proratise_ant_direct_maladie = individu('smic_proratise', current_period_ant_direct_maladie)
                calc_plafond_allegement_mmid_ant_direct_maladie = 0.0
                if current_period_ant_direct_maladie.start.year < 2024:
                    calc_plafond_allegement_mmid_ant_direct_maladie = calc_allegement_mmid_ant_direct_maladie.plafond * calc_smic_proratise_ant_direct_maladie
                else:
                    calc_coefficient_proratisation_ant_direct_maladie = individu('coefficient_proratisation', current_period_ant_direct_maladie)
                    calc_parameters_smic_2023_12_ant_direct_maladie = parameters('2023-12').marche_travail.salaire_minimum.smic
                    calc_smic_horaire_brut_2023_12_ant_direct_maladie = calc_parameters_smic_2023_12_ant_direct_maladie.smic_b_horaire
                    calc_nbh_travail_2023_12_ant_direct_maladie = calc_parameters_smic_2023_12_ant_direct_maladie.nb_heures_travail_mensuel
                    calc_smic_proratise_2O23_12_ant_direct_maladie = calc_coefficient_proratisation_ant_direct_maladie * calc_smic_horaire_brut_2023_12_ant_direct_maladie * calc_nbh_travail_2023_12_ant_direct_maladie
                    calc_plafond_allegement_mmid_ant_direct_maladie = max_(calc_allegement_mmid_ant_direct_maladie.plafond_smic_courant * calc_smic_proratise_ant_direct_maladie, calc_allegement_mmid_ant_direct_maladie.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ant_direct_maladie)
                calc_sous_plafond_ant_direct_maladie = calc_assiette_allegement_ant_direct_maladie <= calc_plafond_allegement_mmid_ant_direct_maladie
                allegement_anticipe_value = calc_sous_plafond_ant_direct_maladie * calc_allegement_mmid_ant_direct_maladie.taux * calc_assiette_allegement_ant_direct_maladie
                # END INLINE
            elif period.start.month == 12:
                cumul_anticipe_maladie = individu('allegement_cotisation_maladie_base', Period(('month', period.start.offset('first-of', 'year'), 11)), options=[ADD])
                sum_val_ant_sum_maladie = 0.0
                for sub_period_ant_sum_maladie in period.this_year.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_maladie_base for anticipe (sum)
                    calc_allegement_mmid_ant_sum_maladie = parameters(sub_period_ant_sum_maladie).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid
                    calc_assiette_allegement_ant_sum_maladie = individu('assiette_allegement', sub_period_ant_sum_maladie)
                    calc_smic_proratise_ant_sum_maladie = individu('smic_proratise', sub_period_ant_sum_maladie)
                    calc_plafond_allegement_mmid_ant_sum_maladie = 0.0
                    if sub_period_ant_sum_maladie.start.year < 2024:
                        calc_plafond_allegement_mmid_ant_sum_maladie = calc_allegement_mmid_ant_sum_maladie.plafond * calc_smic_proratise_ant_sum_maladie
                    else:
                        calc_coefficient_proratisation_ant_sum_maladie = individu('coefficient_proratisation', sub_period_ant_sum_maladie)
                        calc_parameters_smic_2023_12_ant_sum_maladie = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_ant_sum_maladie = calc_parameters_smic_2023_12_ant_sum_maladie.smic_b_horaire
                        calc_nbh_travail_2023_12_ant_sum_maladie = calc_parameters_smic_2023_12_ant_sum_maladie.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_ant_sum_maladie = calc_coefficient_proratisation_ant_sum_maladie * calc_smic_horaire_brut_2023_12_ant_sum_maladie * calc_nbh_travail_2023_12_ant_sum_maladie
                        calc_plafond_allegement_mmid_ant_sum_maladie = max_(calc_allegement_mmid_ant_sum_maladie.plafond_smic_courant * calc_smic_proratise_ant_sum_maladie, calc_allegement_mmid_ant_sum_maladie.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_ant_sum_maladie)
                    calc_sous_plafond_ant_sum_maladie = calc_assiette_allegement_ant_sum_maladie <= calc_plafond_allegement_mmid_ant_sum_maladie
                    computed_value_ant_sum_maladie = calc_sous_plafond_ant_sum_maladie * calc_allegement_mmid_ant_sum_maladie.taux * calc_assiette_allegement_ant_sum_maladie
                    sum_val_ant_sum_maladie += computed_value_ant_sum_maladie
                    # END INLINE
                allegement_anticipe_value = sum_val_ant_sum_maladie - cumul_anticipe_maladie

        allegement_progressif_value = 0.0
        if recouvrement_progressif:
            if period.start.month == 1:
                current_period_prog_direct_maladie = period.first_month
                # BEGIN INLINE compute_allegement_cotisation_maladie_base for progressif (direct)
                calc_allegement_mmid_prog_direct_maladie = parameters(current_period_prog_direct_maladie).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid
                calc_assiette_allegement_prog_direct_maladie = individu('assiette_allegement', current_period_prog_direct_maladie)
                calc_smic_proratise_prog_direct_maladie = individu('smic_proratise', current_period_prog_direct_maladie)
                calc_plafond_allegement_mmid_prog_direct_maladie = 0.0
                if current_period_prog_direct_maladie.start.year < 2024:
                    calc_plafond_allegement_mmid_prog_direct_maladie = calc_allegement_mmid_prog_direct_maladie.plafond * calc_smic_proratise_prog_direct_maladie
                else:
                    calc_coefficient_proratisation_prog_direct_maladie = individu('coefficient_proratisation', current_period_prog_direct_maladie)
                    calc_parameters_smic_2023_12_prog_direct_maladie = parameters('2023-12').marche_travail.salaire_minimum.smic
                    calc_smic_horaire_brut_2023_12_prog_direct_maladie = calc_parameters_smic_2023_12_prog_direct_maladie.smic_b_horaire
                    calc_nbh_travail_2023_12_prog_direct_maladie = calc_parameters_smic_2023_12_prog_direct_maladie.nb_heures_travail_mensuel
                    calc_smic_proratise_2O23_12_prog_direct_maladie = calc_coefficient_proratisation_prog_direct_maladie * calc_smic_horaire_brut_2023_12_prog_direct_maladie * calc_nbh_travail_2023_12_prog_direct_maladie
                    calc_plafond_allegement_mmid_prog_direct_maladie = max_(calc_allegement_mmid_prog_direct_maladie.plafond_smic_courant * calc_smic_proratise_prog_direct_maladie, calc_allegement_mmid_prog_direct_maladie.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_prog_direct_maladie)
                calc_sous_plafond_prog_direct_maladie = calc_assiette_allegement_prog_direct_maladie <= calc_plafond_allegement_mmid_prog_direct_maladie
                allegement_progressif_value = calc_sous_plafond_prog_direct_maladie * calc_allegement_mmid_prog_direct_maladie.taux * calc_assiette_allegement_prog_direct_maladie
                # END INLINE
            elif period.start.month > 1:
                up_to_this_month_maladie = Period(('month', period.start.offset('first-of', 'year'), period.start.month))
                up_to_previous_month_maladie = Period(('month', period.start.offset('first-of', 'year'), period.start.month - 1))
                cumul_progressif_maladie = individu('allegement_cotisation_maladie_base', up_to_previous_month_maladie, options=[ADD])
                sum_val_prog_sum_maladie = 0.0
                for sub_period_prog_sum_maladie in up_to_this_month_maladie.get_subperiods(MONTH):
                    # BEGIN INLINE compute_allegement_cotisation_maladie_base for progressif (sum)
                    calc_allegement_mmid_prog_sum_maladie = parameters(sub_period_prog_sum_maladie).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid
                    calc_assiette_allegement_prog_sum_maladie = individu('assiette_allegement', sub_period_prog_sum_maladie)
                    calc_smic_proratise_prog_sum_maladie = individu('smic_proratise', sub_period_prog_sum_maladie)
                    calc_plafond_allegement_mmid_prog_sum_maladie = 0.0
                    if sub_period_prog_sum_maladie.start.year < 2024:
                        calc_plafond_allegement_mmid_prog_sum_maladie = calc_allegement_mmid_prog_sum_maladie.plafond * calc_smic_proratise_prog_sum_maladie
                    else:
                        calc_coefficient_proratisation_prog_sum_maladie = individu('coefficient_proratisation', sub_period_prog_sum_maladie)
                        calc_parameters_smic_2023_12_prog_sum_maladie = parameters('2023-12').marche_travail.salaire_minimum.smic
                        calc_smic_horaire_brut_2023_12_prog_sum_maladie = calc_parameters_smic_2023_12_prog_sum_maladie.smic_b_horaire
                        calc_nbh_travail_2023_12_prog_sum_maladie = calc_parameters_smic_2023_12_prog_sum_maladie.nb_heures_travail_mensuel
                        calc_smic_proratise_2O23_12_prog_sum_maladie = calc_coefficient_proratisation_prog_sum_maladie * calc_smic_horaire_brut_2023_12_prog_sum_maladie * calc_nbh_travail_2023_12_prog_sum_maladie
                        calc_plafond_allegement_mmid_prog_sum_maladie = max_(calc_allegement_mmid_prog_sum_maladie.plafond_smic_courant * calc_smic_proratise_prog_sum_maladie, calc_allegement_mmid_prog_sum_maladie.plafond_smic_2023_12_31 * calc_smic_proratise_2O23_12_prog_sum_maladie)
                    calc_sous_plafond_prog_sum_maladie = calc_assiette_allegement_prog_sum_maladie <= calc_plafond_allegement_mmid_prog_sum_maladie
                    computed_value_prog_sum_maladie = calc_sous_plafond_prog_sum_maladie * calc_allegement_mmid_prog_sum_maladie.taux * calc_assiette_allegement_prog_sum_maladie
                    sum_val_prog_sum_maladie += computed_value_prog_sum_maladie
                    # END INLINE
                allegement_progressif_value = sum_val_prog_sum_maladie - cumul_progressif_maladie

        allegement = (
            (recouvrement_fin_annee * allegement_annuel_value)
            + (recouvrement_anticipe * allegement_anticipe_value)
            + (recouvrement_progressif * allegement_progressif_value)
            )

        return allegement


def compute_allegement_cotisation_maladie_base(individu, period, parameters):
    '''
        Le calcul de l'allègement de cotisation maladie sur les bas et moyens salaires (Ex-CICE).
    '''
    allegement_mmid = parameters(period).prelevements_sociaux.reductions_cotisations_sociales.alleg_gen.mmid

    assiette_allegement = individu('assiette_allegement', period)
    smic_proratise = individu('smic_proratise', period)
    if period.start.year < 2024:
        plafond_allegement_mmid = allegement_mmid.plafond * smic_proratise
    else:
        coefficient_proratisation = individu('coefficient_proratisation', period)
        parameters_smic_2023_12 = parameters('2023-12').marche_travail.salaire_minimum.smic
        smic_horaire_brut_2023_12 = parameters_smic_2023_12.smic_b_horaire
        nbh_travail_2023_12 = parameters_smic_2023_12.nb_heures_travail_mensuel
        smic_proratise_2O23_12 = coefficient_proratisation * smic_horaire_brut_2023_12 * nbh_travail_2023_12
        plafond_allegement_mmid = max_(allegement_mmid.plafond_smic_courant * smic_proratise, allegement_mmid.plafond_smic_2023_12_31 * smic_proratise_2O23_12)

    sous_plafond = assiette_allegement <= plafond_allegement_mmid
    return sous_plafond * allegement_mmid.taux * assiette_allegement


###############################
#  Helper functions and classes
###############################


def switch_on_allegement_mode(individu, period, parameters, mode_recouvrement, variable_name):
    '''
        Switch on 3 possible payment options for allegements

        Name of the computation method specific to the allegement
        should precisely be the variable name prefixed with 'compute_'
    '''
    compute_function = globals()['compute_' + variable_name]
    TypesAllegementModeRecouvrement = mode_recouvrement.possible_values
    recouvrement_fin_annee = (mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
    recouvrement_anticipe = (mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
    recouvrement_progressif = (mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

    return (
        (recouvrement_fin_annee * compute_allegement_annuel(individu, period, parameters, variable_name, compute_function))
        + (recouvrement_anticipe * compute_allegement_anticipe(individu, period, parameters, variable_name, compute_function))
        + (recouvrement_progressif * compute_allegement_progressif(individu, period, parameters, variable_name, compute_function))
        )


def compute_allegement_annuel(individu, period, parameters, variable_name, compute_function):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return sum(
            compute_function(individu, sub_period, parameters)
            for sub_period in period.this_year.get_subperiods(MONTH)
            )


def compute_allegement_anticipe(individu, period, parameters, variable_name, compute_function):
    if period.start.month < 12:
        return compute_function(individu, period.first_month, parameters)
    if period.start.month == 12:
        cumul = individu(
            variable_name,
            Period(('month', period.start.offset('first-of', 'year'), 11)), options = [ADD])
        return sum(
            compute_function(individu, sub_period, parameters)
            for sub_period in period.this_year.get_subperiods(MONTH)
            ) - cumul


def compute_allegement_progressif(individu, period, parameters, variable_name, compute_function):
    if period.start.month == 1:
        return compute_function(individu, period.first_month, parameters)

    if period.start.month > 1:
        up_to_this_month = Period(('month', period.start.offset('first-of', 'year'), period.start.month))
        up_to_previous_month = Period(('month', period.start.offset('first-of', 'year'), period.start.month - 1))
        cumul = individu(variable_name, up_to_previous_month, options = [ADD])
        return sum(
            compute_function(individu, sub_period, parameters)
            for sub_period in up_to_this_month.get_subperiods(MONTH)
            ) - cumul


def taux_exo_cice(assiette_allegement, smic_proratise, cice):
    taux_cice = ((assiette_allegement / (smic_proratise + 1e-16)) <= cice.plafond_smic) * cice.taux
    return taux_cice
