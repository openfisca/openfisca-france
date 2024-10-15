# The number of CPUs available.
ncpus = $$(which nproc > /dev/null && nproc || sysctl -n hw.logicalcpu)

all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip build twine

install: deps
	@# Install OpenFisca-France for development.
	@# `make install` installs the editable version of OpenFisca-France.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade
	pip install openfisca-core[web-api]

build: clean deps
	@# Install OpenFisca-France for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-France, the same we put in the hands of users and reusers.
	python -m build
	pip uninstall --yes openfisca-france
	find dist -name "*.whl" -exec pip install {}[dev] \;
	pip install openfisca-core[web-api]

check-syntax-errors:
	python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

check-path-length:
	@# Verify that there is no path exceeding Windows limit
	python openfisca_france/scripts/check_path_length.py

check-yaml:
	@# check yaml style
	.github/lint-changed-yaml-tests.sh

check-all-yaml:
	@# check yaml style
	yamllint openfisca_france/parameters
	yamllint tests

test: clean check-syntax-errors check-style
	@# Launch tests from openfisca_france/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	openfisca test --country-package openfisca_france tests

test-parallel: MAKEFLAGS = --output-sync -j -l $(shell echo $$((${ncpus} + 1))) --silent
test-parallel: NODES = $(shell seq ${ncpus})
test-parallel: ;
	@# Launch tests in parallel.
	@#
	@# Usage:
	@#
	@# 		make test-parallel  # It will use the number of CPUs available.
	@# 		make test-parallel ncpus=4  # It will split tests in 4 parallel groups.
	@#
	@$(foreach step, ${NODES}, ${MAKE} test-parallel-${step} ncpus=${ncpus})

test-parallel-%: PYTEST = ${PYTEST_ADDOPTS} -qx
test-parallel-%: TESTS = $(shell python .github/split_tests.py ${ncpus} $(shell echo $$(($* - 1))))
test-parallel-%: ;
	@# Launch a specific test group, useful for test-driven developement.
	@#
	@# Usage:
	@#
	@# 		make test-parallel-8  # Assuming you have 8 CPUs, it will launch the last test group.
	@# 		make test-parallel-4 ncpus=16  # It will split tests in 16 and launch de 4th group.
	@# 		make test-parallel-2 ncpus=1  # This fails because the group is out of bounds.
	@#
	@echo "[$*/${ncpus}] Starting tests..."
	@PYTEST_ADDOPTS="${PYTEST}" openfisca test --country-package openfisca_france ${TESTS}
	@echo "[$*/${ncpus}] Finished!"
