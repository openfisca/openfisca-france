#! /usr/bin/env python
# -*- coding: utf-8 -*-
########### DESCRIPTION ############
## Ce programme est utilisé pour renseigner les dates de début et de fin des variables d'entrée
## Il n'est a priori plus utile puisque désormais ces dates ont été remplies dans OpenFisca
## Ce programme trouve, à partir de 2005, les cases qui sont présentes dans la déclaration de revenus
## grâce à des requêtes au simulateur de la DGFiP
## Le résultat est date_variables.json qui contient pour chaque variable, les années à partir desquelles la case existe
## ATTENTION : ce script interroge le simulateur en ligne de la DGFiP, qui n'est pas complet : certaines cases de la déclaration pro (2042 c) n'y sont pas, ainsi certaines variables peuvent exister même si le .json dit le contraire. Le fichier 2_init_foyer_3_encapsulation3.sas peut aider pour ces cas-là (il vient d'INES, voir avec Mahdi)

import codecs
import collections
import cStringIO
import json
import os
import sys
import urllib
import urllib2

from lxml import etree

import openfisca_france
tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()


def main():
    global dates
    dates = {}

    def test(var):
        global dates, t
        t = 0
        p = 0
        j = 3
        year = 2005
        dates[var] = []

        def requete(p, i, year, var):
            global t, dates, j
            j = min(i, 8 - 1 * p * (year < 2010))
            path = 'http://www3.finances.gouv.fr/calcul_impot/' + str(year + 1) + '/complet/calc_c_p' + str(p) + str(j) + '_data.htm'
            request = urllib2.Request(path, headers = {
                'User-Agent': 'OpenFisca-Script',
                })
            response = urllib2.urlopen(request)
            response_html = response.read()
            if 'Erreur' in response_html:
                raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
            page_doc = etree.parse(cStringIO.StringIO(response_html), etree.HTMLParser())
            for element in page_doc.xpath('//input[@name]'):
                code = element.get('name')
                if code == var:
                    t = 1
                    j = i
                    dates[var].append(year) # Si la case existe pour l'année, on rajoute l'année dans le fichier résultat

        for year in range(2005,2014): # On teste toutes les pages du simulateur pour trouver la variable
            requete(p, j, year, var) # Pour accélérer le programme, on cherche d'abord à la même page pour l'année suivante
            for i in range(1, 10):
                if not t:
                    p = 0
                    requete(0, i, year, var)
            lim = 8 if year < 2010 else 9
            for i in range(0, lim):
                if not t:
                    p = 1
                    requete(1, i, year, var)
            t = 0

    for column in tax_benefit_system.variables.itervalues(): # On teste les variables une par une
        var = column.cerfa_field
        if isinstance(var, dict):
            for k,v in var.iteritems():
                if len('_' + v) > 2:
                    test('_' + v)
        elif var is not None:
            if len(var) > 1:
                test('_' + var)

        with codecs.open(os.path.join('dates_variables.json'),'w', encoding='utf-8') as fichier:
            json.dump(dates, fichier, encoding='utf-8', ensure_ascii=False, indent=2,
                sort_keys=True)

main()
