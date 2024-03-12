import logging


from openfisca_core.taxscales import MarginalRateTaxScale
from openfisca_france.model.base import *


# TODO:
# Manquent:
# - les agriculteurs
# - les cotisations minimales
# - la gestion de la temporatité

# Il manque également le régime micro social qui consiste en un forfait unique couvrant l'ensemble des cotisations ainsi que la csg et la crds
# https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073189/LEGISCTA000037051840/#LEGISCTA000037051840


log = logging.getLogger(__name__)


class categorie_non_salarie(Variable):
    value_type = Enum
    possible_values = TypesCategorieNonSalarie
    default_value = TypesCategorieNonSalarie.non_pertinent
    entity = Individu
    label = 'Type du travailleur salarié (artisan, commercant, profession libérale, etc)'
    definition_period = YEAR


class cotisations_non_salarie_micro_social(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisations sociales des travailleurs non salaries'
    definition_period = YEAR

    def formula_2009_01_01(individu, period, parameters):
        assiette_service = individu.foyer_fiscal('assiette_service', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        assiette_vente = individu.foyer_fiscal('assiette_vente', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        assiette_proflib = individu.foyer_fiscal('assiette_proflib', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        cotisations_prestation = parameters(period).prelevements_sociaux.professions_liberales.auto_entrepreneur
        cotisations_non_salarie_micro_social = (
            assiette_service * cotisations_prestation.cotisations_prestations.service
            + assiette_vente * cotisations_prestation.cotisations_prestations.vente
            + assiette_proflib * cotisations_prestation.cotisations_prestations.cipav
            )
        return - cotisations_non_salarie_micro_social

    def formula_2011_01_01(individu, period, parameters):
        assiette_service = individu.foyer_fiscal('assiette_service', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        assiette_vente = individu.foyer_fiscal('assiette_vente', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        assiette_proflib = individu.foyer_fiscal('assiette_proflib', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        cotisations_prestation = parameters(period).prelevements_sociaux.professions_liberales.auto_entrepreneur
        cotisations_non_salarie_micro_social = (
            assiette_service * (cotisations_prestation.cotisations_prestations.service + cotisations_prestation.formation_professionnelle.servicecom_chiffre_affaires)
            + assiette_vente * (cotisations_prestation.cotisations_prestations.vente + cotisations_prestation.formation_professionnelle.ventecom_chiffre_affaires)
            + assiette_proflib * (cotisations_prestation.cotisations_prestations.cipav + cotisations_prestation.formation_professionnelle.professions_liberales_chiffre_affaires)
            )
        return - cotisations_non_salarie_micro_social


class cotisations_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisations sociales des travailleurs non salaries'
    definition_period = YEAR

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
        cotisations_non_salarie_micro_social = individu('cotisations_non_salarie_micro_social', period)

        return cotisations_non_salarie + cotisations_non_salarie_micro_social


class deces_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation décès des artisans et invalidité-décès des commercants'
    definition_period = YEAR

    def formula_2004(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        deces_ac = parameters(period).prelevements_sociaux.cotisations_taxes_independants_artisans_commercants.deces_ac
        # Artisan
        bareme_artisan = MarginalRateTaxScale(name = 'deces_artisan')
        bareme_artisan.add_bracket(0, deces_ac.artisans.sous_pss)
        bareme_artisan.add_bracket(1, 0)
        bareme_artisan.multiply_thresholds(plafond_securite_sociale_annuel)
        # Commercant (Invalidite + Deces)
        bareme_commercant = MarginalRateTaxScale(name = 'deces_commercant')
        bareme_commercant.add_bracket(0, deces_ac.commercants_industriels.apres_2004.sous_pss)
        bareme_commercant.add_bracket(1, 0)
        bareme_commercant.multiply_thresholds(plafond_securite_sociale_annuel)
        # Calcul du montant
        assiette = individu('rpns_imposables', period)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        return -bareme_artisan.calc(assiette * artisan) - bareme_commercant.calc(assiette * commercant)

    def formula_1975(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        deces_ac = parameters(period).prelevements_sociaux.cotisations_taxes_independants_artisans_commercants.deces_ac
        # Avant 2004, le montant était forfaitaire pour les commerçants
        montant_commercant = deces_ac.commercants_industriels.avant_2004.montant_forfaitaire_total
        categorie_non_salarie = individu('categorie_non_salarie', period)
        # Artisan
        bareme_artisan = MarginalRateTaxScale(name = 'deces_artisan')
        bareme_artisan.add_bracket(0, deces_ac.artisans.sous_pss)
        bareme_artisan.add_bracket(1, 0)
        bareme_artisan.multiply_thresholds(plafond_securite_sociale_annuel)
        assiette = individu('rpns_imposables', period)
        # Type
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)

        return -bareme_artisan.calc(assiette * artisan) - (montant_commercant * commercant)


class formation_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation formation des artisans et des commercants'
    definition_period = YEAR

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        formation = parameters(period).prelevements_sociaux.cotisations_taxes_independants_artisans_commercants.formation_ac
        # Artisan
        bareme_artisan = MarginalRateTaxScale(name = 'formation_artisan')
        bareme_artisan.add_bracket(0, formation.artisans.sous_pss)
        bareme_artisan.add_bracket(1, 0)
        bareme_artisan.multiply_thresholds(plafond_securite_sociale_annuel)
        # Commercant
        bareme_commercant = MarginalRateTaxScale(name = 'formation_commercant')
        bareme_commercant.add_bracket(0, formation.commercants_industriels.sous_pss)
        bareme_commercant.add_bracket(1, 0)
        bareme_commercant.multiply_thresholds(plafond_securite_sociale_annuel)
        assiette = individu('rpns_imposables', period)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        return -bareme_artisan.calc(assiette * artisan) - bareme_commercant.calc(assiette * commercant)


class maladie_maternite_artisan_commercant_taux(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie et maternité des artisans et des commercants'
    definition_period = YEAR

    def formula_2020_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            )
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_imposables', period)
        assiette_pss = assiette / plafond_securite_sociale_annuel

        taux = where(assiette_pss != 0, (
            0.0085 + ((0.041 - 0.0085) * min_(max_(assiette_pss, 0), 0.4) / 0.4)
            + ((0.072 - 0.041) * min_(max_((assiette_pss) - 0.4, 0), 0.7) / (1.1 - 0.4))
            - (0.007 * (assiette_pss > 5) * ((assiette_pss - 5) / assiette_pss))
            ), 0)

        return artisan * taux

    def formula_2018_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            )
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_imposables', period)
        assiette_pss = assiette / plafond_securite_sociale_annuel
        taux = (
            0.0085 + ((0.041 - 0.0085) * min_(max_(assiette_pss, 0), 0.4) / 0.4)
            + ((0.072 - 0.041) * min_(max_((assiette_pss) - 0.4, 0), 0.7) / (1.1 - 0.4))
            - (0.007 * (assiette_pss > 5))
            )

        return artisan * where(assiette_pss != 0, taux, 0)

    def formula_2017_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        artisan = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            )
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_imposables', period)
        taux = (0.03 + (0.065 - 0.03) * min_(max_(assiette / plafond_securite_sociale_annuel, 0), 0.7) / 0.7) + 0.007

        return artisan * taux


class maladie_maternite_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie et maternité des artisans et des commercants'
    definition_period = YEAR

    def formula(individu, period):
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_imposables', period)
        taux = individu('maladie_maternite_artisan_commercant_taux', period)

        return -(taux * assiette)


class retraite_complementaire_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation de la retraite complémentaire des artisans et des commercants'
    definition_period = YEAR

    def formula_2013(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        retraite_complementaire = parameters(period).prelevements_sociaux.cotisations_taxes_independants_artisans_commercants.ret_comp_ac.art_ind_com
        montant_du_plafond_rci = retraite_complementaire.montant_du_plafond_rci
        bareme = MarginalRateTaxScale(name = 'retraite_complementaire')
        bareme.add_bracket(0, retraite_complementaire.sous_plafond_rci)
        bareme.add_bracket(montant_du_plafond_rci, retraite_complementaire.entre_1_plafond_rci_et_4_plafonds_pss)
        bareme.add_bracket(4 * plafond_securite_sociale_annuel, 0)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            ) * individu('rpns_imposables', period)
        return -bareme.calc(assiette)


class vieillesse_artisan_commercant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation vieillesse (plafonnée et déplafonnée) des artisans et des commercants'
    definition_period = YEAR

    def formula_2014(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        vieillesse_artisan_commercant = parameters(period).prelevements_sociaux.cotisations_taxes_independants_artisans_commercants.ret_ac
        bareme = MarginalRateTaxScale(name = 'vieillesse')
        categorie_non_salarie = individu('categorie_non_salarie', period)
        # Les taux sous_pss sont les mêmes pour artisans et commercants
        bareme.add_bracket(0, vieillesse_artisan_commercant.artisans.sous_pss + vieillesse_artisan_commercant.tous_independants.tout_salaire)
        bareme.add_bracket(1, vieillesse_artisan_commercant.tous_independants.tout_salaire)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        artisan = (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
        commercant = (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
        assiette = (artisan + commercant) * individu('rpns_imposables', period)
        return -bareme.calc(assiette)


class famille_independant(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation famille des indépendants'
    definition_period = YEAR

    def formula_2018_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_imposables', period)
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
        return - (taux * assiette)

    def formula_2015_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.artisan)
            + (categorie_non_salarie == TypesCategorieNonSalarie.commercant)
            + (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_imposables', period)
        taux = (
            0.0215 + (.031) * min_(
                max_(
                    assiette / plafond_securite_sociale_annuel - 1.1,
                    0
                    ),
                (1.4 - 1.1)
                )
            / (1.4 - 1.1)
            )
        return - (taux * assiette)


class formation_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation formation professionelle des professions libérales'
    definition_period = YEAR

    def formula(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        bareme = MarginalRateTaxScale(name = 'formation_profession_liberale')
        taux = parameters(period).prelevements_sociaux.professions_liberales.formation_pl.sous_pss
        bareme.add_bracket(0, taux)
        bareme.add_bracket(1, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_imposables', period)
        return -bareme.calc(assiette)


class maladie_maternite_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation maladie maternité des professions libérales'
    definition_period = YEAR

    def formula_2022_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_imposables', period)
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
        cotisation_supplementaire = 0.003 * min_(assiette, (3 * plafond_securite_sociale_annuel))

        return - (
            (taux * assiette) + cotisation_supplementaire
            )

    def formula_2021_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_imposables', period)
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
        cotisation_supplementaire = 0.0015 * min_(assiette, (3 * plafond_securite_sociale_annuel))

        return - (
            (taux * assiette) + cotisation_supplementaire
            )

    def formula_2018_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_imposables', period)
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
            taux * assiette
            )

    def formula_2017_01_01(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_imposables', period)
            )
        taux = (
            .03 + (.065 - .03) * min_(
                max_(
                    assiette / plafond_securite_sociale_annuel,
                    0
                    ),
                0.7
                )
            / 0.7
            )
        return - (
            taux * assiette
            )

    def formula_2012_12_31(individu, period, parameters):
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            * individu('rpns_imposables', period)
            )
        return - (
            0.065 * assiette
            )


class retraite_complementaire_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation de retraite complémentarie des professions libérales'
    definition_period = YEAR

    def formula_2013(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        bareme = MarginalRateTaxScale(name = 'retraite_complementaire')
        bareme.add_bracket(0, .09)  # TODO taux à la louche car hétérogène
        bareme.add_bracket(5, 0)  # TODO on peut améliorer le calcul car on a les parametres
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_imposables', period)
        return -bareme.calc(assiette)


class vieillesse_profession_liberale(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation retraite des professions libérales'
    definition_period = YEAR

    def formula_2015(individu, period, parameters):
        plafond_securite_sociale_annuel = parameters(period).prelevements_sociaux.pss.plafond_securite_sociale_annuel
        bareme = MarginalRateTaxScale(name = 'vieillesse')
        assurance_vieillesse = parameters(period).prelevements_sociaux.professions_liberales.ret_pl.assurance_vieillesse
        bareme.add_bracket(0, assurance_vieillesse.sous_1_pss)
        bareme.add_bracket(1, assurance_vieillesse.entre_1_et_5_pss)
        bareme.add_bracket(5, 0)
        bareme.multiply_thresholds(plafond_securite_sociale_annuel)
        categorie_non_salarie = individu('categorie_non_salarie', period)
        assiette = (
            (categorie_non_salarie == TypesCategorieNonSalarie.profession_liberale)
            ) * individu('rpns_imposables', period)
        return -bareme.calc(assiette)
