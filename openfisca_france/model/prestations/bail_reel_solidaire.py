from openfisca_france.model.base import *
import os
import csv


ZONAGE_ABC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../../assets/zonage-communes/zonage-abc-juillet-2024.csv'
    )


def preload_zone_abc():
    if not os.path.exists(ZONAGE_ABC):
        return None
    with open(ZONAGE_ABC, 'r', encoding='latin1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return {
            row['CODGEO']: row['Zone en vigueur depuis le 5 juillet 2024']
            for row in reader
            }


class bail_reel_solidaire(Variable):
    entity = Menage
    value_type = float
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000032918488'
    label = 'Bail réel solidaire'
    definition_period = MONTH

    def formula(menage, period, parameters):
        nb_personnes = menage.nb_persons()[0]
        _zone_abc_by_depcom = preload_zone_abc()

        if _zone_abc_by_depcom is None:
            return False

        depcom = menage('depcom', period.first_month)
        zone = _zone_abc_by_depcom.get(depcom[0].decode('utf-8'))

        if zone is None:
            return False  # Si le code INSEE n'est pas trouvé, le ménage n'est pas éligible

        # Accès aux paramètres selon la zone
        params = parameters(period).prestations_sociales.bail_reel_solidaire.plafonds_par_zones[f'zone_{zone}']
        # print(params)

        # Calcul des ressources (revenu fiscal de référence)
        rfr = menage.sum(menage.members.foyer_fiscal('rfr', period.n_2), role = FoyerFiscal.DECLARANT_PRINCIPAL)[0]

        # print("RFR: ", rfr)

        # Détermination du plafond selon le nombre de personnes
        if nb_personnes > 6:
            plafond_base = params.nb_personnes_6
            personnes_supp = nb_personnes - 6
            plafond = plafond_base + (personnes_supp * params.nb_personnes_supplementaires)
        else:
            plafond = getattr(params, f'nb_personnes_{nb_personnes}')

        return rfr <= plafond
