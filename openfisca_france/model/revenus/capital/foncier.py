# -*- coding: utf-8 -*-

from ...base import *  # noqa


# Rentes viagères
build_column('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1AW'))

build_column('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1BW'))
build_column('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1CW'))
build_column('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1DW'))


# Revenus fonciers
build_column('f4ba', IntCol(entity = 'foy',
    label = u"Revenus fonciers imposables",
    val_type = "monetary",
    cerfa_field = u'4BA'))

build_column('f4bb', IntCol(entity = 'foy',
    label = u"Déficit imputable sur les revenus fonciers",
    val_type = "monetary",
    cerfa_field = u'4BB'))

build_column('f4bc', IntCol(entity = 'foy',
    label = u"Déficit imputable sur le revenu global",
    val_type = "monetary",
    cerfa_field = u'4BC'))

build_column('f4bd', IntCol(entity = 'foy',
    label = u"Déficits antérieurs non encore imputés",
    val_type = "monetary",
    cerfa_field = u'4BD'))

build_column('f4be', IntCol(entity = 'foy',
    label = u"Micro foncier: recettes brutes sans abattement",
    val_type = "monetary",
    cerfa_field = u'4BE'))

# Prime d'assurance loyers impayés
build_column('f4bf', IntCol(entity = 'foy',
    label = u"Primes d'assurance pour loyers impayés des locations conventionnées",
    val_type = "monetary",
    cerfa_field = u'4BF'))

build_column('f4bl', IntCol(entity = 'foy', label = u"",
    end = date(2009, 12, 31)))  # TODO: cf 2010 2011

# Variables utilisées par mes aides TODO: consolider
class revenus_locatifs(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus locatifs"

class valeur_locative_immo_non_loue(Variable):
    column = FloatCol
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Valeur locative des biens immobiliers possédés et non loués"

class valeur_locative_terrains_non_loue(Variable):
    column = FloatCol
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Valeur locative des terrains possédés et non loués"
