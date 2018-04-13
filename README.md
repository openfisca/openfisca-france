# OpenFisca-France

[![Build Status](https://travis-ci.org/openfisca/openfisca-france.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-france)

## [EN] Introduction
OpenFisca is a versatile microsimulation free software. This repository contains the OpenFisca model of the French tax and benefit system. Therefore, the working language here is French. You can however check the [general OpenFisca documentation](http://openfisca.org/doc/) in English!
> We host a public instance of of the [OpenFisca-France Web API](https://fr.openfisca.org/api/v18/). Learn more about its endpoint in the [Swagger documentation](https://fr.openfisca.org/legislation/swagger).
> If you need to run large amount of calculations, or add extensions, you should [host your own instance](#servez-openfisca-france-avec-l-api-web-openfisca).

## [FR] Introduction
[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation du système social et fiscal français. Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](http://openfisca.org/doc/).
> Nous mettons à disposition une instance publique de [l'API Web OpenFisca-France](https://fr.openfisca.org/api/v18/). Découvrez ses capacité sur sa [documentation Swagger](https://fr.openfisca.org/legislation/swagger).
> Si vous avez besoin de réaliser un grand nombre de calculs ou d'ajouter des extensions, vous pouvez [servir votre propre instance](#servez-openfisca-france-avec-l-api-web-openfisca).

## API Web publique : interrogez OpenFisca-France sans installation

OpenFisca met à disposition une [API Web publique](http://openfisca.org/doc/openfisca-web-api/endpoints.html) qui ne demande aucune installation.
Utilisez l'API publique si vous souhaitez :
- accéder à un paramètre (Ex : [le montant du SMIC horaire brut](https://fr.openfisca.org/api/v18/parameter/cotsoc.gen.smic_h_b)) ;
- consulter une formule de calcul (Ex : [le calcul de l'allocation de base des allocations familiales](https://fr.openfisca.org/api/v18/variable/af_base)) ;
- faire des calculs sur une situation (Ex : le calcul du coût du travail).

L'ensembles des endpoints sont décrits dans la [documentation Swagger](https://fr.openfisca.org/legislation/swagger).

[L'explorateur de législation](https://legislation.openfisca.fr/) contient la liste des paramètres et variables disponibles.

## Installation

Ce paquet requiert [Python 2.7](https://www.python.org/downloads/) et [pip](https://pip.pypa.io/en/stable/installing/).

Plateformes supportées :
- distributions GNU/Linux (en particulier Debian and Ubuntu) ;
- Mac OS X ;
- Windows (nous recommandons d'utiliser [ConEmu](https://conemu.github.io/) à la place de la console par défaut) ;

Pour les autres OS : si vous pouvez exécuter Python et Numpy, l'installation d'OpenFisca devrait fonctionner.

### Installez un environnement virtuel avec Pew

Nous recommandons l'utilisation d'un [environnement virtuel](https://virtualenv.pypa.io/en/stable/) (_virtualenv_) avec un gestionnaire de _virtualenv_ tel que [Pew](https://github.com/berdario/pew).

- Un _[virtualenv](https://virtualenv.pypa.io/en/stable/)_ crée un environnement pour les besoins spécifiques du projet sur lequel vous travaillez.
- Un gestionnaire de _virtualenv_, tel que [Pew](https://github.com/berdario/pew), vous permet de facilement créer, supprimer et naviguer entre différents projets.

Pour installer Pew, lancez une fenêtre de terminal et suivez ces instructions :

```sh
python --version # Python 2.7.9 ou plus récent devrait être installé sur votre ordinateur.
# Si non, téléchargez-le sur http://www.python.org et téléchargez pip.
```

```sh
pip install --upgrade pip
pip install pew
```
Créez un nouveau _virtualenv_ nommé **openfisca** et configurez-le avec python2.7 :

```sh
pew new openfisca --python=python2.7
# Si demandé, répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```
Le  _virtualenv_  **openfisca** sera alors activé, c'est-à-dire que les commandes suivantes s'exécuteront directement dans l'environnement virtuel. Vous verrez dans votre terminal :

```sh
Installing setuptools, pip, wheel...done.
Launching subshell in virtual environment. Type 'exit' or 'Ctrl+D' to return.
```

Informations complémentaires :
- sortez du _virtualenv_ en tapant `exit` (or Ctrl-D) ;
- re-rentrez en tapant `pew workon openfisca` dans votre terminal.

Bravo :tada: Vous êtes prêt·e à installer OpenFisca-France !

Nous proposons deux procédures d'installation. Choisissez l'installation A ou B ci-dessous en fonction de l'usage que vous souhaitez faire d'OpenFisca-France.

### A. Installation minimale (pip install)

Suivez cette installation si vous souhaitez :
- procéder à des calculs sur une large population ;
- créer des simulations fiscales ;
- écrire une extension au-dessus de la législation française (exemple : les extensions de [Paris](https://github.com/sgmap/openfisca-paris) et [Rennes](https://github.com/sgmap/openfisca-rennesmetropole) ;
- servir OpenFisca-France avec l'API Web OpenFisca.

Pour pouvoir modifier OpenFisca-France, consultez l'[Installation avancée](#b-installation-avancée-git-clone).

#### Installer OpenFisca-France avec pip install

Dans votre _virtualenv_, vérifiez les pré-requis :

```sh
python --version  # Devrait afficher "Python 2.7.xx".
#Si non, vérifiez que vous passez --python=python2.7 lors de la création de votre environnement virtuel.
```

```sh
pip --version  # Devrait afficher au moins 9.0.x
#Si non, exécutez "pip install --upgrade pip".
```
Installez OpenFisca-France :

```sh
pip install openfisca-france
```
Félicitations :tada: OpenFisca-France est prêt à être utilisé !

#### Prochaines étapes

- Apprenez à utiliser OpenFisca avec nos [tutoriels](http://openfisca.org/doc/) (en anglais).
- Hébergez et servez votre instance d'OpenFisca-France avec l'[API Web OpenFisca](#servez-openfisca-france-avec-lapi-web-openfisca).

En fonction de vos projets, vous pourriez bénéficier de l'installation des paquets suivants dans votre _virtualenv_ :
- pour installer une extension ou écrire une législation au-dessus d'OpenFisca-France, consultez la [documentation sur les extensions](http://openfisca.org/doc/contribute/extensions.html) (en anglais) ;
- pour représenter graphiquement vos résultats, essayez la bibliothèque [matplotlib](http://matplotlib.org/) ;
- pour gérer vos données, découvrez la bibliothèque [pandas](http://pandas.pydata.org/).

### B. Installation avancée (Git Clone)

Suivez cette installation si vous souhaitez :
- enrichir ou modifier la législation d'OpenFisca-France ;
- contribuer au code source d'OpenFisca-France.

#### Cloner OpenFisca-France avec Git

Premièrement, assurez-vous que [Git](https://www.git-scm.com/) est bien installé sur votre machine.

Dans votre _virtualenv_, assurez-vous que vous êtes dans le répertoire où vous souhaitez cloner OpenFisca-France.

Vérifiez les pré-requis :

```sh
python --version  # Devrait afficher "Python 2.7.xx".
#Si non, vérifiez que vous passez --python=python2.7 lors de la création de votre environnement virtuel.
```

```sh
pip --version  # Devrait afficher au moins 9.0.
#Si non, exécutez "pip install --upgrade pip".
```

Clonez OpenFisca-France sur votre machine :

```sh
git clone https://github.com/openfisca/openfisca-france.git
cd openfisca-france
pip install -e .
```

Vous pouvez vous assurer que votre installation s'est bien passée en exécutant :

```sh
pip install -e ".[test]"
nosetests tests/test_basics.py # Ces test peuvent prendre jusqu'à 60 secondes.
```
:tada: OpenFisca-France est prêt à être utilisé !

#### Prochaines étapes

- Pour enrichir ou faire évoluer la législation d'OpenFisca-France, lisez _[Coding the Legislation](http://openfisca.org/doc/coding-the-legislation/index.html)_ (en anglais).
- Pour contribuer au code, lisez le _[Contribution Guidebook](http://openfisca.org/doc/contribute/index.html)_ (en anglais).

## Servez OpenFisca-France avec l'API Web OpenFisca

Il est possible de servir l'API Web d'OpenFisca-France sur votre propre serveur :

```sh
openfisca serve
```

Pour en savoir plus sur la commande `openfisca serve` et ses options, consultez la [documentation de référence](https://openfisca.readthedocs.io/en/latest/openfisca_serve.html).

Testez votre installation en requêtant la commande suivante :

```sh
curl "http://localhost:6000/parameter/cotsoc.gen.smic_h_b"
```
Vous devriez avoir le resultat suivant :
```JSON
{
  "description": "SMIC horaire brut",
  "id": "cotsoc.gen.smic_h_b",
  "values": {
    "2001-08-01": 6.67,
    "2002-07-01": 6.83,
    "2003-07-01": 7.19,
    "2004-07-01": 7.61,
    "2005-07-01": 8.03,
    "2006-07-01": 8.27,
    "2007-07-01": 8.44,
    "2008-05-01": 8.63,
    "2008-07-01": 8.71,
    "2009-07-01": 8.82,
    "2010-01-01": 8.86,
    "2011-01-01": 9.0,
    "2011-12-01": 9.19,
    "2012-01-01": 9.22,
    "2012-07-01": 9.4,
    "2013-01-01": 9.43,
    "2014-01-01": 9.53,
    "2015-01-01": 9.61,
    "2016-01-01": 9.67,
    "2017-01-01": 9.76
  }
}
```

:tada: Vous servez OpenFisca-France via l'API Web OpenFisca !

Pour en savoir plus, explorez [la documentation de l'API Web](https://fr.openfisca.org/legislation/swagger).

Vous pouvez activer le suivi des visites sur votre instance via Piwik avec _[le Tracker API OpenFisca](https://github.com/openfisca/tracker)_ (en anglais).

## Stratégie de versionnement

Le code d'OpenFisca-France est déployé de manière continue et automatique. Ainsi, à chaque fois que le code de la législation évolue sur la branche principale `master`, une nouvelle version est publiée.

De nouvelles versions sont donc publiées très régulièrement. Cependant, la différence entre deux versions consécutives étant réduite, les efforts d'adaptation pour passer de l'une à l'autre sont en général très limités.

Par ailleurs, OpenFisca-France respecte les règles du [versionnement sémantique](http://semver.org/). Tous les changements qui ne font pas l'objet d'une augmentation du numéro majeur de version sont donc garantis rétro-compatibles.

> Par exemple, si mon application utilise la version `13.1.1`, je sais qu'elle fonctionnera également avec la version `13.2.0`. En revanche, il est possible qu'une adaptation soit nécessaire sur mon client pour pouvoir utiliser la version `14.0.0`.

Enfin, les impacts et périmètres des évolutions sont tous documentés sur le [CHANGELOG](CHANGELOG.md) du package. Ce document permet aux contributeurs de suivre les évolutions et d'établir leur propre stratégie de mise à jour.

## Contributeurs

Voir la [liste des contributeurs](https://github.com/openfisca/openfisca-france/graphs/contributors).
