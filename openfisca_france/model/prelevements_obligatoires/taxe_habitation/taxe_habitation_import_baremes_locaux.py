# -*- coding: utf-8 -*-

import os
import csv
import codecs
import pkg_resources
import sys
import openfisca_france
from numpy import fromiter
from openfisca_france.model.base import *


# Importe les barèmes locaux de la taxe d'habitation


def preload_taux_by_com(year = None):
    global taux_by_com
    taux_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            taux_by_com = {
                row['code_insee_commune']: row['taux_com']
                for row in csv_reader
                }


def preload_taux_by_epci(year = None):
    global taux_by_epci
    taux_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            taux_by_epci = {
                row['code_insee_commune']: row['taux_epci']
                for row in csv_reader
                }


def preload_valeur_locative_moyenne_by_com(year = None):
    global valeur_locative_moyenne_by_com
    valeur_locative_moyenne_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            valeur_locative_moyenne_by_com = {
                row['code_insee_commune']: row['valeur_locative_moyenne_com']
                for row in csv_reader
                }


def preload_valeur_locative_moyenne_by_epci(year = None):
    global valeur_locative_moyenne_by_epci
    valeur_locative_moyenne_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            valeur_locative_moyenne_by_epci = {
                row['code_insee_commune']: row['valeur_locative_moyenne_epci']
                for row in csv_reader
                }


def preload_abt_general_base_by_com(year = None):
    global abt_general_base_by_com
    abt_general_base_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_general_base_by_com = {
                row['code_insee_commune']: row['abt_general_base_com']
                for row in csv_reader
                }


def preload_abt_general_base_by_epci(year = None):
    global abt_general_base_by_epci
    abt_general_base_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_general_base_by_epci = {
                row['code_insee_commune']: row['abt_general_base_epci']
                for row in csv_reader
                }


def preload_abt_pac_1_2_by_com(year = None):
    global abt_pac_1_2_by_com
    abt_pac_1_2_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_pac_1_2_by_com = {
                row['code_insee_commune']: row['abt_pac_1_2_com']
                for row in csv_reader
                }


def preload_abt_pac_1_2_by_epci(year = None):
    global abt_pac_1_2_by_epci
    abt_pac_1_2_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_pac_1_2_by_epci = {
                row['code_insee_commune']: row['abt_pac_1_2_epci']
                for row in csv_reader
                }


def preload_abt_pac_3pl_by_com(year = None):
    global abt_pac_3pl_by_com
    abt_pac_3pl_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_pac_3pl_by_com = {
                row['code_insee_commune']: row['abt_pac_3pl_com']
                for row in csv_reader
                }


def preload_abt_pac_3pl_by_epci(year = None):
    global abt_pac_3pl_by_epci
    abt_pac_3pl_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_pac_3pl_by_epci = {
                row['code_insee_commune']: row['abt_pac_3pl_epci']
                for row in csv_reader
                }


def preload_abt_condition_modeste_by_com(year = None):
    global abt_condition_modeste_by_com
    abt_condition_modeste_by_com = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_condition_modeste_by_com = {
                row['code_insee_commune']: row['abt_condition_modeste_com']
                for row in csv_reader
                }


def preload_abt_condition_modeste_by_epci(year = None):
    global abt_condition_modeste_by_epci
    abt_condition_modeste_by_epci = None
    assert year is not None
    if os.path.isfile('{}/assets/taxe_habitation/parametres_th_{}.csv'.format(openfisca_france.__name__, year)):
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/taxe_habitation/parametres_th_{}.csv'.format(year),
                ) as csv_file:
            if sys.version_info < (3, 0):
                csv_reader = csv.DictReader(csv_file)
            else:
                utf8_reader = codecs.getreader("utf-8")
                csv_reader = csv.DictReader(utf8_reader(csv_file))
            abt_condition_modeste_by_epci = {
                row['code_insee_commune']: row['abt_condition_modeste_epci']
                for row in csv_reader
                }


class code_INSEE_commune(Variable):
    value_type = str
    default_value = "01001"
    max_length = 5
    entity = Menage
    label = u"Code INSEE de la commune de résidence du ménage"
    definition_period = YEAR


class taux_th_commune(Variable):
    value_type = float
    default_value = 0
    entity = Menage
    label = u"Taux de taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_taux_by_com(year = annee)
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
    label = u"Taux de taxe d'habitation de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_taux_by_epci(year = annee)
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
    label = u"Valeur locative moyenne utilisée pour le calcul des abattements de la taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_valeur_locative_moyenne_by_com(year = annee)
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
    label = u"Valeur locative moyenne utilisée pour le calcul des abattements de la taxe d'habitation de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_valeur_locative_moyenne_by_epci(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement général à la base - taxe d'habitation de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_general_base_by_com(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement général à la base - taxe d'habitation de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_general_base_by_epci(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les deux premières personnes à charge - TH de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_pac_1_2_by_com(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les deux premières personnes à charge - TH de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_pac_1_2_by_epci(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les personnes à charge à partir de la troisième - TH de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_pac_3pl_by_com(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement obligatoire pour charges de famille, pour les personnes à charge à partir de la troisième - TH de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_pac_3pl_by_epci(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement pour personnes de condition modeste - TH de la commune"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_condition_modeste_by_com(year = annee)
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
    label = u"Quotité (ajustée) de l'abattement pour personnes de condition modeste - TH de l'EPCI"
    definition_period = YEAR

    def formula(menage, period):
        code_INSEE_commune = menage('code_INSEE_commune', period)
        annee = period.start.offset('first-of', 'year').year
        preload_abt_condition_modeste_by_epci(year = annee)
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
