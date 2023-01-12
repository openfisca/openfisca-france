from numpy.core.defchararray import startswith

from openfisca_france.model.base import *


class coloc(Variable):
    value_type = bool
    entity = Menage
    label = 'Vie en colocation'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class logement_crous(Variable):
    value_type = bool
    entity = Menage
    label = 'Le logement est géré par les CROUS '
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class logement_chambre(Variable):
    value_type = bool
    entity = Menage
    label = 'Le logement est considéré comme une chambre'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class loyer(Variable):
    value_type = float
    entity = Menage
    set_input = set_input_divide_by_period
    unit = 'currency'
    label = "Loyer ou mensualité d'emprunt pour un primo-accédant"
    definition_period = MONTH


class depcom(Variable):
    value_type = str
    max_length = 5
    entity = Menage
    label = 'Code INSEE (depcom) de la commune du lieu de résidence'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesCodeInseeRegion(Enum):
    __order__ = 'non_renseigne guadeloupe martinique guyane reunion mayotte ile_de_france centre_val_de_loire bourgogne_franche_comte normandie hauts_de_france grand_est pays_de_la_loire bretagne nouvelle_aquitaine occitanie auvergne_rhone_alpes provence_alpes_cote_d_azur corse'
    non_renseigne = 'Non renseigné'
    guadeloupe = '01'
    martinique = '02'
    guyane = '03'
    reunion = '04'
    mayotte = '06'
    ile_de_france = '11'
    centre_val_de_loire = '24'
    bourgogne_franche_comte = '27'
    normandie = '28'
    hauts_de_france = '32'
    grand_est = '44'
    pays_de_la_loire = '52'
    bretagne = '53'
    nouvelle_aquitaine = '75'
    occitanie = '76'
    auvergne_rhone_alpes = '84'
    provence_alpes_cote_d_azur = '93'
    corse = '94'


class region(Variable):
    value_type = Enum
    possible_values = TypesCodeInseeRegion
    default_value = TypesCodeInseeRegion.non_renseigne
    entity = Menage
    label = 'Code INSEE de la région du lieu de résidence'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        regions_list: list[str] = parameters(period).geopolitique.regions.liste
        regions = [
            (parameters(period).geopolitique.regions[region], TypesCodeInseeRegion[region])
            for region in regions_list
            ]

        regions_elig = [
            sum([startswith(depcom, str.encode(codes_insee)) for codes_insee in parametres_region.departements]) > 0
            for (parametres_region, _) in regions
            ]
        codes_insee_regions = [code_insee_region for (_, code_insee_region) in regions]

        return select(regions_elig, codes_insee_regions, default = TypesCodeInseeRegion.non_renseigne)


class charges_locatives(Variable):
    value_type = float
    entity = Menage
    set_input = set_input_divide_by_period
    label = 'Charges locatives'
    definition_period = MONTH


class proprietaire_proche_famille(Variable):
    value_type = bool
    entity = Famille
    label = 'Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class habite_chez_parents(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu habite chez ses parents"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class statut_occupation_logement(Variable):
    value_type = Enum
    possible_values = TypesStatutOccupationLogement  # defined in model/base.py
    entity = Menage
    default_value = TypesStatutOccupationLogement.non_renseigne
    label = "Statut d'occupation du logement"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class residence_ile_de_france(Variable):
    label = 'Le logement est situé dans la région Île-de-France'
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, str.encode(departement_idf)) for departement_idf in parameters(period).geopolitique.regions.ile_de_france.departements])  # TOOPTIMIZE: string encoding into bytes array should be done at load time


class residence_dom(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period):
        residence_guadeloupe = menage('residence_guadeloupe', period)
        residence_martinique = menage('residence_martinique', period)
        residence_guyane = menage('residence_guyane', period)
        residence_reunion = menage('residence_reunion', period)
        residence_mayotte = menage('residence_mayotte', period)

        return residence_guadeloupe + residence_martinique + residence_reunion + residence_guyane + residence_mayotte


class residence_guadeloupe(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'971')


class residence_martinique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'972')


class residence_guyane(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'973')


class residence_reunion(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'974')


class residence_saint_pierre_et_miquelon(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'975')


class residence_mayotte(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'976')


class residence_saint_bartelemy(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'977')


class residence_saint_martin(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return startswith(depcom, b'978')


class TypesLieuResidence(Enum):
    non_renseigne = 'Non renseigné'
    metropole = 'Métropole'
    guadeloupe = 'Guadeloupe'
    martinique = 'Martinique'
    guyane = 'Guyane'
    la_reunion = 'La réunion'
    saint_pierre_et_miquelon = 'Saint Pierre et Miquelon'
    mayotte = 'Mayotte'
    saint_bartelemy = 'Saint Bartelemy'
    saint_martin = 'Saint Martin'


class residence(Variable):
    value_type = Enum
    possible_values = TypesLieuResidence
    default_value = TypesLieuResidence.non_renseigne
    entity = Menage
    label = 'Zone de résidence'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        return select(
            [
                menage('residence_guadeloupe', period),
                menage('residence_martinique', period),
                menage('residence_guyane', period),
                menage('residence_reunion', period),
                menage('residence_saint_pierre_et_miquelon', period),
                menage('residence_mayotte', period),
                menage('residence_saint_bartelemy', period),
                menage('residence_saint_martin', period)
                ],
            [
                TypesLieuResidence.guadeloupe,
                TypesLieuResidence.martinique,
                TypesLieuResidence.guyane,
                TypesLieuResidence.la_reunion,
                TypesLieuResidence.saint_pierre_et_miquelon,
                TypesLieuResidence.mayotte,
                TypesLieuResidence.saint_bartelemy,
                TypesLieuResidence.saint_martin
                ],
            default=TypesLieuResidence.metropole
            )
