# -*- coding: utf-8 -*-

import itertools
import uuid
import datetime

from openfisca_core import conv
import openfisca_core.simulations

from .entities import Familles, Menages, Individus, FoyersFiscaux


def N_(message):
    return message


class Simulation(openfisca_core.simulations.AbstractSimulation):
    def __init__(self, tbs, test_case):
        self.tax_benefit_system = tbs

        assert 'parent1' in test_case
        parent1 = test_case['parent1']

        parent2 = test_case['parent2'] if 'parent2' in test_case else None
        axes = test_case['axes'] if 'axes' in test_case else None
        period = test_case['period'] if 'period' in test_case else None

        enfants = test_case['enfants'] if 'enfants' in test_case else []
        famille = test_case['famille'].copy() if 'famille' in test_case else {}
        foyer_fiscal = test_case['foyer_fiscal'].copy() if 'foyer_fiscal' in test_case else {}
        menage = test_case['menage'].copy() if 'menage' in test_case else {}

        individus = []
        for index, individu in enumerate([parent1, parent2] + (enfants or [])):
            if individu is None:
                continue
            ident = individu.get('id')
            if ident is None:
                individu = individu.copy()
                individu['id'] = ident = 'ind{}'.format(index)
            individus.append(individu)
            if index <= 1:
                famille.setdefault('parents', []).append(ident)
                foyer_fiscal.setdefault('declarants', []).append(ident)
                if index == 0:
                    menage['personne_de_reference'] = ident
                else:
                    menage['conjoint'] = ident
            else:
                famille.setdefault('enfants', []).append(ident)
                foyer_fiscal.setdefault('personnes_a_charge', []).append(ident)
                menage.setdefault('enfants', []).append(ident)

        refined_dict = dict(
            axes=axes,
            period=period,
            test_case=dict(
                familles=[famille],
                foyers_fiscaux=[foyer_fiscal],
                individus=individus,
                menages=[menage],
                ),
            )

        conv.check(self.make_json_or_python_to_attributes())(refined_dict)

        self.instantiate_variables()

    def make_json_or_python_to_test_case(self, period=None, repair=False):
        assert period is not None

        def json_or_python_to_test_case(value, state=None):
            if value is None:
                return value, None
            if state is None:
                state = conv.default_state

            variable_class_by_name = self.tax_benefit_system.variable_class_by_name

            # First validation and conversion step
            test_case, error = conv.pipe(
                conv.test_isinstance(dict),
                conv.struct(
                    dict(
                        familles=conv.pipe(
                            conv.make_item_to_singleton(),
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.test_isinstance(dict),
                                drop_none_items=True,
                                ),
                            conv.function(openfisca_core.simulations.set_entities_json_id),
                            conv.uniform_sequence(
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            enfants=conv.pipe(
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items=True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            id=conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            parents=conv.pipe(
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items=True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            ).iteritems(),
                                        (
                                            (variable_class.__name__, variable_class.json_to_python())
                                            for variable_class in variable_class_by_name.itervalues()
                                            if variable_class.entity is Familles and hasattr(variable_class, 'column_type')
                                            ),
                                        )),
                                    drop_none_values=True,
                                    ),
                                drop_none_items=True,
                                ),
                            conv.default([]),
                            ),
                        foyers_fiscaux=conv.pipe(
                            conv.make_item_to_singleton(),
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.test_isinstance(dict),
                                drop_none_items=True,
                                ),
                            conv.function(openfisca_core.simulations.set_entities_json_id),
                            conv.uniform_sequence(
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            declarants=conv.pipe(
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items=True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            id=conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            personnes_a_charge=conv.pipe(
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items=True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            ).iteritems(),
                                        (
                                            (variable_class.__name__, variable_class.json_to_python())
                                            for variable_class in variable_class_by_name.itervalues()
                                            if variable_class.entity is FoyersFiscaux and hasattr(variable_class, 'column_type')
                                            ),
                                        )),
                                    drop_none_values=True,
                                    ),
                                drop_none_items=True,
                                ),
                            conv.default([]),
                            ),
                        individus=conv.pipe(
                            conv.make_item_to_singleton(),
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.test_isinstance(dict),
                                drop_none_items=True,
                                ),
                            conv.function(openfisca_core.simulations.set_entities_json_id),
                            conv.uniform_sequence(
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            id=conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            ).iteritems(),
                                        (
                                            (variable_class.__name__, variable_class.json_to_python())
                                            for variable_class in variable_class_by_name.itervalues()
                                            if (variable_class.entity is Individus and
                                                hasattr(variable_class, 'column_type') and
                                                variable_class.__name__ not in (
                                                'idfam', 'idfoy', 'idmen', 'quifam', 'quifoy', 'quimen'))
                                            ),
                                        )),
                                    drop_none_values=True,
                                    ),
                                drop_none_items=True,
                                ),
                            conv.empty_to_none,
                            conv.not_none,
                            ),
                        menages=conv.pipe(
                            conv.make_item_to_singleton(),
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.test_isinstance(dict),
                                drop_none_items=True,
                                ),
                            conv.function(openfisca_core.simulations.set_entities_json_id),
                            conv.uniform_sequence(
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            autres=conv.pipe(
                                                # personnes ayant un lien autre avec la personne de référence
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            # conjoint de la personne de référence
                                            conjoint=conv.test_isinstance((basestring, int)),
                                            enfants=conv.pipe(
                                                # enfants de la personne de référence ou de son conjoint
                                                conv.make_item_to_singleton(),
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items=True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            id=conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            personne_de_reference=conv.test_isinstance((basestring, int)),
                                            ).iteritems(),
                                        (
                                            (variable_class.__name__, variable_class.json_to_python())
                                            for variable_class in variable_class_by_name.itervalues()
                                            if variable_class.entity is Menages and hasattr(variable_class, 'column_type')
                                            ),
                                        )),
                                    drop_none_values=True,
                                    ),
                                drop_none_items=True,
                                ),
                            conv.default([]),
                            ),
                        ),
                    ),
                )(value, state=state)
            if error is not None:
                return test_case, error

            # Second validation step
            familles_individus_id = [individu['id'] for individu in test_case['individus']]
            foyers_fiscaux_individus_id = [individu['id'] for individu in test_case['individus']]
            menages_individus_id = [individu['id'] for individu in test_case['individus']]
            test_case, error = conv.struct(
                dict(
                    familles=conv.uniform_sequence(
                        conv.struct(
                            dict(
                                enfants=conv.uniform_sequence(conv.test_in_pop(familles_individus_id)),
                                parents=conv.uniform_sequence(conv.test_in_pop(familles_individus_id)),
                                ),
                            default=conv.noop,
                            ),
                        ),
                    foyers_fiscaux=conv.uniform_sequence(
                        conv.struct(
                            dict(
                                declarants=conv.uniform_sequence(conv.test_in_pop(foyers_fiscaux_individus_id)),
                                personnes_a_charge=conv.uniform_sequence(conv.test_in_pop(
                                    foyers_fiscaux_individus_id)),
                                ),
                            default=conv.noop,
                            ),
                        ),
                    menages=conv.uniform_sequence(
                        conv.struct(
                            dict(
                                autres=conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                                conjoint=conv.test_in_pop(menages_individus_id),
                                enfants=conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                                personne_de_reference=conv.test_in_pop(menages_individus_id),
                                ),
                            default=conv.noop,
                            ),
                        ),
                    ),
                default=conv.noop,
                )(test_case, state=state)

            individu_by_id = {
                individu['id']: individu
                for individu in test_case['individus']
                }

            if repair:
                # Affecte à une famille chaque individu qui n'appartient à aucune d'entre elles.
                new_famille = dict(
                    enfants=[],
                    parents=[],
                    )
                new_famille_id = None
                for individu_id in familles_individus_id[:]:
                    # Tente d'affecter l'individu à une famille d'après son foyer fiscal.
                    foyer_fiscal, foyer_fiscal_role = find_foyer_fiscal_and_role(test_case, individu_id)
                    if foyer_fiscal_role == u'declarants' and len(foyer_fiscal[u'declarants']) == 2:
                        for declarant_id in foyer_fiscal[u'declarants']:
                            if declarant_id != individu_id:
                                famille, other_role = find_famille_and_role(test_case, declarant_id)
                                if other_role == u'parents' and len(famille[u'parents']) == 1:
                                    # Quand l'individu n'est pas encore dans une famille, mais qu'il est déclarant
                                    # dans un foyer fiscal, qu'il y a un autre déclarant dans ce même foyer fiscal
                                    # et que cet autre déclarant est seul parent dans sa famille, alors ajoute
                                    # l'individu comme autre parent de cette famille.
                                    famille[u'parents'].append(individu_id)
                                    familles_individus_id.remove(individu_id)
                                break
                    elif foyer_fiscal_role == u'personnes_a_charge' and foyer_fiscal[u'declarants']:
                        for declarant_id in foyer_fiscal[u'declarants']:
                            famille, other_role = find_famille_and_role(test_case, declarant_id)
                            if other_role == u'parents':
                                # Quand l'individu n'est pas encore dans une famille, mais qu'il est personne à charge
                                # dans un foyer fiscal, qu'il y a un déclarant dans ce foyer fiscal et que ce déclarant
                                # est parent dans sa famille, alors ajoute l'individu comme enfant de cette famille.
                                famille[u'enfants'].append(individu_id)
                                familles_individus_id.remove(individu_id)
                            break

                    if individu_id in familles_individus_id:
                        # L'individu n'est toujours pas affecté à une famille.
                        # Tente d'affecter l'individu à une famille d'après son ménage.
                        menage, menage_role = find_menage_and_role(test_case, individu_id)
                        if menage_role == u'personne_de_reference':
                            conjoint_id = menage[u'conjoint']
                            if conjoint_id is not None:
                                famille, other_role = find_famille_and_role(test_case, conjoint_id)
                                if other_role == u'parents' and len(famille[u'parents']) == 1:
                                    # Quand l'individu n'est pas encore dans une famille, mais qu'il est personne de
                                    # référence dans un ménage, qu'il y a un conjoint dans ce ménage et que ce
                                    # conjoint est seul parent dans sa famille, alors ajoute l'individu comme autre
                                    # parent de cette famille.
                                    famille[u'parents'].append(individu_id)
                                    familles_individus_id.remove(individu_id)
                        elif menage_role == u'conjoint':
                            personne_de_reference_id = menage[u'personne_de_reference']
                            if personne_de_reference_id is not None:
                                famille, other_role = find_famille_and_role(test_case,
                                    personne_de_reference_id)
                                if other_role == u'parents' and len(famille[u'parents']) == 1:
                                    # Quand l'individu n'est pas encore dans une famille, mais qu'il est conjoint
                                    # dans un ménage, qu'il y a une personne de référence dans ce ménage et que
                                    # cette personne est seul parent dans une famille, alors ajoute l'individu comme
                                    # autre parent de cette famille.
                                    famille[u'parents'].append(individu_id)
                                    familles_individus_id.remove(individu_id)
                        elif menage_role == u'enfants' and (menage['personne_de_reference'] is not None
                                or menage[u'conjoint'] is not None):
                            for other_id in (menage['personne_de_reference'], menage[u'conjoint']):
                                if other_id is None:
                                    continue
                                famille, other_role = find_famille_and_role(test_case, other_id)
                                if other_role == u'parents':
                                    # Quand l'individu n'est pas encore dans une famille, mais qu'il est enfant dans un
                                    # ménage, qu'il y a une personne à charge ou un conjoint dans ce ménage et que
                                    # celui-ci est parent dans une famille, alors ajoute l'individu comme enfant de
                                    # cette famille.
                                    famille[u'enfants'].append(individu_id)
                                    familles_individus_id.remove(individu_id)
                                break

                    if individu_id in familles_individus_id:
                        # L'individu n'est toujours pas affecté à une famille.
                        individu = individu_by_id[individu_id]
                        age = find_age(individu, period.start.date)
                        if len(new_famille[u'parents']) < 2 and (age is None or age >= 18):
                            new_famille[u'parents'].append(individu_id)
                        else:
                            new_famille[u'enfants'].append(individu_id)
                        if new_famille_id is None:
                            new_famille[u'id'] = new_famille_id = unicode(uuid.uuid4())
                            test_case[u'familles'].append(new_famille)
                        familles_individus_id.remove(individu_id)

                # Affecte à un foyer fiscal chaque individu qui n'appartient à aucun d'entre eux.
                new_foyer_fiscal = dict(
                    declarants=[],
                    personnes_a_charge=[],
                    )
                new_foyer_fiscal_id = None
                for individu_id in foyers_fiscaux_individus_id[:]:
                    # Tente d'affecter l'individu à un foyer fiscal d'après sa famille.
                    famille, famille_role = find_famille_and_role(test_case, individu_id)
                    if famille_role == u'parents' and len(famille[u'parents']) == 2:
                        for parent_id in famille[u'parents']:
                            if parent_id != individu_id:
                                foyer_fiscal, other_role = find_foyer_fiscal_and_role(test_case, parent_id)
                                if other_role == u'declarants' and len(foyer_fiscal[u'declarants']) == 1:
                                    # Quand l'individu n'est pas encore dans un foyer fiscal, mais qu'il est parent
                                    # dans une famille, qu'il y a un autre parent dans cette famille et que cet autre
                                    # parent est seul déclarant dans son foyer fiscal, alors ajoute l'individu comme
                                    # autre déclarant de ce foyer fiscal.
                                    foyer_fiscal[u'declarants'].append(individu_id)
                                    foyers_fiscaux_individus_id.remove(individu_id)
                                break
                    elif famille_role == u'enfants' and famille[u'parents']:
                        for parent_id in famille[u'parents']:
                            foyer_fiscal, other_role = find_foyer_fiscal_and_role(test_case, parent_id)
                            if other_role == u'declarants':
                                # Quand l'individu n'est pas encore dans un foyer fiscal, mais qu'il est enfant dans une
                                # famille, qu'il y a un parent dans cette famille et que ce parent est déclarant dans
                                # son foyer fiscal, alors ajoute l'individu comme personne à charge de ce foyer fiscal.
                                foyer_fiscal[u'personnes_a_charge'].append(individu_id)
                                foyers_fiscaux_individus_id.remove(individu_id)
                                break

                    if individu_id in foyers_fiscaux_individus_id:
                        # L'individu n'est toujours pas affecté à un foyer fiscal.
                        # Tente d'affecter l'individu à un foyer fiscal d'après son ménage.
                        menage, menage_role = find_menage_and_role(test_case, individu_id)
                        if menage_role == u'personne_de_reference':
                            conjoint_id = menage[u'conjoint']
                            if conjoint_id is not None:
                                foyer_fiscal, other_role = find_foyer_fiscal_and_role(test_case, conjoint_id)
                                if other_role == u'declarants' and len(foyer_fiscal[u'declarants']) == 1:
                                    # Quand l'individu n'est pas encore dans un foyer fiscal, mais qu'il est personne de
                                    # référence dans un ménage, qu'il y a un conjoint dans ce ménage et que ce
                                    # conjoint est seul déclarant dans un foyer fiscal, alors ajoute l'individu comme
                                    # autre déclarant de ce foyer fiscal.
                                    foyer_fiscal[u'declarants'].append(individu_id)
                                    foyers_fiscaux_individus_id.remove(individu_id)
                        elif menage_role == u'conjoint':
                            personne_de_reference_id = menage[u'personne_de_reference']
                            if personne_de_reference_id is not None:
                                foyer_fiscal, other_role = find_foyer_fiscal_and_role(test_case,
                                    personne_de_reference_id)
                                if other_role == u'declarants' and len(foyer_fiscal[u'declarants']) == 1:
                                    # Quand l'individu n'est pas encore dans un foyer fiscal, mais qu'il est conjoint
                                    # dans un ménage, qu'il y a une personne de référence dans ce ménage et que
                                    # cette personne est seul déclarant dans un foyer fiscal, alors ajoute l'individu
                                    # comme autre déclarant de ce foyer fiscal.
                                    foyer_fiscal[u'declarants'].append(individu_id)
                                    foyers_fiscaux_individus_id.remove(individu_id)
                        elif menage_role == u'enfants' and (menage['personne_de_reference'] is not None
                                or menage[u'conjoint'] is not None):
                            for other_id in (menage['personne_de_reference'], menage[u'conjoint']):
                                if other_id is None:
                                    continue
                                foyer_fiscal, other_role = find_foyer_fiscal_and_role(test_case, other_id)
                                if other_role == u'declarants':
                                    # Quand l'individu n'est pas encore dans un foyer fiscal, mais qu'il est enfant dans
                                    # un ménage, qu'il y a une personne à charge ou un conjoint dans ce ménage et que
                                    # celui-ci est déclarant dans un foyer fiscal, alors ajoute l'individu comme
                                    # personne à charge de ce foyer fiscal.
                                    foyer_fiscal[u'declarants'].append(individu_id)
                                    foyers_fiscaux_individus_id.remove(individu_id)
                                    break

                    if individu_id in foyers_fiscaux_individus_id:
                        # L'individu n'est toujours pas affecté à un foyer fiscal.
                        individu = individu_by_id[individu_id]
                        age = find_age(individu, period.start.date)
                        if len(new_foyer_fiscal[u'declarants']) < 2 and (age is None or age >= 18):
                            new_foyer_fiscal[u'declarants'].append(individu_id)
                        else:
                            new_foyer_fiscal[u'personnes_a_charge'].append(individu_id)
                        if new_foyer_fiscal_id is None:
                            new_foyer_fiscal[u'id'] = new_foyer_fiscal_id = unicode(uuid.uuid4())
                            test_case[u'foyers_fiscaux'].append(new_foyer_fiscal)
                        foyers_fiscaux_individus_id.remove(individu_id)

                # Affecte à un ménage chaque individu qui n'appartient à aucun d'entre eux.
                new_menage = dict(
                    autres=[],
                    conjoint=None,
                    enfants=[],
                    personne_de_reference=None,
                    )
                new_menage_id = None
                for individu_id in menages_individus_id[:]:
                    # Tente d'affecter l'individu à un ménage d'après sa famille.
                    famille, famille_role = find_famille_and_role(test_case, individu_id)
                    if famille_role == u'parents' and len(famille[u'parents']) == 2:
                        for parent_id in famille[u'parents']:
                            if parent_id != individu_id:
                                menage, other_role = find_menage_and_role(test_case, parent_id)
                                if other_role == u'personne_de_reference' and menage[u'conjoint'] is None:
                                    # Quand l'individu n'est pas encore dans un ménage, mais qu'il est parent
                                    # dans une famille, qu'il y a un autre parent dans cette famille et que cet autre
                                    # parent est personne de référence dans un ménage et qu'il n'y a pas de conjoint
                                    # dans ce ménage, alors ajoute l'individu comme conjoint de ce ménage.
                                    menage[u'conjoint'] = individu_id
                                    menages_individus_id.remove(individu_id)
                                elif other_role == u'conjoint' and menage[u'personne_de_reference'] is None:
                                    # Quand l'individu n'est pas encore dans un ménage, mais qu'il est parent
                                    # dans une famille, qu'il y a un autre parent dans cette famille et que cet autre
                                    # parent est conjoint dans un ménage et qu'il n'y a pas de personne de référence
                                    # dans ce ménage, alors ajoute l'individu comme personne de référence de ce ménage.
                                    menage[u'personne_de_reference'] = individu_id
                                    menages_individus_id.remove(individu_id)
                                break
                    elif famille_role == u'enfants' and famille[u'parents']:
                        for parent_id in famille[u'parents']:
                            menage, other_role = find_menage_and_role(test_case, parent_id)
                            if other_role in (u'personne_de_reference', u'conjoint'):
                                # Quand l'individu n'est pas encore dans un ménage, mais qu'il est enfant dans une
                                # famille, qu'il y a un parent dans cette famille et que ce parent est personne de
                                # référence ou conjoint dans un ménage, alors ajoute l'individu comme enfant de ce
                                # ménage.
                                menage[u'enfants'].append(individu_id)
                                menages_individus_id.remove(individu_id)
                                break

                    if individu_id in menages_individus_id:
                        # L'individu n'est toujours pas affecté à un ménage.
                        # Tente d'affecter l'individu à un ménage d'après son foyer fiscal.
                        foyer_fiscal, foyer_fiscal_role = find_foyer_fiscal_and_role(test_case, individu_id)
                        if foyer_fiscal_role == u'declarants' and len(foyer_fiscal[u'declarants']) == 2:
                            for declarant_id in foyer_fiscal[u'declarants']:
                                if declarant_id != individu_id:
                                    menage, other_role = find_menage_and_role(test_case, declarant_id)
                                    if other_role == u'personne_de_reference' and menage[u'conjoint'] is None:
                                        # Quand l'individu n'est pas encore dans un ménage, mais qu'il est déclarant
                                        # dans un foyer fiscal, qu'il y a un autre déclarant dans ce foyer fiscal et que
                                        # cet autre déclarant est personne de référence dans un ménage et qu'il n'y a
                                        # pas de conjoint dans ce ménage, alors ajoute l'individu comme conjoint de ce
                                        # ménage.
                                        menage[u'conjoint'] = individu_id
                                        menages_individus_id.remove(individu_id)
                                    elif other_role == u'conjoint' and menage[u'personne_de_reference'] is None:
                                        # Quand l'individu n'est pas encore dans un ménage, mais qu'il est déclarant
                                        # dans une foyer fiscal, qu'il y a un autre déclarant dans ce foyer fiscal et
                                        # que cet autre déclarant est conjoint dans un ménage et qu'il n'y a pas de
                                        # personne de référence dans ce ménage, alors ajoute l'individu comme personne
                                        # de référence de ce ménage.
                                        menage[u'personne_de_reference'] = individu_id
                                        menages_individus_id.remove(individu_id)
                                    break
                        elif foyer_fiscal_role == u'personnes_a_charge' and foyer_fiscal[u'declarants']:
                            for declarant_id in foyer_fiscal[u'declarants']:
                                menage, other_role = find_menage_and_role(test_case, declarant_id)
                                if other_role in (u'personne_de_reference', u'conjoint'):
                                    # Quand l'individu n'est pas encore dans un ménage, mais qu'il est personne à charge
                                    # dans un foyer fiscal, qu'il y a un déclarant dans ce foyer fiscal et que ce
                                    # déclarant est personne de référence ou conjoint dans un ménage, alors ajoute
                                    # l'individu comme enfant de ce ménage.
                                    menage[u'enfants'].append(individu_id)
                                    menages_individus_id.remove(individu_id)
                                    break

                    if individu_id in menages_individus_id:
                        # L'individu n'est toujours pas affecté à un ménage.
                        if new_menage[u'personne_de_reference'] is None:
                            new_menage[u'personne_de_reference'] = individu_id
                        elif new_menage[u'conjoint'] is None:
                            new_menage[u'conjoint'] = individu_id
                        else:
                            new_menage[u'enfants'].append(individu_id)
                        if new_menage_id is None:
                            new_menage[u'id'] = new_menage_id = unicode(uuid.uuid4())
                            test_case[u'menages'].append(new_menage)
                        menages_individus_id.remove(individu_id)

            remaining_individus_id = set(familles_individus_id).union(foyers_fiscaux_individus_id, menages_individus_id)
            if remaining_individus_id:
                individu_index_by_id = {
                    individu[u'id']: individu_index
                    for individu_index, individu in enumerate(test_case[u'individus'])
                    }
                if error is None:
                    error = {}
                for individu_id in remaining_individus_id:
                    error.setdefault('individus', {})[individu_index_by_id[individu_id]] = state._(
                        u"Individual is missing from {}").format(
                            state._(u' & ').join(
                                word
                                for word in [
                                    u'familles' if individu_id in familles_individus_id else None,
                                    u'foyers_fiscaux' if individu_id in foyers_fiscaux_individus_id else None,
                                    u'menages' if individu_id in menages_individus_id else None,
                                    ]
                                if word is not None
                                ))
            if error is not None:
                return test_case, error

            # Third validation step
            parents_id = set(
                parent_id
                for famille in test_case['familles']
                for parent_id in famille['parents']
                )
            test_case, error = conv.struct(
                dict(
                    familles=conv.pipe(
                        conv.uniform_sequence(
                            conv.struct(
                                dict(
                                    enfants=conv.uniform_sequence(
                                        conv.test(
                                            lambda individu_id:
                                                individu_by_id[individu_id].get('handicap', False)
                                                or find_age(individu_by_id[individu_id], period.start.date,
                                                    default=0) <= 25,
                                            error=u"Une personne à charge d'un foyer fiscal doit avoir moins de"
                                                    u" 25 ans ou être handicapée",
                                            ),
                                        ),
                                    parents=conv.pipe(
                                        conv.empty_to_none,
                                        conv.not_none,
                                        conv.test(lambda parents: len(parents) <= 2,
                                            error=N_(u'A "famille" must have at most 2 "parents"'))
                                        ),
                                    ),
                                default=conv.noop,
                                ),
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    foyers_fiscaux=conv.pipe(
                        conv.uniform_sequence(
                            conv.struct(
                                dict(
                                    declarants=conv.pipe(
                                        conv.empty_to_none,
                                        conv.not_none,
                                        conv.test(
                                            lambda declarants: len(declarants) <= 2,
                                            error=N_(u'A "foyer_fiscal" must have at most 2 "declarants"'),
                                            ),
                                        conv.uniform_sequence(conv.pipe(
                                            # conv.test(lambda individu_id:
                                            #     find_age(individu_by_id[individu_id], period.start.date,
                                            #         default = 100) >= 18,
                                            #     error = u"Un déclarant d'un foyer fiscal doit être agé d'au moins 18"
                                            #         u" ans",
                                            #     ),
                                            conv.test(
                                                lambda individu_id: individu_id in parents_id,
                                                error = u"Un déclarant ou un conjoint sur la déclaration d'impôt, doit"
                                                        u" être un parent dans sa famille",
                                                ),
                                            )),
                                        ),
                                    personnes_a_charge=conv.uniform_sequence(
                                        conv.test(
                                            lambda individu_id:
                                                individu_by_id[individu_id].get('handicap', False)
                                                or find_age(individu_by_id[individu_id], period.start.date,
                                                    default=0) <= 25,
                                            error=u"Une personne à charge d'un foyer fiscal doit avoir moins de"
                                                    u" 25 ans ou être handicapée",
                                            ),
                                        ),
                                    ),
                                default=conv.noop,
                                ),
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    # individus = conv.uniform_sequence(
                    #     conv.struct(
                    #         dict(
                    #             date_naissance = conv.test(
                    #                 lambda date_naissance: period.start.date - date_naissance >= datetime.timedelta(0),
                    #                 error = u"L'individu doit être né au plus tard le jour de la simulation",
                    #                 ),
                    #             ),
                    #         default = conv.noop,
                    #         drop_none_values = 'missing',
                    #         ),
                    #     ),
                    menages=conv.pipe(
                        conv.uniform_sequence(
                            conv.struct(
                                dict(
                                    personne_de_reference=conv.not_none,
                                    ),
                                default=conv.noop,
                                ),
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    ),
                default=conv.noop,
                )(test_case, state=state)

            return test_case, error

        return json_or_python_to_test_case

    def suggest(self):
        """Returns a dict of suggestions and modifies self.test_case applying those suggestions."""
        test_case = self.test_case
        if test_case is None:
            return None

        period_start_date = self.period.start.date
        period_start_year = self.period.start.year
        suggestions = dict()

        for individu in test_case['individus']:
            individu_id = individu['id']
            if individu.get('age') is None and individu.get('age_en_mois') is None and individu.get('date_naissance') is None:
                # Add missing date_naissance date to person (a parent is 40 years old and a child is 10 years old.
                is_parent = any(individu_id in famille['parents'] for famille in test_case['familles'])
                birth_year = period_start_year - 40 if is_parent else period_start_year - 10
                date_naissance = datetime.date(birth_year, 1, 1)
                individu['date_naissance'] = date_naissance
                suggestions.setdefault('test_case', {}).setdefault('individus', {}).setdefault(individu_id, {})[
                    'date_naissance'] = date_naissance.isoformat()
            if individu.get('activite') is None:
                if find_age(individu, period_start_date) < 16:
                    individu['activite'] = 2  # Étudiant, élève
                    suggestions.setdefault('test_case', {}).setdefault('individus', {}).setdefault(individu_id, {})[
                        'activite'] = u'2'  # Étudiant, élève

        individu_by_id = {
            individu['id']: individu
            for individu in test_case['individus']
            }

        for foyer_fiscal in test_case['foyers_fiscaux']:
            if len(foyer_fiscal['declarants']) == 1 and foyer_fiscal['personnes_a_charge']:
                # Suggest "parent isolé" when foyer_fiscal contains a single "declarant" with "personnes_a_charge".
                if foyer_fiscal.get('caseT') is None:
                    suggestions.setdefault('test_case', {}).setdefault('foyers_fiscaux', {}).setdefault(
                        foyer_fiscal['id'], {})['caseT'] = foyer_fiscal['caseT'] = True
            elif len(foyer_fiscal['declarants']) == 2:
                # Suggest "PACSé" or "Marié" instead of "Célibataire" when foyer_fiscal contains 2 "declarants" without
                # "statut_marital".
                statut_marital = 5  # PACSé
                for individu_id in foyer_fiscal['declarants']:
                    individu = individu_by_id[individu_id]
                    if individu.get('statut_marital') == 1:  # Marié
                        statut_marital = 1
                for individu_id in foyer_fiscal['declarants']:
                    individu = individu_by_id[individu_id]
                    if individu.get('statut_marital') is None:
                        individu['statut_marital'] = statut_marital
                        suggestions.setdefault('test_case', {}).setdefault('individus', {}).setdefault(individu_id, {})[
                            'statut_marital'] = unicode(statut_marital)

        return suggestions or None



# Finders

def find_age(individu, date, default=None):
    date_naissance = individu.get('date_naissance')
    if isinstance(date_naissance, dict):
        date_naissance = date_naissance.values()[0] if date_naissance else None
    if date_naissance is not None:
        age = date.year - date_naissance.year
        if date.month < date_naissance.month or date.month == date_naissance.month and date.day < date_naissance.day:
            age -= 1
        return age

    age = individu.get('age')
    if isinstance(age, dict):
        age = age.values()[0] if age else None
    if age is not None:
        return age

    age_en_mois = individu.get('age_en_mois')
    if isinstance(age_en_mois, dict):
        age_en_mois = age_en_mois.values()[0] if age_en_mois else None
    if age_en_mois is not None:
        return age_en_mois / 12.0

    return default


def find_famille_and_role(test_case, individu_id):
    for famille in test_case['familles']:
        for role in (u'parents', u'enfants'):
            if individu_id in famille[role]:
                return famille, role
    return None, None


def find_foyer_fiscal_and_role(test_case, individu_id):
    for foyer_fiscal in test_case['foyers_fiscaux']:
        for role in (u'declarants', u'personnes_a_charge'):
            if individu_id in foyer_fiscal[role]:
                return foyer_fiscal, role
    return None, None


def find_menage_and_role(test_case, individu_id):
    for menage in test_case['menages']:
        for role in (u'personne_de_reference', u'conjoint'):
            if menage[role] == individu_id:
                return menage, role
        for role in (u'enfants', u'autres'):
            if individu_id in menage[role]:
                return menage, role
    return None, None
