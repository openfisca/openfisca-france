import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)


# Prélèvements sociaux sur les revenus du capital
# (dispositifs codés à partir de 2013 : cf. doctring de la variable assiette_csg_revenus_capital)


# 1. Définition de variables associées aux revenus du capital soumis aux prélèvements sociaux mais
#    ni au barème de l'impôt sur le revenu, ni au prélèvement forfaitaire libératoire
#    (et donc non présents sur les déclarations de revenu)


class interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018(Variable):
    '''
    NB :
    (1) Cette variable est définie indépendemment de epargne_revenus_non_imposables
    (2) Les intérêts des PEL de plus de 12 ans et ouverts avant 2018 sont imposables à l'impôt sur le revenu, et donc déjà présents dans la déclaration de revenus (ex : case 2TR pour les revenus de 2018)
    '''
    value_type = float
    entity = Individu
    label = 'Intérêts des plans épargne logement (PEL) de moins de 12 ans ouverts avant le 1er janvier 2018'
    definition_period = YEAR


class interets_compte_epargne_logement_ouvert_avant_2018(Variable):
    ''' NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables '''
    value_type = float
    entity = Individu
    label = 'Intérêts des comptes épargne logement (CEL) ouverts avant le 1er janvier 2018'
    definition_period = YEAR


class interets_pel_cel_non_soumis_IR(Variable):
    ''' NB : Cette variable est définie indépendemment de epargne_revenus_non_imposables '''
    value_type = float
    entity = Individu
    label = "Intérêts des plans épargne logement (PEL) et des comptes épargne logement (CEL) non soumis à l'impôt sur le revenu"
    definition_period = YEAR

    def formula(individu, period):

        interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018 = individu('interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018', period)
        interets_compte_epargne_logement_ouvert_avant_2018 = individu('interets_compte_epargne_logement_ouvert_avant_2018', period)

        return (
            interets_plan_epargne_logement_moins_de_12_ans_ouvert_avant_2018
            + interets_compte_epargne_logement_ouvert_avant_2018
            )


class assurance_vie_ps_exoneree_irpp_pl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement libératoire mais soumis aux prélèvements sociaux"
    definition_period = YEAR


# 2. Assiette des revenus du capital soumis à la CSG (valable pour les autres prélèvements sociaux)

class assiette_csg_plus_values(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Assiette des plus-values soumis à la CSG'
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
            3SG, 3SL, 3VA, 3VB, 3VO, 3VP, 3VZ, 3VW, 3WG, 3WH et 3WM représentent à elles seules 88% des
            montants associés aux plus-values (cases de classe 3). On se limite donc aux
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
        f3vt = foyer_fiscal('f3vt', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        # plus-values vente d'entreprise retraite
        pveximpres_i = foyer_fiscal.members('pveximpres', period)
        pveximpres = foyer_fiscal.sum(pveximpres_i)

        return f3vg + f3sg + f3sl + f3va_2014 + f3vz + f3we + f3vt + rpns_pvce + glo_taxation_ir_forfaitaire + pveximpres

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
        f3vt = foyer_fiscal('f3vt', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        # plus-values vente d'entreprise retraite
        pveximpres_i = foyer_fiscal.members('pveximpres', period)
        pveximpres = foyer_fiscal.sum(pveximpres_i)

        return f3vg + f3sg + f3sl + f3va_2016 + f3vz + f3we + f3vt + rpns_pvce + glo_taxation_ir_forfaitaire + pveximpres

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
        f3vt = foyer_fiscal('f3vt', period)
        f3pi = foyer_fiscal('f3pi', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        # plus-values vente d'entreprise retraite
        pveximpres_i = foyer_fiscal.members('pveximpres', period)
        pveximpres = foyer_fiscal.sum(pveximpres_i)

        return f3vg + f3sg + f3sl + f3va + f3ua + f3vz + f3we + f3vt + f3pi + rpns_pvce + glo_taxation_ir_forfaitaire + pveximpres

    def formula_2018_01_01(foyer_fiscal, period, parameters):

        # Plus-values mobilières brutes (avant abattement)
        f3vg = foyer_fiscal('f3vg', period)
        f3we = foyer_fiscal('f3we', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        f3pi = foyer_fiscal('f3pi', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        # plus-values vente d'entreprise retraite
        pveximpres_i = foyer_fiscal.members('pveximpres', period)
        pveximpres = foyer_fiscal.sum(pveximpres_i)

        return f3vg + f3ua + f3vz + f3we + rpns_pvce + f3sj + f3sk + f3vm + f3vt + f3wi + f3wj + f3pi + f3tj + glo_taxation_ir_forfaitaire + pveximpres

    def formula_2019_01_01(foyer_fiscal, period, parameters):

        # Plus-values mobilières brutes (avant abattement)
        f3vg = foyer_fiscal('f3vg', period)
        f3we = foyer_fiscal('f3we', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        f3pi = foyer_fiscal('f3pi', period)
        f3an = foyer_fiscal('f3an', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        # Plus-values immobilières
        f3vz = foyer_fiscal('f3vz', period)

        # plus-values vente d'entreprise retraite
        pveximpres_i = foyer_fiscal.members('pveximpres', period)
        pveximpres = foyer_fiscal.sum(pveximpres_i)

        return f3vg + f3ua + f3vz + f3we + rpns_pvce + f3sj + f3sk + f3vt + f3wi + f3wj + f3pi + f3tj + f3an + glo_taxation_ir_forfaitaire + pveximpres


class assiette_csg_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Assiette des revenus du capital soumis à la CSG'
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
        Note à partir de 2018 : du fait du PFU, la base des revenus du capital au titre de l'impôt sur le revenu se rapproche de la base au titre des prélèvements sociaux,
                                d'où le fait qu'on utilise cette variable. En revanche, concernant les prêts participatifs, le montant au titre de l'impôt sur le revenu
                                forfaitaire est le montant net des pertes, alors que celui soumis au titre des prélèvements sociaux est le montant brut. Cependant,
                                la case 2TT contient le montant des intérêts de ces prêts après déduction de ces pertes. Donc, on est contraint de prendre un montant net.
        '''

        # Revenus du capital présents dans la section 2 de la déclaration de revenus
        revenus_capitaux_prelevement_bareme = foyer_fiscal('revenus_capitaux_prelevement_bareme', period, options = [ADD])
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])

        # Rentes viagères à titre onéreux
        rente_viagere_titre_onereux_net = foyer_fiscal('rente_viagere_titre_onereux_net', period)

        # Revenus des produits d'épargne logement
        interets_pel_cel_non_soumis_IR_i = foyer_fiscal.members('interets_pel_cel_non_soumis_IR', period)
        interets_pel_cel_non_soumis_IR = foyer_fiscal.sum(interets_pel_cel_non_soumis_IR_i)

        # Revenus fonciers
        rev_cat_rfon = foyer_fiscal('revenu_categoriel_foncier', period)

        # Plus-values
        assiette_csg_plus_values = foyer_fiscal('assiette_csg_plus_values', period)

        # produits d'assurance-vie exonérés d'impôt sur le revenu et de prélèvement forfaitaire libératoire (et donc non présents dans revenus_capitaux_prelevement_bareme et revenus_capitaux_prelevement_liberatoire)
        assurance_vie_ps_exoneree_irpp_pl = foyer_fiscal('assurance_vie_ps_exoneree_irpp_pl', period)

        # Gains de levée d'option assimilées salaires pour l'IR et soumis aux prélèvements sociaux des revenus du patrimoine
        f3vj_i = foyer_fiscal.members('f3vj', period)
        f3vj = foyer_fiscal.sum(f3vj_i)

        # Crédits d'impôt sur valeurs étrangères déduits de la base CSG
        credits_impot_sur_valeurs_etrangeres = foyer_fiscal('credits_impot_sur_valeurs_etrangeres', period)

        return max_(
            revenus_capitaux_prelevement_bareme
            + revenus_capitaux_prelevement_liberatoire
            + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + rente_viagere_titre_onereux_net
            + interets_pel_cel_non_soumis_IR
            + rev_cat_rfon
            + assiette_csg_plus_values
            + assurance_vie_ps_exoneree_irpp_pl
            + f3vj
            - credits_impot_sur_valeurs_etrangeres,
            0
            )


# 3. Variables de prélèvements sociaux sur les revenus du capital

class csg_glo_assimile_salaire_ir_et_ps(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "CSG sur GLO assimilés salaires pour les prélèvements sociaux, en plus de l'être pour l'IR (cases 1TT et similaires)"
    entity = Individu
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        f1tt = individu('f1tt', period)
        csg_activite = parameters(period).prelevements_sociaux.contributions_sociales.csg.activite
        taux = csg_activite.imposable.taux + csg_activite.deductible.taux
        return - f1tt * taux


class crds_glo_assimile_salaire_ir_et_ps(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = "CRDS sur GLO assimilés salaires pour les prélèvements sociaux, en plus de l'être pour l'IR (cases 1TT et similaires)"
    entity = Individu
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        f1tt = individu('f1tt', period)
        return - f1tt * (
            parameters(period).prelevements_sociaux.contributions_sociales.crds.taux
            )


class contribution_salariale_glo_assimile_salaire(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = 'Contribution salariale sur GLO'
    entity = FoyerFiscal
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Existe avant 2013, mais pas codé pour cette période antérieure.
        '''
        contribution = parameters(period).prelevements_sociaux.contributions_assises_specifiquement_accessoires_salaire.cont_sur_options
        f1tt_i = foyer_fiscal.members('f1tt', period)
        f1tt = foyer_fiscal.sum(f1tt_i)
        f3vn = foyer_fiscal('f3vn', period)
        return - (f1tt + f3vn) * contribution.salarie.taux_plein


class csg_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'CSG sur les revenus du capital'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        et il y a aussi un problème pour les années postérieures à 2017/2018
        '''
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        csg = parameters(period).taxation_capital.prelevements_sociaux.csg

        csg_glo_assimile_salaire_ir_et_ps_i = foyer_fiscal.members('csg_glo_assimile_salaire_ir_et_ps', period)
        csg_glo_assimile_salaire_ir_et_ps = foyer_fiscal.sum(csg_glo_assimile_salaire_ir_et_ps_i)

        # Pour les revenus du patrimoine, le changement de CSG se fait à partir des revenus de 2017,
        # mais le taux de CSG déductible se fait à partir des revenus 2018. Pour les revenus de placement le timing est différent,
        # et reste à être pris en compte ici : cf. II.B de l'art. 67 de loi 2017-1837 et 3° et 4° du V.A de l'art. 8 de loi 2017-1836
        return (
            - assiette_csg_revenus_capital * csg.taux_global.produits_de_placement
            + csg_glo_assimile_salaire_ir_et_ps
            )


class crds_revenus_capital(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = FoyerFiscal
    label = 'CRDS sur les revenus du capital'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux

        crds_glo_assimile_salaire_ir_et_ps_i = foyer_fiscal.members('crds_glo_assimile_salaire_ir_et_ps', period)
        crds_glo_assimile_salaire_ir_et_ps = foyer_fiscal.sum(crds_glo_assimile_salaire_ir_et_ps_i)

        return (
            - assiette_csg_revenus_capital * taux_crds
            + crds_glo_assimile_salaire_ir_et_ps
            )


class prelevements_sociaux_revenus_capital_hors_csg_crds(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prélèvements sociaux (hors CSG et CRDS) sur les revenus du capital'
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F2329'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        prelevements_sociaux = parameters(period).taxation_capital.prelevements_sociaux

        taux = (
            prelevements_sociaux.prelevement_social.produits_de_placement
            + prelevements_sociaux.caps.produits_de_placement
            )

        contribution_salariale_glo_assimile_salaire = foyer_fiscal('contribution_salariale_glo_assimile_salaire', period)

        return -assiette_csg_revenus_capital * taux + contribution_salariale_glo_assimile_salaire

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        prelevements_sociaux = parameters(period).taxation_capital.prelevements_sociaux

        taux = (
            prelevements_sociaux.prelevement_social.produits_de_placement
            + prelevements_sociaux.caps.produits_de_placement
            + prelevements_sociaux.caps.rsa
            )

        contribution_salariale_glo_assimile_salaire = foyer_fiscal('contribution_salariale_glo_assimile_salaire', period)

        return -assiette_csg_revenus_capital * taux + contribution_salariale_glo_assimile_salaire

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        prelevements_sociaux = parameters(period).taxation_capital.prelevements_sociaux

        taux = (
            prelevements_sociaux.prelevement_social.produits_de_placement
            + prelevements_sociaux.caps.produits_de_placement
            + prelevements_sociaux.prelevements_solidarite.produits_de_placement
            )

        contribution_salariale_glo_assimile_salaire = foyer_fiscal('contribution_salariale_glo_assimile_salaire', period)

        return -assiette_csg_revenus_capital * taux + contribution_salariale_glo_assimile_salaire

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        assiette_csg_revenus_capital = foyer_fiscal('assiette_csg_revenus_capital', period)
        taux = parameters(period).taxation_capital.prelevements_sociaux.prelevements_solidarite.produits_de_placement

        contribution_salariale_glo_assimile_salaire = foyer_fiscal('contribution_salariale_glo_assimile_salaire', period)

        return -assiette_csg_revenus_capital * taux + contribution_salariale_glo_assimile_salaire


class prelevements_sociaux_revenus_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prélèvements sociaux sur les revenus du capital'
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F2329'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Attention : Pour les années avant 2013, cette formule n'est pas entièrement correcte car le taux de la CSG n'était pas unique (distinction revenus du patrimoine et revenus de placement)
        '''
        csg_revenus_capital = foyer_fiscal('csg_revenus_capital', period)
        crds_revenus_capital = foyer_fiscal('crds_revenus_capital', period)
        prelevements_sociaux_revenus_capital_hors_csg_crds = foyer_fiscal('prelevements_sociaux_revenus_capital_hors_csg_crds', period)

        return csg_revenus_capital + crds_revenus_capital + prelevements_sociaux_revenus_capital_hors_csg_crds
