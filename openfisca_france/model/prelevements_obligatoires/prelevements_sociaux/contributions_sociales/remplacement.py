import logging

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import (montant_csg_crds)

log = logging.getLogger(__name__)


class TypesTauxCSGRemplacement(Enum):
    __order__ = "non_renseigne exonere taux_reduit taux_plein"  # Needed to preserve the enum order in Python 2
    non_renseigne = "Non renseigné/non pertinent"
    exonere = "Exonéré"
    taux_reduit = "Taux réduit"
    taux_plein = "Taux plein"


class taux_csg_remplacement(Variable):
    default_value = TypesTauxCSGRemplacement.taux_plein
    value_type = Enum
    possible_values = TypesTauxCSGRemplacement
    entity = Individu
    label = "Taux retenu sur la CSG des revenus de remplacment"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2015(individu, period, parameters):
        rfr = individu.foyer_fiscal("rfr", period=period.n_2)
        nbptr = individu.foyer_fiscal("nbptr", period=period.n_2)
        seuils = parameters(period).prelevements_sociaux.contributions_sociales.csg.retraite_invalidite.seuils
        seuil_exoneration = (seuils.seuil_rfr1 + (nbptr - 1) * seuils.rfr2_demi_part_suppl)
        seuil_reduction = seuils.seuil_rfr2 + (nbptr - 1) * seuils.rfr2_demi_part_suppl
        taux_csg_remplacement = where(rfr <= seuil_exoneration, TypesTauxCSGRemplacement.exonere,
            where(rfr <= seuil_reduction, TypesTauxCSGRemplacement.taux_reduit, TypesTauxCSGRemplacement.taux_plein))
        return taux_csg_remplacement


# Allocations chômage


class csg_deductible_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CSG déductible sur les allocations chômage"
    reference = "http://vosdroits.service-public.fr/particuliers/F2329.xhtml"
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_brut = individu("chomage_brut", period)
        csg_imposable_chomage = individu("csg_imposable_chomage", period)
        taux_csg_remplacement = individu("taux_csg_remplacement", period)
        parameters = parameters(period)
        montant_csg = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            indicatrice_taux_plein = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            law_node = parameters.prelevements_sociaux.contributions_sociales.csg.chomage.deductible,
            plafond_securite_sociale = parameters.cotsoc.gen.plafond_securite_sociale)
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = (parameters.prelevements_sociaux.contributions_sociales.csg.chomage.min_exo * nbh_travail * parameters.cotsoc.gen.smic_h_b)
        csg_deductible_chomage = max_(-montant_csg - max_(cho_seuil_exo - (chomage_brut + csg_imposable_chomage + montant_csg), 0), 0)
        return -csg_deductible_chomage


class csg_imposable_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CSG imposable sur les allocations chômage"
    reference = "http://vosdroits.service-public.fr/particuliers/F2329.xhtml"
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_brut = individu("chomage_brut", period)
        parameters = parameters(period)

        montant_csg = montant_csg_crds(
            base_avec_abattement=chomage_brut,
            law_node=parameters.prelevements_sociaux.contributions_sociales.csg.chomage.imposable,
            plafond_securite_sociale=parameters.cotsoc.gen.plafond_securite_sociale)
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = (parameters.prelevements_sociaux.contributions_sociales.csg.chomage.min_exo * nbh_travail * parameters.cotsoc.gen.smic_h_b)
        csg_imposable_chomage = max_(-montant_csg - max_(cho_seuil_exo - (chomage_brut + montant_csg), 0), 0)
        return -csg_imposable_chomage


class crds_chomage(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CRDS sur les allocations chômage"
    reference = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_brut = individu("chomage_brut", period)
        csg_deductible_chomage = individu("csg_deductible_chomage", period)
        csg_imposable_chomage = individu("csg_imposable_chomage", period)
        taux_csg_remplacement = individu("taux_csg_remplacement", period)
        law = parameters(period)
        smic_h_b = law.cotsoc.gen.smic_h_b
        # salaire_mensuel_reference = chomage_brut / .7
        # heures_mensuelles = min_(salaire_mensuel_reference / smic_h_b, 35 * 52 / 12)  # TODO: depuis 2001 mais avant ?
        heures_mensuelles = 35 * 52 / 12
        cho_seuil_exo = (law.prelevements_sociaux.contributions_sociales.csg.chomage.min_exo * heures_mensuelles * smic_h_b)
        eligible = (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit) + (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein)
        montant_crds = (montant_csg_crds(
            base_avec_abattement=chomage_brut,
            law_node=law.prelevements_sociaux.contributions_sociales.crds.activite,
            plafond_securite_sociale=law.cotsoc.gen.plafond_securite_sociale)
            * eligible)
        crds_chomage = max_(-montant_crds - max_(cho_seuil_exo - (chomage_brut + csg_imposable_chomage + csg_deductible_chomage + montant_crds), 0), 0)
        return -crds_chomage


class chomage_imposable(Variable):
    value_type = float
    unit = "currency"
    cerfa_field = {
        0: "1AP",
        1: "1BP",
        2: "1CP",
        3: "1DP",
        4: "1EP"}
    entity = Individu
    label = "Allocations chômage imposables"
    set_input = set_input_divide_by_period
    reference = ("http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm")
    definition_period = MONTH

    def formula(individu, period):
        chomage_brut = individu("chomage_brut", period)
        csg_deductible_chomage = individu("csg_deductible_chomage", period)

        return chomage_brut + csg_deductible_chomage


class chomage_net(Variable):
    value_type = float
    entity = Individu
    label = "Allocations chômage nettes"
    set_input = set_input_divide_by_period
    reference = "http://vosdroits.service-public.fr/particuliers/N549.xhtml"
    definition_period = MONTH

    def formula(individu, period):
        chomage_imposable = individu("chomage_imposable", period)
        csg_imposable_chomage = individu("csg_imposable_chomage", period)
        crds_chomage = individu("crds_chomage", period)

        return chomage_imposable + csg_imposable_chomage + crds_chomage


# Pensions


class csg_deductible_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CSG déductible sur les pensions de retraite"
    reference = "https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"
    definition_period = MONTH

    def formula(individu, period, parameters):
        retraite_brute = individu("retraite_brute", period)
        taux_csg_remplacement = individu("taux_csg_remplacement", period)
        law = parameters(period)

        montant_csg = montant_csg_crds(
            base_sans_abattement=retraite_brute,
            indicatrice_taux_plein=(taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein),
            indicatrice_taux_reduit=(taux_csg_remplacement == TypesTauxCSGRemplacement.taux_reduit),
            law_node=law.prelevements_sociaux.contributions_sociales.csg.retraite_invalidite.deductible,
            plafond_securite_sociale=law.cotsoc.gen.plafond_securite_sociale)
        return montant_csg


class csg_imposable_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CSG imposable sur les pensions de retraite"
    reference = "https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"
    definition_period = MONTH

    def formula(individu, period, parameters):
        retraite_brute = individu("retraite_brute", period)
        law = parameters(period)

        montant_csg = montant_csg_crds(
            base_sans_abattement=retraite_brute,
            law_node=law.prelevements_sociaux.contributions_sociales.csg.retraite_invalidite.imposable,
            plafond_securite_sociale=law.cotsoc.gen.plafond_securite_sociale)
        return montant_csg


class crds_retraite(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = "CRDS sur les pensions de retraite"
    reference = "http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"
    definition_period = MONTH

    def formula(individu, period, parameters):
        retraite_brute = individu("retraite_brute", period)
        taux_csg_remplacement = individu("taux_csg_remplacement", period)
        law = parameters(period)

        montant_crds = (
            montant_csg_crds(
                base_sans_abattement=retraite_brute,
                law_node=law.prelevements_sociaux.contributions_sociales.crds.retraite,
                plafond_securite_sociale=law.cotsoc.gen.plafond_securite_sociale,) * (taux_csg_remplacement == TypesTauxCSGRemplacement.exonere)
            )
        return montant_crds


class casa(Variable):
    value_type = float
    entity = Individu
    label = "Contribution additionnelle de solidarité et d'autonomie"
    reference = "http://www.service-public.fr/actualites/002691.html"
    definition_period = MONTH

    def formula_2013_04_01(individu, period, parameters):
        retraite_brute = individu('retraite_brute', period = period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        cotisations = parameters(period).prelevements_sociaux.cotisations_securite_sociale_regime_general
        casa = (
            (taux_csg_remplacement == TypesTauxCSGRemplacement.taux_plein)
            * cotisations.casa.pensions_retraite_preretraite_invalidite.calc(retraite_brute)
            )
        return - casa
# TODO Mettre à jour la formule pour prendre en compte les seuils d'exonération

class retraite_imposable(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {0: "1AS", 1: "1BS", 2: "1CS", 3: "1DS", 4: "1ES"}
    entity = Individu
    label = "Retraites au sens strict imposables (rentes à titre onéreux exclues)"
    set_input = set_input_divide_by_period
    reference = "http://vosdroits.service-public.fr/particuliers/F415.xhtml"
    definition_period = MONTH

    def formula(individu, period):
        retraite_brute = individu("retraite_brute", period)
        csg_deductible_retraite = individu("csg_deductible_retraite", period)

        return retraite_brute + csg_deductible_retraite


class retraite_nette(Variable):
    value_type = float
    entity = Individu
    label = "Pensions de retraite nettes"
    set_input = set_input_divide_by_period
    reference = "http://vosdroits.service-public.fr/particuliers/N20166.xhtml"
    definition_period = MONTH

    def formula(individu, period):
        retraite_imposable = individu("retraite_imposable", period)
        casa = individu("casa", period)
        csg_imposable_retraite = individu("csg_imposable_retraite", period)
        crds_retraite = individu("crds_retraite", period)

        return retraite_imposable + csg_imposable_retraite + crds_retraite + casa


class crds_pfam(Variable):
    value_type = float
    entity = Famille
    label = "CRDS sur les prestations familiales)"
    reference = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"
    definition_period = YEAR

    def formula(famille, period, parameters):
        af = famille("af", period, options=[ADD])
        cf = famille("cf", period, options=[ADD])
        asf = famille("asf", period, options=[ADD])
        ars = famille("ars", period)
        paje = famille("paje", period, options=[ADD])
        ape = famille("ape", period, options=[ADD])
        apje = famille("apje", period, options=[ADD])
        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux_global

        return -(af + cf + asf + ars + paje + ape + apje) * taux_crds
