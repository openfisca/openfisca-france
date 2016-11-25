# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class pensions_alimentaires_percues(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AO",
        QUIFOY['conj']: u"1BO",
        QUIFOY['pac1']: u"1CO",
        QUIFOY['pac2']: u"1DO",
        QUIFOY['pac3']: u"1EO",
        }
    column = FloatCol(val_type = "monetary")
    entity = Individu
    label = u"Pensions alimentaires perçues"

  # (f1ao, f1bo, f1co, f1do, f1eo)
class pensions_alimentaires_percues_decl(Variable):
    column = BoolCol(default = True)
    entity = Individu
    label = u"Pension déclarée"



class pensions_alimentaires_versees_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"Pensions alimentaires versées pour un individu"



class gains_exceptionnels(Variable):
    column = FloatCol
    entity = Individu
    label = u"Gains exceptionnels"



class allocation_aide_retour_emploi(Variable):
    column = FloatCol
    entity = Individu
    label = u"Allocation d'aide au retour à l'emploi"


class allocation_securisation_professionnelle(Variable):
    column = FloatCol
    entity = Individu
    label = u"Allocation de sécurisation professionnelle"


class prime_forfaitaire_mensuelle_reprise_activite(Variable):
    column = FloatCol
    entity = Individu
    label = u"Prime forfaitaire mensuelle pour la reprise d'activité"


class indemnites_volontariat(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités de volontariat"


class dedommagement_victime_amiante(Variable):
    column = FloatCol
    entity = Individu
    label = u"Dédommagement versé aux victimes de l'amiante"


class prestation_compensatoire(Variable):
    column = FloatCol
    entity = Individu
    label = u"Prestation compensatoire"


class pensions_invalidite(Variable):
    column = FloatCol
    entity = Individu
    label = u"Pensions d'invalidité"


class bourse_enseignement_sup(Variable):
    column = FloatCol
    entity = Individu
    label = u"Bourse de l'enseignement supérieur"




# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
class f8ta(Variable):
    cerfa_field = u"8TA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Retenue à la source en France ou impôt payé à l'étranger"




class f8th(Variable):
    cerfa_field = u"8TH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Retenue à la source élus locaux"




class f8td_2002_2005(Variable):
    cerfa_field = u"8TD"
    column = IntCol
    entity = FoyerFiscal
    label = u"Contribution exceptionnelle sur les hauts revenus"
    start_date = date(2002, 1, 1)
    stop_date = date(2005, 12, 31)



class f8td(Variable):
    cerfa_field = u"8TD"
    column = BoolCol
    entity = FoyerFiscal
    label = u"Revenus non imposables dépassent la moitié du RFR"
    start_date = date(2011, 1, 1)
    stop_date = date(2014, 12, 31)




class f8ti(Variable):
    cerfa_field = u"8TK"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus de l'étranger exonérés d'impôt"



class f8tk(Variable):
    cerfa_field = u"8TK"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Revenus de l'étranger imposables"



# Auto-entrepreneur : versements libératoires d’impôt sur le revenu
class f8uy(Variable):
    cerfa_field = u"8UY"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé"
    start_date = date(2009, 1, 1)


