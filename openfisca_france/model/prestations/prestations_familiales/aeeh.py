from openfisca_france.model.base import *
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesLieuResidence


class aeeh_niveau_handicap(Variable):
    value_type = int
    entity = Individu
    label = "Catégorie de handicap prise en compte pour l'AEEH"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aeeh(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation de l'enfant handicapé"
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F14809'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2006_01_01(famille, period, parameters):
        '''Allocation d'éducation de l'enfant handicapé.

        Remplace l'allocation d'éducation spéciale (AES) depuis le 1er janvier 2006.
        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.
        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit
        son activité professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        '''
        isole = not_(famille('en_couple', period))
        prestations_familiales = parameters(period).prestations_sociales.prestations_familiales

        base = prestations_familiales.education_presence_parentale.aeeh.base
        complement_d_allocation = prestations_familiales.education_presence_parentale.aeeh.complement_allocation
        majoration = prestations_familiales.education_presence_parentale.aeeh.majoration_parent_isole

        age = famille.members('age', period)
        handicap = famille.members('handicap', period)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)

        # Indicatrice d'isolement pour les indidivus
        isole = famille.project(isole)
        enfant_handicape = handicap * (age < prestations_familiales.education_presence_parentale.aeeh.age_maximum_enfant)
        montant_par_enfant = enfant_handicape * prestations_familiales.bmaf.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation._children['1ere_categorie']
            + (niveau_handicap == 2) * (complement_d_allocation._children['1ere_categorie'] + majoration._children['2e_categorie'] * isole)
            + (niveau_handicap == 3) * (complement_d_allocation._children['2e_categorie'] + majoration._children['3e_categorie'] * isole)
            + (niveau_handicap == 4) * (complement_d_allocation._children['3e_categorie'] + majoration._children['4e_categorie'] * isole)
            + (niveau_handicap == 5) * (complement_d_allocation._children['4e_categorie'] + majoration._children['5e_categorie'] * isole)
            + (niveau_handicap == 6) * majoration._children['6e_categorie'] * isole
            ) + (niveau_handicap == 6) * complement_d_allocation._children['6e_categorie']

        montant_total = famille.sum(montant_par_enfant, role=Famille.ENFANT)

        # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
        # versement des prestations familiales.
        # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
        # complément ni avec la majoration de parent isolé.
        # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
        # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
        # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
        # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumises à la CRDS
        return montant_total


class aes(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation spéciale"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    end = '2005-12-31'

    def formula_2002_04_01(famille, period, parameters):
        janvier = period.this_year.first_month
        # isole = not_(famille('en_couple', janvier))
        prestations_familiales = parameters(period).prestations_sociales.prestations_familiales

        base = prestations_familiales.education_presence_parentale.aes.base
        complement_d_allocation = prestations_familiales.education_presence_parentale.aes.complement_d_allocation
        complement_d_allocation._children['6e_categorie'] = complement_d_allocation._children['6e_categorie']

        age = famille.members('age', janvier)
        handicap = famille.members('handicap', janvier)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)
        # Indicatrice d'isolement pour les indidivus
        # isole = famille.project(isole)

        enfant_handicape = handicap * (age < prestations_familiales.education_presence_parentale.aes.age_maximum_enfant)

        montant_par_enfant = enfant_handicape * prestations_familiales.bmaf.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation._children['1ere_categorie']
            + (niveau_handicap == 2) * complement_d_allocation._children['1ere_categorie']
            )

        montant_total = famille.sum(montant_par_enfant, role = Famille.ENFANT)
        return montant_total


class besoin_educatif_particulier(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant possède une reconnaissance d’un besoin éducatif particulier"
    definition_period = MONTH


class aeeh_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Éligibilité à l'allocation d'éducation de l'enfant handicapé (AEEH)"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006743351/",
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073189/LEGISCTA000006156691/"
        ]
    documentation = """
        L’Allocation d’éducation de l’enfant handicapé (AEEH) est une prestation familiale destinée, sous conditions, aux personnes qui ont à leur charge et à domicile un enfant de moins de 21 ans en situation de handicap.
        L’attribution de cette aide fait l’objet d’une évaluation préalable.

                    """
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2005_12_20(famille, period, parameters):
        age = famille.members('age', period)
        taux_incapacite = famille.members('taux_incapacite', period)
        besoin_educatif_particulier = famille.members('besoin_educatif_particulier', period)

        aeeh_parameters = parameters(period).prestations.prestations_familiales.aeeh
        residence = famille.members.menage('residence', period)

        condition_age = (age < aeeh_parameters.age_maximum_de_l_enfant)
        condition_taux_incapacite = (
            (
                taux_incapacite >= aeeh_parameters.taux_incapacite_maximal.taux_incapacite_maximal
                ) + (
                (
                    taux_incapacite >= aeeh_parameters.taux_incapacite_minimal.taux_incapacite_minimal
                    ) * (
                        taux_incapacite < aeeh_parameters.taux_incapacite_maximal.taux_incapacite_maximal
                        ) * besoin_educatif_particulier
                )
            )

        condition_residence_FR = False if residence == TypesLieuResidence.non_renseigne else True

        return condition_age * condition_taux_incapacite * condition_residence_FR
