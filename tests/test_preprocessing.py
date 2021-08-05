"""Teste les cotisations par catégorie de salarié produites à l'issue de l'étape preprocessing."""

from collections import OrderedDict
from .cache import tax_benefit_system


cotisations_salarie_by_name = {
    "agff": {},
    "agirc_arrco": {},
    "agirc": {},
    "apec": {},
    "arrco": {},
    "assedic": {},
    "ceg": {},
    "cet": {
        "final_null_date": "2019-01-01"

        },
    "cet2019": {},
    "forfait_annuel": {},
    "maladie_alsace_moselle": {},
    "maladie": {},
    "vieillesse_deplafonnee": {},
    "vieillesse": {},
    }


cotisations_salarie_by_categorie_salarie = {
    "prive_cadre": [
        "agff",
        "agirc_arrco",
        "agirc",
        "apec",
        "arrco",
        "assedic",
        "ceg",
        "cet",
        "cet2019",
        "forfait_annuel",
        "maladie_alsace_moselle",
        "maladie",
        "vieillesse_deplafonnee",
        "vieillesse",
        ],
    }


def test_preprocessing():
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

    categorie_salaries = [
        "prive_cadre",
        ]
    for categorie_salarie in categorie_salaries:
        test = parameters.cotsoc.cotisations_salarie.children["prive_cadre"].children.keys()
        target = cotisations_salarie_by_categorie_salarie[categorie_salarie]
        assert set(test) == set(target), "Les barèmes de cotisations salarié {} ne sont pas les bons".format(
            categorie_salarie)

    cotisations_salaries = set(sum(
        (cotisations_salarie_by_categorie_salarie[categorie_salarie] for categorie_salarie in categorie_salaries),
        [],
        ))

    for cotisation_salarie in sorted(cotisations_salaries):
        bareme = parameters.cotsoc.cotisations_salarie.children["prive_cadre"].children[cotisation_salarie]

        final_null_date = cotisations_salarie_by_name[cotisation_salarie].get("final_null_date")
        if final_null_date:
            thresholds = [
                dict(
                    (parameter_at_instant.instant_str, parameter_at_instant.value)
                    for parameter_at_instant in bracket.threshold.values_list
                    )
                for bracket in bareme.brackets
                ]
            final_thresholds_by_instant_str = OrderedDict(sorted(threshold.items(), reverse = True)[0] for threshold in thresholds)
            assert all([final_threshold is None for final_threshold in final_thresholds_by_instant_str.values()]), "Barème salarié {} ne s'éteint pas (il devrait en {})".format(
                cotisation_salarie,
                final_null_date,
                )
            assert max(final_thresholds_by_instant_str.keys()) == final_null_date, "Barème salarié {} ne s'éteint pas en {}".format(
                cotisation_salarie,
                final_null_date,
                )
