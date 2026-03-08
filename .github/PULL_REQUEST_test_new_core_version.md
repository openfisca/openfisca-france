# Test hebdomadaire de compatibilité avec les nouvelles versions d'openfisca-core

## Contexte

Le déploiement de l'API via openfisca-ops installe toujours la dernière version disponible sur PyPI (`state: latest`). Si une nouvelle version majeure d'openfisca-core est publiée au-delà de la borne supérieure définie dans `pyproject.toml`, elle peut casser la compatibilité sans qu'on le sache avant un déploiement.

## Ce que cette PR ajoute

### `.github/get_latest_core_version.py`

Script Python qui :
- Interroge l'API PyPI pour obtenir la dernière version publiée d'openfisca-core
- La compare avec la borne supérieure définie dans `pyproject.toml` (actuellement `<45`)
- Expose des outputs GitHub Actions si une nouvelle version à tester est détectée

### `.github/workflows/test_new_core_version.yml`

Workflow GitHub Actions déclenché **chaque lundi à 8h UTC** (et manuellement via `workflow_dispatch`) avec 4 jobs :

```
check-new-version
      ↓ (si version > borne actuelle)
test-new-version
      ↙ échec                    ↘ succès
open-issue                    open-pr
(openfisca-france              (bump borne dans
+ openfisca-core)               pyproject.toml)
```

**`check-new-version`** — vérifie s'il existe une nouvelle version à tester.

**`test-new-version`** — patche temporairement `pyproject.toml`, reconstruit openfisca-france depuis les sources, force l'installation de la nouvelle version d'openfisca-core, puis exécute `.github/test-api.sh`.

**`open-issue-on-failure`** — en cas d'échec, ouvre un ticket sur openfisca-france (et optionnellement sur openfisca-core via un secret `CROSS_REPO_TOKEN`). La déduplication évite d'ouvrir plusieurs tickets pour la même version.

**`open-pr-on-success`** — en cas de succès, crée une PR qui met à jour la borne supérieure dans `pyproject.toml`.

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
