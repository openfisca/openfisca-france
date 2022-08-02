from openfisca_france.model.base import Variable, Famille, MONTH, not_, max_, set_input_divide_by_period


class covid_aide_exceptionnelle_famille_montant(Variable):
    entity = Famille
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les familles pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2020-10-31'
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042574431'

    def formula_2020_05(famille, period, parameters):

        montants = parameters(period).prestations_sociales.solidarite_insertion.autre_solidarite.covid19.aide_exceptionnelle_famille
        rsa = famille('rsa', period) > 0
        ass = famille.sum(famille.members('ass', period)) > 0
        al = famille('aide_logement', period) > 0
        af_nbenf = famille('af_nbenf', period)
        aer = famille.sum(famille.members('aer', period)) > 0
        prim_forf = famille.sum(famille.members('prime_forfaitaire_mensuelle_reprise_activite', period)) > 0
        age_i = famille.members('age', period)
        etudiant_i = famille.members('etudiant', period)
        moins_de_25_ans_non_etudiant = famille.any((age_i <= 24) * (etudiant_i == 0), role = Famille.PARENT)
        base_jeune = moins_de_25_ans_non_etudiant * al
        base = (rsa + ass + aer + prim_forf)
        montant = (
            base_jeune * (montants.base_jeune + montants.par_enfant * af_nbenf)
            + base * not_(base_jeune) * (montants.base + montants.par_enfant * af_nbenf)
            + not_(base) * not_(base_jeune) * al * af_nbenf * montants.par_enfant
            )

        period_1 = period.offset(-1, 'month')
        rsa_n_1 = famille('rsa', period_1) > 0
        ass_n_1 = famille.sum(famille.members('ass', period_1)) > 0
        al_n_1 = famille('aide_logement', period_1) > 0
        af_nbenf_n_1 = famille('af_nbenf', period_1) > 0
        aer_n_1 = famille.sum(famille.members('aer', period_1)) > 0
        prim_forf_n_1 = famille.sum(famille.members('prime_forfaitaire_mensuelle_reprise_activite', period_1)) > 0
        age_i_n_1 = famille.members('age', period_1)
        etudiant_i_n_1 = famille.members('etudiant', period_1)
        moins_de_25_ans_non_etudiant_n_1 = famille.any((age_i_n_1 <= 24) * (etudiant_i_n_1 == 0), role = Famille.PARENT)
        base_jeune_n_1 = moins_de_25_ans_non_etudiant_n_1 * al_n_1
        base_n_1 = (rsa_n_1 + ass_n_1 + aer_n_1 + prim_forf_n_1)
        montant_n_1 = (
            base_jeune_n_1 * (montants.base_jeune + montants.par_enfant * af_nbenf_n_1)
            + base_n_1 * not_(base_jeune_n_1) * (montants.base + montants.par_enfant * af_nbenf_n_1)
            + not_(base_n_1) * not_(base_jeune_n_1) * al_n_1 * af_nbenf_n_1 * montants.par_enfant
            )

        return max_(montant, montant_n_1)
