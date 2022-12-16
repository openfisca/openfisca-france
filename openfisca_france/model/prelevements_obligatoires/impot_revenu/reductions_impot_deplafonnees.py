import logging
from numpy import around
from openfisca_france.model.base import *


log = logging.getLogger(__name__)


class reductions_deplafonnees(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur le revenu déplafonnées"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):

        reductions_sans_plafond = [
            'accueil_dans_etablissement_personnes_agees',
            'dfppce',
            'frais_de_comptabilite',
            'assvie',
            'reduction_cotisations_syndicales',
            'creaen',
            'interets_paiements_differes_agriculteurs',
            'mecena',
            'prestations_compensatoires',
            'interets_emprunt_reprise_societe',
            'restauration_patrimoine_bati',  # Malraux, non plafonnées pour les investissements réalisés après 2013
            'reduction_enfants_scolarises',
            'accult',
            'rente_survie',
            ]

        # Step 4: Get other uncapped reductions
        red_deplaf = sum([around(foyer_fiscal(reduction, period)) for reduction in reductions_sans_plafond])

        return red_deplaf


class accult(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Acquisition de biens culturels'
    definition_period = YEAR
    end = '2020-12-31'

    def formula_2002(foyer_fiscal, period, parameters):
        '''
        Acquisition de biens culturels (case 7UO)
        2002-
        '''
        f7uo = foyer_fiscal('f7uo', period)
        P = parameters(period).impot_revenu.calcul_credits_impots.accult

        return P.taux * f7uo


class frais_de_comptabilite(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'frais_de_comptabilite'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Frais de comptabilité et d'adhésion à un CGA ou AA
        2002-
        '''
        f7ff = foyer_fiscal('f7ff', period)
        f7fg = foyer_fiscal('f7fg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.frais_de_comptabilite

        return min_(f7ff, P.plafond * f7fg)


class assvie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'assvie'
    end = '2004-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Assurance-vie (cases GW, GX et GY de la 2042)
        2002-2004
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        f7gw = foyer_fiscal('f7gw_2004', period)
        f7gx = foyer_fiscal('f7gx_2004', period)
        f7gy = foyer_fiscal('f7gy_2004', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.assurances_vie

        plafond = P.plafond + nb_pac * P.increment
        return P.taux * min_(f7gw + f7gx + f7gy, plafond)


class creaen(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'creaen'
    definition_period = YEAR
    end = '2014-12-31'

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2006-2008
        '''
        f7fy = foyer_fiscal('f7fy_2011', period)
        f7gy = foyer_fiscal('f7gy_2010', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.aide_createurs_repreneurs_entreprise

        return (P.reduction * f7fy + P.surplus_si_invalide * f7gy)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2009
        '''
        f7fy = foyer_fiscal('f7fy_2011', period)
        f7gy = foyer_fiscal('f7gy_2010', period)
        f7jy = foyer_fiscal('f7jy_2010', period)
        f7hy = foyer_fiscal('f7hy_2011', period)
        f7ky = foyer_fiscal('f7ky_2011', period)
        f7iy = foyer_fiscal('f7iy_2011', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.aide_createurs_repreneurs_entreprise

        return (
            P.reduction * ((f7jy + f7fy) + f7hy / 2)
            + P.surplus_si_invalide * ((f7ky + f7gy) + f7iy / 2)
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2010-2011
        '''
        f7fy = foyer_fiscal('f7fy_2011', period)
        f7gy = foyer_fiscal('f7gy_2010', period)
        f7jy = foyer_fiscal('f7jy_2010', period)
        f7hy = foyer_fiscal('f7hy_2011', period)
        f7ky = foyer_fiscal('f7ky_2011', period)
        f7iy = foyer_fiscal('f7iy_2011', period)
        f7ly = foyer_fiscal('f7ly_2010', period)
        f7my = foyer_fiscal('f7my_2010', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.aide_createurs_repreneurs_entreprise

        return (
            P.reduction * ((f7jy + f7fy) + (f7hy + f7ly) / 2)
            + P.surplus_si_invalide * ((f7ky + f7gy) + (f7iy + f7my) / 2)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Aide aux créateurs et repreneurs d'entreprises
        2012-
        '''
        f7ly = foyer_fiscal('f7ly_2010', period)
        f7my = foyer_fiscal('f7my_2010', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.aide_createurs_repreneurs_entreprise

        return (
            P.reduction * (f7ly / 2)
            + P.surplus_si_invalide * (f7my / 2)
            )


class accueil_dans_etablissement_personnes_agees(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Hébergement santé'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
        ?-
        '''
        f7cd = foyer_fiscal('f7cd', period)
        f7ce = foyer_fiscal('f7ce', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.accueil_dans_etablissement_personnes_agees

        return P.taux * (min_(f7cd, P.plafond + min_(f7ce, P.plafond)))


class dfppce(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Dons à des organismes d'intérêt général et dons pour le financement des partis politiques"
    reference = 'http://bofip.impots.gouv.fr/bofip/5823-PGP'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf + f7xs
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf + f7xs + f7xt
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu + f7xw
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons

        base = f7uf + f7xs + f7xt + f7xu + f7xw + f7xy
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        rni = foyer_fiscal('rni', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7vc = foyer_fiscal('f7vc', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond

        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)
        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Dons aux autres oeuvres et dons effectués pour le financement des partis
        politiques et des campagnes électorales (2011-2013)
        '''
        rni = foyer_fiscal('rni', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7vc = foyer_fiscal('f7vc', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond

        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)
        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud
        max1 = P.dons_interet_general.plafond * rni
        return P.dons_aux_oeuvres.taux * min_(base, max1)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Dons versés à d’autres organismes d’intérêt général,
        aux associations d’utilité publique, aux candidats aux élections (2019)
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7uh = foyer_fiscal('f7uh', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7vc = foyer_fiscal('f7vc', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond
        taux_donapd = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.taux
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        red_7ud_7va = min_(plafond_reduction_don_coluche, f7va + f7ud) * taux_donapd
        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)

        dons_partipol = min_(P.dons_aux_partis_politiques.plafond_seul * (1 + maries_ou_pacses), f7uh)

        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud + dons_partipol
        max = P.dons_interet_general.plafond * rni

        return red_7ud_7va + P.dons_aux_oeuvres.taux * min_(base, max)

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Dons versés à d’autres organismes d’intérêt général,
        aux associations d’utilité publique, aux candidats aux élections (2019)
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7uh = foyer_fiscal('f7uh', period)
        f7ue = foyer_fiscal('f7ue', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7vc = foyer_fiscal('f7vc', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        PND = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_notre_dame
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond
        taux_donapd = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.taux
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        red_7ud_7va = min_(plafond_reduction_don_coluche, f7va + f7ud) * taux_donapd
        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)

        red_notre_dame = min_(PND.plafond, f7ue) * PND.taux
        report_notre_dame = max_(0, f7ue - PND.plafond)

        dons_partipol = min_(P.dons_aux_partis_politiques.plafond_seul * (1 + maries_ou_pacses), f7uh)

        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud + dons_partipol + report_notre_dame
        max = P.dons_interet_general.plafond * rni

        return red_notre_dame + red_7ud_7va + P.dons_aux_oeuvres.taux * min_(base, max)

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Dons versés à d’autres organismes d’intérêt général,
        aux associations d’utilité publique, aux candidats aux élections (2020)
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7uh = foyer_fiscal('f7uh', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7vc = foyer_fiscal('f7vc', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond
        taux_donapd = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.taux
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        red_7ud_7va = min_(plafond_reduction_don_coluche, f7va + f7ud) * taux_donapd
        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)

        dons_partipol = min_(P.dons_aux_partis_politiques.plafond_seul * (1 + maries_ou_pacses), f7uh)

        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud + dons_partipol
        max = P.dons_interet_general.plafond * rni

        return red_7ud_7va + P.dons_aux_oeuvres.taux * min_(base, max)

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Dons versés à d’autres organismes d’intérêt général,
        aux associations d’utilité publique, aux candidats aux élections (2021)
        '''
        rni = foyer_fiscal('rni', period)
        f7uf = foyer_fiscal('f7uf', period)
        f7uh = foyer_fiscal('f7uh', period)
        f7uj = foyer_fiscal('f7uj', period)
        f7xs = foyer_fiscal('f7xs', period)
        f7xt = foyer_fiscal('f7xt', period)
        f7xu = foyer_fiscal('f7xu', period)
        f7xw = foyer_fiscal('f7xw', period)
        f7xy = foyer_fiscal('f7xy', period)
        f7va = foyer_fiscal('f7va', period)
        f7ud = foyer_fiscal('f7ud', period)
        f7vc = foyer_fiscal('f7vc', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.dons
        plafond_reduction_don_coluche = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.plafond
        taux_donapd = parameters(period).impot_revenu.calcul_reductions_impots.dons.dons_coluche.taux
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        red_7ud_7va = min_(plafond_reduction_don_coluche, f7va + f7ud) * taux_donapd
        report_f7va_f7ud = max_(0, f7va + f7ud - plafond_reduction_don_coluche)

        red_7uj = min_(P.dons_assoc_cult, f7uj) * taux_donapd
        report_7uj = max_(0, f7uj - P.dons_assoc_cult)

        dons_partipol = min_(P.dons_aux_partis_politiques.plafond_seul * (1 + maries_ou_pacses), f7uh)

        base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy + report_f7va_f7ud + report_7uj + dons_partipol
        max = P.dons_interet_general.plafond * rni

        return red_7ud_7va + red_7uj + P.dons_aux_oeuvres.taux * min_(base, max)


class reduction_enfants_scolarises(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'reduction_enfants_scolarises'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Réduction d'impôt au titre des enfants à charge poursuivant leurs études secondaires ou supérieures
        '''
        f7ea = foyer_fiscal('f7ea', period)
        f7eb = foyer_fiscal('f7eb', period)
        f7ec = foyer_fiscal('f7ec', period)
        f7ed = foyer_fiscal('f7ed', period)
        f7ef = foyer_fiscal('f7ef', period)
        f7eg = foyer_fiscal('f7eg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.enfants_scolarises

        return (
            P.college * (f7ea + f7eb / 2)
            + P.lycee * (f7ec + f7ed / 2)
            + P.universite * (f7ef + f7eg / 2)
            )


class interets_paiements_differes_agriculteurs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Intérêts paiement différé agriculteurs'
    definition_period = YEAR

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts pour paiement différé accordé aux agriculteurs
        2005-
        '''
        f7um = foyer_fiscal('f7um', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.interets_paiements_differes_agriculteurs

        max1 = P.plafond * (1 + maries_ou_pacses)
        return P.taux * min_(f7um, max1)


class mecena(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Mécénat d'entreprise"
    definition_period = YEAR

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Mécénat d'entreprise (case 7US)
        2003-
        '''
        f7us = foyer_fiscal('f7us', period)

        return f7us


class prestations_compensatoires(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Prestations compensatoires'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Prestations compensatoires
        '''
        f7wm = foyer_fiscal('f7wm', period)
        f7wn = foyer_fiscal('f7wn', period)
        f7wo = foyer_fiscal('f7wo', period)
        f7wp = foyer_fiscal('f7wp', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.prestations_compensatoires

        div = (f7wo == 0) * 1 + f7wo  # Pour éviter les divisions par zéro

        return (
            (f7wm == 0) * (
                (f7wn == f7wo) * P.taux * min_(f7wn, P.plafond)
                + (f7wn < f7wo) * (f7wo <= P.plafond) * P.taux * f7wn
                + max_(0, (f7wn < f7wo) * (f7wo > P.plafond) * P.taux * P.plafond * f7wn / div)
                )
            + (f7wm != 0) * (
                (f7wn == f7wm) * (f7wo <= P.plafond) * P.taux * f7wm
                + max_(0, (f7wn == f7wm) * (f7wo >= P.plafond) * P.taux * f7wm / div)
                + (f7wn > f7wm) * (f7wo <= P.plafond) * P.taux * f7wn
                + max_(0, (f7wn > f7wm) * (f7wo >= P.plafond) * P.taux * f7wn / div)
                )
            + P.taux * f7wp
            )


class reduction_cotisations_syndicales(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt pour cotisations syndicales"
    definition_period = YEAR
    end = '2011-12-31'

    def formula(foyer_fiscal, period, parameters):
        '''
        Cotisations syndicales : réduction d'impôt (2002-2011) puis crédit d'impôt (2012- )
        '''
        return foyer_fiscal('cotisations_syndicales', period)


class cotisations_syndicales(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Montant de la réduction ou crédit d'impôt pour cotisations syndicales"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        NB: This is but an approximation of the true calculation, as it is done on the level of the tax unit.
        In reality, the ceilings of 1 % of revenues are applied on the individual level (cf. BOI-IR-RICI-20).
        '''

        f7ac = foyer_fiscal.members('f7ac', period)

        cotisations_versees = f7ac

        salaire_imposable = foyer_fiscal.members('salaire_imposable', period, options = [ADD])
        chomage_imposable = foyer_fiscal.members('chomage_imposable', period, options = [ADD])
        retraite_imposable = foyer_fiscal.members('retraite_imposable', period, options = [ADD])

        P = parameters(period).impot_revenu.calcul_reductions_impots.cotisations_syndicales

        plafond = (salaire_imposable + chomage_imposable + retraite_imposable) * P.plafond

        return (P.taux * foyer_fiscal.sum(min_(cotisations_versees, plafond)))


class interets_emprunt_reprise_societe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Intérêts emprunts pour reprise de société'
    definition_period = YEAR

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts d'emprunts pour reprise de société
        2003-
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7fh = foyer_fiscal('f7fh', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.interets_emprunt_reprise_societe

        plafond = P.plafond * (maries_ou_pacses + 1)
        return P.taux * min_(f7fh, plafond)


class restauration_patrimoine_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des dépenses de restauration immobilière - Dispositif Malraux"
    reference = 'http://bofip.impots.gouv.fr/bofip/1372-PGP'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA et 7RB)
        2009-2010
        '''
        f7ra = foyer_fiscal('f7ra_2015', period)
        f7rb = foyer_fiscal('f7rb_2015', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        max1 = P.plafond
        max2 = max_(max1 - f7rb, 0)
        return P.taux_rb * min_(f7rb, max1) + P.taux_ra * min_(f7ra, max2)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD)
        2011
        '''
        f7ra = foyer_fiscal('f7ra_2015', period)
        f7rb = foyer_fiscal('f7rb_2015', period)
        f7rc = foyer_fiscal('f7rc_2015', period)
        f7rd = foyer_fiscal('f7rd_2015', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        max1 = P.plafond
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc, 0)

        return (
            P.taux_rd * min_(f7rd, max1)
            + P.taux_rb * min_(f7rb, max2)
            + P.taux_rc * min_(f7rc, max3)
            + P.taux_ra * min_(f7ra, max4)
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF)
        2012
        '''
        f7ra = foyer_fiscal('f7ra_2015', period)
        f7rb = foyer_fiscal('f7rb_2015', period)
        f7rc = foyer_fiscal('f7rc_2015', period)
        f7rd = foyer_fiscal('f7rd_2015', period)
        f7re = foyer_fiscal('f7re_2016', period)
        f7rf = foyer_fiscal('f7rf_2016', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        max1 = P.plafond
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)

        return (
            P.taux_rd * min_(f7rd, max1)
            + P.taux_rb * min_(f7rb, max2)
            + P.taux_rc * min_(f7rc + f7rf, max3)
            + P.taux_ra * min_(f7ra, max4)
            + P.taux_re * min_(f7re, max5)
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière (cases 7RA, 7RB, 7RC, 7RD, 7RE, 7RF, 7SX, 7SY)
        2013-2015
        '''
        f7ra = foyer_fiscal('f7ra_2015', period)
        f7rb = foyer_fiscal('f7rb_2015', period)
        f7rc = foyer_fiscal('f7rc_2015', period)
        f7rd = foyer_fiscal('f7rd_2015', period)
        f7re = foyer_fiscal('f7re_2016', period)
        f7rf = foyer_fiscal('f7rf_2016', period)
        f7sx = foyer_fiscal('f7sx_2017', period)
        f7sy = foyer_fiscal('f7sy_2017', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        max1 = P.plafond
        max2 = max_(max1 - f7rd, 0)
        max3 = max_(max2 - f7rb, 0)
        max4 = max_(max3 - f7rc - f7sy - f7rf, 0)
        max5 = max_(max4 - f7ra, 0)

        return (
            P.taux_rd * min_(f7rd, max1)
            + P.taux_rb * min_(f7rb, max2)
            + P.taux_rc * min_(f7sy + f7rf + f7rc, max3)
            + P.taux_ra * min_(f7ra, max4) + P.taux_re * min_(f7re + f7sx, max5)
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2016
        '''
        f7nx = foyer_fiscal('f7nx', period)
        f7ny = foyer_fiscal('f7ny', period)
        f7re = foyer_fiscal('f7re_2016', period)
        f7rf = foyer_fiscal('f7rf_2016', period)
        f7sx = foyer_fiscal('f7sx_2017', period)
        f7sy = foyer_fiscal('f7sy_2017', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        max1 = P.plafond
        max2 = max_(max1 - f7nx - f7sy - f7rf, 0)

        return (
            P.taux_rc * min_(f7sy + f7rf + f7nx, max1)
            + P.taux_re * min_(f7re + f7sx + f7ny, max2)
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2017
        '''
        f7sy = foyer_fiscal('f7sy_2017', period)
        f7sx = foyer_fiscal('f7sx_2017', period)

        f7nx = foyer_fiscal('f7nx', period)
        f7ny = foyer_fiscal('f7ny', period)

        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati
        P0 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        depenses_secteur_degrade = f7sy + f7nx
        depenses_secteur_patrimoine_remarquable = f7sx + f7ny
        depenses_PSMV_2017 = f7tx
        depenses_non_PSMV_2017 = f7ty

        max1 = max_(P0.plafond - depenses_secteur_degrade, 0)
        max3 = max_(P.plafond - depenses_PSMV_2017, 0)

        return (
            P.taux_30 * (
                min_(depenses_secteur_degrade, P0.plafond)
                + min_(depenses_PSMV_2017, P.plafond)
                )
            + P.taux_22 * (
                min_(depenses_secteur_patrimoine_remarquable, max1)
                + min_(depenses_non_PSMV_2017, max3)
                )
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2018
        '''
        # plaf 100K
        f7nx = foyer_fiscal('f7nx', period)
        f7ny = foyer_fiscal('f7ny', period)

        # plaf 400K
        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)

        # reports
        f7kz = foyer_fiscal('f7kz', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati
        P0 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        base_nx = min_(P.plafond, f7nx)
        base_ny = min_(P.plafond - f7nx, f7ny)

        base_tx = min_(P0.plafond, f7tx)
        base_ty = min_(P0.plafond - f7tx, f7ty)

        ri = (f7kz
            + P.taux_30 * (base_nx + base_tx)
            + P.taux_22 * (base_ny + base_ty))

        return ri

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2019
        '''
        # plaf 100K
        f7nx = foyer_fiscal('f7nx', period)
        f7ny = foyer_fiscal('f7ny', period)

        # plaf 400K
        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)

        # reports
        f7kz = foyer_fiscal('f7kz', period)
        f7ky = foyer_fiscal('f7ky', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati
        P0 = parameters('2019-01-01').impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        base_nx = min_(P.plafond, f7nx)
        base_ny = min_(P.plafond - f7nx, f7ny)

        base_tx = min_(P0.plafond, f7tx)
        base_ty = min_(P0.plafond - f7tx, f7ty)

        ri = (f7kz + f7ky
            + P.taux_30 * (base_nx + base_tx)
            + P.taux_22 * (base_ny + base_ty))

        return ri

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2020
        '''
        # plaf 100K
        f7nx = foyer_fiscal('f7nx', period)
        f7ny = foyer_fiscal('f7ny', period)

        # plaf 400K
        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)

        # reports
        f7kz = foyer_fiscal('f7kz', period)
        f7ky = foyer_fiscal('f7ky', period)
        f7kx = foyer_fiscal('f7kx', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati
        P0 = parameters('2019-01-01').impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        base_nx = min_(P.plafond, f7nx)
        base_ny = min_(P.plafond - f7nx, f7ny)

        base_tx = min_(P0.plafond, f7tx)
        base_ty = min_(P0.plafond - f7tx, f7ty)

        ri = (f7kz + f7ky + f7kx
            + P.taux_30 * (base_nx + base_tx)
            + P.taux_22 * (base_ny + base_ty))

        return ri

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de restauration immobilière
        2021
        '''
        # plaf 400K
        f7tx = foyer_fiscal('f7tx', period)
        f7ty = foyer_fiscal('f7ty', period)

        # reports
        f7ky = foyer_fiscal('f7ky', period)
        f7kx = foyer_fiscal('f7kx', period)
        f7kw = foyer_fiscal('f7kw', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_patrimoine_bati

        base_tx = min_(P.plafond, f7tx)
        base_ty = min_(P.plafond - f7tx, f7ty)

        ri = (f7ky + f7kx + f7kw
            + P.taux_30 * (base_tx)
            + P.taux_22 * (base_ty))

        return ri


class rente_survie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'rente_survie'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Rentes de survie et contrats d'épargne handicap
        2002-
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        nbR = foyer_fiscal('nbR', period)
        f7gz = foyer_fiscal('f7gz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.rente_survie

        max1 = P.plafond + (nb_pac_majoration_plafond - nbR) * P.increment
        return P.taux * min_(f7gz, max1)
