import requests
import pkg_resources  # part of setuptools
import json
import sys

package_version = pkg_resources.require("openfisca-france")[0].version

response_API = requests.get('https://fr.openfisca.org/api/latest/spec')
data = json.loads(response_API.text)
api_package_version = data['info']['version']

sys.stdout.write("API package version: {}\nLocal package version: {}\n".format(api_package_version, package_version))

if api_package_version != package_version:
    sys.exit("The version of the API deployed on fr.openfisca.org/api/latest/spec does not match the local package version.")
