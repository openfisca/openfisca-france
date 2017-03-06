# Contribuer à OpenFisca-France

Avant tout, merci de votre volonté de contribuer au bien commun qu'est OpenFisca ! 

Afin de faciliter la réutilisation d'OpenFisca et d'améliorer la qualité du code, les contributions à OpenFisca suivent certaines règles.

Certaines règles sont communes à tous les dépôts OpenFisca et sont détaillées dans [la documentation générale](https://doc.openfisca.fr/contribute/guidelines.html).


## Format du Changelog

Les évolutions d'OpenFisca-France doivent pouvoir être comprises par des réutilisateurs qui n'interviennent pas nécessairement sur le code. Le Changelog, rédigé en français, se doit donc d'être le plus explicite possible. 

Chaque évolution sera documentée par les élements suivants :

- Sur la première ligne figure en guise de titre le numéro de version, et un lien vers la Pull Request introduisant le changement. Le niveau de titre doit correspondre au niveau d'incrémentation de la version.

> Par exemple :
> # 13.0.0 - [#671](https://github.com/openfisca/openfisca-france/pull/671)
> 
> ## 13.2.0 - [#676](https://github.com/openfisca/openfisca-france/pull/676)
> 
> ### 13.1.5 - [#684](https://github.com/openfisca/openfisca-france/pull/684)

- La deuxième ligne indique de quel type de changement il s'agit. Les types possibles sont :
  - `Évolution du système socio-fiscal`: Amélioration, correction, mise à jour d'un calcul. Impacte les réutilisateurs intéressés par les calculs.
  - `Amélioration technique`: Amélioration des performances, évolution de la procédure d'installation, de la syntaxe des formules… Impacte les réutilisateurs rédigeant des règles et/ou déployant leur propre instance.
  - `Correction d'un crash`: Impacte tous les réutilisateurs.
  - `Changement mineur`: Refactoring, métadonnées… N'a aucun impact sur les réutilisateurs.
    
- Dans le cas d'une `Évolution du système socio-fiscal`, il est ensuite précisé les périodes concernées par l'évolution, ainsi que les zones du modèle de calcul impactées. Ces zones correspondent à l'arborescence des fichiers dans le modèle.

> Par exemple :
> - Périodes concernées : Jusqu'au 31/12/2015.
> - Zones impactées : `prestations/minima_sociaux/cmu`

- Enfin, dans tous les cas hors `Changement mineur`, les corrections apportées doivent être explicitées de détails donnés d'un point de vue fonctionnel : dans quel cas d'usage constatait-on un erreur / un problème ? Quelle nouvelle fonctionalité est disponible ? Quel nouveau comportement est adopté ?

> Par exemple:
>
> * Détails :
>   - Ces variables renvoient désormais un montant annuel et non mensuel :
>     - `acs`
>     - `bourse_college`
>     - `bourse_lycee`
>   - _Les valeurs mensuelles précédentes étaient obtenues par une division par 12 et non par un calcul réel._
>
> Ou :
>
> * Détails :
>   - Déplacement du test runner depuis `france` vers `core`.
>   - _Il devient possible d'exécuter `openfisca-run-test` sur un fichier YAML. [Plus d'informations](http://openfisca.readthedocs.io/en/latest/openfisca-run-test.html)._

Dans le cas où une Pull Request contient plusieurs évolutions distinctes, plusieurs paragraphes peuvent être ajoutés au Changelog.
