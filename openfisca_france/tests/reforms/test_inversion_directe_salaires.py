# -*- coding: utf-8 -*-

from __future__ import division

import datetime


from openfisca_core import periods, taxscales

from openfisca_france.reforms import inversion_directe_salaires
from openfisca_france.model.base import CAT
from openfisca_france.tests.base import assert_near, tax_benefit_system

TAUX_DE_PRIME = inversion_directe_salaires.TAUX_DE_PRIME


def check_inversion_directe_salaires(type_sal, year = 2014):
    period = periods.period("{}".format(year))
    min_brut = 12 * 500
    max_brut = 12 * 4000
    count = 1 + 1
    if type_sal <= 1:
        axes = [dict(count = count, max = max_brut, min = min_brut, name = 'salaire_de_base')]
    else:
        axes = [
            [
                dict(count = count, max = max_brut, min = min_brut, name = 'traitement_indiciaire_brut'),
                dict(count = count, max = TAUX_DE_PRIME * max_brut + .01, min = TAUX_DE_PRIME * min_brut,
                     name = 'primes_fonction_publique'),
            ]
        ]
    single_entity_kwargs = dict(
        axes = axes,  # TODO: min = 0
        period = period,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            type_sal = type_sal,
            cotisation_sociale_mode_recouvrement = 1,
            ),
        )
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        **single_entity_kwargs
        ).new_simulation(debug = False)

    smic_horaire = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
    smic_annuel = smic_horaire * 35 * 52
    try:
        salaire_de_base = simulation.get_holder('salaire_de_base').array
    except KeyError:
        salaire_de_base = None
        pass
    try:
        traitement_indiciaire_brut = simulation.get_holder('traitement_indiciaire_brut').array
        primes_fonction_publique = simulation.get_holder('primes_fonction_publique').array
    except KeyError:
        traitement_indiciaire_brut = None
        primes_fonction_publique = None
        pass

    if type_sal <= 1:
        for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            simulation.get_or_new_holder('contrat_de_travail').set_input(
                periods.period("{}-{}".format(year, month)), (salaire_de_base < smic_annuel) * 1.)  # temps plein ou temps partiel
            simulation.get_or_new_holder('heures_remunerees_volume').set_input(
                periods.period("{}-{}".format(year, month)), ((salaire_de_base / 12) // smic_horaire) * (salaire_de_base < smic_annuel))

    imposable = simulation.calculate_add('salaire_imposable')
    print imposable
    cotisations_name = [
        'mmid_salarie',
        'chomage_salarie',
        'vieillesse_plafonnee_salarie',
        'vieillesse_deplafonnee_salarie',
        'arrco_salarie',
        'agff_salarie',
        ]
    cotisation_by_name = dict()
    for cotisation_name in cotisations_name:
        cotisation_by_name[cotisation_name] = simulation.calculate_add(cotisation_name, period = period)

    salarie = simulation.legislation_at(period.start).cotsoc.cotisations_salarie
    plafond_securite_sociale_annuel = simulation.legislation_at(period.start).cotsoc.gen.plafond_securite_sociale * 12
    if type_sal == 0:
        cat = 'prive_non_cadre'
    elif type_sal == 1:
        cat = 'prive_cadre'
    elif type_sal == 2:
        cat = 'public_titulaire_etat'
    for cotisation_name, cotisation in cotisation_by_name.iteritems():
        print cotisation_name, cotisation
    for name, bareme in salarie[cat].iteritems():
        if not isinstance(bareme, taxscales.AbstractTaxScale):
            continue
        x = bareme.scale_tax_scales(plafond_securite_sociale_annuel)
        print name, bareme
        print x.calc(salaire_de_base if salaire_de_base else traitement_indiciaire_brut)

    inversion_reform = inversion_directe_salaires.build_reform(tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)

    try:
        inverse_simulation.get_holder('salaire_de_base').delete_arrays()
    except KeyError:
        pass
    try:
        inverse_simulation.get_holder('traitement_indiciaire_brut').delete_arrays()
        inverse_simulation.get_holder('primes_fonction_publique').delete_arrays()
    except KeyError:
        pass

    inverse_simulation.get_or_new_holder('salaire_imposable_pour_inversion').set_input(
        period, imposable.copy())

    if type_sal <= 1:
        for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            inverse_simulation.get_or_new_holder('contrat_de_travail').set_input(
                periods.period("{}-{}".format(year, month)), (salaire_de_base < smic_annuel) * 1.)  # temps plein ou partiel
            inverse_simulation.get_or_new_holder('heures_remunerees_volume').set_input(
                periods.period("{}-{}".format(year, month)), ((salaire_de_base / 12) // smic_horaire) * (brut < smic_annuel))

    new_salaire_de_base = inverse_simulation.calculate('salaire_de_base')
    new_traitement_indiciaire_brut = inverse_simulation.calculate('traitement_indiciaire_brut')
    new_primes_fonction_publique = inverse_simulation.calculate('primes_fonction_publique')

    print type_sal
    if salaire_de_base is not None:
        assert_near(new_salaire_de_base, salaire_de_base, absolute_error_margin = 1)
    if traitement_indiciaire_brut is not None:
        assert_near(new_primes_fonction_publique, primes_fonction_publique, absolute_error_margin =  None, relative_error_margin = .05)
        assert_near(new_traitement_indiciaire_brut, traitement_indiciaire_brut, absolute_error_margin =  None, relative_error_margin = .05)


def test_sal(year = 2014):
    for type_sal_category in ('public_titulaire_etat', ): # ('prive_cadre', 'prive_non_cadre'):
        yield check_inversion_directe_salaires, CAT[type_sal_category], year


if __name__ == '__main__':
    import logging
    import sys
    for function, type_sal, year in test_sal():
        function(type_sal, year)

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
