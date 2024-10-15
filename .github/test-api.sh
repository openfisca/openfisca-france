#! /usr/bin/env bash

PORT=5000
ENDPOINT=spec

openfisca serve --country-package openfisca_france --port $PORT --workers 1 &
server_pid=$!

curl --retry-connrefused --retry 10 --retry-delay 5 --fail http://127.0.0.1:$PORT/$ENDPOINT | python -m json.tool > /dev/null
result=$?

kill $server_pid

exit $?
