from openfisca_core.scripts import build_tax_benefit_system
from openfisca_web_api.app import create_app

country_package = 'openfisca_france'
extensions = ['openfisca_paris']
reforms = ['openfisca_france.reforms.plf2015.plf2015']

tax_benefit_system = build_tax_benefit_system(
    country_package_name = country_package,
    extensions = extensions,
    reforms = reforms,
)

application = create_app(tax_benefit_system)