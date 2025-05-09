from openfisca_france.model.base import *
import openfisca_france
import csv
import codecs
import importlib
import numpy as np


def bail_reel_solidaire_zones_elligibles():
    with importlib.resources.files(
        openfisca_france.__name__).joinpath(
        'assets/zonage-communes/zonage-abc-juillet-2024.csv'
    ).open('rb') as csv_file:
        utf8_reader = codecs.getreader('utf-8')
        csv_reader = csv.DictReader(utf8_reader(csv_file), delimiter=';')
        return {
            row['CODGEO']: row['Zone en vigueur depuis le 5 juillet 2024']
            for row in csv_reader
        }


class bail_reel_solidaire_zones_menage(Variable):
    value_type = str
    label = 'Zone du ménage pour le Bail Réel Solidaire'
    entity = Menage
    definition_period = MONTH

    def formula(menage, period):
        depcom = menage('depcom', period)
        return np.fromiter(
            (bail_reel_solidaire_zones_elligibles().get(
                depcom_cell.decode('utf-8')) for depcom_cell in depcom),
            dtype='<U4'  # String length max for zones (A, Abis, B1, B2, C)
        )


class bail_reel_solidaire_plafond_total(Variable):
    value_type = float
    label = 'Plafond de ressources total du Bail Réel Solidaire'
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        params = parameters(period).prestations_sociales.bail_reel_solidaire
        zones_abc_eligibles = params.parametres_generaux.zones_abc_eligibles
        plafonds_par_zones = params.plafonds_par_zones
        zones_menage = menage('bail_reel_solidaire_zones_menage', period)
        nb_personnes = menage.nb_persons()
        nb_personnes_max = params.parametres_generaux.nombre_personnes_maximum

        def calcul_plafonds_zone(zone):
            plafond_zone = plafonds_par_zones[f'zone_{zone}']
            plafond_base = select(
                [nb_personnes == i if i < 6 else nb_personnes >=
                    i for i in range(1, 7)],
                [plafond_zone[f'nb_personnes_{i}'] for i in range(1, 7)]
            )
            plafond_supp = where(
                nb_personnes > nb_personnes_max,
                (nb_personnes - nb_personnes_max) *
                plafond_zone.nb_personnes_supplementaires,
                0
            )
            return plafond_base + plafond_supp

        return select(
            [zones_menage == zone for zone in zones_abc_eligibles],
            [calcul_plafonds_zone(zone) for zone in zones_abc_eligibles]
        )


class bail_reel_solidaire(Variable):
    value_type = bool
    label = 'Éligibilité au Bail Réel Solidaire'
    entity = Menage
    definition_period = MONTH
    reference = [
        'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000032918488',
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000437021'
    ]

    def formula(menage, period):
        plafond_total = menage('bail_reel_solidaire_plafond_total', period)
        zones_menage = menage('bail_reel_solidaire_zones_menage', period)
        rfr = menage.sum(menage.members.foyer_fiscal(
            'rfr', period.n_2), role=FoyerFiscal.DECLARANT_PRINCIPAL)
        return where(zones_menage is not None, rfr <= plafond_total, False)
