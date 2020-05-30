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

from typing import Generic, TypeVar

T = TypeVar('T')


class Keyboard(Generic[T], object):
    __slots__ = [
        "all",
        "alphabetic",
        "numeric",
        "symbol",
        "function",
        "alphanumeric"
    ]

    def __init__(self, all: T = None, alphabetic: T = None, numeric: T = None, symbol: T = None, function: T = None,
                 alphanumeric: T = None):
        self.all: T = all
        self.alphabetic: T = alphabetic
        self.numeric: T = numeric
        self.symbol: T = symbol
        self.function: T = function
        self.alphanumeric: T = alphanumeric

    def __str__(self):
        return "Keyboard(all={}, alphabetic={}, numeric={}, symbol={}, function={}, alphanumeric={})".format(
            self.all, self.alphabetic, self.numeric, self.symbol, self.function,
            self.alphanumeric
        )

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)


class VisitedWebsites(object):
    __slots__ = ["unique", "changed", "change_rate", ]

    def __init__(self, unique: int, changed: int, change_rate: int):
        self.unique: int = unique
        self.changed: int = changed
        self.change_rate: float = change_rate

    def __str__(self):
        return "VisitedWebsites(unique={}, changed={}, change_rate={})".format(
            self.unique, self.changed, self.change_rate
        )

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)


class Clicks(Generic[T], object):
    __slots__ = ["all", "left", "middle", "right", "other"]

    def __init__(self, all: T = None, left: T = None, middle: T = None, right: T = None, other: T = None):
        self.all: T = all
        self.left: T = left
        self.middle: T = middle
        self.right: T = right
        self.other: T = other

    def __str__(self):
        return "Clicks(all={}, left={}, middle={}, right={}, other={})".format(
            self.all, self.left, self.middle, self.right, self.other
        )

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)


class DirectionStatistics(object):
    __slots__ = ["changes", "change_rate"]

    def __init__(self, changes: int, change_rate: float):
        self.changes: int = changes
        self.change_rate: float = change_rate

    def __str__(self):
        return "DirectionStatistics(changes={}, change_rate={})".format(
            self.changes, self.change_rate
        )

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)


class BasicStats(object):
    __slots__ = ["sum", "avg", "std"]

    def __init__(self, sum: float, avg: float, std: float):
        self.sum: float = sum
        self.avg: float = avg
        self.std: float = std

    def __str__(self):
        return "BasicStats(sum={}, avg={}, std={})".format(self.sum, self.avg, self.std)

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)


class RateStats(object):
    __slots__ = ["rate", "total"]

    def __init__(self, rate: float, total: float):
        self.rate: float = rate
        self.total: float = total

    def __str__(self):
        return "RateStats(rate={}, total={})".format(self.rate, self.total)

    def __iter__(self):
        for k in self.__slots__:
            yield k, self.__getattribute__(k)
