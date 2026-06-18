# Test quotidien de compatibilité avec les nouvelles versions d'openfisca-core

## Contexte

Le déploiement de l'API via openfisca-ops installe toujours la dernière version disponible sur PyPI (`state: latest`). Une nouvelle version d'openfisca-core — mineure ou majeure — peut casser la compatibilité sans qu'on le sache avant un déploiement.

## Ce que cette PR ajoute

### `.github/test-api.sh` (modifié)

Enrichi avec un test fonctionnel en plus du test de démarrage existant :
- Calcule `revenu_disponible`, `cout_du_travail`, `revenus_nets_du_travail`, `prestations_sociales` et `impots_directs` pour un célibataire salarié à 2000€/mois brut sur l'année **N-1** (dynamique)
- Vérifie la cohérence : `revenu_disponible = revenus_nets_du_travail + impots_directs + prestations_sociales`
- L'objectif est de détecter un plantage lié à une incompatibilité avec openfisca-core, pas de valider les montants (c'est le rôle des tests YAML)

### `.github/get_latest_core_version.py` (nouveau)

Script Python qui :
- Interroge l'API PyPI pour obtenir la dernière version publiée d'openfisca-core
- Compare avec les deux bornes de `pyproject.toml` (`>=min, <max`)
- Détecte deux cas : **mineure** (nouvelle version dans les bornes) ou **majeure** (au-delà de la borne supérieure)
- La borne minimale sert de marqueur de "dernière version testée" : on ne reteste que quand une vraie nouveauté sort

### `.github/workflows/test_new_core_version.yml` (nouveau)

Workflow déclenché **chaque jour à 5h heure de Paris** (et manuellement via `workflow_dispatch`) :

```
check-new-version  (latest > borne min ?)
        ↓ oui
test-new-version   (make build + force install + test-api.sh)
    ↙ échec                        ↘ succès
open-issue                      open-pr
(france + core)            minor → bump borne min (>=44.2.2, <45)
                           major → bump borne max (>=43, <46)
```

**`open-issue-on-failure`** — déduplication : vérifie qu'un ticket pour cette version n'existe pas déjà avant d'en ouvrir un.

## Secrets requis

| Secret | Requis | Usage |
|--------|--------|-------|
| `GITHUB_TOKEN` | ✅ automatique | Ouvrir tickets et PRs sur openfisca-france |
| `CROSS_REPO_TOKEN` | ⚠️ optionnel | Ouvrir tickets sur openfisca-core (PAT avec `issues: write`) |

## Comment tester cette PR

### En local

```bash
uv pip install requests packaging --python .venv/bin/python
.venv/bin/python .github/get_latest_core_version.py
```

### Dans la CI

La branche contient un commit temporaire qui abaisse la borne à `<44` pour forcer le déclenchement de toute la chaîne de jobs :

1. Pousser la branche
2. GitHub → Actions → "Test compatibilité nouvelle version openfisca-core" → **Run workflow**
3. Vérifier que les 4 jobs s'enchaînent : `check-new-version` → `test-new-version` → `open-issue` ou `open-pr`

⚠️ **Avant de merger** : supprimer le commit temporaire avec `git revert HEAD`.
