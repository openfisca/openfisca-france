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


from numpy import zeros, logical_not as not_
from openfisca_core.taxscales import MarginalRateTaxScale, TaxScalesTree, combine_tax_scales, scale_tax_scales

from scipy.optimize import fsolve

from openfisca_france.model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME
from openfisca_france.model.cotisations_sociales.remplacement import exo_csg_chom
from openfisca_france import surveys


log = logging.getLogger(__name__)

# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont en CG et BH en 2010

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup

# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés) salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)      salaire total 0,55%
# TODO: accident du travail ?


############################################################################
# # Salaires
############################################################################


def _salbrut_from_sali(sali, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire imposable
    sauf pour les fonctionnaires où il renvoie le tratement indiciaire brut
    Note : le supplément familial de traitement est imposable
    '''
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss

    salarie = scale_tax_scales(TaxScalesTree('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg = scale_tax_scales(TaxScalesTree('csg', _defaultP.csg), plaf_ss)

    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

#    log.info("Le dictionnaire des barèmes des cotisations salariés des titulaires de l'Etat contient : \n %s", salarie['fonc']["etat"])

    # Salariés du privé

    noncadre = combine_tax_scales(salarie['noncadre'])
    cadre = combine_tax_scales(salarie['cadre'])

    # On ajoute la CSG deductible
    noncadre.add_tax_scale(csg['act']['deduc'])
    cadre.add_tax_scale(csg['act']['deduc'])

    nca = noncadre.inverse()
    cad = cadre.inverse()
    brut_nca = nca.calc(sali)
    brut_cad = cad.calc(sali)
    salbrut = brut_nca * (type_sal == CAT['prive_non_cadre'])
    salbrut += brut_cad * (type_sal == CAT['prive_cadre'])

    # public etat
    # TODO: modifier la contribution exceptionelle de solidarité
    # en fixant son seuil de non imposition dans le barème (à corriger dans param.xml
    # et en tenant compte des éléments de l'assiette
    salarie['fonc']["etat"].update({'excep_solidarite' : salarie['fonc']['commun']['solidarite']})

    public_etat = salarie['fonc']["etat"]['pension']
#    public_colloc = combine_tax_scales(salarie['fonc']["colloc"]) TODO:

    # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
    # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
    bareme_csg_titulaire_etat = (csg['act']['deduc']).multiply_rates(1 + TAUX_DE_PRIME, inplace = False, new_name = "csg deduc titutaire etat")
    public_etat.add_tax_scale(bareme_csg_titulaire_etat)
    bareme_prime = MarginalRateTaxScale(name = "taux de prime")
    bareme_prime.add_bracket(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
    public_etat.add_tax_scale(bareme_prime)

    etat = public_etat.inverse()

    # TODO: complete this to deal with the fonctionnaire
    supp_familial_traitement = 0  # TODO: dépend de salbrut
    indemnite_residence = 0  # TODO: fix bug

#    print 'sali', sali / 12
    brut_etat = etat.calc(sali)
#    print 'brut_etat', brut_etat/12
#     print 'impot', public_etat.calc(brut_etat) / 12
#     print 'brut_etat', brut_etat / 12
    salbrut_etat = (brut_etat)
#                 # TODO: fonctionnaire
#    print 'salbrut_etat', salbrut_etat / 12
    salbrut += salbrut_etat * (type_sal == CAT['public_titulaire_etat'])

# #        <NODE desc= "Supplément familial de traitement " shortname="Supp. fam." code= "supp_familial_traitement" color = "0,99,143"/>
# #        <NODE desc= "Indemnité de résidence" shortname="Ind. rés." code= "indemenite_residence" color = "0,99,143"/>
    return salbrut + hsup


def _salbrut_from_salnet(salnet, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire net
    Renvoie 0 sauf pour les salariés non cadres, cadres (TODO: et les contractuels de la fonction publique ?)
    '''
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss

    salarie = scale_tax_scales(TaxScalesTree('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg_deduc = scale_tax_scales(_defaultP.csg.act.deduc, plaf_ss)
    csg_impos = scale_tax_scales(_defaultP.csg.act.impos, plaf_ss)
    crds = scale_tax_scales(_defaultP.crds.act, plaf_ss)
    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

    # Salariés du privé
    prive_non_cadre = combine_tax_scales(salarie['noncadre'])
    prive_cadre = combine_tax_scales(salarie['cadre'])

    # On ajoute la CSG deductible et imposable
    for bareme in [prive_non_cadre, prive_cadre]:
        bareme.add_tax_scale(csg_deduc)
        bareme.add_tax_scale(csg_impos)
        bareme.add_tax_scale(crds)

    inversed_bareme = {'prive_non_cadre': prive_non_cadre.inverse(),
                       'prive_cadre' : prive_cadre.inverse()}

    salbrut = zeros(len(salnet))
    for category in ['prive_non_cadre', 'prive_cadre']:
        salbrut += inversed_bareme[category].calc(salnet) * (type_sal == CAT[category])

    return salbrut + hsup

############################################################################
# # Allocations chômage
############################################################################

def _chobrut_from_choi(choi, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    P = _defaultP.csg.chom
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scale_tax_scales(TaxScalesTree('csg', P), plaf_ss)
    taux_plein = csg['plein']['deduc']
    taux_reduit = csg['reduit']['deduc']

    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()
    chobrut = (csg_rempl == 1) * choi + (csg_rempl == 2) * chom_reduit.calc(choi) + (csg_rempl == 3) * chom_plein.calc(choi)
    isexo = exo_csg_chom(chobrut, csg_rempl, _defaultP)
    chobrut = not_(isexo) * chobrut + (isexo) * choi

    return chobrut


def _chobrut_from_chonet(chonet, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    P = _defaultP.csg.chom
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scale_tax_scales(TaxScalesTree('csg', P), plaf_ss)
    crds = scale_tax_scales(_defaultP.crds.rst, plaf_ss)  # crds.rst est la CRDS sur les revenus de remplacement donc valable aussi pour le chômage

    taux_plein = combine_tax_scales(csg['plein'])
    taux_reduit = combine_tax_scales(csg['reduit'])
    taux_plein.add_tax_scale(crds)
    taux_reduit.add_tax_scale(crds)
    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()

    chobrut = (csg_rempl == 1) * chonet + (csg_rempl == 2) * chom_reduit.calc(chonet) + (csg_rempl == 3) * chom_plein.calc(chonet)
    isexo = exo_csg_chom(chobrut, csg_rempl, _defaultP)
    chobrut = not_(isexo) * chobrut + (isexo) * chonet
    return chobrut


############################################################################
# # Pensions
############################################################################


def _rstbrut_from_rsti(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions imposables
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()
    rst_reduit = P.reduit.deduc.inverse()
    rstbrut = (csg_rempl == 2) * rst_reduit.calc(rsti) + (csg_rempl == 3) * rst_plein.calc(rsti)
    return rstbrut


def _rstbrut_from_rstnet(rstnet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes
    '''
    P = _defaultP.csg.retraite
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scale_tax_scales(TaxScalesTree('csg', P), plaf_ss)
    crds = scale_tax_scales(_defaultP.crds.rst, plaf_ss)
    taux_plein = combine_tax_scales(csg['plein'])
    taux_reduit = combine_tax_scales(csg['reduit'])
    taux_plein.add_tax_scale(crds)
    taux_reduit.add_tax_scale(crds)

    if hasattr(_defaultP.prelsoc, 'add_ret'):
        casa = MarginalRateTaxScale(name = "casa")
        casa.add_bracket(0, _defaultP.prelsoc.add_ret)
        taux_plein.add_tax_scale(casa)
        taux_reduit.add_tax_scale(casa)

    rst_plein = taux_plein.inverse()
    rst_reduit = taux_reduit.inverse()
    rstbrut = (csg_rempl == 2) * rst_reduit.calc(rstnet) + (csg_rempl == 3) * rst_plein.calc(rstnet)
    return rstbrut


def brut_to_net(year = None, net_variable_name = None, tax_benefit_system = None, **kwargs):
    simulation = surveys.new_simulation_from_array_dict(
        array_dict = kwargs,
        tax_benefit_system = tax_benefit_system.__class__(),
        year = year,
        )
    return simulation.calculate(net_variable_name)


def _num_rstbrut_from_rstnet(self, rstnet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
    function = lambda x: brut_to_net(
        csg_rempl = csg_rempl,
        net_variable_name = 'rstnet',
        rstbrut = x,
        tax_benefit_system = self.holder.entity.simulation.tax_benefit_system,
        year = _defaultP.datesim.year,
        ) - rstnet
    return fsolve(function, rstnet)


def _num_chobrut_from_chonet(self, chonet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
    function = lambda x: brut_to_net(
        chobrut = x,
        csg_rempl = csg_rempl,
        net_variable_name = 'chonet',
        tax_benefit_system = self.holder.entity.simulation.tax_benefit_system,
        year = _defaultP.datesim.year,
        ) - chonet
    return fsolve(function, chonet)


def _num_salbrut_from_salnet(self, agem, salnet, hsup, type_sal, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
    function = lambda x: brut_to_net(
        agem = agem,
        hsup = hsup,
        net_variable_name = 'salnet',
        primes = TAUX_DE_PRIME * x * (type_sal >= 2),
        salbrut = x,
        tax_benefit_system = self.holder.entity.simulation.tax_benefit_system,
        type_sal = type_sal,
        year = _defaultP.datesim.year,
        ) - salnet
    return fsolve(function, salnet)

def _primes_from_salbrut(salbrut, type_sal):
    return salbrut * TAUX_DE_PRIME * (type_sal >= 2)
