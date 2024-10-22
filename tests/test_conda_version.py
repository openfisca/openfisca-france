import os
import tempfile
import subprocess
import pytest
import re

def test_pyproject_version_script():
    # Create a temporary file with the specified content
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    temp_file.write("version: X.X.X\n    - openfisca-core-api>=43,<44\n")
    temp_file.close()

    # Read the values
    # Run the pyproject_version.py script without arguments and read {'openfisca_france': '169.1.0', 'openfisca_core_api': '>=43,<44'}
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', '.github', 'pyproject_version.py')
    result = subprocess.run(['python3', script_path], stdout=subprocess.PIPE, check=True)
    # Extract the version of openfisca_france
    content = result.stdout.decode('utf-8')
    version_match = re.search(r'^version\s*=\s*"([\d.]*)"', content, re.MULTILINE)
    if version_match:
        openfisca_version = version_match.group(1)
    # Extract dependencies
    version = re.search(r'openfisca-core\[web-api\]\s*(>=\s*[\d\.]*,\s*<\d*)"', content, re.MULTILINE)
    assert version.group(1) == '>=43,<44'


    # Run the pyproject_version.py script with the --replace True argument
    subprocess.run(['python3', script_path, '--replace', 'True', '--filename', temp_file.name], check=True)

    # Check the value has changed
    with open(temp_file.name, 'r') as file:
        content = file.read()
        assert f"version: {openfisca_version}" not in content
        assert "openfisca-core-api>=43,<44" in content

    # Clean up the temporary file
    os.remove(temp_file.name)

if __name__ == "__main__":
    pytest.main()