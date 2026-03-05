import os
import re

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

# Resolve pyproject.toml relative to repo root (parent of .github/), so this works in CI regardless of cwd
_script_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_script_dir)
_pyproject_path = os.path.join(_repo_root, "pyproject.toml")

# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing
with open(_pyproject_path, "rb") as file:
    config = tomllib.load(file)
    deps = config["project"]["dependencies"]
    printed = False
    for dep in deps:
        d = dep.strip() if isinstance(dep, str) else str(dep).strip()
        # Local path: pass through as-is for pip install
        if "openfisca-core" in d and "file:" in d:
            print(d)  # noqa: T201
            printed = True
            break
        # Git URL (e.g. from a PR branch): pass through as-is for pip install
        if "openfisca-core" in d and " @" in d:
            print(d)  # noqa: T201
            printed = True
            break
        version = re.search(r"openfisca-core\[([^\]]+)\]\s*>=\s*([\d\.]*)", d)
        if version:
            print(f"openfisca-core[{version[1]}]=={version[2]}")  # noqa: T201
            printed = True
            break
    if not printed:
        # Fallback: any openfisca-core dep (e.g. plain package name)
        for dep in deps:
            d = dep.strip() if isinstance(dep, str) else str(dep).strip()
            if "openfisca-core" in d:
                print(d)  # noqa: T201
                printed = True
                break
        if not printed:
            import sys
            print("get_minimal_version.py: no openfisca-core dependency found in pyproject.toml", file=sys.stderr)
            sys.exit(1)
