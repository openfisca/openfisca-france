# -*- coding: utf-8 -*-

import collections
import itertools

from openfisca_core import entities


class Entreprises(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    index_for_person_variable_name = 'entreprise_id'
    key_plural = 'entreprises'
    key_singular = 'entreprise'
    label = u'Entreprise'
    role_for_person_variable_name = 'entreprise_role'
    roles_key = ['salaries']  # 'dirigeants']
    label_by_role_key = {
        'salaries': u'Salariés',
        # 'dirigeants': u'Dirigeants',
        }
    symbol = 'entreprise'

    def iter_member_persons_role_and_id(self, member):
        role = 0

        salaries_id = member['salariés']
        for salarie_role, salarie_id in enumerate(salaries_id, role):
            assert salarie_id is not None
            yield salarie_role, salarie_id


class Familles(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    index_for_person_variable_name = 'idfam'
    key_plural = 'familles'
    key_singular = 'famille'
    label = u'Famille'
    max_cardinality_by_role_key = {'parents': 2}
    role_for_person_variable_name = 'quifam'
    roles_key = ['parents', 'enfants']
    label_by_role_key = {
        'enfants': u'Enfants',
        'parents': u'Parents',
        }
    symbol = 'fam'

    def iter_member_persons_role_and_id(self, member):
        role = 0

        parents_id = member['parents']
        assert 1 <= len(parents_id) <= 2
        for parent_role, parent_id in enumerate(parents_id, role):
            assert parent_id is not None
            yield parent_role, parent_id
        role += 2

        enfants_id = member.get('enfants')
        if enfants_id is not None:
            for enfant_role, enfant_id in enumerate(enfants_id, role):
                assert enfant_id is not None
                yield enfant_role, enfant_id


class FoyersFiscaux(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    index_for_person_variable_name = 'idfoy'
    key_plural = 'foyers_fiscaux'
    key_singular = 'foyer_fiscal'
    label = u'Déclaration d\'impôt'
    max_cardinality_by_role_key = {'declarants': 2}
    role_for_person_variable_name = 'quifoy'
    roles_key = ['declarants', 'personnes_a_charge']
    label_by_role_key = {
        'declarants': u'Déclarants',
        'personnes_a_charge': u'Personnes à charge',
        }
    symbol = 'foy'

    def iter_member_persons_role_and_id(self, member):
        role = 0

        declarants_id = member['declarants']
        assert 1 <= len(declarants_id) <= 2
        for declarant_role, declarant_id in enumerate(declarants_id, role):
            assert declarant_id is not None
            yield declarant_role, declarant_id
        role += 2

        personnes_a_charge_id = member.get('personnes_a_charge')
        if personnes_a_charge_id is not None:
            for personne_a_charge_role, personne_a_charge_id in enumerate(personnes_a_charge_id, role):
                assert personne_a_charge_id is not None
                yield personne_a_charge_role, personne_a_charge_id


class Individus(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    is_persons_entity = True
    key_plural = 'individus'
    key_singular = 'individu'
    label = u'Personne'
    symbol = 'ind'


class Menages(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    index_for_person_variable_name = 'idmen'
    key_plural = 'menages'
    key_singular = 'menage'
    label = u'Logement principal'
    max_cardinality_by_role_key = {'conjoint': 1, 'personne_de_reference': 1}
    role_for_person_variable_name = 'quimen'
    roles_key = ['personne_de_reference', 'conjoint', 'enfants', 'autres']
    label_by_role_key = {
        'autres': u'Autres',
        'conjoint': u'Conjoint',
        'enfants': u'Enfants',
        'personne_de_reference': u'Personne de référence',
        }
    symbol = 'men'

    def iter_member_persons_role_and_id(self, member):
        role = 0

        personne_de_reference_id = member['personne_de_reference']
        assert personne_de_reference_id is not None
        yield role, personne_de_reference_id
        role += 1

        conjoint_id = member.get('conjoint')
        if conjoint_id is not None:
            yield role, conjoint_id
        role += 1

        autres_id = member.get('autres') or []
        enfants_id = member.get('enfants') or []
        for enfant_role, enfant_id in enumerate(itertools.chain(enfants_id, autres_id), role):
            yield enfant_role, enfant_id

entities = [Familles, FoyersFiscaux, Individus, Menages]
