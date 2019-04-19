# -*- coding: utf-8 -*-

import subprocess

import pytest


@pytest.fixture()
def serve():
    process = subprocess.Popen(['openfisca', 'serve', '--country-package', 'openfisca_france'])
    yield "serve"
    process.terminate()


def test_response(serve):
    try:
        subprocess.check_call(['wget', '--quiet', '--retry-connrefused', '--waitretry=1', '--tries=10', 'http://localhost:5000/parameters', '--output-document=/dev/null'])
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Could not reach OpenFisca Web API at localhost:5000 after 10s")
    except OSError:
        try:
            subprocess.check_call(['wget', '--version'])
        except OSError:
            raise OSError("Check if 'wget'(https://www.gnu.org/software/wget/) is installed on your computer")
        raise
