# This file is part of 'analyzer', the tool used to process the information
# collected for Andrea Esposito's Thesis.
# Copyright (C) 2020  Andrea Esposito
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""A data module to work with interaction data.
"""

import logging
import csv
import json
import typing
import dataclasses
import numpy as np
import pandas as pd
import dotmap
from .user import User
from .common import KeyboardInformation, MouseInformation, \
    ScreenCoordinates, ScrollInformation, Emotions


class CollectedDataSeries:
    """A series of collected data.

    This class represents a series of collected data and provides useful methods.

    Attributes
    ----------
    series : pandas.Series
        The data series
    """

    def __init__(self, data: typing.List['CollectedData']):
        """Initialize a new series.

        Parameters
        ----------
        data : list [CollectedData]
            The data
        """

        self.series = sorted(data, key=lambda obj: obj.timestamp)

    def __len__(self):
        return len(self.series)

    def split_by_seconds(self) -> typing.List[typing.List['CollectedData']]:
        start_time = self.series[0].timestamp
        # The timestamps are in milliseconds: to get it in seconds, the last
        # three digits must be 0, so we divide and then multiply by 1000.
        start_seconds = int(int(start_time / 1000) * 1000)
        split_list = [list()]
        for obj in self.series:
            if obj.timestamp >= start_seconds + 1000:
                start_seconds = int(int(obj.timestamp / 1000) * 1000)
                split_list.append(list())
            split_list[-1].append(obj)

        return split_list

    @property
    def clicks_per_seconds(self):
        # TODO: Change to be per-user
        split_list = self.split_by_seconds()
        final = dict()
        for piece in split_list:
            current_timestamp = int(int(piece[0].timestamp / 1000) * 1000)
            final[current_timestamp] = {'left': 0, 'right': 0, 'middle': 0, 'others': 0}
            for obj in piece:
                final[current_timestamp]['left'] += int(obj.mouse.buttons.l)
                final[current_timestamp]['middle'] += int(obj.mouse.buttons.m)
                final[current_timestamp]['right'] += int(obj.mouse.buttons.r)
                final[current_timestamp]['others'] += sum(i >= 3 for i in obj.mouse.buttons_list())
            final[current_timestamp]['total'] = sum(final[current_timestamp].values())

        return final

    def to_csv(self, file_name):
        """Convert a list of CollectedData to a DataFrame.

        This function converts a list of CollectedData to a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The data converted into a DataFrame
        """

        with open(file_name, 'w') as file:
            writer = csv.DictWriter(file, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=self.series[0].to_dict().keys())
            writer.writeheader()
            for obj in self.series:
                writer.writerow(obj.to_dict())


@dataclasses.dataclass(frozen=True)
class CollectedData:
    """The collected data.

    This class represents the data collected from the server.

    Attributes
    ----------
    data_id : str
        The object's id.
    user : User
        The user that produced this data.
    timestamp : int
        The timestamp on which this data was produced.
    url : string
        The visited URL.
    mouse: MouseInformation
        Various data regarding the mouse.
    scroll : ScrollInformation
        Various data about the scroll position.
    window : ScreenCoordinates;
        Data about the browser's window's dimensions.
    keyboard : KeyboardInformation
        Data about the pressed keys.
    emotions : DotMap
        The emotions value, fetched from Affectiva.
    """

    # pylint: disable=too-many-instance-attributes
    # All nine attributes are needed as defined by the data schema

    data_id: str
    user: User
    timestamp: int = None
    url: str = None
    mouse: MouseInformation = None
    scroll: ScrollInformation = None
    window: ScreenCoordinates = None
    keyboard: KeyboardInformation = None
    emotions: Emotions = None

    def __eq__(self, obj):
        return isinstance(obj, CollectedData) and self.data_id == obj.data_id

    def to_dict(self):
        return {
            # Basic data
            'id': self.data_id,
            'timestamp': self.timestamp,
            'url': self.url,
            # User data
            'user.gender': self.user.gender,
            'user.age': self.user.age,
            'user.internet': self.user.internet,
            # Window data
            'window.x': self.window.x,
            'window.y': self.window.y,
            # Mouse data
            'mouse.position.x': self.mouse.position.x,
            'mouse.position.y': self.mouse.position.y,
            'mouse.buttons': self.mouse.buttons_list(),
            # Scroll data
            'scroll.absolute.x': self.scroll.absolute.x,
            'scroll.absolute.y': self.scroll.absolute.y,
            'scroll.relative.x': self.scroll.relative.x,
            'scroll.relative.y': self.scroll.relative.y,
            # Keyboard data
            'keyboard.alpha': self.keyboard.alpha,
            'keyboard.numeric': self.keyboard.numeric,
            'keyboard.symbol': self.keyboard.symbol,
            'keyboard.function': self.keyboard.function,
            # Emotions data
            'emotions.exist': self.emotions is not None,
            'emotions.joy': getattr(self.emotions, 'joy', None),
            'emotions.fear': getattr(self.emotions, 'fear', None),
            'emotions.disgust': getattr(self.emotions, 'disgust', None),
            'emotions.sadness': getattr(self.emotions, 'sadness', None),
            'emotions.anger': getattr(self.emotions, 'anger', None),
            'emotions.surprise': getattr(self.emotions, 'surprise', None),
            'emotions.contempt': getattr(self.emotions, 'contempt', None),
            'emotions.valence': getattr(self.emotions, 'valence', None),
            'emotions.engagement': getattr(self.emotions, 'engagement', None),
        }

    @staticmethod
    def from_json(users: typing.Set[User], data: str) \
            -> typing.List['CollectedData']:
        """Create a list of data from a JSON string.

        This method can be used to generate a list of data starting from a JSON
        string.

        Parameters
        ----------
        users : set [User]
            The set of users that generated this data.
        data : str
            The JSON string. It must represent a valid JSON array.

        Returns
        -------
        list [CollectedData]
            The list of users represented by the JSON array.
        """

        logging.getLogger(__name__).debug(
            'Loading the collected data from a JSON string...'
        )
        parsed = json.loads(data)

        collected_data_list = []
        for index, obj in enumerate(parsed, start=1):
            logging.getLogger(__name__).debug(
                'Loading object %d of %d',
                index,
                len(parsed)
            )
            try:
                current_user = [u for u in users if u.user_id == obj['ui']][0]
            except IndexError:
                logging.getLogger(__name__).warning(
                    "The user with id '%s' doesn't exist. A new empty user will be created.",
                    obj['ui']
                )
                new_user = User(obj['ui'])
                users.add(new_user)
                current_user = new_user

            emotions = Emotions(
                joy=obj.get('e').get('j', None),
                fear=obj.get('e').get('f', None),
                disgust=obj.get('e').get('d', None),
                sadness=obj.get('e').get('s', None),
                anger=obj.get('e').get('a', None),
                surprise=obj.get('e').get('s', None),
                contempt=obj.get('e').get('c', None),
                valence=obj.get('e').get('v', None),
                engagement=obj.get('e').get('e', None),
            ) if obj.get('e', None) is not None else None

            collected_data_list.append(
                CollectedData(
                    data_id=obj['_id']['$oid'],
                    user=current_user,
                    timestamp=obj['t'],
                    url=obj['u'],
                    window=ScreenCoordinates(*obj['w']),
                    emotions=emotions,
                    keyboard=KeyboardInformation(
                        alpha=obj['k']['a'],
                        symbol=obj['k']['s'],
                        function=obj['k']['f'],
                        numeric=obj['k']['n']
                    ),
                    mouse=MouseInformation(
                        position=ScreenCoordinates(*obj['m']['p']),
                        buttons=dotmap.DotMap(obj['m']['b'])
                    ),
                    scroll=ScrollInformation(
                        relative=ScreenCoordinates(*obj['s']['r']),
                        absolute=ScreenCoordinates(*obj['s']['a'])
                    )
                )
            )

        return collected_data_list
