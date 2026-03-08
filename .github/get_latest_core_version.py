'''
Vérifie si une nouvelle version d'openfisca-core est disponible au-delà de la borne
supérieure définie dans pyproject.toml. Si oui, écrit les outputs GitHub Actions.
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

    if Version(latest) >= Version(max_bound):
        new_max_major = current_max_major + 1
        print(f'Nouvelle version {latest} dépasse la borne <{max_bound} — test requis')  # noqa: T201
        set_github_output('has_new_version', 'true')
        set_github_output('new_version', latest)
        set_github_output('new_max_bound', str(new_max_major))
        set_github_output('current_max_bound', str(current_max_major))
        sys.exit(0)
    else:
        print(f'La version {latest} est déjà dans les bornes — aucune action requise')  # noqa: T201
        set_github_output('has_new_version', 'false')
        sys.exit(0)
