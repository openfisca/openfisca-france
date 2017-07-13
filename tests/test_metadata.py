# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from cache import tax_benefit_system


def test_metadata():
    metadata = tax_benefit_system.get_package_metadata()
    assert_equal(metadata['name'], 'openfisca-france')
    assert_equal(metadata['repository_url'], 'https://github.com/openfisca/openfisca-france')
