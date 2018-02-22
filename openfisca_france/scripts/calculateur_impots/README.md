# Calculateur_impots

This directory contains all the codes necessary to produce a battery of YAML tests of the French income tax, which can be done by running the program [create_tests.py](./create_tests.py). These tests can later be run in a separate program to check that the income tax is correctly computed by OpenFisca-France for each year.

It uses the income tax simulator of the French Ministry of Finance DGFIP, that is [available online](https://www.impots.gouv.fr/portail/simulateurs), to provide the benchmark results of income tax simulation.


## Inputs

* **A Tax & Benefit system**

It is defined in [base.py](./base.py) as the default *FrenchTaxBenefitSystem()*

* **A serie of Test case Scenarios**

Each test is build upon one scenario, which must contains a test case and a period. They can be builded from the [input_scenario_builder](./input_scenario_builder/build_scenarios_to_test.py).

These scenarios must have been stored in a .JSON format in [openfisca-france/tests/calculateur_impots/scenarios](../../../tests/calculateur_impots/scenarios/). If no scenarios are to be found in this folder, the programm will build new scenarios to test, by running the [input_scenario_builder](./input_scenario_builder/build_scenarios_to_test.py).

## Functionning

For each input scenario found in the folder, a test is created following these three steps :

* First, the program reads the JSON file containing the input scenario to test and deduce from its name which aspect of the income tax legislation it is made to test (a certain type of income, a certain feature of the income tax..).

* Then, it connects to the online DGFiP income tax simulator and gets back the official results of the simulation for this given test case scenario. The input scenario and the associated results are stored into a JSON file.

* Finally, it converts the informations contained in this JSON file into a YAML test that is runable.

## Outputs

All the outputs, as well as the input scenarios, are stored in the [openfisca-france/tests/calculateur_impots/](../../tests/calculateur_impots/) folder.

* **JSON files**

The intermediate JSON files are stored in the subfolder [/json](../../../tests/calculateur_impots/json/) with one file for each variable tested, and for each period tested.

* **YAML tests**

The YAML tests produced are stored in the subfolder [/yaml](../../../tests/calculateur_impots/yaml/) with one file for each variable tested and one test for each period in a given file.


-----------------

NB : to test the result of an OpenFisca income tax simulation for a given year and a given scenario, one can use [compare_openfisca_impots.py](./compare_openfisca_impots.py) and define by hand the scenario wanted in *define_scenario()*

NB2 : to run the YAML tests created, one can use the command *openfisca-run-test* like the following example :
```
openfisca-run-test tests/calculateur_impots/yaml/chomage_imposable.yaml --c openfisca_france
```

NB3 : to run the YAML test by testing only a subset of the output variables defined in the test, one can use the `only-variables` option, by typing:
```
openfisca-run-test tests/calculateur_impots/yaml/chomage_imposable.yaml --c openfisca_france -o variable1 variable2
```

where `variable1` and `variable2` are the output variables to be tested.

NB4 : to run the YAML test by excluding from output variables a subset of variables, one can use the `ignore-variables` option, by typing:
```
openfisca-run-test tests/calculateur_impots/yaml/chomage_imposable.yaml --c openfisca_france -i variable1 variable2
```

where `variable1` and `variable2` are the output variables to be excluded. This option is the reverse of the `only` option.