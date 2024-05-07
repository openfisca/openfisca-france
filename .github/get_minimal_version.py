import re
import tomli
# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing
with open('./pyproject.toml', 'rb') as file:
    config = tomli.load(file)
    deps = config['project']['dependencies']
    for dep in deps:
        version = re.search(r'openfisca-core\[([^\]]+)\]\s*>=\s*([\d\.]*)', dep)
        if version:
            try:
                print(f'openfisca-core[{version[1]}]=={version[2]}')  # noqa: T201 <- This is to avoid flake8 print detection.
            except Exception as e:
                print(f'Error processing "{dep}": {e}')  # noqa: T201 <- This is to avoid flake8 print detection.
                exit(1)
