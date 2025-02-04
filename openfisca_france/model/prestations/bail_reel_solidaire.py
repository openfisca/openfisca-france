from openfisca_france.model.base import *
import os
import csv
import numpy as np


def load_zonage_file(period, parameters):
    chemin_fichier_zonage_abc = os.path.join(parameters(period).prestations_sociales.bail_reel_solidaire.parametres_generaux.fichier_zonage[0])

    if not os.path.exists(chemin_fichier_zonage_abc):
        return None

    with open(chemin_fichier_zonage_abc, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        return {row['CODGEO']: row['Zone en vigueur depuis le 5 juillet 2024'] for row in csv_reader}


def plafond_par_zone_et_composition(nb_personnes, plafonds_par_zones, zone):
    plafond_zone = plafonds_par_zones[f'zone_{zone}']

    tranches_composition = range(1, 7)
    conditions_nb_personnes = [
        nb_personnes == i if i < 6 else nb_personnes >= i
        for i in tranches_composition
        ]

    plafonds_revenus = [
        plafond_zone[f'nb_personnes_{i}']
        for i in tranches_composition
        ]

    return select(conditions_nb_personnes, plafonds_revenus)


def plafond_supplementaire_par_zone(nb_personnes, plafonds_par_zones, zone, nb_personnes_max):
    return where(
        nb_personnes > nb_personnes_max,
        (nb_personnes - nb_personnes_max) * plafonds_par_zones[f'zone_{zone}']['nb_personnes_supplementaires'],
        0
        )


class bail_reel_solidaire(Variable):
    entity = Menage
    value_type = bool
    reference = [
        'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000032918488',
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000437021'
        ]
    label = 'Bail réel solidaire'
    definition_period = MONTH

    def formula(menage, period, parameters):
        parametres = parameters(period).prestations_sociales.bail_reel_solidaire.parametres_generaux
        zones_abc_eligibles = parametres.zones_abc_eligibles
        nb_personnes_max = parametres.nombre_personnes_maximum

        zones_par_depcom = load_zonage_file(period, parameters)
        if not zones_par_depcom:
            return False

        nb_personnes = menage.nb_persons()
        depcom = menage('depcom', period.first_month)
        zones_menage = np.array([zones_par_depcom.get(d.decode('utf-8'), None) for d in depcom])

        plafonds_par_zones = parameters(period).prestations_sociales.bail_reel_solidaire.plafonds_par_zones

        plafond_revenu_base = select(
            [zones_menage == zone for zone in zones_abc_eligibles],
            [plafond_par_zone_et_composition(nb_personnes, plafonds_par_zones, zone) for zone in zones_abc_eligibles]
            )

        plafond_revenu_supplementaire = select(
            [zones_menage == zone for zone in zones_abc_eligibles],
            [plafond_supplementaire_par_zone(nb_personnes, plafonds_par_zones, zone, nb_personnes_max) for zone in zones_abc_eligibles]
            )

        rfr = menage.sum(menage.members.foyer_fiscal(
            'rfr', period.n_2), role=FoyerFiscal.DECLARANT_PRINCIPAL)

        return where(zones_menage is not None, rfr <= (plafond_revenu_base + plafond_revenu_supplementaire), False)
