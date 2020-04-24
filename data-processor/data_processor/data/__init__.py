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

"""A module to deal with the data stored on the server.

This module is a collection of classes, functions, etc to deal with the
collected data that's stored on the server.

Examples
--------

.. code-block:: python
   :caption: How to create an object from a JSON.

   from data_processor.user import User
   from data_processor.data import CollectedData
   user_list = YOUR_USER_LIST
   json_string = "[YOUR_OBJECT]"
   CollectedData.from_json(user_list, json_string)
   # [CollectedData(...), ...]
"""

from .common import *
from .collected_data import CollectedData
from .user import User
