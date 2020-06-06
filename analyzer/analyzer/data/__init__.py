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

"""The data module

This module contains the definition of all the data used by the tool.

Notes
-----

All the definitions in this module aim at memory efficiency. For this reason,
all of the defined classes define the `__slots__` magic attributes, thus
removing the automatic `__dict__` attribute.
"""

from .base import Speed2D, ScreenCoordinates, MouseData, KeyboardData, \
    ScrollData
from .emotions import Emotions
from .user import User
from .website import Website
from .interaction import Interaction

from .loader import load_interactions, load_websites, load_users
