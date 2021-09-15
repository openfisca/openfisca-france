import requests
import re
import sys
import pkg_resources  # part of setuptools

package_version = pkg_resources.require("openfisca-france")[0].version

response_API = requests.get('https://fr.openfisca.org/legislation/swagger')
data = response_API.text
api_package_version = re.search('countryPackageVersion":"(.*)","entities', data).group(1)

sys.stdout.write(str(api_package_version == package_version))
