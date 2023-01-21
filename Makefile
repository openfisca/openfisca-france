## The openfisca command module.
openfisca = openfisca_core.scripts.openfisca_command

all: test

uninstall:
	@python -m pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs python -m pip uninstall -y

clean:
	@ls -d * | grep "build\|dist" | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name "*.pyc" | xargs rm -rf

## Install project's overall dependencies
install-deps:
	@python -m pip install --upgrade pip build wheel

## Install project's build dependencies.
install-dist:
	@python -m pip install ".[ci,dev]"

## Install project's development dependencies.
install-edit:
	@# `make install` installs the editable version of OpenFisca-France.
	@# This allows contributors to test as they code.
	@python -m pip install --upgrade --editable ".[dev]"
	@python -m pip install openfisca-core[web-api]

## Install OpenFisca-France for deployment and publishing.
build:
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-France, the same we put in the hands of users and reusers.
	@python -m build
	@python -m pip uninstall --yes openfisca-france
	@find dist -name "*.whl" -exec python -m pip install --no-deps {} \;
	@python -m pip install openfisca-core[web-api]

check-syntax-errors:
	@python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	@autopep8 `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	@flake8 `git ls-files | grep "\.py$$"`

## Check yaml style
check-yaml:
	@.github/lint-changed-yaml-tests.sh

## Check all yaml style
check-all-yaml:
	@python -m yamllint .

test-python:
	@python -m ${openfisca} test tests/**/*.py

## Verify that there is no path exceeding Windows limit
test-path-length:
	@python openfisca_france/scripts/check_path_length.py

test: clean check-syntax-errors check-style
	@# Launch tests from openfisca_france/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	@python -m ${openfisca} test --country-package openfisca_france tests

## Upload to PyPi.
publish:
	@python -m twine upload dist/* \
		--username $PYPI_USERNAME \
		--password $PYPI_PASSWORD
	@git tag `python setup.py --version`
	@git push --tags  # update the repository version
