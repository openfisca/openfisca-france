import logging

import numpy as np

from openfisca_france.model.base import *

# TODO:
# check hsup everywhere !

# Helpers

from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme

log = logging.getLogger(__name__)

taux_aot_by_depcom = None
taux_smt_by_depcom = None


# Cotisations proprement dites


class conge_individuel_formation_cdd(Variable):
    value_type = float
    entity = Individu
    label = "Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    # TODO: date de début
    def formula(individu, period, parameters):
        contrat_de_travail_duree = individu('contrat_de_travail_duree', period)
        TypesContratDeTravailDuree = contrat_de_travail_duree.possible_values
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)

        conge_individuel_formation = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.formation.conge_individuel_formation
        cotisation = - conge_individuel_formation.cdd * (contrat_de_travail_duree == TypesContratDeTravailDuree.cdd) * assiette_cotisations_sociales
        return cotisation


class redevable_taxe_apprentissage(Variable):
    value_type = bool
    entity = Individu
    label = "Entreprise redevable de la taxe d'apprentissage"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        # L'association a but non lucratif ne paie pas d'IS de droit commun article 206 du Code général des impôts
        # -> pas de taxe d'apprentissage
        association = individu('entreprise_est_association_non_lucrative', period)

        return not_(association)


class contribution_developpement_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = "Contribution additionnelle au développement de l'apprentissage"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = "employeur",
            bareme_name = "apprentissage_contribution_additionnelle",
            variable_name = "contribution_developpement_apprentissage",
            )
        return cotisation * redevable_taxe_apprentissage


class contribution_supplementaire_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = "Contribution supplémentaire à l'apprentissage"
    reference = "https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_01_01(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        ratio_alternants = individu('ratio_alternants', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)
        contribution = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.apprentissage.apprentissage_contribution_supplementaire

        multiplier = (salarie_regime_alsace_moselle * contribution.multiplicateur_alsace_moselle) + (1 - salarie_regime_alsace_moselle)

        taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .05)
        taux_conditionnel = (
            (effectif_entreprise >= 2000) * (ratio_alternants < .01) * contribution.plus_de_2000_moins_de_1pc
            + (effectif_entreprise < 2000) * (ratio_alternants < .01) * contribution.plus_de_250_moins_de_1pc
            + (.01 <= ratio_alternants) * (ratio_alternants < .02) * contribution.plus_de_250_entre_1_et_2pc
            + (.02 <= ratio_alternants) * (ratio_alternants < .03) * contribution.plus_de_250_entre_2_et_3pc
            + (.03 <= ratio_alternants) * (ratio_alternants < .04) * contribution.plus_de_250_entre_3_et_4pc
            + (.04 <= ratio_alternants) * (ratio_alternants < .05) * contribution.plus_de_250_entre_4_et_5pc
            )
        taux_contribution = taxe_due * taux_conditionnel * multiplier
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage

    def formula_2012_01_01(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        ratio_alternants = individu('ratio_alternants', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)
        contribution = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.apprentissage.apprentissage_contribution_supplementaire

        multiplier = (salarie_regime_alsace_moselle * contribution.multiplicateur_alsace_moselle) + (1 - salarie_regime_alsace_moselle)

        taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .04)
        taux_conditionnel = (
            (effectif_entreprise >= 2000) * (ratio_alternants < .01) * contribution.plus_de_2000_moins_de_1pc
            + (effectif_entreprise < 2000) * (ratio_alternants < .01) * contribution.plus_de_250_moins_de_1pc
            + (.01 <= ratio_alternants) * (ratio_alternants < .02) * contribution.plus_de_250_entre_1_et_2pc
            + (.02 <= ratio_alternants) * (ratio_alternants < .03) * contribution.plus_de_250_entre_2_et_3pc
            + (.03 <= ratio_alternants) * (ratio_alternants < .04) * contribution.plus_de_250_entre_3_et_4pc
            )
        taux_contribution = taux_conditionnel * taxe_due * multiplier
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage

    def formula_2011_01_01(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        ratio_alternants = individu('ratio_alternants', period)
        contribution = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.apprentissage.apprentissage_contribution_supplementaire

        taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .04)
        taux_conditionnel = (
            (effectif_entreprise >= 2000) * (ratio_alternants < .01) * contribution.plus_de_2000_moins_de_1pc
            + (effectif_entreprise < 2000) * (ratio_alternants < .01) * contribution.plus_de_250_moins_de_1pc
            + (.01 <= ratio_alternants) * (ratio_alternants < .02) * contribution.plus_de_250_entre_1_et_2pc
            + (.02 <= ratio_alternants) * (ratio_alternants < .03) * contribution.plus_de_250_entre_2_et_3pc
            + (.03 <= ratio_alternants) * (ratio_alternants < .04) * contribution.plus_de_250_entre_3_et_4pc
            )
        taux_contribution = taux_conditionnel * taxe_due
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage

    def formula_2009_01_01(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        ratio_alternants = individu('ratio_alternants', period)
        contribution = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.apprentissage.apprentissage_contribution_supplementaire

        taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .03)
        taux_conditionnel = (
            (ratio_alternants < .01) * contribution.plus_de_250_moins_de_1pc
            + (.01 <= ratio_alternants) * (ratio_alternants < .02) * contribution.plus_de_250_entre_1_et_2pc
            + (.02 <= ratio_alternants) * (ratio_alternants < .03) * contribution.plus_de_250_entre_2_et_3pc
            )
        taux_contribution = taux_conditionnel * taxe_due
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage


class cotisations_employeur_main_d_oeuvre(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation sociales employeur main d'oeuvre"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        conge_individuel_formation_cdd = individu('conge_individuel_formation_cdd', period)
        contribution_developpement_apprentissage = individu(
            'contribution_developpement_apprentissage', period)
        contribution_supplementaire_apprentissage = individu(
            'contribution_supplementaire_apprentissage', period)
        financement_organisations_syndicales = individu('financement_organisations_syndicales', period)
        fnal = individu('fnal', period)
        formation_professionnelle = individu('formation_professionnelle', period)
        participation_effort_construction = individu('participation_effort_construction', period, options = [ADD])
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period, options = [ADD])
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options = [ADD])

        taxe_apprentissage = individu('taxe_apprentissage', period, options = [ADD])
        versement_transport = individu('versement_transport', period, options = [ADD])

        cotisations_employeur_main_d_oeuvre = (
            conge_individuel_formation_cdd
            + contribution_developpement_apprentissage
            + contribution_supplementaire_apprentissage
            + financement_organisations_syndicales
            + fnal
            + formation_professionnelle
            + participation_effort_construction
            + prevoyance_obligatoire_cadre
            + complementaire_sante_employeur
            + taxe_apprentissage
            + versement_transport
            )

        return cotisations_employeur_main_d_oeuvre


class fnal(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation fonds national action logement (FNAL)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        fnal_cotisation = individu('fnal_cotisation', period)
        fnal_contribution = individu('fnal_contribution', period)
        return fnal_cotisation + fnal_contribution


class fnal_cotisation(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation fonds national action logement (FNAL)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2015-01-01'

    def formula(individu, period, parameters):
        return apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_cotisation',
            variable_name = "fnal_cotisation",
            )


class fnal_contribution(Variable):
    value_type = float
    entity = Individu
    label = "Contribution fonds national action logement (FNAL)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2020_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        effectif_plus_de_50_salaries = effectif_entreprise >= 50
        contribution_plus_de_50_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_plus_de_50_salaries',
            variable_name = "fnal_contribution",
            )
        contribution_moins_de_50_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_moins_de_50_salaries',
            variable_name = "fnal_contribution",
            )
        return effectif_plus_de_50_salaries * contribution_plus_de_50_salaries + (1 - effectif_plus_de_50_salaries) * contribution_moins_de_50_salaries

    def formula_2015_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        effectif_plus_de_20_salaries = effectif_entreprise >= 20
        contribution_plus_de_20_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_plus_de_20_salaries',
            variable_name = "fnal_contribution",
            )
        contribution_moins_de_20_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_moins_de_20_salaries',
            variable_name = "fnal_contribution",
            )
        return effectif_plus_de_20_salaries * contribution_plus_de_20_salaries + (1 - effectif_plus_de_20_salaries) * contribution_moins_de_20_salaries

    def formula_2007_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        effectif_plus_de_20_salaries = effectif_entreprise >= 20
        contribution_plus_de_20_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_plus_de_20_salaries',
            variable_name = "fnal_contribution",
            )
        return effectif_plus_de_20_salaries * contribution_plus_de_20_salaries

    def formula(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        effectif_plus_de_10_salaries = effectif_entreprise >= 10
        contribution_plus_de_10_salaries = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal_contribution_plus_de_10_salaries',
            variable_name = "fnal_contribution",
            )
        return effectif_plus_de_10_salaries * contribution_plus_de_10_salaries


class financement_organisations_syndicales(Variable):
    value_type = float
    entity = Individu
    label = "Contribution patronale au financement des organisations syndicales"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_01_01(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'financement_organisations_syndicales',
            variable_name = 'financement_organisations_syndicales',
            )
        contrat_de_droit_prive = (
            + (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )

        return cotisation * contrat_de_droit_prive


class formation_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = "PEFPC - Formation professionnelle"
    reference = "https://www.service-public.fr/professionnels-entreprises/vosdroits/F22570"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2019-01-01'

    def formula_2016_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        cotisation_0_10 = (effectif_entreprise < 11) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_moins_de_11_salaries',
            variable_name = 'formation_professionnelle',
            )

        cotisation_11 = (effectif_entreprise >= 11) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_11_salaries_et_plus',
            variable_name = 'formation_professionnelle',
            )
        return cotisation_0_10 + cotisation_11

    def formula(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        cotisation_0_9 = (effectif_entreprise < 10) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_moins_de_10_salaries',
            variable_name = 'formation_professionnelle',
            )

        cotisation_10_19 = ((effectif_entreprise >= 10) * (effectif_entreprise < 20)) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_entre_10_et_19_salaries',
            variable_name = 'formation_professionnelle',
            )

        cotisation_20 = (effectif_entreprise >= 20) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_20_salaries_et_plus',
            variable_name = 'formation_professionnelle',
            )
        return cotisation_0_9 + cotisation_10_19 + cotisation_20


class participation_effort_construction(Variable):
    value_type = float
    entity = Individu
    label = "Participation à l'effort de construction"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TO DO : integration de la variable peec_employeur : les critères d'éligibilité employeur incluent d'autres dimensions que l'effectif

    def formula_2020_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        bareme = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'construction_plus_de_50_salaries',
            variable_name = 'participation_effort_construction',
            )

        cotisation = bareme * (effectif_entreprise >= 50)

        return cotisation

    def formula_2005_01_01(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        bareme = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'construction_plus_de_20_salaries',
            variable_name = 'participation_effort_construction',
            )

        cotisation = bareme * (effectif_entreprise >= 20)

        return cotisation

    def formula(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        bareme = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'construction_plus_de_10_salaries',
            variable_name = 'participation_effort_construction',
            )

        cotisation = bareme * (effectif_entreprise >= 10)

        return cotisation


class taxe_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = "Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"
    reference = "https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)

        cotisation_regime_alsace_moselle = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage_taxe_alsace_moselle',
            variable_name = 'taxe_apprentissage',
            )

        cotisation_regime_general = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage_taxe',
            variable_name = 'taxe_apprentissage',
            )

        cotisation = np.where(
            salarie_regime_alsace_moselle,
            cotisation_regime_alsace_moselle,
            cotisation_regime_general,
            )

        return cotisation * redevable_taxe_apprentissage


class taxe_salaires(Variable):
    value_type = float
    entity = Individu
    label = "Taxe sur les salaires"
    definition_period = MONTH
    set_input = set_input_divide_by_period
# Voir
# http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8920/fichedescriptiveformulaire_8920.pdf

    def formula(individu, period, parameters):
        assujettie_taxe_salaires = individu('assujettie_taxe_salaires', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period)
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period)
        prise_en_charge_employeur_prevoyance_complementaire = individu(
            'prise_en_charge_employeur_prevoyance_complementaire', period, options = [ADD])

        entreprise_est_association_non_lucrative = individu('entreprise_est_association_non_lucrative', period)
        effectif_entreprise = individu('effectif_entreprise', period)

        # impots.gouv.fr
        # La taxe est due notamment par les : [...] organismes sans but lucratif
        assujettissement = assujettie_taxe_salaires + entreprise_est_association_non_lucrative

        taxe_salaires = parameters(period).prelevements_sociaux.autres_taxes_participations_assises_salaires.taxsal
        bareme = taxe_salaires.taux_maj
        base = assiette_cotisations_sociales + (
            - prevoyance_obligatoire_cadre + prise_en_charge_employeur_prevoyance_complementaire
            - complementaire_sante_employeur
            )

        # TODO: exonérations apprentis
        # TODO: modify if DOM

        cotisation_individuelle = (
            bareme.calc(
                base,
                factor = 1 / 12,
                round_base_decimals = 2
                )
            + round_(taxe_salaires.taux.metro * base, 2)
            )

        # Une franchise et une décôte s'appliquent à cette taxe
        # Etant donné que nous n'avons pas la distribution de salaires de l'entreprise,
        # elles sont estimées en prenant l'effectif de l'entreprise et
        # considérant que l'unique salarié de la individu est la moyenne.
        # http://www.impots.gouv.fr/portal/dgi/public/popup?typePage=cpr02&espId=2&docOid=documentstandard_1845
        estimation = cotisation_individuelle * effectif_entreprise * 12
        conditions = [estimation < taxe_salaires.franchise, estimation <= taxe_salaires.decote_montant, estimation > taxe_salaires.decote_montant]
        results = [0, estimation - (taxe_salaires.decote_montant - estimation) * taxe_salaires.decote_taux, estimation]

        estimation_reduite = np.select(conditions, results)

        # Abattement spécial de taxe sur les salaires
        # Les associations à but non lucratif bénéficient d'un abattement important
        estimation_abattue_negative = estimation_reduite - taxe_salaires.abattement_special
        estimation_abattue = switch(
            entreprise_est_association_non_lucrative,
            {
                0: estimation_reduite,
                1: (estimation_abattue_negative >= 0) * estimation_abattue_negative,
                }
            )

        with np.errstate(invalid='ignore'):
            cotisation = switch(effectif_entreprise == 0, {
                True: individu.filled_array(0),
                False: estimation_abattue / effectif_entreprise / 12
                })

        return - cotisation * assujettissement
