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
import json
import typing
import dataclasses
import dotmap
from .user import User
from .common import KeyboardInformation, MouseInformation, \
    ScreenCoordinates, ScrollInformation


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
    emotions: dotmap.DotMap = None

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

        parsed = json.loads(data)

        logging.getLogger(__name__).debug(
            'Loading the collected data from a JSON string.'
        )
        collected_data_list = []
        for obj in parsed:
            current_user = [u for u in users if u.user_id == obj['ui']][0]

            collected_data_list.append(
                CollectedData(
                    data_id=obj['_id']['$oid'],
                    user=current_user,
                    timestamp=obj['t'],
                    url=obj['u'],
                    window=ScreenCoordinates(*obj['w']),
                    emotions=obj.get('e', None),
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
