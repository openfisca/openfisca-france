# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import datetime
import logging

from openfisca_core.accessors import law

from ..base import (dated_function, DatedFormulaColumn, FloatCol, FoyersFiscaux, Individus, EntityToPersonColumn,
    QUIFOY, reference_formula, SimpleFormulaColumn)


log = logging.getLogger(__name__)
VOUS = QUIFOY['vous']


# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont
#        en CG et BH en 2010

# temp = 0
# if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp
# else :
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
# a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds,
#      'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps,
#      'ir': P.ir, 'prelsoc': P.prelsoc}
# return Dicts2Object(**a)


def _mhsup(hsup):
    """
    Heures supplémentaires comptées négativement
    """
    return -hsup

############################################################################
# # Revenus du capital
############################################################################


# revenus du capital soumis au barème


@reference_formula
class csg_cap_bar(SimpleFormulaColumn):
    """Calcule la CSG sur les revenus du capital soumis au barème."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CSG sur les revenus du capital soumis au barème"
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"

    def function(self, rev_cap_bar, _P):
        return -rev_cap_bar * _P.csg.capital.glob

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class csg_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CSG sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = csg_cap_bar


@reference_formula
class crds_cap_bar(SimpleFormulaColumn):
    """Calcule la CRDS sur les revenus du capital soumis au barème."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CRDS sur les revenus du capital soumis au barème"
    url = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, rev_cap_bar, _P):
        return -rev_cap_bar * _P.crds.capital

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class crds_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CRDS sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = crds_cap_bar


@reference_formula
class prelsoc_cap_bar(DatedFormulaColumn):
    """Calcule le prélèvement social sur les revenus du capital soumis au barème"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème"
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    @dated_function(start = datetime.date(2002, 1, 1), stop = datetime.date(2005, 12, 31))
    def function_2002_2005(self, rev_cap_bar, P = law.prelsoc):
        total = P.base_pat
        return -rev_cap_bar * total

    @dated_function(start = datetime.date(2006, 1, 1), stop = datetime.date(2008, 12, 31))
    def function_2006_2008(self, rev_cap_bar, P = law.prelsoc):
        total = P.base_pat + P.add_pat
        return -rev_cap_bar * total

    @dated_function(start = datetime.date(2009, 1, 1), stop = datetime.date(2015, 12, 31))
    def function_2009_2015(self, rev_cap_bar, P = law.prelsoc):
        total = P.base_pat + P.add_pat + P.rsa
        return -rev_cap_bar * total

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class prelsoc_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = prelsoc_cap_bar


# plus-values de valeurs mobilières


def _csg_pv_mo(f3vg, _P):
    """
    Calcule la CSG sur les plus-values de cession mobilière
    """
    return -f3vg * _P.csg.capital.glob


def _crds_pv_mo(f3vg, _P):
    """
    Calcule la CRDS sur les plus-values de cession mobilière
    """
    return -f3vg * _P.crds.capital


def _prelsoc_pv_mo__2005(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc
    total = P.base_pat
    return -f3vg * total


def _prelsoc_pv_mo_2006_2008(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat
    return -f3vg * total


def _prelsoc_pv_mo_2009_(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -f3vg * total


# plus-values immobilières


def _csg_pv_immo(f3vz, _P):
    """
    Calcule la CSG sur les plus-values de cession immobilière
    """
    return -f3vz * _P.csg.capital.glob


def _crds_pv_immo(f3vz, _P):
    """
    Calcule la CRDS sur les plus-values de cession immobilière
    """
    return -f3vz * _P.crds.capital


def _prelsoc_pv_immo__2005(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat

    return -f3vz * total


def _prelsoc_pv_immo_2006_2008(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat

    return -f3vz * total


def _prelsoc_pv_immo_2009_(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -f3vz * total


# revenus fonciers


def _csg_fon(rev_cat_rfon, _P):
    '''
    Calcule la CSG sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer
    '''
    return -rev_cat_rfon * _P.csg.capital.glob


def _crds_fon(rev_cat_rfon, _P):
    '''
    Calcule la CRDS sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer
    '''
    return -rev_cat_rfon * _P.crds.capital


def _prelsoc_fon__2005(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer
    '''
    P = _P.prelsoc
    total = P.base_pat

    return -rev_cat_rfon * total


def _prelsoc_fon_2006_2008(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer
    '''
    P = _P.prelsoc
    total = P.base_pat + P.add_pat

    return -rev_cat_rfon * total


def _prelsoc_fon_2009_(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer
    '''
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -rev_cat_rfon * total


# revenus du capital soumis au prélèvement libératoire


@reference_formula
class csg_cap_lib(SimpleFormulaColumn):
    """Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CSG sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"

    def function(self, rev_cap_lib, _P):
        return -rev_cap_lib * _P.csg.capital.glob

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class csg_cap_lib_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CSG sur les revenus du capital soumis au prélèvement libératoire (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = csg_cap_lib


@reference_formula
class crds_cap_lib(SimpleFormulaColumn):
    """Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, rev_cap_lib, _P):
        return -rev_cap_lib * _P.crds.capital

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class crds_cap_lib_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = crds_cap_lib


@reference_formula
class prelsoc_cap_lib(SimpleFormulaColumn):
    """Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    def function(self, period, rev_cap_lib, prelsoc = law.prelsoc):
        year = period.start.year
        if year < 2006:
            total = prelsoc.base_pat
        elif year < 2009:
            total = prelsoc.base_pat + prelsoc.add_pat
        else:
            total = prelsoc.base_pat + prelsoc.add_pat + prelsoc.rsa
        return -rev_cap_lib * total

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class prelsoc_cap_lib_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = prelsoc_cap_lib


# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.csg.capital.nonimp
# #        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)
