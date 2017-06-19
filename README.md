# OpenFisca-France

[![Build Status](https://travis-ci.org/openfisca/openfisca-france.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-france)

## [EN] Introduction
OpenFisca is a versatile microsimulation free software. This repository contains the OpenFisca model of the French tax and benefit system. Therefore, the working language here is French. You can however check the [general OpenFisca documentation](https://doc.openfisca.fr/) in English!

## [FR] Introduction
[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation du système social et fiscal français. Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](https://doc.openfisca.fr/).

## Legislation Explorer, un guide de l'API publique OpenFisca

OpenFisca France met à disposition une [API Web publique](https://api.openfisca.fr/api/1/swagger) qui ne demande aucune installation.
Utilisez l'API publique si vous souhaitez :
- accéder à un paramètre (Ex : [le montant du SMIC horaire brut](https://legislation.openfisca.fr/cotsoc.gen.smic_h_b)) ;
- consulter une formule de calcul (Ex : [le calcul de l'allocation de base des Allocations familiales](https://legislation.openfisca.fr/af_base) ;
- faire des calculs ponctuels sur une situation (Ex : le calcul une taxe d'habitation pour un ménage).

[L'explorateur de législation](https://legislation.openfisca.fr/) contient la liste des paramètres et variables disponibles.

## Installation

Ce paquet requiert Python 2.7.

Plateformes supportées :
- distribution GNU/Linux (en particulier Debian and Ubuntu) ;
- Mac OS X ;
- Windows (nous recommandons d'utiliser [ConEmu](https://conemu.github.io/) à la place de la console par défaut) ; 

Pour les autres OS : si vous pouvez exécuter Python et Numpy, l'installation d'OpenFisca devrait fonctionner.

### Installez un environnement virtuel avec Pew

Nous recommandons l'utilisation d'un [environnement virtuel](https://virtualenv.pypa.io/en/stable/) (abrévié en "_virtualenv_") avec un gestionnaire de _virtualenv_ tel que [pew](https://github.com/berdario/pew).

- Un _[virtualenv](https://virtualenv.pypa.io/en/stable/)_ créé un environnement pour les besoins spécifiques du projet sur lequel vous travaillez.
- Un gestionnaire de _virtualenv_, tel que [pew](https://github.com/berdario/pew), vous permet de facilement créer, supprimer et naviguer entre différents projets.

Pour installer Pew, lancez une fenêtre de terminal et suivez ces instructions : 

```sh
pip install --upgrade pip
pip install pew  # répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```
Créez un nouveau _virtualenv_ nommé **openfisca** et configurez-le avec python2.7 :

```sh
pew new openfisca --python=python2.7
```

Le  _virtualenv_  **openfisca** sera alors activé, c'est-à-dire que les commandes suivantes s'exécuteront directement dans l'environnement virtuel.

Informations complémentaires :
- sortez du _virtualenv_ en tapant `exit` (or Ctrl-D) ;
- re-rentrez en tapant `pew workon openfisca` dans votre terminal.

### Installation minimale (pip install)

Suivez cette installation si vous souhaitez :
- procéder à des calculs sur une large population ;
- créer des simulations fiscales ;
- écrire une extension au dessus de la législation française (exemple : les extensions de Paris et Rennes) ;
- servir OpenFisca-France avec l'API Web OpenFisca.

Pour pouvoir modifier OpenFisca-France, consultez l'[Installation avancée](#installation-avancée-git-clone).

#### Installer OpenFisca-France avec pip install

Dans votre _virtualenv_, vérifiez les pré-requis :

```sh
python --version  # Devrait afficher "Python 2.7.xx".
#Si non, vérifiez que vous passez --python=python2.7 lors de la création de votre environnement virtuel.
```

```sh
pip --version  # Devrait afficher au moins 9.0.
#Si non, exécutez "pip install --upgrade pip".
```
Installez OpenFisca-France :

```sh
pip install openfisca-france
```

#### Prochaines étapes

- Apprenez à utiliser OpenFisca avec nos [tutoriels](https://doc.openfisca.fr/getting-started.html) (en anglais).
- Hébergez et servez votre instance d'OpenFisca-France avec l'[API Web OpenFisca](#servez-openfisca-france-avec-lapi-web-openfisca).

En fonction de vos projets, vous pourriez bénéficier de l'installation des paquets suivants dans votre _virtualenv_ :
- pour installer une extension or écrire une législation au dessus d'OpenFisca France, consultez la [documentation sur les extensions](https://doc.openfisca.fr/contribute/extensions.html) (en anglais);
- pour représenter graphiquement vos résultats, essayez la librairie [matplotlib](http://matplotlib.org/) ;
- pour gérer vos données, découvrez la librairie [pandas](http://pandas.pydata.org/).

### Installation avancée (Git Clone)

Suivez cette installation si vous souhaitez :
- créer ou changer la législation d'OpenFisca-France ;
- contribuer au code source d'OpenFisca-France.
>***A propos d'OpenFisca-Core***: si vous avez besoin de modifier le code source d'OpenFisca-Core (exemple : vous souhaitez contribuer à une fonctionnalité concernant l'ensemble des _Country Packages_), suivez les instructions de la [section _Installation_ d'OpenFisca-Core](https://github.com/openfisca/openfisca-core#installation).

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
```
OpenFisca-France est prêt à être utilisé !

#### Prochaines étapes

- Pour écrire une nouvelle législation, lisez _[Coding the Legislation](https://doc.openfisca.fr/coding-the-legislation/index.html)_ (en anglais).
- Pour contribuer au code, lisez le _[Contribution Guidebook](https://doc.openfisca.fr/contribute/index.html)_ (en anglais).

## Servez OpenFisca-France avec l'API Web OpenFisca

Si vous développez une application web, vous pouvez brancher OpenFisca-France à l'API Web OpenFisca.

Pour ce faire, installez l'API Web OpenFisca :

- si vous avez installé OpenFisca-France avec pip install : 
    ```sh
    pip install openfisca-france[api]
    ```
- si vous avez installé OpenFisca-France avec git clone:

    ```sh
    pip install -e '.[api]'
    ```

Puis servez l'API Web OpenFisca localement :

```sh
openfisca-serve --port 2000
```

Testez votre installation en requêtant la commande suivante :

```sh
curl "http://localhost:2000/api/1/swagger"
```

Pour en savoir plus, explorez _[OpenFisca Web API documentation](https://doc.openfisca.fr/openfisca-web-api/index.html)_ (en anglais).

## Stratégie de versionnement

Le code d'OpenFisca-France est versionné de manière continue et automatique. Ainsi, à chaque fois que le code de la législation évolue sur la branche principale `master`, une nouvelle version est publiée.

De nouvelles versions sont donc publiées très régulièrement. Cependant, la différence entre deux versions consécutives étant réduite, les efforts d'adaptation pour passer de l'une à l'autre sont en général très limités.

Par ailleurs, OpenFisca-France respecte les règles du [versionnement sémantique](http://semver.org/). Tous les changements qui ne font pas l'objet d'une augmentation du numéro majeur de version sont donc garantis rétro-compatibles.

> Par exemple, si mon application utilise la version `13.1.1`, je sais qu'elle fonctionnera également avec la version `13.2.0`. En revanche, il est possible qu'une adaptation soit nécessaire sur mon client pour pouvoir utiliser la version `14.0.0`.

Enfin, les impacts et périmètres des évolutions sont tous documentés sur le [CHANGELOG](CHANGELOG.md) du package. Ce document permet aux contributeurs de suivre les évolutions et d'établir leur propre stratégie de mise à jour.

## Contributeurs

Voir la [liste des contributeurs](https://github.com/openfisca/openfisca-france/graphs/contributors).
