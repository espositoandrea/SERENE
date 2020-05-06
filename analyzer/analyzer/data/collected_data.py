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
import time
import json
import typing
import dataclasses
import numpy as np
import pandas as pd
import dotmap
from .user import User
from .common import KeyboardInformation, MouseInformation, \
    ScreenCoordinates, ScrollInformation, Emotions


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
            'Loading the collected data from a JSON string: START...'
        )
        start_time = time.time()

        parsed = json.loads(data)

        collected_data_list = []
        for obj in parsed:
            try:
                current_user = [u for u in users if u.user_id == obj['ui']][0]
            except IndexError:
                current_user = User(obj['ui'])

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
        logging.getLogger(__name__).debug(
            '... END: Loaded the collected data from a JSON string. '
            'Took %.3f seconds',
            time.time() - start_time
        )

        return collected_data_list

    @staticmethod
    def to_dataframe(data: typing.List["CollectedData"]):
        """Convert a list of CollectedData to a DataFrame.

        This function converts a list of CollectedData to a pandas DataFrame.

        Parameters
        ----------
        data : list [CollectedData]
            The list of data to be converted.

        Returns
        -------

        pandas.DataFrame
            The data converted into a DataFrame
        """
        df_data = {
            # Basic data
            'id': list(),
            'timestamp': list(),
            'url': list(),
            # Window data
            'window.x': list(),
            'window.y': list(),
            # Mouse data
            'mouse.position.x': list(),
            'mouse.position.y': list(),
            'mouse.buttons': list(),
            # Scroll data
            'scroll.absolute.x': list(),
            'scroll.absolute.y': list(),
            'scroll.relative.x': list(),
            'scroll.relative.y': list(),
            # Keyboard data
            'keyboard.alpha': list(),
            'keyboard.numeric': list(),
            'keyboard.symbol': list(),
            'keyboard.function': list(),
            # Emotions data
            'emotions.exist': list(),
            'emotions.joy': list(),
            'emotions.fear': list(),
            'emotions.disgust': list(),
            'emotions.sadness': list(),
            'emotions.anger': list(),
            'emotions.surprise': list(),
            'emotions.contempt': list(),
            'emotions.valence': list(),
            'emotions.engagement': list(),
        }

        for obj in data[700:2000]:
            # Add basic data
            df_data['id'].append(obj.data_id)
            df_data['timestamp'].append(obj.timestamp)
            df_data['url'].append(obj.url)

            # Add window data
            df_data['window.x'].append(obj.window.x)
            df_data['window.y'].append(obj.window.y)

            # Add mouse data
            df_data['mouse.position.x'].append(obj.mouse.position.x)
            df_data['mouse.position.y'].append(obj.mouse.position.x)
            df_data['mouse.buttons'].append(
                ','.join(str(b) for b in obj.mouse.buttons_list())
            )

            # Add scroll data
            df_data['scroll.absolute.x'].append(obj.scroll.absolute.x)
            df_data['scroll.absolute.y'].append(obj.scroll.absolute.y)
            df_data['scroll.relative.x'].append(obj.scroll.relative.x)
            df_data['scroll.relative.y'].append(obj.scroll.relative.y)

            # Add keyboard data
            df_data['keyboard.alpha'].append(obj.keyboard.alpha)
            df_data['keyboard.numeric'].append(obj.keyboard.numeric)
            df_data['keyboard.symbol'].append(obj.keyboard.symbol)
            df_data['keyboard.function'].append(obj.keyboard.function)

            # Add emotions data
            if obj.emotions is not None:
                df_data['emotions.exist'].append(True)
                df_data['emotions.joy'].append(obj.emotions.joy)
                df_data['emotions.fear'].append(obj.emotions.fear)
                df_data['emotions.disgust'].append(obj.emotions.disgust)
                df_data['emotions.sadness'].append(obj.emotions.sadness)
                df_data['emotions.anger'].append(obj.emotions.anger)
                df_data['emotions.surprise'].append(obj.emotions.surprise)
                df_data['emotions.contempt'].append(obj.emotions.contempt)
                df_data['emotions.valence'].append(obj.emotions.valence)
                df_data['emotions.engagement'].append(obj.emotions.engagement)
            else:
                df_data['emotions.exist'].append(False)
                df_data['emotions.joy'].append(None)
                df_data['emotions.fear'].append(None)
                df_data['emotions.disgust'].append(None)
                df_data['emotions.sadness'].append(None)
                df_data['emotions.anger'].append(None)
                df_data['emotions.surprise'].append(None)
                df_data['emotions.contempt'].append(None)
                df_data['emotions.valence'].append(None)
                df_data['emotions.engagement'].append(None)

        data_frame = pd.DataFrame(df_data)
        data_frame.fillna(value=np.nan, inplace=True)
        return data_frame
