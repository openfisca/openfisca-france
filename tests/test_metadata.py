from .cache import tax_benefit_system


def test_metadata():
    metadata = tax_benefit_system.get_package_metadata()
    assert metadata['name'] == 'openfisca-france'
    assert metadata['repository_url'] == 'https://github.com/openfisca/openfisca-france'
