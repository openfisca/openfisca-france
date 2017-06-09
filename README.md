# OpenFisca-France

[![Build Status](https://travis-ci.org/openfisca/openfisca-france.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-france)

## [EN] Introduction
OpenFisca is a versatile microsimulation free software. This repository contains the OpenFisca model of the French tax and benefit system. Therefore, the working language here is French. You can however check the [general OpenFisca documentation](https://doc.openfisca.fr/) in English !

## [FR] Introduction
[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation du système social et fiscal français. Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](https://doc.openfisca.fr/).

## Legislation Explorer, un guide de l'API publique OpenFisca

OpenFisca France met à disposition une [API Web publique](https://doc.openfisca.fr/openfisca-web-api/index.html) qui ne demande aucune installation.
Utilisez l'API publique si :
- vous souhaitez accéder à un paramètre (Ex : [le montant du SMIC horaire brut](https://legislation.openfisca.fr/cotsoc.gen.smic_h_b)) ;
- vous souhaitez consulter une formule de calcul (Ex : [le calcul de l'allocation de base des Allocations familiales](https://legislation.openfisca.fr/af_base) ;
- vous souhaitez faire des calculs ponctuels sur une situation (Ex : le calcul une taxe d'habitation pour un ménage).

[L'explorateur de législation](https://legislation.openfisca.fr/) contient la liste des paramètres et variables disponibles.

## [EN] Installation

This package requires Python 2.7.

Supported platforms:
- GNU/Linux distributions (in particular Debian and Ubuntu);
- Mac OS X;
- Microsoft Windows (we recommend using [ConEmu](https://conemu.github.io/) instead of the default console).

Other OS should work if they can execute Python and NumPy.

>***A note on dependencies***: OpenFisca-Core will be installed automatically as a requirement of OpenFisca-France. Run pip freeze to see the installed packages: openfisca_core and openfisca_france should be listed.

### [EN] Setting up a virtual environment with Pew

We recommend using a [virtual environment](https://virtualenv.pypa.io/en/stable/) (abbreviated as "virtualenv") with a virtualenv manager such as [pew](https://github.com/berdario/pew).

- A [virtualenv](https://virtualenv.pypa.io/en/stable/) is a project specific environment created to suit the needs of the project you are working on.
- A virtualenv manager, such as [pew](https://github.com/berdario/pew), lets you easily create, remove and toggle between several virtualenvs.

To install pew, launch a terminal on your computer and follow these instructions:

```sh
pip install --upgrade pip
pip install pew  # answer "Y" to the question about modifying your shell config file.
```
To set-up and create a new a virtualenv named **openfisca** running python2.7:

```sh
pew new openfisca --python=python2.7
```

The virtualenv you just created will be automatically activated. This means you will operate in the virtualenv immediately.
- Exit the virtualenv with `exit` (or Ctrl-D).
- Re-enter with `pew workon openfisca`.

### [EN] Minimal Installation (pip install)

Follow this installation if you wish to:
- run calculations on a large population;
- create tax & benefits simulations;
- write an extension to this legislation (e.g. city specific tax & benefits);
- serve this Country Package with the OpenFisca Web API.

For more advanced uses, head to the [Advanced Installation](#en-advanced-installation-git-clone).

#### [EN] Install a Country Package with pip install

Inside your virtualenv, check the prerequisites:

```sh
python --version  # should print "Python 2.7.xx".
#if not, make sure you pass the python version as an argument when creating your virtualenv
```

```sh
pip --version  # should print at least 9.0.
#if not, run "pip install --upgrade pip"
```
Install the OpenFisca Country Package:

```sh
#Example: Openfisca-France
pip install openfisca-france
```

#### [EN] Next steps

- To learn how to use OpenFisca, follow our [tutorials](https://doc.openfisca.fr/getting-started.html).
- To serve your country package, serve the [OpenFisca web API](#serve-your-country-package-with-the-openFisca-web-api).

Depending on what you want to do with OpenFisca, you may want to install yet other packages in your virtualenv:
- To install extensions or write on top of your country package, head to the [Extensions documentation](https://doc.openfisca.fr/contribute/extensions.html).
- To plot simulation results, try [matplotlib](http://matplotlib.org/).
- To manage data, check out [pandas](http://pandas.pydata.org/).

### [EN] Advanced installation (Git Clone)

Follow this tutorial if you wish to:
- create or change this Country Package's legislation;
- contribute to the source code.

>***A note on OpenFisca-Core***: If you need to modify OpenFisca-Core source code (e.g. you want to contribute to a Country Package agnostic feature), follow this [install tutorial](https://github.com/openfisca/openfisca-core#installation) section before completing the step below. By default just continue below.

#### [EN] Clone a Country Package with Git

First of all, make sure [Git](https://www.git-scm.com/) is installed on your machine.

Set your working directory to the location where you want this OpenFisca Country Package cloned.

Inside your virtualenv, check the prerequisites:

```sh
python --version  # should print "Python 2.7.xx".
#if not, make sure you pass the python version as an argument when creating your virtualenv
```

```sh
pip --version  # should print at least 9.0.
#if not, run "pip install --upgrade pip"
```
Clone the Country Package on your machine:

```sh
#Example: Openfisca-France
git clone https://github.com/openfisca/openfisca-france.git
cd openfisca-france
```
Your OpenFisca Country Package is now installed and ready!

#### [EN] Next steps

- To write new legislation, read the [Coding the legislation](https://doc.openfisca.fr/coding-the-legislation/index.html) section to know how to write legislation.
- To contribute to the code, read our [Contribution Guidebook](https://doc.openfisca.fr/contribute/index.html).

## [EN] Serve your Country Package with the OpenFisca Web API

If you are considering building a web application, you can plug the OpenFisca Web API to your Country Package.

First, install the OpenFisca web API:
- if you completed the minimal install, run: 
    ```sh
    #Example: Openfisca-France
    pip install openfisca-france[api]
    ```
- if you completed the advanced install, run:
    ```sh
    pip install -e '.[api]'
    ```

Then serve the Openfisca Web API locally:

```sh
openfisca-serve --port 2000
```

You can make sure that the API is working by requesting:

```sh
curl "http://localhost:2000/api/2/entities"
```

To learn more, go to the [OpenFisca Web API documentation](https://doc.openfisca.fr/openfisca-web-api/index.html)


## Stratégie de versionnement

Le code d'Openfisca-France est versionné de manière continue et automatique. Ainsi, à chaque fois que le code de la législation évolue sur la branche principale `master`, une nouvelle version est publiée.

De nouvelles versions sont donc publiées très régulièrement. Cependant, la différence entre deux versions consécutives étant réduite, les efforts d'adaptation pour passer de l'une à l'autre sont en général très limités.

Par ailleurs, OpenFisca-France respecte les règles du [versionnement sémantique](http://semver.org/). Tous les changements qui ne font pas l'objet d'une augmentation du numéro majeur de version sont donc garantis rétro-compatibles.

> Par exemple, si mon application utilise la version `13.1.1`, je sais qu'elle fonctionnera également avec la version `13.2.0`. En revanche, il est possible qu'une adaptation soit nécessaire sur mon client pour pouvoir utiliser la version `14.0.0`.

Enfin, les impacts et périmètres des évolutions sont tous documentés sur le [CHANGELOG](CHANGELOG.md) du package. Ce document permet aux contributeurs de suivre les évolutions et d'établir leur propre stratégie de mise à jour.

## Contributeurs

Voir la [liste des contributeurs](https://github.com/openfisca/openfisca-france/graphs/contributors).
