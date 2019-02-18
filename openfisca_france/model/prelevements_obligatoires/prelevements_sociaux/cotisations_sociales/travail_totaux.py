# -*- coding: utf-8 -*-

import logging


from openfisca_france.model.base import *


log = logging.getLogger(__name__)


class cotisations_employeur(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales employeur"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        cotisations_employeur_contributives = individu('cotisations_employeur_contributives', period)
        cotisations_employeur_non_contributives = individu(
            'cotisations_employeur_non_contributives', period)
        cotisations_employeur_main_d_oeuvre = individu('cotisations_employeur_main_d_oeuvre', period)

        return (
            cotisations_employeur_contributives
            + cotisations_employeur_non_contributives
            + cotisations_employeur_main_d_oeuvre
            )


class cotisations_employeur_contributives(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales employeur contributives"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        ags = individu('ags', period)
        agff_employeur = individu('agff_employeur', period, options = [ADD])
        agirc_employeur = individu('agirc_employeur', period, options = [ADD])
        agirc_gmp_employeur = individu('agirc_gmp_employeur', period, options = [ADD])
        apec_employeur = individu('apec_employeur', period)
        arrco_employeur = individu('arrco_employeur', period)
        chomage_employeur = individu('chomage_employeur', period)
        cotisation_exceptionnelle_temporaire_employeur = individu(
            'cotisation_exceptionnelle_temporaire_employeur', period)
        fonds_emploi_hospitalier = individu('fonds_emploi_hospitalier', period, options = [ADD])
        ircantec_employeur = individu('ircantec_employeur', period, options = [ADD])
        pension_civile_employeur = individu('pension_civile_employeur', period, options = [ADD])
        rafp_employeur = individu('rafp_employeur', period, options = [ADD])
        vieillesse_deplafonnee_employeur = individu('vieillesse_deplafonnee_employeur', period, options = [ADD])
        vieillesse_plafonnee_employeur = individu('vieillesse_plafonnee_employeur', period, options = [ADD])

        cotisations = (
            # prive
            ags
            + agff_employeur
            + agirc_employeur
            + agirc_gmp_employeur
            + apec_employeur
            + arrco_employeur
            + chomage_employeur
            + cotisation_exceptionnelle_temporaire_employeur
            + vieillesse_deplafonnee_employeur
            + vieillesse_plafonnee_employeur
            # public
            + fonds_emploi_hospitalier
            + ircantec_employeur
            + pension_civile_employeur
            + rafp_employeur
            )

        return cotisations


class cotisations_employeur_non_contributives(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales employeur non-contributives"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        penibilite = individu('penibilite', period, options = [ADD])
        accident_du_travail = individu('accident_du_travail', period, options = [ADD])
        allocations_temporaires_invalidite = individu('allocations_temporaires_invalidite', period, options = [ADD])
        contribution_solidarite_autonomie = individu('contribution_solidarite_autonomie', period)
        famille = individu('famille', period)
        mmid_employeur = individu('mmid_employeur', period, options = [ADD])
        taxe_salaires = individu('taxe_salaires', period, options = [ADD])
        forfait_social = individu('forfait_social', period, options = [ADD])

        cotisations_employeur_non_contributives = (
            allocations_temporaires_invalidite
            + penibilite
            + accident_du_travail
            + contribution_solidarite_autonomie
            + famille
            + mmid_employeur
            + taxe_salaires
            + forfait_social
            )

        return cotisations_employeur_non_contributives


class cotisations_salariales_contributives(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales salariales contributives"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        agff_salarie = individu('agff_salarie', period)
        agirc_salarie = individu('agirc_salarie', period)
        agirc_gmp_salarie = individu('agirc_gmp_salarie', period)
        apec_salarie = individu('apec_salarie', period)
        arrco_salarie = individu('arrco_salarie', period)
        chomage_salarie = individu('chomage_salarie', period)
        cotisation_exceptionnelle_temporaire_salarie = individu('cotisation_exceptionnelle_temporaire_salarie', period)
        ircantec_salarie = individu('ircantec_salarie', period)
        pension_civile_salarie = individu('pension_civile_salarie', period)
        rafp_salarie = individu('rafp_salarie', period)
        vieillesse_deplafonnee_salarie = individu('vieillesse_deplafonnee_salarie', period)
        vieillesse_plafonnee_salarie = individu('vieillesse_plafonnee_salarie', period)

        cotisations_salariales_contributives = (
            # prive
            agff_salarie
            + agirc_salarie
            + agirc_gmp_salarie
            + apec_salarie
            + arrco_salarie
            + chomage_salarie
            + cotisation_exceptionnelle_temporaire_salarie
            + vieillesse_deplafonnee_salarie
            + vieillesse_plafonnee_salarie
            # public
            + ircantec_salarie
            + pension_civile_salarie
            + rafp_salarie
            )

        return cotisations_salariales_contributives


class cotisations_salariales_non_contributives(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales salariales non-contributives"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        contribution_exceptionnelle_solidarite = individu('contribution_exceptionnelle_solidarite', period, options = [ADD])
        mmid_salarie = individu('mmid_salarie', period)

        cotisations_salariales_non_contributives = (
            # prive
            mmid_salarie
            # public
            + contribution_exceptionnelle_solidarite
            )

        return cotisations_salariales_non_contributives


class cotisations_salariales(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales salariales"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        cotisations_salariales_non_contributives = individu(
            'cotisations_salariales_non_contributives', period)
        exoneration_cotisations_salariales_apprenti = individu('exoneration_cotisations_salariales_apprenti', period, options = [ADD])
        exoneration_cotisations_salarie_stagiaire = individu('exoneration_cotisations_salarie_stagiaire', period, options = [ADD])

        return (
            cotisations_salariales_contributives
            + cotisations_salariales_non_contributives
            + exoneration_cotisations_salariales_apprenti
            + exoneration_cotisations_salarie_stagiaire
            )
