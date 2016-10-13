#! /usr/bin/env python
# -*- coding: utf-8 -*-
#TODO: reduce margin error from 2 to 0 by coding the floor and round rules

"""Compare income taxes computed by finances.gouv.fr web simulator with OpenFisca results."""


########### DESCRIPTION ############
## Ce script compare la simulation OpenFisca d'un scenario (à définir ci-dessous) avec l'officielle (DGFiP)
## Il renvoie les erreurs d'OpenFisca : les valeurs attendues et les valeurs obtenues pour une dizaine de variables
## quand elles diffèrent de plus de la marge d'erreur (=2€ à ce jour)

import argparse
import collections
import cStringIO
import logging
import os
import sys
import urllib
import urllib2

from lxml import etree
import numpy as np

import openfisca_france
from openfisca_france.model.base import transform_scenario_to_tax_calculator_inputs


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()


def define_scenario(year):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        period = year,
        parent1 = dict(
            activite = u'Actif occupé',
            date_naissance = 1973,
            salaire_imposable = 48000,
            statut_marital = u'Marié',
            ),
        parent2 = dict(
            activite = u'Actif occupé',
            date_naissance = 1973,
            statut_marital = u'Marié',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '1993-02-01',
                ),
#            dict(
#                activite = u'Étudiant, élève',
#                date_naissance = '2000-04-17',
#                ),
            ],
        foyer_fiscal = dict(  #TODO: pb avec f2ck
            f5rn = 5000,
            mbic_mvct = 2000,
            ),
        )
    scenario.suggest()
    return scenario


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    year = 2010
    scenario = define_scenario(year)
    compare(scenario, tested = True)
    return 0


def compare(scenario, tested = False):
    year = scenario.period.date.year
    totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')

    impots_arguments = transform_scenario_to_tax_calculator_inputs(scenario)
    simulation = scenario.new_simulation(debug = True)

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-' + str(year + 1) + '.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    page_doc = etree.parse(cStringIO.StringIO(response_html), etree.HTMLParser())
    fields = collections.OrderedDict()
    names = {  # Sert à afficher le nom des variables retournées par le script
                #TODO: mutualiser ce dictionnaire avec request_impots, qui contient le même
        'CIGE': u'Crédit aides aux personnes',
        'CIRELANCE': u'Crédit d\'impôt exceptionnel sur les revenus 2008',
        'IAVIM': u'Impôt avant imputations',
        'IDEC': u'Décote',
        'IDRS2': u'Droits simples',
        'IINET': u'Montant net à payer',
        'IINETIR': u'Impôt sur le revenu net',
        'IREST': u'Montant net à restituer',
        'IRESTIR': u'Impôt sur le revenu net',
        'ITRED': u'Total des réductions d\'impôt',
        'I2DH': u'Prélèvement libératoire de 7,5%',
        'NAPCRP': u'Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d\'activité et'
            u' de remplacement',
        'NBPT': u'Nombre de parts',
        'NBP': u'Nombre de parts',
        'PERPPLAFTV': u'Plafond de déduction pour les revenus 2014 au titre de l\'épargne retraite, pour déclarant 1',
        'PPETOT': u'Prime pour l\'emploi',
        'REVKIRE': u'Revenu fiscal de référence',
        'RNICOL': u'Revenu net imposable ou déficit à reporter',
        'RRBG': u'Revenu brut global ou déficit',
        'TEFF': u'?',#TODO (ebnc_impo)
        'TOTPAC': u'Nombre de personnes à charge',
        'TXMARJ': u'Taux marginal d\'imposition',
        'TXMOYIMP': u'Taux moyen d\'imposition',
        'IRETS' : u'?',#TODO
        'RNI': u'?',#TODO
        'AVFISCOPTER': u'?',#TODO (f8tf)
        'CIRCM': u'?',#TODO (f2dc)
        'BCSG': u'Base CSG',
        'BRDS': u'Base CRDS',
        'BPRS': u'Base prélèvement social et contributions annexes',
        'NAPCS': u'Montant net CSG',
        'NAPRD': u'Montant net CRDS',
        'NAPPS': u'Montant net prélèvement social et contributions annexes',
        'CICA': u'?',#TODO (f4tq)
        'CICORSE': u'?',#TODO (f8to)
        'CIDEPENV': u'?',#TODO (f7sz)
        'CIGARD': u'?',#TODO (f7ga)
        'CIHABPRIN': u'?',#TODO (f7vy)
        'CIPRETUD': u'?',#TODO (f7uk)
        'CITEC': u'?',#TODO (f7wr)
        'CIDEVDUR': u'?',#TODO (f7wf)
        'CIADCRE': u'?',#TODO (f7dg)
        'CIMOBIL': u'?',#TODO (f1ar)
        'CIPERT': u'?',#TODO (f3vv)
        'IAVF2': u'?',#TODO (f8th)
        'IPROP': u'Impôt proportionnel',
        'RFOR': u'?',#TODO (f7up)
        'PERPPLAFTP': u'?',
        'PERPPLAFTC': u'?',#TODO (f2ch, f2dh, maries_ou_pacses)
        'RHEBE': u'?',#TODO (7ce)
        'RAA': u'?',#TODO (7ud)
        'RAH': u'?',#TODO (7ce)
        'RAIDE': u'?',#TODO (7df)
        'RCEL': u'?',#TODO (scellier)
        'RCELHJK': u'?',#TODO (scellier)
        'RCELHNO': u'?',#TODO (7hn)
        'RCELHM': u'?',#TODO (7hm)
        'RCELHR': u'?',#TODO (7hr)
        'RCELREPHS': u'?',#TODO (7hs)
        'RCELRRED09': u'?',#TODO (7la)
        'RCELRREDLD': u'?',#TODO (7ld)
        'RCELRREDLE': u'?',#TODO (7le)
        'RCELRREDLF': u'?',#TODO (7lf)
        'RCELRREDLM': u'?',#TODO (7lm)
        'RCELRREDMG': u'?',#TODO (7mg)
        'RCELREPHR': u'?',#TODO (scellier)
        'RCELRREDLA': u'?',#TODO (scellier)
        'RCELRREDLS': u'?',#TODO (7ls)
        'RCELREPGJ': u'?',#TODO (7gj)
        'RCELREPGK': u'?',#TODO (7gk)
        'RCELREPGL': u'?',#TODO (7gl)
        'RCELREPGW': u'?',#TODO (f7gw)
        'RCELREPGX': u'?',#TODO (f7gx)
        'RCELFD': u'?',#TODO (f7fd)
        'RCELRREDLB': u'?',#TODO (f7lb)
        'RCELRREDLC': u'?',#TODO (f7lc)
        'RCELRREDLZ': u'?',#TODO (f7lz)
        'RCONS': u'?',#TODO (7uh)
        'RCODJT': u'?',#TODO (7jt)
        'RCODJU': u'?',#TODO (7jt)
        'RCODJV': u'?',#TODO (7jv)
        'RCODJW': u'?',#TODO (7jw)
        'RCODJX': u'?',#TODO (7jx)
        'RCOLENT': u'?',#TODO (7ls)
        'RDIFAGRI': u'?',#TODO (7um)
        'RDONS': u'?',#TODO (7uf)
        'RDUFLOGIH': u'?',#TODO (7gh)
        'REI': u'?',#TODO (f8tf)
        'RILMIA': u'?',#TODO (7ia)
        'RILMIB': u'?',#TODO (7ib)
        'RILMIC': u'?',#TODO (7ic)
        'RILMIH': u'?',#TODO (7ih)
        'RILMJI': u'?',#TODO (7ji)
        'RILMJS': u'?',#TODO (7ji)
        'RFIPC': u'?',#TODO
        'RILMJX': u'?',#TODO
        'RILMJV': u'?',#TODO
        'RILMJW': u'?',#TODO
        'RCELREPHG': u'?',#TODO
        'RCELREPGV': u'?',#TODO
        'RCELRREDLM': u'?',#TODO
        'RCELRREDMG': u'?',#TODO
        'RFORET': u'?',#TODO (f7uc)
        'RINVDOMTOMLG': u'?',#TODO (f7ui)
        'RTELEIR': u'?',#TODO (7ul)
        'RCOTFOR': u'?',#TODO (7ul)
        'RCODELOP': u'?',#TODO (7uh)
        'RCELLIER': u'?',#TODO (7hk)
        'RCELCOM': u'?',#TODO (7np)
        'RCELHL': u'?',#TODO (7hl)
        'RCELJP': u'?',#TODO (7jp)
        'RCELJOQR': u'?',#TODO (7jo)
        'RCELNQ': u'?',#TODO (7nq)
        'RCELREPGP': u'?',#TODO (7gp)
        'RCELREPGS': u'?',#TODO (7gs)
        'RCELREPGU': u'?',#TODO (7gu)
        'RCELREPGT': u'?',#TODO (7gt)
        'RCELREPGV': u'?',#TODO (7gv)
        'RCELREPHA': u'?',#TODO (7ha)
        'RCELREPHB': u'?',#TODO (7hb)
        'RCELREPHD': u'?',#TODO (7hd)
        'RCELREPHE': u'?',#TODO (7he)
        'RCELREPHF': u'?',#TODO (7hf)
        'RCELREPHG': u'?',#TODO (7hg)
        'RCELREPHH': u'?',#TODO (7hh)
        'RCELREPHT': u'?',#TODO (7ht)
        'RCELREPHU': u'?',#TODO (7hu)
        'RCELREPHV': u'?',#TODO (7hv)
        'RCELREPHW': u'?',#TODO (7hw)
        'RCELREPHX': u'?',#TODO (7hx)
        'RCELREPHZ': u'?',#TODO (7hz)
        'RCELFABC': u'?',#TODO (7fa)
        'RCEL2012': u'?',#TODO (7ja)
        'RCELJBGL': u'?',#TODO (7jb)
        'RRESINEUV': u'?',#TODO (7ij)
        'RCELNBGL': u'?',#TODO (7nb)
        'RLOCIDEFG': u'?',#TODO (7id)
        'RFCPI': u'?',#TODO (7gq)
        'RFIPC': u'?',#TODO (7fm)
        'RINNO': u'?',#TODO (7gq)
        'RCINE': u'?',#TODO (7gn)
        'RIDOMENT': u'?',#TODO (7ur)
        'RIDOMPROE1': u'?',#TODO (f7sz)
        'RIDOMPROE2': u'?',#TODO (f7qz)
        'RIDOMPROE3': u'?',#TODO (f7qz)
        'RIDOMPROE4': u'?',#TODO (f7oz)
        'RIDOMPROE5': u'?',#TODO (f7oz)
        'RLOGDOM': u'?',#TODO (f7qd)
        'RNOUV': u'?',#TODO (cappme)
        'RPATNAT': u'?',#TODO (7ka)
        'RPATNATOT': u'?',#TODO (7ka)
        'RRDOM': u'?',#TODO (7ub)
        'RRESTIMO': u'?',#TODO (7rd)
        'RRESIVIEU': u'?',#TODO (7im)
        'RMEUBLE': u'?',#TODO (7ik)
        'RREDMEUB': u'?',#TODO (7is)
        'RREPA': u'?',#TODO (7ud)
        'RRPRESCOMP': u'?',#TODO (7wp)
        'RRESIMEUB': u'?',#TODO (7io)
        'RREPMEU': u'?',#TODO (7ip)
        'RPRESCOMPREP': u'?',#TODO (7wp)
        'RREPNPRO': u'?',#TODO (7ir)
        'RPROREP': u'?',#TODO (7is)
        'RINVRED': u'?',#TODO (7it)
        'RREDREP': u'?',#TODO (7iu)
        'RILMIX': u'?',#TODO (7ix)
        'RILMIZ': u'?',#TODO (7iz)
        'RRIRENOV': u'?',#TODO (7nz)
        'RSOCREPR': u'?',#TODO (7fh)
        'RSOUFIP':  u'?',#TODO (7fq)
        'RSURV': u'?',#TODO (7gz)
        'RTITPRISE': u'?',#TODO (7cu)
        'RTOURNEUF': u'?', #TODO (f7xc)
        'RTOURREP': u'?', #TODO (7xi)
        'RTOUREPA': u'?', #TODO (7xj)
        'RTOUHOTR': u'?', #TODO (7xk)
        'RTOUR': u'?',#TODO (f7xd)
        'RTOURTRA': u'?',#TODO (f7xc)
        'RTOURHOT': u'?',#TODO (f7xc)
        'RTOURES': u'?',#TODO (f7xc)
        }
    for element in page_doc.xpath('//input[@type="hidden"][@name]'):
        code = element.get('name')
        fields[code] = {
            'code': code,
            'name': names[code] if (code in names) else u'nom inconnu',
            'value': float(element.get('value').replace(" ", "")),
            }
    iinet = 1
    if tested:
        for code, field in fields.iteritems():
            if code == 'IINETIR' or code == 'IRESTIR':
                iinet = 0
            compare_variable(code, field, simulation, totpac, year)
#            print u'{} : {} ({})'.format(code, fields[code]['value'], fields[code]['name']).encode('utf-8')
#    print simulation.calculate('reductions')
#    print fields['ITRED']['value']
        if iinet: # S'il n'y a pas IINETIR et IRESTIR dans les résultats, on compare irpp à IINET (s'ils y sont c'est
                # normal que les résultats soient différents
            compare_variable('IINETIR', fields['IINET'], simulation, totpac, year)

    return fields


if __name__ == "__main__":
#    sys.exit(main())
    main()
