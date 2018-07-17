# -*- coding: utf-8 -*-

from __future__ import division

import logging

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont
#        en CG et BH en 2010


############################################################################
# # Revenus du capital
############################################################################

class interets_plan_epargne_logement(Variable):
    """ NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables """
    value_type = float
    entity = Individu
    label = u"Intérêts des plans épargne logement (PEL)"
    definition_period = YEAR

class interets_compte_epargne_logement(Variable):
    """ NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables """
    value_type = float
    entity = Individu
    label = u"Intérêts des comptes épargne logement (CEL)"
    definition_period = YEAR

class assurance_vie_ps_exoneree_irpp_pl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement libératoire mais soumis aux prélèvements sociaux"
    definition_period = YEAR


class assiette_csg_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Assiette des revenus du capital soumis à la CSG"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Hypothèses dérrière ce calcul :
            (1) On ne distingue pas la CSG sur les revenus du patrimoine (art. L136-6 du CSS)
                de celle sur les revenus de placement (art. L136-6 du CSS)
                Les taux de la CSG et de l'ensemble des prélèvements sociaux sont identiques pour
                ces deux types de revenu depuis 2013 seulement, d'où le fait qu'on ne définit cette variable
                qu'à partir de 2013.
            (2) Le timing de la soumission des intérêts des PEL et CEL aux prélèvements sociaux
                est complexe. Cette soumission peut se faire annuellement, ou en cumulé, et ce
                en fonction de différents paramètres. Mais on ne prend pas en compte cette fonctionnalité.
        '''

        # Revenus du capital présents dans la section 2 de la déclaration de revenus
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        rev_cap_lib = foyer_fiscal('rev_cap_bar', period, options = [ADD])

        # Rentes viagères à titre onéreux
        retraite_titre_onereux_net = foyer_fiscal('retraite_titre_onereux_net', period)

        # Revenus des produits d'épargne logement
        interets_plan_epargne_logement_i = foyer_fiscal.members('interets_plan_epargne_logement', period)
        interets_plan_epargne_logement = foyer_fiscal.sum(interets_plan_epargne_logement_i)
        interets_compte_epargne_logement_i = foyer_fiscal.members('interets_compte_epargne_logement', period)
        interets_compte_epargne_logement = foyer_fiscal.sum(interets_compte_epargne_logement_i)

        # Revenus fonciers
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)

        # Plus-values
        f3vg = foyer_fiscal('f3vg', period)
        f3vz = foyer_fiscal('f3vz', period)

        # produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement forfaitaire libératoire (et donc non présents dans rev_cap_bar et rev_cap_lib)
        assurance_vie_ps_exoneree_irpp_pl = foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)


        return (
            rev_cap_bar
            + rev_cap_lib
            + retraite_titre_onereux_net
            + interets_plan_epargne_logement
            + interets_compte_epargne_logement
            + rev_cat_rfon
            + f3vg
            + f3vz
            + assurance_vie_ps_exoneree_irpp_pl
            )


class csg_revenus_capital(Variable):
    """Calcule la CSG sur les revenus du capital."""
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus du capital"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        _P = parameters(period)

        return -assiette_csg_revenus_capital * _P.prelevements_sociaux.contributions.csg.capital.glob


# revenus du capital soumis au barème


class crds_cap_bar(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au barème."""
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital soumis au barème"
    reference = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -revenus_capitaux_prelevement_bareme * _P.crds.revenus_du_patrimoine


class prelsoc_cap_bar(Variable):
    """Calcule le prélèvement social sur les revenus du capital soumis au barème"""
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème"
    reference = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine
        return -revenus_capitaux_prelevement_bareme * total

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine
        return -revenus_capitaux_prelevement_bareme * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa
        return -revenus_capitaux_prelevement_bareme * total

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine + P.caps.rsa +
            P.prelevements_solidarite.revenus_du_patrimoine
            )
        return -revenus_capitaux_prelevement_bareme * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine +
            P.prelevements_solidarite.revenus_du_patrimoine
            )
        return -revenus_capitaux_prelevement_bareme * total




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



class crds_cap_lib(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire."""
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire"
    reference = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -revenus_capitaux_prelevement_liberatoire * _P.crds.revenus_du_patrimoine


class prelsoc_cap_lib(Variable):
    """Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire."""
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire"
    reference = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
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
        return -revenus_capitaux_prelevement_liberatoire * total

# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.prelevements_sociaux.contributions.csg.capital.nonimp
# #        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)
