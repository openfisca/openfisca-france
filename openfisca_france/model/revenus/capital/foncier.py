from openfisca_france.model.base import *


# Rentes viagères
class f1aw(Variable):
    cerfa_field = "1AW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans"
    definition_period = YEAR


class f1bw(Variable):
    cerfa_field = "1BW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans"
    definition_period = YEAR


class f1cw(Variable):
    cerfa_field = "1CW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans"
    definition_period = YEAR


class f1dw(Variable):
    cerfa_field = "1DW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans"
    definition_period = YEAR


# Revenus fonciers
class f4ba(Variable):
    cerfa_field = "4BA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Revenus fonciers imposables"
    definition_period = YEAR


class f4bb(Variable):
    cerfa_field = "4BB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Déficit imputable sur les revenus fonciers"
    definition_period = YEAR


class f4bc(Variable):
    cerfa_field = "4BC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Déficit imputable sur le revenu global"
    definition_period = YEAR


class f4bd(Variable):
    cerfa_field = "4BD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Déficits antérieurs non encore imputés"
    definition_period = YEAR


class f4be(Variable):
    cerfa_field = "4BE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Micro foncier: recettes brutes sans abattement"
    definition_period = YEAR


# Prime d'assurance loyers impayés
class f4bf(Variable):
    cerfa_field = "4BF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = "Primes d'assurance pour loyers impayés des locations conventionnées"
    end = '2016-12-31'
    definition_period = YEAR


class f4bl(Variable):
    value_type = int
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR
    # TODO: cf 2010 2011


# Variables utilisées par mes aides
class valeur_patrimoine_loue(Variable):
    value_type = float
    entity = Individu
    label = "Valeur des biens immobiliers et des terrains loués"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class revenus_locatifs(Variable):
    value_type = float
    entity = Individu
    label = "Revenus locatifs"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        """
        Revenus locatifs utilisés pour les bases ressources des minima sociaux
        Si cette variable n'est pas renseignée, on prend les revenus fonciers catégoriels de la section 4 de la déclaration 2042
        Néanmoins, selon la législation, le concept de revenus locatifs pour ces bases ressources peut être plus large, notamment
        pour les indépendants (exemple : case 5ND du formulaire 2042-C-PRO). Ce point reste à améliorer.
        """
        revenu_categoriel_foncier = individu.foyer_fiscal('revenu_categoriel_foncier', period.this_year)
        montant = revenu_categoriel_foncier * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) / 12
        return max_(montant, 0)


class valeur_immo_non_loue(Variable):
    value_type = float
    entity = Individu
    label = "Valeur des biens immobiliers possédés et non loués"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class valeur_locative_immo_non_loue(Variable):
    value_type = float
    entity = Individu
    label = "Valeur locative, à l'année, des biens immobiliers possédés et non loués"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class valeur_terrains_non_loues(Variable):
    value_type = float
    entity = Individu
    label = "Valeur des terrains possédés et non loués"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class valeur_locative_terrains_non_loues(Variable):
    value_type = float
    entity = Individu
    label = "Valeur locative, à l'année, des terrains possédés et non loués"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
