all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

install:
	pip install --upgrade pip twine wheel
	pip install --editable .[dev] --upgrade && pip install openfisca-core[web-api]

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

check-no-prints:
	@test -z "`git grep -w print openfisca_france/model`"

check-syntax-errors:
	python -m compileall -q .

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

test: clean check-syntax-errors check-no-prints check-style format-style
	@# Launch tests from openfisca_france/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	nosetests tests --exe --with-doctest
	openfisca-run-test --country-package openfisca_france tests

performance:
	python openfisca_france/scripts/performance_tests/test_tests.py
