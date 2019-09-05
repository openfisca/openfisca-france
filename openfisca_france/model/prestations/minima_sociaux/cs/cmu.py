from datetime import date
from numpy import (
    select,
    where,
    logical_not as not_,
    logical_or as or_,
    minimum as min_,
    maximum as max_,
    round as round_,
    )
from openfisca_france.model.base import (
    Variable,
    Famille,
    MONTH,
    )


class cmu_forfait_logement_base(Variable):
    value_type = float
    entity = Famille
    label = "Forfait logement applicable en cas de propriété ou d'occupation à titre gratuit"
    definition_period = MONTH

    def formula(famille, period, parameters):
        cmu_nbp_foyer = famille('cmu_nbp_foyer', period)
        P = parameters(period).cs.cmu.forfait_logement
        law_rsa = parameters(period).prestations.minima_sociaux.rmi

        return forfait_logement(cmu_nbp_foyer, P, law_rsa)


class cmu_forfait_logement_al(Variable):
    value_type = float
    entity = Famille
    label = "Forfait logement applicable en cas d'aide au logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        nb_personnes_foyer = famille('cmu_nbp_foyer', period)
        aide_logement = famille('aide_logement', period)
        P = parameters(period).cs.cmu.forfait_logement_al
        law_rsa = parameters(period).prestations.minima_sociaux.rmi

        return (aide_logement > 0) * min_(12 * aide_logement, forfait_logement(nb_personnes_foyer, P, law_rsa))


class cmu_nbp_foyer(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = "Nombre de personnes dans le foyer CMU-C"
    definition_period = MONTH

    def formula(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        cmu_nb_pac = famille('cmu_nb_pac', period)

        return nb_parents + cmu_nb_pac


class cmu_nb_pac(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = "Nombre de personnes à charge au titre de la CMU-C"
    definition_period = MONTH

    def formula(famille, period, parameters):
        P = parameters(period).cs.cmu
        age = famille.members('age', period)
        return famille.sum((age >= 0) * (age <= P.age_limite_pac), role = Famille.ENFANT)


class cmu_c_plafond(Variable):
    value_type = float
    entity = Famille
    label = "Plafond annuel de ressources pour l'éligibilité à la CMU-C"
    definition_period = MONTH
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006753234"

    def formula(famille, period, parameters):
        """
        - Le plafond dépends du nombre de personnes dans le foyer.
        - À un plafond de base pour une personne, on applique pour chaque personne supplémentaire un certain coefficient supplémentaire
                - Un coefficient pour la 2eme personne,
                - Un coefficient pour les 3e et 4e personne,
                - Un coefficient pour toute personne supplémentaire
        - Si un enfant est en garde alternée, on ne prend en compte que la moitié de son coefficient.
        - Pour savoir quel coefficient est attribué à chaque enfant, il faut trier les enfants de chaque famille par age.
        """

        cmu = parameters(period).cs.cmu
        age_i = famille.members('age_en_mois', period)
        is_couple = (famille('nb_parents', period) == 2)
        is_enfant = famille.members.has_role(Famille.ENFANT)
        cmu_eligible_majoration_dom = famille('cmu_eligible_majoration_dom', period)
        coeff_garde_alt_i = where(famille.members('garde_alternee', period), 0.5, 1)

        # 0 pour l'aîné, 1 pour le cadet, etc.
        rang_dans_fratrie = famille.members.get_rank(famille, - age_i, condition = is_enfant)

        # Famille monoparentale

        coeff_enfant_i = select(
            [rang_dans_fratrie == 0, rang_dans_fratrie <= 2, rang_dans_fratrie >= 3],
            [cmu.coeff_p2, cmu.coeff_p3_p4, cmu.coeff_p5_plus]
            ) * coeff_garde_alt_i

        coeff_monoparental = 1 + famille.sum(coeff_enfant_i, role = Famille.ENFANT)

        # Couple

        coeff_enfant_i = select(
            [rang_dans_fratrie <= 1, rang_dans_fratrie >= 2],
            [cmu.coeff_p3_p4, cmu.coeff_p5_plus]
            ) * coeff_garde_alt_i

        coeff_couple = 1 + cmu.coeff_p2 + famille.sum(coeff_enfant_i, role = Famille.ENFANT)

        coefficient_famille = where(is_couple, coeff_couple, coeff_monoparental)
        coefficient_dom = 1 + cmu_eligible_majoration_dom * cmu.majoration_dom

        plafonds = (
            cmu.plafond_base
            * coefficient_dom
            * coefficient_famille
            )

        return round_(plafonds)


class cmu_eligible_majoration_dom(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        menage = famille.demandeur.menage
        residence_guadeloupe = menage('residence_guadeloupe', period)
        residence_martinique = menage('residence_martinique', period)
        residence_guyane = menage('residence_guyane', period)
        residence_reunion = menage('residence_reunion', period)

        return residence_guadeloupe | residence_martinique | residence_guyane | residence_reunion


class cmu_c(Variable):
    value_type = bool
    label = "Éligibilité à la CMU-C"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        cmu_c_plafond = famille('cmu_c_plafond', period)
        cmu_base_ressources = famille('cmu_base_ressources', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        cmu_acs_eligibilite = famille('cmu_acs_eligibilite', period)

        if period.start.date >= date(2016, 1, 1):
            eligibilite_rsa = famille('rsa', period) > 0
        else:
            # Avant 2016, seules les bénéficiaires du RSA socle avait le droit d'office à la CMU.
            rsa_socle = famille('rsa_socle', period)
            rsa_socle_majore = famille('rsa_socle_majore', period)
            rsa_forfait_logement = famille('rsa_forfait_logement', period)
            rsa_base_ressources = famille('rsa_base_ressources', period)
            socle = max_(rsa_socle, rsa_socle_majore)
            rsa = famille('rsa', period)
            eligibilite_rsa = (rsa > 0) * (rsa_base_ressources < socle - rsa_forfait_logement)

        eligibilite_basique = cmu_base_ressources <= cmu_c_plafond

        return (
            cmu_acs_eligibilite
            * not_(residence_mayotte)
            * or_(eligibilite_basique, eligibilite_rsa)
            )

# Helper functions


def forfait_logement(nbp_foyer, P, law_rsa):
    '''
    Calcule le forfait logement en fonction du nombre de personnes dans le "foyer CMU" et d'un jeu de taux
    '''
    montant_rsa_socle = law_rsa.rmi * (
        1
        + law_rsa.txp2 * (nbp_foyer >= 2)
        + law_rsa.txp3 * (nbp_foyer >= 3)
        )

    return 12 * montant_rsa_socle * select(
        [nbp_foyer == 1, nbp_foyer == 2, nbp_foyer > 2],
        [P.taux_1p, P.taux_2p, P.taux_3p_plus]
        )
