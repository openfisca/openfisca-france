from nose.tools import raises

import openfisca_france

tbs = openfisca_france.init_tax_benefit_system()

familles = tbs.entity_class_by_key_plural['familles']

def test_extension_not_already_loaded():
	assert familles.column_by_name.get('paris_logement_famille') is None

def test_load_extension():
	from openfisca_france.model.extensions import import_extension
	import_extension('https://github.com/sgmap/openfisca-paris.git')
	assert familles.column_by_name.get('paris_logement_familles') is not None
	tbs.index_columns()
	assert tbs.column_by_name.get('paris_logement_familles') is not None

def test_unload_extensions():
	from openfisca_france.model.extensions import unload_all_extensions
	unload_all_extensions()
	assert familles.column_by_name.get('paris_logement_famille') is None
	assert tbs.column_by_name.get('paris_logement_famille') is None

@raises(IOError)
def test_failure_to_load_extension_when_directory_doesnt_exist():
	from openfisca_france.model.extensions import import_extension
	import_extension('/this/is/not/a/real/path')

@raises(IOError)
def test_failure_to_load_extension_when_git_repo_doesnt_exist():
	from openfisca_france.model.extensions import import_extension
	import_extension('https://github.com/not/a/real/git/repo.git')

