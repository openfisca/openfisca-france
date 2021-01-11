import logging

log = logging.getLogger(__name__)


def init_single_entity(scenario, axes = None, enfants = None, famille = None, foyer_fiscal = None, menage = None, parent1 = None, parent2 = None, period = None):
    if enfants is None:
        enfants = []
    assert parent1 is not None

    familles = {}
    foyers_fiscaux = {}
    menages = {}
    individus = {}

    count_so_far = 0
    for nth in range(0, 1):
        famille_nth = famille.copy() if famille is not None else {}
        foyer_fiscal_nth = foyer_fiscal.copy() if foyer_fiscal is not None else {}
        menage_nth = menage.copy() if menage is not None else {}
        group = [parent1, parent2] + (enfants or [])
        for index, individu in enumerate(group):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                id = 'ind{}'.format(index + count_so_far)
            individus[id] = individu
            if index <= 1:
                famille_nth.setdefault('parents', []).append(id)
                foyer_fiscal_nth.setdefault('declarants', []).append(id)
                if index == 0:
                    menage_nth['personne_de_reference'] = id
                else:
                    menage_nth['conjoint'] = id
            else:
                famille_nth.setdefault('enfants', []).append(id)
                foyer_fiscal_nth.setdefault('personnes_a_charge', []).append(id)
                menage_nth.setdefault('enfants', []).append(id)

        count_so_far += len(group)
        familles["f{}".format(nth)] = famille_nth
        foyers_fiscaux["ff{}".format(nth)] = foyer_fiscal_nth
        menages["m{}".format(nth)] = menage_nth

    test_data = {
        'period': period,
        'familles': familles,
        'foyers_fiscaux': foyers_fiscaux,
        'menages': menages,
        'individus': individus
        }
    if axes:
        test_data['axes'] = axes
    scenario.init_from_dict(test_data)
    return scenario
