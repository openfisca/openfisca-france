#! /usr/bin/env python
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


import collections
import json
import os
import sys
import urllib
import urllib2

from lxml import etree

def main():

    year = 2011
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        '0DA': 1970,
        'pre_situation_famille': 'C',
        '0CF': 0, # nombre de personnes à charge
#        '0F1': 1990, # âge de la première personne à charge
        '0BT': 0, # case T
        '1AJ': 60000,
    }

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-'+str(year+1)+'.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })

    response = urllib2.urlopen(request, urllib.urlencode(impots_arguments))

    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()
    names = {   'CIGE': u'Crédit aides aux personnes',
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
                'NAPCRP': u'Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d\'activité et de remplacement',
                'NBPT': u'Nombre de parts',
                'NBP': u'Nombre de parts',
                'PERPPLAFTV': u'Plafond de déduction pour les revenus 2014 au titre de l\'épargne retraite, pour déclarant 1',
                'PPETOT': u'Prime pour l\'emploi',
                'REVKIRE': u'Revenu fiscal de réfgrepérence',
                'RNICOL': u'Revenu net imposable ou déficit à reporter',
                'RRBG': u'Revenu brut global ou déficit',
                'TOTPAC': u'Nombre de personnes à charge',
                'TXMARJ': u'Taux marginal d\'imposition',
                'TXMOYIMP': u'Taux moyen d\'imposition',
                'IRETS' : u'?',#TODO
                'RNI': u'?',#TODO
                'CIRCM': u'?',#TODO (f2dc)
                'BCSG': u'?',#TODO (f2dc)
                'BRDS': u'?',#TODO (f2dc)
                'NAPCS': u'?',#TODO (f2dc)
                'NAPRD': u'?',#TODO (f2dc)
                'NAPPS': u'?',#TODO (f2dc)
                'CICA': u'?',#TODO (f4tq)
                'CIHABPRIN': u'?',#TODO (f7vy)
                'CIPRETUD': u'?',#TODO (f7uk)
                'BPRS': u'?',#TODO (f2ch)
                'CIDEVDUR': u'?',#TODO (f7wf)
                'CIADCRE': u'?',#TODO (f7dg) 
                'RFOR': u'?',#TODO (f7up)       
                'PERPPLAFTC': u'?',#TODO (f2ch, f2dh, marpac)      
            }
    for element in page_doc.xpath('//input[@type="hidden"][@name]'): 
        code = element.get('name')
        fields[code] = {
            'code' : code,
            'name' : names[code] if (code in names) else u'nom inconnu',
            'value' : float(element.get('value').replace(" ","")),
            }
    for code in ('IINET', 'ITRED'):
        print u'{} : {} ({})'.format(code, fields[code]['value'], fields[code]['name']).encode('utf-8')


if __name__ == "__main__":
    sys.exit(main())

