# -*- coding: utf-8 -*-

import datetime
from typing import Callable, List, Optional

import pytest

from openfisca_core import periods
from openfisca_core.reforms import Reform
from openfisca_france.scenarios import init_single_entity


@pytest.fixture
def new_scenario(axes, parent1, parent2, enfants) -> Callable[..., object]:
    def _scenario(
            reform: Reform,
            count: int,
            _max: int,
            _min: int,
            name: str,
            year: int,
            people: int
            ) -> object:

        return init_single_entity(
            reform.new_scenario(),
            axes = axes(count, _max, _min, name),
            period = periods.period(year),
            parent1 = parent1(year),
            parent2 = parent2(year, people),
            enfants = enfants(year, people),
            )

    return _scenario


@pytest.fixture
def axes() -> Callable[..., List[List[dict]]]:
    def _axes(count: int, _max: int, _min: int, name: str) -> List[List[dict]]:
        return [[
            dict(
                count = count,
                max = _max,
                min = _min,
                name = name,
                ),
            ]]

    return _axes


@pytest.fixture
def parent1() -> Callable[..., dict]:
    def _parent1(year: int) -> dict:
        return dict(date_naissance = datetime.date(year - 40, 1, 1))

    return _parent1


@pytest.fixture
def parent2() -> Callable[..., Optional[dict]]:
    def _parent2(year: int, people: int) -> Optional[dict]:
        if people >= 2:
            return dict(date_naissance = datetime.date(year - 40, 1, 1))

    return _parent2


@pytest.fixture
def enfants() -> Callable[..., List[dict]]:
    def _enfants(year: int, people: int) -> List[dict]:
        return [
            dict(date_naissance = datetime.date(year - 9, 1, 1))
            for number in (3, 4)
            if people >= number
            ]

    return _enfants
