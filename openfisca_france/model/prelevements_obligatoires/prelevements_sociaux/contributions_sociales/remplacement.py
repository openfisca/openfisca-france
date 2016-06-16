# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import maximum as max_, minimum as min_


from ....base import *  # noqa analysis:ignore
from .base import montant_csg_crds


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
    entity_class = Individus
    label = u"Taux retenu sur la CSG des revenus de remplacment"




############################################################################
# # Allocations chômage
############################################################################


class csg_deductible_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.this_month
        chomage_brut = simulation.calculate('chomage_brut', period)
        csg_imposable_chomage = simulation.calculate('csg_imposable_chomage', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)
        montant_csg = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = law.csg.chomage.deductible,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = law.csg.chomage.min_exo * nbh_travail * law.cotsoc.gen.smic_h_b
        csg_deductible_chomage = max_(
            - montant_csg - max_(cho_seuil_exo - (chomage_brut + csg_imposable_chomage + montant_csg), 0),
            0,
            )

        return period, - csg_deductible_chomage


class csg_imposable_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les allocations chômage"
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        period = period.this_month
        chomage_brut = simulation.calculate('chomage_brut', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            law_node = law.csg.chomage.imposable,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        nbh_travail = 35 * 52 / 12  # = 151.67  # TODO: depuis 2001 mais avant ?
        cho_seuil_exo = law.csg.chomage.min_exo * nbh_travail * law.cotsoc.gen.smic_h_b
        csg_imposable_chomage = max_(- montant_csg - max_(cho_seuil_exo - (chomage_brut + montant_csg), 0), 0)
        return period, - csg_imposable_chomage


class crds_chomage(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les allocations chômage"
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/contrib-remb-dette-sociale.htm"

    def function(self, simulation, period):
        period = period.this_month
        chomage_brut = simulation.calculate('chomage_brut', period)
        csg_deductible_chomage = simulation.calculate('csg_deductible_chomage', period)
        csg_imposable_chomage = simulation.calculate('csg_imposable_chomage', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        smic_h_b = law.cotsoc.gen.smic_h_b
        # salaire_mensuel_reference = chomage_brut / .7
        # heures_mensuelles = min_(salaire_mensuel_reference / smic_h_b, 35 * 52 / 12)  # TODO: depuis 2001 mais avant ?
        heures_mensuelles = 35 * 52 / 12
        cho_seuil_exo = law.csg.chomage.min_exo * heures_mensuelles * smic_h_b

        montant_crds = montant_csg_crds(
            base_avec_abattement = chomage_brut,
            law_node = law.crds.activite,
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
        cerfa_field = {QUIFOY['vous']: u"1AP",
                   QUIFOY['conj']: u"1BP",
                   QUIFOY['pac1']: u"1CP",
                   QUIFOY['pac2']: u"1DP",
                   QUIFOY['pac3']: u"1EP",
                   })  # (f1ap, f1bp, f1cp, f1dp, f1ep)
    entity_class = Individus
    label = u"Allocations chômage imposables"
    set_input = set_input_divide_by_period
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/chomage.htm"

    def function(self, simulation, period):
        period = period
        chomage_brut = simulation.calculate('chomage_brut', period)
        csg_deductible_chomage = simulation.calculate_add('csg_deductible_chomage', period)

        return period, chomage_brut + csg_deductible_chomage


class chomage_net(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Allocations chômage nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N549.xhtml"

    def function(self, simulation, period):
        period = period
        chomage_imposable = simulation.calculate('chomage_imposable', period)
        csg_imposable_chomage = simulation.calculate_add('csg_imposable_chomage', period)
        crds_chomage = simulation.calculate_add('crds_chomage', period)

        return period, chomage_imposable + csg_imposable_chomage + crds_chomage


############################################################################
# # Pensions
############################################################################

class csg_deductible_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG déductible sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.this_month
        retraite_brute = simulation.calculate('retraite_brute', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            indicatrice_taux_plein = (taux_csg_remplacement == 3),
            indicatrice_taux_reduit = (taux_csg_remplacement == 2),
            law_node = law.csg.retraite.deductible,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


class csg_imposable_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les pensions de retraite"
    url = u"https://www.lassuranceretraite.fr/cs/Satellite/PUBPrincipale/Retraites/Paiement-Votre-Retraite/Prelevements-Sociaux?packedargs=null"  # noqa

    def function(self, simulation, period):
        period = period.this_month
        retraite_brute = simulation.calculate('retraite_brute', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = law.csg.retraite.imposable,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            )
        return period, montant_csg


class crds_retraite(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les pensions de retraite"
    url = u"http://www.pensions.bercy.gouv.fr/vous-%C3%AAtes-retrait%C3%A9-ou-pensionn%C3%A9/le-calcul-de-ma-pension/les-pr%C3%A9l%C3%A8vements-effectu%C3%A9s-sur-ma-pension"  # noqa

    def function(self, simulation, period):
        period = period.this_month
        retraite_brute = simulation.calculate('retraite_brute', period)
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            base_sans_abattement = retraite_brute,
            law_node = law.crds.retraite,
            plafond_securite_sociale = law.cotsoc.gen.plafond_securite_sociale,
            ) * (taux_csg_remplacement == 1)
        return period, montant_crds


class casa(DatedVariable):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle de solidarité et d'autonomie"
    url = u"http://www.service-public.fr/actualites/002691.html"

    @dated_function(date(2013, 4, 1))
    def function_2013(self, simulation, period):
        period = period.this_month
        retraite_brute = simulation.calculate('retraite_brute', period)
        rfr_holder = simulation.compute('rfr', period.start.offset('first-of', 'year').offset(-2, 'year').period('year'))
        taux_csg_remplacement = simulation.calculate('taux_csg_remplacement', period)
        law = simulation.legislation_at(period.start)

        rfr = self.cast_from_entity_to_roles(rfr_holder)

        casa = (taux_csg_remplacement == 3) * law.prelsoc.add_ret * retraite_brute * (rfr > 13900)
        # TODO: insert in parameters file and deal with nombre de part fiscales

        return period, - casa


class retraite_imposable(Variable):
    base_function = requested_period_added_value
    column = FloatCol(
            val_type = "monetary",
            cerfa_field = {QUIFOY['vous']: u"1AS",
                           QUIFOY['conj']: u"1BS",
                           QUIFOY['pac1']: u"1CS",
                           QUIFOY['pac2']: u"1DS",
                           QUIFOY['pac3']: u"1ES",
                            })  # (f1as, f1bs, f1cs, f1ds, f1es)
    entity_class = Individus
    label = u"Retraites au sens strict imposables (rentes à titre onéreux exclues)"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/F415.xhtml"

    def function(self, simulation, period):
        period = period
        retraite_brute = simulation.calculate_add('retraite_brute', period)
        csg_deductible_retraite = simulation.calculate_add('csg_deductible_retraite', period)

        return period, retraite_brute + csg_deductible_retraite


class retraite_nette(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Pensions de retraite nettes"
    set_input = set_input_divide_by_period
    url = u"http://vosdroits.service-public.fr/particuliers/N20166.xhtml"

    # def function(self, retraite_imposable, csg_imposable_retraite, crds_retraite, casa):
    # return retraite_imposable + csg_imposable_retraite + crds_retraite + casa
    def function(self, simulation, period):
        period = period
        retraite_imposable = simulation.calculate('retraite_imposable', period)
        csg_imposable_retraite = simulation.calculate_add('csg_imposable_retraite', period)
        crds_retraite = simulation.calculate_add('crds_retraite', period)

        return period, retraite_imposable + csg_imposable_retraite + crds_retraite


class crds_pfam(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"CRDS sur les prestations familiales)"
    url = "http://www.cleiss.fr/docs/regimes/regime_francea1.html"

    def function(self, simulation, period):
        '''
        Renvoie la CRDS des prestations familiales
        '''
        period = period
        af = simulation.calculate_add('af', period)
        cf = simulation.calculate_add('cf', period)
        asf = simulation.calculate_add('asf', period)
        ars = simulation.calculate('ars', period)
        paje = simulation.calculate_add('paje', period)
        ape = simulation.calculate_add('ape', period)
        apje = simulation.calculate_add('apje', period)
        _P = simulation.legislation_at(period.start)

        return period, -(af + cf + asf + ars + paje + ape + apje) * _P.fam.af.crds
