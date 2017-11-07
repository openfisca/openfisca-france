# OpenFisca-France

[![Build Status](https://travis-ci.org/openfisca/openfisca-france.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-france)

## [EN] Introduction
OpenFisca is a versatile microsimulation free software. This repository contains the OpenFisca model of the French tax and benefit system. Therefore, the working language here is French. You can however check the [general OpenFisca documentation](https://doc.openfisca.fr/) in English !

## [FR] Introduction
[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation du système social et fiscal français. Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](https://doc.openfisca.fr/).

## Stratégie de versionnement

Le code d'Openfisca-France est versionné de manière continue et automatique. Ainsi, à chaque fois que le code de la législation évolue sur la branche principale `master`, une nouvelle version est publiée.

De nouvelles versions sont donc publiées très régulièrement. Cependant, la différence entre deux versions consécutives étant réduite, les efforts d'adaptation pour passer de l'une à l'autre sont en général très limités.

Par ailleurs, OpenFisca-France respecte les règles du [versionnement sémantique](http://semver.org/). Tous les changements qui ne font pas l'objet d'une augmentation du numéro majeur de version sont donc garantis rétro-compatibles.
 
> Par exemple, si mon application utilise la version `13.1.1`, je sais qu'elle fonctionnera également avec la version `13.2.0`. En revanche, il est possible qu'une adaptation soit nécessaire sur mon client pour pouvoir utiliser la version `14.0.0`.

Enfin, les impacts et périmètres des évolutions sont tous documentés sur le [CHANGELOG](CHANGELOG.md) du package. Ce document permet aux contributeurs de suivre les évolutions et d'établir leur propre stratégie de mise à jour.

## Contributeurs

Voir la [liste des contributeurs](https://github.com/openfisca/openfisca-france/graphs/contributors).
