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

"""A module containing various definitions to work with intervals."""

from typing import Tuple

from .features import DirectionStatistics, RateStats, BasicStats, Clicks, \
    Keyboard, VisitedWebsites
from .ranges import RangeData


# pylint: disable=too-many-instance-attributes
class IntervalData:
    """The data associated to an interval of Interaction objects.

    This class holds the data that can be calculated from a range (or interval)
    of Interaction objects.

    Attributes
    ----------
    middle_index : int
        The index of the middle object.
    slopes : RangeData [DirectionStatistics]
        The data calculated using the slopes.
    mouse_movements : RangeData [RateStats]
        The data calculated using the mouse movements.
    scrolls : RangeData [RateStats]
        The data calculated using the scrolling movements.
    avg_speed : RangeData [(BasicStats, BasicStats, BasicStats)]
        The data calculated using the speed.
    avg_acceleration : RangeData [(BasicStats, BasicStats, BasicStats)]
        The data calculated using the acceleration.
    clicks : RangeData [Clicks [BasicStats]]
        The data calculated using the click events.
    keys : RangeData [Keyboard [BasicStats]]
        The data calculated using the keyboard's click events.
    urls : RangeData [VisitedWebsites]
        The data calculated using the visited websites' data.
    event_times : RangeData [BasicStats]
        The data calculated using the time between two interactions.
    idle : RangeData [BasicStats]
        The data calculated using the idle time.

    See Also
    --------
    * Range
    * RangeData
    """
    __slots__ = [
        'middle_index',
        'slopes',
        'mouse_movements',
        'scrolls',
        'avg_speed',
        'avg_acceleration',
        'clicks',
        'keys',
        'urls',
        'event_times',
        'idle'
    ]

    # pylint: disable=too-many-arguments
    def __init__(self, middle_index: int,
                 slopes: RangeData[DirectionStatistics] = None,
                 mouse_movements: RangeData[RateStats] = None,
                 scrolls: RangeData[RateStats] = None,
                 avg_speed: RangeData[
                     Tuple[BasicStats, BasicStats, BasicStats]] = None,
                 avg_acceleration: RangeData[
                     Tuple[BasicStats, BasicStats, BasicStats]] = None,
                 clicks: RangeData[Clicks[BasicStats]] = None,
                 keys: RangeData[Keyboard[BasicStats]] = None,
                 urls: RangeData[VisitedWebsites] = None,
                 event_times: RangeData[BasicStats] = None,
                 idle: RangeData[BasicStats] = None):
        """Create a new set of data.

        Parameters
        ----------
        middle_index : int
            The index of the middle object.
        slopes : RangeData [DirectionStatistics]
            The data calculated using the slopes.
        mouse_movements : RangeData [RateStats]
            The data calculated using the mouse movements.
        scrolls : RangeData [RateStats]
            The data calculated using the scrolling movements.
        avg_speed : RangeData [(BasicStats, BasicStats, BasicStats)]
            The data calculated using the speed.
        avg_acceleration : RangeData [(BasicStats, BasicStats, BasicStats)]
            The data calculated using the acceleration.
        clicks : RangeData [Clicks [BasicStats]]
            The data calculated using the click events.
        keys : RangeData [Keyboard [BasicStats]]
            The data calculated using the keyboard's click events.
        urls : RangeData [VisitedWebsites]
            The data calculated using the visited websites' data.
        event_times : RangeData [BasicStats]
            The data calculated using the time between two interactions.
        idle : RangeData [BasicStats]
            The data calculated using the idle time.
        """
        self.middle_index: int = middle_index
        self.slopes: RangeData[DirectionStatistics] = slopes
        self.mouse_movements: RangeData[RateStats] = mouse_movements
        self.scrolls: RangeData[RateStats] = scrolls
        self.avg_speed: RangeData[
            Tuple[BasicStats, BasicStats, BasicStats]] = avg_speed
        self.avg_acceleration: RangeData[
            Tuple[BasicStats, BasicStats, BasicStats]] = avg_acceleration
        self.clicks: RangeData[Clicks[BasicStats]] = clicks
        self.keys: RangeData[Keyboard[BasicStats]] = keys
        self.urls: RangeData[VisitedWebsites] = urls
        self.event_times: RangeData[BasicStats] = event_times
        self.idle: RangeData[BasicStats] = idle

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns
        -------
        dict [str, any]
            A dictionary representing the object. The keys are equal to the
            class attributes.
        """
        return {
            'slopes': self.slopes.to_dict() if self.slopes else None,
            'mouse_movements': self.mouse_movements.to_dict()
                               if self.mouse_movements else None,
            'scrolls': self.scrolls.to_dict() if self.scrolls else None,
            'avg_speed': self.avg_speed.to_dict() if self.avg_speed else None,
            'avg_acceleration': self.avg_acceleration.to_dict()
                                if self.avg_acceleration else None,
            'clicks': self.clicks.to_dict() if self.clicks else None,
            'keys': self.keys.to_dict() if self.keys else None,
            'urls': self.urls.to_dict() if self.urls else None,
            'event_times': self.event_times.to_dict() if self.event_times
                           else None,
            'idle': self.idle.to_dict() if self.idle else None,
        }
