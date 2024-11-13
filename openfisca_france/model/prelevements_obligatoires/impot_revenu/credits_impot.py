import logging

from numpy import around, logical_or as or_

from openfisca_france.model.base import *

log = logging.getLogger(__name__)


# TODO : mettre à jour quaenv() et prlire()

class credits_impot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédits d'impôt pour l'impôt sur les revenus"
    definition_period = YEAR

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d'impôt pour l'impôt sur les revenus, prenant en compte
        le plafonnement des niches fiscales qui s'applique à la plupart
        des réductions et crédits d'impôts
        '''

        credits_plaf = [
            'ci_saldom',
            'ci_gardenf',
            'ci_investissement_forestier',

            # dans le doute:
            'aidper',
            'assloy',
            'autent',
            'creimp',
            'direpa',
            'drbail',
            'inthab',
            'preetu',
            'quaenv',
            ]

        credits_sans_plaf = [
            # dans le doute:
            'credit_cotisations_syndicales',
            ]

        P = parameters(period).impot_revenu.credits_impots.plaf_nich
        P2021 = parameters('2021-01-01').impot_revenu.credits_impots.plaf_nich

        # Get remainder of allowance for niches fiscales
        red_plaf = foyer_fiscal('reductions_plafonnees', period)
        red_plaf_om = foyer_fiscal('reductions_plafonnees_om_sofica', period)
        red_plaf_esus_sfs = foyer_fiscal('reductions_plafonnees_esus_sfs', period)
        impot_net = foyer_fiscal('ip_net', period)

        # prise en compte des possibles restitutions des CI lorsque les RI sont déjà plafonnées par le montant de l'impôt
        reductions_plafonnees_tot = min_(impot_net, red_plaf
            + max_(0, red_plaf_om - P.plafonnement_des_niches.majoration_om)
            + max_(0, red_plaf_esus_sfs - P2021.plafonnement_des_niches.majoration_esus_sfs))

        remaining_allowance = P.plafond - reductions_plafonnees_tot

        # credit available within the limit
        montants_plaf = sum([around(foyer_fiscal(credit, period)) for credit in credits_plaf])
        cred_plaf = min_(remaining_allowance, montants_plaf)

        # credit available without the ceiling
        cred_sans_plaf = sum([around(foyer_fiscal(credit, period)) for credit in credits_sans_plaf])

        return cred_plaf + cred_sans_plaf

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d'impôt pour l'impôt sur les revenus, prenant en compte
        le plafonnement des niches fiscales qui s'applique à la plupart
        des réductions et crédits d'impôts
        '''

        credits_plaf = [
            'ci_saldom',
            'ci_gardenf',
            'ci_investissement_forestier',

            # dans le doute:
            'aidper',
            'assloy',
            'autent',
            'creimp',
            'direpa',
            'drbail',
            'inthab',
            'preetu',
            'quaenv',
            ]

        credits_sans_plaf = [
            # dans le doute:
            'credit_cotisations_syndicales',
            ]

        P = parameters(period).impot_revenu.credits_impots.plaf_nich

        # Get remainder of allowance for niches fiscales
        red_plaf = foyer_fiscal('reductions_plafonnees', period)
        red_plaf_om = foyer_fiscal('reductions_plafonnees_om_sofica', period)
        impot_net = foyer_fiscal('ip_net', period)

        # prise en compte des possibles restitutions des CI lorsque les RI sont déjà plafonnées par le montant de l'impôt
        reductions_plafonnees_tot = min_(impot_net, red_plaf
            + max_(0, red_plaf_om - P.plafonnement_des_niches.majoration_om))

        remaining_allowance = P.plafond - reductions_plafonnees_tot

        # credit available within the limit
        montants_plaf = sum([around(foyer_fiscal(credit, period)) for credit in credits_plaf])
        cred_plaf = min_(remaining_allowance, montants_plaf)

        # credit available without the ceiling
        cred_sans_plaf = sum([around(foyer_fiscal(credit, period)) for credit in credits_sans_plaf])

        return cred_plaf + cred_sans_plaf

    def formula(foyer_fiscal, period, parameters):
        '''
        Crédits d'impôt pour l'impôt sur les revenus
        Ancienne formule, pas vérifié si correcte pour toutes les années jusqu'à la nouvelle formule
        '''
        credits = [
            # Depuis 2002
            'acqgpl',
            'aidper',
            'creimp',
            'drbail',
            'prlire',
            # Depuis 2005
            'ci_gardenf',
            'aidmob',
            'assloy',
            'divide',
            'direpa',
            'drbail',
            'jeunes',
            'preetu',
            'quaenv',
            # Depuis 2007
            'inthab',
            'ci_saldom',
            # Depuis 2008
            'creimp_exc_2008',
            # Depuis 2009
            'autent',
            # Depuis 2010
            'percvm',
            # Depuis 2012
            'credit_cotisations_syndicales'
            ]

        montants = [around(foyer_fiscal(credit, period)) for credit in credits]
        total_credits = sum(montants)

        return total_credits


class nb_pac2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Nombre de personnes à charges (en comptant les enfants en résidence alternée comme une demi personne à charge)'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbF = foyer_fiscal('nbF', period)
        nbJ = foyer_fiscal('nbJ', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbH = foyer_fiscal('nbH', period)

        return nbF + nbJ + nbpac_invalideR - nbH / 2


class ci_investissement_forestier(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt au titre des investissements forestiers"
    definition_period = YEAR

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2014
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2015
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7ux = foyer_fiscal('f7ux_2018', period)
        f7tj = foyer_fiscal('f7tj', period)
        f7vp = foyer_fiscal('f7vp', period)
        f7tk = foyer_fiscal('f7tk', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7vp + f7tk)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7ux + f7tj)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7ux = foyer_fiscal('f7ux_2018', period)
        f7tj = foyer_fiscal('f7tj', period)
        f7vp = foyer_fiscal('f7vp', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7vm = foyer_fiscal('f7vm', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7to = foyer_fiscal('f7to', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7vp + f7tk + f7vn + f7to)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7ux + f7tj + f7vm + f7tm)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7ux = foyer_fiscal('f7ux_2018', period)
        f7tj = foyer_fiscal('f7tj', period)
        f7vp = foyer_fiscal('f7vp', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7vm = foyer_fiscal('f7vm', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7to = foyer_fiscal('f7to', period)
        f7vq = foyer_fiscal('f7vq', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7vr = foyer_fiscal('f7vr', period)
        f7tq = foyer_fiscal('f7tq', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7vp + f7tk + f7vn + f7to + f7vr + f7tq)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7ux + f7tj + f7vm + f7tm + f7vq + f7tp)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2018
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7ux = foyer_fiscal('f7ux_2018', period)
        f7tj = foyer_fiscal('f7tj', period)
        f7vp = foyer_fiscal('f7vp', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7vm = foyer_fiscal('f7vm', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7to = foyer_fiscal('f7to', period)
        f7vq = foyer_fiscal('f7vq', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7vr = foyer_fiscal('f7vr', period)
        f7tq = foyer_fiscal('f7tq', period)
        f7vs = foyer_fiscal('f7vs', period)
        f7tr = foyer_fiscal('f7tr', period)
        f7vl = foyer_fiscal('f7vl', period)
        f7ts = foyer_fiscal('f7ts', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7vp + f7tk + f7vn + f7to + f7vr + f7tq + f7vl + f7ts)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7ux + f7tj + f7vm + f7tm + f7vq + f7tp + f7vs + f7tr)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7tj = foyer_fiscal('f7tj', period)
        f7tk = foyer_fiscal('f7tk', period)

        f7vm = foyer_fiscal('f7vm', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7to = foyer_fiscal('f7to', period)
        f7vq = foyer_fiscal('f7vq', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7vr = foyer_fiscal('f7vr', period)
        f7tq = foyer_fiscal('f7tq', period)
        f7vs = foyer_fiscal('f7vs', period)
        f7tr = foyer_fiscal('f7tr', period)
        f7vl = foyer_fiscal('f7vl', period)
        f7ts = foyer_fiscal('f7ts', period)
        f7vj = foyer_fiscal('f7vj', period)
        f7tt = foyer_fiscal('f7tt', period)
        f7vk = foyer_fiscal('f7vk', period)
        f7tu = foyer_fiscal('f7tu', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7tk + f7vn + f7to + f7vr + f7tq + f7vl + f7ts + f7vk + f7tu)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7tj + f7vm + f7tm + f7vq + f7tp + f7vs + f7tr + f7vj + f7tt)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2020
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7tj = foyer_fiscal('f7tj', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7to = foyer_fiscal('f7to', period)
        f7vq = foyer_fiscal('f7vq', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7vr = foyer_fiscal('f7vr', period)
        f7tq = foyer_fiscal('f7tq', period)
        f7vs = foyer_fiscal('f7vs', period)
        f7tr = foyer_fiscal('f7tr', period)
        f7vl = foyer_fiscal('f7vl', period)
        f7ts = foyer_fiscal('f7ts', period)
        f7vj = foyer_fiscal('f7vj', period)
        f7tt = foyer_fiscal('f7tt', period)
        f7vk = foyer_fiscal('f7vk', period)
        f7tu = foyer_fiscal('f7tu', period)
        f7vh = foyer_fiscal('f7vh', period)
        f7tv = foyer_fiscal('f7tv', period)
        f7vi = foyer_fiscal('f7vi', period)
        f7tw = foyer_fiscal('f7tw', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7tk + f7to + f7vr + f7tq + f7vl + f7ts + f7vk + f7tu + f7vi + f7tw)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7tj + f7tm + f7vq + f7tp + f7vs + f7tr + f7vj + f7tt + f7vh + f7tv)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2021
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7tj = foyer_fiscal('f7tj', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7to = foyer_fiscal('f7to', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7tq = foyer_fiscal('f7tq', period)
        f7vs = foyer_fiscal('f7vs', period)
        f7tr = foyer_fiscal('f7tr', period)
        f7vl = foyer_fiscal('f7vl', period)
        f7ts = foyer_fiscal('f7ts', period)
        f7vj = foyer_fiscal('f7vj', period)
        f7tt = foyer_fiscal('f7tt', period)
        f7vk = foyer_fiscal('f7vk', period)
        f7tu = foyer_fiscal('f7tu', period)
        f7vh = foyer_fiscal('f7vh', period)
        f7tv = foyer_fiscal('f7tv', period)
        f7vi = foyer_fiscal('f7vi', period)
        f7tw = foyer_fiscal('f7tw', period)
        f7vm = foyer_fiscal('f7vm', period)
        f7ta = foyer_fiscal('f7ta', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7tb = foyer_fiscal('f7tb', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7tk + f7to + f7tq + f7vl + f7ts + f7vk + f7tu + f7vi + f7tw + f7vn + f7tb)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7tj + f7tm + f7tp + f7vs + f7tr + f7vj + f7tt + f7vh + f7tv + f7vm + f7ta)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot

    def formula_2023_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2023
        '''
        # À compter de 2023, le crédit d'impôt au titre de la rémunération versée pour la réalisation d'un contrat conclu pour la gestion de bois et forêts (DEFI « Contrat ») est abrogé, d'où le retrait de la formule du paramètre plafond_cga. Par ailleurs, le paramètre taux_adhesion_org_producteurs est retiré également car la formule change, pour les cotisations versées à un assureur (DEFI « Assurance »), le plafond de dépenses éligibles à l’hectare est porté de 6 € à 15 € ;

        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7up = foyer_fiscal('f7up', period)
        f7ut = foyer_fiscal('f7ut', period)

        f7ua = foyer_fiscal('f7ua', period)
        f7ub = foyer_fiscal('f7ub', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7ui = foyer_fiscal('f7ui', period)

        f7tj = foyer_fiscal('f7tj', period)
        f7tk = foyer_fiscal('f7tk', period)
        f7tm = foyer_fiscal('f7tm', period)
        f7to = foyer_fiscal('f7to', period)
        f7tp = foyer_fiscal('f7tp', period)
        f7tq = foyer_fiscal('f7tq', period)
        f7vs = foyer_fiscal('f7vs', period)
        f7tr = foyer_fiscal('f7tr', period)
        f7vl = foyer_fiscal('f7vl', period)
        f7ts = foyer_fiscal('f7ts', period)
        f7vj = foyer_fiscal('f7vj', period)
        f7tt = foyer_fiscal('f7tt', period)
        f7vk = foyer_fiscal('f7vk', period)
        f7tu = foyer_fiscal('f7tu', period)
        f7vh = foyer_fiscal('f7vh', period)
        f7tv = foyer_fiscal('f7tv', period)
        f7vi = foyer_fiscal('f7vi', period)
        f7tw = foyer_fiscal('f7tw', period)
        f7vm = foyer_fiscal('f7vm', period)
        f7ta = foyer_fiscal('f7ta', period)
        f7vn = foyer_fiscal('f7vn', period)
        f7tb = foyer_fiscal('f7tb', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # travaux année N
        ci_trav_adh = min_(P.travaux.plafond * (maries_ou_pacses + 1), f7ua + f7ub + f7tk + f7to + f7tq + f7vl + f7ts + f7vk + f7tu + f7vi + f7tw + f7vn + f7tb)
        ci_trav = min_(P.travaux.plafond * (maries_ou_pacses + 1) - ci_trav_adh, f7up + f7ut + f7tj + f7tm + f7tp + f7vs + f7tr + f7vj + f7tt + f7vh + f7tv + f7vm + f7ta)

        ci_travaux = P.travaux.taux_adhesion_org_producteurs * ci_trav_adh + P.travaux.taux * ci_trav

        # contrat de gestion
        ci_cg_adh = min_(P.plafond_cga * (maries_ou_pacses + 1), f7ui)
        ci_cg = min_(P.plafond_cga * (maries_ou_pacses + 1) - ci_cg_adh, f7uq)

        ci_cg_tot = P.travaux.taux_adhesion_org_producteurs * ci_cg_adh + P.travaux.taux * ci_cg

        return ci_travaux + ci_cg_tot



class acqgpl(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte"
    end = '2007-12-31'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
        2002-2007
        '''
        f7up = foyer_fiscal('f7up_2007', period)
        f7uq = foyer_fiscal('f7uq_2007', period)
        acqgpl = parameters(period).impot_revenu.credits_impots.acqgpl

        return f7up * acqgpl.mont_up + f7uq * acqgpl.mont_uq


class aidmob(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt aide à la mobilité"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt aide à la mobilité
        2005-2008
        '''
        f1ar = foyer_fiscal('f1ar', period)
        f1br = foyer_fiscal('f1br', period)
        f1cr = foyer_fiscal('f1cr', period)
        f1dr = foyer_fiscal('f1dr', period)
        f1er = foyer_fiscal('f1er', period)
        montant = parameters(period).impot_revenu.credits_impots.aidmob.montant

        return (f1ar + f1br + f1cr + f1dr + f1er) * montant


class aidper(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédits d’impôt pour dépenses d’équipement de l’habitation principale en faveur de l’aide aux personnes'
    reference = 'http://bofip.impots.gouv.fr/bofip/3859-PGP'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        nbH = foyer_fiscal('nbH', period)
        f7wi_2009 = foyer_fiscal('f7wi_2009', period)
        f7wj = foyer_fiscal('f7wj', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf = P_aide_pers.plafond.plafond_commun

        nb_pac_non_alternes = nb_pac_majoration_plafond - nbH / 2

        # S'il y a des PAC en résidence alternée, ils sont décomptés en premier
        max0 = (
            P_plaf.celib * (maries_ou_pacses == 0)
            + P_plaf.couple * (maries_ou_pacses == 1)
            + (
                P_plaf.maj_pac1 * (nbH >= 1)
                + P_plaf.maj_pac2 * (nbH >= 2)
                + P_plaf.maj_pac3 * max_(nbH - 2, 0)
                ) / 2
            + (nbH >= 2) * P_plaf.maj_pac3 * nb_pac_non_alternes
            + (nbH == 1) * (P_plaf.maj_pac2 * (nb_pac_non_alternes >= 1) + P_plaf.maj_pac3 * max_(nb_pac_non_alternes - 1, 0))
            + (nbH == 0) * (P_plaf.maj_pac1 + (nb_pac_non_alternes >= 1) + P_plaf.maj_pac2 * (nb_pac_non_alternes >= 2) + P_plaf.maj_pac3 * max_(nb_pac_non_alternes - 2, 0))
            )

        max1 = max_(0, max0 - f7wj)
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max0)
            + P_aide_pers.taux.taux_risques_techno_ascenseurs * min_(f7wi_2009, max1)
            )

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wi_2009 = foyer_fiscal('f7wi_2009', period)
        f7wj = foyer_fiscal('f7wj', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf = P_aide_pers.plafond.plafond_commun

        max0 = P_plaf.celib * (maries_ou_pacses == 0) + P_plaf.couple * (maries_ou_pacses == 1) + P_plaf.maj_pac * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max0)
            + P_aide_pers.taux.taux_risques_techno_ascenseurs * min_(f7wi_2009, max1)
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wi_2012 = foyer_fiscal('f7wi_2012', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7sf_2011 = foyer_fiscal('f7sf_2011', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf = P_aide_pers.plafond.plafond_commun

        # Les plafonds sont appliqués par contribuable et habitation. Ici, on suppose que 7wl, 7wj et 7wi d'une part et 7sf d'autre part sont associés à deux habitations distinctes : 7wl, 7wj et 7wi sont associées à l'habitation principale tandis que 7sf est associée aux logements donnés à la location.
        max0 = P_plaf.celib * (maries_ou_pacses == 0) + P_plaf.couple * (maries_ou_pacses == 1) + P_plaf.maj_pac * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wl)
        max2 = max_(0, max1 - f7wj)
        return (
            P_aide_pers.taux.taux_risques_techno * min_(f7wl, max0)
            + P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max1)
            + P_aide_pers.taux.taux_ascenseurs * min_(f7wi_2012, max2)
            + P_aide_pers.taux.taux_risques_techno * min_(f7sf_2011, max0)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wi_2012 = foyer_fiscal('f7wi_2012', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf_commun = P_aide_pers.plafond.plafond_commun
        P_plaf_maj = P_aide_pers.plafond.maj_plaf_risques_techno_avant_2015

        # Les plafonds sont appliqués par contribuable et habitation. Ici, on suppose que 7wl, 7wj et 7wi d'une part et 7wr d'autre part sont associés à deux habitations distinctes : 7wl, 7wj et 7wi sont associées à l'habitation principale tandis que 7wr est associée aux logements donnés à la location.
        max0 = P_plaf_commun.celib * (maries_ou_pacses == 0) + P_plaf_commun.couple * (maries_ou_pacses == 1) + P_plaf_commun.maj_pac * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)
        max2 = max_(0, max1 - f7wi_2012)
        max_maj = P_plaf_maj.celib * (maries_ou_pacses == 0) + P_plaf_maj.couple * (maries_ou_pacses == 1)
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max0)
            + P_aide_pers.taux.taux_ascenseurs * min_(f7wi_2012, max1)
            + P_aide_pers.taux.taux_risques_techno * (min_(f7wl, max2) + min_(max_(0, f7wl - max2), max_maj))
            + P_aide_pers.taux.taux_risques_techno * min_(f7wr, max0 + max_maj)
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf_commun = P_aide_pers.plafond.plafond_commun
        P_plaf_maj = P_aide_pers.plafond.maj_plaf_risques_techno_avant_2015

        # Les plafonds sont appliqués par contribuable et habitation. Ici, on suppose que 7wl, 7wj et 7wi d'une part et 7wr d'autre part sont associés à deux habitations distinctes : 7wl, 7wj et 7wi sont associées à l'habitation principale tandis que 7wr est associée aux logements donnés à la location.
        max0 = P_plaf_commun.celib * (maries_ou_pacses == 0) + P_plaf_commun.couple * (maries_ou_pacses == 1) + P_plaf_commun.maj_pac * nb_pac_majoration_plafond
        max1 = max_(0, max0 - f7wj)
        max_maj = P_plaf_maj.celib * (maries_ou_pacses == 0) + P_plaf_maj.couple * (maries_ou_pacses == 1)
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max0)
            + P_aide_pers.taux.taux_risques_techno * (min_(f7wl, max1) + min_(max_(0, f7wl - max1), max_maj))
            + P_aide_pers.taux.taux_risques_techno * min_(f7wr, max0 + max_maj)
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf_commun = P_aide_pers.plafond.plafond_commun

        # Les plafonds sont appliqués par contribuable et habitation. Ici, on suppose que 7wl, 7wj et 7wi d'une part et 7wr d'autre part sont associés à deux habitations distinctes : 7wl, 7wj et 7wi sont associées à l'habitation principale tandis que 7wr est associée aux logements donnés à la location.
        max_hors_risques_techno = P_plaf_commun.celib * (maries_ou_pacses == 0) + P_plaf_commun.couple * (maries_ou_pacses == 1) + P_plaf_commun.maj_pac * nb_pac_majoration_plafond
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wj, max_hors_risques_techno)
            + P_aide_pers.taux.taux_risques_techno * min_(f7wl, P_aide_pers.plafond.plafond_risque_techno_apres_2015)
            + P_aide_pers.taux.taux_risques_techno * min_(f7wr, P_aide_pers.plafond.plafond_risque_techno_apres_2015)
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wi = foyer_fiscal('f7wi', period)
        f7wj = foyer_fiscal('f7wj', period)
        f7wl = foyer_fiscal('f7wl', period)
        f7wr = foyer_fiscal('f7wr', period)
        P_aide_pers = parameters(period).impot_revenu.credits_impots.equ_hab_princ_aide_personnes
        P_plaf_commun = P_aide_pers.plafond.plafond_commun

        # Les plafonds sont appliqués par contribuable et habitation. Ici, on suppose que 7wl, 7wj et 7wi d'une part et 7wr d'autre part sont associés à deux habitations distinctes : 7wl, 7wj et 7wi sont associées à l'habitation principale tandis que 7wr est associée aux logements donnés à la location.
        max_hors_risques_techno = P_plaf_commun.celib * (maries_ou_pacses == 0) + P_plaf_commun.couple * (maries_ou_pacses == 1) + P_plaf_commun.maj_pac * nb_pac_majoration_plafond
        return (
            P_aide_pers.taux.taux_equ_pers_agees_hand * min_(f7wi + f7wj, max_hors_risques_techno)
            + P_aide_pers.taux.taux_risques_techno * min_(f7wl, P_aide_pers.plafond.plafond_risque_techno_apres_2015)
            + P_aide_pers.taux.taux_risques_techno * min_(f7wr, P_aide_pers.plafond.plafond_risque_techno_apres_2015)
            )


class assloy(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt primes d’assurance pour loyers impayés'
    reference = 'http://bofip.impots.gouv.fr/bofip/844-PGP.html?identifiant=BOI-IR-RICI-320-20120912'
    definition_period = YEAR
    end = '2016-12-31'

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
        2005-2016
        '''
        f4bf = foyer_fiscal('f4bf', period)
        P = parameters(period).impot_revenu.credits_impots.assloy

        return P.taux * f4bf


class autent(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'autent'
    definition_period = YEAR

    def formula_2009(foyer_fiscal, period, parameters):
        '''
        Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
        2009-
        '''
        f8uy = foyer_fiscal('f8uy', period)

        return f8uy


class ci_gardenf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Frais de garde des enfants à l’extérieur du domicile'
    reference = 'http://bofip.impots.gouv.fr/bofip/865-PGP?datePubl=13/04/2013'
    definition_period = YEAR

    def formula_2005(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
        2005-
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        f7ge = foyer_fiscal('f7ge', period)
        f7gf = foyer_fiscal('f7gf', period)
        f7gg = foyer_fiscal('f7gg', period)
        P = parameters(period).impot_revenu.credits_impots.gardenf

        max1 = P.plafond
        return P.taux * (
            min_(f7ga, max1)
            + min_(f7gb, max1)
            + min_(f7gc, max1)
            + min_(f7ge, max1 / 2)
            + min_(f7gf, max1 / 2)
            + min_(f7gg, max1 / 2)
            )


class credit_cotisations_syndicales(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt pour cotisations syndicales"
    reference = 'http://bofip.impots.gouv.fr/bofip/1605-PGP'
    definition_period = YEAR

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Cotisations syndicales : réduction d'impôt (2002-2011) puis crédit d'impôt (2012- )
        '''
        f7ac = foyer_fiscal.members('f7ac', period)

        cotisations_versees = f7ac

        salaire_imposable = foyer_fiscal.members('salaire_imposable', period, options = [ADD])
        chomage_imposable = foyer_fiscal.members('chomage_imposable', period, options = [ADD])
        retraite_imposable = foyer_fiscal.members('retraite_imposable', period, options = [ADD])

        cotisations_syndicales = parameters(period).impot_revenu.credits_impots.cotisations_syndicales

        plafond = (salaire_imposable + chomage_imposable + retraite_imposable) * cotisations_syndicales.plafond

        return (cotisations_syndicales.taux * foyer_fiscal.sum(min_(cotisations_versees, plafond)))


class creimp_exc_2008(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt exceptionnel sur les revenus 2008"
    definition_period = YEAR
    end = '2008-12-31'

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt exceptionnel sur les revenus 2008
        http://www11.minefi.gouv.fr/boi/boi2009/5fppub/textes/5b2509/5b2509.pdf
        '''
        rni = foyer_fiscal('rni', period)
        nbptr = foyer_fiscal('nbptr', period)
        iai = foyer_fiscal('iai', period)
        mohist = foyer_fiscal('mohist', period)
        elig_creimp_exc_2008 = foyer_fiscal('elig_creimp_exc_2008', period)

        # TODO: gérer les DOM-TOM, corriger les formules, inclure 7KA
        rpp = rni / nbptr

        return (
            elig_creimp_exc_2008
            * (mohist < 10700)
            * (rpp <= 12475)
            * around(
                (2 / 3)
                * min_(12475, iai)
                * (rpp < 11674)
                + (rpp > 11673)
                * max_(0, 8317 * (12475 - rpp) / 802)
                )
            )


class creimp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Ensemble de crédits d'impôt"
    definition_period = YEAR
    # TODO: ajouter le crédit d'impôt sur impôts imposés à l'étranger, aux cases 5AK, 5AL, 5DF, 5DG, 5UR, 5US, 5EY, 5EZ, 5XJ, 5XK, 5XS, 5XX, 4BL et 4BK

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8to - f8tp)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)

        return (f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8td_2002_2005 = foyer_fiscal('f8td_2002_2005', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8we = foyer_fiscal('f8we', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8td_2002_2005 + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa
            + f8wb + f8wc + f8we
            )

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc
            + f8wd + f8we + f8wr + f8ws + f8wt + f8wu
            )

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc
            + f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx
            )

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wc
            + f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx
            )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8ws = foyer_fiscal('f8ws', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)
        f8wx = foyer_fiscal('f8wx', period)

        return (
            f2ab + f8ta + f8tb + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd
            + f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tz + f8uz + f8wa + f8wb + f8wd
            + f8we + f8wr + f8wt + f8wu + f8wv
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)
        f8wv = foyer_fiscal('f8wv', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8ts + f8tz + f8uz + f8wa + f8wb
            + f8wc + f8wd + f8we + f8wr + f8wt + f8wu + f8wv
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tl + f8ts + f8tz + f8uw
            + f8uz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8wt + f8wu
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8to - f8tp + f8tl + f8ts + f8tz + f8uw
            + f8uz + f8vm + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8wt + f8wu + f8vl
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wb = foyer_fiscal('f8wb', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8we = foyer_fiscal('f8we', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab + f8ta + f8tb + f8tc
            + f8te - f8tf + f8tg + f8to - f8tp
            + f8tl + f8ts + f8tz + f8uw + f8uz
            + f8vm + f8wa + f8wb + f8wc + f8wd
            + f8we + f8wr + f8wt + f8wu + f8vl
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8te = foyer_fiscal('f8te_2018', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab + f8ta + f8tb + f8tc
            + f8te - f8tf + f8tg + f8to - f8tp
            + f8tl + f8ts + f8tz + f8uw + f8uz
            + f8vm + f8wa + f8wc + f8wd
            + f8wr + f8wt + f8wu + f8vl
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8tz = foyer_fiscal('f8tz', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8wu = foyer_fiscal('f8wu', period)

        # 8VM, 8WM, 8UM all in one (ind.-level) case? Why/how?
        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        # Alternatively, but need to check cases first:
        # f8vm = (foyer_fiscal('f8vm', period)
        #     + foyer_fiscal('f8wm', period)
        #     + foyer_fiscal('f8um', period))

        return (
            f2ab + f8ta + f8tb + f8tc
            - f8tf + f8tg + f8to - f8tp
            + f8tl + f8ts + f8tz + f8uw + f8uz
            + f8vm + f8wa + f8wc + f8wd
            + f8wr + f8wt + f8wu + f8vl
            )

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8te = foyer_fiscal('f8te', period)
        f8la = foyer_fiscal('f8la', period)

        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab + f8ta + f8tb + f8tc
            - f8tf + f8tg + f8to - f8tp
            + f8tl + f8ts + f8uw + f8uz
            + f8vm + f8wa + f8wc + f8wd
            + f8wr + f8wt + f8vl + f8te + f8la
            )

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)
        f8ta = foyer_fiscal('f8ta', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tc = foyer_fiscal('f8tc', period)
        f8tf = foyer_fiscal('f8tf', period)
        f8tg = foyer_fiscal('f8tg', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8to = foyer_fiscal('f8to', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8ts = foyer_fiscal('f8ts', period)
        f8uw = foyer_fiscal('f8uw', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8vl = foyer_fiscal('f8vl', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wt = foyer_fiscal('f8wt', period)
        f8te = foyer_fiscal('f8te', period)
        f8la = foyer_fiscal('f8la', period)
        f8wg = foyer_fiscal('f8wg', period)
        f8wh = foyer_fiscal('f8wh', period)

        f8vm_i = foyer_fiscal.members('f8vm', period)
        f8vm = foyer_fiscal.sum(f8vm_i)

        return (
            f2ab + f8ta + f8tb + f8tc
            - f8tf + f8tg + f8to - f8tp
            + f8tl + f8ts + f8uw + f8uz
            + f8vm + f8wa + f8wc + f8wd
            + f8wr + f8wt + f8vl + f8te
            + f8la + f8wg + f8wh
            )


class acompte_ir_elus_locaux(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Acompte d'impôt associé au prélèvement à la source des indemnités des élus locaux"
    definition_period = YEAR
    end = '2017-12-31'  # On neutralise cette variable à partir de 2018 car cette variable n'est pas un montant de revenu, mais un montant d'impôt, versé en acompte. Or, pour le moment, à partir de 2018, on ne dispose pas de cet acompte.

    def formula(foyer_fiscal, period):
        '''
        Si un élu local a été prélevé à la source de l'impôt associé à ses indemnités
        et qu'il décide au final d'être imposé comme au titre des salaires et traitements,
        son impôt est calculé après déclaration 2042 des revenus, mais est diminué de l'acompte correspondant au montant déjà prélevé à la source
        Cf. document 2041 GI. Pour l'année 2016 :
        https://www.impots.gouv.fr/portail/files/formulaires/2041-gi/2017/2041-gi_1936.pdf
        '''
        f8th = foyer_fiscal('f8th', period)

        return f8th


class prelevement_forfaitaire_non_liberatoire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prélèvement forfaitaire non libératoire sur les revenus du capital'
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period):
        '''
        A partir des revenus de 2013, certains revenus du capital qui pouvaient
        profiter du prélèvement forfaitaire libératoire sont passés à l'imposition obligatoire au barème.
        Mais un prélèvement forfaitaire demeure à partir de 2013, pour éviter les trous de trésorerie
        (car un prélèvement forfaitaire est à la source). Ce prélèvement est non-libératoire : il
        correspond à un acompte d'impot_revenu_restant_a_payer, qui est donc déduit de l'impôt dû au moment du calcul de
        l'impôt final après déclaration des revenus
        '''
        f2ck = foyer_fiscal('f2ck', period)

        return f2ck


class acomptes_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Ensemble des acomptes de l'IR"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period):
        '''
        Acomptes d'impôt sur le revenu pris en compte dans le calcul de l'impôt final.
        On déduit de l'impôt final ces acomptes. Si les acomptes dépassent l'impôt final,
        l'excédent est restitué.
        La variable impot_revenu_restant_a_payer correspond à l'impôt après prise en compte de cette déduction
        '''

        acompte_ir_elus_locaux = foyer_fiscal('acompte_ir_elus_locaux', period)
        prelevement_forfaitaire_non_liberatoire = foyer_fiscal('prelevement_forfaitaire_non_liberatoire', period)
        prlire = foyer_fiscal('prlire', period)

        return acompte_ir_elus_locaux + prelevement_forfaitaire_non_liberatoire + prlire


class direpa(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt directive « épargne »'
    definition_period = YEAR
    end = '2017-12-31'

    def formula_2006(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt directive « épargne » (case 2BG)
        2006-2017
        '''
        f2bg = foyer_fiscal('f2bg', period)

        return f2bg


class divide(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt dividendes"
    end = '2009-12-31'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d'impôt dividendes
        2005-2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2gr = foyer_fiscal('f2gr', period)
        credits_impots_divide = parameters(period).impot_revenu.credits_impots.divide
        revenus_capitaux_mobiliers_dividendes_taux = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm.revenus_capitaux_mobiliers_dividendes

        max1 = credits_impots_divide.plafond * (maries_ou_pacses + 1)
        return min_(revenus_capitaux_mobiliers_dividendes_taux.taux_abattement * (f2dc + f2gr), max1)


class drbail(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt représentatif de la taxe additionnelle au droit de bail'
    definition_period = YEAR
    end = '2017-12-31'

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
        2002-2017
        '''
        f4tq = foyer_fiscal('f4tq', period)
        P = parameters(period).impot_revenu.credits_impots.drbail

        return P.taux * f4tq


class inthab(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt intérêts des emprunts pour l’habitation principale'
    reference = 'http://bofip.impots.gouv.fr/bofip/3863-PGP.html?identifiant=BOI-IR-RICI-350-20120912'
    definition_period = YEAR

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7UH)
        2007
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        f7uh = foyer_fiscal('f7uh_2007', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        return interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(max0, f7uh)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        max1 = max_(max0 - f7vy, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vy, max0)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vz, max1)
            )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VX, 7VY et 7VZ)
        2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vy, max1)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vz, max2)
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vy, max1)
            + interets_emprunt_habitation_principale.logements_2010.taux_applique_premiere_annuite_remboursement * min_(f7vw, max2)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vz, max3)
            )

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        f7vu = foyer_fiscal('f7vu', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vy, max1)
            + interets_emprunt_habitation_principale.logements_2010.taux_applique_premiere_annuite_remboursement * min_(f7vw, max2)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vu, max3)
            + interets_emprunt_habitation_principale.cas_base.taux_2 * min_(f7vz, max4)
            + interets_emprunt_habitation_principale.logements_2010.taux_2 * min_(f7vv, max5)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2012 - 2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vu = foyer_fiscal('f7vu', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vw = foyer_fiscal('f7vw', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vy = foyer_fiscal('f7vy', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge

        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vy, 0)
        max3 = max_(max2 - f7vw, 0)
        max4 = max_(max3 - f7vu, 0)
        max5 = max_(max4 - f7vz, 0)
        max6 = max_(max5 - f7vv, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vy, max1)
            + interets_emprunt_habitation_principale.logements_2010.taux_applique_premiere_annuite_remboursement * min_(f7vw, max2)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vu, max3)
            + interets_emprunt_habitation_principale.cas_base.taux_2 * min_(f7vz, max4)
            + interets_emprunt_habitation_principale.logements_2010.taux_2 * min_(f7vv, max5)
            + interets_emprunt_habitation_principale.logements_2011.taux_2 * min_(f7vt, max6)
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2014
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vu = foyer_fiscal('f7vu', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vu, 0)
        max3 = max_(max2 - f7vz, 0)
        max4 = max_(max3 - f7vv, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.logements_2011.taux_applique_premiere_annuite_remboursement * min_(f7vu, max1)
            + interets_emprunt_habitation_principale.cas_base.taux_2 * min_(f7vz, max2)
            + interets_emprunt_habitation_principale.logements_2010.taux_2 * min_(f7vv, max3)
            + interets_emprunt_habitation_principale.logements_2011.taux_2 * min_(f7vt, max4)
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2015
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vz, 0)
        max3 = max_(max2 - f7vv, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_2 * min_(f7vz, max1)
            + interets_emprunt_habitation_principale.logements_2010.taux_2 * min_(f7vv, max2)
            + interets_emprunt_habitation_principale.logements_2011.taux_2 * min_(f7vt, max3)
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
        2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vx = foyer_fiscal('f7vx', period)
        f7vz = foyer_fiscal('f7vz', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vz, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.cas_base.taux_2 * min_(f7vz, max1)
            + interets_emprunt_habitation_principale.logements_2011.taux_2 * min_(f7vt, max2)
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale
        2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vt = foyer_fiscal('f7vt', period)
        f7vv = foyer_fiscal('f7vv', period)
        f7vx = foyer_fiscal('f7vx', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        # NB : max0 = plafond initial du montant d'intérêts retenus pour calculer le crédit
        #      max1..max4 = plafonds après imputations successives (dans l'ordre décrit dans la législation) des intérêts éligibles au crédit d'impôt
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge
        max1 = max_(max0 - f7vx, 0)
        max2 = max_(max1 - f7vv, 0)

        return (
            interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)
            + interets_emprunt_habitation_principale.logements_2010.taux_2 * min_(f7vv, max1)
            + interets_emprunt_habitation_principale.logements_2011.taux_2 * min_(f7vt, max2)
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt intérêts des emprunts pour l’habitation principale
        2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        invalidite_decl = foyer_fiscal('caseP', period)
        invalidite_conj = foyer_fiscal('caseF', period)
        nbpac_invalideG = foyer_fiscal('nbG', period)
        nbpac_invalideR = foyer_fiscal('nbR', period)
        nbpac_invalideI = foyer_fiscal('nbI', period)
        f7vx = foyer_fiscal('f7vx', period)
        interets_emprunt_habitation_principale = parameters(period).impot_revenu.credits_impots.interets_emprunt_habitation_principale

        invalide = invalidite_decl | invalidite_conj | (nbpac_invalideG != 0) | (nbpac_invalideR != 0) | (nbpac_invalideI != 0)
        max0 = interets_emprunt_habitation_principale.plafond_base * (maries_ou_pacses + 1) * (1 + invalide) + nb_pac_majoration_plafond * interets_emprunt_habitation_principale.majoration_plafond_par_enfant_charge

        return interets_emprunt_habitation_principale.cas_base.taux_applique_premiere_annuite_remboursement * min_(f7vx, max0)


class jeunes(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'jeunes'
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        jeunes_ind_i = foyer_fiscal.members('jeunes_ind', period)

        return foyer_fiscal.sum(jeunes_ind_i)


class jeunes_ind(Variable):
    value_type = float
    entity = Individu
    label = "Crédit d'impôt en faveur des jeunes"
    end = '2008-12-31'
    definition_period = YEAR

    def formula_2005_01_01(individu, period, parameters):
        '''
        Crédit d'impôt en faveur des jeunes
        2005-2008

        rfr de l'année où jeune de moins de 26 à travaillé six mois
        cf. http://www3.finances.gouv.fr/calcul_impot/2009/pdf/form-2041-GY.pdf
        Attention seuls certains
        '''
        janvier = period.first_month
        age = individu('age', janvier)
        salaire_imposable = individu('salaire_imposable', period, options = [ADD])
        elig_creimp_jeunes = individu('elig_creimp_jeunes', period)
        P = parameters(period).impot_revenu.credits_impots.jeunes

        # TODO: vérifier si les jeunes sous le foyer fiscal de leurs parents sont éligibles

        rfr = individu.foyer_fiscal('rfr', period)
        nbptr = individu.foyer_fiscal('nbptr', period)
        maries_ou_pacses = individu.foyer_fiscal('maries_ou_pacses', period)

        elig = (age < P.age) * (
            rfr
            < P.rfr_plaf
            * (maries_ou_pacses * P.rfr_mult + not_(maries_ou_pacses))
            + max_(0, nbptr - 2)
            * .5
            * P.rfr_maj
            + (nbptr == 1.5)
            * P.rfr_maj
            )

        montant = (
            (P.min <= salaire_imposable) * (salaire_imposable < P.int) * P.montant
            + (P.int <= salaire_imposable) * (salaire_imposable <= P.max) * (P.max - salaire_imposable) * P.taux
            )

        return elig_creimp_jeunes * elig * max_(25, montant)  # D'après  le document num. 2041 GY

        # somme calculée sur formulaire 2041


class percvm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt pertes sur cessions de valeurs mobilières'
    end = '2010-12-31'
    definition_period = YEAR

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pertes sur cessions de valeurs mobilières (3VV)
        -2010
        '''
        f3vv_end_2010 = foyer_fiscal('f3vv_end_2010', period)
        P = parameters(period).impot_revenu.credits_impots.percvm

        return P.taux * f3vv_end_2010


class preetu(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt pour souscription de prêts étudiants'
    definition_period = YEAR
    end = '2018-12-31'

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2005
        '''
        f7uk = foyer_fiscal('f7uk', period)
        P = parameters(period).impot_revenu.credits_impots.preetu

        return P.taux * min_(f7uk, P.max)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2006-2007
        '''
        f7uk = foyer_fiscal('f7uk', period)
        f7vo = foyer_fiscal('f7vo', period)
        P = parameters(period).impot_revenu.credits_impots.preetu

        max1 = P.max * (1 + f7vo)
        return P.taux * min_(f7uk, max1)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
        2008-
        '''
        f7uk = foyer_fiscal('f7uk', period)
        f7vo = foyer_fiscal('f7vo', period)
        f7td = foyer_fiscal('f7td', period)
        P = parameters(period).impot_revenu.credits_impots.preetu

        max1 = P.max * f7vo
        return P.taux * min_(f7uk, P.max) + P.taux * min_(f7td, max1)


class prlire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prélèvement libératoire à restituer (case 2DH)'
    definition_period = YEAR

    def formula_2002(foyer_fiscal, period, parameters):
        f2dh = foyer_fiscal('f2dh', period)
        f2ch = foyer_fiscal('f2ch', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)
        jeune_veuf = foyer_fiscal('jeune_veuf', period)
        parameters_rvcm = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        abattement_assurance_vie = parameters_rvcm.produits_assurances_vies_assimiles.abattement_couple * maries_ou_pacses + parameters_rvcm.produits_assurances_vies_assimiles.abattement_celib * (celibataire_ou_divorce | veuf | jeune_veuf)

        plaf_resid = max_(abattement_assurance_vie - f2ch, 0)
        return parameters(period).impot_revenu.credits_impots.prlire.taux * min_(f2dh, plaf_resid)


class quaenv(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédits d’impôt pour dépenses en faveur de la qualité environnementale (2005 - 2014) / de la transition energétique (2014 - ) '
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH)
        2005
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wf = foyer_fiscal('f7wf_2012', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wh = foyer_fiscal('f7wh', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        n = nb_pac_majoration_plafond
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * (n >= 1) + P.pac2 * (n >= 2) + P.pac2 * (max_(n - 2, 0))

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_wg * min_(f7wg, max1)
            + P.taux_wh * min_(f7wh, max2)
            )

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WQ)
        2006-2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7wf = foyer_fiscal('f7wf_2012', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wq = foyer_fiscal('f7wq', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_wg * min_(f7wg, max1)
            + P.taux_wh * min_(f7wh, max2)
            + P.taux_wq * min_(f7wq, max3)
            )

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WG, 7WH, 7WK, 7WQ, 7SB, 7SC, 7SD, 7SE)
        2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7we = foyer_fiscal('f7we_2013', period)
        f7wf = foyer_fiscal('f7wf_2012', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7sb = foyer_fiscal('f7sb_2011', period)
        f7sc = foyer_fiscal('f7sc_2009', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wg)
        max6 = max_(0, max5 - f7sc)
        max7 = max_(0, max6 - f7wh)
        max8 = max_(0, max7 - f7sb)

        return or_(not_(f7we), rfr < P.max_rfr) * (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_se * min_(f7se, max1)
            + P.taux_wk * min_(f7wk, max2)
            + P.taux_sd * min_(f7sd, max3)
            + P.taux_wg * min_(f7wg, max4)
            + P.taux_sc * min_(f7sc, max5)
            + P.taux_wh * min_(f7wh, max6)
            + P.taux_sb * min_(f7sb, max7)
            + P.taux_wq * min_(f7wq, max8)
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
        2010-2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7we = foyer_fiscal('f7we_2013', period)
        f7wf = foyer_fiscal('f7wf_2012', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wk = foyer_fiscal('f7wk', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7sb = foyer_fiscal('f7sb_2011', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond

        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wh)
        max6 = max_(0, max5 - f7sb)
        max7 = max_(0, max6 - f7wq)
        return not_(f7wg) * or_(not_(f7we), (rfr < P.max_rfr)) * (
            P.taux_wf * min_(f7wf, max0)
            + P.taux_se * min_(f7se, max1)
            + P.taux_wk * min_(f7wk, max2)
            + P.taux_sd * min_(f7sd, max3)
            + P.taux_wh * min_(f7wh, max4)
            + P.taux_sb * min_(f7sb, max5)
            + P.taux_wq * min_(f7wq, max6)
            + P.taux_sh * min_(f7sh, max7)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2012
        '''
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sm = foyer_fiscal('f7sm_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7so = foyer_fiscal('f7so_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7tt = foyer_fiscal('f7tt_2012', period)
        f7tu = foyer_fiscal('f7tu_2012', period)
        f7tv = foyer_fiscal('f7tv_2012', period)
        f7tw = foyer_fiscal('f7tw_2012', period)
        f7tx = foyer_fiscal('f7tx_2012', period)
        f7ty = foyer_fiscal('f7ty_2012', period)
        f7st = foyer_fiscal('f7st', period)
        f7su = foyer_fiscal('f7su', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7sz = foyer_fiscal('f7sz_2015', period)
        f7we = foyer_fiscal('f7we_2013', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wk = foyer_fiscal('f7wk', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        maxi1 = max_(0, max0 - f7ty)
        maxi2 = max_(0, maxi1 - f7tx)
        maxi3 = max_(0, maxi2 - f7tw)
        maxi4 = max_(0, maxi3 - f7tv)
        maxi5 = max_(0, maxi4 - f7tu)
        collectif = (
            P.taux_ty * min_(f7ty, max0)
            + P.taux_tx * min_(f7tx, maxi1)
            + P.taux_tw * min_(f7tw, maxi2)
            + P.taux_tv * min_(f7tv, maxi3)
            + P.taux_tu * min_(f7tu, maxi4)
            + P.taux_tt * min_(f7tt, maxi5)
            )

        max1 = max_(0, max0 - quaenv_bouquet * (f7ss + f7st) - not_(quaenv_bouquet) * (f7ss + f7st + f7sv))
        max2 = max_(0, max1 - quaenv_bouquet * (f7sn + f7sr + f7sq) - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr))
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = max_(0, max3 - quaenv_bouquet * (f7se) - not_(quaenv_bouquet) * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp))
        max5 = max_(0, max4 - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp) - not_(quaenv_bouquet) * (f7sm))
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))

        montant = (
            quaenv_bouquet * (
                P.taux10 * min_(max8, f7sk + f7sl)
                + P.taux11 * min_(max7, f7sm)
                + P.taux15 * min_(max6, f7sf + f7si + f7su + f7sw)
                + P.taux18 * min_(max5, f7sd + f7sj)
                + P.taux23 * min_(max4, f7sg + f7sh + f7so + f7sp)
                + P.taux26 * min_(max3, f7se)
                + P.taux32 * min_(max2, f7sv)
                + P.taux34 * min_(max1, f7sn + f7sr + f7sq)
                + P.taux40 * min_(max0, f7ss + f7st)
                )
            + not_(quaenv_bouquet) * (
                P.taux32 * min_(max0, f7ss + f7st + f7sv)
                + P.taux26 * min_(max1, f7sn + f7sq + f7sr)
                + P.taux17 * min_(max2, f7se)
                + P.taux15 * min_(max3, f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)
                + P.taux11 * min_(max4, f7sm)
                + P.taux10 * min_(max5, f7sd + not_(f7wk) * (f7sj + f7sk + f7sl))
                )
            )

        return not_(f7wg) * or_(not_(f7we), (rfr < P.max_rfr)) * (montant + collectif) + f7sz

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale
        2013
        '''
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sm = foyer_fiscal('f7sm_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7so = foyer_fiscal('f7so_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7su = foyer_fiscal('f7su', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7sz = foyer_fiscal('f7sz_2015', period)
        f7we = foyer_fiscal('f7we_2013', period)
        f7wg = foyer_fiscal('f7wg_2013', period)
        f7wk = foyer_fiscal('f7wk', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac_majoration_plafond
        max1 = max_(0, max0 - quaenv_bouquet * (f7ss + f7st) - not_(quaenv_bouquet) * (f7ss + f7st + f7sv))
        max2 = max_(0, max1 - quaenv_bouquet * (f7sn + f7sr + f7sq) - not_(quaenv_bouquet) * (f7sn + f7sq + f7sr))
        max3 = max_(0, max2 - quaenv_bouquet * (f7sv) - not_(quaenv_bouquet) * (f7se))
        max4 = max_(0, max3 - quaenv_bouquet * (f7se) - not_(quaenv_bouquet) * (f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp))
        max5 = max_(0, max4 - quaenv_bouquet * (f7sg + f7sh + f7so + f7sp) - not_(quaenv_bouquet) * (f7sm))
        max6 = max_(0, max5 - quaenv_bouquet * (f7sd + f7sj))
        max7 = max_(0, max6 - quaenv_bouquet * (f7sf + f7si + f7su + f7sw))
        max8 = max_(0, max7 - quaenv_bouquet * (f7sm))

        montant = (
            quaenv_bouquet * (
                P.taux10 * min_(max8, f7sk + f7sl)
                + P.taux11 * min_(max7, f7sm)
                + P.taux15 * min_(max6, f7sf + f7si + f7su + f7sw)
                + P.taux18 * min_(max5, f7sd + f7sj)
                + P.taux23 * min_(max4, f7sg + f7sh + f7so + f7sp)
                + P.taux26 * min_(max3, f7se)
                + P.taux32 * min_(max2, f7sv)
                + P.taux34 * min_(max1, f7sn + f7sr + f7sq)
                + P.taux40 * min_(max0, f7ss + f7st)
                )
            + not_(quaenv_bouquet) * (
                + P.taux32 * min_(max0, f7ss + f7st + f7sv)
                + P.taux26 * min_(max1, f7sn + f7sq + f7sr)
                + P.taux17 * min_(max2, f7se)
                + P.taux15 * min_(max3, f7sf + f7sg + f7sh + f7si + f7so + f7su + f7sw + f7sp)
                + P.taux11 * min_(max4, f7sm)
                + P.taux10 * min_(max5, f7sd + not_(f7wk) * (f7sj + f7sk + f7sl))
                )
            )
        return or_(not_(or_(f7we, f7wg)), (rfr < P.max_rfr)) * montant + f7sz  # TODO : attention, la condition porte sur le RFR des années passées (N-2 et N-3)

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale (1.1-31.8.2014) et transition energétique (1.9-31.12.2014)
        2014
        '''
        f7rg = foyer_fiscal('f7rg_2015', period)
        f7rh = foyer_fiscal('f7rh_2016', period)
        f7ri = foyer_fiscal('f7ri_2015', period)
        f7rj = foyer_fiscal('f7rj_2015', period)
        f7rk = foyer_fiscal('f7rk_2015', period)
        f7rl = foyer_fiscal('f7rl_2015', period)
        f7rn = foyer_fiscal('f7rn_2015', period)
        f7rp = foyer_fiscal('f7rp_2015', period)
        f7rq = foyer_fiscal('f7rq_2015', period)
        f7rr = foyer_fiscal('f7rr_2015', period)
        f7rs = foyer_fiscal('f7rs_2015', period)
        f7rt = foyer_fiscal('f7rt_2015', period)
        f7rv = foyer_fiscal('f7rv_2015', period)
        f7rw = foyer_fiscal('f7rw_2015', period)
        f7rz = foyer_fiscal('f7rz_2015', period)
        f7sa = foyer_fiscal('f7sa_2015', period)
        f7sb = foyer_fiscal('f7sb_2015', period)
        f7sc = foyer_fiscal('f7sc_2016', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7tv = foyer_fiscal('f7tv_2012', period)
        f7tw = foyer_fiscal('f7tw_2012', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7vh = foyer_fiscal('f7vh_2014', period)
        f7wb = foyer_fiscal('f7wb_2015', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wk = foyer_fiscal('f7wk', period)
        f7wt = foyer_fiscal('f7wt', period)
        f7wu = foyer_fiscal('f7wu', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        depenses_transition_energetique = (
            f7sa
            + f7sb
            + f7sc
            + f7wb
            + f7rg
            + f7vh
            + f7rh
            + f7ri
            + f7wu
            + f7rj
            + f7rk
            + f7rl
            + f7rn
            + f7rp
            + f7rr
            + f7rs
            + f7rq
            + f7rt
            + f7rv
            + f7rw
            + f7rz
            + f7tv
            + f7tw
            )

        max0 = (
            P.max * (1 + maries_ou_pacses)
            + P.pac1 * nb_pac2
            )

        max00 = max_(0, max0 - depenses_transition_energetique)

        max1 = max_(0, max00 - quaenv_bouquet * (f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st) - not_(quaenv_bouquet) * (max00))

        credit_quaenv = (
            quaenv_bouquet * (P.taux25 * (min_(max00,
                f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st))
                + P.taux15 * min_(max1,
                    f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw)
                              )
            + not_(quaenv_bouquet) * P.taux15 * (min_(max00,
                f7se + f7wc + f7vg + f7sn + f7sp + f7sr + f7ss + f7sq + f7st + f7sf + f7sg
                + f7sh + f7si + f7sv + f7sw + f7sd + not_(f7wk) * (f7wt + f7sj + f7sk + f7sl)))
            )

        # TODO: inclure la condition de non cumul éco-prêt / crédit quaenv si RFR > ... (condition complexifiée à partir de 2014)
        # TODO : inclure la condition de RFR2 (si pas de bouquet les dépenses f7s n'ouvrent aps droit à un crédit sauf si RFR < à un certain seuil)
        # TODO : inclure la condition de bouquet sur 2 périodes (si pas de bouquet avec les dépenses du 1.1 au 31.8, le bouquet peut s'apprécier
        #          sur la base des dépenses faites du 1.1 au 31.12 mais le taux sera de 25% pour la 1ère moitié de l'année et 30% l'autre)

        return P.taux30 * min_(max0, depenses_transition_energetique) + min_(max_(0, max0 - depenses_transition_energetique), credit_quaenv)

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la qualité environnementale (1.1-31.8.2014) et transition energétique (1.9.2014-31.12.2015)
        2015
        '''
        f7aa = foyer_fiscal('f7aa_2016', period)
        f7ad = foyer_fiscal('f7ad', period)
        f7af = foyer_fiscal('f7af', period)
        f7ah = foyer_fiscal('f7ah', period)
        f7ak = foyer_fiscal('f7ak', period)
        f7al = foyer_fiscal('f7al', period)
        f7am = foyer_fiscal('f7am', period)
        f7an = foyer_fiscal('f7an', period)
        f7aq = foyer_fiscal('f7aq', period)
        f7ar = foyer_fiscal('f7ar', period)
        f7av = foyer_fiscal('f7av', period)
        f7ax = foyer_fiscal('f7ax', period)
        f7ay = foyer_fiscal('f7ay', period)
        f7az = foyer_fiscal('f7az', period)
        f7bb = foyer_fiscal('f7bb', period)
        f7bc = foyer_fiscal('f7bc', period)
        f7bd = foyer_fiscal('f7bd', period)
        f7be = foyer_fiscal('f7be', period)
        f7bf = foyer_fiscal('f7bf', period)
        f7bh = foyer_fiscal('f7bh', period)
        f7bk = foyer_fiscal('f7bk', period)
        f7bl = foyer_fiscal('f7bl', period)
        f7rg = foyer_fiscal('f7rg_2015', period)
        f7rh = foyer_fiscal('f7rh_2016', period)
        f7ri = foyer_fiscal('f7ri_2015', period)
        f7rj = foyer_fiscal('f7rj_2015', period)
        f7rk = foyer_fiscal('f7rk_2015', period)
        f7rl = foyer_fiscal('f7rl_2015', period)
        f7rn = foyer_fiscal('f7rn_2015', period)
        f7rp = foyer_fiscal('f7rp_2015', period)
        f7rq = foyer_fiscal('f7rq_2015', period)
        f7rr = foyer_fiscal('f7rr_2015', period)
        f7rs = foyer_fiscal('f7rs_2015', period)
        f7rt = foyer_fiscal('f7rt_2015', period)
        f7ru = foyer_fiscal('f7ru_2015', period)
        f7rv = foyer_fiscal('f7rv_2015', period)
        f7rw = foyer_fiscal('f7rw_2015', period)
        f7rz = foyer_fiscal('f7rz_2015', period)
        f7sa = foyer_fiscal('f7sa_2015', period)
        f7sb = foyer_fiscal('f7sb_2015', period)
        f7sc = foyer_fiscal('f7sc_2016', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sm = foyer_fiscal('f7sm_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7so = foyer_fiscal('f7so_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7su = foyer_fiscal('f7su', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7sz = foyer_fiscal('f7sz_2015', period)
        f7ta = foyer_fiscal('f7ta_2015', period)
        f7tb = foyer_fiscal('f7tb_2015', period)
        f7tc = foyer_fiscal('f7tc', period)
        f7tn = foyer_fiscal('f7tn', period)
        f7tp = foyer_fiscal('f7tp_2015', period)
        f7tq = foyer_fiscal('f7tq_2015', period)
        f7tr = foyer_fiscal('f7tr_2015', period)
        f7ts = foyer_fiscal('f7ts_2015', period)
        f7tt = foyer_fiscal('f7tt_2012', period)
        f7tv = foyer_fiscal('f7tv_2012', period)
        f7tw = foyer_fiscal('f7tw_2012', period)
        f7tx = foyer_fiscal('f7tx_2015', period)
        f7ty = foyer_fiscal('f7ty_2015', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7vh = foyer_fiscal('f7vh_2014', period)
        f7vi = foyer_fiscal('f7vi_2015', period)
        f7vk = foyer_fiscal('f7vk_2015', period)
        f7vl = foyer_fiscal('f7vl_2015', period)
        f7wb = foyer_fiscal('f7wb_2015', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wi = foyer_fiscal('f7wi_2015', period)
        f7wt = foyer_fiscal('f7wt', period)
        f7wu = foyer_fiscal('f7wu', period)
        f7wv = foyer_fiscal('f7wv', period)
        f7ww = foyer_fiscal('f7ww', period)
        f7xb = foyer_fiscal('f7xb', period)
        f7xc = foyer_fiscal('f7xc_2015', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        quaenv_bouquet = foyer_fiscal('quaenv_bouquet', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        depenses_transition_energetique_bouquet_2ans_2014_part2 = (
            f7sa + f7sb + f7sc + f7wb + f7rg + f7vh + f7rh + f7ri + f7wu + f7rj + f7rk + f7rl
            + f7rn + f7rp + f7rr + f7rs + f7rq + f7rt + f7rv + f7rw + f7rz + f7tv + f7tw
            )
        depenses_transition_energetique_bouquet_2ans_2015 = (
            f7ta + f7tb + f7tc + f7xb + f7xc + f7wh + f7wi + f7vi + f7wv + f7ww + f7vk + f7vl
            + f7tn + f7tp + f7tr + f7ts + f7tq + f7tt + f7tx + f7ty + f7ru + f7su + f7sm + f7so + f7sz
            )
        depenses_transition_energetique_2015 = (
            f7aa + f7ad + f7af + f7ah + f7ak + f7al + f7am + f7an + f7aq + f7ar + f7av + f7ax
            + f7ay + f7az + f7bb + f7bc + f7bd + f7be + f7bf + f7bh + f7bk + f7bl
            )
        depenses_transition_energetique = (
            depenses_transition_energetique_bouquet_2ans_2014_part2 * quaenv_bouquet
            + depenses_transition_energetique_bouquet_2ans_2015
            + depenses_transition_energetique_2015
            )

        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2
        max00 = max_(0, max0 - depenses_transition_energetique)
        max1 = max_(0, max00 - quaenv_bouquet * (f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st) - not_(quaenv_bouquet) * (max00))
        credit_quaenv_bouquet_2ans = (
            quaenv_bouquet * (
                P.taux25 * (min_(max00,
                    f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st))
                + P.taux15 * min_(max1,
                    f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw)
                )
            )

        # TODO: inclure la condition de non cumul éco-prêt / crédit quaenv si RFR > ... (condition complexifiée à partir de 2014)

        return (
            P.taux30 * min_(max0, depenses_transition_energetique)
            + min_(max_(0, max0 - depenses_transition_energetique), credit_quaenv_bouquet_2ans)
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_pac2 = foyer_fiscal('nb_pac2', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv
        max0 = P.max * (1 + maries_ou_pacses) + P.pac1 * nb_pac2

        cases_depenses = [
            'f7aa_2016', 'f7ad', 'f7af', 'f7ah', 'f7ak', 'f7al', 'f7am', 'f7an', 'f7aq', 'f7ar', 'f7av', 'f7ax',
            'f7ay', 'f7az', 'f7bb', 'f7bc', 'f7bd', 'f7be', 'f7bf', 'f7bh', 'f7bk', 'f7bl', 'f7bm_2016', 'f7cb',
            ]
        depenses_transition_energetique = sum([foyer_fiscal(case, period) for case in cases_depenses])

        return P.taux30 * min_(max0, depenses_transition_energetique)

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        personnes_a_charge = foyer_fiscal('nb_pac2', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        cases_depenses = [
            'f7ad', 'f7af', 'f7ah', 'f7ak', 'f7al', 'f7am', 'f7an', 'f7aq', 'f7ar', 'f7av', 'f7ax', 'f7ay', 'f7az',
            'f7bb', 'f7bc', 'f7bd', 'f7be', 'f7bf', 'f7bh', 'f7bk', 'f7bl', 'f7cb',
            ]
        depenses_transition_energetique = sum([foyer_fiscal(case, period) for case in cases_depenses])
        plafond_depenses_energetiques = P.max * (1 + maries_ou_pacses) + P.pac1 * personnes_a_charge

        return P.taux30 * min_(plafond_depenses_energetiques, depenses_transition_energetique)

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2018
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        personnes_a_charge = foyer_fiscal('nb_pac2', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        cases_depenses = [
            'f7aa', 'f7ad', 'f7af', 'f7ah', 'f7ak', 'f7al', 'f7am', 'f7an', 'f7aq', 'f7ar', 'f7as', 'f7av', 'f7ax', 'f7ay', 'f7az',
            'f7bb', 'f7bc', 'f7bd', 'f7be', 'f7bf', 'f7bh', 'f7bk', 'f7bl', 'f7bm', 'f7cb',
            ]
        depenses_transition_energetique = sum([foyer_fiscal(case, period) for case in cases_depenses])
        cases_depense_taux_reduit = ['f7ao', 'f7ap']
        depenses_transition_energetique_taux_reduit = sum([foyer_fiscal(case, period) for case in cases_depense_taux_reduit])

        plafond_depenses_energetiques = P.max * (1 + maries_ou_pacses) + P.pac1 * personnes_a_charge
        plafond_depenses_energetiques_taux_reduit = max_(0, plafond_depenses_energetiques - depenses_transition_energetique)

        return (
            P.taux30 * min_(plafond_depenses_energetiques, depenses_transition_energetique)
            + P.taux15 * min_(plafond_depenses_energetiques_taux_reduit, depenses_transition_energetique_taux_reduit)
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Crédits d’impôt pour dépenses en faveur de la transition energétique
        2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        personnes_a_charge = foyer_fiscal('nb_pac2', period)
        P = parameters(period).impot_revenu.credits_impots.quaenv

        cases_depenses = [
            'f7aa', 'f7ad', 'f7af', 'f7ah', 'f7ak', 'f7al', 'f7ar', 'f7as', 'f7av', 'f7ax', 'f7ay', 'f7az',
            'f7bb', 'f7bc', 'f7bd', 'f7be', 'f7bf', 'f7bh', 'f7bk', 'f7bl', 'f7bm', 'f7cb', 'f7bn',
            ]
        depenses_transition_energetique = sum([foyer_fiscal(case, period) for case in cases_depenses])
        f7bq = foyer_fiscal('f7bq', period)

        plafond = P.max * (1 + maries_ou_pacses) + P.pac1 * personnes_a_charge
        plafondint = min_(plafond, f7bq)
        plafond_ordinaire = (plafond - plafondint)

        return (
            P.taux30 * min_(plafond_ordinaire, depenses_transition_energetique)
            + P.taux50 * plafondint
            )


class quaenv_bouquet(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = "Indicateur de réalisation d'un bouquet de travaux, dans le cadre du crédit d'impôt en faveur de la qualité environnementale"
    definition_period = YEAR
    reference = 'http://bofip.impots.gouv.fr/bofip/3883-PGP.html?identifiant=BOI-IR-RICI-280-20170807'
    end = '2015-12-31'

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2012
        '''
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7so = foyer_fiscal('f7so_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7ve = foyer_fiscal('f7ve', period)
        f7vf = foyer_fiscal('f7vf', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7wa = foyer_fiscal('f7wa_2012', period)
        f7wb = foyer_fiscal('f7wb_2015', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wf = foyer_fiscal('f7wf_2012', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wq = foyer_fiscal('f7wq', period)
        f7ws = foyer_fiscal('f7ws', period)
        f7wt = foyer_fiscal('f7wt', period)

        t1 = ((f7wt * f7ws + f7wq + f7wf) > 0) * 1
        t2 = ((f7wc * f7wb + f7wa) > 0) * 1
        t3 = ((f7vg * f7vf + f7ve) > 0) * 1
        t4 = ((f7sn + f7so) > 0) * 1
        t5 = ((f7sr + f7ss) > 0) * 1
        t6 = ((f7st + f7sp + f7sq + f7sd + f7se) > 0) * 1
        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (f7wh == 1)
        return bouquet

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2013
        '''
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7so = foyer_fiscal('f7so_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wt = foyer_fiscal('f7wt', period)

        t1 = f7wt
        t2 = f7wc
        t3 = f7vg
        t4 = ((f7sn + f7so) > 0) * 1
        t5 = ((f7sr + f7ss) > 0) * 1
        t6 = ((f7st + f7sp + f7sq + f7sd + f7se) > 0) * 1
        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (f7wh == 1)
        return bouquet

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux
        2014
        '''
        f7rn = foyer_fiscal('f7rn_2015', period)
        f7rp = foyer_fiscal('f7rp_2015', period)
        f7rq = foyer_fiscal('f7rq_2015', period)
        f7rr = foyer_fiscal('f7rr_2015', period)
        f7rs = foyer_fiscal('f7rs_2015', period)
        f7rt = foyer_fiscal('f7rt_2015', period)
        f7sa = foyer_fiscal('f7sa_2015', period)
        f7sb = foyer_fiscal('f7sb_2015', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7vh = foyer_fiscal('f7vh_2014', period)
        f7wb = foyer_fiscal('f7wb_2015', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wt = foyer_fiscal('f7wt', period)
        f7wu = foyer_fiscal('f7wu', period)

        depense_2014_eligible = (
            f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st
            + f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw
            )

        t1 = ((f7wt + f7wu) > 0) * 1
        t2 = ((f7wc + f7wb) > 0) * 1
        t3 = ((f7vg + f7vh) > 0) * 1
        t4 = ((f7sn + f7rn) > 0) * 1
        t5 = ((f7sr + f7rr + f7ss + f7rs) > 0) * 1
        t6 = ((f7sd + f7sa + f7se + f7sb + f7sp + f7rp + f7sq + f7rq + f7st + f7rt) > 0) * 1

        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (depense_2014_eligible > 0)
        return bouquet

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Les dépenses de travaux dépendent d'un bouquet de travaux (sur 2 ans)
        2015
        '''
        f7rn = foyer_fiscal('f7rn_2015', period)
        f7rp = foyer_fiscal('f7rp_2015', period)
        f7rq = foyer_fiscal('f7rq_2015', period)
        f7rr = foyer_fiscal('f7rr_2015', period)
        f7rs = foyer_fiscal('f7rs_2015', period)
        f7rt = foyer_fiscal('f7rt_2015', period)
        f7sa = foyer_fiscal('f7sa_2015', period)
        f7sb = foyer_fiscal('f7sb_2015', period)
        f7sd = foyer_fiscal('f7sd_2015', period)
        f7se = foyer_fiscal('f7se_2015', period)
        f7sf = foyer_fiscal('f7sf_2015', period)
        f7sg = foyer_fiscal('f7sg_2015', period)
        f7sh = foyer_fiscal('f7sh_2015', period)
        f7si = foyer_fiscal('f7si_2015', period)
        f7sj = foyer_fiscal('f7sj_2015', period)
        f7sk = foyer_fiscal('f7sk_2015', period)
        f7sl = foyer_fiscal('f7sl_2015', period)
        f7sn = foyer_fiscal('f7sn_2015', period)
        f7sp = foyer_fiscal('f7sp', period)
        f7sq = foyer_fiscal('f7sq_2015', period)
        f7sr = foyer_fiscal('f7sr_2015', period)
        f7ss = foyer_fiscal('f7ss', period)
        f7st = foyer_fiscal('f7st', period)
        f7sv = foyer_fiscal('f7sv', period)
        f7sw = foyer_fiscal('f7sw', period)
        f7ta = foyer_fiscal('f7ta_2015', period)
        f7tb = foyer_fiscal('f7tb_2015', period)
        f7tn = foyer_fiscal('f7tn', period)
        f7tp = foyer_fiscal('f7tp_2015', period)
        f7tq = foyer_fiscal('f7tq_2015', period)
        f7tr = foyer_fiscal('f7tr_2015', period)
        f7ts = foyer_fiscal('f7ts_2015', period)
        f7tt = foyer_fiscal('f7tt_2012', period)
        f7vg = foyer_fiscal('f7vg', period)
        f7vh = foyer_fiscal('f7vh_2014', period)
        f7wb = foyer_fiscal('f7wb_2015', period)
        f7wc = foyer_fiscal('f7wc_2015', period)
        f7wh = foyer_fiscal('f7wh', period)
        f7wt = foyer_fiscal('f7wt', period)
        f7wu = foyer_fiscal('f7wu', period)
        f7wv = foyer_fiscal('f7wv', period)
        f7xb = foyer_fiscal('f7xb', period)

        depense_2014_eligible = (
            f7sd + f7se + f7wc + f7vg + f7wt + f7sn + f7sp + f7sr + f7ss + f7sq + f7st
            + f7sf + f7sg + f7sh + f7si + f7sj + f7sk + f7sl + f7sv + f7sw
            )

        depense_2015_eligible = (f7ta + f7tb + f7xb + f7wh + f7wv + f7tn + f7tp + f7tr + f7ts + f7tq + f7tt)

        t1 = ((f7wt + f7wu + f7wv) > 0) * 1
        t2 = ((f7wc + f7wb + f7xb) > 0) * 1
        t3 = ((f7vg + f7vh + f7wh) > 0) * 1
        t4 = ((f7sn + f7rn + f7tn) > 0) * 1
        t5 = ((f7sr + f7rr + f7tr + f7ss + f7rs + f7ts) > 0) * 1
        t6 = ((
            f7sd + f7sa + f7ta
            + f7se + f7sb + f7tb
            + f7sp + f7rp + f7tp
            + f7sq + f7rq + f7tq
            + f7st + f7rt + f7tt
            ) > 0) * 1

        bouquet = ((t1 + t2 + t3 + t4 + t5 + t6) > 1) * (depense_2014_eligible > 0) * (depense_2015_eligible > 0)
        return bouquet


class ci_saldom(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Crédit d’impôt emploi d’un salarié à domicile'
    definition_period = YEAR

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2007-2008
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7dg = foyer_fiscal('f7dg', period)
        f7dl = foyer_fiscal('f7dl', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        isinvalid = f7dg
        nbpacmin = nb_pac_majoration_plafond + f7dl
        maxBase = P.plafond
        maxDuMaxNonInv = P.plafond_maximum
        maxNonInv = min_(maxBase + P.increment_plafond * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.plafond_invalides * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
        2009-
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7dg = foyer_fiscal('f7dg', period)
        f7dl = foyer_fiscal('f7dl', period)
        f7dq = foyer_fiscal('f7dq', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        isinvalid = f7dg
        annee1 = f7dq
        nbpacmin = nb_pac_majoration_plafond + f7dl
        maxBase = P.plafond * not_(annee1) + P.plafond_1ere_annee * annee1
        maxDuMaxNonInv = P.plafond_maximum * not_(annee1) + P.plafond_invalides_1ere_annee * annee1
        maxNonInv = min_(maxBase + P.increment_plafond * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.plafond_invalides * isinvalid

        return P.taux * min_(f7db, maxEffectif)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile
        2011 - 2016
        NB: Normalement, le plafond est aussi augmenté pour chaque personne
        agée de plus de 65 ans dans le foyer (en plus des PACs et des
        ascendants de 65 ans remplissant les conditions de l'APA). On ne
        prend pas en compte le nombre de ces individus ici.
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)

        f7db = foyer_fiscal('f7db', period)
        f7dl = foyer_fiscal('f7dl', period)

        annee1 = foyer_fiscal('f7dq', period)
        invalide = foyer_fiscal('f7dg', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        # détérminer le plafond

        if invalide.any():
            plaf = P.plafond_invalides
        else:
            if annee1.any():
                plaf = min_(P.plafond_invalides_1ere_annee, P.plafond_1ere_annee + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))
            else:
                plaf = min_(P.plafond_maximum, P.plafond + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))

        # calcul du CI
        ci = min_(plaf, f7db) * P.taux

        return ci

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile
        2020
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)

        f7db = foyer_fiscal('f7db', period)
        f7dr = foyer_fiscal('f7dr', period)
        f7dl = foyer_fiscal('f7dl', period)

        annee1 = foyer_fiscal('f7dq', period)
        invalide = foyer_fiscal('f7dg', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        # détérminer le plafond
        if invalide.any():
            plaf = P.plafond_invalides
        else:
            if annee1.any():
                plaf = min_(P.plafond_invalides_1ere_annee, P.plafond_1ere_annee + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))
            else:
                plaf = min_(P.plafond_maximum, P.plafond + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))

        # calcul du CI
        ci = min_(plaf, max_(0, f7db - f7dr)) * P.taux

        return ci
