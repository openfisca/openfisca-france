#! /usr/bin/env python
# -*- coding: utf-8 -*-

########### DESCRIPTION ############
## Ce script (qui n'est pas utilisé par l'UI) sert à calculer les impôts dûs par les différentes combinaisons
## de foyers fiscaux quand les jeunes adultes ont le choix d'être rattachés au foyer fiscal de leurs parents
## Il prend en entrée un scenario contenant un unique foyer fiscal, où sont rattachés les enfants.
## Il ne gère ni le cas de séparation des parents, ni les pensions alimentaires. Même si pour la séparation, il suffit
## de faire tourner le programme deux fois en rattachant successivement les enfants au parent1 puis au parent2 ;
## et pour les pensions il suffit d'inscrire une pension versée et reçue au sein même du foyer (mais le script n'aide pas
## à calculer la pension optimale - qui est la plupart du temps la pension maximale (5698€ si l'enfant n'habite pas chez
## les parents)
#TODO: gestion des APL et autres prestations (pour l'instant on retourne l'irpp, je ne sais pas si en retournant le
# revenu disponible on gérerait les droits aux prestations)


import copy
import logging
import numpy as np
import os

import openfisca_france

from openfisca_france.model.base import *


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
tax_benefit_system = openfisca_france.FranceTaxBenefitSystem()


def split(scenario):
# On fait l'hypothèse que le scénario ne contient qu'un seul foyer fiscal
    tax_benefit_system = scenario.tax_benefit_system
    test_case = scenario.test_case
    foyer_fiscal = test_case['foyers_fiscaux'][0]
    individus = test_case['individus']
    year = scenario.period
    rattachements_possibles = [] # Contient en réalité les détachements possibles puisqu'au départ tous les membres sous rattachés au même foyer
    detachements_impossibles = []
    scenarios = []
    impots = []

    for pac_index, pac_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
        pac = individus[pac_id].copy()
        age = year - pac.pop('date_naissance').year - 1
        if 18 <= age < (21 + 4 * (pac['activite'] == TypesActivite.etudiant)): # Exprime la condition de rattachement au foyer pour les majeurs
            rattachements_possibles.append(pac_id)
        else:
            detachements_impossibles.append(pac_id)

    foyers_possibles = partiesDe(list(rattachements_possibles))
    n = len(foyers_possibles)
    j = 1
    min_ = [-1, 0]
    for i in range(0, n):
        scenarios.append(scenario.__class__())
        scenarios[i].__dict__ = copy.copy(scenario.__dict__)
        scenarios[i].test_case = copy.deepcopy(scenario.test_case)
        scenarios[i].test_case['foyers_fiscaux'][0]['personnes_a_charge'] = foyers_possibles[i]+detachements_impossibles
        for jeune in rattachements_possibles:
            if jeune not in foyers_possibles[i]:
                scenarios[i].test_case['foyers_fiscaux'][j] = { 'declarants': [jeune], 'personnes_a_charge': [] }
                j += 1
        scenarios[i].suggest()
        simulation  = scenarios[i].new_simulation()
        irpp = - round(np.sum(simulation.calculate('irpp')))
        if irpp < min_[1] or min_[0] == -1:
            min_ = [i, irpp]
        impots.append(irpp)

    print "Le plus avantageux pour votre famille est que les jeunes rattachés à votre foyer fiscal soient : {}. Vous paierez alors {}€ d'impôts. (Seuls les jeunes éligibles au rattachement sont indiqués (18 <= age < 21 si pas étudiant / 25 sinon. Le calculateur a émis l'hypothèse qu'il n'y avait qu'un seul foyer fiscal au départ, auquel tous les jeunes éligibles étaient rattachés.)".format(foyers_possibles[min_[0]],min_[1])
    return impots


def partiesDe(tab): # Calcule l'ensemble des parties des éléments d'un array, sous forme d'un array d'arrays
    n = len(tab)
    if n == 0:
        return [[]]
    else:
        a = tab.pop()
        tab2 = partiesDe(tab)
        return add(a, tab2)


def add(a, tab): # Concatène un array d'arrays (tab) avec le même array où un élément (a) aura été rajouté à chaque sous-array
    n = len(tab)
    for i in range (0, n):
        b = list(tab[i])
        tab.append(b)
        tab[i].append(a)
    return tab


def define_scenario(year):
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        parent1 = dict(
            activite = u'actif',
            date_naissance = 1973,
#            cadre = True,
            salaire_imposable = 90000,
            statut_marital = u'celibataire',
            ),
        enfants = [
            dict(
                activite = u'etudiant',
                date_naissance = '1992-02-01',
                ),
            dict(
                activite = u'etudiant',
                date_naissance = '2000-04-17',
                ),
            ],
        foyer_fiscal = dict(  #TODO: pb avec f2ck
#                f7cn = 1500,
                f7rd = 100000
            ),
        period = year,
        )
    scenario.suggest()
    return scenario


def main():
    split(define_scenario(2014))
    return 0


if __name__ == "__main__":
#    sys.exit(main())
    main()
