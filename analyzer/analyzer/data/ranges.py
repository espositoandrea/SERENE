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

from typing import List, Generic, TypeVar, Iterator

T = TypeVar('T')


class Range(Generic[T], object):
    __slots__ = ["preceding", "middle", "following"]

    def __init__(self, preceding: List[T], middle: T, following: List[T]):
        self.preceding: List[T] = preceding
        self.middle: T = middle
        self.following: List[T] = following

    def __str__(self):
        return "Range(preceding={}, middle={}, following={})".format(self.preceding, self.middle, self.following)

    @property
    def full(self) -> Iterator[T]:
        return (obj for obj in self)

    @property
    def first_half(self) -> Iterator[T]:
        return iter(self.preceding + [self.middle])

    @property
    def second_half(self) -> Iterator[T]:
        return iter([self.middle] + self.following)

    def __iter__(self):
        for obj in self.preceding:
            yield obj
        yield self.middle
        for obj in self.following:
            yield obj


class RangeData(Generic[T], object):
    __slots__ = ["full", "before", "after"]

    def __init__(self, full: T = None, before: T = None, after: T = None):
        self.full: T = full
        self.before: T = before
        self.after: T = after

    def __str__(self):
        return "RangeData(full={}, before={}, after={})".format(self.full, self.before, self.after)

    def to_dict(self):
        return {
            'full': self.full,
            'before': self.before,
            'after': self.after
        }
