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


@dataclasses.dataclass
class ScreenCoordinates:
    x: int
    y: int


@dataclasses.dataclass()
class ScrollData:
    absolute: ScreenCoordinates
    relative: ScreenCoordinates


@dataclasses.dataclass
class KeyboardData:
    any: bool
    alpha: bool
    numeric: bool
    function: bool
    symbol: bool


@dataclasses.dataclass
class Speed2D:
    total: float
    x: float
    y: float


@dataclasses.dataclass
class MouseData:
    @dataclasses.dataclass
    class Clicks:
        any: bool
        left: bool
        middle: bool
        right: bool
        others: bool

    position: ScreenCoordinates
    clicks: Clicks
    speed: Speed2D = None
    acceleration: Speed2D = None
