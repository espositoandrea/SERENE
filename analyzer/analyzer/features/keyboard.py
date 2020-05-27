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
from typing import Generic, TypeVar, List

import numpy as np

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

    # all keys
    avg = keys.all / range_width
    std_dev = np.std([obj.keyboard.any for obj in interactions])
    all = BasicStats(keys.all, avg, std_dev)

    # alphabetic keys
    avg = keys.alphabetic / range_width
    std_dev = np.std([obj.keyboard.alpha for obj in interactions])
    alpha = BasicStats(keys.alphabetic, avg, std_dev)

    # numeric keys
    avg = keys.numeric / range_width
    std_dev = np.std([obj.keyboard.numeric for obj in interactions])
    numeric = BasicStats(keys.numeric, avg, std_dev)

    # symbol keys
    avg = keys.symbol / range_width
    std_dev = np.std([obj.keyboard.symbol for obj in interactions])
    symbol = BasicStats(keys.symbol, avg, std_dev)

    # function keys
    avg = keys.function / range_width
    std_dev = np.std([obj.keyboard.function for obj in interactions])
    function = BasicStats(keys.function, avg, std_dev)

    # alphanumeric keys
    avg = keys.alphanumeric / range_width
    std_dev = np.std([obj.keyboard.alpha or obj.keyboard.numeric for obj in interactions])
    alphanum = BasicStats(keys.alphanumeric, avg, std_dev)

    return Keyboard(
        all=all,
        alphabetic=alpha,
        numeric=numeric,
        symbol=symbol,
        function=function,
        alphanumeric=alphanum
    )
