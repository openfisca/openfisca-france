TESTS_DIR="openfisca_france/tests/"
IGNORE_OPT=--ignore-files='(test_from_taxipp.py|test_jsons.py|test_fiche_de_paie_api.py|test_brut_to_imposable.py|test_net_to_brut.py|test_rsa.py|generate_json.py|taxipp_utils.py|create_json_then_test.py|compare_openfisca_impots.py)'

check-syntax-errors: clean-pyc
	@# This is a hack around flake8 not displaying E910 errors with the select option.
	test -z "`flake8 --first | grep E901`"

clean-pyc:
	find -name '*.pyc' -exec rm \{\} \;

ctags:
	ctags --recurse=yes .

flake8: clean-pyc
	flake8

test: check-syntax-errors
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT)

test-with-coverage:
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT) --with-coverage --cover-package=openfisca_france --cover-erase --cover-branches --cover-html
