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

import statistics
from typing import List, Tuple

from analyzer.data import Interaction


def interactions_set_directions(interactions: List[Interaction]):
    for obj in interactions:
        obj.slope = obj.mouse.speed.y / obj.mouse.speed.x


def average_direction(interactions: List[Interaction]) -> Tuple[float, float]:
    if not interactions:
        return 0, 0
    elif len(interactions) == 1:
        return interactions[0].slope, 0

    slopes = [obj.slope for obj in interactions]
    return statistics.mean(slopes), statistics.stdev(slopes)
