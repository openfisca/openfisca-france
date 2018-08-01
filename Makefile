all: test

check-no-prints:
	@test -z "`git grep -w print openfisca_france/model`"

check-syntax-errors:
	python -m compileall -q .

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

formatting:
	black --check .

test: check-syntax-errors check-no-prints
	@# Launch tests from openfisca_france/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	nosetests tests --exe --with-doctest
	openfisca-run-test --country-package openfisca_france tests

performance:
	python openfisca_france/scripts/performance_tests/test_tests.py
