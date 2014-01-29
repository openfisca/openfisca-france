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

from numpy import logical_not as not_, maximum as max_, minimum as min_, ones, zeros 

from openfisca_core.baremes import BaremeDict, combineBaremes, scaleBaremes
from openfisca_core.enumerations import Enum

CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])

log = logging.getLogger(__name__)

# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont en CG et BH en 2010

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup

# Exonération de CSG et de CRDS sur les revenus du chômage
# et des préretraites si cela abaisse ces revenus sous le smic brut
# TODO: mettre un trigger pour l'éxonération des revenus du chômage sous un smic

# TODO: RAFP assiette + prime
# TODO: pension assiette = salaire hors prime
# autres salaires + primes


# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés) salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)      salaire total 0,55%
# Taxe sur les salaries (pour ceux non-assujettis à la TVA)           salaire total 4,25%
# TODO: accident du travail ?

#temp = 0
#if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp
#else :
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
#a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds, 'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps, 'ir': P.ir, 'prelsoc': P.prelsoc}
#return Dicts2Object(**a)


############################################################################
## Salaires
############################################################################

def _salbrut(sali, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire imposable
    '''
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss

    salarie = scaleBaremes(BaremeDict('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg = scaleBaremes(BaremeDict('csg', _defaultP.csg), plaf_ss)

    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

    noncadre = combineBaremes(salarie['noncadre'])
    cadre    = combineBaremes(salarie['cadre'])
    fonc     = combineBaremes(salarie['fonc'])

    # On ajoute la CSG deductible
    noncadre.addBareme(csg['act']['deduc'])
    cadre.addBareme(csg['act']['deduc'])
    fonc.addBareme(csg['act']['deduc'])

    nca = noncadre.inverse()
    cad = cadre.inverse()
    fon = fonc.inverse()

    # TODO: complete this to deal with the fonctionnaire
    brut_nca = nca.calc(sali)
    brut_cad = cad.calc(sali)
    brut_fon = fon.calc(sali)

    salbrut = (brut_nca*(type_sal == CAT['prive_non_cadre']) +
               brut_cad*(type_sal == CAT['prive_cadre']) +
               brut_fon*(type_sal == CAT['public_titulaire_etat']) )
    
    return salbrut + hsup

def _salbrut_from_salnet(salnet, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire net
    Renvoie 0 sauf pour les salariés non cadres, cadres (TODO: et les contractuels de la fonction publique ?)  
    '''
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss
    salarie = scaleBaremes(BaremeDict('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg = scaleBaremes(BaremeDict('csg', _defaultP.csg), plaf_ss)
    crds = scaleBaremes(BaremeDict('csrds', _defaultP.crds), plaf_ss)

    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

    noncadre = combineBaremes(salarie['noncadre'])
    cadre    = combineBaremes(salarie['cadre'])
    fonc     = combineBaremes(salarie['fonc'])

    # On ajoute la CSG deductible+imosable et la CRDS
    for baremes in [noncadre, cadre, fonc]:
        baremes.addBareme(csg['act']['deduc'])
        baremes.addBareme(csg['act']['impos'])
        baremes.addBareme(crds['act'])
    
    nca = noncadre.inverse()
    cad = cadre.inverse()
    fon = fonc.inverse()

    # TODO: complete this to deal with the fonctionnaire
    brut_nca = nca.calc(salnet)
    brut_cad = cad.calc(salnet)
    brut_fon = fon.calc(salnet)

    salbrut = (brut_nca*(type_sal == CAT['prive_non_cadre']) +
               brut_cad*(type_sal == CAT['prive_cadre']) +
               brut_fon*(type_sal == CAT['public_titulaire_etat']) )
    
    return salbrut + hsup


############################################################################
## Allocations chômage
############################################################################

def _chobrut(choi, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    # TODO: ajouter la crds ? Malka Louise
    P = _defaultP.csg.chom
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    
    taux_plein = csg['plein']
    taux_reduit = csg['reduit']
    
    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()
    #log.info(chom_plein)
    #log.info(chom_reduit)
    chobrut = (csg_rempl==1)*choi + (csg_rempl==2)*chom_reduit.calc(choi) + (csg_rempl==3)*chom_plein.calc(choi)
    #isexo = exo_csg_chom(choi, _defaultP)
    #chobrut = not_(isexo)*chobrut + (isexo)*choi
#     print  P.plein.impos,  P.plein.deduc
#     print "taux réduit : "
#     print  P.reduit.impos,  P.reduit.deduc
    return chobrut


def _chobrut_from_chonet(chonet, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    P = _defaultP.csg.chom
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    crds = scaleBaremes(BaremeDict('crds', _defaultP.crds), plaf_ss)
    
    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)
    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()
    
    chobrut = (csg_rempl==1)*chonet + (csg_rempl==2)*chom_reduit.calc(chonet) + (csg_rempl==3)*chom_plein.calc(chonet)
    
    return chobrut
    

############################################################################
## Pensions
############################################################################

def _rstbrut(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions imposables
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()  # TODO:     rajouter la non  déductible dans param
    rst_reduit = P.reduit.deduc.inverse()  #
    rstbrut = (csg_rempl==2)*rst_reduit.calc(rsti) + (csg_rempl==3)*rst_plein.calc(rsti)
    return rstbrut


def _rstbrut_from_rstnet(rstnet, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes
    '''
    P = _defaultP.csg.retraite
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    crds = scaleBaremes(BaremeDict('crds', _defaultP.crds), plaf_ss)
    # TODO: rajouter la non  déductible dans param
    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])    
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)
    rst_plein = taux_plein.inverse()
    rst_reduit = taux_reduit.inverse()
    rstbrut = (csg_rempl==2)*rst_reduit.calc(rstnet) + (csg_rempl==3)*rst_plein.calc(rstnet)
    return rstbrut
    

def get_brut_from_net(net, type_sal = 0, hsup = 0, csg_rempl = 0, rev = 'sal', year = 2011):
    import os
    from openfisca_core import model
    from openfisca_core.simulations import ScenarioSimulation
    import openfisca_france
    openfisca_france.init_country()#start_from="brut")    from openfisca_core import model
    param_file = os.path.join(os.path.dirname(model.PARAM_FILE), 'param_actu_IPP.xml')

    simulation = ScenarioSimulation()
    simulation.set_config(year=2011, nmen=2, x_axis="sali", maxrev=1000, param_file=param_file)
    simulation.set_param()
    simulation.compute()
    
    net = [net]

    _defaultP = simulation.P
    if rev =='sal':
        output =  _salbrut_from_salnet(net, hsup, type_sal, _defaultP)
    elif rev == 'cho':
        output =  _chobrut_from_chonet(net, csg_rempl, _defaultP)
    elif rev == 'rst':
        output =  _rstbrut_from_rstnet(net, csg_rempl, _defaultP)
    
    return output



if __name__ == '__main__':
    net = 10000
    brut = get_brut_from_net(12*net)/12
    
    print get_brut_from_net(12*1568.80)/12