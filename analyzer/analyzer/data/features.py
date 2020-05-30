#  This file is part of 'analyzer', the tool used to process the information
#  collected for Andrea Esposito's Thesis.
#  Copyright (C) 2020  Andrea Esposito
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import dataclasses
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclasses.dataclass
class Keyboard(Generic[T]):
    all: T = None
    alphabetic: T = None
    numeric: T = None
    symbol: T = None
    function: T = None
    alphanumeric: T = None

@dataclasses.dataclass
class VisitedWebsites:
    unique: int
    changed: int
    change_rate: float

@dataclasses.dataclass
class Clicks(Generic[T]):
    all: T = None
    left: T = None
    middle: T = None
    right: T = None
    other: T = None

@dataclasses.dataclass
class DirectionStatistics:
    changes: int
    change_rate: float

@dataclasses.dataclass
class BasicStats:
    sum: float
    avg: float
    std: float


@dataclasses.dataclass
class RateStats:
    rate: float
    total: float