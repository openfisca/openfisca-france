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

from openfisca_france.scripts.calculateur_impots.base import general_variable_name_by_tax_calculator_code

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

    request = urllib2.Request('https://www3.impots.gouv.fr/simulateur/cgi-bin/calc-{}.cgi'.format(year + 1), headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    page_doc = etree.parse(cStringIO.StringIO(response_html), etree.HTMLParser())
    fields = collections.OrderedDict()
    names = general_variable_name_by_tax_calculator_code

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
