# -*- coding: utf-8 -*-

from __future__ import division

import datetime


from openfisca_core import periods

from openfisca_france.reforms import inversion_directe_salaires
from openfisca_france.model.base import CAT
from openfisca_france.tests.base import assert_near, tax_benefit_system


def check_inversion_directe_salaires(type_sal, year = 2014):
    period = periods.period("{}".format(year))
    single_entity_kwargs = dict(
        axes = [dict(count = 1 + 1, max = 12 * 4000, min = 12 * 500, name = 'salaire_de_base')],  # TODO: min = 0
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
    brut = simulation.get_holder('salaire_de_base').array
    smic_horaire = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
    smic_annuel = smic_horaire * 35 * 52
    brut = simulation.get_holder('salaire_de_base').array

    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        simulation.get_or_new_holder('contrat_de_travail').set_input(
            periods.period("{}-{}".format(year, month)), (brut < smic_annuel) * 1.)  # temps plein ou temps partiel
        simulation.get_or_new_holder('heures_remunerees_volume').set_input(
            periods.period("{}-{}".format(year, month)), ((brut / 12) // smic_horaire) * (brut < smic_annuel))

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
    # Salariés du privé
    if type_sal == 0:
        cat = 'prive_non_cadre'
    elif type_sal == 1:
        cat = 'prive_cadre'
    for cotisation_name, cotisation in cotisation_by_name.iteritems():
        print cotisation_name, cotisation
    for name, bareme in salarie[cat].iteritems():
        x = bareme.scale_tax_scales(plafond_securite_sociale_annuel)
        print name, bareme
        print x.calc(brut)

#            print 'prive_cadre'
#            for name, bareme in salarie['prive_cadre'].iteritems():
#                print name, bareme
#            prive_non_cadre = salarie['prive_non_cadre'].combine_tax_scales().scale_tax_scales(

    inversion_reform = inversion_directe_salaires.build_reform(tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)

    inverse_simulation.get_holder('salaire_de_base').delete_arrays()
    inverse_simulation.get_or_new_holder('salaire_imposable_pour_inversion').set_input(
        period, imposable.copy())

    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        inverse_simulation.get_or_new_holder('contrat_de_travail').set_input(
            periods.period("{}-{}".format(year, month)), (brut < smic_annuel) * 1.)  # temps plein ou partiel
        inverse_simulation.get_or_new_holder('heures_remunerees_volume').set_input(
            periods.period("{}-{}".format(year, month)), ((brut / 12) // smic_horaire) * (brut < smic_annuel))

#    for cotisation_name in cotisations_name:
#        assert_near(
#            inverse_simulation.calculate_add(cotisation_name),
#            cotisation_by_name[cotisation_name], absolute_error_margin = 1)

    new_brut = inverse_simulation.calculate('salaire_de_base')
    print type_sal
    assert_near(new_brut, brut, absolute_error_margin = 1)


def test_sal(year = 2014):
    for type_sal_category in ('prive_cadre', 'prive_non_cadre'):  # , 'public_titulaire_etat'):
        yield check_inversion_directe_salaires, CAT[type_sal_category], year


if __name__ == '__main__':
    import logging
    import sys
    for function, type_sal, year in test_sal():
        function(type_sal, year)

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
