from openfisca_france.model.base import *


class asf_elig_enfant(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant pouvant ouvrir droit à l'ASF"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)

        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af

        eligibilite = (
            # Âge compatible avec les prestations familiales
            (age >= af.af_cm.age1)
            * (age < af.af_cm.age3)
            * not_(autonomie_financiere)  # Ne perçoit pas plus de ressources que "55% du Smic" au sens CAF
            )

        return eligibilite


class asf_elig(Variable):
    value_type = bool
    entity = Famille
    label = "Éligibilité à l'ASF"
    reference = ['https://www.aide-sociale.fr/allocation-soutien-familial/']
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        isole = not_(famille('en_couple', period))
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        # Parent isolé et ne résident pas à Mayotte
        return not_(residence_mayotte) * isole


class asf_montant(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "Montant de l'allocation de soutien familial (ASF)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf
        asf = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.asf

        asf_par_enfant = (
            famille.members('asf_elig_enfant', period)
            * bmaf
            * asf.montant_asf.orphelin_assimile_seul_parent
            )

        montant = famille.sum(asf_par_enfant, role = Famille.ENFANT)
        pensions_alimentaires_percues = famille.sum(famille.members('pensions_alimentaires_percues', period))

        return max_(montant - pensions_alimentaires_percues, 0)


class asf(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Allocation de soutien familial (ASF)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        asf = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.asf

        asf_elig = famille('asf_elig', period)
        montant = famille('asf_montant', period)

        return asf_elig * (montant > asf.seuil) * montant


class crds_asf(Variable):
    value_type = float
    entity = Famille
    label = "CRDS sur l'allocation de soutien familial'"
    definition_period = MONTH

    def formula(famille, period, parameters):
        asf = famille('asf', period)

        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux

        return -(asf) * taux_crds


class asf_nette_crds(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Complément familial net de CRDS'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        asf = famille('asf', period)
        crds_asf = famille('crds_asf', period)

        return asf + crds_asf
