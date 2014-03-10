# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

from numpy import maximum as max_

from .data import QUIMEN, QUIFOY


PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


def _tax_hab(self, zthabm, aah, aspa, asi, age_holder, isf_tot_holder, rfr_holder, statmarit_holder, nbptr_holder, _P):
    '''
    Taxe d'habitation
    'men'

    Eligibilité:
    - âgé de plus de 60 ans, non soumis à l'impôt de solidarité sur la fortune (ISF) en n-1
    - veuf quel que soit votre âge et non soumis à l'impôt de solidarité sur la fortune (ISF) n-1
    - titulaire de l'allocation de solidarité aux personnes âgées (Aspa)  ou de l'allocation supplémentaire d'invalidité (Asi),
    bénéficiaire de l'allocation aux adultes handicapés (AAH),
    atteint d'une infirmité ou d'une invalidité vous empêchant de subvenir à vos besoins par votre travail.
    '''
    isf_tot = self.cast_from_entity_to_role(isf_tot_holder, role = VOUS)
    isf_tot = self.sum_by_roles(isf_tot)
    rfr = self.cast_from_entity_to_role(rfr_holder, role = VOUS)
    rfr = self.sum_by_roles(rfr)
    nbptr = self.cast_from_entity_to_role(nbptr_holder, role = VOUS)
    nbptr = self.sum_by_roles(nbptr)
    age = self.filter_role(age_holder, role = PREF)
    statmarit = self.filter_role(statmarit_holder, role = PREF)

    P = _P.cotsoc.gen
    concern = ((age >= 60) + (statmarit == 4))*(isf_tot  <= 0) + (aspa > 0) + (asi > 0)
    seuil_th = P.plaf_th_1 + P.plaf_th_supp*(max_(0, (nbptr-1)/2))
    print len(concern), len(rfr), len(seuil_th), len(asi > 0), len(aspa > 0)
    elig = concern * (rfr < seuil_th) + (asi > 0) + (aspa > 0)
    return -zthabm * elig
