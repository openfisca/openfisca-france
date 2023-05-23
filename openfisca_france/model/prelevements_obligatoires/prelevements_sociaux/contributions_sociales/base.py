from openfisca_core import periods, populations
from openfisca_france.model.base import *


def montant_csg_crds(base_avec_abattement = None, base_sans_abattement = None, indicatrice_taux_plein = None,
        indicatrice_taux_reduit = None, law_node = None, plafond_securite_sociale = None):
    assert law_node is not None
    assert plafond_securite_sociale is not None
    if base_sans_abattement is None:
        base_sans_abattement = 0
    if base_avec_abattement is None:
        base = base_sans_abattement
    else:
        base = base_avec_abattement - law_node.abattement.calc(
            base_avec_abattement,
            factor = plafond_securite_sociale,
            round_base_decimals = 2,
            ) + base_sans_abattement
    if indicatrice_taux_plein is None and indicatrice_taux_reduit is None:
        return -law_node.taux * base
    else:
        return - (law_node.taux_plein * indicatrice_taux_plein + law_node.taux_reduit * indicatrice_taux_reduit) * base


def condition_csg_crds_non_residents(individu_or_foyerfiscal, period):
    '''
    Depuis le 1er janvier 2019, les personnes affiliées à un régime obligatoire
    de sécurité sociale autre que français au sein d'un pays de l'EEE (Union
    européenne, Islande, Norvège, Liechtenstein) ou de la Suisse sont exonérées
    de CSG et de CRDS.
    Ces revenus demeurent soumis à un prélèvement de solidarité au taux de 7,5%.
    Reference: https://www.impots.gouv.fr/international-particulier/questions/je-suis-non-resident-suis-je-redevable-des-contributions

    Return:
    * True: la CSG et la CRDS sont exigibles
    * False: la CSG et la CRDS sont exonerees
    '''

    if isinstance(individu_or_foyerfiscal, populations.group_population.GroupPopulation):
        # FoyerFiscal
        rehf = individu_or_foyerfiscal.any(individu_or_foyerfiscal.members('resident_eee_hors_france', period))
    else:
        # Individu
        rehf = individu_or_foyerfiscal('resident_eee_hors_france', period)

    exonere = (
        (periods.period('2019-01-01').start <= period.start)
        * rehf
        )
    return not_(exonere)
