from openfisca_france.model.base import *
import os
import csv
import numpy as np

ZONAGE_ABC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../../assets/zonage-communes/zonage-abc-juillet-2024.csv'
    )
ZONES_ABC = [
    'A', 'Abis', 'B1', 'B2', 'C'
    ]
NB_PERSONNES_MAX = 6


def preload_zone_abc():
    if not os.path.exists(ZONAGE_ABC):
        return None

    with open(ZONAGE_ABC, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return {row['CODGEO']: row['Zone en vigueur depuis le 5 juillet 2024'] for row in reader}


class bail_reel_solidaire(Variable):
    entity = Menage
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000032918488'
    label = 'Bail réel solidaire'
    definition_period = MONTH

    def formula(menage, period, parameters):
        def plafond_par_zone_et_composition(nb_personnes, plafonds_par_zones, zone):
            plafond_zone = plafonds_par_zones[f'zone_{zone}']
            conditions = [
                nb_personnes == 1,
                nb_personnes == 2,
                nb_personnes == 3,
                nb_personnes == 4,
                nb_personnes == 5,
                nb_personnes >= 6
                ]
            plafonds = [
                plafond_zone['nb_personnes_1'],
                plafond_zone['nb_personnes_2'],
                plafond_zone['nb_personnes_3'],
                plafond_zone['nb_personnes_4'],
                plafond_zone['nb_personnes_5'],
                plafond_zone['nb_personnes_6']
                ]
            return select(conditions, plafonds)

        def plafond_supplementaire_par_zone(nb_personnes, plafonds_par_zones, zone):
            return where(nb_personnes > NB_PERSONNES_MAX,
                         (nb_personnes - NB_PERSONNES_MAX) * plafonds_par_zones[f'zone_{zone}']['nb_personnes_supplementaires'], 0)

        zones_par_depcom = preload_zone_abc()
        if not zones_par_depcom:
            return False

        nb_personnes = menage.nb_persons()
        depcom = menage('depcom', period.first_month)
        zones = np.array([zones_par_depcom.get(
            d.decode('utf-8'), None) for d in depcom])

        plafonds_par_zones = parameters(
            period).prestations_sociales.bail_reel_solidaire.plafonds_par_zones

        plafond_base = select(
            [zones == zone for zone in ZONES_ABC],
            [plafond_par_zone_et_composition(
                nb_personnes, plafonds_par_zones, zone) for zone in ZONES_ABC]
            )

        plafond_supp = select(
            [zones == zone for zone in ZONES_ABC],
            [plafond_supplementaire_par_zone(
                nb_personnes, plafonds_par_zones, zone) for zone in ZONES_ABC]
            )

        rfr = menage.sum(menage.members.foyer_fiscal(
            'rfr', period.n_2), role=FoyerFiscal.DECLARANT_PRINCIPAL)

        return where(zones is not None, rfr <= (plafond_base + plafond_supp), False)
