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
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])

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
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus du capital"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Cette formule n'est définie qu'à partir de 2013 : cf. docstring de la variable
        assiette_csg_revenus_capital pour une explication
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        _P = parameters(period)

        return -assiette_csg_revenus_capital * _P.prelevements_sociaux.contributions.csg.capital.glob

# revenus du capital soumis au barème


class crds_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Cette formule n'est définie qu'à partir de 2013 : cf. docstring de la variable
        assiette_csg_revenus_capital pour une explication
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        _P = parameters(period).taxation_capital.prelevements_sociaux

        return -assiette_csg_revenus_capital * _P.crds.revenus_du_patrimoine


# revenus du capital soumis au barème

class prelevements_sociaux_revenus_capital_hors_csg_crds(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux (hors CSG et CRDS) sur les revenus du capital"
    reference = u"https://www.service-public.fr/particuliers/vosdroits/F2329"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Cette formule n'est définie qu'à partir de 2013 : cf. docstring de la variable
        assiette_csg_revenus_capital pour une explication
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine + P.caps.revenus_du_patrimoine +
            P.prelevements_solidarite.revenus_du_patrimoine
            )

        return -assiette_csg_revenus_capital * total

class prelevements_sociaux_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital"
    reference = u"https://www.service-public.fr/particuliers/vosdroits/F2329"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Cette formule n'est définie qu'à partir de 2013 : cf. docstring de la variable
        assiette_csg_revenus_capital pour une explication
        '''
        csg_revenus_capital = foyer_fiscal('csg_revenus_capital', period)
        crds_revenus_capital = foyer_fiscal('crds_revenus_capital', period)
        prelevements_sociaux_revenus_capital_hors_csg_crds = foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period)

        return csg_revenus_capital + crds_revenus_capital + prelevements_sociaux_revenus_capital_hors_csg_crds


# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.prelevements_sociaux.contributions.csg.capital.nonimp
# #        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)
