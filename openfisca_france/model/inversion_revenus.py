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
from numpy import zeros

from openfisca_core.baremes import Bareme, BaremeDict, combineBaremes, scaleBaremes
from openfisca_france.model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME


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

# temp = 0
# if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp
# else :
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
# a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds, 'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps, 'ir': P.ir, 'prelsoc': P.prelsoc}
# return Dicts2Object(**a)


############################################################################
# # Salaires
############################################################################

def _salbrut(sali, hsup, type_sal, _defaultP):
    # indemnite_residence, sup_familial
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

    log.info("Le dictionnaire des barèmes des cotisations salariés des titualires de l'Etat contien : \n %s", salarie['fonc']["etat"])

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

#     print 'sali', sali / 12
    brut_etat = etat.calc(sali)
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
    csg = scaleBaremes(BaremeDict('csg', _defaultP.csg), plaf_ss)
    crds = scaleBaremes(BaremeDict('crds', _defaultP.crds), plaf_ss)
    salarie['noncadre'].update(salarie['commun'])
    salarie['cadre'].update(salarie['commun'])

    # Salariés du privé
    prive_non_cadre = combineBaremes(salarie['noncadre'])
    prive_cadre = combineBaremes(salarie['cadre'])

    # On ajoute la CSG deductible et imposable
    for bareme in [prive_non_cadre, prive_cadre]:
        bareme.addBareme(csg['act']['deduc'])
        bareme.addBareme(csg['act']['impos'])
        bareme.addBareme(crds['act'])

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
    # TODO: ajouter la crds ? Malka Louise
    P = _defaultP.csg.chom
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)

    taux_plein = csg['plein']
    taux_reduit = csg['reduit']

    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()
    # log.info(chom_plein)
    # log.info(chom_reduit)
    chobrut = (csg_rempl == 1) * choi + (csg_rempl == 2) * chom_reduit.calc(choi) + (csg_rempl == 3) * chom_plein.calc(choi)
    # isexo = exo_csg_chom(choi, _defaultP)
    # chobrut = not_(isexo)*chobrut + (isexo)*choi
#     print  P.plein.impos,  P.plein.deduc
#     print "taux réduit : "
#     print  P.reduit.impos,  P.reduit.deduc
    return chobrut


def _chobrut_from_chonet(chonet, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations imposables
    '''
    P = _defaultP.csg.chom
    plaf_ss = 12 * _defaultP.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', P), plaf_ss)
    crds = scaleBaremes(BaremeDict('crds', _defaultP.crds), plaf_ss)

    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)
    chom_plein = taux_plein.inverse()
    chom_reduit = taux_reduit.inverse()

    chobrut = (csg_rempl == 1) * chonet + (csg_rempl == 2) * chom_reduit.calc(chonet) + (csg_rempl == 3) * chom_plein.calc(chonet)

    return chobrut


############################################################################
# # Pensions
############################################################################

def _rstbrut(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions imposables
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()  # TODO:     rajouter la non  déductible dans param
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
    crds = scaleBaremes(BaremeDict('crds', _defaultP.crds), plaf_ss)
    # TODO: rajouter la non  déductible dans param
    taux_plein = combineBaremes(csg['plein'])
    taux_reduit = combineBaremes(csg['reduit'])
    taux_plein.addBareme(crds)
    taux_reduit.addBareme(crds)
    rst_plein = taux_plein.inverse()
    rst_reduit = taux_reduit.inverse()
    rstbrut = (csg_rempl == 2) * rst_reduit.calc(rstnet) + (csg_rempl == 3) * rst_plein.calc(rstnet)
    return rstbrut


def get_brut_from_net(net, type_sal = 0, hsup = 0, csg_rempl = 0, rev = 'sal', year = 2011):


    from openfisca_core.simulations import ScenarioSimulation
    import openfisca_france
    openfisca_france.init_country()

    simulation = ScenarioSimulation()
    simulation.set_config(year = 2011, nmen = 2, x_axis = "sali", maxrev = 100)
    simulation.set_param()
    simulation.compute()

    net = [net]

    _defaultP = simulation.P
    if rev == 'sal':
        output = _salbrut_from_salnet(net, hsup, type_sal, _defaultP)
    elif rev == 'cho':
        output = _chobrut_from_chonet(net, csg_rempl, _defaultP)
    elif rev == 'rst':
        output = _rstbrut_from_rstnet(net, csg_rempl, _defaultP)

    return output



if __name__ == '__main__':
    net = 1961
    brut = get_brut_from_net(12 * net) / 12
    print brut
#    print get_brut_from_net(12 * 1568.80) / 12
