from numpy import ceil, divide, where, zeros_like

from openfisca_france.model.base import Individu, Variable, MONTH, \
    set_input_divide_by_period, round_, max_, min_


class complement_are_allocation_journaliere_brute_are(Variable):
    value_type = float
    entity = Individu
    label = 'Allocation journalière brute ARE après déduction de la complémentaire retraite'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'

    def formula(individu, period):
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)
        crc = individu('complement_are_crc_journaliere', period)  # montant négatif

        return allocation_journaliere + crc


class complement_are_plafond(Variable):
    value_type = float
    entity = Individu
    label = 'Plafond de ressources pour bénéficiaire du complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period, parameters):
        salaire_journalier_reference = individu('salaire_journalier_reference_are', period)
        # Le gain brut est l'appelation métier utilisée dans le calcul du complément ARE et représente la notion de salaire de reprise d'emploi
        gain_brut = individu('salaire_de_base', period)

        plafond = salaire_journalier_reference * parameters(period).chomage.complement_are.coefficient_plafond_global

        return max_(0, (plafond - gain_brut))


class complement_are_theorique(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensuel théorique du complément ARE permettant de déterminer le nombre de jours indemnisables'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        degressivite_are = individu('degressivite_are', period)
        plafond = individu('complement_are_plafond', period)
        are_brute_restante = individu('complement_are_are_brute_restante', period)

        return round_(where(degressivite_are, are_brute_restante, min_(plafond, are_brute_restante)))


class complement_are_brut(Variable):
    value_type = float
    entity = Individu
    label = "Montant de complément ARE dû au demandeur d'emploi"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)
        nombre_jours_indemnises = individu('complement_are_nombre_jours_indemnises', period)

        return round_(allocation_journaliere * nombre_jours_indemnises, 2)


class complement_are_net(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensuel du complément ARE net de déductions'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        allocation_mensuelle_due_brute = individu('complement_are_brut', period)
        deductions_montant_mensuel = individu('complement_are_deductions', period)  # montant négatif

        return max_(0, round_(allocation_mensuelle_due_brute + deductions_montant_mensuel, 2))


class complement_are_salaire_retenu(Variable):
    value_type = float
    entity = Individu
    label = "Montant de salaire retenu pour le calcul du complément ARE après déduction d'un taux"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period, parameters):
        # Le gain brut est l'appelation métier utilisée dans le calcul du complément ARE et représente la notion de salaire de reprise d'emploi
        gain_brut = individu('salaire_de_base', period)

        return round_(gain_brut * parameters(period).chomage.complement_are.coefficient_assiette_salaire_reprise, 1)


class complement_are_base(Variable):
    value_type = float
    entity = Individu
    label = "Base d'ARE restante après déduction du salaire de reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        are_brute_mensuelle = individu('allocation_retour_emploi', period)
        salaire_retenu = individu('complement_are_salaire_retenu', period)

        return max_(0, are_brute_mensuelle - salaire_retenu)


class complement_are_nombre_jours_restants(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours restants avant épuisement des droits à l'assurance chômage"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants_fin_periode = individu('complement_are_nombre_jours_restants_fin_periode', period.last_month)

        return max_(0, nombre_jours_restants_fin_periode)


class complement_are_nombre_jours_restants_fin_periode(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE restants avant épuisement des droits à la fin de la période considérée"
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
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574'

    def formula(individu, period):
        allocation_journaliere_taux_plein = individu('allocation_retour_emploi_journaliere_taux_plein', period)
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)
        degressivite_are = individu('degressivite_are', period)
        complement_are_base = individu('complement_are_base', period)

        nombre_jours_indemnisables = where(
            degressivite_are,
            round_(divide(complement_are_base, allocation_journaliere_taux_plein, out=zeros_like(complement_are_base), where=allocation_journaliere_taux_plein > 0)),
            round_(divide(complement_are_base, allocation_journaliere, out=zeros_like(complement_are_base), where=allocation_journaliere_taux_plein > 0))
            )

        return max_(0, nombre_jours_indemnisables)


class complement_are_nombre_jours_indemnises(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours d'ARE indemnisés par le complement ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574'

    def formula(individu, period):
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)
        nombre_jours_restants = individu('complement_are_nombre_jours_restants', period)

        return where(nombre_jours_indemnisables > nombre_jours_restants, nombre_jours_restants, nombre_jours_indemnisables)


class complement_are_depassement_plafond(Variable):
    value_type = bool
    entity = Individu
    label = 'Le plafond de complément ARE est dépassé'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        complement_are_base = individu('complement_are_base', period)
        plafond = individu('complement_are_plafond', period)

        return (complement_are_base == plafond) * (complement_are_base != 0)


class complement_are_deductions(Variable):
    value_type = float
    entity = Individu
    label = 'Somme des charges déductives du complément ARE (CRC, CSG, CRDS)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period):
        crc = individu('complement_are_crc', period)
        csg = individu('complement_are_csg', period)
        crds = individu('complement_are_crds', period)

        return round_(crc + csg + crds, 2)


class complement_are_crc_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Montant de Cotisation de Retraite Complémentaire (CRC)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period, parameters):
        allocation_retour_emploi_journaliere = individu('allocation_retour_emploi_journaliere', period)
        salaire_journalier_reference = individu('salaire_journalier_reference_are', period)

        seuil_exoneration_crc = parameters(period).chomage.allocation_retour_emploi.montant_minimum_hors_mayotte
        # Le seuil d'exonération de CRC est indexé sur le montant minimum d'ARE

        taux_crc = parameters(period).chomage.complement_are.taux_crc
        crc_theorique = salaire_journalier_reference * taux_crc
        allocation_crc_deduite = allocation_retour_emploi_journaliere - crc_theorique

        return round_(
            where(
                allocation_crc_deduite > seuil_exoneration_crc,
                -1 * crc_theorique,
                0),
            2)


class complement_are_crc(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensualisé de la Cotisation de Retraite Complémentaire (CRC) sur le Complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period):
        crc_journaliere = individu('complement_are_crc_journaliere', period)
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return crc_journaliere * nombre_jours_indemnisables


class complement_are_csg_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Montant journalier de la Contribution Sociale Généralisée (CSG) sur le Complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations',
        'https://www.unedic.org/sites/default/files/circulaires/PRE-CIRC-Circulaire_n_2021-13_du_19_octobre_2021.pdf'  # seuil d'exonération
        ]

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)  # CRC déduite

        parametres_prelevements_sociaux = parameters(period).prelevements_sociaux
        parametres_csg_chomage = parametres_prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage

        # abattement d'assiette pour frais sous 4 plafonds _mensuels_ de la sécurité sociale (PSS)
        max_assiette_mensuelle_eligible_abattement = 4 * parametres_prelevements_sociaux.pss.plafond_securite_sociale_mensuel
        complement_are_nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)
        assiette_mensuelle_csg = allocation_journaliere_brute_are * complement_are_nombre_jours_indemnisables

        assiette_mensuelle_csg_abattable = min_(assiette_mensuelle_csg, max_assiette_mensuelle_eligible_abattement)
        assiette_mensuelle_csg_non_abattue = max_(assiette_mensuelle_csg - max_assiette_mensuelle_eligible_abattement, 0)

        abattement_assiette_csg = parametres_csg_chomage.imposable.abattement.rates[0]
        assiette_journaliere_csg = (
            (assiette_mensuelle_csg_abattable * (1 - abattement_assiette_csg)) + assiette_mensuelle_csg_non_abattue
            ) / complement_are_nombre_jours_indemnisables

        # taux plein par défaut : au demandeur d'emploi de suivre une démarche
        # pour la prise en compte du RFR déterminant les taux réduits
        taux_global_csg_chomage = parametres_csg_chomage.taux_global
        csg_theorique = assiette_journaliere_csg * taux_global_csg_chomage

        # la CSG ne doit pas faire baisser le montant net de l'allocation en-dessous du smic brut
        smic_horaire_brut = parameters(period).marche_travail.salaire_minimum.smic.smic_b_horaire
        seuil_journalier_exoneration = ceil(smic_horaire_brut * 35 / 7)
        allocation_csg_deduite = allocation_journaliere_brute_are - csg_theorique

        csg_prelevee = round_(
            where(
                allocation_csg_deduite > seuil_journalier_exoneration,
                -1 * csg_theorique,
                0),
            2)

        return csg_prelevee


class complement_are_csg(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensualisé des Contributions Sociales Généralisées (CSG)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'

    def formula(individu, period):
        csg_journaliere = individu('complement_are_csg_journaliere', period)
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return csg_journaliere * nombre_jours_indemnisables


class complement_are_crds_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Montant des Contributions au Remboursement de la Dette Sociale (CRDS)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations',
        'https://www.unedic.org/sites/default/files/circulaires/PRE-CIRC-Circulaire_n_2021-13_du_19_octobre_2021.pdf'  # seuil d'exonération
        ]

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('complement_are_allocation_journaliere_brute_are', period)  # CRC déduite

        parametres_prelevements_sociaux = parameters(period).prelevements_sociaux

        # abattement d'assiette pour frais sous 4 plafonds _mensuels_ de la sécurité sociale identique CRDS activité
        complement_are_nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)
        assiette_mensuelle_crds = allocation_journaliere_brute_are * complement_are_nombre_jours_indemnisables

        abattement_assiette_mensuelle_crds = (
            parametres_prelevements_sociaux.contributions_sociales.crds.activite.abattement.calc(
                assiette_mensuelle_crds,
                factor = parametres_prelevements_sociaux.pss.plafond_securite_sociale_mensuel
                )
            )
        assiette_journaliere_crds = (assiette_mensuelle_crds - abattement_assiette_mensuelle_crds) / complement_are_nombre_jours_indemnisables

        # taux global par défaut : au demandeur d'emploi de suivre une démarche
        # pour la prise en compte du RFR (exonération potentielle de CRDS)
        taux_global_crds_chomage = parametres_prelevements_sociaux.contributions_sociales.crds.taux_global
        crds_theorique = assiette_journaliere_crds * taux_global_crds_chomage

        # après la CSG, la CRDS ne doit pas faire baisser le montant net de l'allocation en-dessous du smic brut
        smic_horaire_brut = parameters(period).marche_travail.salaire_minimum.smic.smic_b_horaire
        seuil_journalier_exoneration = ceil(smic_horaire_brut * 35 / 7)

        complement_are_csg_journaliere = individu('complement_are_csg_journaliere', period)
        allocation_csg_crds_deduites = allocation_journaliere_brute_are - complement_are_csg_journaliere - crds_theorique

        crds_prelevee = round_(
            where(
                allocation_csg_crds_deduites > seuil_journalier_exoneration,
                -1 * crds_theorique,
                0),
            2)

        return crds_prelevee


class complement_are_crds(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensualisé des Contributions au Remboursement de la Dette Sociale (CRDS)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period):
        crds_journaliere = individu('complement_are_crds_journaliere', period)
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return crds_journaliere * nombre_jours_indemnisables
