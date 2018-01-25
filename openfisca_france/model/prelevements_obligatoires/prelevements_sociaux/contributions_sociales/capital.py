# -*- coding: utf-8 -*-

from __future__ import division

import logging

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont
#        en CG et BH en 2010


def _mhsup(hsup):
    """
    Heures supplémentaires comptées négativement
    """
    return -hsup

############################################################################
# # Revenus du capital
############################################################################


# revenus du capital soumis au barème


class csg_cap_bar(Variable):
    """Calcule la CSG sur les revenus du capital soumis au barème."""
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus du capital soumis au barème"
    reference = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        _P = parameters(period)

        return -rev_cap_bar * _P.prelevements_sociaux.contributions.csg.capital.glob


class crds_cap_bar(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au barème."""
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital soumis au barème"
    reference = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -rev_cap_bar * _P.crds.revenus_du_patrimoine


class prelsoc_cap_bar(Variable):
    """Calcule le prélèvement social sur les revenus du capital soumis au barème"""
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème"
    reference = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine
        return -rev_cap_bar * total

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -rev_cap_bar * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa
        return -rev_cap_bar * total

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa +
            P.prelevements_solidarite.revenus_du_patrimoine
            )
        return -rev_cap_bar * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine +
            P.prelevements_solidarite.revenus_du_patrimoine
            )
        return -rev_cap_bar * total


class csg_pv_mo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les plus-values de cession de valeurs mobilières"
    reference = "http://vosdroits.service-public.fr/particuliers/F21618.xhtml"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Calcule la CSG sur les plus-values de cession mobilière
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period)

        return -f3vg * _P.prelevements_sociaux.contributions.csg.capital.glob


class crds_pv_mo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les plus-values de cession de valeurs mobilières"
    reference = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Calcule la CRDS sur les plus-values de cession mobilière
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -f3vg * _P.crds.revenus_du_patrimoine


class prelsoc_pv_mo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values
        de cession de valeurs mobilières
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine
        return -f3vg * total

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values
        de cession de valeurs mobilières
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -f3vg * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession de valeurs mobilières
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa
        return -f3vg * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession de valeurs mobilières
        """
        f3vg = foyer_fiscal('f3vg', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -f3vg * total


# Plus-values immobilières

class csg_pv_immo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les plus-values immobilières"
    reference = "http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Calcule la CSG sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period)

        return -f3vz * _P.prelevements_sociaux.contributions.csg.capital.glob


class crds_pv_immo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les plus-values immobilières"
    reference = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Calcule la CRDS sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -f3vz * _P.crds.revenus_du_patrimoine


class prelsoc_pv_immo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les plus-values immobilières"
    reference = "http://www.pap.fr/argent/impots/les-plus-values-immobilieres/a1314/l-imposition-de-la-plus-value-immobiliere"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine

        return -f3vz * total

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine

        return -f3vz * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa
        return -f3vz * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        f3vz = foyer_fiscal('f3vz', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -f3vz * total


# Revenus fonciers

class csg_fon(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus fonciers"
    reference = "http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Calcule la CSG sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period)

        return -rev_cat_rfon * _P.prelevements_sociaux.contributions.csg.capital.glob


class crds_fon(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus fonciers"
    reference = "http://vosdroits.service-public.fr/particuliers/F2329.xhtml"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Calcule la CRDS sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -rev_cat_rfon * _P.crds.revenus_du_patrimoine


class prelsoc_fon(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus fonciers"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        TODO : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine

        return -rev_cat_rfon * total

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine

        return -rev_cat_rfon * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = assiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa
        return -rev_cat_rfon * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = assiette IR valable 2006-2014 mais pourrait changer
        '''
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)
        _P = parameters(period)

        P = _P.taxation_capital.prelevements_sociaux
        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -rev_cat_rfon * total


# revenus du capital soumis au prélèvement libératoire


class csg_cap_lib(Variable):
    """Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire."""
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus du capital soumis au prélèvement libératoire"
    reference = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])
        _P = parameters(period)

        return -rev_cap_lib * _P.prelevements_sociaux.contributions.csg.capital.glob


class crds_cap_lib(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire."""
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire"
    reference = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -rev_cap_lib * _P.crds.revenus_du_patrimoine


class prelsoc_cap_lib(Variable):
    """Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire."""
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire"
    reference = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])
        prelsoc = parameters(period).taxation_capital.prelevements_sociaux

        start_year = period.start.year
        if start_year < 2006:
            total = prelsoc.prelevement_social.revenus_du_patrimoine
        elif start_year < 2009:
            total = prelsoc.prelevement_social.revenus_du_patrimoine + prelsoc.caps.revenus_du_patrimoine
        elif start_year < 2012:
            total = (
                prelsoc.prelevement_social.revenus_du_patrimoine + prelsoc.caps.revenus_du_patrimoine + prelsoc.caps.rsa
                )
        elif start_year < 2013:
            total = (
                prelsoc.prelevement_social.revenus_du_patrimoine + prelsoc.caps.revenus_du_patrimoine +
                prelsoc.caps.rsa + prelsoc.prelevements_solidarite.revenus_du_patrimoine
                )
        else:
            total = (
                prelsoc.prelevement_social.revenus_du_patrimoine + prelsoc.caps.revenus_du_patrimoine +
                prelsoc.prelevements_solidarite.revenus_du_patrimoine
                )
        return -rev_cap_lib * total

# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.prelevements_sociaux.contributions.csg.capital.nonimp
# #        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)
