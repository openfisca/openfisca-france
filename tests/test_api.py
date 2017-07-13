# -*- coding: utf-8 -*-

import subprocess
import time
from unittest import TestCase
from nose.tools import assert_equal


class Test(TestCase):

    def setUp(self):
        self.process = subprocess.Popen("openfisca-serve")

    def tearDown(self):
        self.process.terminate()

    def test_response(self):
        try:
            subprocess.check_call(['wget', '--quiet',  '--retry-connrefused', '--waitretry=1', '--tries=10', 'http://localhost:2000'])
        except subprocess.CalledProcessError:
            import nose.tools; nose.tools.set_trace(); import ipdb; ipdb.set_trace()
            raise subprocess.CalledProcessError("Could not reach OpenFisca Web API at localhost:2000 after 10s")
