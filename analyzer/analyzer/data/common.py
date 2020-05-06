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

"""A collection of classes and types used by other data modules.

See Also
--------
analyzer.data.collected_data : This module uses the classes defined here.
analyzer.data.user : This module uses the classes defined here.
"""

import re
import enum
import dataclasses
import typing
import dotmap


class Gender(enum.Enum):
    """A gender enumerator.

    An enumerator of all the valid gender values.
    """

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    @staticmethod
    def from_str(label: str) -> 'Gender':
        """Get a gender from a string.

        This method can be used to convert a 'natural' string value to a gender.

        Parameters
        ----------
        label : {'maschio', 'm', 'femmina', 'm', 'altro', 'a'}
            The string to be converted.

        Returns
        -------
        Gender
            The gender value associated to `label`.

        Raises
        ------
        NotImplementedError
            Raised if the label can't be converted.
        """

        label = label.lower()
        if label == 'maschio' or label == 'm':
            return Gender.MALE
        if label == 'femmina' or label == 'f':
            return Gender.FEMALE
        if label == 'altro' or label == 'a':
            return Gender.OTHER

        raise NotImplementedError('Invalid Gender string')


class ScreenCoordinates(typing.NamedTuple):
    """Represents a pair of screen coordinates.

    Attributes
    ----------
    x : int
        The coordinate on the x axis.
    y : int
        The coordinate on the y axis.
    """

    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Emotions:
    """Encapsulates all the information extracted by Affectiva [1]_.

    Attributes
    ----------
    joy : float
        The joy value. May be `None` if no value was registered.
    fear : float
        The fear value. May be `None` if no value was registered.
    disgust : float
        The disgust value. May be `None` if no value was registered.
    sadness : float
        The sadness value. May be `None` if no value was registered.
    anger : float
        The anger value. May be `None` if no value was registered.
    surprise : float
        The surprise value. May be `None` if no value was registered.
    contempt : float
        The contempt value. May be `None` if no value was registered.
    valence : float
        The valence value. May be `None` if no value was registered.
    engagement : float
        The engagement value. May be `None` if no value was registered.

    References
    ----------
    .. [1] Affectiva, http://affectiva.com/
    """

    joy: float = None
    fear: float = None
    disgust: float = None
    sadness: float = None
    anger: float = None
    surprise: float = None
    contempt: float = None
    valence: float = None
    engagement: float = None


@dataclasses.dataclass(frozen=True)
class KeyboardInformation:
    """Encapsulates various information regarding the keyboard's state.

    Attributes
    ----------
    alpha: bool
        Is an alphabetic key pressed?
    numeric: bool
        Is a numeric key pressed?
    symbol: bool
        Is a symbol key pressed?
    function: bool
        Is a function key pressed?
    """

    alpha: bool
    numeric: bool
    symbol: bool
    function: bool


@dataclasses.dataclass(frozen=True)
class ScrollInformation:
    """Encapsulates various information regarding the scroll state of the
    window.

    Attributes
    ----------
    absolute : ScreenCoordinates
        The absolute scroll position.
    relative : ScreenCoordinates
        The relative scroll position (from the bottom right of the screen).
    """

    relative: ScreenCoordinates
    absolute: ScreenCoordinates


@dataclasses.dataclass(frozen=True)
class MouseInformation:
    """Encapsulates various data regarding the mouse.

    Attributes
    ----------
    position : ScreenCoordinates
        The mouse position
    buttons : DotMap [str, bool]
        The mouse buttons. The keys are the following.

        l
            Is the left button pressed?
        m
            Is the middle button pressed?
        r
            Is the right button pressed?
        bN
            Is the button `N` (:math:`N \\in \\mathbb{N}, N \\geq 4`) pressed?
    """

    position: ScreenCoordinates
    buttons: dotmap.DotMap

    def buttons_list(self) -> typing.List[int]:
        """Convert the mouse button objets to a list.

        This function converts the data on the mouse buttons to a list of ID.
        The ID are assigned as in the HTML's MouseEvent [1]_.

        Returns
        -------
        list [int]
            A list of mouse buttons' IDs.

        References
        ----------
        .. [1] MDN: HTML's MouseEvent,
           https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/button
           (visited on 6 May 2020)
        """
        final = list()
        for btn in self.buttons:
            if btn == 'l' and self.buttons[btn]:
                final.append(0)
            elif btn == 'm' and self.buttons[btn]:
                final.append(1)
            elif btn == 'r' and self.buttons[btn]:
                final.append(2)
            elif re.match(r'^b\d+?$', btn) and self.buttons[btn]:
                final.append(int(btn[1:]) - 1)
        return final
