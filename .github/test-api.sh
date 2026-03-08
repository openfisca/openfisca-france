#! /usr/bin/env bash

PORT=5000

openfisca serve --country-package openfisca_france --port $PORT --workers 1 &
server_pid=$!

# Test 1 : vérifier que l'API démarre et retourne sa spec
curl --retry-connrefused --retry 10 --retry-delay 5 --fail http://127.0.0.1:$PORT/spec | python -m json.tool > /dev/null
result=$?

if [ $result -ne 0 ]; then
  kill $server_pid
  exit $result
fi

# Test 2 : calculer le revenu_disponible d'un célibataire salarié sur l'année N-1
# L'objectif est de vérifier que l'API ne plante pas suite à une incompatibilité avec openfisca-core,
# pas de valider les montants (c'est le rôle des tests YAML).
python - << EOF
import json
import sys
import urllib.request
from datetime import date

YEAR = date.today().year - 1  # N-1 pour s'assurer que les paramètres de législation existent
SALAIRE = 2000
PORT = $PORT

months = {f"{YEAR}-{m:02d}": SALAIRE for m in range(1, 13)}
cout_du_travail_months = {f"{YEAR}-{m:02d}": None for m in range(1, 13)}

payload = {
    "individus": {
        "individu_1": {
            "salaire_de_base": months,
            "revenus_nets_du_travail": {str(YEAR): None},
            "cout_du_travail": cout_du_travail_months,
        }
    },
    "foyers_fiscaux": {
        "foyer_fiscal_1": {"declarants": ["individu_1"]}
    },
    "familles": {
        "famille_1": {
            "parents": ["individu_1"],
            "prestations_sociales": {str(YEAR): None},
        }
    },
    "menages": {
        "menage_1": {
            "personne_de_reference": ["individu_1"],
            "revenu_disponible": {str(YEAR): None},
            "impots_directs": {str(YEAR): None},
        }
    }
}

req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/calculate",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
except Exception as e:
    print(f"ERREUR appel /calculate : {e}", file=sys.stderr)
    sys.exit(1)

if "error" in result:
    print(f"ERREUR retournée par l'API : {result['error']}", file=sys.stderr)
    sys.exit(1)

# Extraction des valeurs
individu = result["individus"]["individu_1"]
famille = result["familles"]["famille_1"]
menage = result["menages"]["menage_1"]

revenu_disponible    = menage["revenu_disponible"][str(YEAR)]
impots_directs       = menage["impots_directs"][str(YEAR)]
revenus_nets_travail = individu["revenus_nets_du_travail"][str(YEAR)]
prestations_sociales = famille["prestations_sociales"][str(YEAR)]
cout_du_travail_jan  = individu["cout_du_travail"][f"{YEAR}-01"]
salaire_annuel_brut  = SALAIRE * 12

errors = []

# Les valeurs sont-elles des nombres ?
for name, val in [
    ("revenu_disponible", revenu_disponible),
    ("impots_directs", impots_directs),
    ("revenus_nets_du_travail", revenus_nets_travail),
    ("prestations_sociales", prestations_sociales),
    ("cout_du_travail", cout_du_travail_jan),
]:
    if not isinstance(val, (int, float)):
        errors.append(f"{name} n'est pas un nombre : {val}")

if not errors:
    # Le coût du travail dépasse le salaire brut (il inclut les charges patronales)
    if cout_du_travail_jan <= SALAIRE:
        errors.append(f"cout_du_travail={cout_du_travail_jan:.2f} devrait être > salaire_de_base={SALAIRE}")

    # Le net est inférieur au brut (les charges salariales existent)
    if not (0 < revenus_nets_travail < salaire_annuel_brut):
        errors.append(f"revenus_nets_du_travail={revenus_nets_travail:.2f} devrait être entre 0 et {salaire_annuel_brut}")

    # revenu_disponible = revenus_nets_du_travail + impots_directs + prestations_sociales
    #                   + pensions_nettes(=0) + ppe(=0) + revenus_nets_du_capital(=0)
    expected = revenus_nets_travail + impots_directs + prestations_sociales
    if abs(revenu_disponible - expected) > 1:
        errors.append(
            f"revenu_disponible={revenu_disponible:.2f} != "
            f"revenus_nets_du_travail({revenus_nets_travail:.2f}) "
            f"+ impots_directs({impots_directs:.2f}) "
            f"+ prestations_sociales({prestations_sociales:.2f}) "
            f"= {expected:.2f}"
        )

if errors:
    for e in errors:
        print(f"ECHEC : {e}", file=sys.stderr)
    sys.exit(1)

print(
    f"OK : revenu_disponible={revenu_disponible:.2f}€ "
    f"(net_travail={revenus_nets_travail:.2f}€ + prestations={prestations_sociales:.2f}€ + impots={impots_directs:.2f}€) "
    f"pour un salarié à {SALAIRE}€/mois brut en {YEAR}"
)
sys.exit(0)
EOF

result=$?
kill $server_pid
exit $result
