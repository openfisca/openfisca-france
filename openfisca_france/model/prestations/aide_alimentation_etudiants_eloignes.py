from openfisca_core.model_api import Variable, select
from openfisca_france.entities import Individu
from openfisca_core.periods import MONTH


class aide_alimentation_etudiants_eloignes(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = 'Aide financière pour les étudiants éloignés des restaurants universitaires, avec des montants majorés pour les DROM.'
    reference = [
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000050660003',
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000050659996',
        ]

    def formula(individu, period, parameters):
        etudiant = individu('etudiant', period)
        boursier = individu('boursier', period)
        resident_drom = individu('localisation_DROM_aide_alimentation_etudiants_eloignes', period)

        non_boursier = ~boursier
        resident_hors_drom = ~resident_drom

        P = parameters(period).prestations_sociales.aide_alimentation_etudiants_eloignes
        montant_standard_boursier = P.montant_etudiant_standard_boursier
        montant_standard_non_boursier = P.montant_etudiant_standard_non_boursier
        montant_drom_boursier = P.montant_etudiant_drom_boursier
        montant_drom_non_boursier = P.montant_etudiant_drom_non_boursier

        conditions = [
            resident_drom & boursier,
            resident_drom & non_boursier,
            resident_hors_drom & boursier,
            resident_hors_drom & non_boursier,
            ]

        montants = [
            montant_drom_boursier,
            montant_drom_non_boursier,
            montant_standard_boursier,
            montant_standard_non_boursier,
            ]

        montant = select(conditions, montants, default=0)
        return etudiant * montant
