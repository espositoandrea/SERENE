# This file is part of 'data-processor', the tool used to process the information
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

import enum
import dataclasses
import typing
import dotmap


class Sex(enum.Enum):
    """A sex enumerator.

    An enumerator of all the valid sex values.
    """
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    @staticmethod
    def from_str(label: str) -> 'Sex':
        """Get a sex from a string.

        This method can be used to convert a 'natural' string value to a sex.

        Parameters
        ----------
        label : {'maschio', 'femmina', 'altro'}
            The string to be converted.

        Returns
        -------
        Sex
            The sex value associated to `label`.

        Raises
        ------
        NotImplementedError
            Raised if the label can't be converted.
        """

        label = label.lower()
        if label == 'maschio':
            return Sex.MALE
        if label == 'femmina':
            return Sex.FEMALE
        if label == 'altro':
            return Sex.OTHER

        raise NotImplementedError('Invalid Sex string')

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
    """Encapsulates various information regarding the scroll state of the window.

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
            Is the left button pressed?
        r
            Is the left button pressed?
        bN
            Is the button `N` (:math:`N \\in \\mathbb{N}, N \\geq 4`) pressed?
    """

    position: ScreenCoordinates
    buttons: dotmap.DotMap
