# -*- coding: utf-8 -*-

from __future__ import division

import logging

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


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
# a = {'salaire_imposable':sal, 'pat':pat, 'csg':csg, 'crds':crds,
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


class csg_cap_bar(Variable):
    """Calcule la CSG sur les revenus du capital soumis au barème."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CSG sur les revenus du capital soumis au barème"
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_bar = simulation.calculate_add('rev_cap_bar', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cap_bar * _P.csg.capital.glob


class csg_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CSG sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = csg_cap_bar


class crds_cap_bar(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au barème."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CRDS sur les revenus du capital soumis au barème"
    url = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_bar = simulation.calculate_add('rev_cap_bar', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cap_bar * _P.crds.capital


class crds_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CRDS sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = crds_cap_bar


class prelsoc_cap_bar(DatedVariable):
    """Calcule le prélèvement social sur les revenus du capital soumis au barème"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème"
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_2002_2005(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_bar = simulation.calculate_add('rev_cap_bar', period)
        P = simulation.legislation_at(period.start).prelsoc

        total = P.base_pat
        return period, -rev_cap_bar * total

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_2006_2008(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_bar = simulation.calculate_add('rev_cap_bar', period)
        P = simulation.legislation_at(period.start).prelsoc

        total = P.base_pat + P.add_pat
        return period, -rev_cap_bar * total

    @dated_function(start = date(2009, 1, 1))
    def function_2009_2015(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_bar = simulation.calculate_add('rev_cap_bar', period)
        P = simulation.legislation_at(period.start).prelsoc

        total = P.base_pat + P.add_pat + P.rsa
        return period, -rev_cap_bar * total


class prelsoc_cap_bar_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Prélèvements sociaux sur les revenus du capital soumis au barème (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = prelsoc_cap_bar


# plus-values de valeurs mobilières


class csg_pv_mo(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CSG sur les plus-values de cession de valeurs mobilières"
    url = "http://vosdroits.service-public.fr/particuliers/F21618.xhtml"

    def function(self, simulation, period):
        """
        Calcule la CSG sur les plus-values de cession mobilière
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        _P = simulation.legislation_at(period.start)

        return period, -f3vg * _P.csg.capital.glob


class crds_pv_mo(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CRDS sur les plus-values de cession de valeurs mobilières"
    url = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, simulation, period):
        """
        Calcule la CRDS sur les plus-values de cession mobilière
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        _P = simulation.legislation_at(period.start)

        return period, -f3vg * _P.crds.capital


class prelsoc_pv_mo(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values
        de cession de valeurs mobilières
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat
        return period, -f3vg * total

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values
        de cession de valeurs mobilières
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat
        return period, -f3vg * total

    @dated_function(start = date(2009, 1, 1))
    def function_20090101_20151231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values de cession de valeurs mobilières
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat + P.rsa
        return period, -f3vg * total


# plus-values immobilières


class csg_pv_immo(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CSG sur les plus-values immobilières"
    url = "http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e"

    def function(self, simulation, period):
        """
        Calcule la CSG sur les plus-values de cession immobilière
        """
        period = period.this_year
        f3vz = simulation.calculate('f3vz', period)
        _P = simulation.legislation_at(period.start)

        return period, -f3vz * _P.csg.capital.glob


class crds_pv_immo(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CRDS sur les plus-values immobilières"
    url = "http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, simulation, period):
        """
        Calcule la CRDS sur les plus-values de cession immobilière
        """
        period = period.this_year
        f3vz = simulation.calculate('f3vz', period)
        _P = simulation.legislation_at(period.start)

        return period, -f3vz * _P.crds.capital


class prelsoc_pv_immo(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les plus-values immobilières"
    url = "http://www.pap.fr/argent/impots/les-plus-values-immobilieres/a1314/l-imposition-de-la-plus-value-immobiliere"

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        period = period.this_year
        f3vz = simulation.calculate('f3vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat

        return period, -f3vz * total

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        period = period.this_year
        f3vz = simulation.calculate('f3vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat

        return period, -f3vz * total

    @dated_function(start = date(2009, 1, 1))
    def function_20090101_20151231(self, simulation, period):
        """
        Calcule le prélèvement social sur les plus-values de cession immobilière
        """
        period = period.this_year
        f3vz = simulation.calculate('f3vz', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat + P.rsa
        return period, -f3vz * total


# revenus fonciers


class csg_fon(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CSG sur les revenus fonciers"
    url = "http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e"

    def function(self, simulation, period):
        '''
        Calcule la CSG sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cat_rfon * _P.csg.capital.glob


class crds_fon(Variable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"CRDS sur les revenus fonciers"
    url = "http://vosdroits.service-public.fr/particuliers/F2329.xhtml"

    def function(self, simulation, period):
        '''
        Calcule la CRDS sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cat_rfon * _P.crds.capital


class prelsoc_fon(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les revenus fonciers"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    @dated_function(start = date(2002, 1, 1), stop = date(2005, 12, 31))
    def function_20020101_20051231(self, simulation, period):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat

        return period, -rev_cat_rfon * total

    @dated_function(start = date(2006, 1, 1), stop = date(2008, 12, 31))
    def function_20060101_20081231(self, simulation, period):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat

        return period, -rev_cat_rfon * total

    @dated_function(start = date(2009, 1, 1))
    def function_20090101_20151231(self, simulation, period):
        '''
        Calcule le prélèvement social sur les revenus fonciers
        Attention : assiette CSG = asiette IR valable 2006-2014 mais pourrait changer
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        _P = simulation.legislation_at(period.start)

        P = _P.prelsoc
        total = P.base_pat + P.add_pat + P.rsa
        return period, -rev_cat_rfon * total


# revenus du capital soumis au prélèvement libératoire


class csg_cap_lib(Variable):
    """Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CSG sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_généralisée"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_lib = simulation.calculate_add('rev_cap_lib', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cap_lib * _P.csg.capital.glob


class csg_cap_lib_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CSG sur les revenus du capital soumis au prélèvement libératoire (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = csg_cap_lib


class crds_cap_lib(Variable):
    """Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_lib = simulation.calculate_add('rev_cap_lib', period)
        _P = simulation.legislation_at(period.start)

        return period, -rev_cap_lib * _P.crds.capital


class crds_cap_lib_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = crds_cap_lib


class prelsoc_cap_lib(Variable):
    """Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire."""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire"
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"  # noqa

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        rev_cap_lib = simulation.calculate_add('rev_cap_lib', period)
        prelsoc = simulation.legislation_at(period.start).prelsoc

        start_year = period.start.year
        if start_year < 2006:
            total = prelsoc.base_pat
        elif start_year < 2009:
            total = prelsoc.base_pat + prelsoc.add_pat
        else:
            total = prelsoc.base_pat + prelsoc.add_pat + prelsoc.rsa
        return period, -rev_cap_lib * total


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
