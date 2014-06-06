# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import arange, argsort, asarray, cumsum, floor, linspace, logical_and as and_, logical_not as not_, repeat

from .input_variables.base import QUIFAM, QUIFOY, QUIMEN


CHEF = QUIFAM['chef']
ENFS = [QUIFAM['enf{}'.format(i)] for i in range(1, 10)]
PART = QUIFAM['part']
VOUS = QUIFOY['vous']


def _uc(self, agem_holder):
    '''
    Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
    'men'
    '''
    agem = self.split_by_roles(agem_holder)

    uc_adt = 0.5
    uc_enf = 0.3
    uc = 0.5
    for agm in agem.itervalues():
        age = floor(agm / 12)
        adt = (15 <= age) & (age <= 150)
        enf = (0 <= age) & (age <= 14)
        uc += adt * uc_adt + enf * uc_enf
    return uc


def _typ_men(self, isol_holder, af_nbenf_holder):
    '''
    type de menage
    'men'
    TODO: prendre les enfants du ménages et non ceux de la famille
    '''
    af_nbenf = self.cast_from_entity_to_role(af_nbenf_holder, role = CHEF)
    af_nbenf = self.sum_by_entity(af_nbenf)
    isol = self.cast_from_entity_to_role(isol_holder, role = CHEF)
    isol = self.sum_by_entity(isol)

    _0_kid = af_nbenf == 0
    _1_kid = af_nbenf == 1
    _2_kid = af_nbenf == 2
    _3_kid = af_nbenf >= 3

    return (0 * (isol & _0_kid) +  # Célibataire
            1 * (not_(isol) & _0_kid) +  # Couple sans enfants
            2 * (not_(isol) & _1_kid) +  # Couple un enfant
            3 * (not_(isol) & _2_kid) +  # Couple deux enfants
            4 * (not_(isol) & _3_kid) +  # Couple trois enfants et plus
            5 * (isol & _1_kid) +  # Famille monoparentale un enfant
            6 * (isol & _2_kid) +  # Famille monoparentale deux enfants
            7 * (isol & _3_kid))  # Famille monoparentale trois enfants et plus


def _revdisp(self, rev_trav_holder, pen_holder, rev_cap_holder, ir_lps_holder, psoc_holder, ppe_holder, impo):
    '''
    Revenu disponible - ménage
    'men'
    '''
    ir_lps = self.sum_by_entity(ir_lps_holder)
    pen = self.sum_by_entity(pen_holder)
    ppe = self.cast_from_entity_to_role(ppe_holder, role = VOUS)
    ppe = self.sum_by_entity(ppe)
    psoc = self.cast_from_entity_to_role(psoc_holder, role = CHEF)
    psoc = self.sum_by_entity(psoc)
    rev_cap = self.sum_by_entity(rev_cap_holder)
    rev_trav = self.sum_by_entity(rev_trav_holder)

    return rev_trav + pen + rev_cap + ir_lps + psoc + ppe + impo


def _nivvie(revdisp, uc):
    '''
    Niveau de vie du ménage
    'men'
    '''
    return revdisp / uc


def _revnet(self, rev_trav, pen, rev_cap):
    '''
    Revenu net du ménage
    'men'
    '''
    return self.sum_by_entity(rev_trav + pen + rev_cap)


def _nivvie_net(revnet, uc):
    '''
    Niveau de vie net du ménage
    'men'
    '''
    return revnet / uc


def _revini(self, rev_trav, pen, rev_cap, cotpat_contrib, cotsal_contrib):
    '''
    Revenu initial du ménage
    'men'
    '''
    return self.sum_by_entity(rev_trav + pen + rev_cap - cotpat_contrib - cotsal_contrib)


def _nivvie_ini(revini, uc):
    '''
    Niveau de vie initial du ménage
    'men'
    '''
    return revini / uc


def _revprim(rev_trav, cho, rev_cap, cotpat, cotsal):
    '''
    Revenu primaire du ménage
    Ensemble des revenus d'activités superbruts avant tout prélèvement
    Il est égale à la valeur ajoutée produite par les résidents
    'men'
    '''
    return rev_trav + rev_cap - cotpat - cotsal - cho


def _rev_trav(rev_sal, rag, ric, rnc):
    '''
    Revenu du travail
    '''
    return rev_sal + rag + ric + rnc


def _pen(chonet, rstnet, alr, alv, rto):
    '''
    Pensions
    '''
    return chonet + rstnet + alr + alv + rto


def _cotsoc_bar(csg_cap_bar, prelsoc_cap_bar, crds_cap_bar):
    '''
    Cotisations sociales sur les revenus du capital imposés au barème
    '''
    return csg_cap_bar + prelsoc_cap_bar + crds_cap_bar


def _cotsoc_lib(csg_cap_lib, prelsoc_cap_lib, crds_cap_lib):
    '''
    Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire
    '''
    return csg_cap_lib + prelsoc_cap_lib + crds_cap_lib


def _rev_cap(self, fon_holder, rev_cap_bar_holder, cotsoc_bar, rev_cap_lib_holder, cotsoc_lib, imp_lib_holder, rac):
    '''
    Revenus du patrimoine
    '''
    fon = self.cast_from_entity_to_role(fon_holder, role = VOUS)
    imp_lib = self.cast_from_entity_to_role(imp_lib_holder, role = VOUS)
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

    return fon + rev_cap_bar + cotsoc_bar + rev_cap_lib + cotsoc_lib + imp_lib + rac


def _psoc(pfam, mini, logt):
    '''
    Prestations sociales
    '''
    return pfam + mini + logt


def _pfam(af, cf, ars, aeeh, paje, asf, crds_pfam):
    '''
    Prestations familiales
    '''
    return af + cf + ars + aeeh + paje + asf + crds_pfam


def _mini(self, aspa, aah, caah, asi, rsa, aefa, api, ass_holder, psa, majo_rsa):
    '''
    Minima sociaux
    '''
    ass = self.sum_by_entity(ass_holder)

    return aspa + aah + caah + asi + rsa + aefa + api + ass + psa + majo_rsa


def _logt(apl, als, alf, crds_lgtm):
    '''
    Prestations logement
    '''
    return apl + als + alf + crds_lgtm


def _impo(self, irpp_holder, tax_hab):
    '''
    Impôts directs
    '''
    irpp = self.cast_from_entity_to_role(irpp_holder, role = VOUS)
    irpp = self.sum_by_entity(irpp)

    return irpp + tax_hab


def _crds(self, crdssal, crdsrst, crdscho, crds_fon_holder, crds_cap_bar, crds_cap_lib, crds_pfam_holder,
          crds_lgtm_holder, crds_mini_holder, crds_pv_mo_holder, crds_pv_immo_holder):
    '''
    Contribution au remboursement de la dette sociale
    '''
    crds_fon = self.cast_from_entity_to_role(crds_fon_holder, role = VOUS)
    crds_lgtm = self.cast_from_entity_to_role(crds_lgtm_holder, role = CHEF)
    crds_mini = self.cast_from_entity_to_role(crds_mini_holder, role = CHEF)
    crds_pfam = self.cast_from_entity_to_role(crds_pfam_holder, role = CHEF)
    crds_pv_immo = self.cast_from_entity_to_role(crds_pv_immo_holder, role = VOUS)
    crds_pv_mo = self.cast_from_entity_to_role(crds_pv_mo_holder, role = VOUS)

    return (crdssal + crdsrst + crdscho +
            crds_fon + crds_cap_bar + crds_cap_lib + crds_pv_mo + crds_pv_immo +
            crds_pfam + crds_lgtm + crds_mini)


def _csg(self, csgsali, csgsald, csgchoi, csgchod, csgrsti, csgrstd, csg_fon_holder, csg_cap_lib, csg_cap_bar,
         csg_pv_mo_holder, csg_pv_immo_holder):
    """
    Contribution sociale généralisée
    """
    csg_fon = self.cast_from_entity_to_role(csg_fon_holder, role = VOUS)
    csg_pv_immo = self.cast_from_entity_to_role(csg_pv_immo_holder, role = VOUS)
    csg_pv_mo = self.cast_from_entity_to_role(csg_pv_mo_holder, role = VOUS)

    return (csgsali + csgsald + csgchoi + csgchod + csgrsti + csgrstd +
            csg_fon + csg_cap_lib + csg_pv_mo + csg_pv_immo + csg_cap_bar)


def _cotsoc_noncontrib(cotpat_noncontrib, cotsal_noncontrib):
    '''
    Cotisations sociales non contributives (hors prelsoc_cap_lib, prelsoc_cap_bar)
    '''
    return cotpat_noncontrib + cotsal_noncontrib


def _prelsoc_cap(self, prelsoc_fon_holder, prelsoc_cap_lib, prelsoc_cap_bar, prelsoc_pv_mo_holder,
                 prelsoc_pv_immo_holder):
    """
    Prélèvements sociaux sur les revenus du capital
    """
    prelsoc_fon = self.cast_from_entity_to_role(prelsoc_fon_holder, role = VOUS)
    prelsoc_pv_immo = self.cast_from_entity_to_role(prelsoc_pv_immo_holder, role = VOUS)
    prelsoc_pv_mo = self.cast_from_entity_to_role(prelsoc_pv_mo_holder, role = VOUS)

    return prelsoc_fon + prelsoc_cap_lib + prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_pv_immo


def _check_csk(self, prelsoc_cap_bar_holder, prelsoc_pv_mo_holder, prelsoc_fon_holder):
    prelsoc_cap_bar = self.sum_by_entity(prelsoc_cap_bar_holder)
    prelsoc_pv_mo = self.cast_from_entity_to_role(prelsoc_pv_mo_holder, role = CHEF)
    prelsoc_pv_mo = self.sum_by_entity(prelsoc_pv_mo)
    prelsoc_fon = self.cast_from_entity_to_role(prelsoc_fon_holder, role = CHEF)
    prelsoc_fon = self.sum_by_entity(prelsoc_fon)

    return prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_fon


def _check_csg(self, csg_cap_bar_holder, csg_pv_mo_holder, csg_fon_holder):
    csg_cap_bar = self.sum_by_entity(csg_cap_bar_holder)
    csg_pv_mo = self.cast_from_entity_to_role(csg_pv_mo_holder, role = CHEF)
    csg_pv_mo = self.sum_by_entity(csg_pv_mo)
    csg_fon = self.cast_from_entity_to_role(csg_fon_holder, role = CHEF)
    csg_fon = self.sum_by_entity(csg_fon)

    return csg_cap_bar + csg_pv_mo + csg_fon


def _check_crds(self, crds_cap_bar_holder, crds_pv_mo_holder, crds_fon_holder):
    crds_cap_bar = self.sum_by_entity(crds_cap_bar_holder)
    crds_pv_mo = self.cast_from_entity_to_role(crds_pv_mo_holder, role = CHEF)
    crds_pv_mo = self.sum_by_entity(crds_pv_mo)
    crds_fon = self.cast_from_entity_to_role(crds_fon_holder, role = CHEF)
    crds_fon = self.sum_by_entity(crds_fon)

    return crds_cap_bar + crds_pv_mo + crds_fon
