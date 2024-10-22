import os
import tempfile
import subprocess
import re
from unittest import TestCase


class TestPyprojectVersion(TestCase):

    def get_of_version_from_pyproject(self):
        with open('./pyproject.toml', 'r') as file:
            content = file.read()
        # Extract the version of openfisca_france
        version_match = re.search(r'^version\s*=\s*"([\d.]*)"', content, re.MULTILINE)
        if version_match:
            return version_match.group(1)

    def test_pyproject_version_only(self):
        # Run the pyproject_version.py script with the --only_package_version True argument
        script_path = os.path.join('.github', 'pyproject_version.py')
        result = subprocess.run(['python3', script_path, '--only_package_version', 'True'], stdout=subprocess.PIPE, check=True)
        # Extract the version of openfisca_france
        openfisca_version = result.stdout.decode('utf-8').replace('\n', '')
        self.assertEqual(openfisca_version, self.get_of_version_from_pyproject())

    def test_pyproject_version_script(self):
        # Create a temporary file with the specified content
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        temp_file.write('version: X.X.X\n    - openfisca-core-api>=43,<44\n    - numpy>=1.24.3,<2')
        temp_file.close()

        # Read the values
        # Run the pyproject_version.py script without arguments and read {'openfisca_france': '169.1.0', 'openfisca_core_api': '>=43,<44'}
        script_path = os.path.join('.github', 'pyproject_version.py')
        result = subprocess.run(['python3', script_path], stdout=subprocess.PIPE, check=True)
        # Extract the version of openfisca_france
        content = result.stdout.decode('utf-8')
        version_match = re.search(r"'openfisca_france': '([\d.]*)'", content, re.MULTILINE)
        if version_match:
            openfisca_version = version_match.group(1)
        # Extract dependencies
        version = re.search(r"openfisca_core_api': '(>=\s*[\d\.]*,\s*<\d*)'", content, re.MULTILINE)
        if version:
            openfisca_core_api = version.group(1)
        else:
            openfisca_core_api = None
            raise Exception('openfisca-core-api not found')

        # Run the pyproject_version.py script with the --replace True argument
        subprocess.run(['python3', script_path, '--replace', 'True', '--filename', temp_file.name], check=True)

        # Check the value has changed
        with open(temp_file.name, 'r') as file:
            content = file.read()
            self.assertTrue('X.X.X' not in content)
            self.assertTrue(openfisca_version in content)
            self.assertTrue(openfisca_core_api in content)

        # Clean up the temporary file
        os.remove(temp_file.name)
