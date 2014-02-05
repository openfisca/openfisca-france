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

from numpy import (logical_not as not_, logical_or as or_, maximum as max_, minimum as min_,
                   zeros)

from openfisca_core.baremes import Bareme, BaremeDict, combineBaremes, scaleBaremes
from openfisca_core.enumerations import Enum

TAUX_DE_PRIME = 1 / 4  # primes (hors supplément familial et indemnité de résidence) / rémunération brute


CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])

DEBUG_SAL_TYPE = 'public_non_titulaire'

log = logging.getLogger(__name__)

# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont
#        en CG et BH en 2010

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup

# Exonération de CSG et de CRDS sur les revenus du chômage
# et des préretraites si cela abaisse ces revenus sous le smic brut
# TODO: mettre un trigger pour l'éxonération
#       des revenus du chômage sous un smic

# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés)
#        salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)
#        salaire total 0,55%



def _mhsup(hsup):
    """
    Heures supplémentaires comptées négativement
    """
    return -hsup


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
#     print 'salbrut_etat', salbrut_etat / 12
    salbrut += salbrut_etat * (type_sal == CAT['public_titulaire_etat'])

# #        <NODE desc= "Supplément familial de traitement " shortname="Supp. fam." code= "supp_familial_traitement" color = "0,99,143"/>
# #        <NODE desc= "Indemnité de résidence" shortname="Ind. rés." code= "indemenite_residence" color = "0,99,143"/>
    return salbrut + hsup


def _type_sal(titc, statut, chpub, cadre):
    '''
    Catégorie de salarié
    0: prive_non_cadre
    1: prive_cadre
    2: public_titulaire_etat
    3: public_titulaire_militaire
    4: public_titulaire_territoriale
    5: public_titulaire_hospitaliere
    6: public_non_titulaire
    '''
    cadre = (statut == 8) * (chpub > 3) * cadre
    # noncadre = (statut ==8)*(chpub>3)*not_(cadre)

    # etat_stag = (chpub==1)*(titc == 1)
    etat_tit = (chpub == 1) * (titc == 2)
    etat_cont = (chpub == 1) * (titc == 3)

    militaire = 0  # TODO:

    # colloc_stag = (chpub==2)*(titc == 1)
    colloc_tit = (chpub == 2) * (titc == 2)
    colloc_cont = (chpub == 2) * (titc == 3)

    # hosp_stag = (chpub==2)*(titc == 1)
    hosp_tit = (chpub == 2) * (titc == 2)
    hosp_cont = (chpub == 2) * (titc == 3)

    contract = (colloc_cont + hosp_cont + etat_cont) > 1

    return (0 + 1 * cadre + 2 * etat_tit + 3 * militaire
            + 4 * colloc_tit + 5 * hosp_tit + 6 * contract)


def _taille_entreprise(nbsala):
    '''
    0 : "Non pertinent"
    1 : "Moins de 10 salariés"
    2 : "De 10 à 19 salariés"
    3 : "De 20 à 199 salariés"
    4 : "Plus de 200 salariés"
    '''
    return (0 + 1 * (nbsala >= 1) + 1 * (nbsala >= 4) + 1 * (nbsala >= 5)
              + 1 * (nbsala >= 7))


def build_pat(_P):
    '''
    Construit le dictionnaire de barèmes des cotisations patronales
    à partir des informations contenues dans P.cotsoc.pat
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    pat = scaleBaremes(BaremeDict('pat', _P.cotsoc.pat), plaf_ss)
    pat['noncadre'].update(pat['commun'])
    pat['cadre'].update(pat['commun'])
    pat['fonc']['contract'].update(pat['commun'])

    # Renaiming
    pat['prive_non_cadre'] = pat.pop('noncadre')
    pat['prive_cadre'] = pat.pop('cadre')

    log.info("Le dictionnaire des barèmes des cotisations patronales des non cadres contient: \n %s", pat['prive_non_cadre'].keys())
    log.info("Le dictionnaire des barèmes des cotisations patronales des cadres contient: \n %s", pat['prive_cadre'].keys())

    # Rework commun to deal with public employees
    for var in ["maladie", "apprentissage", "apprentissage2", "vieillesseplaf", "vieillessedeplaf", "formprof", "chomfg", "construction", "assedic"]:
        del pat['commun'][var]

    for var in ["apprentissage", "apprentissage2", "formprof", "chomfg", "construction", "assedic"]:
        del pat['fonc']['contract'][var]

    pat['fonc']['etat'].update(pat['commun'])
    pat['fonc']['colloc'].update(pat['commun'])
    del pat['commun']

    pat['etat_t'] = pat['fonc']['etat']
    pat['colloc_t'] = pat['fonc']['colloc']
    pat['contract'] = pat['fonc']['contract']

    for var in ['etat', 'colloc', 'contract' ]:
        del pat['fonc'][var]

    # Renaiming
    pat['public_titulaire_etat'] = pat.pop('etat_t')
    del pat['public_titulaire_etat']['rafp']

    pat['public_titulaire_territoriale'] = pat.pop('colloc_t')
    pat['public_titulaire_hospitaliere'] = pat['public_titulaire_territoriale']
    pat['public_non_titulaire'] = pat.pop('contract')

    log.info("Le dictionnaire des barèmes des cotisations patronales des salariés titulaires de l'etat contient : \n %s", pat['public_titulaire_etat'].keys())
    log.info("Le dictionnaire des barèmes des cotisations patronales titulaires des collectivités locales contient : \n %s", pat['public_titulaire_territoriale'].keys())
    log.info("Le dictionnaire des barèmes des cotisations patronales titulaires hospitaliers contient : \n %s", pat['public_titulaire_hospitaliere'].keys())
    log.error("Le dictionnaire des barèmes des cotisations patronales du public contractuels contient : \n %s", pat['public_non_titulaire'].keys())

    return pat


def _cotpat_contrib(salbrut, hsup, type_sal, indemnite_residence, primes, cot_pat_rafp, cot_pat_pension_civile, _P):
    '''
    Cotisation sociales patronales contributives
    '''
    pat = build_pat(_P)
    cotpat = zeros(len(salbrut))
    for category in CAT:
        iscat = (type_sal == category[1])  # category[1] is the numerical index
        if category[0] in pat.keys():
            for bar in pat[category[0]].itervalues():
                if category[0] in ["prive_cadre", "prive_non_cadre", "public_non_titulaire"]:  # TODO: move up
                    is_contrib = (bar.option == "contrib")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes))
                             ) * is_contrib
                    cotpat += temp
                    if is_contrib == 1:
                        log.info(bar)
                        log.info(temp)

        if category[0] == DEBUG_SAL_TYPE:
            log.error("rafp pat: %s" % str(cot_pat_rafp / 12))
            log.error("pension civile pat: %s" % str(cot_pat_pension_civile / 12))

    cotpat += cot_pat_rafp + cot_pat_pension_civile
    return cotpat

def _cotpat_main_d_oeuvre(salbrut, hsup, type_sal, primes, indemnite_residence, _P):
    '''
    Cotisation sociales patronales main d'oeuvre
    (TODO: complete avec justification TaxIPP)
    '''
    pat = build_pat(_P)
    cotpat = zeros(len(salbrut))
    for category in CAT:
        iscat = (type_sal == category[1])  # category[1] is the numerical index
        if category[0] in pat.keys():
            for bar in pat[category[0]].itervalues():
                is_mo = (bar.option == "main-d-oeuvre")
                temp = -(iscat
                         * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes))
                         * is_mo)
                cotpat += temp
                if is_mo == 1:
                    if  category[0] == DEBUG_SAL_TYPE:
                        log.error(category[0])
                        log.error(bar._name)
                        log.error(temp / 12)
    return cotpat


def _cotpat_transport(salbrut, hsup, type_sal, indemnite_residence, primes, _P):
    '''
    Versement transport
    '''
    pat = build_pat(_P)
    transport = zeros(len(salbrut))
    for category in CAT:
        iscat = (type_sal == category[1])  # category[1] is the numerical index of the category
        if category[0] in pat.keys():  # category[0] is the name of the category
            if 'transport' in pat[category[0]]:
                bar = pat[category[0]]['transport']
                temp = -bar.calc(salbrut + indemnite_residence + primes) * iscat  # check
                transport += temp
                if  category[0] == DEBUG_SAL_TYPE:
                    log.error(category[0])
                    log.error(bar._name)
                    log.error(temp / 12)
    return transport


def _cotpat_accident(salbrut, type_sal, taux_accident_travail):
    '''
    Cotisations patronales accident du travail et maladie professionelle
    '''
    prive = (type_sal == CAT['prive_non_cadre']) + (type_sal == CAT['prive_non_cadre'])
    return -salbrut * taux_accident_travail * prive  # TODO: check public


def _cotpat_noncontrib(salbrut, hsup, type_sal, primes, indemnite_residence, cotpat_accident, _P):
    '''
    Cotisation sociales patronales non contributives
    '''
    pat = build_pat(_P)
    cotpat = zeros(len(salbrut))
    for category in CAT:
        iscat = (type_sal == category[1])
        if category[0] in pat.keys():
            for bar in pat[category[0]].itervalues():
                is_noncontrib = (bar.option == "noncontrib")
                temp = -(iscat
                         * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes))
                         * is_noncontrib)
                cotpat += temp
                if is_noncontrib == 1:
                    if  category[0] == DEBUG_SAL_TYPE:
                        log.info(category[0])
                        log.error(bar)
                        log.error(temp / 12)
                        log.error("\n \n")

    log.error("accident : %s" % cotpat_accident)
    return cotpat + cotpat_accident

def _cotpat(cotpat_contrib, cotpat_noncontrib,
            cotpat_main_d_oeuvre, cotpat_transport):
    '''
    Cotisations sociales patronales
    '''
    return (cotpat_contrib + cotpat_noncontrib
            + cotpat_main_d_oeuvre + cotpat_transport)


def build_sal(_P):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    à partir des informations contenues dans P.cotsoc.sal
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss

    sal = scaleBaremes(BaremeDict('sal', _P.cotsoc.sal), plaf_ss)
    sal['noncadre'].update(sal['commun'])
    sal['cadre'].update(sal['commun'])

    # Renaiming
    sal['prive_non_cadre'] = sal.pop('noncadre')
    sal['prive_cadre'] = sal.pop('cadre')
    sal['public_titulaire_etat'] = sal['fonc']['etat']

    sal['public_titulaire_territoriale'] = sal['fonc']['colloc']
    sal['public_titulaire_hospitaliere'] = sal['fonc']['colloc']
    sal['public_non_titulaire'] = sal['fonc']['contract']

    for type_sal_category in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere',
                               'public_non_titulaire']:
        sal[type_sal_category]['excep_solidarite'] = sal['fonc']['commun']['solidarite']

    del sal['public_titulaire_etat']['rafp']
    del sal['public_titulaire_etat']['pension']

    sal['public_non_titulaire'].update(sal['commun'])
    del sal['public_non_titulaire']['arrco']
    del sal['public_non_titulaire']['assedic']

    # Cleaning
    del sal['commun']
    del sal['fonc']['etat']
    del sal['fonc']['colloc']
    del sal['fonc']['contract']

    log.info("Le dictionnaire des barèmes des salariés non cadres du privé  contient : \n %s \n", sal['prive_non_cadre'].keys())
    log.info("Le dictionnaire des barèmes des salariés cadres du privé contient : \n %s \n", sal['prive_cadre'].keys())
    log.info("Le dictionnaire des barèmes des salariés titulaires de l'etat contient : \n %s \n", sal['public_titulaire_etat'].keys())
    log.info("Le dictionnaire des barèmes des salariés titulaires des collectivités locales contient : \n %s \n", sal['public_titulaire_territoriale'].keys())
    log.info("Le dictionnaire des barèmes des salariés titulaires de la fonction publique hospitalière contient : \n %s \n", sal['public_titulaire_hospitaliere'].keys())
    log.error("Le dictionnaire des barèmes des salariés du public contractuels contient : \n %s \n", sal['public_non_titulaire'].keys())
    return sal


def seuil_fds(_P):
    '''
    Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    from math import  floor
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
    seuil_mensuel = floor(100 * (pt_ind * ind_maj_ref) / 12)
    return seuil_mensuel


def _cotsal_contrib(salbrut, hsup, type_sal, primes, indemnite_residence, cot_sal_rafp, cot_sal_pension_civile, _P):
    '''
    Cotisations sociales salariales contributives
    '''
    sal = build_sal(_P)
    cotsal = zeros(len(salbrut))
    for category in CAT:
        iscat = (type_sal == category[1])
        if category[0] in sal:
            for bar in sal[category[0]].itervalues():
                is_contrib = (bar.option == "contrib")
                temp = -(iscat
                         * bar.calc(salbrut - hsup
                                    + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes))
                        ) * is_contrib
                cotsal += temp
                if  category[0] == DEBUG_SAL_TYPE:
                    log.error(category[0])
                    log.error(bar._name)
                    log.error(temp / 12)

        if category[0] == DEBUG_SAL_TYPE:
            log.info("pension civile sal %s" % str(cot_sal_pension_civile / 12))
            log.info("rafp sal %s" % str(cot_sal_rafp / 12))

    public = ((type_sal == CAT['public_titulaire_etat'])
              + (type_sal == CAT['public_titulaire_territoriale'])
              + (type_sal == CAT['public_titulaire_hospitaliere']))
    return cotsal + (cot_sal_rafp + cot_sal_pension_civile) * public



def _cotsal_noncontrib(salbrut, hsup, type_sal, primes, indemnite_residence, _P):
    '''
    Cotisations sociales salariales non-contributives
    '''
    sal = build_sal(_P)
    cotsal = zeros(len(salbrut))
    seuil_assuj_fds = seuil_fds(_P)
    for category in CAT:
        iscat = (type_sal == category[1])
        if category[0] in sal:
            for bar in sal[category[0]].itervalues():
                is_noncontrib = (bar.option == "noncontrib")
                is_exempt_fds = (category[0] in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere']) * (bar._name == 'solidarite') * ((salbrut - hsup) <= seuil_assuj_fds)  # TODO: check assiette voir IPP
#                 if DEBUG:
#                     print bar._name
                is_noncontrib = (bar.option == "noncontrib") and (bar._name in ["famille", "maladie"])
                temp = -(iscat
                         * bar.calc(salbrut + (primes + indemnite_residence) - hsup) * (category[0] == 'public_non_titulaire')
                         * is_noncontrib * not_(is_exempt_fds)
                         )
                cotsal += temp
    return cotsal


def _cotsal(cotsal_contrib, cotsal_noncontrib):
    '''
    Cotisations sociales salariales
    '''
    return cotsal_contrib + cotsal_noncontrib


def _csgsald(salbrut, primes, indemnite_residence, hsup, _P):
    '''
    CSG deductible sur les salaires
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.deduc, plaf_ss)
    return -12 * csg.calc((salbrut + primes + indemnite_residence - hsup) / 12)


def _csgsali(salbrut, hsup, primes, indemnite_residence, _P):
    '''
    CSG imposable sur les salaires
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.impos, plaf_ss)
    return -12 * csg.calc((salbrut + primes + indemnite_residence - hsup) / 12)


def _crdssal(salbrut, hsup, primes, indemnite_residence, _P):
    '''
    CRDS sur les salaires
    '''
    plaf_ss = _P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.act, plaf_ss)
    return -12 * crds.calc((salbrut - hsup + primes + indemnite_residence) / 12)


def _sal_h_b(salbrut):
    '''
    Salaire horaire brut
    '''
    nbh_travaillees = 151.67 * 12
    return salbrut / nbh_travaillees


def _alleg_fillon(salbrut, sal_h_b, type_sal, taille_entreprise, _P):
    '''
    Allègement de charges patronales sur les bas et moyens salaires
    dit allègement Fillon
    '''
    if _P.datesim.year >= 2007:
        # TO DO: deal with taux between 2005 and 2007
        P = _P.cotsoc
        taux_fillon = taux_exo_fillon(sal_h_b, taille_entreprise, P)
        alleg_fillon = (taux_fillon * salbrut
                         * ((type_sal == CAT['prive_non_cadre'])
                                | (type_sal == CAT['prive_cadre'])))
        return alleg_fillon
    else:
        return 0 * salbrut


def _alleg_cice(salbrut, sal_h_b, type_sal, taille_entreprise, _P):
    '''
    Crédit d'imôt pour la compétitivité et l'emploi
    '''
    if _P.datesim.year >= 2013:
        P = _P.cotsoc
        taux_cice = taux_exo_cice(sal_h_b, P)
        alleg_cice = (taux_cice * salbrut
                        * or_((type_sal == CAT['prive_non_cadre']), (type_sal == CAT['prive_cadre'])))
        return alleg_cice
    else:
        return 0 * salbrut


def _taxes_sal(salbrut, tva_ent, _P):
    P = _P.cotsoc.taxes_sal
    maj = P.taux_maj  # TODO: exonérations apprentis
    taxes_sal = maj.calc(salbrut) + P.taux.metro * salbrut  # TODO: modify if DOM
    return -taxes_sal * not_(tva_ent)


def _tehr(salbrut, _P):
    """
    Taxe exceptionelle sur les hauts revenus
    """
    # TODO: a affiner avec condition de plafond
    #       sur le chiffre d'affaire des entreprises
    bar = _P.cotsoc.tehr
    return -bar.calc(salbrut)


def _sal(salbrut, primes, indemnite_residence, csgsald, cotsal, hsup):
    '''
    Calcul du salaire imposable
    '''
    return salbrut + primes + indemnite_residence + csgsald + cotsal - hsup


def _salnet(sal, crdssal, csgsali):
    '''
    Calcul du salaire net d'après définition INSEE
    net = net de csg et crds
    '''
    return sal + crdssal + csgsali


def _salsuperbrut(salbrut, primes, indemnite_residence, cotpat, alleg_fillon, alleg_cice, taxes_sal, tehr):
    """
    Salaires superbruts
    """
    salsuperbrut = salbrut + primes + indemnite_residence - cotpat - alleg_fillon - alleg_cice - taxes_sal - tehr
    expression = ("   salbrut             %s \n"
                  " + cotpat              %s \n"
                  " + primes              %s \n"
                  " + indemnite_residence %s \n"
                  " - alleg_fillon        %s \n"
                  " - alleg_cice          %s \n"
                  " + taxes_sal           %s \n"
                  " + tehr                %s \n"
                  " = salsuperbut         %s") % (salbrut, cotpat, primes, indemnite_residence,
                                                  - alleg_fillon, -alleg_cice, taxes_sal, tehr, salsuperbrut)
    log.info(expression)
    return salsuperbrut

def _cot_pat_pension_civile(salbrut, type_sal, _P):
    """
    Pension civile part patronale
    Note : salbrut est égal au traitement indiciaire brut 
    """
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    pat = scaleBaremes(BaremeDict('pat', _P.cotsoc.pat), plaf_ss)
    terr_or_hosp = (type_sal == CAT['public_titulaire_territoriale']) + (type_sal == CAT['public_titulaire_hospitaliere'])
    cot_pat_pension_civile = (
         (type_sal == CAT['public_titulaire_etat']) * pat['fonc']['etat']['pension'].calc(salbrut)
       + terr_or_hosp * pat['fonc']['colloc']['cnracl'].calc(salbrut)
                             )
    return -cot_pat_pension_civile

def _cot_sal_pension_civile(salbrut, type_sal, _P):
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    sal = scaleBaremes(BaremeDict('sal', _P.cotsoc.sal), plaf_ss)
    terr_or_hosp = (type_sal == CAT['public_titulaire_territoriale']) + (type_sal == CAT['public_titulaire_hospitaliere'])
    cot_sal_pension_civile = (
         (type_sal == CAT['public_titulaire_etat']) * sal['fonc']['etat']['pension'].calc(salbrut)
       + terr_or_hosp * sal['fonc']['colloc']['cnracl1'].calc(salbrut)
                             )
    return -cot_sal_pension_civile


def _cot_sal_rafp(salbrut, type_sal, primes, supp_familial_traitement, indemnite_residence, _P):
    '''
    Part salariale de la retraite additionelle de la fonction publique
    TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    Note: sal_brut est le traitement indiciaire brut pour les fonctionnaires
    '''
    eligibles = ((type_sal == CAT['public_titulaire_etat'])
                 + (type_sal == CAT['public_titulaire_territoriale'])
                 + (type_sal == CAT['public_titulaire_hospitaliere']))
    tib = salbrut * eligibles / 12
    plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
    base_imposable = primes + supp_familial_traitement + indemnite_residence
    plaf_ss = _P.cotsoc.gen.plaf_ss
    sal = scaleBaremes(BaremeDict('sal', _P.cotsoc.sal), plaf_ss)
    assiette = min_(base_imposable / 12 , plaf_ass * tib)
    # Même régime pour etat et colloc
    cot_sal_rafp = eligibles * sal['fonc']['etat']['rafp'].calc(assiette)
    return -12 * cot_sal_rafp

def _cot_pat_rafp(salbrut, type_sal, primes, supp_familial_traitement, indemnite_residence, _P):
    '''
    Part patronale de la retraite additionelle de la fonction publique
    TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    Note: salbrut est le traitement indiciaire brut pour les fonctionnaires
    '''
    eligibles = ((type_sal == CAT['public_titulaire_etat'])
                 + (type_sal == CAT['public_titulaire_territoriale'])
                 + (type_sal == CAT['public_titulaire_hospitaliere']))
    tib = salbrut * eligibles / 12
    plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
    base_imposable = primes + supp_familial_traitement + indemnite_residence
    plaf_ss = _P.cotsoc.gen.plaf_ss
    pat = scaleBaremes(BaremeDict('pat', _P.cotsoc.pat), plaf_ss)
    assiette = min_(base_imposable / 12, plaf_ass * tib)
    cot_pat_rafp = eligibles * pat['fonc']['etat']['rafp'].calc(assiette)
    return -12 * cot_pat_rafp


def _primes(type_sal, salbrut):
    '''
    Calcul des primes pour les fonctionnaries
    Note: sal_brut est égal au traitement indiciaire brut
    '''
<<<<<<< HEAD
    tib = salbrut * (type_sal == CAT['public_titulaire_etat'])
=======
    public = (type_sal == CAT['public_titulaire_etat']) + (type_sal == CAT['public_titulaire_territoriale']) + (type_sal == CAT['public_titulaire_hospitaliere'])
    tib = salbrut * public
>>>>>>> Cotisation sociales almost done
    return TAUX_DE_PRIME * tib


def _supp_familial_traitement(type_sal, salbrut, af_nbenf, _P):
    '''
    Supplément familial de traitement
    '''
    # TODO: un seul sft par couple où est présent un fonctionnaire
    fonc_nbenf = af_nbenf
    P = _P.fonc.supp_fam

    part_fixe_1 = P.fixe.enf1
    part_fixe_2 = P.fixe.enf2
    part_fixe_supp = P.fixe.enfsupp
    part_fixe = (part_fixe_1 * (fonc_nbenf >= 1) + (part_fixe_2 - part_fixe_1) * (fonc_nbenf >= 2) +
                  part_fixe_supp * max_(0, fonc_nbenf - 2))

    # pct_variable_1 = 0
    pct_variable_2 = P.prop.enf2
    pct_variable_3 = P.prop.enf3
    pct_variable_supp = P.prop.enfsupp
    pct_variable = (pct_variable_2 * (fonc_nbenf >= 2) + (pct_variable_3 - pct_variable_2) * (fonc_nbenf >= 3) +
                      pct_variable_supp * max_(0, fonc_nbenf - 3))

    indice_maj_min = P.IM_min
    indice_maj_max = P.IM_max

    plancher_mensuel_1 = P.fixe.enf1
    plancher_mensuel_2 = _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_2
    plancher_mensuel_3 = _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_3
    plancher_mensuel_supp = _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_supp

    plancher = (plancher_mensuel_1 * (fonc_nbenf >= 1) +
                (plancher_mensuel_2 - plancher_mensuel_1) * (fonc_nbenf >= 2) +
                (plancher_mensuel_3 - plancher_mensuel_2 - plancher_mensuel_1) * (fonc_nbenf >= 3) +
                plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

    plafond_mensuel_1 = P.fixe.enf1
    plafond_mensuel_2 = _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_2
    plafond_mensuel_3 = _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_3
    plafond_mensuel_supp = _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_supp

    plafond = (plafond_mensuel_1 * (fonc_nbenf >= 1) + (plafond_mensuel_2 - plafond_mensuel_1) * (fonc_nbenf >= 2) +
               (plafond_mensuel_3 - plafond_mensuel_2 - plafond_mensuel_1) * (fonc_nbenf >= 3) +
               plafond_mensuel_supp * max_(0, fonc_nbenf - 3))

    sft = min_(max_(part_fixe + pct_variable * salbrut, plancher), plafond) * (type_sal >= 2)
    # Nota Bene:
    # type_sal is an EnumCol which enum is:
    # CAT = Enum(['prive_non_cadre',
    #             'prive_cadre',
    #             'public_titulaire_etat',
    #             'public_titulaire_militaire',
    #             'public_titulaire_territoriale',
    #             'public_titulaire_hospitaliere',
    #             'public_non_titulaire'])
    return 12 * sft


def _traitement_brut_mensuel(indice_maj, _P):
    Indice_majore_100 = _P.fonc.IM_100
    traitement_brut = Indice_majore_100 * indice_maj / 1200
    return traitement_brut


def _indemnite_residence(salbrut, type_sal, zone_apl, _P):
    '''
    Indemnité de résidence des fonctionnaires
    '''
    P = _P.fonc.indem_resid
    min_zone_1, min_zone_2, min_zone_3 = P.min * P.taux.zone1, P.min * P.taux.zone2, P.min * P.taux.zone3
    taux = P.taux.zone1 * (zone_apl == 1) + P.taux.zone2 * (zone_apl == 2) + P.taux.zone3 * (zone_apl == 3)
    plancher = min_zone_1 * (zone_apl == 1) + min_zone_2 * (zone_apl == 2) + min_zone_3 * (zone_apl == 3)
    return 12 * max_(plancher, taux * salbrut / 12) * (type_sal >= 2)


def _indice_majore(type_sal, salbrut, _P):
    '''
    Indice majoré
    '''
    traitement_annuel_brut = _P.fonc.IM_100
    return (salbrut * 1200 / traitement_annuel_brut) * (type_sal >= 2)


def _gipa(type_sal, _P):
    '''
    Indemnité de garantie individuelle du pouvoir d'achat
    '''
    # http://www.emploi-collectivites.fr/salaire-fonction-publique#calcul-indice-salarial
    pass


############################################################################
# # Helper functions
############################################################################

def taux_exo_fillon(sal_h_b, taille_entreprise, P):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    # La divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    smic_h_b = P.gen.smic_h_b
    Pf = P.exo_bas_sal.fillon
    seuil = Pf.seuil
    tx_max = (Pf.tx_max * (taille_entreprise > 2) +
               Pf.tx_max2 * (taille_entreprise <= 2))
    if seuil <= 1:
        return 0
    return (tx_max * min_(1, max_(seuil * smic_h_b / (sal_h_b + 1e-10) - 1, 0)
                          / (seuil - 1)))


def taux_exo_cice(sal_h_b, P):
    smic_h_b = P.gen.smic_h_b
    Pc = P.exo_bas_sal.cice
    plafond = Pc.max * smic_h_b
    taux_cice = (sal_h_b <= plafond) * Pc.taux
    return taux_cice
