# -*- coding: utf-8 -*-

from __future__ import division
import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)


# Prélèvements sociaux sur les revenus du capital
# (dispositifs codés à partir de 2013 : cf. doctring de la variable assiette_csg_revenus_capital)


# 1. Définition de variables associées aux revenus du capital soumis aux prélèvements sociaux mais
#    ni au barème de l'impôt sur le revenu, ni au prélèvement forfaitaire libératoire
#    (et donc non présents sur les déclarations de revenu)


class interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018(Variable):
    """
    NB :
    (1) Cette variable est définie indépendemment de epargne_revenus_non_imposables
    (2) Les intérêts des PEL de plus de 12 ans sont imposables à l'impôt sur le revenu, et donc déjà présents dans les cases 2TR ou 2FA (attention: formulaire IR 2019 sur revenus 2018 non connu au moment de coder cette variable)
    """
    value_type = float
    entity = Individu
    label = u"Intérêts des plans épargne logement (PEL) de moins de 12 ans ouverts avant le 1er janvier 2018"
    definition_period = YEAR


class interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018(Variable):
    """
    NB :
    (1) Cette variable est définie indépendemment de epargne_revenus_non_imposables
    (2) Les intérêts des PEL de plus de 12 ans sont imposables à l'impôt sur le revenu, et donc déjà présents dans les cases 2TR ou 2FA (attention: formulaire IR 2019 sur revenus 2018 non connu au moment de coder cette variable)
    """
    value_type = float
    entity = Individu
    label = u"Intérêts des plans épargne logement (PEL) de moins de 12 ans ouverts à partir du 1er janvier 2018"
    definition_period = YEAR


class interets_compte_epargne_logement_ouvert_avant_2018(Variable):
    """ NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables """
    value_type = float
    entity = Individu
    label = u"Intérêts des comptes épargne logement (CEL) ouverts avant le 1er janvier 2018"
    definition_period = YEAR


class interets_compte_epargne_logement_ouvert_a_partir_de_2018(Variable):
    """ NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables """
    value_type = float
    entity = Individu
    label = u"Intérêts des comptes épargne logement (CEL) ouverts à partir du 1er janvier 2018"
    definition_period = YEAR


class assurance_vie_ps_exoneree_irpp_pl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement libératoire mais soumis aux prélèvements sociaux"
    definition_period = YEAR


# 2. Assiette des revenus du capital soumis à la CSG (valable pour les autres prélèvements sociaux)

class assiette_csg_plus_values(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Assiette des plus-values soumis à la CSG"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        Attention : cette formule est susceptible de contenir des erreurs pour les années avant 2013 (cf. commentaires sur assiette_csg_revenus_capital)

        Notes sur le champ de cette variable :
            Cette assiette de plus-values est partielle. De nombreux types de plus-values sont
            manquants, rien que parmi les plus-values déclarées dans la déclaration de revenus
            au titre de l'impôt sur le revenu. Ceci s'explique par la complexité de la législation sur
            la prise en compte des plus-values dans le calcul des prélèvements sociaux (exemple : plus-values
            réalisées sur PEA taxables selon les règles en vigueur l'année de réalisation et non l'année de retrait,
            plus-values taxées après report, et taxables parfois selon la législation en vigueur au moment du report et non
            pas au moment de la taxation, etc.).
            Critère de choix : on part des dénombrements fiscaux de la déclaration 2042 des revenus 2016
            (montants totaux déclarés au niveau national pour chaque case), et on constate que les cases 3VH, 3VG,
            3SG, 3SL, 3VA, 3VB, 3VO, 3VP, 3VZ, 3VW, 3WG, 3WH et 3WM représentent à elles seules 88% de
            l'ensemble des cases associées aux plus-values (cases de classe 3). On se limite donc aux
            plus-values associées à ces cases. Parmi ces cases, certaines ne donnent pas lieu à une imposition
            pendant l'année courante du fait d'un report ou sursis d'imposition (3WG, 3WH, 3WM), ou ne sont
            tout simplement pas comptabilisées dans l'assiette CSG (3VH, 3VW). Au total, le nombre de cases
            est fortement réduit, mais en ne perdant potentiellement qu'une faible partie des plus-values présentes
            dans l'assiette CSG (même en excluant ces cases importantes mais non sujettes à imposition, les cases
            restantes représentent 82% des montants de l'ensemble des cases de classe 3 (hors cases supprimées).
            NB : en plus des cases les plus importantes, on inclut aussi 3WE, car les abattements
            renseignés dans les cases 3SG et 3SL peuvent aussi être associés à des montants nets renseignés en 3WE.

        Notes concernant les plus-values immobilières :
            (1) Les plus-values immobilières déclarées en 3VZ sont les plus-values nettes sousmises à
                l'impôt sur le revenu. Or, les prélèvements sociaux sont appliqués aussi sur une valeure
                nette, mais déterminée via des abattements différents de ceux de l'impôt sur le revenu
                (cf. formulaire 2048-IMM de 2018 par exemple pour une explication). On ignore ces
                différences d'abattement, et on suppose que la valeur nette au sens des prélèvements
                sociaux est la même que celle au sens de l'impôt sur le revenu.
            (2) On ne compte pas la case 3VW dans la base soumise aux prélèvements sociaux. Ce montant,
                exonéré de l'impôt sur le revenu, semble être exonéré aussi des prélèvements sociaux,
                même s'il est déclaré dans la déclaration de revenus : cf. art. L136-7 du CSS, qui
                cite l'art. 150 U du CGI.
        '''

        # Plus-values mobilières brutes (avant abattement)
        f3vg = foyer_fiscal('f3vg', period)
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3va_2014 = foyer_fiscal('f3va_2014', period)
        f3we = foyer_fiscal('f3we', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        return f3vg + f3sg + f3sl + f3va_2014 + f3vz + f3we

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Notes concernant les plus-values immobilières : cf. formule commençant en 2013
        '''

        # Plus-values mobilières brutes (avant abattement)
        f3vg = foyer_fiscal('f3vg', period)
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3va_2016_i = foyer_fiscal.members('f3va_2016', period)
        f3va_2016 = foyer_fiscal.sum(f3va_2016_i)
        f3we = foyer_fiscal('f3we', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        return f3vg + f3sg + f3sl + f3va_2016 + f3vz + f3we

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Notes concernant les plus-values immobilières : cf. formule commençant en 2013
        '''

        # Plus-values mobilières brutes (avant abattement)
        f3vg = foyer_fiscal('f3vg', period)
        f3sg = foyer_fiscal('f3sg', period)
        f3sl = foyer_fiscal('f3sl', period)
        f3va = foyer_fiscal('f3va', period)
        f3we = foyer_fiscal('f3we', period)
        f3ua = foyer_fiscal('f3ua', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        return f3vg + f3sg + f3sl + f3va + f3ua + f3vz + f3we


class assiette_csg_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Assiette des revenus du capital soumis à la CSG"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Hypothèses dérrière ce calcul :
            (1) On ne distingue pas la CSG sur les revenus du patrimoine (art. L136-6 du CSS)
                de celle sur les revenus de placement (art. L136-6 du CSS)
                ATTENTION : Les taux de la CSG et de l'ensemble des prélèvements sociaux sont identiques pour
                ces deux types de revenu depuis 2013 seulement, la formule devrait donc être corrigée pour les années avant 2013.
            (2) Le timing de la soumission des intérêts des PEL et CEL aux prélèvements sociaux
                est complexe. Cette soumission peut se faire annuellement, ou en cumulé, et ce
                en fonction de différents paramètres. Mais on ne prend pas en compte cette fonctionnalité.
        NB : catégorie(s) de revenu non encore incluse(s) dans cette assiette : épargne salariale
        '''

        # Revenus du capital présents dans la section 2 de la déclaration de revenus
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])

        # Rentes viagères à titre onéreux
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)

        # Revenus des produits d'épargne logement
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018_i = foyer_fiscal.members('interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018', period)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018 = foyer_fiscal.sum(interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018_i)
        interets_compte_epargne_logement_ouvert_avant_2018_i = foyer_fiscal.members('interets_compte_epargne_logement_ouvert_avant_2018', period)
        interets_compte_epargne_logement_ouvert_avant_2018 = foyer_fiscal.sum(interets_compte_epargne_logement_ouvert_avant_2018_i)

        # Revenus fonciers
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)

        # Plus-values
        assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)

        # produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement forfaitaire libératoire (et donc non présents dans revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        assurance_vie_ps_exoneree_irpp_pl = foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)

        return (
            revenus_capitaux_prelevement_bareme
            + revenus_capitaux_prelevement_liberatoire
            + rente_viagere_titre_onereux_net
            + interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018
            + interets_compte_epargne_logement_ouvert_avant_2018
            + rev_cat_rfon
            + assiette_csg_plus_values
            + assurance_vie_ps_exoneree_irpp_pl
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Cf. docstring de la formule précédente
        Différence par rapport à la formule précédente :
           - Ajout des intérêts de PEL et CEL ouverts à partir du 1er janvier 2018
           - On remplace les variables revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire
             par revenus_capitaux_prelevement_forfaitaire_unique_ir
             Note : du fait du PFU, la base des revenus du capital au titre de l'impôt sur le revenu se rapproche de la base au titre des prélèvements sociaux,
                    d'où le fait qu'on utilise cette variable. En revanche, concernant les prêts participatifs, le montant au titre de l'impôt sur le revenu
                    forfaitaire est le montant net des pertes, alors que celui soumis au titre des prélèvements sociaux est le montant brut. Cependant,
                    la case 2TT contient le montant des intérêts de ces prêts après déduction de ces pertes. Donc, on est contraint de prendre un montant net.
        '''

        # Revenus du capital présents dans la section 2 de la déclaration de revenus
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])

        # Rentes viagères à titre onéreux
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)

        # Revenus des produits d'épargne logement
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018_i = foyer_fiscal.members('interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018', period)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018 = foyer_fiscal.sum(interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018_i)
        interets_compte_epargne_logement_ouvert_avant_2018_i = foyer_fiscal.members('interets_compte_epargne_logement_ouvert_avant_2018', period)
        interets_compte_epargne_logement_ouvert_avant_2018 = foyer_fiscal.sum(interets_compte_epargne_logement_ouvert_avant_2018_i)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018_i = foyer_fiscal.members('interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018', period)
        interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018 = foyer_fiscal.sum(interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018_i)
        interets_compte_epargne_logement_ouvert_a_partir_de_2018_i = foyer_fiscal.members('interets_compte_epargne_logement_ouvert_a_partir_de_2018', period)
        interets_compte_epargne_logement_ouvert_a_partir_de_2018 = foyer_fiscal.sum(interets_compte_epargne_logement_ouvert_a_partir_de_2018_i)

        # Revenus fonciers
        rev_cat_rfon = foyer_fiscal('rev_cat_rfon', period)

        # Plus-values
        assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)

        # produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement forfaitaire libératoire (et donc non présents dans revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        assurance_vie_ps_exoneree_irpp_pl = foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)

        return (
            revenus_capitaux_prelevement_forfaitaire_unique_ir
            + rente_viagere_titre_onereux_net
            + interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018
            + interets_compte_epargne_logement_ouvert_avant_2018
            + interets_plan_epargne_logement_moins_de_12_ans_ouvert_a_partir_de_2018
            + interets_compte_epargne_logement_ouvert_a_partir_de_2018
            + rev_cat_rfon
            + assiette_csg_plus_values
            + assurance_vie_ps_exoneree_irpp_pl
            )


# 3. Variables de prélèvements sociaux sur les revenus du capital

class csg_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CSG sur les revenus du capital"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period)

        return -assiette_csg_revenus_capital * P.prelevements_sociaux.contributions.csg.capital.glob

# revenus du capital soumis au barème


class crds_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"CRDS sur les revenus du capital"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period).taxation_capital.prelevements_sociaux

        return -assiette_csg_revenus_capital * P.crds.revenus_du_patrimoine


class prelevements_sociaux_revenus_capital_hors_csg_crds(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux (hors CSG et CRDS) sur les revenus du capital"
    reference = u"https://www.service-public.fr/particuliers/vosdroits/F2329"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine
            + P.caps.revenus_du_patrimoine
            + P.prelevements_solidarite.revenus_du_patrimoine
            )

        return -assiette_csg_revenus_capital * total

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine
            + P.caps.revenus_du_patrimoine
            + P.prelevements_solidarite.revenus_du_patrimoine
            + P.caps.rsa
            )

        return -assiette_csg_revenus_capital * total

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        P = parameters(period).taxation_capital.prelevements_sociaux

        total = (
            P.prelevement_social.revenus_du_patrimoine
            + P.caps.revenus_du_patrimoine
            + P.prelevements_solidarite.revenus_du_patrimoine
            )

        return -assiette_csg_revenus_capital * total


class prelevements_sociaux_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Prélèvements sociaux sur les revenus du capital"
    reference = u"https://www.service-public.fr/particuliers/vosdroits/F2329"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        csg_revenus_capital = foyer_fiscal('csg_revenus_capital', period)
        crds_revenus_capital = foyer_fiscal('crds_revenus_capital', period)
        prelevements_sociaux_revenus_capital_hors_csg_crds = foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period)

        return csg_revenus_capital + crds_revenus_capital + prelevements_sociaux_revenus_capital_hors_csg_crds
