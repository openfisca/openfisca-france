# -*- coding: utf-8 -*-



import numpy as np
import os
import pkg_resources
import pandas

grilles_path =  os.path.join(
    pkg_resources.get_distribution('openfisca_france').location,
    'openfisca_france',
    'assets',
    'grilles_fonction_publique',
    'test_grid.xlsx',
    )
    
# Grille FPT fictive : ancienne et actuelle
test_grid = pandas.read_excel(grilles_path)

# Calculer le TBI
# Valeur du point d'indice
val_point = 4.3


def compute_tib(date, versant, corps, grade_num, echelon):
    # subset bon versant, corps, grade_nom, grade_num, echelon
    indiv_grid = test_grid.loc[
        (test_grid['versant'] == versant) & 
        (test_grid['corps'] == corps) &
        (test_grid['grade_num'] == grade_num) &
        (test_grid['echelon'] == echelon)
        ] 
    # subset bonne date
    indiv_grid_borne_sup = indiv_grid.loc[indiv_grid['date_effet_debut'] < date]
    date_debut_grid_indiv = indiv_grid_borne_sup['date_effet_debut'].max()
    indiv_grid = indiv_grid_borne_sup.loc[indiv_grid_borne_sup['date_effet_debut'] == date_debut_grid_indiv]
    # compute rem
    traitement_indiciaire_brut = indiv_grid.IM * val_point
    return traitement_indiciaire_brut.values



def get_indice(variable, period, categorie_salarie, corps, grade, echelon):
    indice_majore = variable.zeros()
    for categorie_salarie_grille in np.unique(categorie_salarie):
        for corps_grille in np.unique(corps):
            for grade_grille in np.unique(grade):
                for echelon_grille in np.unique(echelon):
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

def get_indice_from_grille(period, categorie_salarie, corps, grade_num, echelon):
    # subset bon versant, corps, grade_nom, grade_num, echelon
    date = int(period.__str__().replace('-', '') + '01')
    
    test_grid['categorie_salarie'] = 4
    test_grid.loc[test_grid['versant'] == 'FPH', 'categorie_salarie'] = 5    
    indiv_grid = test_grid.loc[
        (test_grid['categorie_salarie'] == categorie_salarie) & 
        (test_grid['corps'] == corps) &
        (test_grid['grade_num'] == grade_num) &
        (test_grid['echelon'] == echelon)
        ] 
    # subset bonne date
    indiv_grid_borne_sup = indiv_grid.loc[indiv_grid['date_effet_debut'] < date]
    date_debut_grid_indiv = indiv_grid_borne_sup['date_effet_debut'].max()
    indiv_grid = indiv_grid_borne_sup.loc[indiv_grid_borne_sup['date_effet_debut'] == date_debut_grid_indiv]
    # compute rem
    # TODO check unique value 
    return indiv_grid.IM.values.squeeze()


if __name__ == "__main__":
    # date = 20140201 
    versant, corps, grade_num, echelon =  'FPT', 'redacteur', 1, 13
    categorie_salarie = 4
    # print compute_tib(date, versant, corps, grade_num, echelon)
    from openfisca_core.periods import period    
    period = period("2014-02")
    print get_indice_from_grille(period, categorie_salarie, corps, grade_num, echelon)
         
