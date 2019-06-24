# -*- coding: utf-8 -*-

import datetime
from typing import List, Optional

import pytest


@pytest.fixture
def axes():
    def _axes(count: int, max: int, min: int, name: str) -> List[List[dict]]:
        return [[
            dict(
                count = 2,
                max = 18000,
                min = 0,
                name = 'salaire_imposable',
                ),
            ]]

    return _axes


@pytest.fixture
def parent1():
    def _parent1(year: int) -> dict:
        return dict(date_naissance = datetime.date(year - 40, 1, 1))

    return _parent1


@pytest.fixture
def parent2():
    def _parent2(year: int, people: int) -> Optional[dict]:
        if people >= 2:
            return dict(date_naissance = datetime.date(year - 40, 1, 1))

    return _parent2


@pytest.fixture
def enfants():
    def _enfants(year: int, people: int) -> List[dict]:
        return [
            dict(date_naissance = datetime.date(year - 9, 1, 1))
            for number in (3, 4)
            if people >= number
            ]

    return _enfants
