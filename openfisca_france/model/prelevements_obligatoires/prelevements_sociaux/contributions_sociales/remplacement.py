# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import maximum as max_


from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.contributions_sociales.base import (
    montant_csg_crds
    )
log = logging.getLogger(__name__)


class taux_csg_remplacement(Variable):
    column = EnumCol(
        default = 3,
        enum = Enum([
            u"Non renseigné/non pertinent",
            u"Exonéré",
            u"Taux réduit",
            u"Taux plein",
            ]),
        )
    entity = Individu
    label = u"Taux retenu sur la CSG des revenus de remplacment"


############################################################################
# # Allocations chômage
############################################################################


class csg_deductible_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CSG déductible sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(individu, period, legislation):
        period = period.this_month
        chomage_brut = individu('chomage_brut', period)
        csg_imposable_chomage = individu('csg_imposable_chomage', period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        legislation = legislation(period.start)
        montant_csg = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = legislation.prelevements_sociaux.contributions.csg.chomage.deductible,
            plafond_securite_sociale = legislation.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = (
            legislation.prelevements_sociaux.contributions.csg.chomage.min_exo * nbh_travail *
            legislation.cotsoc.gen.smic_h_b
            )
        csg_deductible_chomage = max_(
            - montant_csg - max_(cho_seuil_exo - (chomage_brut + csg_imposable_chomage + montant_csg), 0),
            0,
            )
        return period, - csg_deductible_chomage


class csg_imposable_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CSG imposable sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(individu, period, legislation):
        period = period.this_month
        chomage_brut = individu('chomage_brut', period)
        legislation = legislation(period.start)

        montant_csg = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            law_node = legislation.prelevements_sociaux.contributions.csg.chomage.imposable,
            plafond_securite_sociale = legislation.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = (
            legislation.prelevements_sociaux.contributions.csg.chomage.min_exo * nbh_travail *
            legislation.cotsoc.gen.smic_h_b
            )
        csg_imposable_chomage = max_(- montant_csg - max_(cho_seuil_exo - (chomage_brut + montant_csg), 0), 0)
        return period, - csg_imposable_chomage


class crds_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CRDS sur les allocations chômage"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"

    def function(individu, period, legislation):
        period = period.this_month
        chomage_brut = individu('chomage_brut', period)
        csg_deductible_chomage = individu('csg_deductible_chomage', period)
        csg_imposable_chomage = individu('csg_imposable_chomage', period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        law = legislation(period.start)
        smic_h_b = law.cotsoc.gen.smic_h_b
        # salaire_mensuel_reference = chomage_brut / .7
        # heures_mensuelles = min_(salaire_mensuel_reference / smic_h_b, 35 * 52 / 12)  # TODO: depuis 2001 mais avant ?
        heures_mensuelles = 35 * 52 / 12
        cho_seuil_exo = law.prelevements_sociaux.contributions.csg.chomage.min_exo * heures_mensuelles * smic_h_b

        montant_crds = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            law_node = law.prelevements_sociaux.contributions.crds.activite,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (2 <= taux_csg_remplacement)

        crds_chomage = max_(
            -montant_crds - max_(
                cho_seuil_exo - (chomage_brut + csg_imposable_chomage + csg_deductible_chomage + montant_crds), 0
                ), 0
            )
        return period, -crds_chomage


class chomage_imposable(Variable):
    base_function = requested_period_added_value
    column = FloatCol(
        val_type = "monetary",
        cerfa_field = {
            QUIFOY['vous']: u"1AP",
            QUIFOY['conj']: u"1BP",
            QUIFOY['pac1']: u"1CP",
            QUIFOY['pac2']: u"1DP",
            QUIFOY['pac3']: u"1EP",
            })
    entity = Individu
    label = u"Allocations chômage imposables"
    set_input = set_input_divide_by_period
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm"

    def function(individu, period):
        chomage_brut = individu('chomage_brut', period)
        csg_deductible_chomage = individu('csg_deductible_chomage', period, options = [ADD])

        return period, chomage_brut + csg_deductible_chomage


class chomage_net(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity = Individu
    label = u"Allocations chômage nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    def function(individu, period):
        chomage_imposable = individu('chomage_imposable', period)
        csg_imposable_chomage = individu('csg_imposable_chomage', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])

        return period, chomage_imposable + csg_imposable_chomage + crds_chomage


############################################################################
# # Pensions
############################################################################

class csg_deductible_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CSG déductible sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(individu, period, legislation):
        period = period.this_month
        retraite_brute = individu('retraite_brute', period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        law = legislation(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = law.prelevements_sociaux.contributions.csg.retraite.deductible,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


class csg_imposable_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CSG imposable sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(individu, period, legislation):
        period = period.this_month
        retraite_brute = individu('retraite_brute', period)
        law = legislation(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = law.prelevements_sociaux.contributions.csg.retraite.imposable,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


class crds_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Individu
    label = u"CRDS sur les pensions de retraite"
    url = u"http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"  # noqa

    def function(individu, period, legislation):
        period = period.this_month
        retraite_brute = individu('retraite_brute', period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        law = legislation(period.start)

        montant_crds = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = law.prelevements_sociaux.contributions.crds.retraite,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (taux_csg_remplacement == 1)
        return period, montant_crds


class casa(DatedVariable):
    column = FloatCol
    entity = Individu
    label = u"Contribution additionnelle de solidarité et d'autonomine"
    start_date = date(2013, 4, 1)
    url = u"http://www.service-public.fr/actualites/002691.html"

    @dated_function(start = date(2015, 1, 1))
    def function_2015(individu, period, legislation):
        period = period.this_month
        retraite_brute = individu('retraite_brute', period = period)
        rfr = individu.foyer_fiscal('rfr', period = period.n_2)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        contributions = legislation(period.start).prelevements_sociaux.contributions
        casa = (
            (taux_csg_remplacement == 3) *
            (rfr > contributions.csg.remplacement.pensions_de_retraite_et_d_invalidite.seuil_de_rfr_2) *
            contributions.casa.calc(retraite_brute)
            )
        return period, - casa

    @dated_function(start = date(2013, 4, 1), stop = date(2014, 12, 31))
    def function_2013_2014(individu, period, legislation):
        period = period.this_month
        retraite_brute = individu('retraite_brute', period = period)
        taux_csg_remplacement = individu('taux_csg_remplacement', period)
        contributions = legislation(period.start).prelevements_sociaux.contributions
        casa = (
            (taux_csg_remplacement == 3) *
            contributions.casa.calc(retraite_brute)
            )
        return period, - casa


class retraite_imposable(Variable):
    base_function = requested_period_added_value
    column = FloatCol(
        val_type = "monetary",
        cerfa_field = {
            QUIFOY['vous']: u"1AS",
            QUIFOY['conj']: u"1BS",
            QUIFOY['pac1']: u"1CS",
            QUIFOY['pac2']: u"1DS",
            QUIFOY['pac3']: u"1ES",
            })
    entity = Individu
    label = u"Retraites au sens strict imposables (rentes à titre onéreux exclues)"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/F415.xhtml"

    def function(individu, period):
        retraite_brute = individu('retraite_brute', period, options = [ADD])
        csg_deductible_retraite = individu('csg_deductible_retraite', period, options = [ADD])

        return period, retraite_brute + csg_deductible_retraite


class retraite_nette(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity = Individu
    label = u"Pensions de retraite nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    def function(individu, period):
        retraite_imposable = individu('retraite_imposable', period)
        casa = individu('casa', period, options = [ADD])
        csg_imposable_retraite = individu('csg_imposable_retraite', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])

        return period, retraite_imposable + csg_imposable_retraite + crds_retraite + casa


class crds_pfam(Variable):
    column = FloatCol
    entity = Famille
    label = u"CRDS sur les prestations familiales)"
    url = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"

    def function(famille, period, legislation):
        period = period
        af = famille('af', period, options = [ADD])
        cf = famille('cf', period, options = [ADD])
        asf = famille('asf', period, options = [ADD])
        ars = famille('ars', period)
        paje = famille('paje', period, options = [ADD])
        ape = famille('ape', period, options = [ADD])
        apje = famille('apje', period, options = [ADD])
        taux_crds = legislation(period.start).prelevements_sociaux.contributions.crds.taux

        return period, -(af + cf + asf + ars + paje + ape + apje) * taux_crds
