all: test

check-no-prints:
	@test -z "`git grep -w print openfisca_france/model`"

check-syntax-errors:
	@# This is a hack around flake8 not displaying E910 errors with the select option.
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	@test -z "`flake8 --first $(shell git ls-files | grep "\.py$$") | grep E901`"

clean:
	rm -rf build dist
	find . -name '*.mo' -exec rm \{\} \;
	find . -name '*.pyc' -exec rm \{\} \;

flake8:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

test: check-syntax-errors check-no-prints
	@# Launch tests from openfisca_france/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	nosetests openfisca_france/tests --exe --with-doctest

test-xunit-force: check-syntax-errors check-no-prints
	export FORCE=true; nosetests openfisca_france/tests/test_yaml.py --exe --with-xunit
