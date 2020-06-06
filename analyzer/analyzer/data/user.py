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

"""Module containing the definition of the User class."""

from typing import Dict, Union

from analyzer.data.base import BaseObject


class User(BaseObject):
    """A user.

    This class represents a user.

    Attributes
    ----------
    id : str
        The user's id.
    age : int
        The user's age.
    internet : int
        The average number of hours the user's use internet.
    gender : str
        The user's gender.
    """
    __slots__ = ["id", "age", "internet", "gender"]

    def __init__(self, id: str, age: int, internet: int, gender: str):
        """Create a new user.

        Parameters
        ----------
        id : str
            The user's id.
        age : int
            The user's age.
        internet : int
            The average number of hours the user's use internet.
        gender : str
            The user's gender.
        """
        self.id: str = id
        self.age: int = age
        self.internet: int = internet
        self.gender: str = gender

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """Convert the object to a dictionary.

        Returns
        -------
        dict [str, int or str]
            A dictionary representing the object. The keys are 'id', 'age',
            'internet' and 'gender'.
        """
        return {
            'id': self.id,
            'age': self.age,
            'internet': self.internet,
            'gender': self.gender
        }
