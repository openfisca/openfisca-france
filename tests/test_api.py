# -*- coding: utf-8 -*-

import subprocess
import requests
from unittest import TestCase
from nose.tools import assert_equal


class Test(TestCase):

    def setUp(self):
        self.process = subprocess.Popen("openfisca-serve")

    def tearDown(self):
        self.process.terminate()

    def test_response(self):
        assert_equal(
            requests.get("http://localhost:2000").status_code,
            200
            )
