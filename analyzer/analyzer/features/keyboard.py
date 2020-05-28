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
import statistics
from typing import Generic, TypeVar, List

from .base import BasicStats
from ..data import Interaction

T = TypeVar('T')


@dataclasses.dataclass
class Keyboard(Generic[T]):
    all: T = None
    alphabetic: T = None
    numeric: T = None
    symbol: T = None
    function: T = None
    alphanumeric: T = None


def number_of_keys(interactions: List[Interaction]) -> Keyboard[int]:
    n_all = 0
    n_alphabetic = 0
    n_numeric = 0
    n_symbol = 0
    n_function = 0
    for obj in interactions:
        if not obj.keyboard.any:
            continue
        n_all += 1
        if obj.keyboard.alpha:
            n_alphabetic += 1
        if obj.keyboard.numeric:
            n_numeric += 1
        if obj.keyboard.symbol:
            n_symbol += 1
        if obj.keyboard.function:
            n_function += 1

    return Keyboard(
        all=n_all,
        alphabetic=n_alphabetic,
        numeric=n_numeric,
        symbol=n_symbol,
        function=n_function,
        alphanumeric=n_alphabetic + n_numeric
    )


def keyboard_statistics(interactions: List[Interaction], range_width: int) -> Keyboard[BasicStats]:
    keys = number_of_keys(interactions)

    if not interactions:
        no_keys = BasicStats(0, 0, 0)
        return Keyboard(no_keys, no_keys, no_keys, no_keys, no_keys, no_keys)
    elif len(interactions) == 1:
        all = BasicStats(keys.all, keys.all, 0)
        alpha = BasicStats(keys.alphabetic, keys.alphabetic, 0)
        numeric = BasicStats(keys.numeric, keys.numeric, 0)
        symbol = BasicStats(keys.symbol, keys.symbol, 0)
        function = BasicStats(keys.function, keys.function, 0)
        alphanum = BasicStats(keys.alphanumeric, keys.alphanumeric, 0)
        return Keyboard(
            all=all,
            alphabetic=alpha,
            numeric=numeric,
            symbol=symbol,
            function=function,
            alphanumeric=alphanum
        )

    # all keys
    avg = keys.all / range_width
    std_dev = sum([(int(obj.keyboard.any) - avg) ** 2 for obj in interactions]) / len(interactions)
    all = BasicStats(keys.all, avg, std_dev)

    # alphabetic keys
    avg = keys.alphabetic / range_width
    std_dev = sum([(int(obj.keyboard.alpha) - avg) ** 2 for obj in interactions]) / len(interactions)
    alpha = BasicStats(keys.alphabetic, avg, std_dev)

    # numeric keys
    avg = keys.numeric / range_width
    std_dev = sum([(int(obj.keyboard.numeric) - avg) ** 2 for obj in interactions]) / len(interactions)
    numeric = BasicStats(keys.numeric, avg, std_dev)

    # symbol keys
    avg = keys.symbol / range_width
    std_dev = sum([(int(obj.keyboard.symbol) - avg) ** 2 for obj in interactions]) / len(interactions)
    symbol = BasicStats(keys.symbol, avg, std_dev)

    # function keys
    avg = keys.function / range_width
    std_dev = sum([(int(obj.keyboard.function) - avg) ** 2 for obj in interactions]) / len(interactions)
    function = BasicStats(keys.function, avg, std_dev)

    # alphanumeric keys
    avg = keys.alphanumeric / range_width
    std_dev = sum([(int(obj.keyboard.alpha or obj.keyboard.numeric) - avg) ** 2 for obj in interactions]) / len(
        interactions)
    alphanum = BasicStats(keys.alphanumeric, avg, std_dev)

    return Keyboard(
        all=all,
        alphabetic=alpha,
        numeric=numeric,
        symbol=symbol,
        function=function,
        alphanumeric=alphanum
    )
