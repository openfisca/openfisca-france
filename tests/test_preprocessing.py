'''Teste les cotisations par catégorie de salarié produites à l'issue de l'étape preprocessing.'''

from collections import OrderedDict

from openfisca_core.parameters.parameter_scale import ParameterScale
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import (
    cotisations_employeur_by_categorie_salarie,
    cotisations_salarie_by_categorie_salarie,
    )


from .cache import tax_benefit_system


cotisations_salarie_by_name = {
    'agff': {
        'start_non_null_date': '2001-04-01',
        'final_null_date': '2019-01-01',
        },
    'agirc_arrco': {
        'start_non_null_date': '2019-01-01',
        },
    'agirc': {
        'start_non_null_date': '1948-01-01',
        'final_null_date': '2019-01-01',
        },
    'apec': {
        'start_non_null_date': '1971-01-01',
        },
    'arrco': {
        'start_non_null_date': '1962-01-01',
        'final_null_date': '2019-01-01',
        },
    'asf': {
        'start_non_null_date': '1984-01-01',
        },
    'ceg': {
        'start_non_null_date': '2019-01-01',
        },
    'cet': {
        'start_non_null_date': '1997-01-01',
        'final_null_date': '2019-01-01',
        },
    'cet2019': {
        'start_non_null_date': '2019-01-01',
        },
    'chomage': {
        'start_non_null_date': '1959-01-01',
        'final_null_date': '2018-10-01',
        },
    'cnracl_s_ti': {
        'start_non_null_date': '1947-09-19',
        },
    'cnracl_s_nbi': {
        'start_non_null_date': '1947-09-19',
        },
    'excep_solidarite': {
        'start_non_null_date': '1982-11-01',
        'final_null_date': '2018-01-01',
        },
    'ircantec': {
        'start_non_null_date': '1971-01-01',
        },
    'maladie_alsace_moselle': {
        'start_non_null_date': '1946-07-01',
        },
    'maladie': {
        'start_non_null_date': '1967-10-01',
        'final_null_date': '2018-01-01',
        },
    'pension': {
        'start_non_null_date': '1925-01-01',
        },
    'rafp': {
        'start_non_null_date': '2005-01-01'
        },
    'vieillesse_deplafonnee': {
        'start_non_null_date': '2004-07-01'
        },
    'vieillesse_plafonnee': {
        'start_non_null_date': '1993-07-01',
        },
    }


def test_preprocessing():
    '''Tests the result of parameters preprocessing.'''
    parameters = tax_benefit_system.parameters
    assert set(parameters.cotsoc.cotisations_employeur.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        'public_titulaire_militaire',
        'public_titulaire_territoriale',
        ]), 'Les barèmes de cotisations employeur de certaines catégories de salariés sont manquants'

    assert set(parameters.cotsoc.cotisations_salarie.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        # 'public_titulaire_militaire',  FIXME Il y en a sûrement mais pas actuellement
        'public_titulaire_territoriale',
        ]), 'Les barèmes de cotisations salarié de certaines catégories instant_sde salariés sont manquants'

    categorie_salaries = [
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        'public_titulaire_territoriale',
        ]

    for categorie_salarie in categorie_salaries:
        test = parameters.cotsoc.cotisations_salarie.children[categorie_salarie].children.keys()
        target = cotisations_salarie_by_categorie_salarie[categorie_salarie]
        assert set(test) == set(target), 'Les barèmes de cotisations salarié {} ne sont pas les bons'.format(
            categorie_salarie)

        test = parameters.cotsoc.cotisations_employeur.children[categorie_salarie].children.keys()
        target = cotisations_employeur_by_categorie_salarie[categorie_salarie]
        assert set(test) == set(target), 'Les barèmes de cotisations employeur {} ne sont pas les bons'.format(
            categorie_salarie)

    for categorie_salarie in categorie_salaries:
        cotisations_salaries = set(cotisations_salarie_by_categorie_salarie[categorie_salarie])
        for cotisation_salarie in sorted(cotisations_salaries):
            bareme = parameters.cotsoc.cotisations_salarie.children[categorie_salarie].children[cotisation_salarie]

            assert isinstance(bareme, ParameterScale), f"{cotisation_salarie} entry's class is {type(bareme)} which is not a ParameterScale"

            final_null_date = cotisations_salarie_by_name[cotisation_salarie].get('final_null_date')
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

            start_non_null_date = cotisations_salarie_by_name[cotisation_salarie].get('start_non_null_date')
            if start_non_null_date:
                thresholds = [
                    dict(
                        (parameter_at_instant.instant_str, parameter_at_instant.value)
                        for parameter_at_instant in bracket.threshold.values_list
                        )
                    for bracket in bareme.brackets
                    ]
                start_thresholds_by_instant_str = OrderedDict(sorted(threshold.items())[0] for threshold in thresholds)
                assert all([start_threshold is not None for start_threshold in start_thresholds_by_instant_str.values()]), 'Barème salarié {} ne commence pas à la bonne date (il devrait en {})'.format(
                    cotisation_salarie,
                    start_non_null_date,
                    )
                assert min(start_thresholds_by_instant_str.keys()) == start_non_null_date, 'Barème salarié {} ne commence pas en {}'.format(
                    cotisation_salarie,
                    start_non_null_date,
                    )
