import re

# This script fetches and prints the minimal versions of Openfisca-Core and Openfisca-France
# dependencies in order to ensure their compatibility during CI testing
with open('./setup.py') as file:
    for line in file:
        #: Check for released versions.
        version = re.search(r'(Core|France)\s*>=\s*([\d\.]*)', line)

        #: Check for pre-release versions.
        pre = re.search(r'(Core|France)\s@\s(.*)\'\,$', line)

        if version:
            print(f'OpenFisca-{version[1]}=={version[2]}')  # noqa: T201 <- This is to avoid flake8 print detection.

        if pre:
            print(f'{pre[2]}')  # noqa: T201 <- The same as supra.
