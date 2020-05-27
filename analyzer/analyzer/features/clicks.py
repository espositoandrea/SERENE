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
from typing import List, Generic, TypeVar

import numpy as np

from .base import BasicStats
from ..data import Interaction

T = TypeVar('T')


@dataclasses.dataclass
class Clicks(Generic[T]):
    all: T = None
    left: T = None
    middle: T = None
    right: T = None
    other: T = None


def number_of_clicks(interactions: List[Interaction]) -> Clicks[int]:
    clicks_stats = Clicks(0, 0, 0, 0, 0)
    for obj in interactions:
        if not obj.mouse.clicks.any:
            continue
        clicks_stats.all += 1
        if obj.mouse.clicks.left:
            clicks_stats.left += 1
        if obj.mouse.clicks.middle:
            clicks_stats.middle += 1
        if obj.mouse.clicks.right:
            clicks_stats.right += 1
        if obj.mouse.clicks.others:
            clicks_stats.other += 1

    return clicks_stats


def clicks_statistics(interactions: List[Interaction], range_width: int) -> Clicks[BasicStats]:
    clicks = number_of_clicks(interactions)

    # left button
    avg = clicks.left / range_width
    std_dev = np.std([obj.mouse.clicks.left for obj in interactions])
    left = BasicStats(clicks.left, avg, std_dev)

    # middle button
    avg = clicks.middle / range_width
    std_dev = np.std([obj.mouse.clicks.middle for obj in interactions])
    middle = BasicStats(clicks.middle, avg, std_dev)

    # right button
    avg = clicks.right / range_width
    std_dev = np.std([obj.mouse.clicks.right for obj in interactions])
    right = BasicStats(clicks.right, avg, std_dev)

    # other buttons
    avg = clicks.other / range_width
    std_dev = np.std([obj.mouse.clicks.others for obj in interactions])
    other = BasicStats(clicks.other, avg, std_dev)

    # all buttons
    avg = clicks.all / range_width
    std_dev = np.std([obj.mouse.clicks.any for obj in interactions])
    all = BasicStats(clicks.all, avg, std_dev)

    return Clicks(all, left, middle, right, other)
