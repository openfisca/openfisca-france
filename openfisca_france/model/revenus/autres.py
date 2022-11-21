from openfisca_france.model.base import *


class pensions_alimentaires_percues(Variable):
    cerfa_field = {
        0: '1AO',
        1: '1BO',
        2: '1CO',
        3: '1DO',
        4: '1EO',
        }
    value_type = float
    unit = 'currency'
    entity = Individu
    label = 'Pensions alimentaires perçues'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class pensions_alimentaires_percues_decl(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = 'Pension déclarée'
    definition_period = YEAR


class pensions_alimentaires_versees_individu(Variable):
    value_type = float
    entity = Individu
    label = 'Pensions alimentaires versées pour un individu'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class gains_exceptionnels(Variable):
    value_type = float
    entity = Individu
    label = 'Gains exceptionnels'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class allocation_securisation_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = 'Allocation de sécurisation professionnelle'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prime_forfaitaire_mensuelle_reprise_activite(Variable):
    value_type = float
    entity = Individu
    label = "Prime forfaitaire mensuelle pour la reprise d'activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_volontariat(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités de volontariat'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class dedommagement_victime_amiante(Variable):
    value_type = float
    entity = Individu
    label = "Dédommagement versé aux victimes de l'amiante"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class prestation_compensatoire(Variable):
    value_type = float
    entity = Individu
    label = 'Prestation compensatoire'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class pensions_invalidite(Variable):
    value_type = float
    entity = Individu
    label = "Pensions d'invalidité"
    # Cette case est apparue dans la déclaration 2014
    # Auparavant, les pensions d'invalidité étaient incluses dans la case 1AS
    cerfa_field = {
        0: '1AZ',
        1: '1BZ',
        2: '1CZ',
        3: '1DZ',
        }
    # start_date = date(2014, 1, 1)
    definition_period = MONTH
    set_input = set_input_divide_by_period


class bourse_enseignement_sup(Variable):
    value_type = float
    entity = Individu
    label = "Toute bourse de l'enseignement supérieur"
    definition_period = MONTH
    set_input = set_input_divide_by_period


# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
class f8ta(Variable):
    cerfa_field = '8TA'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Retenue à la source en France ou impôt payé à l'étranger"
    definition_period = YEAR


class f8vl(Variable):
    cerfa_field = '8VL'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Impôt payé à l'étranger sur revenus de capitaux mobiliers et plus-values ouvrant droit à un crédit d'impôt"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f8vm(Variable):
    cerfa_field = {
        0: '8VM',
        1: '8WM',
        2: '8UM',
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Impôt payé à l'étranger sur revenus de capitaux mobiliers et plus-values ouvrant droit à un crédit d'impôt"
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


class f8th(Variable):
    cerfa_field = '8TH'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Retenue à la source élus locaux'
    end = '2016-12-31'
    definition_period = YEAR


class f8td_2002_2005(Variable):
    cerfa_field = '8TD'
    value_type = int
    entity = FoyerFiscal
    label = 'Contribution exceptionnelle sur les hauts revenus'
    # start_date = date(2002, 1, 1)
    end = '2005-12-31'
    definition_period = YEAR


class f8td(Variable):
    cerfa_field = '8TD'
    value_type = bool
    entity = FoyerFiscal
    label = 'Revenus non imposables dépassent la moitié du RFR'
    # start_date = date(2011, 1, 1)
    end = '2014-12-31'
    definition_period = YEAR


class f8ti(Variable):
    cerfa_field = '8TK'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Revenus de l'étranger exonérés d'impôt"
    definition_period = YEAR


# Auto-entrepreneur : versements libératoires d’impôt sur le revenu
class f8uy(Variable):
    cerfa_field = '8UY'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR
