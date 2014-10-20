TESTS_DIR="openfisca_france/tests/"
IGNORE_OPT=--ignore-files='(test_from_taxipp.py|test_plfrss2014.py|test_jsons.py)'

check-syntax-errors:
	@# This is a hack around flake8 not displaying E910 errors with the select option.
	test -z "`flake8 --first | grep E901`"

test: check-syntax-errors
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT)

test-with-coverage:
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT) --with-coverage --cover-package=openfisca_france --cover-erase --cover-branches --cover-html
