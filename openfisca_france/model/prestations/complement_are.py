from numpy import where

from calendar import monthrange

from openfisca_france.model.base import Individu, Variable, MONTH, \
    set_input_divide_by_period, set_input_divide_by_period, round_, max_, min_

class complement_are_gain_brut(Variable):
    value_type = float
    entity = Individu
    label = "Montant du salaire de reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class complement_are_salaire_journalier_reference(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class complement_are_allocation_journaliere(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class complement_are_degressivite_are(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est soumis à la dégressivité de l'ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class complement_are_allocation_journaliere_taux_plein(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière ARE taux plein (en cas de degressivité)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu('complement_are_allocation_journaliere',period)

class complement_are_allocation_mensuelle_brute_are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle brute ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_mois = individu('complement_are_nombre_jours_mois', period)
        degressivite_are = individu('complement_are_degressivite_are', period)
        allocation_journaliere_taux_plein = individu('complement_are_allocation_journaliere_taux_plein', period)
        allocation_journaliere = individu('complement_are_allocation_journaliere', period)

        return where(degressivite_are, nombre_jours_mois * allocation_journaliere_taux_plein ,nombre_jours_mois * allocation_journaliere)

class complement_are_allocation_journaliere_brute_are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière brute ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_journaliere = individu('complement_are_allocation_journaliere', period)
        crc = individu('complement_are_crc', period)

        return allocation_journaliere - crc

class complement_are_nombre_jours_mois(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours dans le mois à considérer dans les calculs de l'ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        mois_period = period.start.month
        annee_period = period.start.year

        return monthrange(annee_period, mois_period)[1]

class complement_are_plafond(Variable):
    value_type = float
    entity = Individu
    label = "Plafond du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        salaire_journalier_reference = individu('complement_are_salaire_journalier_reference', period)
        gain_brut = individu('complement_are_gain_brut', period)

        plafond = salaire_journalier_reference * parameters(period).chomage.complement_are.coefficient_plafond_global

        return max_(0, (plafond - gain_brut))

class complement_are_montant_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        degressivite_are = individu('complement_are_degressivite_are', period)
        plafond = individu('complement_are_plafond', period)
        are_brute_restante = individu('complement_are_are_brute_restante',period)

        return round_(where(degressivite_are, are_brute_restante, min_(plafond, are_brute_restante)))

class complement_are_allocation_mensuelle_due_brute(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_journaliere = individu('complement_are_allocation_journaliere', period)
        nombre_jours_indemnises = individu('complement_are_nombre_jours_indemnises', period)

        return round_(allocation_journaliere * nombre_jours_indemnises, 2)

class complement_are_allocation_mensuelle_due_brute_apres_deductions(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_mensuelle_due_brute = individu('complement_are_allocation_mensuelle_due_brute', period)
        deductions_montant_mensuel = individu('complement_are_deductions_montant_mensuel', period)

        return max_(0, round_(allocation_mensuelle_due_brute - deductions_montant_mensuel, 2))

class complement_are_salaire_retenu_reprise_activite(Variable):
    value_type = float
    entity = Individu
    label = "Montant de salaire retenu pour le calcul du complément ARE après déduction d'un taux"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        gain_brut = individu('complement_are_gain_brut', period)

        return round_(gain_brut * parameters(period).chomage.complement_are.taux_deduction_unique, 1)

class complement_are_are_brute_restante(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'ARE restant après déduction du montant à déduire"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_mensuelle_brute_are = individu('complement_are_allocation_mensuelle_brute_are', period)
        salaire_retenu_reprise_activite = individu('complement_are_salaire_retenu_reprise_activite', period)

        return max_(0, allocation_mensuelle_brute_are - salaire_retenu_reprise_activite)

class complement_are_nombre_jours_restants(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE restants"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants_fin_periode = individu('complement_are_nombre_jours_restants_fin_periode', period.last_month)

        return max_(0, nombre_jours_restants_fin_periode)

class complement_are_nombre_jours_restants_fin_periode(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE restants à la fin de la période considérée"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants = individu('complement_are_nombre_jours_restants', period)
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return max_(0, nombre_jours_restants - nombre_jours_indemnisables)

class complement_are_nombre_jours_indemnisables(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE indemnisables par le complement ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574?init=true&page=1&query=2019-797&searchField=ALL&tab_selection=all"

    def formula(individu, period):
        allocation_journaliere_taux_plein = individu('complement_are_allocation_journaliere_taux_plein', period)
        allocation_journaliere = individu('complement_are_allocation_journaliere', period)
        degressivite_are = individu('complement_are_degressivite_are', period)
        montant_mensuel = individu('complement_are_montant_mensuel', period)

        return max_(0, where
                (
                    degressivite_are,
                    round_(montant_mensuel / allocation_journaliere_taux_plein),
                    round_(montant_mensuel / allocation_journaliere)
                )
            )

class complement_are_nombre_jours_indemnises(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE indemnisés par le complement ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574?init=true&page=1&query=2019-797&searchField=ALL&tab_selection=all"

    def formula(individu, period):
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)
        nombre_jours_restants = individu('complement_are_nombre_jours_restants', period)

        return where(nombre_jours_indemnisables > nombre_jours_restants, nombre_jours_restants, nombre_jours_indemnisables)

class complement_are_depassement_plafond(Variable):
    value_type = bool
    entity = Individu
    label = "Le plafond de complément ARE est dépassé"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        montant_servi = individu('complement_are_montant_servi', period)
        plafond = individu('complement_are_plafond', period)

        return (montant_servi == plafond) * (montant_servi != 0)

class complement_are_deductions_montant_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Somme des charges déductives du complément ARE (CRC, CSG, CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        crc_mensuelle = individu('complement_are_crc_mensuelle', period)
        csg_mensuelle = individu('complement_are_csg_mensuelle', period)
        crds_mensuelle = individu('complement_are_crds_mensuelle',period)

        return round_(crc_mensuelle + csg_mensuelle + crds_mensuelle, 2)

class complement_are_crc(Variable):
    value_type = float
    entity = Individu
    label = "Montant de Cotisation de Retraite Complémentaire (CRC)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere = individu('complement_are_allocation_journaliere', period)
        salaire_journalier_reference = individu('complement_are_salaire_journalier_reference', period)
        seuil_exoneration_crc =  parameters(period).chomage.complement_are.seuil_exoneration_crc
        coefficient_crc = parameters(period).chomage.complement_are.coefficient_crc

        return round_(
            where(
                allocation_journaliere > seuil_exoneration_crc,
                salaire_journalier_reference * coefficient_crc,
                0),
            2)

class complement_are_crc_mensuelle(Variable):
    value_type = float
    entity = Individu
    label = "Montant de Cotisation de Retraite Complémentaire (CRC)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        complement_are_crc = individu('complement_are_crc', period)
        complement_are_nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return round_(complement_are_crc * complement_are_nombre_jours_indemnisables, 2)

class complement_are_csg(Variable):
    value_type = float
    entity = Individu
    label = "Montant des Contributions Sociales Généralisées (CSG)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)
        csg_montant_retenu = individu('complement_are_csg_montant_retenu', period)
        seuil_exoneration_contributions =  parameters(period).chomage.complement_are.seuil_exoneration_contributions
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_csg = parameters(period).chomage.complement_are.coefficient_csg

        return round_(
                where(
                    csg_montant_retenu >= seuil_exoneration_contributions,
                    allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_csg,
                    0),
                2)

class complement_are_csg_montant_retenu(Variable):
    value_type = float
    entity = Individu
    label = "Montant retenu pour la détermination du seuil d'éxonération de CSG"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_csg =  parameters(period).chomage.complement_are.coefficient_csg

        return round_(allocation_journaliere_brute_are - (allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_csg), 2)

class complement_are_csg_mensuelle(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensualisé des Contributions Sociales Généralisées (CSG)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        complement_are_csg = individu('complement_are_csg', period)
        complement_are_nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return round_(complement_are_csg * complement_are_nombre_jours_indemnisables, 2)

class complement_are_crds(Variable):
    value_type = float
    entity = Individu
    label = "Montant des Contributions au Remboursement de la Dette Sociale (CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)
        crds_montant_retenu = individu('complement_are_crds_montant_retenu', period)
        seuil_exoneration_contributions =  parameters(period).chomage.complement_are.seuil_exoneration_contributions
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_crds =  parameters(period).chomage.complement_are.coefficient_crds

        return round_(
                where(
                    crds_montant_retenu >= seuil_exoneration_contributions,
                    allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_crds,
                    0),
                2)

class complement_are_crds_montant_retenu(Variable):
    value_type = float
    entity = Individu
    label = "Montant retenu pour la détermination du seuil d'exonération de CRDS"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        csg_montant_retenu = individu('complement_are_csg_montant_retenu', period)
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_crds =  parameters(period).chomage.complement_are.coefficient_crds

        return round_(csg_montant_retenu - (allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_crds), 2)

class complement_are_crds_mensuelle(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensualisé des Contributions au Remboursement de la Dette Sociale (CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        complement_are_crds = individu('complement_are_crds', period)
        complement_are_nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return round_(complement_are_crds * complement_are_nombre_jours_indemnisables, 2)