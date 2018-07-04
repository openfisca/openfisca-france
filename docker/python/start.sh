#!/bin/sh

openfisca serve \
--log-level debug \
--bind '0.0.0.0:6000' \
--workers 4 \
--timeout 6000 \
--log-file=- \
--worker-tmp-dir /mem \
--preload \
--country-package openfisca_france
