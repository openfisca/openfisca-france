# -*- coding: utf-8 -*-

import subprocess
import time
from unittest import TestCase
from nose.tools import assert_equal


class TestOldApi(TestCase):

    def setUp(self):
        self.process = subprocess.Popen("openfisca-serve")

    def tearDown(self):
        self.process.terminate()

    def test_response(self):
        try:
            subprocess.check_call(['wget', '--quiet',  '--retry-connrefused', '--waitretry=1', '--tries=10', 'http://localhost:2000', '--output-document=/dev/null'])
        except subprocess.CalledProcessError:
            raise subprocess.CalledProcessError("Could not reach OpenFisca Web API at localhost:2000 after 10s")


class TestNewApi(TestCase):

    def setUp(self):
        self.process = subprocess.Popen(['openfisca', 'serve'])

    def tearDown(self):
        self.process.terminate()

    def test_response(self):
        try:
            subprocess.check_call(['wget', '--quiet',  '--retry-connrefused', '--waitretry=1', '--tries=10', 'http://localhost:6000/parameters', '--output-document=/dev/null'])
        except subprocess.CalledProcessError:
            raise subprocess.CalledProcessError("Could not reach OpenFisca Web API at localhost:6000 after 10s")
        except OSError:
            try:
                subprocess.check_call(['wget', '--version'])
            except OSError:
                raise OSError("Check if 'wget'(https://www.gnu.org/software/wget/) is installed on your computer")
