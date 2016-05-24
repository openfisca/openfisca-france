# -*- coding: utf-8 -*-

import numpy as np
import os
import pkg_resources
#import pandas
from datetime import datetime

asset_path =  os.path.join(
    pkg_resources.get_distribution('openfisca_france').location,
    'openfisca_france',
    'assets',
    'grilles_fonction_publique',
    )
    
xls_path =  os.path.join(
    asset_path,
    'testgrid_CNRACL.xlsx',
    )

csv_path = os.path.join(asset_path, 'territoriale_et_hospitaliere.csv')


datefunc = lambda x: datetime.strptime(x, '%Y-%m-%d')
test_grid = np.recfromcsv(csv_path, delimiter = ',', converters = {0: datefunc, 1: datefunc})

test_grid['categorie_salarie'] = 4
test_grid['categorie_salarie'][test_grid['versant'] == 'FPH'] = 5

test_grid['date_effet_fin'][(np.logical_not(test_grid['date_effet_fin'])).astype('bool')] = datetime(2999, 12, 31)


def get_indice(variable, period, categorie_salarie, corps, grade, echelon):

    indice_majore = variable.zeros()
    categories_salaries_grille = set(np.unique(categorie_salarie)).intersection(set([4, 5]))
    assert (np.logical_or(categorie_salarie == 4, categorie_salarie == 5) == True).all(), "Bad categorie_salarie: {}".format(categorie_salarie)
    
    corpses_grille = set(np.unique(corps)) - set([''])
    
    grades_grille = set(np.unique(grade)) - set([''])
    assert (grade > 0).all(), "Bad grade: {}".format(grade)
    
    echelons_grille = set(np.unique(echelon)) - set([0])
    assert (np.logical_and(echelon >= test_grid['echelon'].min(), echelon <= test_grid['echelon'].max() )).all(), "Bad echelon: {}".format(echelon)
    
    for categorie_salarie_grille in categories_salaries_grille:
        for corps_grille in corpses_grille:
           for grade_grille in grades_grille:
               for echelon_grille in echelons_grille:
                    indice_grille = get_indice_from_grille(
                        period,
                        categorie_salarie_grille,
                        corps_grille,
                        grade_grille,
                        echelon_grille
                        )
                    condition = (
                       (categorie_salarie == categorie_salarie_grille) &
                       (corps == corps_grille) &
                       (grade == grade_grille) &
                       (echelon == echelon_grille)
                       )
                    
                    indice_majore = np.where(condition, indice_grille, indice_majore)

    return indice_majore

def get_indice_from_grille(period, categorie_salarie, corps, grade, echelon):
    date = datefunc(period.start.__str__())   
    indiv_grid = test_grid[
        (test_grid['categorie_salarie'] == categorie_salarie) &
        (test_grid['corps_label'] == corps) &
        (test_grid['grade'] == grade) &
        (test_grid['echelon'] == echelon) &
        (test_grid['date_effet_debut'] <= date) &
        (test_grid['date_effet_fin'] >= date)
        ]    
 
    return indiv_grid['im'].squeeze()
    
#def compute_tib(period, versant, corps, grade, echelon):
#
#    date = period.start
#    indiv_grid = test_grid[
#        (test_grid['versant'] == versant) &
#        (test_grid['corps_label'] == corps) &
#        (test_grid['grade'] == grade) &
#        (test_grid['echelon'] == echelon) &
#        (test_grid['date_effet_debut'] <= date) &
#        (test_grid['date_effet_fin'] >= date)
#        ]
#        
#    traitement_indiciaire_brut = indiv_grid.IM * simulation.legislation_at(period.start).cotsoc.sal.fonc.commun.pt_ind
#    return traitement_indiciaire_brut.values

