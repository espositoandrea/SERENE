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
from typing import List

from analyzer.data import Interaction


@dataclasses.dataclass
class DirectionStatistics:
    changes: int
    change_rate: float


def interactions_set_directions(interactions: List[Interaction]):
    for obj in interactions:
        if obj.mouse.speed.y == 0 and obj.mouse.speed.x == 0:
            obj.slope = None
        elif obj.mouse.speed.x == 0:
            obj.slope = float('inf')
        else:
            obj.slope = obj.mouse.speed.y / obj.mouse.speed.x


def direction_changes(interactions: List[Interaction], range_width) -> DirectionStatistics:
    changes = 0
    for i, obj in enumerate(interactions[1:], 1):
        prev = interactions[i - 1]
        if obj.slope != prev.slope:
            changes += 1
    return DirectionStatistics(changes=changes, change_rate=changes / range_width)
