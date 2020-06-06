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

"""A module to work with ranges."""

from typing import List, Generic, TypeVar, Iterator

T = TypeVar('T')


class Range(Generic[T]):
    """A range.

    This class represents a range, as defined in math: given a point $x$ and a
    width $w$, a range is in the form $[x - w, x + w]$.

    Attributes
    ----------
    preceding : list [T]
        A list of values in the range $[x - w, x)$.
    middle : T
        The element $x$.
    following : list [T]
        A list of values in the range $(x, x + w]$.
    """
    __slots__ = ["preceding", "middle", "following"]

    def __init__(self, preceding: List[T], middle: T, following: List[T]):
        """Create a new range.

        Parameters
        ----------
        preceding : list [T]
            A list of values in the range $[x - w, x)$.
        middle : T
            The element $x$.
        following : list [T]
            A list of values in the range $(x, x + w]$.
        """
        self.preceding: List[T] = preceding
        self.middle: T = middle
        self.following: List[T] = following

    def __str__(self):
        """Return a string representing the range.

        Returns
        -------
        str
            A string representing the range.
        """
        return "Range(preceding={}, middle={}, following={})".format(
            self.preceding, self.middle, self.following)

    @property
    def full(self) -> Iterator[T]:
        """Get the full flattened interval.

        Returns
        -------
        Iterator [T]
            An iterator of all the objects in the range.
        """
        return (obj for obj in self)

    @property
    def first_half(self) -> Iterator[T]:
        """Get the first half of the range, defined as $[x - w, x]$

        Returns
        -------
        Iterator [T]
            An iterator of all the objects in the first half of the range.
        """
        return iter(self.preceding + [self.middle])

    @property
    def second_half(self) -> Iterator[T]:
        """Get the second half of the range, defined as $[x, x + w]$

        Returns
        -------
        Iterator [T]
            An iterator of all the objects in the second half of the range.
        """
        return iter([self.middle] + self.following)

    def __iter__(self):
        """The iterator of the range.

        Yields
        ------
        T
            An object of the range. The order in the range is respected.
        """
        for obj in self.preceding:
            yield obj
        yield self.middle
        for obj in self.following:
            yield obj


class RangeData(Generic[T]):
    """The data associated to a range.

    This class holds the data associated to a Range.

    Attributes
    ----------
    full : T
        The data associated to the entire Range.
    before : T
        The data associated to the first half of the Range.
    after : T
        The data associated to the second half of the Range.
    """
    __slots__ = ["full", "before", "after"]

    def __init__(self, full: T = None, before: T = None, after: T = None):
        """Create a new set of data.

        Parameters
        ----------
        full : T
            The data associated to the entire Range.
        before : T
            The data associated to the first half of the Range.
        after : T
            The data associated to the second half of the Range.
        """
        self.full: T = full
        self.before: T = before
        self.after: T = after

    def __str__(self):
        """Get a string representing the data.

        Returns
        -------
        str
            A string representing the data.
        """
        return "RangeData(full={}, before={}, after={})".format(self.full,
                                                                self.before,
                                                                self.after)

    def to_dict(self):
        """Convert the object to a dictionary.

        Returns
        -------
        dict [str, T]
            A dictionary representing the object. The keys are: 'full', 'before'
            and 'after'.
        """
        return {
            'full': self.full,
            'before': self.before,
            'after': self.after
        }
