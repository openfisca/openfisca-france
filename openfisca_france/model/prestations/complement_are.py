from numpy import where

from calendar import monthrange

from openfisca_france.model.base import Individu, Variable, MONTH, \
    set_input_divide_by_period, set_input_divide_by_period, round_, max_, min_

class remuneration_reprise_emploi_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant du salaire de reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class salaire_journalier_reference_are(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class allocation_journaliere_are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class degressivite_are(Variable):
    value_type = bool
    entity = Individu
    label = "Soumis à la dégressivité"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class allocation_journaliere_are_taux_plein(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière ARE taux plein (en cas de degressivité)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return individu('allocation_journaliere_are',period)

class allocation_mensuelle_brute_are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle brute ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_mois_complement_are = individu('nombre_jours_mois_complement_are', period)
        degressivite_are = individu('degressivite_are', period)
        allocation_journaliere_are_taux_plein = individu('allocation_journaliere_are_taux_plein', period)
        allocation_journaliere_are = individu('allocation_journaliere_are', period)

        return where(degressivite_are, nombre_jours_mois_complement_are * allocation_journaliere_are_taux_plein ,nombre_jours_mois_complement_are * allocation_journaliere_are)

class allocation_journaliere_brute_are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation journalière brute ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_journaliere_are = individu('allocation_journaliere_are', period)
        crc_complement_are = individu('crc_complement_are', period)

        return allocation_journaliere_are - crc_complement_are

class nombre_jours_mois_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours dans le mois à considérer dans les calculs de l'ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        mois_period = period.start.month
        annee_period = period.start.year

        return monthrange(annee_period, mois_period)[1]

class plafond_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Plafond du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        salaire_journalier_reference_are = individu('salaire_journalier_reference_are', period)
        remuneration_reprise_emploi_are = individu('remuneration_reprise_emploi_are', period)

        plafond = salaire_journalier_reference_are * parameters(period).chomage.complement_are.coefficient_plafond_global

        return max_(0, (plafond - remuneration_reprise_emploi_are))

class montant_mensuel_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        degressivite_are = individu('degressivite_are', period)
        plafond_complement_are = individu('plafond_complement_are', period)
        are_brute_restante_complement_are = individu('are_brute_restante_complement_are',period)

        return round_(where(degressivite_are, are_brute_restante_complement_are, min_(plafond_complement_are, are_brute_restante_complement_are)))

class allocation_mensuelle_due_brute_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_journaliere_are = individu('allocation_journaliere_are', period)
        nombre_jours_indemnises_complement_are = individu('nombre_jours_indemnises_complement_are', period)

        return round_(allocation_journaliere_are * nombre_jours_indemnises_complement_are,2)

class allocation_mensuelle_due_brute_apres_deduction_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel du complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_mensuelle_due_brute_complement_are = individu('allocation_mensuelle_due_brute_complement_are', period)
        deductions_montant_mensuel_complement_are = individu('deductions_montant_mensuel_complement_are', period)

        return max_(0, round_(allocation_mensuelle_due_brute_complement_are - deductions_montant_mensuel_complement_are,2))

class salaire_retenu_reprise_activite_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant de salaire retenu pour le calcul du complément ARE après déduction d'un taux"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        remuneration_reprise_emploi_are = individu('remuneration_reprise_emploi_are', period)

        return round_(remuneration_reprise_emploi_are * parameters(period).chomage.complement_are.taux_deduction_unique,1)

class are_brute_restante_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant d'ARE restant après déduction du montant à déduire"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        allocation_mensuelle_brute_are = individu('allocation_mensuelle_brute_are', period)
        salaire_retenu_reprise_activite_complement_are = individu('salaire_retenu_reprise_activite_complement_are', period)

        return max_(0, allocation_mensuelle_brute_are - salaire_retenu_reprise_activite_complement_are)

class nombre_jours_restants_are(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE restants"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants_are_mois_precedent = individu('futurs_nombre_jours_restants_are', period.last_month)

        return max_(0, nombre_jours_restants_are_mois_precedent)

class futurs_nombre_jours_restants_are(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE restants à la fin de la période considérée"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants_are = individu('nombre_jours_restants_are', period)
        nombre_jours_indemnisables_complement_are = individu('nombre_jours_indemnisables_complement_are', period)

        return max_(0, nombre_jours_restants_are - nombre_jours_indemnisables_complement_are)

class nombre_jours_indemnisables_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE indemnisables par le complement ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574?init=true&page=1&query=2019-797&searchField=ALL&tab_selection=all"

    def formula(individu, period):
        allocation_journaliere_are_taux_plein = individu('allocation_journaliere_are_taux_plein', period)
        allocation_journaliere_are = individu('allocation_journaliere_are', period)
        degressivite_are = individu('degressivite_are', period)
        montant_mensuel_complement_are = individu('montant_mensuel_complement_are', period)

        return max_(0, where
                (
                    degressivite_are,
                    round_(montant_mensuel_complement_are / allocation_journaliere_are_taux_plein),
                    round_(montant_mensuel_complement_are / allocation_journaliere_are)
                )
            )

class nombre_jours_indemnises_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE indemnisés par le complement ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574?init=true&page=1&query=2019-797&searchField=ALL&tab_selection=all"

    def formula(individu, period):
        nombre_jours_indemnisables_complement_are = individu('nombre_jours_indemnisables_complement_are', period)
        nombre_jours_restants_are = individu('nombre_jours_restants_are', period)

        return where(nombre_jours_indemnisables_complement_are > nombre_jours_restants_are, nombre_jours_restants_are, nombre_jours_indemnisables_complement_are)

class depassement_plafond_complement_are(Variable):
    value_type = bool
    entity = Individu
    label = "Dépassement du plafond de complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        montant_servi_complement_are = individu('montant_servi_complement_are', period)
        plafond_complement_are = individu('plafond_complement_are', period)

        return (montant_servi_complement_are == plafond_complement_are) * (montant_servi_complement_are != 0)

class deductions_montant_mensuel_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Somme des charges déductives du complément ARE (CRC, CSG, CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        crc_mensuelle_complement_are = individu('crc_mensuelle_complement_are', period)
        csg_mensuelle_complement_are = individu('csg_mensuelle_complement_are', period)
        crds_mensuelle_complement_are = individu('crds_mensuelle_complement_are',period)

        return round_(crc_mensuelle_complement_are + csg_mensuelle_complement_are + crds_mensuelle_complement_are, 2)

class crc_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant de Cotisation de Retraite Complémentaire (CRC)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_are = individu('allocation_journaliere_are', period)
        salaire_journalier_reference_are = individu('salaire_journalier_reference_are', period)
        seuil_exoneration_crc =  parameters(period).chomage.complement_are.seuil_exoneration_crc
        coefficient_crc = parameters(period).chomage.complement_are.coefficient_crc

        return round_(
            where(
                allocation_journaliere_are > seuil_exoneration_crc,
                salaire_journalier_reference_are * coefficient_crc,
                0),
            2)

class crc_mensuelle_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant de Cotisation de Retraite Complémentaire (CRC)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        crc_complement_are = individu('crc_complement_are', period)
        nombre_jours_indemnisables_complement_are = individu('nombre_jours_indemnisables_complement_are', period)

        return round_(crc_complement_are * nombre_jours_indemnisables_complement_are, 2)

class csg_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant des Contributions Sociales Généralisées (CSG)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('allocation_journaliere_brute_are', period)
        csg_montant_retenu = individu('csg_montant_retenu_complement_are', period)
        seuil_exoneration_contributions =  parameters(period).chomage.complement_are.seuil_exoneration_contributions
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_csg = parameters(period).chomage.complement_are.coefficient_csg

        return round_(
                where(
                    csg_montant_retenu >= seuil_exoneration_contributions,
                    allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_csg,
                    0),
                2)

class csg_montant_retenu_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant retenu pour la détermination du seuil d'éxonération de CSG"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('allocation_journaliere_brute_are', period)
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_csg =  parameters(period).chomage.complement_are.coefficient_csg

        return round_(allocation_journaliere_brute_are - (allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_csg), 2)

class csg_mensuelle_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensualisé des Contributions Sociales Généralisées (CSG)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        csg_complement_are = individu('csg_complement_are', period)
        nombre_jours_indemnisables_complement_are = individu('nombre_jours_indemnisables_complement_are', period)

        return round_(csg_complement_are * nombre_jours_indemnisables_complement_are, 2)

class crds_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant des Contributions au Remboursement de la Dette Sociale (CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('allocation_journaliere_brute_are', period)
        crds_montant_retenu = individu('crds_montant_retenu_complement_are', period)
        seuil_exoneration_contributions =  parameters(period).chomage.complement_are.seuil_exoneration_contributions
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_crds =  parameters(period).chomage.complement_are.coefficient_crds

        return round_(
                where(
                    crds_montant_retenu >= seuil_exoneration_contributions,
                    allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_crds,
                    0),
                2)

class crds_montant_retenu_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant retenu pour la détermination du seuil d'exonération de CRDS"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period, parameters):
        csg_montant_retenu = individu('csg_montant_retenu', period)
        allocation_journaliere_brute_are = individu('allocation_journaliere_brute_are', period)
        coefficient_assiette_contributions =  parameters(period).chomage.complement_are.coefficient_assiette_contributions
        coefficient_crds =  parameters(period).chomage.complement_are.coefficient_crds

        return round_(csg_montant_retenu - (allocation_journaliere_brute_are * coefficient_assiette_contributions * coefficient_crds), 2)

class crds_mensuelle_complement_are(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensualisé des Contributions au Remboursement de la Dette Sociale (CRDS)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations"

    def formula(individu, period):
        crds_complement_are = individu('crds_complement_are', period)
        nombre_jours_indemnisables_complement_are = individu('nombre_jours_indemnisables_complement_are', period)

        return round_(crds_complement_are * nombre_jours_indemnisables_complement_are, 2)