# Consignes du dépôt

Ce fichier est destiné aux agents IA, en complément de `README.md`, `CONTRIBUTING.md`, `pyproject.toml` et `Makefile`.

## Structure du projet et organisation des modules
- `openfisca_france/` — package Python principal : formules, paramètres et scripts.
- `tests/` — tests unitaires et scénarios (Python et YAML).
- `pyproject.toml` — métadonnées du paquet et configuration des outils de développement.
- `Makefile` — cibles de développement courantes (`install`, `build`, `test`, `check-style`).
- `.github/` — workflows CI.

## Commandes de build, test et développement
- Installer les dépendances de développement : `uv run make install` (installation en mode editable + groupe dev).
- Construire le paquet : `uv run make build` (construire la wheel et l'installer pour les vérifications finales).
- Lancer l'ensemble des tests et vérifications : `uv run make test` (exécute les vérifications de syntaxe, de style, YAML et `openfisca test`).
- Exécuter les tests directement : `uv run openfisca test --country-package openfisca_france tests`.
- Vérifications de style : `uv run make check-style` ; formatage automatique : `uv run make format-style`.

## Style de code et conventions de nommage
- Indentation : 4 espaces. Respecter PEP8 lorsque applicable.
- Guillemets : préférer les apostrophes simples pour les docstrings et littéraux (configuré dans `pyproject.toml`).
- Linters/formatters : `flake8` et `autopep8` sont utilisés ; exécuter `make check-style` / `make format-style`.
- Nommage : `snake_case` pour fonctions/variables, `PascalCase` pour classes, les chemins de modules reflètent les zones du modèle (par ex. `prestations/minima_sociaux/cmu`).

## Consignes de tests
- Framework : `pytest` (appelé via le wrapper `openfisca test`). Les tests se trouvent dans `tests/`.
- Nommage : garder les tests sous `tests/` et utiliser des noms descriptifs `test_*.py` ; les scénarios YAML suivent la structure existante de `tests/`.
- Exécuter un test unique : `openfisca test --country-package openfisca_france tests/path/to/test.yaml`.

## Consignes de commit et de pull request
- Suivre CONTRIBUTING.md du dépôt et les règles du changelog pour les modifications fonctionnelles (les entrées du changelog sont en français).
- Commits : sujet court à l'impératif, référencer l'issue/PR concernée, ajouter un corps clair si nécessaire.
- PRs : inclure une description, l'issue liée, des tests couvrant les changements, et s'assurer que la CI est verte (`uv run make test`). Mettre à jour le CHANGELOG pour les changements de comportement.

## Conseils de sécurité et de configuration
- Ne jamais committer de secrets ou identifiants. Utiliser `.gitignore` pour les fichiers générés et les configurations locales.
- Si vous devez tester contre une branche non publiée de `openfisca-core`, suivre les instructions dans `CONTRIBUTING.md` et revenir en arrière avant de fusionner.


