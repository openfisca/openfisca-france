"""Teste les cotisations par catégorie de salarié produites à l'issue de l'étape preprocessing."""

import datetime
from openfisca_france.model.revenus.activite.salarie import categorie_salarie
from .cache import tax_benefit_system

import pytest


years = range(2006, 2020)


# @pytest.mark.parametrize("year", years)
def test_preprocessing(year = None):
    """Basic test for a specific year.

    Args:
        year (int): Year.
    """
    parameters = tax_benefit_system.parameters

    assert set(parameters.cotsoc.cotisations_employeur.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        'public_titulaire_militaire',
        'public_titulaire_territoriale',
        ]), "Les barèmes de cotisations employeur de certaines catégories de salariés sont manquants"

    assert set(parameters.cotsoc.cotisations_salarie.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        # 'public_titulaire_militaire',  FIXME Il y en a sûrement mais pas actuellement
        'public_titulaire_territoriale',
        ]), "Les barèmes de cotisations salarié de certaines catégories de salariés sont manquants"

    # categorie_salarie = "prive_cadre"
    # print(parameters.cotsoc.cotisations_salarie.children["prive_cadre"].children.keys())


if __name__ == "__main__":
    test_basics()