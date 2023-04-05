from openfisca_core.periods import Period

from openfisca_france.model.base import (
    ADD, 
    calculate_output_add, 
    Famille,
    Individu,
    max_, 
    not_, 
    min_, 
    MONTH,
    Reform, 
    set_input_divide_by_period, 
    Variable, 
    TypesActivite, 
    where
    )

from numpy import datetime64


class aah_deconjugalisee(Reform):
    name = 'Double affichage de l\'AAH'

    class aah_base_ressources(Variable):
        value_type = float
        label = 'Base ressources de l\'allocation adulte handicapé'
        entity = Individu
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2022_01_01(individu, period, parameters):
            
            law = parameters(period)
            aah = law.prestations_sociales.prestations_etat_de_sante.invalidite.aah

            en_activite = individu('activite', period) == TypesActivite.actif

            def assiette_conjoint(revenus_conjoint):
                af_nbenf = individu.famille('af_nbenf', period)
                revenus = (1 - law.impot_revenu.calcul_revenus_imposables.tspr.abatpro.taux) * revenus_conjoint
                return max_(revenus - (aah.abattement_conjoint.abattement_forfaitaire.base + aah.abattement_conjoint.abattement_forfaitaire.majoration_pac * af_nbenf), 0)

            def assiette_revenu_activite_demandeur(revenus_demandeur):
                smic_brut_annuel = 12 * law.marche_travail.salaire_minimum.smic.smic_b_horaire * law.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
                tranche1 = min_(aah.travail_ordinaire.tranche_smic * smic_brut_annuel, revenus_demandeur)
                tranche2 = revenus_demandeur - tranche1
                return (1 - aah.travail_ordinaire.abattement_30) * tranche1 + (1 - aah.travail_ordinaire.abattement_sup) * tranche2

                
            def base_ressource_eval_trim():
                three_previous_months = Period(('month', period.first_month.start, 3)).offset(-3)
                base_ressources_activite_milieu_protege = individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
                base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - base_ressources_activite_milieu_protege
                base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + base_ressources_activite_milieu_protege

                base_ressource_demandeur = assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite

                base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.demandeur('aah_base_ressources_hors_activite_eval_trimestrielle', period)
                base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_activite_eval_trimestrielle', period) + individu.famille.conjoint('aah_base_ressources_hors_activite_eval_trimestrielle', period)
                base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

                return base_ressource_demandeur + assiette_conjoint(base_ressource_conjoint)

            def base_ressource_eval_annuelle():
                base_ressource = individu('aah_base_ressources_eval_annuelle', period)

                base_ressource_demandeur_conjoint = individu.famille.demandeur('aah_base_ressources_eval_annuelle', period)
                base_ressource_conjoint_conjoint = individu.famille.conjoint('aah_base_ressources_eval_annuelle', period)
                base_ressource_conjoint = base_ressource_conjoint_conjoint * individu.has_role(Famille.DEMANDEUR) + base_ressource_demandeur_conjoint * individu.has_role(Famille.CONJOINT)

                return assiette_revenu_activite_demandeur(base_ressource) + assiette_conjoint(base_ressource_conjoint)

            return where(
                en_activite,
                base_ressource_eval_trim() / 12,
                base_ressource_eval_annuelle() / 12
                )

        def formula(individu, period, parameters):
            return

    class aah_base_ressources_deconjugalisee(Variable):
        value_type = float
        label = 'Base ressources de l\'allocation adulte handicapé'
        entity = Individu
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2022_01_01(individu, period, parameters):
            law = parameters(period)
            aah = law.prestations_sociales.prestations_etat_de_sante.invalidite.aah

            en_activite = individu('activite', period) == TypesActivite.actif

            def assiette_revenu_activite_demandeur(revenus_demandeur):
                smic_brut_annuel = 12 * law.marche_travail.salaire_minimum.smic.smic_b_horaire * law.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
                total_tranche1 = min_(aah.travail_ordinaire.tranche_smic * smic_brut_annuel, revenus_demandeur)
                total_tranche2 = revenus_demandeur - total_tranche1
                return (1 - aah.travail_ordinaire.abattement_30) * total_tranche1 + (1 - aah.travail_ordinaire.abattement_sup) * total_tranche2

            def base_ressource_eval_trim():
                three_previous_months = Period(('month', period.first_month.start, 3)).offset(-3)
                base_ressources_activite_milieu_protege = individu('aah_base_ressources_activite_milieu_protege', three_previous_months, options = [ADD])
                base_ressource_activite = individu('aah_base_ressources_activite_eval_trimestrielle', period) - base_ressources_activite_milieu_protege
                base_ressource_hors_activite = individu('aah_base_ressources_hors_activite_eval_trimestrielle', period) + base_ressources_activite_milieu_protege

                base_ressource_demandeur = assiette_revenu_activite_demandeur(base_ressource_activite) + base_ressource_hors_activite

                return base_ressource_demandeur

            def base_ressource_eval_annuelle():
                base_ressource = assiette_revenu_activite_demandeur(individu('aah_base_ressources_eval_annuelle', period))

                return base_ressource

            return where(
                en_activite,
                base_ressource_eval_trim() / 12,
                base_ressource_eval_annuelle() / 12
                )

        def formula(individu, period, parameters):
            return

    class aah_base(Variable):
        calculate_output = calculate_output_add
        value_type = float
        label = 'Montant de l\'Allocation adulte handicapé (hors complément) pour un individu, mensualisée'
        entity = Individu
        reference = [
            'Article L821-1 du Code de la sécurité sociale',
            'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=53AFF5AA4010B01F0539052A33180B39.tplgfr35s_1?idArticle=LEGIARTI000033813790&cidTexte=LEGITEXT000006073189&dateTexte=20180412'
            ]
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2022_01_01(individu, period, parameters):
            law = parameters(period).prestations_sociales

            aah_eligible = individu('aah_eligible', period)
            aah_base_ressources = individu('aah_base_ressources', period)
            plaf_ress_aah = individu('aah_plafond_ressources', period)
            # Le montant de l'AAH est plafonné au montant de base.
            montant_max = law.prestations_etat_de_sante.invalidite.aah.montant
            montant_aah = min_(montant_max, max_(0, plaf_ress_aah - aah_base_ressources))

            aah_base_non_cumulable = individu('aah_base_non_cumulable', period)

            return aah_eligible * min_(montant_aah, max_(0, montant_max - aah_base_non_cumulable))
        
        def formula(individu, period, parameters):
            return

    class aah_base_deconjugalisee(Variable):
        calculate_output = calculate_output_add
        value_type = float
        label = 'Montant de l\'Allocation adulte handicapé (hors complément) pour un individu, mensualisée'
        entity = Individu
        reference = [
            'Article L821-1 du Code de la sécurité sociale',
            'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=53AFF5AA4010B01F0539052A33180B39.tplgfr35s_1?idArticle=LEGIARTI000033813790&cidTexte=LEGITEXT000006073189&dateTexte=20180412'
            ]
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2022_01_01(individu, period, parameters):
            law = parameters(period).prestations_sociales

            aah_eligible = individu('aah_eligible', period)
            aah_base_ressources = individu('aah_base_ressources_deconjugalisee', period)
            plaf_ress_aah = individu('aah_plafond_ressources_deconjugalisee', period)
            # Le montant de l'AAH est plafonné au montant de base.
            montant_max = law.prestations_etat_de_sante.invalidite.aah.montant
            montant_aah = min_(montant_max, max_(0, plaf_ress_aah - aah_base_ressources))

            aah_base_non_cumulable = individu('aah_base_non_cumulable', period)

            return aah_eligible * min_(montant_aah, max_(0, montant_max - aah_base_non_cumulable))
        
        def formula(individu, period, parameters):
            return

    class aah_plafond_ressources_deconjugalisee(Variable):
        value_type = float
        label = 'Montant plafond des ressources déconjugalisées pour bénéficier de l\'Allocation adulte handicapé (hors complément)'
        entity = Individu
        reference = [
            'Article D821-2 du Code de la sécurité sociale',
            'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=4B54EC7065520E4812F84677B918A48E.tplgfr28s_2?idArticle=LEGIARTI000019077584&cidTexte=LEGITEXT000006073189&dateTexte=20081218'
            ]
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula(individu, period, parameters):
            law = parameters(period).prestations_sociales

            af_nbenf = individu.famille('af_nbenf', period)
            montant_max = law.prestations_etat_de_sante.invalidite.aah.montant

            return montant_max * (
                1 + (law.prestations_etat_de_sante.invalidite.aah.majoration_plafond.majoration_par_enfant_supplementaire * af_nbenf)
                )

    class aah(Variable):
        calculate_output = calculate_output_add
        value_type = float
        label = 'Allocation adulte handicapé mensualisée'
        reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006754198'
        entity = Individu
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2022_01_01(individu, period, parameters):
            aah_base = individu('aah_base', period)
            aah_parameters = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
            m_2 = datetime64(period.offset(-60, 'day').start)

            aah_date_debut_hospitalisation = individu('aah_date_debut_hospitalisation', period)
            aah_date_debut_incarceration = individu('aah_date_debut_incarceration', period)
            aah_reduction = (aah_date_debut_hospitalisation <= m_2) + (aah_date_debut_incarceration <= m_2)

            return where(aah_reduction, aah_base * aah_parameters.pourcentage_aah.prison_hospitalisation, aah_base)
        
        def formula(individu, period, parameters):
            return

    class aah_deconjugalisee(Variable):
        calculate_output = calculate_output_add
        value_type = float
        label = 'Allocation adulte handicapé mensualisée'
        reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006754198'
        entity = Individu
        definition_period = MONTH
        set_input = set_input_divide_by_period

        def formula_2023_03_01(individu, period, parameters):
            aah_base = individu('aah_base_deconjugalisee', period)
            aah_parameters = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah
            m_2 = datetime64(period.offset(-60, 'day').start)

            aah_date_debut_hospitalisation = individu('aah_date_debut_hospitalisation', period)
            aah_date_debut_incarceration = individu('aah_date_debut_incarceration', period)
            aah_reduction = (aah_date_debut_hospitalisation <= m_2) + (aah_date_debut_incarceration <= m_2)

            return where(aah_reduction, aah_base * aah_parameters.pourcentage_aah.prison_hospitalisation, aah_base)
        
        def formula(individu, period, parameters):
            return

    def apply(self):
        for variable in [self.aah_base_ressources, self.aah_base, self.aah]:
            self.update_variable(variable)
        for variable in [self.aah_base_ressources_deconjugalisee, self.aah_base_deconjugalisee, self.aah_plafond_ressources_deconjugalisee, self.aah_deconjugalisee]:
            self.add_variable(variable)
