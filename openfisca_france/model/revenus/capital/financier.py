# -*- coding: utf-8 -*-

from ...base import *  # noqa


# RVCM
# revenus au prélèvement libératoire
build_column('f2da', IntCol(label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2DA',
                start = date(2008, 1, 1),
                end = date(2012, 12, 31)))  # à vérifier sur la nouvelle déclaration des revenus 2013

build_column('f2dh', IntCol(label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2DH'))

build_column('f2ee', IntCol(label = u"Autres produits de placement soumis aux prélèvements libératoires",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2EE'))

# revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
build_column('f2dc', IntCol(entity = 'foy',
                label = u"Revenus des actions et parts donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2DC'))

build_column('f2fu', IntCol(entity = 'foy',
                label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2FU'))
build_column('f2ch', IntCol(entity = 'foy',
                label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2CH'))

#  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
build_column('f2ts', IntCol(entity = 'foy', label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2TS'))
build_column('f2go', IntCol(entity = 'foy',
                label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2GO'))
build_column('f2tr', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2TR'))


# Autres revenus des valeurs et capitaux mobiliers
build_column('f2cg', IntCol(entity = 'foy',
                label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible",
                val_type = "monetary",
                cerfa_field = u'2CG'))

build_column('f2bh', IntCol(entity = 'foy',
                label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'2BH'))

build_column('f2ca', IntCol(entity = 'foy',
                label = u"Frais et charges déductibles",
                val_type = "monetary",
                cerfa_field = u'2CA'))

build_column('f2ck', IntCol(entity = 'foy',
                label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé",
                val_type = "monetary",
                cerfa_field = u'2CK',
                start = date(2013, 1, 1)))  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

build_column('f2ab', IntCol(entity = 'foy',
                label = u"Crédits d'impôt sur valeurs étrangères",
                val_type = "monetary",
                cerfa_field = u'2AB'))

build_column('f2bg', IntCol(entity = 'foy',
                label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables",
                val_type = "monetary",
                cerfa_field = u'2BG'))

build_column('f2aa', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'2AA'))

build_column('f2al', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                start = date(2008, 1, 1),
                cerfa_field = u'2AL'))

build_column('f2am', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                start = date(2009, 1, 1),
                cerfa_field = u'2AM'))

build_column('f2an', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AN',
                start = date(2010, 1, 1)))

build_column('f2aq', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AQ',
                start = date(2011, 1, 1)))

build_column('f2ar', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AR',
                start = date(2012, 1, 1)))

# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
#
build_column('f2as', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits: année 2012",
                val_type = "monetary",
                end = date(2011, 12, 31)))  # TODO: vérifier existence <=2011

build_column('f2dm', IntCol(entity = 'foy',
                label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %",
                val_type = "monetary",
                cerfa_field = u'2DM',
                start = date(2008, 1, 1)))  # TODO: nouvelle case à utiliser où c'est nécessaire
# TODO: vérifier existence avant 2012

build_column('f2gr', IntCol(entity = 'foy',
                label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)",
                val_type = "monetary",
                cerfa_field = u'2GR',
                start = date(2005, 1, 1),
                end = date(2009, 12, 31)))  # TODO: vérifier existence à partir de 2011


# Utilisés par mes aides. TODO: à consolider
class epargne_non_remuneree(Variable):
    column = FloatCol
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Épargne non rémunérée"

class interets_epargne_sur_livrets(Variable):
    column = FloatCol
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Intérêts versés pour l'épargne sur livret"

class revenus_capital(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus du capital"
