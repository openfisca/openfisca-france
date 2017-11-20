#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Use finances.gouv.fr web simulator as an API to compute income taxes."""


import argparse
import collections
import logging
import os
import sys
import urllib2

from lxml import etree


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    request = urllib2.Request('http://www3.finances.gouv.fr/calcul_impot/2014/simplifie/calc_s_data.htm', headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request)
    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()
    for element in page_doc.xpath('//*[@name]'):
        tag = element.tag.lower()
        if tag in ('a', 'form'):
            continue
        assert tag == 'input', tag
#        field = collections.OrderedDict(
#            (attribute_name, attribute_value)
#            for attribute_name, attribute_value in attributes.iteritems()
#            if attribute_value
#            )
        attributes = element.attrib
        name = attributes['name']
        type = attributes['type']
        if type in ('checkbox', 'radio'):
            existing_field = fields.get(name)
            if existing_field is None:
                field = collections.OrderedDict(
                    (attribute_name, attribute_value)
                    for attribute_name, attribute_value in attributes.iteritems()
                    if attribute_value
                    )
                if field.pop('checked', False):
                    field['default'] = field['value']
                field['values'] = [field.pop('value')]
                fields[name] = field
            else:
                value = attributes['value']
                for attribute_name, attribute_value in attributes.iteritems():
                    if attribute_name == 'value':
                        continue
                    if attribute_name == 'checked':
                        existing_field['default'] = value
                        continue
                    assert existing_field.get(attribute_name) == attribute_value, etree.tostring(element)
                existing_field['values'].append(value)
        else:
            assert type in ('hidden', 'text'), type
            assert name not in fields, name
            fields[name] = collections.OrderedDict(
                (attribute_name, attribute_value)
                for attribute_name, attribute_value in attributes.iteritems()
                if attribute_value
                )

    import json
    print json.dumps(fields, encoding = 'utf-8', ensure_ascii = False, indent = 2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
