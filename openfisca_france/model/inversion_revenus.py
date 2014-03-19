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
from openfisca_core.baremes import Bareme, BaremeDict, combineBaremes, scaleBaremes
from openfisca_france.model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME
from openfisca_france.model.cotisations_sociales.remplacement import exo_csg_chom


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

def _salbrut(sali, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire imposable
    sauf pour les fonctionnaires où il renvoie le tratement indiciaire brut
    Note : le supplément familial de traitement est imposable
    '''
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss

    salarie = scaleBaremes(BaremeDict('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg = scaleBaremes(BaremeDict('csg', _defaultP.csg), plaf_ss)

    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

#    log.info("Le dictionnaire des barèmes des cotisations salariés des titulaires de l'Etat contient : \n %s", salarie['fonc']["etat"])

    # Salariés du privé

    noncadre = combineBaremes(salarie['noncadre'])
    cadre = combineBaremes(salarie['cadre'])

    # On ajoute la CSG deductible
    noncadre.addBareme(csg['act']['deduc'])
    cadre.addBareme(csg['act']['deduc'])

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
#    public_colloc = combineBaremes(salarie['fonc']["colloc"]) TODO:

    # Pour a fonction publique la csg est calculée sur l'ensemble salbrut(=TIB) + primes
    # Imposable = TIB - csg( (1+taux_prime)*TIB ) - pension(TIB) + taux_prime*TIB
    bareme_csg_titulaire_etat = (csg['act']['deduc']).multTaux(1 + TAUX_DE_PRIME, inplace = False, new_name = "csg deduc titutaire etat")
    public_etat.addBareme(bareme_csg_titulaire_etat)
    bareme_prime = Bareme(name = "taux de prime")
    bareme_prime.addTranche(0, -TAUX_DE_PRIME)  # barème équivalent à taux_prime*TIB
    public_etat.addBareme(bareme_prime)

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

    salarie = scaleBaremes(BaremeDict('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg_deduc = scaleBaremes(_defaultP.csg.act.deduc, plaf_ss)
    csg_impos = scaleBaremes(_defaultP.csg.act.impos, plaf_ss)
    crds = scaleBaremes(_defaultP.crds.act, plaf_ss)
    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

    # Salariés du privé
    prive_non_cadre = combineBaremes(salarie['noncadre'])
    prive_cadre = combineBaremes(salarie['cadre'])

    # On ajoute la CSG deductible et imposable
    for bareme in [prive_non_cadre, prive_cadre]:
        bareme.addBareme(csg_deduc)
        bareme.addBareme(csg_impos)
        bareme.addBareme(crds)

    inversed_bareme = {'prive_non_cadre': prive_non_cadre.inverse(),
                       'prive_cadre' : prive_cadre.inverse()}

    salbrut = zeros(len(salnet))
    for category in ['prive_non_cadre', 'prive_cadre']:
        salbrut += inversed_bareme[category].calc(salnet) * (type_sal == CAT[category])

    return salbrut + hsup

############################################################################
# # Allocations chômage
############################################################################

def _chobrut(choi, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    P = _defaultP.csg.chom
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
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
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    crds = scaleBaremes(_defaultP.crds.rst, plaf_ss)  # crds.rst est la CRDS sur les revenus de remplacement

    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)
    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()

    chobrut = (csg_rempl == 1) * chonet + (csg_rempl == 2) * chom_reduit.calc(chonet) + (csg_rempl == 3) * chom_plein.calc(chonet)

    isexo = exo_csg_chom(chobrut, csg_rempl, _defaultP)
    chobrut = not_(isexo) * chobrut + (isexo) * chonet
    return chobrut


############################################################################
# # Pensions
############################################################################

def _rstbrut(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions imposables
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()  # TODO: rajouter la non  déductible dans param
    rst_reduit = P.reduit.deduc.inverse()  #
    rstbrut = (csg_rempl == 2) * rst_reduit.calc(rsti) + (csg_rempl == 3) * rst_plein.calc(rsti)
    return rstbrut


def _rstbrut_from_rstnet(rstnet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes
    '''
    P = _defaultP.csg.retraite
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    crds = scaleBaremes(_defaultP.crds.rst, plaf_ss)
    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)

    if hasattr(_defaultP.prelsoc, 'add_ret'):
        casa = Bareme(name = "casa")
        casa.addTranche(0, _defaultP.prelsoc.add_ret)
        taux_plein.addBareme(casa)
        taux_reduit.addBareme(casa)

    rst_plein = taux_plein.inverse()
    rst_reduit = taux_reduit.inverse()
    rstbrut = (csg_rempl == 2) * rst_reduit.calc(rstnet) + (csg_rempl == 3) * rst_plein.calc(rstnet)
    return rstbrut


from openfisca_france import surveys

def brut_to_net(brut_variable_name, net_variable_name, net_value, other_vars, _defaultP): 
    '''
    Fonction générique pour inverser numériquement
    '''
    import numpy as np
    from scipy.optimize import fsolve
    import openfisca_france, datetime
    year = _defaultP.datesim.year
    
    def brut_to_net(brut, other_vars):
        TaxBenefitSystem = openfisca_france.init_country()
        tax_benefit_system = TaxBenefitSystem()
        
        parent1 = dict(age = np.array(40).repeat(len(brut.values()[0])))
        parent1.update(brut)
        parent1.update(other_vars)
        print parent1

        simulation = surveys.new_simulation_from_array_dict(
            array_dict = parent1,
            tax_benefit_system = tax_benefit_system,
            year = year,
            )
        
        # simulation = tax_benefit_system.new_scenario().init_single_entity(
        #     parent1 = parent1,
        #     year = year,
        #     ).new_simulation(debug = True)


        simulation.compact_legislation = _defaultP
        simulation.default_compact_legislation = _defaultP
        return simulation.calculate(net_variable_name)

    function = lambda x : brut_to_net({ brut_variable_name:x},
                                       other_vars) - net_value

    sol =fsolve(function, net_value)
    print "sol", sol
    return sol


def _num_rstbrut_from_rstnet(rstnet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
    brut_variable_name = "rstbrut"
    net_variable_name = "rstnet"
    net_value = rstnet.tolist()[0]
    other_vars = dict(csg_rempl=csg_rempl.tolist()[0])
    return brut_to_net(brut_variable_name, net_variable_name, net_value, other_vars, _defaultP)
    

def _num_chobrut_from_chonet(chonet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
    brut_variable_name = "chobrut"
    net_variable_name = "chonet"
    net_value = chonet.tolist()[0]
    other_vars = dict(csg_rempl=csg_rempl.tolist()[0])
    print 'other vars', other_vars
    return brut_to_net(brut_variable_name, net_variable_name, net_value, other_vars, _defaultP)


def _num_salbrut_from_salnet(salnet, hsup, type_sal, primes, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes par inversion numérique
    '''
#    other_vars = dict(hsup=hsup.tolist()[0], type_sal=type_sal.tolist()[0], primes=primes.tolist()[0])
    other_vars = dict(hsup=hsup, type_sal=type_sal, primes=primes)
    print 'other vars', other_vars
    brut_variable_name = "salbrut"
    net_variable_name = "salnet"
    net_value = salnet
    return brut_to_net(brut_variable_name, net_variable_name, net_value, other_vars, _defaultP)



if __name__ == '__main__':
#     net = 1961
#     brut = get_brut_from_net(12 * net) / 12
#     print brut
# #    print get_brut_from_net(12 * 1568.80) / 12


    import openfisca_france, datetime
    year = 2013
    rstbrut = _num_rstbrut_from_rstnet(20000, 2, None)
    print rstnet
    
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()
    parent1 = dict(birth = datetime.date(year - 40, 1, 1))
    parent1.update(dict(rstbrut=rstbrut.tolist()[0], csg_rempl = 2))
    print 'parent 1 final', parent1    
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = parent1,
        year = year,
        ).new_simulation(debug = True)
    print "brut", simulation.calculate('rstbrut')
    print "net", simulation.calculate('rstnet')

