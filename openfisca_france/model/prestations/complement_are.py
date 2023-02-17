from numpy import ceil, divide, where, zeros_like

from openfisca_france.model.base import Individu, Variable, MONTH, \
    set_input_divide_by_period, set_input_dispatch_by_period, TypesActivite, \
    round_, max_, min_


class complement_are_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est éligible au Complément ARE car il perçoit un salaire"
    definition_period = MONTH
    reference = [
        'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044345334',
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000041798325/'
        ]
    set_input = set_input_divide_by_period

    def formula(individu, period):
        activite = individu('activite', period)
        reprise_activite = (activite == TypesActivite.actif)

        # le complément ARE prend le pas sur l'ARE lorsqu'un salaire est perçu
        return reprise_activite * individu('salaire_de_base', period) > 0


class complement_are_plafond(Variable):
    value_type = float
    entity = Individu
    label = 'Plafond de ressources pour bénéficiaire du complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period, parameters):
        salaire_journalier_reference = individu('are_salaire_journalier_reference', period)

        # Le gain brut est l'appelation métier utilisée dans le calcul du complément ARE
        # et représente la notion de salaire de reprise d'emploi
        gain_brut = individu('salaire_de_base', period)
        plafond = salaire_journalier_reference * parameters(period).chomage.allocations_assurance_chomage.complement_are.coefficient_plafond_global

        return max_(0, (plafond - gain_brut))


class complement_are_brut(Variable):
    value_type = float
    entity = Individu
    label = "Complément ARE brut pour reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        complement_are_eligibilite = individu('complement_are_eligibilite', period)
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)
        nombre_jours_indemnises = individu('complement_are_nombre_jours_indemnises', period)

        return complement_are_eligibilite * round_(allocation_journaliere * nombre_jours_indemnises, 2)


class complement_are_net(Variable):
    value_type = float
    entity = Individu
    label = 'Montant mensuel du complément ARE net de déductions'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'
    documentation = '''
    Le Complément ARE net perçu permet de conserver une partie de ses allocations chômage
    à la reprise d'activité si le salaire de l'emploi repris est inférieur
    au salaire ayant initialement débloqué les droits au chômage.
    '''

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
        # Le gain brut est l'appelation métier utilisée dans le calcul du complément ARE
        # et représente la notion de salaire de reprise d'emploi
        gain_brut = individu('salaire_de_base', period)

        return round_(gain_brut * parameters(period).chomage.allocations_assurance_chomage.complement_are.taux_remuneration_retenue, 1)


class complement_are_base(Variable):
    value_type = float
    entity = Individu
    label = "Base d'ARE restante après déduction du salaire de reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire'

    def formula(individu, period):
        are_brute_mensuelle = individu('allocation_retour_emploi_montant', period)
        salaire_retenu = individu('complement_are_salaire_retenu', period)

        # une part des revenus mensuels bruts issus de l’activité reprise
        # sont déduits du montant total de l’ARE qui aurait été versé
        # en l’absence de reprise d’activité
        return max_(0, are_brute_mensuelle - salaire_retenu)


class complement_are_nombre_jours_restants(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours restants avant épuisement des droits à l'assurance chômage"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        nombre_jours_restants_fin_droits = individu(
            'complement_are_nombre_jours_restants_fin_droits',
            period.last_month
            )

        return max_(0, nombre_jours_restants_fin_droits)


class complement_are_nombre_jours_restants_fin_droits(Variable):
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
    label = "Nombre de jours d'ARE indemnisés par le Complément ARE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038829574'

    def formula(individu, period):
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)
        nombre_jours_restants = individu('complement_are_nombre_jours_restants', period)

        return where(
            nombre_jours_indemnisables > nombre_jours_restants,
            nombre_jours_restants,
            nombre_jours_indemnisables
            )


class complement_are_deductions(Variable):
    value_type = float
    entity = Individu
    label = 'Charges mensuelles déductives du complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period):
        cotisation_retraite_complementaire = individu('complement_are_cotisation_retraite_complementaire', period)
        csg = individu('complement_are_csg', period)
        crds = individu('complement_are_crds', period)

        return round_(cotisation_retraite_complementaire + csg + crds, 2)


class complement_are_cotisation_retraite_complementaire(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation de retraite complémentaire mensuelle sur le Complément ARE'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/cumul-allocation-salaire',
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'
        ]

    def formula(individu, period):
        cotisation_retraite_complementaire_journaliere = individu('chomage_cotisation_retraite_complementaire_journaliere', period)
        nombre_jours_indemnisables = individu('complement_are_nombre_jours_indemnisables', period)

        return cotisation_retraite_complementaire_journaliere * nombre_jours_indemnisables


class complement_are_csg_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Contribution Sociale Généralisée (CSG) journalière sur le Complément ARE'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations',
        'https://www.unedic.org/sites/default/files/circulaires/PRE-CIRC-Circulaire_n_2021-13_du_19_octobre_2021.pdf'  # seuil d'exonération
        ]

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('assiette_csg_crds_chomage_journaliere', period)  # CRC déduite

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
    label = 'Contribution Sociale Généralisée (CSG) mensuelle sur Complément ARE'
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
    label = 'Contribution au Remboursement de la Dette Sociale (CRDS) journalière sur Complément ARE'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations',
        'https://www.unedic.org/sites/default/files/circulaires/PRE-CIRC-Circulaire_n_2021-13_du_19_octobre_2021.pdf'  # seuil d'exonération
        ]

    def formula(individu, period, parameters):
        allocation_journaliere_brute_are = individu('assiette_csg_crds_chomage_journaliere', period)  # CRC déduite

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
    label = 'Contribution au Remboursement de la Dette Sociale (CRDS) mensuelle sur Complément ARE'
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
