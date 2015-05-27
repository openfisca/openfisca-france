# OpenFisca France

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-france.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-france)

## Presentation

[OpenFisca](http://www.openfisca.fr/) is a versatile microsimulation free software.
This is the source code of the France module.

Please consult http://www.openfisca.fr/presentation

## Documentation

Please consult http://www.openfisca.fr/documentation

## Installation

Requirement: [OpenFisca-Core](https://github.com/openfisca/openfisca-core).

Clone the OpenFisca-France Git repository on your machine and install the Python package.
Assuming you are in your working directory:

```
git clone https://github.com/openfisca/openfisca-france.git
cd openfisca-france
pip install --editable . --user
python setup.py compile_catalog
```

For your information, the Tunisian tax-benefit system is also available:
[OpenFisca-Tunisia](https://github.com/openfisca/openfisca-tunisia).


## Tests

Before submitting a pull request, please execute tests:

    make test

To download tests from [Ludwig](https://mes-aides.gouv.fr/tests/)
(the tests tool from [Mes aides](https://mes-aides.gouv.fr/)),
see [OpenFiscaFrance.jl](https://github.com/openfisca/OpenFiscaFrance.jl)

## Contribute

OpenFisca is a free software project.
Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see COPYING).

Feel free to join the OpenFisca development team on [GitHub](https://github.com/openfisca) or contact us by email at
contact@openfisca.fr
