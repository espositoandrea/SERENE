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
import math
from typing import List, Generic, TypeVar

from .data import Interaction

T = TypeVar('T')


@dataclasses.dataclass
class Range(Generic[T]):
    preceding: List[T]
    middle: T
    following: List[T]


def interactions_split_intervals(interactions: List[Interaction], width: int) -> List[Range[int]]:
    """Split the series of interactions in intervals based on the emotions.

    Parameters
    ----------
    interactions : list [dict]
        The list of interactions.
    width : int
        The width in milliseconds of the entire wanted range.

    Returns
    -------
    list [Range]
        A list which elements contain:

        1. The list of interactions in the given interval that precedes the
           emotions measurement
        2. The interaction containing the emotions measurement
        3. The list of interactions in the given interval that succedes the
           emotions measurement
    """

    def has_emotions_over_value(obj: Interaction) -> bool:
        limit = 1.0
        return (obj.emotions.joy or -1) >= limit or \
               (obj.emotions.fear or -1) >= limit or \
               (obj.emotions.disgust or -1) >= limit or \
               (obj.emotions.sadness or -1) >= limit or \
               (obj.emotions.anger or -1) >= limit or \
               (obj.emotions.surprise or -1) >= limit or \
               (obj.emotions.contempt or -1) >= limit or \
               (obj.emotions.valence or -1) >= limit or \
               (obj.emotions.engagement or -1) >= limit

    def get_emotions_indexes() -> List[int]:
        indexes = list()
        for i, obj in enumerate(interactions):
            if has_emotions_over_value(obj):
                indexes.append(i)

        return indexes

    split = list()

    for index in get_emotions_indexes():
        current_range = Range([], index, [])

        for i in range(max(math.floor(index - width / 2), 0), index):
            if interactions[i].timestamp >= interactions[index].timestamp - width / 2:
                current_range.preceding.append(i)

        for i in range(index + 1, min(math.floor(index + width / 2) + 1, len(interactions))):
            if interactions[i].timestamp > interactions[index].timestamp + width / 2:
                break
            current_range.following.append(i)
        split.append(current_range)

    return split


def flatten_range(to_flatten: Range[T]) -> List[T]:
    return [obj for obj in to_flatten.preceding] + [to_flatten.middle] + [obj for obj in to_flatten.following]


def interactions_from_range(interactions: List[Interaction], range: Range[int]) -> Range[Interaction]:
    """Converts a range of interactions indexes to a list of interactions.

    Parameters
    ----------
    interactions : list[dict]
        The original interactions series
    range : (list [int], int, list [int])
        The range to be converted

    Returns
    -------
    (list [dict], int, list [dict]) or list [dict]
        If `flatten` is False, the returned value will be a tuple containing the
        interactions in the same format as the indexes of the range (a list of
        preceding objects, the middle object and a list of following objects);
        if `flatten` is True, the returned value will be the list of
        interactions contained in the range.
    """

    final = Range(
        [interactions[i] for i in range.preceding],
        interactions[range.middle],
        [interactions[i] for i in range.following]
    )

    return final
