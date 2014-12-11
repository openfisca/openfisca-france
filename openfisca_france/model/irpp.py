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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import logging

from numpy import (datetime64, logical_and as and_, logical_not as not_, logical_or as or_, logical_xor as xor_,
    maximum as max_, minimum as min_, round)

from .base import *


log = logging.getLogger(__name__)


# TODO: contribution exceptionnelle sur les hauts revenus (>=2011)
# TODO: 8ti et 8tk (cerfa 2047)
# TODO: CSG, CRDS et prélèvements sociaux sur revenu du patrimione, d'activité et de remplacement
# TODO: finir RPNS (prise en compte des plafonds / cases non codées : codées pour certaines années mais pas pour
# d'autres - car des cases sont réutilisées pour des variables différentes suivant les années)

# zetrf = zeros(taille)
# jveuf = zeros(taille, dtype = bool)
# Reprise du crédit d'impôt en faveur des jeunes, des accomptes et des versements mensues de prime pour l'emploi
# reprise = zeros(taille) # TODO : reprise=J80
# Pcredit = P.credits_impots
# if hasattr(P.reductions_impots,'saldom'): Pcredit.saldom =  P.reductions_impots.saldom
# credits_impot = Credits(Pcredit, table)
# Réduction d'impôt
# reductions = Reductions(IPnet, P.reductions_impots)

# def mcirra():
#    # impôt sur le revenu
#    mcirra = -((IMP<=-8)*IMP)
#    mciria = max_(0,(IMP>=0)*IMP)
# #        mciria = max_(0,(IMP>=0)*IMP - credimp_etranger - cont_rev_loc - ( f8to + f8tb + f8tc ))
#
#    # Dans l'ERFS, les prelevement libératoire sur les montants non déclarés
#    # sont intégrés. Pas possible de le recalculer.
#
#    # impot sur le revenu du foyer (hors prélèvement libératoire, revenus au quotient)
#    irpp   = -(mciria + ppetot - mcirra )


###############################################################################
# # Initialisation de quelques variables utiles pour la suite
###############################################################################


@reference_formula
class age(AlternativeFormulaColumn):
    column = AgeCol(val_type = "age")
    entity_class = Individus
    label = u"Âge (en années)"

    @alternative_function()
    def age_from_birth(self, birth, period):
        return (datetime64(period.date) - birth).astype('timedelta64[Y]')

    @alternative_function()
    def age_from_agem(self, agem):
        return agem // 12

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


def _age_from_agem(agem):
    return agem // 12


def _age_from_birth(birth, period):
    return (datetime64(period.date) - birth).astype('timedelta64[Y]')


def _agem_from_age(age):
    return age * 12


def _agem_from_birth(birth, period):
    return (datetime64(period.date) - birth).astype('timedelta64[M]')


@reference_formula
class nb_adult(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_adult"

    def function(self, marpac, celdiv, veuf):
        return 2 * marpac + 1 * (celdiv | veuf)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class nb_pac(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"nb_pac"

    def function(self, nbF, nbJ, nbR):
        return nbF + nbJ + nbR

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class enfant_a_charge(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge non marié, de moins de 18 ans au 1er janvier de l'année de perception des" \
        u" revenus, ou né durant la même année, ou handicapés quel que soit son âge"

    def function(self, age, alt, inv, quifoy):
        return and_(and_(quifoy >= 2, or_(age < 18, inv)), not_(alt))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class nbF(PersonToEntityColumn):
    cerfa_field = u'F'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge  non mariés, de moins de 18 ans au 1er janvier de l'année de perception des" \
        u" revenus, ou nés durant la même année ou handicapés quel que soit leur âge"
    operation = 'add'
    variable = enfant_a_charge


@reference_formula
class nombre_enfants_a_charge_menage(PersonToEntityColumn):
    entity_class = Menages
    label = u"Nombre d'enfants à charge  non mariés, de moins de 18 ans au 1er janvier de l'année de perception des" \
        u" revenus, ou nés durant la même année ou handicapés quel que soit leur âge"
    operation = 'add'
    variable = enfant_a_charge


@reference_formula
class enfant_a_charge_invalide(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge titulaire de la carte d'invalidité"

    def function(self, alt, inv, quifoy):
        return and_(and_(quifoy >= 2, inv), not_(alt))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class nbG(PersonToEntityColumn):
    cerfa_field = u'G'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge titulaires de la carte d'invalidité"
    operation = 'add'
    variable = enfant_a_charge_invalide


@reference_formula
class enfant_a_charge_garde_alternee(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge en résidence alternée, non marié, de moins de 18 ans au 1er janvier de l'année de" \
        u" perception des revenus, ou né durant la même année ou handicapés quel que soit son âge"

    def function(self, age, alt, inv, quifoy):
        return and_(and_(quifoy >= 2, or_(age < 18, inv)), alt)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class nbH(PersonToEntityColumn):
    cerfa_field = u'H'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de" \
        u" l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge"
    operation = 'add'
    variable = enfant_a_charge_garde_alternee


@reference_formula
class enfant_a_charge_garde_alternee_invalide(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge en résidence alternée titulaire de la carte d'invalidité"

    def function(self, alt, inv, quifoy):
        return and_(and_(quifoy >= 2, inv), alt)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class nbI(PersonToEntityColumn):
    cerfa_field = u'I'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité"
    operation = 'add'
    variable = enfant_a_charge_garde_alternee_invalide


@reference_formula
class enfant_majeur_celibataire_sans_enfant(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant majeur célibataire sans enfant"

    def function(self, age, inv, quifoy):
        return and_(and_(quifoy >= 2, age >= 18), not_(inv))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class nbJ(PersonToEntityColumn):
    cerfa_field = u'J'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants majeurs célibataires sans enfant"
    operation = 'add'
    variable = enfant_majeur_celibataire_sans_enfant


@reference_formula
class nombre_enfants_majeurs_celibataires_sans_enfant(PersonToEntityColumn):
    entity_class = Menages
    label = u"Nombre d'enfants majeurs célibataires sans enfant"
    operation = 'add'
    variable = enfant_majeur_celibataire_sans_enfant


@reference_formula
class marpac(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"marpac"

    def function(self, statmarit_holder):
        '''
        Marié (1) ou Pacsé (5)
        'foy'
        '''
        statmarit = self.filter_role(statmarit_holder, role = VOUS)

        return (statmarit == 1) | (statmarit == 5)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class celdiv(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"celdiv"

    def function(self, statmarit_holder):
        '''
        Célibataire (2) ou divorcé (3)
        'foy'
        '''
        statmarit = self.filter_role(statmarit_holder, role = VOUS)

        return (statmarit == 2) | (statmarit == 3)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class veuf(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"veuf"

    def function(self, statmarit_holder):
        '''
        Veuf (4)
        'foy'
        '''
        statmarit = self.filter_role(statmarit_holder, role = VOUS)

        return statmarit == 4

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class jveuf(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"jveuf"

    def function(self, statmarit_holder):
        '''
        Jeune Veuf
        'foy'
        '''
        statmarit = self.filter_role(statmarit_holder, role = VOUS)

        return statmarit == 6

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



###############################################################################
# # Revenus catégoriels
###############################################################################


@reference_formula
class rev_sal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_sal"

    def function(self, sal, cho):
        '''
        Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)
        'ind'
        '''
        return sal + cho

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class salcho_imp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"salcho_imp"

    def function(self, rev_sal, cho_ld, fra, abatpro =  law.ir.tspr.abatpro):
        """
        Salaires après abattements
        'ind'
        """
        amin = abatpro.min * not_(cho_ld) + abatpro.min2 * cho_ld
        abatfor = round(min_(max_(abatpro.taux * rev_sal, amin), abatpro.max))
        return (fra > abatfor) * (rev_sal - fra) + (fra <= abatfor) * max_(0, rev_sal - abatfor)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_act_sal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_act_sal"

    def function(self, sali):
        ''' Revenus d'activités salariées'''
        return sali #TODO: vérifier cette définition

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class rev_act_nonsal(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_act_nonsal"

    def function(self, rpns_i):
        ''' Revenus d'activités non salariées '''
        return rpns_i #TODO: vérifier cette définition

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_act(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_act"

    def function(self, rev_act_nonsal, rev_act_sal):
        ''' Revenus d'activités '''
        return rev_act_nonsal + rev_act_sal

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_pen(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rev_pen"

    def function(self, alr, alr_decl, rst):
        """
        Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)
        'ind'
        """
        return alr * alr_decl + rst

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class pen_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"pen_net"

    def function(self, rev_pen, abatpen =  law.ir.tspr.abatpen):
        """
        Pensions après abattements
        'ind'
        """
    #    TODO: problème car les pensions sont majorées au niveau du foyer
    #    d11 = ( AS + BS + CS + DS + ES +
    #            AO + BO + CO + DO + EO )
    #    penv2 = (d11-f11> abatpen.max)*(penv + (d11-f11-abatpen.max)) + (d11-f11<= abatpen.max)*penv
    #    Plus d'abatement de 20% en 2006
        return max_(0, rev_pen - round(max_(abatpen.taux * rev_pen , abatpen.min)))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

#    return max_(0, rev_pen - min_(round(max_(abatpen.taux*rev_pen , abatpen.min)), abatpen.max))  le max se met au niveau du foyer

@reference_formula
class indu_plaf_abat_pen(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"indu_plaf_abat_pen"

    def function(self, rev_pen_holder, pen_net_holder, abatpen =  law.ir.tspr.abatpen):
        """
        Plafonnement de l'abattement de 10% sur les pensions du foyer
        'foy'
        """
        pen_net = self.sum_by_entity(pen_net_holder)
        rev_pen = self.sum_by_entity(rev_pen_holder)

        abat = rev_pen - pen_net
        return abat - min_(abat, abatpen.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class abat_sal_pen(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"abat_sal_pen"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)

    def function(self, salcho_imp, pen_net, abatsalpen =  law.ir.tspr.abatsalpen):
        """
        Abattement de 20% sur les salaires
        'ind'
        """
        return min_(abatsalpen.taux * max_(salcho_imp + pen_net, 0), abatsalpen.max)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class sal_pen_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"sal_pen_net"

    def function(self, salcho_imp, pen_net, abat_sal_pen):
        """
        Salaires et pensions après abattement de 20% sur les salaires
        'ind'
        """
        return salcho_imp + pen_net - abat_sal_pen

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rto(SimpleFormulaColumn):
    """Rentes viagères à titre onéreux (avant abattements)"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Rentes viagères (rentes à titre onéreux)"
    url = u"http://fr.wikipedia.org/wiki/Rente_viagère"

    def function(self, f1aw, f1bw, f1cw, f1dw):
        return f1aw + f1bw + f1cw + f1dw

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class rto_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Rentes viagères (rentes à titre onéreux) (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = rto


@reference_formula
class rto_net(SimpleFormulaColumn):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Rentes viagères après abattements"
    url = u"http://www.lafinancepourtous.fr/Vie-professionnelle-et-retraite/Retraite/Epargne-retraite/La-rente-viagere/La-fiscalite-de-la-rente-viagere"  # noqa

    def function(self, f1aw, f1bw, f1cw, f1dw, abatviag = law.ir.tspr.abatviag):
        return round(abatviag.taux1 * f1aw + abatviag.taux2 * f1bw + abatviag.taux3 * f1cw + abatviag.taux4 * f1dw)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class rto_net_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Rentes viagères après abattements (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = rto_net


@reference_formula
class tspr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"tspr"

    def function(self, sal_pen_net, rto_net_declarant1):
        '''
        Traitements salaires pensions et rentes individuelles
        'ind'
        '''
        return sal_pen_net + rto_net_declarant1

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat_pv(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Plus-values"
    start_date = date(2013, 1, 1)
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, f3vg, f3vh):
        return f3vg - f3vh

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat_tspr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Salaires, pensions et rentes"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, tspr_holder, indu_plaf_abat_pen):
        '''
        Traitemens salaires pensions et rentes
        'foy'
        '''
        tspr = self.sum_by_entity(tspr_holder)

        return tspr + indu_plaf_abat_pen

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class deficit_rcm(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Deficit capitaux mobiliers"
    start_date = date(2009, 1, 1)
    url = "http://www.lefigaro.fr/impots/2008/04/25/05003-20080425ARTFIG00254-les-subtilites-des-revenus-de-capitaux-mobiliers-.php"

    def function(self, _P, f2aa, f2al, f2am, f2an, f2aq, f2ar):
        return f2aa + f2al + f2am + f2an + f2aq + f2ar

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat_rvcm(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Capitaux"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    @dated_function(start = date(2002, 1, 1), stop = date(2004, 12, 31))
    def function_20020101_20041231(self, marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2gr, f2tr, _P, finpfl =  law.ir.autre.finpfl, rvcm =  law.ir.rvcm):
        """
        Revenus des valeurs et capitaux mobiliers
        """
    
        f2dc_bis = f2dc
        f2tr_bis = f2tr
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + marpac))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)
    
        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + marpac)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)
    
        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a
    
        DEF = deficit_rcm
        return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    @dated_function(start = date(2005, 1, 1), stop = date(2012, 12, 31))
    def function_20050101_20121231(self, marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2gr, f2tr, finpfl =  law.ir.autre.finpfl, rvcm =  law.ir.rvcm):
        """
        Revenus des valeurs et capitaux mobiliers
        """
    
        # Add f2da to f2dc and f2ee to f2tr when no PFL
        f2dc_bis = f2dc
        f2tr_bis = f2tr
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + marpac))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)
    
        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + marpac)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)
    
        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a
    
        DEF = deficit_rcm
        return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    @dated_function(start = date(2013, 1, 1), stop = date(2015, 12, 31))
    def function_20130101_20151231(self, marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2tr, f2da, f2ee, finpfl =  law.ir.autre.finpfl, rvcm =  law.ir.rvcm):
        """
        Revenus des valeurs et capitaux mobiliers
        """
        # Add f2da to f2dc and f2ee to f2tr when no PFL
        f2dc_bis = f2dc + f2da  # TODO: l'abattement de 40% est déduit uniquement en l'absence de revenus déclarés case 2DA
        f2tr_bis = f2tr + f2ee
    
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + marpac))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2fu * (1 - rvcm.abatmob_taux)
    
        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + marpac)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)
    
        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a
    
        DEF = deficit_rcm
        return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')







@reference_formula
class rfr_rvcm(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rfr_rvcm"

    def function(self, marpac, f2dc, f2ts, f2ca, f2gr, f2fu, f2da, finpfl =  law.ir.autre.finpfl, rvcm =  law.ir.rvcm):
        '''
        Abattements sur rvcm à réintégrer dans le revenu fiscal de référence
        '''
        if finpfl:
            f2dc_bis = f2dc + f2da
        else:
            f2dc_bis = f2dc

        # Calcul de i121
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)

        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + marpac)
        i121 = - min_(0, rev - h12)
        return max_((rvcm.abatmob_taux) * (f2dc_bis + f2fu) - i121, 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat_rfon(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Foncier"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, f4ba, f4bb, f4bc, f4bd, f4be, microfoncier =  law.ir.microfoncier):
        """
        Revenus fonciers
        TODO: add assert in validator
        """
        # # Calcul du revenu catégoriel
        if ((f4be != 0) & ((f4ba != 0) | (f4bb != 0) | (f4bc != 0))).any():
            log.error(("Problème de déclarations des revenus : incompatibilité de la déclaration des revenus fonciers (f4ba, f4bb, f4bc) et microfonciers (f4be)"))

        a13 = f4ba + f4be - microfoncier.taux * f4be * (f4be <= microfoncier.max)
        b13 = f4bb
        c13 = a13 - b13
        d13 = f4bc
        e13 = c13 - d13 * (c13 >= 0)
        f13 = f4bd * (e13 >= 0)
        g13 = max_(0, e13 - f13)
        rev_cat_rfon = (c13 >= 0) * (g13 + e13 * (e13 < 0)) - (c13 < 0) * d13
        return rev_cat_rfon

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat_rpns(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Rpns"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, nbnc_pvce_holder, mbic_mvct, rpns_i_holder, defrag, defacc, defncn, defmeu):
        '''
        Revenus personnels non salariés
        'foy'
        '''
        return self.sum_by_entity(rpns_i_holder) - self.sum_by_entity(nbnc_pvce_holder) - defrag - defncn - defacc - defmeu - mbic_mvct

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cat(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenus catégoriels"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, rev_cat_tspr, rev_cat_rvcm, rev_cat_rfon, rev_cat_rpns, rev_cat_pv):
        '''
        Revenus Categoriels
        '''
        return rev_cat_tspr + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns + rev_cat_pv

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


@reference_formula
class deficit_ante(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déficit global antérieur"
    url = "http://impotsurlerevenu.org/declaration-de-revenus-fonciers-2044/796-deficits-anterieurs-restant-a-imputer-cadre-450.php"

    def function(self, f6fa, f6fb, f6fc, f6fd, f6fe, f6fl):
        '''
        Déficits antérieurs
        '''
        return f6fa + f6fb + f6fc + f6fd + f6fe + f6fl

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rbg(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu brut global"
    url = "http://www.documentissime.fr/dossiers-droit-pratique/dossier-19-l-impot-sur-le-revenu-les-modalites-generales-d-imposition/la-determination-du-revenu-imposable/le-revenu-brut-global.html"

    def function(self, rev_cat, deficit_ante, f6gh, nbic_impm_holder, nacc_pvce_holder, cga =  law.ir.rpns.cga_taux2):
        '''Revenu brut global
        '''
        # (Total 17)
        # sans les revenus au quotient
        nacc_pvce = self.sum_by_entity(nacc_pvce_holder)
        return max_(0,
                    rev_cat + f6gh + (self.sum_by_entity(nbic_impm_holder) + nacc_pvce) * (1 + cga) - deficit_ante)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class csg_deduc_patrimoine(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, f6de):
        '''
        CSG déductible sur les revenus du patrimoine
        http://bofip.impots.gouv.fr/bofip/887-PGP
        '''
        return max_(f6de, 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class csg_deduc_patrimoine_simulated(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine simulée"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, rev_cat_rfon, rev_cap_bar, rto, taux =  law.csg.capital.deduc):
        '''
        Cette fonction simule le montant mentionné dans la case f6de de la déclaration 2042
        http://bofip.impots.gouv.fr/bofip/887-PGP
        '''
        patrimoine_deduc = rev_cat_rfon + rev_cap_bar + rto
        return taux * patrimoine_deduc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class csg_deduc(SimpleFormulaColumn):  # f6de
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, rbg, csg_deduc_patrimoine):
        # f6de
        ''' CSG déductible '''
        # min_(f6de, max_(rbg, 0))
        return min_(csg_deduc_patrimoine, max_(rbg, 0))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rng(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu net global"
    url = "http://impotsurlerevenu.org/definitions/114-revenu-net-global.php"

    def function(self, rbg, csg_deduc, charges_deduc):
        ''' Revenu net global (total 20) '''
        return max_(0, rbg - csg_deduc - charges_deduc)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rni(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu net imposable"
    url = "http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php"

    def function(self, rng, abat_spe):
        ''' Revenu net imposable ou déficit à reporter'''
        return rng - abat_spe

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ir_brut(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ir_brut"

    def function(self, nbptr, taux_effectif, rni, bareme =  law.ir.bareme):
        '''
        Impot sur le revenu avant non imposabilité et plafonnement du quotient
        'foy'
        '''
        return (taux_effectif == 0) * nbptr * bareme.calc(rni / nbptr) + taux_effectif * rni

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ir_ss_qf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ir_ss_qf"

    def function(self, ir_brut, rni, nb_adult, bareme =  law.ir.bareme):
        '''
        Impôt sans quotient familial
        '''
        A = bareme.calc(rni / nb_adult)
        return nb_adult * A

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ir_plaf_qf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ir_plaf_qf"

    def function(self, ir_brut, ir_ss_qf, nb_adult, nb_pac, nbptr, marpac, veuf, jveuf, celdiv, caseE, caseF, caseG, caseH, caseK, caseN, caseP, caseS, caseT, caseW, nbF, nbG, nbH, nbI, nbR, plafond_qf =  law.ir.plafond_qf):
        '''
        Impôt après plafonnement du quotient familial et réduction complémentaire
        '''
        A = ir_ss_qf
        I = ir_brut

        aa0 = (nbptr - nb_adult) * 2  # nombre de demi part excédant nbadult
        # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
        # diviser par 2)
        aa1 = min_((nbptr - 1) * 2, 2) / 2  # deux première demi part excédants une part
        aa2 = max_((nbptr - 2) * 2, 0)  # nombre de demi part restantes
        # celdiv parents isolés
        condition61 = celdiv & caseT
        B1 = plafond_qf.celib_enf * aa1 + plafond_qf.marpac * aa2
        # tous les autres
        B2 = plafond_qf.marpac * aa0  # si autre
        # celdiv, veufs (non jveuf) vivants seuls et autres conditions
        # TODO: année en dur... pour caseH
        condition63 = (celdiv | (veuf & not_(jveuf))) & not_(caseN) & (nb_pac == 0) & (caseK | caseE) & (caseH < 1981)
        B3 = plafond_qf.celib

        B = B1 * condition61 + \
            B2 * (not_(condition61 | condition63)) + \
            B3 * (condition63 & not_(condition61))
        C = max_(0, A - B)
        # Impôt après plafonnement
        IP0 = max_(I, C)

        # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
        # pas de réduction complémentaire
        condition62a = (I >= C)
        # réduction complémentaire
        condition62b = (I < C)
        # celdiv veuf
        condition62caa0 = (celdiv | (veuf & not_(jveuf)))
        condition62caa1 = (nb_pac == 0) & (caseP | caseG | caseF | caseW)
        condition62caa2 = caseP & ((nbF - nbG > 0) | (nbH - nbI > 0))
        condition62caa3 = not_(caseN) & (caseE | caseK) & (caseH >= 1981)
        condition62caa = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
        # marié pacs
        condition62cab = (marpac | jveuf) & caseS & not_(caseP | caseF)
        condition62ca = (condition62caa | condition62cab)

        # plus de 590 euros si on a des plus de
        condition62cb = ((nbG + nbR + nbI) > 0) | caseP | caseF
        D = plafond_qf.reduc_postplafond * (condition62ca + ~condition62ca * condition62cb * (
            1 * caseP + 1 * caseF + nbG + nbR + nbI / 2))

        E = max_(0, A - I - B)
        Fo = D * (D <= E) + E * (E < D)
        IP1 = IP0 - Fo

        # TODO: 6.3 Cas particulier: Contribuables domiciliés dans les DOM.
        # conditionGuadMarReu =
        # conditionGuyane=
        # conitionDOM = conditionGuadMarReu | conditionGuyane
        # postplafGuadMarReu = 5100
        # postplafGuyane = 6700
        # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1)

        # Récapitulatif

        return condition62a * IP0 + condition62b * IP1  # IP2 si DOM

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class avantage_qf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"avantage_qf"

    def function(self, ir_ss_qf, ir_plaf_qf):
        return ir_ss_qf - ir_plaf_qf

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class decote(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"decote"

    def function(self, ir_plaf_qf, decote =  law.ir.decote):
        '''
        Décote
        '''
        return (ir_plaf_qf < decote.seuil) * (decote.seuil - ir_plaf_qf) * 0.5

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class nat_imp(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"nat_imp"

    def function(self, iai, credits_impot, cehr):
        '''
        Renvoie True si le foyer est imposable, False sinon
        '''
        # def _nat_imp(rni, nbptr, non_imposable = law.ir.non_imposable):
        # seuil = non_imposable.seuil + (nbptr - 1)*non_imposable.supp
        return (iai - credits_impot + cehr) > 0

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ip_net(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ip_net"

    def function(self, ir_plaf_qf, cncn_info_holder, decote, taux =  law.ir.rpns.taux16):
        '''
        irpp après décote
        '''
        return max_(0, ir_plaf_qf + self.sum_by_entity(cncn_info_holder) * taux - decote)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class iaidrdi(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"iaidrdi"

    def function(self, ip_net, reductions):
        '''
        Impôt après imputation des réductions d'impôt
        '''
        return ip_net - reductions

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cont_rev_loc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"cont_rev_loc"
    start_date = date(2001, 1, 1)

    def function(self, f4bl, crl =  law.ir.crl):
        '''
        Contribution sur les revenus locatifs
        '''
        return round(crl.taux * (f4bl >= crl.seuil) * f4bl)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class teicaa(SimpleFormulaColumn):  # f5rm
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"teicaa"

    def function(self, f5qm_holder, bareme =  law.ir.teicaa):
        # f5rm

        """
        Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
        """
        f5qm = self.filter_role(f5qm_holder, role = VOUS)
        f5rm = self.filter_role(f5qm_holder, role = CONJ)

        return bareme.calc(f5qm) + bareme.calc(f5rm)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class assiette_vente(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"assiette_vente"
    start_date = date(2009, 1, 1)

    def function(self, ebic_impv_holder):
        '''
        Assiette régime microsociale pour les ventes
        '''
        return self.sum_by_entity(ebic_impv_holder)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

    # P = _P.ir.rpns.microentreprise
    # assert (ebic_impv <= P.vente.max)


@reference_formula
class assiette_service(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"assiette_service"
    start_date = date(2009, 1, 1)

    def function(self, ebic_imps_holder):
        '''
        Assiette régime microsociale pour les prestations et services
        '''
        return self.sum_by_entity(ebic_imps_holder)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

    # P = _P.ir.rpns.microentreprise
    # assert (ebic_imps <= P.servi.max)


@reference_formula
class assiette_proflib(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"assiette_proflib"
    start_date = date(2009, 1, 1)

    def function(self, ebnc_impo_holder, P =  law.ir.rpns.microentreprise):
        '''
        Assiette régime microsociale pour les professions libérales
        '''
        # TODO: distinction RSI/CIPAV (pour les cotisations sociales)
        # http://vosdroits.service-public.fr/professionnels-entreprises/F23267.xhtml
        return self.sum_by_entity(ebnc_impo_holder)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

    # assert (ebnc_impo <= P.specialbnc.max)


@reference_formula
class microsocial(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"microsocial"
    start_date = date(2009, 1, 1)
    url = "http://fr.wikipedia.org/wiki/R%C3%A9gime_micro-social"

    def function(self, assiette_service, assiette_vente, assiette_proflib, _P, microsocial =  law.ir.rpns.microsocial):
        # TODO: check this
        return assiette_service * microsocial.servi + assiette_vente * microsocial.vente + assiette_proflib * microsocial.bnc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class microentreprise(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"microentreprise"
    start_date = date(2009, 1, 1)

    def function(self, ebnc_impo_holder, ebic_imps_holder, ebic_impv_holder, me =  law.ir.rpns.microentreprise):
        ebnc_impo = self.sum_by_entity(ebnc_impo_holder)
        ebic_imps = self.sum_by_entity(ebic_imps_holder)
        ebic_impv = self.sum_by_entity(ebic_impv_holder)
        return ebnc_impo * (1 - me.specialbnc.taux) + ebic_imps * (1 - me.servi.taux) + ebic_impv * (1 - me.vente.taux)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class plus_values(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"plus_values"

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, f3vg, f3vh, f3vl, f3vm, f3vi_holder, f3vf_holder, f3vd_holder, rpns_pvce_holder, _P, plus_values =  law.ir.plus_values):  # f3sd is in f3vd holder
        # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: f3vt, 2013 f3Vg au barème / tout refaire
        """
    
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
            # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
    
        return round(out)

    @dated_function(start = date(2008, 1, 1), stop = date(2011, 12, 31))
    def function_20080101_20111231(self, f3vg, f3vh, f3vl, f3vm, f3vi_holder, f3vf_holder, f3vd_holder, rpns_pvce_holder, _P, plus_values =  law.ir.plus_values):  # f3sd is in f3vd holder
        # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: f3vt, 2013 f3Vg au barème / tout refaire
        """
    
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
            # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
            # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
    
        return round(out)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, f3vg, f3vh, f3vl, f3vm, f3vi_holder, f3vf_holder, f3vd_holder, rpns_pvce_holder, _P, plus_values =  law.ir.plus_values):  # f3sd is in f3vd holder
        # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: f3vt, 2013 f3Vg au barème / tout refaire
        """
    
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        # TODO: remove this todo use sum for all fields after checking
        # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
    #        out = plus_values.taux2 * f3vd + plus_values.taux3 * f3vi + plus_values.taux4 * f3vf + plus_values.taux1 *max_(
    #            0, f3vg - f3vh)
        out = (plus_values.taux2 * (f3vd + f3sd) + plus_values.taux3 * (f3vi + f3si) +
            plus_values.taux4 * (f3vf + f3sf) + plus_values.taux1 * max_(0, f3vg - f3vh) + plus_values.pvce * rpns_pvce)
                # TODO: chek this rpns missing ?
        return round(out)

    @dated_function(start = date(2013, 1, 1), stop = date(2015, 12, 31))
    def function_20130101_20151231(self, f3vg, f3vh, f3vl, f3vm, f3vi_holder, f3vf_holder, f3vd_holder, f3sa, _P, rpns_pvce_holder, plus_values =  law.ir.plus_values):  # f3sd is in f3vd holder
        # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: f3vt, 2013 f3Vg au barème / tout refaire
        """
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
        # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
    
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
        #  out = plus_values.taux2 * f3vd + plus_values.taux3 * f3vi + plus_values.taux4 * f3vf + plus_values.taux1 * max_(
        #          0, f3vg - f3vh)
        out = (plus_values.taux2 * (f3vd + f3sd) + plus_values.taux3 * (f3vi + f3si) +
            plus_values.taux4 * (f3vf + f3sf) + plus_values.taux1 * max_(0, - f3vh) + plus_values.pvce * (rpns_pvce + f3sa))
        # TODO: chek this 3VG
        return round(out)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')








@reference_formula
class iai(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt avant imputations"
    url = "http://forum-juridique.net-iris.fr/finances-fiscalite-assurance/43963-declaration-impots.html"

    def function(self, iaidrdi, plus_values, cont_rev_loc, teicaa):
        '''
        impôt avant imputation de l'irpp
        '''
        return iaidrdi + plus_values + cont_rev_loc + teicaa

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class cehr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Contribution exceptionnelle sur les hauts revenus"
    url = "http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006069577&idSectionTA=LEGISCTA000025049019"

    def function(self, rfr, nb_adult, bareme =  law.ir.cehr):
        '''
        Contribution exceptionnelle sur les hauts revenus
        'foy'
        '''
        return bareme.calc(rfr / nb_adult) * nb_adult

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



def _cesthra(self, sal_holder, bareme = law.ir.cesthra):
    '''
    Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité
    'foy'
    PLF 2013 (rejeté) : 'taxe à 75%'
    '''
    sal = self.split_by_roles(sal_holder)

    cesthra = 0
    for rev in sal.itervalues():
        cesthra += bareme.calc(rev)
    return cesthra


@reference_formula
class irpp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu des personnes physiques"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_impot_revenu&espId=1&impot=IR&sfid=50"

    def function(self, iai, credits_impot, cehr, P =  law.ir.recouvrement):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        # TODO: crade ?
        pre_result = iai - credits_impot + cehr
        return ((iai > P.seuil) *
            ((pre_result < P.min) * (pre_result > 0) * iai * 0 +
            ((pre_result <= 0) + (pre_result >= P.min)) * (- pre_result)) +
            (iai <= P.seuil) * ((pre_result < 0) * (-pre_result) +
            (pre_result >= 0) * 0 * iai ))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



###############################################################################
# # Autres totaux utiles pour la suite
###############################################################################


@reference_formula
class alv(SimpleFormulaColumn):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Pensions alimentaires versées"
    url = u"http://vosdroits.service-public.fr/particuliers/F2.xhtml"

    def function(self, f6gi, f6gj, f6el, f6em, f6gp, f6gu):
        return -(f6gi + f6gj + f6el + f6em + f6gp + f6gu)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class alv_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Pensions alimentaires versées (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = alv


@reference_formula
class rfr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Revenu fiscal de référence"

    def function(self, rni, f3va_holder, f3vi_holder, rfr_cd, rfr_rvcm, rpns_exon_holder, rpns_pvce_holder, rev_cap_lib, f3vz, microentreprise):
        '''
        Revenu fiscal de référence
        f3vg -> rev_cat_pv -> ... -> rni
        '''
        f3va = self.sum_by_entity(f3va_holder)
        f3vi = self.sum_by_entity(f3vi_holder)
        rpns_exon = self.sum_by_entity(rpns_exon_holder)
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        return (max_(0, rni) + rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va +
                f3vz + microentreprise)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class glo(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Gain de levée d'options"
    url = "http://www.officeo.fr/imposition-au-bareme-progressif-de-l-impot-sur-le-revenu-des-gains-de-levee-d-options-sur-actions-et-attributions-d-actions-gratuites"

    def function(self, f1tv, f1tw, f1tx, f3vf, f3vi, f3vj):
        # f1tv contient f1uv
        # f1tw contient f1uw
        # f1tx contient f1ux
        # f3vf contient f3sf
        # f3vi contient f3si
        # f3vj contient f3vk voir data.py TODO: rename
        '''
        Gains de levée d'option
        '''
        return f1tv + f1tw + f1tx + f3vf + f3vi + f3vj

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rev_cap_bar(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rev_cap_bar"
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    def function(self, f2dc, f2gr, f2ch, f2ts, f2go, f2tr, f2fu, avf, f2da, f2ee, finpfl =  law.ir.autre.finpfl, majGO =  law.ir.rvcm.majGO):
        """
        Revenus du capital imposés au barème
        """
        # year = period.start.year
        # if year <= 2011:
        #     return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf
        # elif year > 2011:
        #     return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf + (f2da + f2ee)
        return f2dc + f2gr + f2ch + f2ts + f2go * majGO + f2tr + f2fu - avf + (f2da + f2ee) * finpfl

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')

    # We add f2da an f2ee to allow for comparaison between years


@reference_formula
class rev_cap_lib(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"rev_cap_lib"
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function_20020101_20071231(self, f2dh, f2ee, _P, finpfl =  law.ir.autre.finpfl):
        '''
        Revenu du capital imposé au prélèvement libératoire
        '''
        out = f2dh + f2ee
        return out * not_(finpfl)

    @dated_function(start = date(2008, 1, 1), stop = date(2015, 12, 31))
    def function_20080101_20151231(self, f2da, f2dh, f2ee, _P, finpfl =  law.ir.autre.finpfl):
        '''
        Revenu du capital imposé au prélèvement libératoire
        '''
        out = f2da + f2dh + f2ee
        return out * not_(finpfl)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class avf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"avf"

    def function(self, f2ab):
        '''
        Avoir fiscal et crédits d'impôt (zavff)
        '''
        return f2ab

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class imp_lib(DatedFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"imp_lib"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function_20020101_20071231(self, f2dh, f2ee, _P, prelevement_liberatoire =  law.ir.rvcm.prelevement_liberatoire):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        out = -(prelevement_liberatoire.assvie * f2dh + prelevement_liberatoire.autre * f2ee)
        return out

    @dated_function(start = date(2008, 1, 1), stop = date(2012, 12, 31))
    def function_20080101_20121231(self, f2da, f2dh, f2ee, _P, finpfl =  law.ir.autre.finpfl, prelevement_liberatoire =  law.ir.rvcm.prelevement_liberatoire):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        out = -(prelevement_liberatoire.action * f2da + prelevement_liberatoire.autre * f2ee) * not_(finpfl) \
            - prelevement_liberatoire.assvie * f2dh
        return out

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')





@reference_formula
class fon(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"fon"
    url = "http://impotsurlerevenu.org/definitions/220-revenu-foncier.php"

    def function(self, f4ba, f4bb, f4bc, f4bd, f4be, microfoncier =  law.ir.microfoncier):
        '''
        Revenus fonciers
        '''
        return f4ba - f4bb - f4bc + round(f4be * (1 - microfoncier.taux))

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_pvce(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_pvce"

    def function(self, frag_pvce, arag_pvce, mbic_pvce, abic_pvce, macc_pvce, aacc_pvce, mbnc_pvce, abnc_pvce, mncn_pvce, cncn_pvce):
        '''
        Plus values de cession
        'ind'
        frag_pvce (f5hx, f5ix, f5jx)
        arag_pvce (f5he, f5ie, f5je)
        mbic_pvce (f5kq, f5lq, f5mq)
        abic_pvce (f5ke, f5le, f5me)
        macc_pvce (f5nq, f5oq, f5pq)
        aacc_pvce (f5ne, f5oe, f5pe)
        mncn_pvce (f5kv, f5lv, f5mv)
        cncn_pvce (f5so, f5nt, f5ot)
        mbnc_pvce (f5hr, f5ir, f5jr)
        abnc_pvce (f5qd, f5rd, f5sd)
        '''
        return (frag_pvce + arag_pvce + mbic_pvce + abic_pvce + macc_pvce + aacc_pvce + mbnc_pvce +
                abnc_pvce + mncn_pvce + cncn_pvce)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_exon(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_exon"

    def function(self, frag_exon, arag_exon, nrag_exon, mbic_exon, abic_exon, nbnc_proc, nbic_exon, macc_exon, aacc_exon, nacc_exon, mbnc_exon, abnc_proc, nrag_pvce, abnc_exon, nbnc_exon, mncn_exon, cncn_exon, cncn_jcre, cncn_info, nbic_pvce, cga = law.ir.rpns.cga_taux2):
        '''
        Plus values de cession
        'ind'
        frag_exon (f5hn, f5in, f5jn)
        arag_exon (f5hb, f5ib, f5jb)
        nrag_exon (f5hh, f5ih, f5jh)
        mbic_exon (f5kn, f5ln, f5mn)
        abic_exon (f5kb, f5lb, f5mb)
        nbic_exon (f5kh, f5lh, f5mh)
        macc_exon (f5nn, f5on, f5pn)
        aacc_exon (f5nb, f5ob, f5pb)
        nacc_exon (f5nh, f5oh, f5ph)
        mbnc_exon (f5hp, f5ip, f5jp)
        abnc_exon (f5qb, f5rb, f5sb)
        nbnc_exon (f5qh, f5rh, f5sh)
        nbnc_pvce (f5qj, f5rj, f5sj)
        '''

        return (frag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + nbnc_proc * (1 + cga) +
                nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc +
                abnc_exon + nbnc_exon + mncn_exon + cncn_exon + cncn_jcre + cncn_info + nbic_pvce + nrag_pvce)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class defrag(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déficit agricole des années antérieures"

    def function(self, f5qf, f5qg, f5qn, f5qo, f5qp, f5qq, frag_impo_holder, nrag_impg_holder, frag_fore_holder, frag_pvct_holder, arag_impg_holder, cga =  law.ir.rpns.cga_taux2):
        frag_fore = self.sum_by_entity(frag_fore_holder)
        frag_impo = self.sum_by_entity(frag_impo_holder)
        arag_impg = self.sum_by_entity(arag_impg_holder)
        nrag_impg = self.sum_by_entity(nrag_impg_holder)
        frag_pvct = self.sum_by_entity(frag_pvct_holder)
        return min_(f5qf + f5qg + f5qn + f5qo + f5qp + f5qq, (1 + cga) * (frag_impo + nrag_impg + frag_pvct)
                    + arag_impg + frag_fore)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class defacc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déficit industriels et commerciaux non professionnels des années antérieures"

    def function(self, f5rn, f5ro, f5rp, f5rq, f5rr, f5rw, macc_impv_holder, macc_imps_holder, nacc_impn_holder, macc_pvct_holder, aacc_impn_holder, microentreprise =  law.ir.rpns.microentreprise, cga =  law.ir.rpns.cga_taux2):
        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))

        nacc_impn = self.sum_by_entity(nacc_impn_holder)
        macc_pvct = self.sum_by_entity(macc_pvct_holder)
        macc_impv = self.sum_by_entity(macc_impv_holder)
        macc_imps = self.sum_by_entity(macc_imps_holder)
        aacc_impn = self.sum_by_entity(aacc_impn_holder)
        macc_timp = abat_rpns(macc_impv, microentreprise.vente) + abat_rpns(macc_imps, microentreprise.servi)
        return min_(f5rn + f5ro + f5rp + f5rq + f5rr + f5rw, aacc_impn + macc_pvct + macc_timp + (1 + cga) * nacc_impn)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class defncn(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déficit non commerciaux non professionnels des années antérieures"

    def function(self, f5ht, f5it, f5jt, f5kt, f5lt, f5mt, mncn_impo_holder, mncn_pvct_holder, cncn_aimp_holder, cncn_bene_holder, cga =  law.ir.rpns.cga_taux2, spbnc =  law.ir.rpns.microentreprise.specialbnc):
        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))
        cncn_bene = self.sum_by_entity(cncn_bene_holder)
        mncn_impo = self.sum_by_entity(mncn_impo_holder)
        mncn_pvct = self.sum_by_entity(mncn_pvct_holder)
        cncn_aimp = self.sum_by_entity(cncn_aimp_holder)
        return min_(f5ht + f5it + f5jt + f5kt + f5lt + f5mt, abat_rpns(mncn_impo, spbnc) +
                    mncn_pvct + cncn_aimp + (1 + cga) * cncn_bene)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class defmeu(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Déficit des locations meublées non professionnelles des années antérieures"

    def function(self, f5ga, f5gb, f5gc, f5gd, f5ge, f5gf, f5gg, f5gh, f5gi, f5gj, alnp_imps_holder, nacc_defs_holder):
        nacc_defs = self.sum_by_entity(nacc_defs_holder)
        alnp_imps = self.sum_by_entity(alnp_imps_holder)
        return min_(f5ga + f5gb + f5gc + f5gd + f5ge + f5gf + f5gg + f5gh + f5gi + f5gj, alnp_imps + nacc_defs)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rag(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rag"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=BA&pageId=prof_ba&sfid=50"

    def function(self, frag_exon, frag_impo, arag_exon, arag_impg, arag_defi, nrag_exon, nrag_impg, nrag_defi, nrag_ajag):
        '''
        Revenus agricoles
        'ind'
        frag_exon (f5hn, f5in, f5jn)
        frag_impo (f5ho, f5io, f5jo)
        arag_exon (f5hb, f5ib, f5jb)
        arag_impg (f5hc, f5ic, f5jc)
        arag_defi (f5hf, f5if, f5jf)
        nrag_exon (f5hh, f5ih, f5jh)
        nrag_impg (f5hi, f5ii, f5ji)
        nrag_defi (f5hl, f5il, f5jl)
        nrag_ajag (f5hm, f5im, f5jm)
        '''
        return (frag_exon + frag_impo +
                arag_exon + arag_impg - arag_defi +
                nrag_exon + nrag_impg - nrag_defi +
                nrag_ajag)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ric(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"ric"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?pageId=prof_bic&espId=2&impot=BIC&sfid=50"

    def function(self, mbic_exon, mbic_impv, mbic_imps, abic_exon, nbic_exon, abic_impn, nbic_impn, abic_imps, nbic_imps, abic_defn, nbic_defn, abic_defs, nbic_defs, nbic_apch, microentreprise =  law.ir.rpns.microentreprise):
        '''
        Bénéfices industriels et commerciaux
        'ind'
        mbic_exon (f5kn, f5ln, f5mn)
        abic_exon (f5kb, f5lb, f5mb)
        nbic_exon (f5kh, f5lh, f5mh)
        mbic_impv (f5ko, f5lo, f5mo)
        mbic_imps (f5kp, f5lp, f5mp)
        abic_impn (f5kc, f5lc, f5mc)
        abic_imps (f5kd, f5ld, f5md)
        nbic_impn (f5ki, f5li, f5mi)
        nbic_imps (f5kj, f5lj, f5mj)
        abic_defn (f5kf, f5lf, f5mf)
        abic_defs (f5kg, f5lg, f5mg)
        nbic_defn (f5kl, f5ll, f5ml)
        nbic_defs (f5km, f5lm, f5mm)
        nbic_apch (f5ks, f5ls, f5ms)
        '''
        zbic = (mbic_exon + mbic_impv + mbic_imps
                + abic_exon + nbic_exon
                + abic_impn + nbic_impn
                + abic_imps + nbic_imps
                - abic_defn - nbic_defn
                - abic_defs - nbic_defs
                + nbic_apch)

        cond = (mbic_impv > 0) & (mbic_imps == 0)
        taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

        cbic = min_(mbic_impv + mbic_imps + mbic_exon,
                    max_(microentreprise.vente.min,
                         round(mbic_impv * microentreprise.vente.taux + mbic_imps * microentreprise.servi.taux + mbic_exon * taux)))
        return zbic - cbic

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rac(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rac"
    url = "http://vosdroits.service-public.fr/particuliers/F1225.xhtml"

    def function(self, macc_exon, macc_impv, macc_imps, aacc_exon, aacc_impn, aacc_imps, aacc_defn, aacc_defs, nacc_exon, nacc_impn, nacc_defn, nacc_defs, mncn_impo, cncn_bene, cncn_defi, microentreprise =  law.ir.rpns.microentreprise):
        '''
        Revenus accessoires individuels
        'ind'
        macc_exon (f5nn, f5on, f5pn)
        aacc_exon (f5nb, f5ob, f5pb)
        nacc_exon (f5nh, f5oh, f5ph)
        macc_impv (f5no, f5oo, f5po)
        macc_imps (f5np, f5op, f5pp)
        aacc_impn (f5nc, f5oc, f5pc)
        aacc_imps (f5nd, f5od, f5pd)
        aacc_defn (f5nf, f5of, f5pf)
        aacc_defs (f5ng, f5og, f5pg)
        nacc_impn (f5ni, f5oi, f5pi)
        nacc_defn (f5nl, f5ol, f5pl)
        nacc_defs (f5nm, f5om, f5pm)
        mncn_impo (f5ku, f5lu, f5mu)
        cncn_bene (f5sn, f5ns, f5os)
        cncn_defi (f5sp, f5nu, f5ou, f5sr)
        f5sv????
        '''
        zacc = (macc_exon + macc_impv + macc_imps
                + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs
                + nacc_exon + nacc_impn - nacc_defn - nacc_defs
                + mncn_impo + cncn_bene - cncn_defi)
    #TODO: aacc_imps aacc_defs
        cond = (macc_impv > 0) & (macc_imps == 0)
        taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

        cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, max_(microentreprise.vente.min, round(
            macc_impv * microentreprise.vente.taux
            + macc_imps * microentreprise.servi.taux + macc_exon * taux
            + mncn_impo * microentreprise.specialbnc.taux)))

        return zacc - cacc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rnc(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rnc"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&pageId=prof_bnc&impot=BNC&sfid=50"

    def function(self, mbnc_exon, mbnc_impo, abnc_exon, nbnc_exon, abnc_impo, nbnc_impo, abnc_defi, nbnc_defi, specialbnc =  law.ir.rpns.microentreprise.specialbnc):
        '''
        Revenus non commerciaux individuels
        'ind'
        mbnc_exon (f5hp, f5ip, f5jp)
        abnc_exon (f5qb, f5rb, f5sb)
        nbnc_exon (f5qh, f5rh, f5sh)
        mbnc_impo (f5hq, f5iq, f5jq)
        abnc_impo (f5qc, f5rc, f5sc)
        abnc_defi (f5qe, f5re, f5se)
        nbnc_impo (f5qi, f5ri, f5si)
        nbnc_defi (f5qk, f5rk, f5sk)
        f5ql, f5qm????
        '''
        zbnc = (mbnc_exon + mbnc_impo
                + abnc_exon + nbnc_exon
                + abnc_impo + nbnc_impo
                - abnc_defi - nbnc_defi)

        cbnc = min_(mbnc_exon + mbnc_impo, max_(specialbnc.min, round((mbnc_exon + mbnc_impo) * specialbnc.taux)))

        return zbnc - cbnc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns"

    def function(self, rag, ric, rac, rnc):
        '''
        Revenus des professions non salariées individuels
        'ind'
        '''
        return rag + ric + rac + rnc

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_pvct(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_pvct"

    def function(self, frag_pvct, mbic_pvct, macc_pvct, mbnc_pvct, mncn_pvct):
        '''
        Plus values de court terme
        'ind'
        frag_pvct (f5hw, f5iw, f5jw)
        mbic_pvct (f5kx, f5lx, f5mx)
        macc_pvct (f5nx, f5ox, f5px)
        mbnc_pvct (f5hv, f5iv, f5jv)
        mncn_pvct (f5ky, f5ly, f5my)
        '''
        return frag_pvct + macc_pvct + mbic_pvct + mbnc_pvct + mncn_pvct

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_mvct(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_mvct"

    def function(self, macc_mvct_holder, mbnc_mvct, mncn_mvct_holder):
        """Moins values de court terme

        'ind'
        macc_mvct (f5iu)
        mncn_mvct (f5ju)
        mbnc_mvct (f5kz)
        """
        macc_mvct = self.cast_from_entity_to_role(macc_mvct_holder, role = VOUS)
        mncn_mvct = self.cast_from_entity_to_role(mncn_mvct_holder, role = VOUS)
        return mbnc_mvct + macc_mvct  # mncn_mvct ?

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_mvlt(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_mvlt"

    def function(self, mbic_mvlt, macc_mvlt, mbnc_mvlt, mncn_mvlt):
        '''
        Moins values de long terme
        'ind'
        mbic_mvlt (f5kr, f5lr, f5mr)
        macc_mvlt (f5nr, f5or, f5pr)
        mncn_mvlt (f5kw, f5lw, f5mw)
        mbnc_mvlt (f5hs, f5is, f5js)
        '''
        return mbic_mvlt + macc_mvlt + mbnc_mvlt + mncn_mvlt

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class rpns_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"rpns_i"

    def function(self, frag_impo, arag_impg, nrag_impg, arag_defi, nrag_defi, mbic_impv, mbic_imps, abic_impn, abic_imps, abic_defn, abic_defs, nbic_impn, nbic_imps, nbic_defn, nbic_defs, macc_impv, macc_imps, nbic_mvct, aacc_impn, aacc_defn, aacc_gits, nacc_impn, nacc_defn, nacc_defs, aacc_imps, mbnc_impo, nacc_meup, abic_impm, abic_defm, abnc_impo, abnc_defi, nbic_impm, alnp_imps, nbnc_impo, nbnc_defi, alnp_defs, cbnc_assc, mncn_impo, cncn_bene, cncn_defi, abnc_proc, rpns_pvct, rpns_mvct, nbnc_proc, frag_fore, f5sq, mncn_exon, cncn_exon, cncn_aimp, cncn_adef, cncn_info, cncn_jcre, revimpres, pveximpres, pvtaimpres, cga_taux2 =  law.ir.rpns.cga_taux2, microentreprise =  law.ir.rpns.microentreprise):
        '''
        Revenus des professions non salariées individuels
        '''
        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))

        # Jeunes agriculteurs montant de l'abattement de 50% ou 100%
        # nrag_ajag = f5hm + f5im + f5jm

    #    # déficits agricole des années antérieurs (imputables uniquement
    #    # sur des revenus agricoles)
    #    rag_timp = frag_impo + frag_pvct + arag_impg + nrag_impg
    #    cond = (AUTRE <= microentreprise.def_agri_seuil)
    #    def_agri = cond*(arag_defi + nrag_defi) + not_(cond)*min_(rag_timp, arag_defi + nrag_defi)
    #    # TODO : check 2006 cf art 156 du CGI pour 2006
    #    def_agri_ant    = min_(max_(0,rag_timp - def_agri), f5sq)

        def_agri = f5sq + arag_defi + nrag_defi

        # # B revenus industriels et commerciaux professionnels
        # regime micro entreprise
        mbic_timp = abat_rpns(mbic_impv, microentreprise.vente) + abat_rpns(mbic_imps, microentreprise.servi)

        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        abic_timp = abic_impn + abic_imps - (abic_defn + abic_defs)

        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

        # Abatemment artisant pécheur
        # nbic_apch = f5ks + f5ls + f5ms # TODO : à intégrer qqpart

        # # C revenus industriels et commerciaux non professionnels
        # (revenus accesoires du foyers en nomenclature INSEE)

        # regime micro entreprise
        macc_timp = abat_rpns(macc_impv, microentreprise.vente) + abat_rpns(macc_imps, microentreprise.servi)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        aacc_timp = (max_(0, (aacc_impn + (aacc_gits > 0) * max_(microentreprise.servi.min, aacc_gits *
            (1 - microentreprise.vente.taux)) + (aacc_imps > 0) * max_(microentreprise.servi.min, aacc_imps *
            (1 - microentreprise.servi.taux)) + (nacc_meup > 0) * max_(microentreprise.servi.min, nacc_meup *
            (1 - microentreprise.vente.taux)) + nacc_defs - aacc_defn)))
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nacc_timp = max_(0, nacc_impn - nacc_defn)

        # # E revenus non commerciaux non professionnels
        # regime déclaratif special ou micro-bnc
        mncn_timp = abat_rpns(mncn_impo, microentreprise.specialbnc)

        # régime de la déclaration controlée
        # total 11
        cncn_timp = max_(0, cncn_bene - cncn_defi)
        # Abatement jeunes créateurs

        # # D revenus non commerciaux professionnels
        # regime déclaratif special ou micro-bnc
        mbnc_timp = abat_rpns(mbnc_impo, microentreprise.specialbnc)

        # regime de la déclaration contrôlée bénéficiant de l'abattement association agréée
        abnc_timp = abnc_impo - abnc_defi

        # regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
        nbnc_timp = nbnc_impo - nbnc_defi

        # # Totaux
        atimp = arag_impg + abic_timp + aacc_timp + abnc_timp
        ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp + cncn_timp

        majo_cga = max_(0, cga_taux2 * (ntimp + frag_impo))  # Pour ne pas avoir à majorer les déficits
        # total 6
        rev_NS = frag_impo + frag_fore + atimp + ntimp + majo_cga - def_agri

        # revenu net après abatement
        # total 7
        rev_NS_mi = mbic_timp + max_(0, macc_timp) + mbnc_timp + mncn_timp
        exon = max_(0, macc_timp + nacc_timp - rpns_mvct) - macc_timp - nacc_timp  # ajout artificiel
        RPNS = (rev_NS + rev_NS_mi + rpns_pvct + exon + abic_impm - abic_defm + alnp_imps + cncn_aimp - nbic_mvct)
        return RPNS

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class abat_spe(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Abattements spéciaux"
    url = "http://bofip.impots.gouv.fr/bofip/2036-PGP"

    def function(self, age_holder, caseP, caseF, rng, nbN, abattements_speciaux =  law.ir.abattements_speciaux):
        """
        Abattements spéciaux

        - pour personnes âges ou invalides : âgé(e) de plus de 65 ans
          ou invalide (titulaire d’une pension d’invalidité militaire ou d’accident
          du travail d’au moins 40 % ou titulaire de la carte d’invalidité),
          abattement de 2 172 € si rng du foyer fiscal inférieur à 13 370 €
                        1 086 € si rng  compris entre 13 370 € et 21 570 €.
          Abattement doublé si conjoint remplit également ces conditions
          d’âge ou d’invalidité.
        - pour enfants à charge ayant fondé un foyer distinct : Si  rattachement
          enfants mariés ou pacsés ou enfants  célibataires, veufs, divorcés, séparés, chargés de famille,
          abattement 5 495 € par personne ainsi rattachée.
          Si l’enfant de la personne rattachée est réputé à charge de
          l’un et l’autre de ses parents (garde alternée), cet abattement est divisé
          par deux soit 2 748€. Exemple : 10 990 € pour un jeune ménage et 8 243 €
          pour un célibataire avec un jeune enfant en résidence alternée.
        """
        age = self.split_by_roles(age_holder, roles = [VOUS, CONJ])

        ageV, ageC = age[VOUS], age[CONJ]
        invV, invC = caseP, caseF
        nb_elig_as = (1 * (((ageV >= 65) | invV) & (ageV > 0)) +
                      1 * (((ageC >= 65) | invC) & (ageC > 0))
                      )
        as_inv = (nb_elig_as * abattements_speciaux.inv_montant * ((rng <= abattements_speciaux.inv_max1)
                  + ((rng > abattements_speciaux.inv_max1) & (rng <= abattements_speciaux.inv_max2)) * 0.5))

        as_enf = nbN * abattements_speciaux.enf_montant

        return min_(rng, as_inv + as_enf)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class taux_effectif(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"taux_effectif"
    start_date = date(2009, 1, 1)

    def function(self, rni, nbptr, microentreprise, abnc_proc_holder, nbnc_proc_holder, bareme =  law.ir.bareme, me =  law.ir.rpns.microentreprise, cga =  law.ir.rpns.cga_taux2):
        abnc_proc = self.sum_by_entity(abnc_proc_holder)
        nbnc_proc = self.sum_by_entity(nbnc_proc_holder)
        base_fictive = rni + microentreprise + abnc_proc + nbnc_proc * (1 + cga)
        trigger = (microentreprise != 0) | (abnc_proc != 0) | (nbnc_proc != 0)
        return trigger * nbptr * bareme.calc(base_fictive / nbptr) / max_(1, base_fictive)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



###############################################################################
# # Calcul du nombre de parts
###############################################################################


@reference_formula
class nbptr(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Nombre de parts"
    url = "http://vosdroits.service-public.fr/particuliers/F2705.xhtml"

    def function(self, nb_pac, marpac, celdiv, veuf, jveuf, nbF, nbG, nbH, nbI, nbR, nbJ, caseP, caseW, caseG, caseE, caseK, caseN, caseF, caseS, caseL, caseT, quotient_familial =  law.ir.quotient_familial):
        '''
        Nombre de parts du foyer
        'foy'
        note 1 enfants et résidence alternée (formulaire 2041 GV page 10)

        quotient_familial.conj : nb part associées au conjoint d'un couple marié ou pacsé
        quotient_familial.enf1 : nb part 2 premiers enfants
        quotient_familial.enf2 : nb part enfants de rang 3 ou plus
        quotient_familial.inv1 : nb part supp enfants invalides (I, G)
        quotient_familial.inv2 : nb part supp adultes invalides (R)
        quotient_familial.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
        quotient_familial.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
        quotient_familial.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
        quotient_familial.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
        quotient_familial.not6 : nb part supp note 6
        quotient_familial.isol : demi-part parent isolé (T)
        quotient_familial.edcd : enfant issu du mariage avec conjoint décédé;
        '''
        no_pac = nb_pac == 0  # Aucune personne à charge en garde exclusive
        has_pac = not_(no_pac)
        no_alt = nbH == 0  # Aucun enfant à charge en garde alternée
        has_alt = not_(no_alt)

        # # nombre de parts liées aux enfants à charge
        # que des enfants en résidence alternée
        enf1 = (no_pac & has_alt) * (quotient_familial.enf1 * min_(nbH, 2) * 0.5
                                     + quotient_familial.enf2 * max_(nbH - 2, 0) * 0.5)
        # pas que des enfants en résidence alternée
        enf2 = (has_pac & has_alt) * ((nb_pac == 1) * (quotient_familial.enf1 * min_(nbH, 1) * 0.5
            + quotient_familial.enf2 * max_(nbH - 1, 0) * 0.5) + (nb_pac > 1) * (quotient_familial.enf2 * nbH * 0.5))
        # pas d'enfant en résidence alternée
        enf3 = quotient_familial.enf1 * min_(nb_pac, 2) + quotient_familial.enf2 * max_((nb_pac - 2), 0)

        enf = enf1 + enf2 + enf3
        # # note 2 : nombre de parts liées aux invalides (enfant + adulte)
        n2 = quotient_familial.inv1 * (nbG + nbI / 2) + quotient_familial.inv2 * nbR

        # # note 3 : Pas de personne à charge
        # - invalide

        n31a = quotient_familial.not31a * (no_pac & no_alt & caseP)
        # - ancien combatant
        n31b = quotient_familial.not31b * (no_pac & no_alt & (caseW | caseG))
        n31 = max_(n31a, n31b)
        # - personne seule ayant élevé des enfants
        n32 = quotient_familial.not32 * (no_pac & no_alt & ((caseE | caseK) & not_(caseN)))
        n3 = max_(n31, n32)
        # # note 4 Invalidité de la personne ou du conjoint pour les mariés ou
        # # jeunes veuf(ve)s
        n4 = max_(quotient_familial.not41 * (1 * caseP + 1 * caseF), quotient_familial.not42 * (caseW | caseS))

        # # note 5
        #  - enfant du conjoint décédé
        n51 = quotient_familial.cdcd * (caseL & ((nbF + nbJ) > 0))
        #  - enfant autre et parent isolé
        n52 = quotient_familial.isol * caseT * (((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2))) + 1 * has_pac)
        n5 = max_(n51, n52)

        # # note 6 invalide avec personne à charge
        n6 = quotient_familial.not6 * (caseP & (has_pac | has_alt))

        # # note 7 Parent isolé
        n7 = quotient_familial.isol * caseT * ((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2)) + 1 * has_pac)

        # # Régime des mariés ou pacsés
        m = 1 + quotient_familial.conj + enf + n2 + n4

        # # veufs  hors jveuf
        v = 1 + enf + n2 + n3 + n5 + n6

        # # celib div
        c = 1 + enf + n2 + n3 + n6 + n7

        return (marpac | jveuf) * m + (veuf & not_(jveuf)) * v + celdiv * c

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



###############################################################################
# # Calcul de la prime pour l'emploi
###############################################################################


@reference_formula
class ppe_coef(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"ppe_coef"

    def function(self, jour_xyz):
        '''
        PPE: coefficient de conversion en cas de changement en cours d'année
        '''
        nb_jour = (jour_xyz == 0) + jour_xyz
        return 360 / nb_jour

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_elig(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"ppe_elig"

    def function(self, rfr, ppe_coef, marpac, veuf, celdiv, nbptr, ppe =  law.ir.credits_impot.ppe):
        '''
        PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
        'foy'
        CF ligne 1: http://bofip.impots.gouv.fr/bofip/3913-PGP.html
        '''
        seuil = (veuf | celdiv) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
                + marpac * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
        return (rfr * ppe_coef) <= seuil

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_rev(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"ppe_rev"

    def function(self, sal, hsup, rpns, ppe =  law.ir.credits_impot.ppe):
        '''
        base ressource de la ppe
        'ind'
        '''
        # Revenu d'activité salarié
        rev_sa = sal + hsup  # TODO: + TV + TW + TX + AQ + LZ + VJ
        # Revenu d'activité non salarié
        rev_ns = min_(0, rpns) / ppe.abatns + max_(0, rpns) * ppe.abatns
            #TODO: très bizarre la partie min(0,rpns) - après vérification c'est dans la loi
        return rev_sa + rev_ns

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_coef_tp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"ppe_coef_tp"

    def function(self, ppe_du_sa, ppe_du_ns, ppe_tp_sa, ppe_tp_ns, ppe =  law.ir.credits_impot.ppe):
        '''
        PPE: coefficient de conversion temps partiel
        'ind'
        '''
        frac_sa = ppe_du_sa / ppe.TP_nbh
        frac_ns = ppe_du_ns / ppe.TP_nbj
        tp = ppe_tp_sa | ppe_tp_ns | (frac_sa + frac_ns >= 1)
        return tp + not_(tp) * (frac_sa + frac_ns)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_base(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"ppe_base"

    def function(self, ppe_rev, ppe_coef_tp, ppe_coef_holder):
        ppe_coef = self.cast_from_entity_to_roles(ppe_coef_holder)

        return ppe_rev / (ppe_coef_tp + (ppe_coef_tp == 0)) * ppe_coef

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_elig_i(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"ppe_elig_i"

    def function(self, ppe_rev, ppe_coef_tp, ppe =  law.ir.credits_impot.ppe):
        '''
        Eligibilité individuelle à la ppe
        Attention : condition de plafonnement introduite dans ppe brute
        'ind'
        '''
        return (ppe_rev >= ppe.seuil1) & (ppe_coef_tp != 0)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe_brute(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prime pour l'emploi brute"

    def function(self, ppe_elig, ppe_elig_i_holder, ppe_rev_holder, ppe_base_holder, ppe_coef, ppe_coef_tp_holder, nb_pac, marpac, celdiv, veuf, caseT, caseL, nbH, ppe =  law.ir.credits_impot.ppe):
        '''
        Prime pour l'emploi (avant éventuel dispositif de cumul avec le RSA)
        'foy'
        Cf. http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/la-prime-pour-l-emploi-ppe,1034.html
        '''
        ppe_base = self.split_by_roles(ppe_base_holder)
        ppe_coef_tp = self.split_by_roles(ppe_coef_tp_holder)
        ppe_elig_i = self.split_by_roles(ppe_elig_i_holder)
        ppe_rev = self.split_by_roles(ppe_rev_holder)

        eliv, elic, eli1, eli2, eli3 = ppe_elig_i[VOUS], ppe_elig_i[CONJ], ppe_elig_i[PAC1], \
            ppe_elig_i[PAC2], ppe_elig_i[PAC3],
        basevi, baseci = ppe_rev[VOUS], ppe_rev[CONJ]
        basev, basec, base1, base2, base3 = ppe_base[VOUS], ppe_base[CONJ], ppe_base[PAC1], ppe_base[PAC2], ppe_base[PAC1]
        coef_tpv, coef_tpc, coef_tp1, coef_tp2, coef_tp3 = ppe_coef_tp[VOUS], ppe_coef_tp[CONJ], \
            ppe_coef_tp[PAC1], ppe_coef_tp[PAC2], ppe_coef_tp[PAC1]

        nb_pac_ppe = max_(0, nb_pac - eli1 - eli2 - eli3)

        ligne2 = marpac & xor_(basevi >= ppe.seuil1, baseci >= ppe.seuil1)
        ligne3 = (celdiv | veuf) & caseT & not_(veuf & caseT & caseL)
        ligne1 = not_(ligne2) & not_(ligne3)

        base_monact = ligne2 * (eliv * basev + elic * basec)
        base_monacti = ligne2 * (eliv * basevi + elic * baseci)

        def ppe_bar1(base):
    #        cond1 = ligne1 | ligne3
    #        cond2 = ligne2
    #        return 1 / ppe_coef * ((cond1 & (base <= ppe.seuil2)) * (base) * ppe.taux1 +
    #                           (cond1 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2 +
    #                           (cond2 & (base <= ppe.seuil2)) * (base * ppe.taux1) +
    #                           (cond2 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * ((ppe.seuil3 - base) * ppe.taux2) +
    #                           (cond2 & (base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)
            return (1 / ppe_coef) * (
                ((base <= ppe.seuil2)) * (base) * ppe.taux1
                + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2
                + ligne2 * ((base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)

        def ppe_bar2(base):
            return (1 / ppe_coef) * (
                (base <= ppe.seuil2) * (base) * ppe.taux1
                + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base1) * ppe.taux2)

        # calcul des primes individuelles.

        ppev = eliv * ppe_bar1(basev)
        ppec = elic * ppe_bar1(basec)
        ppe1 = eli1 * ppe_bar2(base1)
        ppe2 = eli2 * ppe_bar2(base2)
        ppe3 = eli3 * ppe_bar2(base3)

        # Primes de monoactivité
        ppe_monact_vous = (eliv & ligne2 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil4)) * ppe.monact
        ppe_monact_conj = (elic & ligne2 & (baseci >= ppe.seuil1) & (basec <= ppe.seuil4)) * ppe.monact

        # Primes pour enfants à charge
        maj_pac = ppe_elig * (eliv | elic) * (
            (ligne1 & marpac & ((ppev + ppec) != 0) & (min_(basev, basec) <= ppe.seuil3)) * ppe.pac
            * (nb_pac_ppe + nbH * 0.5)
            + (ligne1 & (celdiv | veuf) & eliv & (basev <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monacti >= ppe.seuil1) & (base_monact <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monact > ppe.seuil3) & (base_monact <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) + 0.5 * ((nb_pac_ppe == 0) & (nbH != 0)))
            + (ligne3 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil3)) * (
                (min_(nb_pac_ppe, 1) * 2 * ppe.pac + max_(nb_pac_ppe - 1, 0) * ppe.pac)
                + (nb_pac_ppe == 0) * (min_(nbH, 2) * ppe.pac + max_(nbH - 2, 0) * ppe.pac * 0.5))
            + (ligne3 & (basev > ppe.seuil3) & (basev <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) * 2 + ((nb_pac_ppe == 0) & (nbH != 0))))

        def coef(coef_tp):
            return (coef_tp <= 0.5) * coef_tp * 1.45 + (coef_tp > 0.5) * (0.55 * coef_tp + 0.45)

        ppe_vous = ppe_elig * (ppev * coef(coef_tpv) + ppe_monact_vous)
        ppe_conj = ppe_elig * (ppec * coef(coef_tpc) + ppe_monact_conj)
        ppe_pac1 = ppe_elig * (ppe1 * coef(coef_tp1))
        ppe_pac2 = ppe_elig * (ppe2 * coef(coef_tp2))
        ppe_pac3 = ppe_elig * (ppe3 * coef(coef_tp3))

        ppe_tot = ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 + maj_pac

        ppe_tot = (ppe_tot != 0) * max_(ppe.versmin, ppe_tot)
        # from pandas import DataFrame
        # decompo = {0: ppev, 1 :ppe_vous, 2: ppec,3: ppe_conj, 4: maj_pac, 5 : ppe_monact_vous, 6: ppe_monact_conj,
            #8: basev, 81 : basevi, 9: basec, 91 : baseci, 10:ppe_tot}
        # ppe DataFrame(decompo).to_string()

        return ppe_tot

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')



@reference_formula
class ppe(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = FoyersFiscaux
    label = u"Prime pour l'emploi"
    url = "http://vosdroits.service-public.fr/particuliers/F2882.xhtml"

    def function(self, ppe_brute, rsa_act_i_holder):
        """
        PPE effectivement versée
        'foy'
        """
    #   TODO: les foyers qui paient l'ISF n'ont pas le droit à la PPE
        rsa_act_i = self.split_by_roles(rsa_act_i_holder, roles = [VOUS, CONJ])

    #   On retranche le RSA activité de la PPE
    #   Dans les agrégats officiels de la DGFP, c'est la PPE brute qu'il faut comparer
        ppe = max_(ppe_brute - rsa_act_i[VOUS] - rsa_act_i[CONJ], 0)
        return ppe

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')
