import logging

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import (
    montant_csg_crds
    )
log = logging.getLogger(__name__)


class TypesTauxCSGRemplacement(Enum):
    __order__ = 'non_renseigne exonere taux_reduit taux_plein'  # Needed to preserve the enum order in Python 2
    non_renseigne = 'Non renseigné/non pertinent'
    exonere = 'Exonéré'
    taux_reduit = 'Taux réduit'
    taux_plein = 'Taux plein'


class TypesTauxCSGRetraite(Enum):
    __order__ = 'non_renseigne exonere taux_reduit taux_intermediaire taux_plein'  # Needed to preserve the enum order in Python 2
    non_renseigne = 'Non renseigné/non pertinent'
    exonere = 'Exonéré'
    taux_reduit = 'Taux réduit'
    taux_intermediaire = 'Taux intermédiaire'
    taux_plein = 'Taux plein'


def montant_csg_crds_2_taux(base_avec_abattement = None, base_sans_abattement = None, indicatrice_taux_plein = None,
        indicatrice_taux_reduit = None, law_node = None, plafond_securite_sociale = None):
    assert law_node is not None
    assert plafond_securite_sociale is not None
    if base_sans_abattement is None:
        base_sans_abattement = 0
    if base_avec_abattement is None:
        base = base_sans_abattement
    else:
        base = base_avec_abattement - law_node.abattement.calc(
            base_avec_abattement,
            factor = plafond_securite_sociale,
            round_base_decimals = 2,
            ) + base_sans_abattement
    if indicatrice_taux_plein is None and indicatrice_taux_reduit is None:
        return -law_node.taux * base
    else:
        return - (
            law_node.taux_plein * indicatrice_taux_plein
            + law_node.taux_reduit * indicatrice_taux_reduit
            ) * base


def montant_csg_crds_3_taux(base_avec_abattement = None, base_sans_abattement = None, indicatrice_taux_plein = None,
        indicatrice_taux_reduit = None, indicatrice_taux_intermediaire = None, law_node = None, plafond_securite_sociale = None):
    assert law_node is not None
    assert plafond_securite_sociale is not None
    if base_sans_abattement is None:
        base_sans_abattement = 0
    if base_avec_abattement is None:
        base = base_sans_abattement
    else:
        base = base_avec_abattement - law_node.abattement.calc(
            base_avec_abattement,
            factor = plafond_securite_sociale,
            round_base_decimals = 2,
            ) + base_sans_abattement
    if indicatrice_taux_plein is None and indicatrice_taux_reduit is None and indicatrice_taux_intermediaire is None:
        return -law_node.taux * base
    else:
        return - (
            law_node.taux_plein * indicatrice_taux_plein
            + law_node.taux_reduit * indicatrice_taux_reduit
            + law_node.taux_median * indicatrice_taux_intermediaire
            ) * base


# Allocations chômage

class assiette_csg_crds_chomage_journaliere(Variable):
    value_type = float
    entity = Individu
    label = 'Allocation journalière brute ARE après déduction de la complémentaire retraite'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.unedic.org/indemnisation/fiches-thematiques/retenues-sociales-sur-les-allocations'

    def formula(individu, period):
        allocation_journaliere = individu('allocation_retour_emploi_journaliere', period)
        cotisation_retraite_complementaire_journaliere = individu('chomage_cotisation_retraite_complementaire_journaliere', period)  # montant négatif

        return allocation_journaliere + cotisation_retraite_complementaire_journaliere


class csg_deductible_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG déductible sur les allocations chômage'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2015(individu, period, parameters):
        csg_imposable_chomage = individu('csg_imposable_chomage', period)
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        chomage_brut = individu('chomage_brut', period)
        chomage_cotisation_retraite_complementaire_journaliere = individu('chomage_cotisation_retraite_complementaire_journaliere', period)
        assiette_csg_chomage = chomage_brut - chomage_cotisation_retraite_complementaire_journaliere

        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_chomage,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.deductible,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        nbh_travail = parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel

        cho_seuil_exo = (
            parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.min_exo
            * nbh_travail
            * parameters.marche_travail.salaire_minimum.smic.smic_b_horaire
            )

        csg_deductible_chomage = max_(
            - montant_csg
            - max_(cho_seuil_exo - (
                chomage_brut
                + csg_imposable_chomage
                + montant_csg
                ), 0),
            0,
            )

        return - csg_deductible_chomage


class csg_imposable_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG imposable sur les allocations chômage'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2015(individu, period, parameters):
        parameters = parameters(period)

        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )

        chomage_brut = individu('chomage_brut', period)
        chomage_cotisation_retraite_complementaire_journaliere = individu('chomage_cotisation_retraite_complementaire_journaliere', period)
        assiette_csg_chomage = chomage_brut - chomage_cotisation_retraite_complementaire_journaliere

        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_chomage,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.imposable,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        nbh_travail = parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel
        cho_seuil_exo = (
            parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.min_exo
            * nbh_travail
            * parameters.marche_travail.salaire_minimum.smic.smic_b_horaire
            )
        csg_imposable_chomage = max_(- montant_csg - max_(cho_seuil_exo - (chomage_brut + montant_csg), 0), 0)
        return - csg_imposable_chomage


class crds_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CRDS sur les allocations chômage'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2015(individu, period, parameters):
        csg_deductible_chomage = individu('csg_deductible_chomage', period)
        csg_imposable_chomage = individu('csg_imposable_chomage', period)
        parameters = parameters(period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_remplacement = where(
            rfr <= seuil_exoneration,
            TypesTauxCSGRemplacement.exonere,
            where(
                rfr <= seuil_reduction,
                TypesTauxCSGRemplacement.taux_reduit,
                TypesTauxCSGRemplacement.taux_plein,
                )
            )
        smic_h_b = parameters.marche_travail.salaire_minimum.smic.smic_b_horaire
        # salaire_mensuel_reference = chomage_brut / .7
        # heures_mensuelles = min_(salaire_mensuel_reference / smic_h_b, 35 * 52 / 12)
        heures_mensuelles = parameters.marche_travail.salaire_minimum.smic.nb_heures_travail_mensuel

        chomage_brut = individu('chomage_brut', period)
        chomage_cotisation_retraite_complementaire_journaliere = individu('chomage_cotisation_retraite_complementaire_journaliere', period)
        assiette_crds_chomage = chomage_brut - chomage_cotisation_retraite_complementaire_journaliere

        cho_seuil_exo = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.allocations_chomage.min_exo * heures_mensuelles * smic_h_b
        eligible = (
            (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit)
            + (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein)
            )
        montant_crds = montant_csg_crds(
            base_avec_abattement = assiette_crds_chomage,
            law_node = parameters.prelevements_sociaux.contributions_sociales.crds.activite,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ) * eligible
        crds_chomage = max_(
            -montant_crds - max_(
                cho_seuil_exo - (assiette_crds_chomage + csg_imposable_chomage + csg_deductible_chomage + montant_crds), 0
                ), 0
            )
        return -crds_chomage


class chomage_imposable(Variable):
    value_type = float
    unit = 'currency'
    cerfa_field = {
        0: '1AP',
        1: '1BP',
        2: '1CP',
        3: '1DP',
        4: '1EP',
        }
    entity = Individu
    label = 'Allocations chômage imposables'
    set_input = set_input_divide_by_period
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm'
    definition_period = MONTH

    def formula(individu, period):
        chomage_brut = individu('chomage_brut', period)
        csg_deductible_chomage = individu('csg_deductible_chomage', period)

        return chomage_brut + csg_deductible_chomage


class chomage_net(Variable):
    value_type = float
    entity = Individu
    label = 'Allocations chômage nettes'
    set_input = set_input_divide_by_period
    reference = 'http://vosdroits.service-public.fr/particuliers/N549.xhtml'
    definition_period = MONTH

    def formula(individu, period):
        chomage_imposable = individu('chomage_imposable', period)
        csg_imposable_chomage = individu('csg_imposable_chomage', period)
        crds_chomage = individu('crds_chomage', period)

        return chomage_imposable + csg_imposable_chomage + crds_chomage


# Pensions

class csg_deductible_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG déductible sur les pensions de retraite'
    reference = 'https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2019(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        seuil_taux_intermediaire = seuils.seuil_rfr3.seuil_rfr3 + (nbptr - 1) * 2 * seuils.seuil_rfr3.demi_part_suppl_rfr3

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr <= seuil_taux_intermediaire, rfr > seuil_taux_intermediaire],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_intermediaire, TypesTauxCSGRetraite.taux_plein]
            )

        montant_csg = montant_csg_crds_3_taux(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_retraite == TypesTauxCSGRetraite.taux_plein),
            indicatrice_taux_reduit = (taux_csg_retraite == TypesTauxCSGRetraite.taux_reduit),
            indicatrice_taux_intermediaire = (taux_csg_retraite == TypesTauxCSGRetraite.taux_intermediaire),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.deductible,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        return montant_csg

    def formula_2015(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr > seuil_reduction],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_plein]
            )

        montant_csg = montant_csg_crds_2_taux(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_retraite == TypesTauxCSGRetraite.taux_plein),
            indicatrice_taux_reduit = (taux_csg_retraite == TypesTauxCSGRetraite.taux_reduit),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.deductible,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        return montant_csg

    def formula(individu, period, parameters):  # formula_1997_2014 à corriger (cf. commentaire au niveau de la variable)
        retraite_brute = individu('retraite_brute', period)
        parameters = parameters(period)

        montant_csg = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.deductible.taux_plein * retraite_brute
        return - montant_csg


class csg_imposable_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG imposable sur les pensions de retraite'
    reference = 'https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2019(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        seuil_taux_intermediaire = seuils.seuil_rfr3.seuil_rfr3 + (nbptr - 1) * 2 * seuils.seuil_rfr3.demi_part_suppl_rfr3

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr <= seuil_taux_intermediaire, rfr > seuil_taux_intermediaire],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_intermediaire, TypesTauxCSGRetraite.taux_plein]
            )

        montant_csg = montant_csg_crds_3_taux(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_retraite == TypesTauxCSGRetraite.taux_plein),
            indicatrice_taux_reduit = (taux_csg_retraite == TypesTauxCSGRetraite.taux_reduit),
            indicatrice_taux_intermediaire = (taux_csg_retraite == TypesTauxCSGRetraite.taux_intermediaire),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.imposable,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        return montant_csg

    def formula_2015(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr > seuil_reduction],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_plein]
            )

        montant_csg = montant_csg_crds_2_taux(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_retraite == TypesTauxCSGRetraite.taux_plein),
            indicatrice_taux_reduit = (taux_csg_retraite == TypesTauxCSGRetraite.taux_reduit),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.imposable,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            )
        return montant_csg

    def formula(individu, period, parameters):  # formula_1997_2014 à corriger (cf. commentaire au niveau de la variable)
        retraite_brute = individu('retraite_brute', period)
        parameters = parameters(period)

        montant_csg = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.pensions_retraite_invalidite.imposable.taux_plein * retraite_brute
        return - montant_csg


class crds_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CRDS sur les pensions de retraite'
    reference = 'http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # TODO : formule à partir de 2015 seulement. Pour les années d'avant, certaines seuils de RFR sont manquants, ainsi que des informations relatives à des exonérations passées.

    def formula_2019(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2
        seuil_taux_intermediaire = seuils.seuil_rfr3.seuil_rfr3 + (nbptr - 1) * 2 * seuils.seuil_rfr3.demi_part_suppl_rfr3

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr <= seuil_taux_intermediaire, rfr > seuil_taux_intermediaire],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_intermediaire, TypesTauxCSGRetraite.taux_plein]
            )

        montant_crds = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = parameters.prelevements_sociaux.contributions_sociales.crds.retraite,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ) * (taux_csg_retraite != TypesTauxCSGRetraite.exonere)

        return montant_crds

    def formula_2015(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr > seuil_reduction],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_plein]
            )

        montant_crds = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = parameters.prelevements_sociaux.contributions_sociales.crds.retraite,
            plafond_securite_sociale = parameters.prelevements_sociaux.pss.plafond_securite_sociale_mensuel,
            ) * (taux_csg_retraite != TypesTauxCSGRetraite.exonere)
        return montant_crds

    def formula(individu, period, parameters):  # formula_1997_2014 à corriger (cf. commentaire au niveau de la variable)
        retraite_brute = individu('retraite_brute', period)
        parameters = parameters(period)
        taux = parameters.prelevements_sociaux.contributions_sociales.crds.retraite.taux

        return - taux * retraite_brute


class casa(Variable):
    value_type = float
    entity = Individu
    label = "Contribution additionnelle de solidarité et d'autonomie"
    reference = 'http://www.service-public.fr/actualites/002691.html et https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073189/LEGISCTA000042675227/#LEGISCTA000042675234'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_01_01(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils_csg = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils_csg.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils_csg.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils_csg.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils_csg.seuil_rfr2.demi_part_suppl_rfr2
        seuil_taux_intermediaire = seuils_csg.seuil_rfr3.seuil_rfr3 + (nbptr - 1) * 2 * seuils_csg.seuil_rfr3.demi_part_suppl_rfr3

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr <= seuil_taux_intermediaire, rfr > seuil_taux_intermediaire],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_intermediaire, TypesTauxCSGRetraite.taux_plein]
            )
        bareme = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general.casa
        casa = (
            ((taux_csg_retraite == TypesTauxCSGRetraite.taux_plein) + (taux_csg_retraite == TypesTauxCSGRetraite.taux_intermediaire))
            * bareme.pensions_retraite_preretraite_invalidite.calc(retraite_brute)
            )
        return - casa

    def formula_2015_01_01(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period = period.n_2)
        parameters = parameters(period)
        seuils_csg = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils
        seuil_exoneration = seuils_csg.seuil_rfr1.seuil_rfr1 + (nbptr - 1) * 2 * seuils_csg.seuil_rfr1.demi_part_suppl_rfr1
        seuil_reduction = seuils_csg.seuil_rfr2.seuil_rfr2 + (nbptr - 1) * 2 * seuils_csg.seuil_rfr2.demi_part_suppl_rfr2

        taux_csg_retraite = select(
            [rfr <= seuil_exoneration, rfr <= seuil_reduction, rfr > seuil_reduction],
            [TypesTauxCSGRetraite.exonere, TypesTauxCSGRetraite.taux_reduit, TypesTauxCSGRetraite.taux_plein]
            )
        bareme = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general.casa
        casa = (
            (taux_csg_retraite == TypesTauxCSGRetraite.taux_plein)
            * bareme.pensions_retraite_preretraite_invalidite.calc(retraite_brute)
            )
        return - casa

    def formula_2013_04_01(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period)
        ir = individu.foyer_fiscal('irpp', period = period.last_year)
        parameters = parameters(period)
        seuil_exoneration = parameters.prelevements_sociaux.contributions_sociales.csg.remplacement.seuils.seuil_ir

        bareme = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general.casa
        casa = (
            (ir > seuil_exoneration)
            * bareme.pensions_retraite_preretraite_invalidite.calc(retraite_brute)
            )
        return - casa


class retraite_imposable(Variable):
    unit = 'currency'
    value_type = float
    cerfa_field = {
        0: '1AS',
        1: '1BS',
        2: '1CS',
        3: '1DS',
        4: '1ES',
        }
    entity = Individu
    label = 'Retraites au sens strict imposables (rentes à titre onéreux exclues)'
    set_input = set_input_divide_by_period
    reference = 'http://vosdroits.service-public.fr/particuliers/F415.xhtml'
    definition_period = MONTH

    def formula(individu, period):
        retraite_brute = individu('retraite_brute', period)
        csg_deductible_retraite = individu('csg_deductible_retraite', period)

        return retraite_brute + csg_deductible_retraite


class retraite_nette(Variable):
    value_type = float
    entity = Individu
    label = 'Pensions de retraite nettes'
    set_input = set_input_divide_by_period
    reference = 'http://vosdroits.service-public.fr/particuliers/N20166.xhtml'
    definition_period = MONTH

    def formula(individu, period):
        retraite_imposable = individu('retraite_imposable', period)
        casa = individu('casa', period)
        csg_imposable_retraite = individu('csg_imposable_retraite', period)
        crds_retraite = individu('crds_retraite', period)

        return retraite_imposable + csg_imposable_retraite + crds_retraite + casa


class crds_pfam(Variable):
    value_type = float
    entity = Famille
    label = 'CRDS sur les prestations familiales)'
    reference = 'http://www.cleiss.fr/docs/regimes/regime_francea1.html'
    definition_period = YEAR

    def formula(famille, period, parameters):
        af = famille('af', period, options = [ADD])
        cf = famille('cf', period, options = [ADD])
        asf = famille('asf', period, options = [ADD])
        ars = famille('ars', period)
        paje = famille('paje', period, options = [ADD])
        ape = famille('ape', period, options = [ADD])
        apje = famille('apje', period, options = [ADD])
        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux_global

        return -(af + cf + asf + ars + paje + ape + apje) * taux_crds
