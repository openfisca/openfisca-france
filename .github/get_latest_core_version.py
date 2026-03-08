'''
Vérifie si une nouvelle version d'openfisca-core est disponible sur PyPI
par rapport à la borne minimale définie dans pyproject.toml.

Deux cas déclenchent un test :
- Version mineure/patch dans les bornes (ex: 44.3.0 > borne min 44.2.2)
  → si le test passe : PR pour mettre à jour la borne min (>=44.3.0)
- Version majeure au-delà de la borne supérieure (ex: 45.0.0 >= <45)
  → si le test passe : PR pour mettre à jour la borne max (<46)

La borne minimale sert ainsi de marqueur de "dernière version testée".
'''

import os
import re
import sys

import requests
from packaging.version import Version


def get_latest_version(package_name: str) -> str:
    resp = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    return resp['info']['version']


def get_core_bounds() -> tuple[str, str]:
    with open('./pyproject.toml', 'r') as f:
        content = f.read()
    match = re.search(
        r'openfisca-core\[web-api\]\s*>=\s*([\d.]+),\s*<\s*([\d.]+)',
        content,
        )
    if match:
        return match.group(1), match.group(2)
    raise Exception('Impossible de trouver les bornes d\'openfisca-core dans pyproject.toml')


def set_github_output(name: str, value: str):
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f'{name}={value}\n')
    else:
        print(f'  → output: {name}={value}')  # noqa: T201


if __name__ == '__main__':
    latest = get_latest_version('openfisca-core')
    min_bound, max_bound = get_core_bounds()

    print(f'Dernière version openfisca-core sur PyPI : {latest}')  # noqa: T201
    print(f'Borne actuelle dans pyproject.toml : >={min_bound}, <{max_bound}')  # noqa: T201

    current_max_major = int(max_bound.split('.')[0])

    if Version(latest) <= Version(min_bound):
        print(f'La version {latest} est déjà couverte par la borne min >={min_bound} — aucune action requise')  # noqa: T201
        set_github_output('has_new_version', 'false')
        sys.exit(0)

    if Version(latest) >= Version(max_bound):
        # Nouvelle version majeure au-delà de la borne supérieure
        new_max_major = current_max_major + 1
        print(f'Nouvelle version majeure {latest} dépasse la borne <{max_bound} — test requis')  # noqa: T201
        set_github_output('has_new_version', 'true')
        set_github_output('bump_type', 'major')
        set_github_output('new_version', latest)
        set_github_output('new_max_bound', str(new_max_major))
        set_github_output('current_max_bound', str(current_max_major))
        set_github_output('current_min_bound', min_bound)
    else:
        # Nouvelle version mineure/patch dans les bornes
        print(f'Nouvelle version mineure {latest} > borne min >={min_bound} — test requis')  # noqa: T201
        set_github_output('has_new_version', 'true')
        set_github_output('bump_type', 'minor')
        set_github_output('new_version', latest)
        set_github_output('new_max_bound', max_bound.split('.')[0])
        set_github_output('current_max_bound', str(current_max_major))
        set_github_output('current_min_bound', min_bound)
