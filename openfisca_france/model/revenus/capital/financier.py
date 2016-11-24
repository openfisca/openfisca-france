# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa


# RVCM
# revenus au prélèvement libératoire
class f2da(Variable):
    cerfa_field = u"2DA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %"
    start_date = date(2008, 1, 1)
    stop_date = date(2012, 12, 31)

  # à vérifier sur la nouvelle déclaration des revenus 2013

class f2dh(Variable):
    cerfa_field = u"2DH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %"



class f2ee(Variable):
    cerfa_field = u"2EE"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Autres produits de placement soumis aux prélèvements libératoires"



# revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
class f2dc(Variable):
    cerfa_field = u"2DC"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus des actions et parts donnant droit à abattement"



class f2fu(Variable):
    cerfa_field = u"2FU"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement"


class f2ch(Variable):
    cerfa_field = u"2CH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement"



#  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
class f2ts(Variable):
    cerfa_field = u"2TS"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)"


class f2go(Variable):
    cerfa_field = u"2GO"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)"


class f2tr(Variable):
    cerfa_field = u"2TR"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)"




# Autres revenus des valeurs et capitaux mobiliers
class f2cg(Variable):
    cerfa_field = u"2CG"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible"



class f2bh(Variable):
    cerfa_field = u"2BH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible"
    start_date = date(2007, 1, 1)



class f2ca(Variable):
    cerfa_field = u"2CA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Frais et charges déductibles"



class f2ck(Variable):
    cerfa_field = u"2CK"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé"
    start_date = date(2013, 1, 1)

  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

class f2ab(Variable):
    cerfa_field = u"2AB"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Crédits d'impôt sur valeurs étrangères"



class f2bg(Variable):
    cerfa_field = u"2BG"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables"



class f2aa(Variable):
    cerfa_field = u"2AA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2007, 1, 1)



class f2al(Variable):
    cerfa_field = u"2AL"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2008, 1, 1)



class f2am(Variable):
    cerfa_field = u"2AM"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2009, 1, 1)



class f2an(Variable):
    cerfa_field = u"2AN"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2010, 1, 1)



class f2aq(Variable):
    cerfa_field = u"2AQ"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2011, 1, 1)



class f2ar(Variable):
    cerfa_field = u"2AR"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits"
    start_date = date(2012, 1, 1)



# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
#
class f2as(Variable):
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des années antérieures non encore déduits: année 2012"
    stop_date = date(2011, 12, 31)

  # TODO: vérifier existence <=2011

class f2dm(Variable):
    cerfa_field = u"2DM"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %"
    start_date = date(2008, 1, 1)

  # TODO: nouvelle case à utiliser où c'est nécessaire
# TODO: vérifier existence avant 2012

class f2gr(Variable):
    cerfa_field = u"2GR"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)"
    start_date = date(2005, 1, 1)
    stop_date = date(2009, 12, 31)

  # TODO: vérifier existence à partir de 2011


# Utilisés par mes aides. TODO: à consolider
class epargne_non_remuneree(Variable):
    column = FloatCol
    entity = Individu
    base_function = requested_period_last_value
    label = u"Épargne non rémunérée"

class interets_epargne_sur_livrets(Variable):
    column = FloatCol
    entity = Individu
    base_function = requested_period_last_value
    label = u"Intérêts versés pour l'épargne sur livret"

class revenus_capital(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenus du capital"
