#! /usr/bin/env bash

PORT=5000

openfisca serve --country-package openfisca_france --port $PORT --workers 1 &
server_pid=$!

# Test 1 : vérifier que l'API démarre et retourne sa spec
sleep 5
curl --retry-connrefused --retry 3 --retry-delay 5 --fail http://127.0.0.1:$PORT/spec | python -m json.tool > /dev/null
result=$?

if [ $result -ne 0 ]; then
  kill $server_pid
  exit $result
fi

# Test 2 : calculer le revenu_disponible d'un célibataire salarié sur l'année N-1
# L'objectif est de vérifier que l'API ne plante pas suite à une incompatibilité avec openfisca-core,
# pas de valider les montants (c'est le rôle des tests YAML).
python "$(dirname "$0")/test-api.py" $PORT

result=$?
kill $server_pid
exit $result
