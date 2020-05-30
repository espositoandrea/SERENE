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

from abc import ABCMeta, abstractmethod


class BaseObject(object, metaclass=ABCMeta):
    __slots__ = []

    @abstractmethod
    def to_dict(self):
        pass


class ScreenCoordinates(object):
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class ScrollData(object):
    __slots__ = ["absolute", "relative"]

    def __init__(self, absolute: ScreenCoordinates, relative: ScreenCoordinates):
        self.absolute: ScreenCoordinates = absolute
        self.relative: ScreenCoordinates = relative


class KeyboardData(object):
    __slots__ = ["any", "alpha", "numeric", "function", "symbol"]

    def __init__(self, any: bool, alpha: bool, numeric: bool, function: bool, symbol: bool):
        self.any: bool = any
        self.alpha: bool = alpha
        self.numeric: bool = numeric
        self.function: bool = function
        self.symbol: bool = symbol


class Speed2D(object):
    __slots__ = ["total", "x", "y"]

    def __init__(self, total: float, x: float, y: float):
        self.total: float = total
        self.x: float = x
        self.y: float = y


class MouseData(object):
    __slots__ = ["position", "clicks", "speed", "acceleration"]

    class Clicks(object):
        __slots__ = ["any", "left", "middle", "right", "others"]

        def __init__(self, any: bool, left: bool, middle: bool, right: bool, others: bool):
            self.any: bool = any
            self.left: bool = left
            self.middle: bool = middle
            self.right: bool = right
            self.others: bool = others

    def __init__(self, position: ScreenCoordinates, clicks: 'MouseData.Clicks', speed: Speed2D = None,
                 acceleration: Speed2D = None):
        self.position: ScreenCoordinates = position
        self.clicks: MouseData.Clicks = clicks
        self.speed: Speed2D = speed
        self.acceleration: Speed2D = acceleration
