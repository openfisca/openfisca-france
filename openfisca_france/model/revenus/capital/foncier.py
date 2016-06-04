# -*- coding: utf-8 -*-

from ...base import *  # noqa


# Rentes viagères
class f1aw(Variable):
    cerfa_field = u"1AW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans"



class f1bw(Variable):
    cerfa_field = u"1BW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans"


class f1cw(Variable):
    cerfa_field = u"1CW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans"


class f1dw(Variable):
    cerfa_field = u"1DW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans"




# Revenus fonciers
class f4ba(Variable):
    cerfa_field = u"4BA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Revenus fonciers imposables"



class f4bb(Variable):
    cerfa_field = u"4BB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Déficit imputable sur les revenus fonciers"



class f4bc(Variable):
    cerfa_field = u"4BC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Déficit imputable sur le revenu global"



class f4bd(Variable):
    cerfa_field = u"4BD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Déficits antérieurs non encore imputés"



class f4be(Variable):
    cerfa_field = u"4BE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Micro foncier: recettes brutes sans abattement"



# Prime d'assurance loyers impayés
class f4bf(Variable):
    cerfa_field = u"4BF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Primes d'assurance pour loyers impayés des locations conventionnées"



class f4bl(Variable):
    column = IntCol
    entity_class = FoyersFiscaux
    stop_date = date(2009, 12, 31)

  # TODO: cf 2010 2011

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
