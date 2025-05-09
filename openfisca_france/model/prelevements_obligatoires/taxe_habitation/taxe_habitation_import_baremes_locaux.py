import os
import csv
import codecs
import importlib
import openfisca_france
from numpy import fromiter
from openfisca_france.model.base import *


# Importe les barèmes locaux de la taxe d'habitation


def preload_parametres_locaux_taxe_habitation(year = None, variable_to_load = None):
    assert variable_to_load is not None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with importlib.resources.files(
                openfisca_france.__name__).joinpath(
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ).open('rb') as csv_file:
            utf8_reader = codecs.getreader('utf-8')
            csv_reader = csv.DictReader(utf8_reader(csv_file))
            return {
                row['code_insee_commune']: row[variable_to_load]
                for row in csv_reader
                }


class taux_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Taux de taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        taux_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'taux_com')
        default_value = 0
        if taux_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    taux_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class taux_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Taux de taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        taux_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'taux_epci')
        default_value = 0
        if taux_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    taux_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class valeur_locative_moyenne_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Valeur locative moyenne utilisée pour le calcul des abattements de la taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        valeur_locative_moyenne_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'valeur_locative_moyenne_com')
        default_value = 0
        if valeur_locative_moyenne_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    valeur_locative_moyenne_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class valeur_locative_moyenne_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Valeur locative moyenne utilisée pour le calcul des abattements de la taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        valeur_locative_moyenne_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'valeur_locative_moyenne_epci')
        default_value = 0
        if valeur_locative_moyenne_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    valeur_locative_moyenne_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_general_base_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement général à la base - taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_general_base_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_general_base_com')
        default_value = 0
        if abt_general_base_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_general_base_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_general_base_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement général à la base - taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_general_base_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_general_base_epci')
        default_value = 0
        if abt_general_base_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_general_base_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_pac_1_2_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les deux premières personnes à charge - taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_pac_1_2_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_pac_1_2_com')
        default_value = 0
        if abt_pac_1_2_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_pac_1_2_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_pac_1_2_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les deux premières personnes à charge - taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_pac_1_2_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_pac_1_2_epci')
        default_value = 0
        if abt_pac_1_2_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_pac_1_2_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_pac_3pl_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les personnes à charge à partir de la troisième - taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_pac_3pl_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_pac_3pl_com')
        default_value = 0
        if abt_pac_3pl_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_pac_3pl_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_pac_3pl_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les personnes à charge à partir de la troisième - taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_pac_3pl_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_pac_3pl_epci')
        default_value = 0
        if abt_pac_3pl_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_pac_3pl_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_condition_modeste_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement pour personnes de condition modeste - taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_condition_modeste_by_com = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_condition_modeste_com')
        default_value = 0
        if abt_condition_modeste_by_com is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_condition_modeste_by_com.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant


class abt_condition_modeste_th_epci(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = "Quotité (ajustée) de l'abattement pour personnes de condition modeste - taxe d'habitation de l'EPCI (Établissement Public de Coopération Intercommunale)"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('depcom', period.first_month)
        annee = period.start.offset('first-of', 'year').year
        abt_condition_modeste_by_epci = preload_parametres_locaux_taxe_habitation(year = annee, variable_to_load = 'abt_condition_modeste_epci')
        default_value = 0
        if abt_condition_modeste_by_epci is None:
            montant = fromiter((default_value for code_INSEE_commune_cell in code_INSEE_commune), dtype = float)
        else:
            montant = fromiter(
                (
                    abt_condition_modeste_by_epci.get(code_INSEE_commune_cell if isinstance(code_INSEE_commune_cell, str) else code_INSEE_commune_cell.decode('utf-8'), default_value)
                    for code_INSEE_commune_cell in code_INSEE_commune
                    ),
                dtype = float,
                )
        return montant
