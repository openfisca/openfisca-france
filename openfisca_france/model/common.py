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


def mark_weighted_percentiles(a, labels, weights, method, return_quantiles=False):
# from http://pastebin.com/KTLip9ee
    # a is an input array of values.
    # weights is an input array of weights, so weights[i] goes with a[i]
    # labels are the names you want to give to the xtiles
    # method refers to which weighted algorithm.
    #      1 for wikipedia, 2 for the stackexchange post.

    # The code outputs an array the same shape as 'a', but with
    # labels[i] inserted into spot j if a[j] falls in x-tile i.
    # The number of xtiles requested is inferred from the length of 'labels'.

    # First method, "vanilla" weights from Wikipedia article.
    if method == 1:

        # Sort the values and apply the same sort to the weights.
        N = len(a)
        sort_indx = argsort(a)
        tmp_a = a[sort_indx].copy()
        tmp_weights = weights[sort_indx].copy()

        # 'labels' stores the name of the x-tiles the user wants,
        # and it is assumed to be linearly spaced between 0 and 1
        # so 5 labels implies quintiles, for example.
        num_categories = len(labels)
        breaks = linspace(0, 1, num_categories + 1)

        # Compute the percentile values at each explicit data point in a.
        cu_weights = cumsum(tmp_weights)
        p_vals = (1.0 / cu_weights[-1]) * (cu_weights - 0.5 * tmp_weights)

        # Set up the output array.
        ret = repeat(0, len(a))
        if(len(a) < num_categories):
            return ret

        # Set up the array for the values at the breakpoints.
        quantiles = []

        # Find the two indices that bracket the breakpoint percentiles.
        # then do interpolation on the two a_vals for those indices, using
        # interp-weights that involve the cumulative sum of weights.
        for brk in breaks:
            if brk <= p_vals[0]:
                i_low = 0
                i_high = 0
            elif brk >= p_vals[-1]:
                i_low = N - 1
                i_high = N - 1
            else:
                for ii in range(N - 1):
                    if (p_vals[ii] <= brk) and (brk < p_vals[ii + 1]):
                        i_low = ii
                        i_high = ii + 1

            if i_low == i_high:
                v = tmp_a[i_low]
            else:
                # If there are two brackets, then apply the formula as per Wikipedia.
                v = (tmp_a[i_low] +
                    ((brk - p_vals[i_low]) / (p_vals[i_high] - p_vals[i_low])) * (tmp_a[i_high] - tmp_a[i_low]))

            # Append the result.
            quantiles.append(v)

        # Now that the weighted breakpoints are set, just categorize
        # the elements of a with logical indexing.
        for i in range(0, len(quantiles) - 1):
            lower = quantiles[i]
            upper = quantiles[i + 1]
            ret[and_(a >= lower, a < upper)] = labels[i]

        #make sure upper and lower indices are marked
        ret[a <= quantiles[0]] = labels[0]
        ret[a >= quantiles[-1]] = labels[-1]

        return ret

    # The stats.stackexchange suggestion.
    elif method == 2:

        N = len(a)
        sort_indx = argsort(a)
        tmp_a = a[sort_indx].copy()
        tmp_weights = weights[sort_indx].copy()

        num_categories = len(labels)
        breaks = linspace(0, 1, num_categories + 1)

        cu_weights = cumsum(tmp_weights)

        # Formula from stats.stackexchange.com post.
        s_vals = [0.0]
        for ii in range(1, N):
            s_vals.append(ii * tmp_weights[ii] + (N - 1) * cu_weights[ii - 1])
        s_vals = asarray(s_vals)

        # Normalized s_vals for comapring with the breakpoint.
        norm_s_vals = (1.0 / s_vals[-1]) * s_vals

        # Set up the output variable.
        ret = repeat(0, N)
        if(N < num_categories):
            return ret

        # Set up space for the values at the breakpoints.
        quantiles = []

        # Find the two indices that bracket the breakpoint percentiles.
        # then do interpolation on the two a_vals for those indices, using
        # interp-weights that involve the cumulative sum of weights.
        for brk in breaks:
            if brk <= norm_s_vals[0]:
                i_low = 0
                i_high = 0
            elif brk >= norm_s_vals[-1]:
                i_low = N - 1
                i_high = N - 1
            else:
                for ii in range(N - 1):
                    if (norm_s_vals[ii] <= brk) and (brk < norm_s_vals[ii + 1]):
                        i_low = ii
                        i_high = ii + 1

            if i_low == i_high:
                v = tmp_a[i_low]
            else:
                # Interpolate as in the method 1 method, but using the s_vals instead.
                v = (tmp_a[i_low] +
                    (((brk * s_vals[-1]) - s_vals[i_low]) /
                        (s_vals[i_high] - s_vals[i_low])) * (tmp_a[i_high] - tmp_a[i_low]))
            quantiles.append(v)

        # Now that the weighted breakpoints are set, just categorize
        # the elements of a as usual.
        for i in range(0, len(quantiles) - 1):
            lower = quantiles[i]
            upper = quantiles[i + 1]
            ret[and_(a >= lower, a < upper)] = labels[i]

        #make sure upper and lower indices are marked
        ret[a <= quantiles[0]] = labels[0]
        ret[a >= quantiles[-1]] = labels[-1]

        if return_quantiles:
            return ret, quantiles
        else:
            return ret


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


def _typ_men(isol, af_nbenf):
    '''
    type de menage
    'men'
    TODO: prendre les enfants du ménages et non ceux de la famille
    '''
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


def _decile(nivvie, champm, wprm):
    '''
    Décile de niveau de vie disponible
    'men'
    '''
    labels = arange(1, 11)
    method = 2
    decile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
#    print values
#    print len(values)
#    print (nivvie*champm).min()
#    print (nivvie*champm).max()
#    print decile.min()
#    print decile.max()
#    print (nivvie*(decile==1)*champm*wprm).sum()/( ((decile==1)*champm*wprm).sum() )
    del values
    return decile * champm


def _decile_net(nivvie_net, champm, wprm):
    '''
    Décile de niveau de vie net
    'men'
    '''
    labels = arange(1, 11)
    method = 2
    decile, values = mark_weighted_percentiles(nivvie_net, labels, wprm * champm, method, return_quantiles = True)
    return decile * champm


def _pauvre40(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 50% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .4 * values[1]
    return (nivvie <= threshold) * champm


def _pauvre50(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 50% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .5 * values[1]
    return (nivvie <= threshold) * champm


def _pauvre60(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 60% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .6 * values[1]
    return (nivvie <= threshold) * champm


def _weight_ind(self, wprm_holder):
    return self.cast_from_entity_to_roles(wprm_holder)


def _weight_fam(self, weight_ind_holder):
    return self.filter_role(weight_ind_holder, role = CHEF)


def _weight_foy(self, weight_ind_holder):
    return self.filter_role(weight_ind_holder, role = VOUS)
