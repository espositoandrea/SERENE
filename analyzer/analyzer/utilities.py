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

import csv
import os
from typing import List, Dict, Union, Any, Tuple

from analyzer.data import Interaction, User, Website
from analyzer.data.base import BaseObject

BaseValues = Union[int, str, float, bool]
AnalyzerValues = Union[List[Union[Interaction, Dict[str, BaseValues]]], Dict[str, Union[User, Website, BaseValues]]]


def to_csv(values: AnalyzerValues, *filename: str, mode: str = 'w') -> None:
    dest_path = os.path.join(*filename)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    if isinstance(values, dict):
        values = [values[k] for k in values]

    values = [val.to_dict() if isinstance(val, BaseObject) else val for val in values]

    with open(dest_path, mode=mode, encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, values[0].keys())
        if mode != 'a' and mode != 'ab':
            writer.writeheader()

        writer.writerows(values)


def aggregate_data_to_list(values: Dict[Tuple[str, int], Dict[float, Dict[str, Any]]]) -> List[Dict[str, BaseValues]]:
    flattened = list()
    for obj_id, timestamp in values:
        d = {'middle.timestamp': timestamp, 'middle.id': obj_id}
        for range_width, val in values[(obj_id, timestamp)].items():
            for location in ['full', 'before', 'after']:
                # Average speed
                for k in vars(val['avg_speed'][location][0]):
                    d[f'{range_width}.avg_speed.{location}.total.{k}'] = getattr(val['avg_speed'][location][0], k)
                for k in vars(val['avg_speed'][location][1]):
                    d[f'{range_width}.avg_speed.{location}.x.{k}'] = getattr(val['avg_speed'][location][1], k)
                for k in vars(val['avg_speed'][location][2]):
                    d[f'{range_width}.avg_speed.{location}.y.{k}'] = getattr(val['avg_speed'][location][2], k)

                # Clicks
                for k in vars(val['clicks'][location]):
                    for j in vars(getattr(val['clicks'][location], k)):
                        d[f"{range_width}.{location}.clicks.{k}.{j}"] = getattr(getattr(val['clicks'][location], k), j)

                # Time between events
                for k in vars(val['event_times'][location]):
                    d[f"{range_width}.{location}.event_times.{k}"] = getattr(val['event_times'][location], k)

                # Idle time
                for k in vars(val['idle'][location]):
                    d[f"{range_width}.{location}.idle.{k}"] = getattr(val['idle'][location], k)

                # Keyboard
                for k in vars(val['keys'][location]):
                    for j in vars(getattr(val['keys'][location], k)):
                        d[f"{range_width}.{location}.keys.{k}.{j}"] = getattr(getattr(val['keys'][location], k), j)

                # Mouse movements
                for k in vars(val['mouse_movements'][location]):
                    d[f"{range_width}.{location}.mouse_movements.{k}"] = getattr(val['mouse_movements'][location], k)

                # Scrolls
                for k in vars(val['scrolls'][location]):
                    d[f"{range_width}.{location}.scrolls.{k}"] = getattr(val['scrolls'][location], k)

                # Trajectory
                for k in vars(val['slopes'][location]):
                    d[f"{range_width}.{location}.slopes.{k}"] = getattr(val['slopes'][location], k)

                # URLs
                for k in vars(val['urls'][location]):
                    d[f"{range_width}.{location}.urls.{k}"] = getattr(val['urls'][location], k)
        flattened.append(d)
    return flattened
