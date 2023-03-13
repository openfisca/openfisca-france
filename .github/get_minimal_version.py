import re


with open('./setup.py') as file:
    for line in file:
        version = re.search(r'(Core|France)\s*>=\s*([\d\.]*)', line)
        if version:
            print(f'Openfisca-{version[1]}=={version[2]}')
