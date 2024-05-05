import re

# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing
with open('./pyproject.toml') as file:
    for line in file:
        version = re.search(r'core[^>]+>=\s*([\d\.]*)', line)
        if version:
            print(f'OpenFisca-{version[1]}=={version[2]}')  # noqa: T201 <- This is to avoid flake8 print detection.

        if pre:
            print(f'{pre[2]}')  # noqa: T201 <- The same as supra.
