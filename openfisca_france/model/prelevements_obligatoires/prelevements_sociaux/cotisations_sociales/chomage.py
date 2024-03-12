from openfisca_france.model.base import Individu, Variable, MONTH, \
    set_input_dispatch_by_period, round_, where


class chomage_cotisation_retraite_complementaire_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation de retraite complémentaire journalière sur allocation chômage'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period, parameters):
        allocation_retour_emploi_journaliere = individu('allocation_retour_emploi_journaliere', period)
        are_salaire_journalier_reference = individu('are_salaire_journalier_reference', period)

        # le seuil d'exonération de cette cotisation est indexé sur le montant minimum d'ARE
        seuil_exoneration = parameters(period).chomage.allocations_assurance_chomage.alloc_base.montant_minimum.apres_1979.montant_minimum_hors_mayotte

        taux_cotisation = parameters(period).prelevements_sociaux.regimes_complementaires_retraite_secteur_prive.cotisation_retraite_complementaire.chomage.taux
        cotisation_theorique = are_salaire_journalier_reference * taux_cotisation
        allocation_cotisation_deduite = allocation_retour_emploi_journaliere - cotisation_theorique

        return round_(
            where(
                allocation_cotisation_deduite > seuil_exoneration,
                -1 * cotisation_theorique,
                0),
            2)
