TESTS_DIR="openfisca_france/tests"
IGNORE_OPT=--ignore-files='(test_from_taxipp.py|test_plfrss2014.py|test_jsons.py|test_net_to_brut.py)'

check-tests-syntax:
	pyflakes $(TESTS_DIR)

test: check-tests-syntax
	nosetests -v  $(TESTS_DIR) $(IGNORE_OPT)

test-with-coverage:
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT) --with-coverage --cover-package=openfisca_france --cover-erase --cover-branches --cover-html
