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

import dataclasses
from typing import List, Dict

from ..data import Interaction, Website


@dataclasses.dataclass
class VisitedWebsites:
    unique: int
    changed: int
    change_rate: float


def interactions_set_website_categories(interactions: List[Interaction], websites: Dict[str, Website]):
    for obj in interactions:
        obj.url_category = websites.get(obj.url, Website(None)).category


def visited_websites(interactions: List[Interaction]) -> Dict[str, int]:
    websites = dict()
    for obj in interactions:
        if obj.url not in websites:
            websites[obj.url] = 0
        websites[obj.url] += 1

    return websites


def websites_statistics(interactions: List[Interaction], range_width: int = None) -> VisitedWebsites:
    unique = len(visited_websites(interactions))

    last_url = interactions[0].url
    changed = 0
    for obj in interactions[1:]:
        if obj.url == last_url:
            continue
        last_url = obj.url
        changed += 1

    change_rate = changed / range_width if range_width is not None else None

    return VisitedWebsites(unique, changed, change_rate)
