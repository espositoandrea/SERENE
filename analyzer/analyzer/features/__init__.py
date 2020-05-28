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

# Types
from .base import BasicStats, RateStats
from .clicks import Clicks
from .keyboard import Keyboard
from .websites import VisitedWebsites
from .trajectories import DirectionStatistics

# Functions
from .speed import interactions_set_speed, average_speed
from .clicks import clicks_statistics, number_of_clicks
from .keyboard import keyboard_statistics, number_of_keys
from .websites import interactions_set_website_categories, visited_websites, websites_statistics
from .variation import average_events_time, average_idle_time, get_changed_features, mouse_movements_per_milliseconds, \
    scrolls_per_milliseconds
from .trajectories import interactions_set_directions, direction_changes
