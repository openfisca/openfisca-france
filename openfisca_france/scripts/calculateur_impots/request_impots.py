#! /usr/bin/env python
# -*- coding: utf-8 -*-

########### DESCRIPTION ############
## Ce script affiche le résultat de la simulation officielle (DGFiP) en renseignant les champs CERFA_FIELDS
## On peut choisir d'afficher seulement certaines variables en décommentant la ligne 254


import collections
import cStringIO
import json
import os
import sys
import urllib
import urllib2

from lxml import etree

def main():

    year = 2013
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        '0DA': 1970,
#        '0DB': 1970,
        'pre_situation_famille': 'C',
#        '0CF': 2, # nombre de personnes à charge
#        '0F1': 1990, # âge de la première personne à charge
#        '0BT': 1, # case T
        '1AJ': 48000,
#        '5HO': 10000,
        '5NK': 5000
    }

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-' + str(year + 1) + '.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    page_doc = etree.parse(cStringIO.StringIO(response_html), etree.HTMLParser())
    fields = collections.OrderedDict()
    names = {   # Sert à afficher le nom des variables retournées par le script
                #TODO: mutualiser ce dictionnaire avec compare_openfisca_impots, qui contient le même
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
                'BCSG': u'Base CSG',
                'BRDS': u'Base CRDS',
                'BPRS': u'Base prélèvement social et contributions annexes',
                'NAPCS': u'Montant net CSG',
                'NAPRD': u'Montant net CRDS',
                'NAPPS': u'Montant net prélèvement social et contributions annexes',
                'CIRCM': u'?',#TODO (f2dc)
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
                'PERPPLAFTC': u'?',#TODO (f2ch, f2dh, marpac)
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
                'RCODELOP': u'?',#TODO (7uh)
                'RCOLENT': u'?',#TODO (7ls)
                'RDIFAGRI': u'?',#TODO (7um)
                'RDONS': u'?',#TODO (7uf)
                'RDUFLOGIH': u'?',#TODO (7gh)
                'REI': u'?',#TODO (f8tf)
                'RFORET': u'?',#TODO (f7uc)
                'RINVDOMTOMLG': u'?',#TODO (f7ui)
                'RTELEIR': u'?',#TODO (7ul)
                'RCOTFOR': u'?',#TODO (7ul)
                'RCELLIER': u'?',#TODO (7hk)
                'RCELCOM': u'?',#TODO (7np)
                'RCELJP': u'?',#TODO (7jp)
                'RCELHL': u'?',#TODO (7hl)
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
                'RLOCIDEFG': u'?',#TODO (7id)
                'RRESINEUV': u'?',#TODO (7ij)
                'RCELNBGL': u'?',#TODO (7nb)
                'RFCPI': u'?',#TODO (7gq)
                'RFIPC': u'?',#TODO (7fm)
                'RILMIA': u'?',#TODO (7ia)
                'RILMIB': u'?',#TODO (7ib)
                'RILMIC': u'?',#TODO (7ic)
                'RILMIH': u'?',#TODO (7ih)
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
                'RINVRED': u'?',#TODO (7it)
                'RREDREP': u'?',#TODO (7iu)
                'RILMIX': u'?',#TODO (7ix)
                'RILMIZ': u'?',#TODO (7iz)
                'RILMJI': u'?',#TODO (7ji)
                'RILMJS': u'?',#TODO (7ji)
                'RCODJT': u'?',#TODO (7jt)
                'RCODJU': u'?',#TODO (7jt)
                'RCODJV': u'?',#TODO (7jv)
                'RCODJW': u'?',#TODO (7jw)
                'RCODJX': u'?',#TODO (7jx)
                'RPRESCOMPREP': u'?',#TODO (7wp)
                'RCELRREDLM': u'?',#TODO
                'RRIRENOV': u'?',#TODO (7nz)
                'RFIPC': u'?',#TODO
                'RILMJX': u'?',#TODO
                'RILMJV': u'?',#TODO
                'RCELREPHG': u'?',#TODO
                'RILMJW': u'?',#TODO
                'RCELREPGV': u'?',#TODO
                'RCELRREDMG': u'?',#TODO
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
            'code' : code,
            'name' : names[code] if (code in names) else u'nom inconnu',
            'value' : float(element.get('value').replace(" ","")),
            }
#    for code in ('ITRED',):
        print u'{} : {} ({})'.format(code, fields[code]['value'], fields[code]['name']).encode('utf-8')


if __name__ == "__main__":
#    sys.exit(main())
    main()
