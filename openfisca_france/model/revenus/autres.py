# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class pensions_alimentaires_percues(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AO",
        QUIFOY['conj']: u"1BO",
        QUIFOY['pac1']: u"1CO",
        QUIFOY['pac2']: u"1DO",
        QUIFOY['pac3']: u"1EO",
        }
    value_type = float
    unit = 'currency'
    entity = Individu
    label = u"Pensions alimentaires perçues"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class pensions_alimentaires_percues_decl(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = u"Pension déclarée"
    definition_period = YEAR

class pensions_alimentaires_versees_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Pensions alimentaires versées pour un individu"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class gains_exceptionnels(Variable):
    value_type = float
    entity = Individu
    label = u"Gains exceptionnels"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class allocation_aide_retour_emploi(Variable):
    value_type = float
    entity = Individu
    label = u"Allocation d'aide au retour à l'emploi"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class allocation_securisation_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = u"Allocation de sécurisation professionnelle"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prime_forfaitaire_mensuelle_reprise_activite(Variable):
    value_type = float
    entity = Individu
    label = u"Prime forfaitaire mensuelle pour la reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_volontariat(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités de volontariat"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class dedommagement_victime_amiante(Variable):
    value_type = float
    entity = Individu
    label = u"Dédommagement versé aux victimes de l'amiante"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prestation_compensatoire(Variable):
    value_type = float
    entity = Individu
    label = u"Prestation compensatoire"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pensions_invalidite(Variable):
    value_type = float
    entity = Individu
    label = u"Pensions d'invalidité"
    # Cette case est apparue dans la déclaration 2014
    # Auparavant, les pensions d'invalidité étaient incluses dans la case 1AS
    cerfa_field = {
        QUIFOY['vous']: u"1AZ",
        QUIFOY['conj']: u"1BZ",
        QUIFOY['pac1']: u"1CZ",
        QUIFOY['pac2']: u"1DZ",
        }
    definition_period = MONTH
    set_input = set_input_divide_by_period


class bourse_enseignement_sup(Variable):
    value_type = float
    entity = Individu
    label = u"Bourse de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period


# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
class f8ta(Variable):
    cerfa_field = u"8TA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Retenue à la source en France ou impôt payé à l'étranger"
    definition_period = YEAR


class f8th(Variable):
    cerfa_field = u"8TH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Retenue à la source élus locaux"
    definition_period = YEAR


class f8td_2002_2005(Variable):
    cerfa_field = u"8TD"
    value_type = int
    entity = FoyerFiscal
    label = u"Contribution exceptionnelle sur les hauts revenus"
    # start_date = date(2002, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR


class f8td(Variable):
    cerfa_field = u"8TD"
    value_type = bool
    entity = FoyerFiscal
    label = u"Revenus non imposables dépassent la moitié du RFR"
    # start_date = date(2011, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class f8ti(Variable):
    cerfa_field = u"8TK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Revenus de l'étranger exonérés d'impôt"
    definition_period = YEAR


class f8tk(Variable):
    cerfa_field = u"8TK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Revenus de l'étranger imposables"
    definition_period = YEAR


# Auto-entrepreneur : versements libératoires d’impôt sur le revenu
class f8uy(Variable):
    cerfa_field = u"8UY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR
