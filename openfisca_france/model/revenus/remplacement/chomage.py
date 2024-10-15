from numpy import busday_count, datetime64, timedelta64, where

from openfisca_france.model.base import *


class chomeur_longue_duree(Variable):
    cerfa_field = {
        0: '1AI',
        1: '1BI',
        2: '1CI',
        3: '1DI',
        4: '1EI',
        }
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = YEAR
    end = '2017-12-31'
    # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    value_type = float
    entity = Individu
    label = 'Chômage brut'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(individu, period):
        # pas de cumul des revenus de remplacement :
        # ARE (demandeur d'emploi) vs. complément ARE (reprise d'activité + droits au chômage)
        complement_are_brut = individu('complement_are_brut', period)
        allocation_retour_emploi = individu('allocation_retour_emploi', period)

        return complement_are_brut + allocation_retour_emploi


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités de chômage partiel'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class allocation_retour_emploi(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE) mensuelle brute"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    unit = 'currency'
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/allocation-daide-au-retour-lemploi-are'

    def formula(individu, period):
        # L'ARE comprend de nombreuses conditions d'éligibilité non modélisées ici.
        activite = individu('activite', period)  # demandeur d'emploi inscrit à Pôle emploi
        allocation_retour_emploi_montant = individu('allocation_retour_emploi_montant', period)

        return (activite == TypesActivite.chomeur) * allocation_retour_emploi_montant


class allocation_retour_emploi_montant(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'allocation chômage d'aide au retour à l'emploi (ARE) mensuelle brute"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006178163/',
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'
        ]

    def formula(individu, period):
        # Attention : ARE simplifiée (modélisation suffisante pour le Complément ARE)
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1, 'D')
        nombre_jours_mois = busday_count(
            debut_mois,
            fin_mois,
            weekmask= '1' * 7
            )

        degressivite_are = individu('degressivite_are', period)
        allocation_journaliere_taux_plein = individu('allocation_retour_emploi_journaliere_taux_plein', period)
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)

        return where(
            degressivite_are,
            nombre_jours_mois * allocation_journaliere_taux_plein,
            nombre_jours_mois * allocation_journaliere
            )


class allocation_retour_emploi_journaliere(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE) brute journalière au sens Pôle Emploi"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006178163/'


class allocation_retour_emploi_journaliere_taux_plein(Variable):
    value_type = float
    entity = Individu
    label = 'Allocation journalière ARE brute taux plein'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu('allocation_retour_emploi_journaliere', period)


class allocation_travailleur_independant(Variable):
    value_type = float
    entity = Individu
    label = 'Allocation des travailleurs indépendants (ATI)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.legifrance.gouv.fr/codes/id/LEGISCTA000037388330/'
    documentation = '''
    Indemnisation de Pôle emploi en vigueur à partir du 1er novembre 2019 à destination
    des travailleurs non salariés indépendants contraints de mettre fin à leur activité.
    '''


class are_salaire_journalier_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire journalier de référence (SJR) au sens des allocations chômage'
    definition_period = MONTH
    reference = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043628391'
    set_input = set_input_divide_by_period


class degressivite_are(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est soumis à la dégressivité de l'allocation d'Aide au Retour à l'Emploi (ARE)"
    definition_period = MONTH
    reference = [
        'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044345334',
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000041798325/'
        ]
    set_input = set_input_divide_by_period
