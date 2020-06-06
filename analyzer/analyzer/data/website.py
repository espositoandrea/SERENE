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

"""Module containing the definition of the Website class"""

import urllib.parse
from typing import Optional, Dict, Union

from analyzer.data.base import BaseObject


class Website(BaseObject):
    """A website.

    This class represents a website.

    Attributes
    ----------
    url : urllib.parse.ParseResult
        The url of the website.
    count : int
        The number of visits received by the website.
    category : str
        The category of the website.
    """
    __slots__ = ["url", "count", "category"]

    def __init__(self, url: Optional[urllib.parse.ParseResult], count: int = 0,
                 category: str = 'UNKNOWN'):
        """Create a new website
        Parameters
        ----------
        url : urllib.parse.ParseResult
            The url of the website. May be `None`.
        count : int, optional
            The number of visits received by the website.
        category : str, optional
            The category of the website.
        """
        self.url: Optional[urllib.parse.ParseResult] = url
        self.count: int = count
        self.category: str = category

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """Convert the object to a dictionary.

        Returns
        -------
        dict [str, int or str]
            A dictionary representing the object. The keys are 'url', 'count'
            and 'category'.
        """
        return {
            'url': self.url.geturl() if self.url else None,
            'count': int(self.count),
            'category': self.category
        }
