# -*- coding: utf-8 -*-

import logging


from openfisca_core.taxscales import MarginalRateTaxScale
from openfisca_france.model.base import *


# TODO:
# Manquent:
# - les agriculteurs
# - les cotisations minimales
# - la gestion de la temporatité


log = logging.getLogger(__name__)


class categorie_non_salarie(Variable):
    value_type = Enum
    possible_values = TypesCategorieNonSalarie
    default_value = TypesCategorieNonSalarie.non_pertinent
    entity = Individu
    label = "Type du travailleur salarié (artisant, commercant, profession libérale, etc)"
    definition_period = YEAR


class cotisations_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Cotisations sociales des travailleurs non salaries"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        profession_liberale = (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)

        deces_artisan_commercant = individu('deces_artisan_commercant', period)
        famille_independant = individu('famille_independant', period)
        formation_artisan_commercant = individu('formation_artisan_commercant', period)
        retraite_complementaire_artisan_commercant = individu('retraite_complementaire_artisan_commercant', period)
        maladie_maternite_artisan_commercant = individu('maladie_maternite_artisan_commercant', period)
        vieillesse_artisan_commercant = individu('vieillesse_artisan_commercant', period)
        formation_profession_liberale = individu('formation_profession_liberale', period)
        maladie_maternite_profession_liberale = individu('maladie_maternite_profession_liberale', period)
        vieillesse_profession_liberale = individu('vieillesse_profession_liberale', period)
        retraite_complementaire_profession_liberale = individu('retraite_complementaire_profession_liberale', period)

        cotisations_non_salarie = (
            (artisan + commercant) * (
                deces_artisan_commercant
                + famille_independant
                + formation_artisan_commercant
                + retraite_complementaire_artisan_commercant
                + maladie_maternite_artisan_commercant
                + vieillesse_artisan_commercant
                )
            + profession_liberale * (
                famille_independant
                + formation_profession_liberale
                + maladie_maternite_profession_liberale
                + vieillesse_profession_liberale
                + retraite_complementaire_profession_liberale
                )
            )
        return cotisations_non_salarie


class deces_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation décès des artisans et des commercants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'deces')
        deces = parameters(period).prelevements_sociaux.deces_ac.artisans
        bareme.add_bracket(0, deces.sous_pss)
        bareme.add_bracket(1, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_individu', period)

        return -bareme.calc(assiette)


class formation_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation formation des artisans et des commercants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        formation = parameters(period).prelevements_sociaux.formation_ac
        # Artisan
        bareme_artisan = MarginalRateTaxScale(name = 'formation_artisan')
        bareme_artisan.add_bracket(0, formation.artisans_sous_pss)
        bareme_artisan.add_bracket(1, 0)
        bareme_artisan.multiply_thresholds(plafond_securite_sociale_annuel)
        # Comemrcant
        bareme_commercant = MarginalRateTaxScale(name = 'formation_commercant')
        bareme_commercant.add_bracket(0, formation.commercants_industriels.sous_pss)
        bareme_commercant.add_bracket(1, 0)
        bareme_commercant.multiply_thresholds(plafond_securite_sociale_annuel)
        assiette = individu('rpns_individu', period)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        return -bareme_artisan.calc(assiette * artisan) - bareme_commercant.calc(assiette * commercant)


class maladie_maternite_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation maladie et maternité des artisans et des commercants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2018(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'famille')
        bareme.add_bracket(0, 0)
        bareme.add_bracket(1.1, .072)
        bareme.add_bracket(5, .065)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_individu', period)
        cotisation_sous_1_1_pss = assiette * (
            (assiette > .4 * plafond_securite_sociale_annuel) * (assiette <= 1.1 * plafond_securite_sociale_annuel)
            * (
                (.072 - .022) * assiette / (1.1 * plafond_securite_sociale_annuel) + .022
                )
            + (assiette <= .4 * plafond_securite_sociale_annuel)
            * (
                (.022 - .085) * assiette / (0.4 * plafond_securite_sociale_annuel) + .085
                )
            )
        return - (cotisation_sous_1_1_pss + bareme.calc(assiette))

    def formula_2017(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'famille')
        bareme.add_bracket(0, 0)
        bareme.add_bracket(.7, .065)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_individu', period)
        cotisation_sous_1_1_pss = assiette * (
            (assiette < .7 * plafond_securite_sociale_annuel)
            * (
                (.065 - .035) * assiette / (.7 * plafond_securite_sociale_annuel) + .035  # TODO check taux non nul à assiette quasi nulle
                )
            )
        return -(cotisation_sous_1_1_pss + bareme.calc(assiette))


class retraite_complementaire_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation de la retraite complémentaire des artisans et des commercants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2013(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        retraite_complementaire = parameters(period).prelevements_sociaux.ret_comp_ac.artisans_industriels_commercants
        montant_du_plafond_rci = retraite_complementaire.montant_du_plafond_rci
        bareme = MarginalRateTaxScale(name = 'retraite_complementaire')
        bareme.add_bracket(0, retraite_complementaire.sous_plafond_rci)
        bareme.add_bracket(montant_du_plafond_rci, retraite_complementaire.entre_1_plafond_rci_et_4_plafonds_pss)
        bareme.add_bracket(4 * plafond_securite_sociale_annuel, 0)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_individu', period)
        return -bareme.calc(assiette)


class vieillesse_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation vieillesse (plafonnée et déplafonnée) des artisans et des commercants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2014(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        vieillesse_artisan_commercant = parameters(period).prelevements_sociaux.ret_ac
        bareme = MarginalRateTaxScale(name = 'vieillesse')
        bareme.add_bracket(0, vieillesse_artisan_commercant.artisans.sous_pss + vieillesse_artisan_commercant.tous_independants.tout_salaire)
        bareme.add_bracket(1, vieillesse_artisan_commercant.tous_independants.tout_salaire)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_individu', period)
        return -bareme.calc(assiette)


class famille_independant(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation famille des indépendants"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'famille')
        bareme.add_bracket(0, 0)
        bareme.add_bracket(1.4, .031)  # TODO parsing des paramèters pas à jour
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_individu', period)
        taux = (
            0 + (.031) * min_(
                max_(
                    assiette / plafond_securite_sociale_annuel - 1.1,
                    0
                    ),
                (1.4 - 1.1)
                )
            / (1.4 - 1.1)
            )
        return - (
            taux * assiette * (assiette < 1.4 * plafond_securite_sociale_annuel)
            + bareme.calc(assiette)
            )


class formation_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation formation professionelle des professions libérales"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'formation_profession_liberale')
        taux = parameters(period).prelevements_sociaux.formation_pl.formation_professionnelle.sous_pss
        bareme.add_bracket(0, taux)
        bareme.add_bracket(1, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_individu', period)
        return -bareme.calc(assiette)


class maladie_maternite_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation maladie maternité des professions libérales"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'maladie_maternite')
        bareme.add_bracket(0, 0)
        bareme.add_bracket(1.1, .065)  # TODO parsing des paramèters IPP pas à jour
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_individu', period)
            )
        taux = (
            .015 + (.065 - .015) * min_(
                max_(
                    assiette / plafond_securite_sociale_annuel,
                    0
                    ),
                1.1
                )
            / 1.1
            )
        return - (
            taux * assiette * (assiette < 1.1 * plafond_securite_sociale_annuel)
            + bareme.calc(assiette)
            )


class retraite_complementaire_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation de retraite complémentarie des professions libérales"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2013(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'retraite_complementaire')
        bareme.add_bracket(0, .09)  # TODO taux à la louche car hétérogène
        bareme.add_bracket(5, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_individu', period)
        return -bareme.calc(assiette)


class vieillesse_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation retraite des professions libérales"
    definition_period = YEAR
    calculate_output = calculate_output_add

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).cotsoc.gen.plafond_securite_sociale * 12
        bareme = MarginalRateTaxScale(name = 'vieillesse')
        assurance_vieillesse = parameters(period).prelevements_sociaux.ret_pl.assurance_vieillesse
        bareme.add_bracket(0, assurance_vieillesse.sous_1_pss)
        bareme.add_bracket(1, assurance_vieillesse.entre_1_et_5_pss)
        bareme.add_bracket(5, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_individu', period)
        return -bareme.calc(assiette)
