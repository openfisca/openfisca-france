#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Use finances.gouv.fr web simulator as an API to compute income taxes."""


import argparse
import collections
import logging
import os
import sys
import urllib
import urllib2

from lxml import etree


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-2014.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request, urllib.urlencode([
        ('0DA', '1965'),
        ('1AJ', '15000'),
        ('pre_situation_famille', 'C'),
        ('pre_situation_residence', 'M'),
#        ('simplifie', '1'),
        ]))

    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()

#    fieldsOpenFisca = collections.OrderedDict()

#    def fillFields(code, value):
#        if code == 'IAVIM':
#            # Impôt avant imputations
#            fieldsOpenFisca['iai']=value
#        elif code == 'IDEC':
#            # Décote
#            fieldsOpenFisca['decote']=value
#        elif code == 'IDRS2':
#            # Droits simples
#            fieldsOpenFisca['ir_plaf_qf']=value
#        elif code == 'IINET':
#            # Montant net à payer
#            pass
#        elif code == 'IINETIR':
#            # Impôt sur le revenu net
#            fieldsOpenFisca['irpp']=value
#        elif code == 'IREST':
#            # Montant net à restituer
#            pass
#        elif code == 'ITRED':
#            # Total des réductions d'impôt
#            fieldsOpenFisca['reductions']=value
#            pass
#        elif code == 'NAPCRP':
#            # Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d'activité et de remplacement
#            # de source étrangère)
#            # TODO
#            pass
#        elif code == 'NBPT':
#            # Nombre de parts
#            fieldsOpenFisca['nbptr']=value
#        elif code == 'PERPPLAFTV':
#            # Plafond de déduction pour les revenus 2014 au titre de l'épargne retraite, pour déclarant 1
#            # TODO
#            pass
#        elif code == 'PPETOT':
#            # Prime pour l'emploi
#            fieldsOpenFisca['ppe']=value
#        elif code == 'REVKIRE':
#            # Revenu fiscal de référence
#            fieldsOpenFisca['rfr']=value
#        elif code == 'RNICOL':
#            # Revenu net imposable ou déficit à reporter
#            fieldsOpenFisca['rni']=value
#        elif code == 'RRBG':
#            # Revenu brut global ou déficit
#            fieldsOpenFisca['rbg']=value
#        elif code == 'TOTPAC':
#            # Nombre de personnes à charge
#            fieldsOpenFisca['personnes_a_charge']=value
#        elif code == 'TXMARJ':
#            # Taux marginal d'imposition (revenus soumis au barème)
#            # TODO
#            pass
#        elif code == 'TXMOYIMP':
#            # Taux moyen d'imposition
#            # TODO
#            pass
#        else:
#            raise KeyError(u'Unexpected code {} = {}'.format(code, value).encode('utf-8'))

    for element in page_doc.xpath('//input[@type="hidden"][@name]'):
        tag = element.tag.lower()
        parent = element.getparent()
        parent_tag = parent.tag.lower()
        if parent_tag == 'table':
            tr = parent[parent.index(element) - 1]
            assert tr.tag.lower() == 'tr', tr
        else:
            assert parent_tag == 'tr'
            tr = parent
        while True:
            name = etree.tostring(tr[1], encoding = unicode, method = 'text').strip().rstrip(u'*').rstrip()
            if name:
                break
            table = tr.getparent()
            tr = table[table.index(tr) - 1]
        code = element.get('name')
        fields[code] = dict(
            code = code,
            name = name,
            value = float(element.get('value').strip()),
            )
#        fillFields(code,element.get('value'))
    import json
    print json.dumps(fields, encoding = 'utf-8', ensure_ascii = False, indent = 2)
#    print json.dumps(fieldsOpenFisca, encoding = 'utf-8', ensure_ascii = False, indent = 2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
