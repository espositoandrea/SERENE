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

"""A data module to work with users.
"""

import logging
import time
import json
import typing
import dataclasses
from .common import Gender


@dataclasses.dataclass(frozen=True)
class User:
    """A user.

    This class represents a user as seen
    for this study.

    Attributes
    ----------
    user_id : int
        The user's ID.
    age : int
        The user's age.
    gender : Gender
        The user's gender.
    internet : int
        The average time the user spend a day on the internet.
    """

    user_id: str
    age: int = None
    gender: Gender = None
    internet: int = None

    def __eq__(self, obj):
        return isinstance(obj, User) and self.user_id == obj.user_id

    def __str__(self) -> str:
        """Convert a User to a string.

        Returns
        -------
        str
            The string representing the user.
        """
        return f'User <{self.user_id}>'

    @staticmethod
    def from_json(data: str) -> typing.List['User']:
        """Create a list of users from a JSON string.

        This method can be used to generate a list of users starting from a
        JSON string.

        Parameters
        ----------
        data : str
            The JSON string. It must represent a valid JSON array.

        Returns
        -------
        list [User]
            The list of users represented by the JSON array.
        """

        logging.getLogger(__name__).debug(
            'Loading the users from a JSON string: START...'
        )
        start_time = time.time()

        parsed = json.loads(data)

        users_list = []
        for obj in parsed:
            users_list.append(
                User(
                    user_id=obj['_id']['$oid'],
                    age=obj['age'],
                    gender=Gender.from_str(obj['gender']),
                    internet=obj['internet']
                )
            )

        logging.getLogger(__name__).debug(
            '... END: Loaded the users from a JSON string. '
            'Took %.3f seconds',
            time.time() - start_time
        )

        return users_list
