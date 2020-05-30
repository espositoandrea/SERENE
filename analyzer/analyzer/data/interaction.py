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
import gc
import logging
import math
import os
import itertools
import re
import statistics
import time
from copy import copy
from typing import List, Dict, Any, Sequence, Iterator, Union, Tuple, Set

from bson import ObjectId

from analyzer.data.features import DirectionStatistics, RateStats, BasicStats, Clicks, Keyboard, VisitedWebsites
from analyzer.data.ranges import Range
from .base import *
from .emotions import Emotions
from .interval import IntervalData, RangeData
from .website import Website
from ..decorators import timed

logger = logging.getLogger(__name__)


class Interaction(BaseObject):
    __slots__ = [
        "id",
        "user_id",
        "timestamp",
        "url",
        "mouse",
        "scroll",
        "keyboard",
        "emotions",
        "url_category",
        "slope"
    ]

    def __init__(self, **kwargs):
        super().__init__()
        self.id: str = kwargs.get("id")
        self.user_id: str = kwargs.get("user_id")
        self.timestamp: int = kwargs.get("timestamp")
        self.url: str = kwargs.get("url")
        self.mouse: MouseData = kwargs.get("mouse")
        self.scroll: ScrollData = kwargs.get("scroll")
        self.keyboard: KeyboardData = kwargs.get("keyboard")
        self.emotions: Emotions = kwargs.get("emotions")
        self.url_category: str = kwargs.get("url_category")
        self.slope: float = kwargs.get("slope")

    def get_changed_features(self, other: 'Interaction') -> Set[str]:
        return {k for k in self.to_dict() if
                self.to_dict()[k] != other.to_dict()[k] and not re.match(r'^emotions\..*?$',
                                                                         k) and k != 'id' and k != 'timestamp'}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "url": self.url,
            "url.category": self.url_category,
            # Mouse
            "mouse.position.x": self.mouse.position.x,
            "mouse.position.y": self.mouse.position.y,
            "mouse.clicks": self.mouse.clicks.any,
            "mouse.clicks.left": self.mouse.clicks.left,
            "mouse.clicks.right": self.mouse.clicks.right,
            "mouse.clicks.middle": self.mouse.clicks.middle,
            "mouse.clicks.others": self.mouse.clicks.others,
            "mouse.speed": self.mouse.speed.total,
            "mouse.speed.x": self.mouse.speed.x,
            "mouse.speed.y": self.mouse.speed.y,
            "mouse.acceleration": self.mouse.acceleration.total,
            "mouse.acceleration.x": self.mouse.acceleration.x,
            "mouse.acceleration.y": self.mouse.acceleration.y,
            "trajectory.slope": self.slope,
            # Scroll
            "scroll.absolute.x": self.scroll.absolute.x,
            "scroll.absolute.y": self.scroll.absolute.y,
            "scroll.relative.x": self.scroll.relative.x,
            "scroll.relative.y": self.scroll.relative.y,
            # Keyboard
            "keyboard": self.keyboard.any,
            "keyboard.alpha": self.keyboard.alpha,
            "keyboard.numeric": self.keyboard.numeric,
            "keyboard.function": self.keyboard.function,
            "keyboard.symbol": self.keyboard.symbol,
            # Emotions
            "emotions.exists": self.emotions.exists,
            "emotions.joy": self.emotions.joy,
            "emotions.fear": self.emotions.fear,
            "emotions.disgust": self.emotions.disgust,
            "emotions.sadness": self.emotions.sadness,
            "emotions.anger": self.emotions.anger,
            "emotions.surprise": self.emotions.surprise,
            "emotions.contempt": self.emotions.contempt,
            "emotions.valence": self.emotions.valence,
            "emotions.engagement": self.emotions.engagement
        }


def speed(pos0: ScreenCoordinates, pos1: ScreenCoordinates, time: int) -> Speed2D:
    x_dist = pos1.x - pos0.x
    y_dist = pos1.y - pos0.y

    x_speed = x_dist / time
    y_speed = y_dist / time
    tot_speed = math.sqrt((x_speed ** 2) + (y_speed ** 2))

    return Speed2D(total=tot_speed, x=x_speed, y=y_speed)


def acceleration(v0: Speed2D, v1: Speed2D, time: int) -> Speed2D:
    v_x = v1.x - v0.x
    v_y = v1.y - v0.y

    x_acc = v_x / time
    y_acc = v_y / time
    tot_acc = math.sqrt((x_acc ** 2) + (y_acc ** 2))

    return Speed2D(total=tot_acc, x=x_acc, y=y_acc)


class InteractionsList(object):
    __slots__ = ["interactions"]

    def __init__(self, interactions: Sequence[Interaction]):
        logger.info("Creating InteractionsList object")
        self.interactions: List[Interaction] = list(interactions)
        if not self.interactions:
            logger.warning("Empty list")
            return
        logger.info("Sorting by timestamps")
        self.interactions.sort(key=lambda obj: (obj.timestamp, ObjectId(obj.id).generation_time))
        self._set_additional_data()

    def __iter__(self):
        for obj in self.interactions:
            yield obj

    def __getitem__(self, item: int) -> Interaction:
        return self.interactions[item]

    def __len__(self):
        return len(self.interactions)

    def _set_additional_data(self):
        logger.info("Setting speed")

        def set_speed():
            logger.info("Setting speed")
            self.interactions[0].mouse.speed = Speed2D(0, 0, 0)
            self.interactions[0].mouse.acceleration = Speed2D(0, 0, 0)
            helper = self.interactions[0].url

            for i, obj in enumerate(self.interactions):
                if i == 0:
                    continue

                prev = self.interactions[i - 1]
                if obj.url == helper and (obj.timestamp - prev.timestamp) < 200:
                    # There may be objects with the same timestamp, generated by an
                    # interaction and the webcam at the same time. In that case, simply clone
                    # the previous object's speed
                    if obj.timestamp == prev.timestamp:
                        obj.mouse.speed = copy(prev.mouse.speed)
                        obj.mouse.acceleration = copy(prev.mouse.acceleration)
                        continue

                    obj.mouse.speed = speed(
                        prev.mouse.position,
                        obj.mouse.position,
                        obj.timestamp - prev.timestamp
                    )
                    obj.mouse.acceleration = acceleration(
                        prev.mouse.speed,
                        obj.mouse.speed,
                        obj.timestamp - prev.timestamp
                    )
                else:
                    obj.mouse.speed = Speed2D(0, 0, 0)
                    obj.mouse.acceleration = Speed2D(0, 0, 0)
                    helper = obj.url

        def set_directions():
            logger.info("Setting direction")
            for obj in self.interactions:
                if obj.mouse.speed.y == 0 and obj.mouse.speed.x == 0:
                    obj.slope = None
                elif obj.mouse.speed.x == 0:
                    obj.slope = float('inf')
                else:
                    obj.slope = obj.mouse.speed.y / obj.mouse.speed.x

        set_speed()
        set_directions()

    def _get_intervals(self, width: float) -> Iterator[Range[int]]:
        def has_emotions_over_value(obj: Interaction) -> bool:
            limit = 1.0
            return (obj.emotions.joy or -1) >= limit or \
                   (obj.emotions.fear or -1) >= limit or \
                   (obj.emotions.disgust or -1) >= limit or \
                   (obj.emotions.sadness or -1) >= limit or \
                   (obj.emotions.anger or -1) >= limit or \
                   (obj.emotions.surprise or -1) >= limit or \
                   (obj.emotions.contempt or -1) >= limit or \
                   (obj.emotions.valence or -1) >= limit or \
                   (obj.emotions.engagement or -1) >= limit

        def get_emotions_indexes() -> Iterator[int]:
            for i, obj in enumerate(self.interactions):
                if has_emotions_over_value(obj):
                    yield i

        for index in get_emotions_indexes():
            current_range = Range([], index, [])

            for i in range(max(math.floor(index - width / 2), 0), index):
                if self.interactions[i].timestamp >= self.interactions[index].timestamp - width / 2:
                    current_range.preceding.append(i)

            for i in range(index + 1, min(math.floor(index + width / 2) + 1, len(self.interactions))):
                if self.interactions[i].timestamp > self.interactions[index].timestamp + width / 2:
                    break
                current_range.following.append(i)
            yield current_range

    @timed("Analyzed all intervals in %.3fs")
    def process_intervals(self, range_width: float) -> Dict[int, IntervalData]:
        logger.info("Getting intervals of %d milliseconds", range_width)
        temp_intervals = self._get_intervals(range_width)
        logger.info("Calculating aggregate data on intervals")
        intervals = dict()
        for interactions_range in temp_intervals:
            intervals[interactions_range.middle] = self._process_single_interval(interactions_range, range_width)
        logger.info("Running garbage collector")
        gc.collect()
        return intervals

    def _get_direction_changes(self, interactions: Range[int], range_width: float) -> RangeData[DirectionStatistics]:
        def direction_changes(indexes: Iterator[int], width) -> DirectionStatistics:
            changes = 0
            indexes, following = itertools.tee(indexes)
            next(following, None)
            for prev_index, index in zip(indexes, following):
                obj = self.interactions[index]
                prev = self.interactions[prev_index]
                if obj.slope != prev.slope:
                    changes += 1
            return DirectionStatistics(changes=changes, change_rate=changes / width)

        return RangeData(
            full=direction_changes(interactions.full, range_width),
            before=direction_changes(interactions.first_half, range_width / 2),
            after=direction_changes(interactions.second_half, range_width / 2)
        )

    def _get_mouse_movements(self, interactions: Range[int], range_width: float) -> RangeData[RateStats]:
        def mouse_movements_per_milliseconds(indexes: Iterator[int], width: float) -> RateStats:
            count = 0
            current_position = self.interactions[next(indexes)].mouse.position
            for i in indexes:
                new_position = self.interactions[i].mouse.position
                if new_position != current_position:
                    count += 1
                    current_position = new_position

            return RateStats(rate=count / width, total=count)

        return RangeData(
            full=mouse_movements_per_milliseconds(interactions.full, range_width),
            before=mouse_movements_per_milliseconds(interactions.first_half, range_width / 2),
            after=mouse_movements_per_milliseconds(interactions.second_half, range_width / 2)
        )

    def _get_scrolls(self, interactions: Range[int], range_width: float) -> RangeData[RateStats]:
        def scrolls_per_milliseconds(indexes: Iterator[int], width: float) -> RateStats:
            count = 0
            first = next(indexes)
            current_absolute = self.interactions[first].scroll.absolute
            current_relative = self.interactions[first].scroll.relative
            for obj in indexes:
                new_absolute = self.interactions[obj].scroll.absolute
                new_relative = self.interactions[obj].scroll.relative
                if new_absolute != current_absolute or new_relative != current_relative:
                    count += 1
                    current_absolute = new_absolute
                    current_relative = new_relative

            return RateStats(rate=count / width, total=count)

        return RangeData(
            full=scrolls_per_milliseconds(interactions.full, range_width),
            before=scrolls_per_milliseconds(interactions.first_half, range_width / 2),
            after=scrolls_per_milliseconds(interactions.second_half, range_width / 2)
        )

    def _get_average_speed(self, interactions: Range[int]) -> RangeData[
        Tuple[BasicStats, BasicStats, BasicStats]]:
        def average_speed(interactions: Iterator[int]) -> Tuple[BasicStats, BasicStats, BasicStats]:
            speeds = ([], [], [])
            size = 0

            for obj in interactions:
                speeds[0].append(self.interactions[obj].mouse.speed.total)
                speeds[1].append(self.interactions[obj].mouse.speed.x)
                speeds[2].append(self.interactions[obj].mouse.speed.y)
                size += 1

            total = tuple(sum(s) for s in speeds)
            avg = tuple(t / size if size > 0 else 0 for t in total)
            stdev = tuple(
                sum((s - mean) ** 2 for s in speeds[i]) / size if size > 0 else 0 for i, mean in enumerate(avg))

            return BasicStats(sum=total[0], avg=avg[0], std=stdev[0]), \
                   BasicStats(sum=total[1], avg=avg[1], std=stdev[1]), \
                   BasicStats(sum=total[2], avg=avg[2], std=stdev[2])

        return RangeData(
            full=average_speed(interactions.full),
            before=average_speed(interactions.first_half),
            after=average_speed(interactions.second_half)
        )

    def _get_average_acceleration(self, interactions: Range[int]) -> RangeData[
        Tuple[BasicStats, BasicStats, BasicStats]]:
        def average_acceleration(indexes: Iterator[int]) -> Tuple[BasicStats, BasicStats, BasicStats]:
            acc = ([], [], [])
            size = 0

            for obj in indexes:
                acc[0].append(self.interactions[obj].mouse.acceleration.total)
                acc[1].append(self.interactions[obj].mouse.acceleration.x)
                acc[2].append(self.interactions[obj].mouse.acceleration.y)
                size += 1

            total = tuple(sum(s) for s in acc)
            avg = tuple(t / size if size > 0 else 0 for t in total)
            stdev = tuple(
                sum((s - mean) ** 2 for s in acc[i]) / size if size > 0 else 0 for i, mean in enumerate(avg))

            return BasicStats(sum=total[0], avg=avg[0], std=stdev[0]), \
                   BasicStats(sum=total[1], avg=avg[1], std=stdev[1]), \
                   BasicStats(sum=total[2], avg=avg[2], std=stdev[2])

        return RangeData(
            full=average_acceleration(interactions.full),
            before=average_acceleration(interactions.first_half),
            after=average_acceleration(interactions.second_half)
        )

    def _get_clicks_statistics(self, interactions: Range[int], range_width: float) -> RangeData[Clicks[BasicStats]]:
        def clicks_statistics(indexes: List[int], width: float) -> Clicks[BasicStats]:
            def number_of_clicks() -> Clicks[int]:
                clicks_stats = Clicks(0, 0, 0, 0, 0)
                for i in indexes:
                    if not self.interactions[i].mouse.clicks.any:
                        continue
                    clicks_stats.all += 1
                    if self.interactions[i].mouse.clicks.left:
                        clicks_stats.left += 1
                    if self.interactions[i].mouse.clicks.middle:
                        clicks_stats.middle += 1
                    if self.interactions[i].mouse.clicks.right:
                        clicks_stats.right += 1
                    if self.interactions[i].mouse.clicks.others:
                        clicks_stats.other += 1

                return clicks_stats

            clicks = number_of_clicks()

            if not indexes:
                no_clicks = BasicStats(0, 0, 0)
                return Clicks(no_clicks, no_clicks, no_clicks, no_clicks, no_clicks)
            elif len(indexes) == 1:
                left = BasicStats(clicks.left, clicks.left, 0)
                middle = BasicStats(clicks.middle, clicks.middle, 0)
                right = BasicStats(clicks.right, clicks.right, 0)
                other = BasicStats(clicks.other, clicks.other, 0)
                all = BasicStats(clicks.all, clicks.all, 0)
                return Clicks(all, left, middle, right, other)

            # left button
            avg = clicks.left / width
            std_dev = sum([(int(self.interactions[i].mouse.clicks.left) - avg) ** 2 for i in indexes]) / len(indexes)
            left = BasicStats(clicks.left, avg, std_dev)

            # middle button
            avg = clicks.middle / width
            std_dev = sum([(int(self.interactions[i].mouse.clicks.middle) - avg) ** 2 for i in indexes]) / len(indexes)
            middle = BasicStats(clicks.middle, avg, std_dev)

            # right button
            avg = clicks.right / width
            std_dev = sum([(int(self.interactions[i].mouse.clicks.right) - avg) ** 2 for i in indexes]) / len(indexes)
            right = BasicStats(clicks.right, avg, std_dev)

            # other buttons
            avg = clicks.other / width
            std_dev = sum([(int(self.interactions[i].mouse.clicks.others) - avg) ** 2 for i in indexes]) / len(indexes)
            other = BasicStats(clicks.other, avg, std_dev)

            # all buttons
            avg = clicks.all / width
            std_dev = sum([(int(self.interactions[i].mouse.clicks.any) - avg) ** 2 for i in indexes]) / len(indexes)
            all = BasicStats(clicks.all, avg, std_dev)

            return Clicks(all, left, middle, right, other)

        return RangeData(
            full=clicks_statistics(list(interactions.full), range_width),
            before=clicks_statistics(list(interactions.first_half), range_width / 2),
            after=clicks_statistics(list(interactions.second_half), range_width / 2)
        )

    def _get_keyboard_statistics(self, interactions: Range[int], range_width: float) -> RangeData[Keyboard[BasicStats]]:
        def keyboard_statistics(indexes: List[int], width: float) -> Keyboard[BasicStats]:
            def number_of_keys() -> Keyboard[int]:
                n_all = 0
                n_alphabetic = 0
                n_numeric = 0
                n_symbol = 0
                n_function = 0
                for i in indexes:
                    if not self.interactions[i].keyboard.any:
                        continue
                    n_all += 1
                    if self.interactions[i].keyboard.alpha:
                        n_alphabetic += 1
                    if self.interactions[i].keyboard.numeric:
                        n_numeric += 1
                    if self.interactions[i].keyboard.symbol:
                        n_symbol += 1
                    if self.interactions[i].keyboard.function:
                        n_function += 1

                return Keyboard(
                    all=n_all,
                    alphabetic=n_alphabetic,
                    numeric=n_numeric,
                    symbol=n_symbol,
                    function=n_function,
                    alphanumeric=n_alphabetic + n_numeric
                )

            keys = number_of_keys()

            if not indexes:
                no_keys = BasicStats(0, 0, 0)
                return Keyboard(no_keys, no_keys, no_keys, no_keys, no_keys, no_keys)
            elif len(indexes) == 1:
                all = BasicStats(keys.all, keys.all, 0)
                alpha = BasicStats(keys.alphabetic, keys.alphabetic, 0)
                numeric = BasicStats(keys.numeric, keys.numeric, 0)
                symbol = BasicStats(keys.symbol, keys.symbol, 0)
                function = BasicStats(keys.function, keys.function, 0)
                alphanum = BasicStats(keys.alphanumeric, keys.alphanumeric, 0)
                return Keyboard(
                    all=all,
                    alphabetic=alpha,
                    numeric=numeric,
                    symbol=symbol,
                    function=function,
                    alphanumeric=alphanum
                )

            # all keys
            avg = keys.all / width
            std_dev = sum([(int(self.interactions[i].keyboard.any) - avg) ** 2 for i in indexes]) / len(indexes)
            all = BasicStats(keys.all, avg, std_dev)

            # alphabetic keys
            avg = keys.alphabetic / width
            std_dev = sum([(int(self.interactions[i].keyboard.alpha) - avg) ** 2 for i in indexes]) / len(indexes)
            alpha = BasicStats(keys.alphabetic, avg, std_dev)

            # numeric keys
            avg = keys.numeric / width
            std_dev = sum([(int(self.interactions[i].keyboard.numeric) - avg) ** 2 for i in indexes]) / len(indexes)
            numeric = BasicStats(keys.numeric, avg, std_dev)

            # symbol keys
            avg = keys.symbol / width
            std_dev = sum([(int(self.interactions[i].keyboard.symbol) - avg) ** 2 for i in indexes]) / len(indexes)
            symbol = BasicStats(keys.symbol, avg, std_dev)

            # function keys
            avg = keys.function / width
            std_dev = sum([(int(self.interactions[i].keyboard.function) - avg) ** 2 for i in indexes]) / len(indexes)
            function = BasicStats(keys.function, avg, std_dev)

            # alphanumeric keys
            avg = keys.alphanumeric / width
            std_dev = sum(
                [(int(self.interactions[i].keyboard.alpha or self.interactions[i].keyboard.numeric) - avg) ** 2 for i in
                 indexes]) / len(
                indexes)
            alphanum = BasicStats(keys.alphanumeric, avg, std_dev)

            return Keyboard(
                all=all,
                alphabetic=alpha,
                numeric=numeric,
                symbol=symbol,
                function=function,
                alphanumeric=alphanum
            )

        return RangeData(
            full=keyboard_statistics(list(interactions.full), range_width),
            before=keyboard_statistics(list(interactions.first_half), range_width / 2),
            after=keyboard_statistics(list(interactions.second_half), range_width / 2)
        )

    def _get_urls_statistics(self, interactions: Range[int], range_width: float) -> RangeData[VisitedWebsites]:
        def websites_statistics(indexes: Iterator[int], width: float = None) -> VisitedWebsites:
            first = next(indexes)
            last_url = self.interactions[first].url
            unique = {last_url}
            changed = 0
            for obj in indexes:
                if self.interactions[obj].url == last_url:
                    continue
                last_url = self.interactions[obj].url
                unique.add(last_url)
                changed += 1

            change_rate = changed / width if width is not None else None

            return VisitedWebsites(len(unique), changed, change_rate)

        return RangeData(
            full=websites_statistics(interactions.full, range_width),
            before=websites_statistics(interactions.first_half, range_width / 2),
            after=websites_statistics(interactions.second_half, range_width / 2)
        )

    def _get_event_times(self, interactions: Range[int]) -> RangeData[BasicStats]:
        def average_events_time(indexes: Iterator[int]) -> BasicStats:
            indexes, following = itertools.tee(indexes)
            next(following, None)
            times = [self.interactions[index].timestamp - self.interactions[prev_index].timestamp for prev_index, index
                     in zip(indexes, following)]
            return BasicStats(sum(times), statistics.mean(times), statistics.stdev(times)) if len(
                times) > 1 else BasicStats(0, 0, 0)

        return RangeData(
            full=average_events_time(interactions.full),
            before=average_events_time(interactions.first_half),
            after=average_events_time(interactions.second_half)
        )

    def _get_average_idle_time(self, interactions: Range[int]) -> RangeData[BasicStats]:
        def average_idle_time(indexes: Iterator[int]) -> BasicStats:
            idle_times = []
            current_idle = 0
            indexes, following = itertools.tee(indexes)
            next(following)
            for prev, obj in zip(indexes, following):
                changed = self.interactions[obj].get_changed_features(self.interactions[prev])
                if not changed:
                    current_idle += self.interactions[obj].timestamp - self.interactions[prev].timestamp
                else:
                    idle_times.append(current_idle)
                    current_idle = 0

            if current_idle != 0 or not idle_times:
                idle_times.append(current_idle)

            return BasicStats(sum(idle_times), statistics.mean(idle_times), statistics.stdev(idle_times)) if len(
                idle_times) > 1 else BasicStats(0, 0, 0)

        return RangeData(
            full=average_idle_time(interactions.full),
            before=average_idle_time(interactions.first_half),
            after=average_idle_time(interactions.second_half)
        )

    def _process_single_interval(self, interactions_range: Range[int], range_width: float) -> IntervalData:
        intervals = IntervalData(interactions_range.middle)

        intervals.slopes = self._get_direction_changes(interactions_range, range_width)
        intervals.mouse_movements = self._get_mouse_movements(interactions_range, range_width)
        intervals.scrolls = self._get_scrolls(interactions_range, range_width)
        intervals.avg_speed = self._get_average_speed(interactions_range)
        intervals.avg_acceleration = self._get_average_acceleration(interactions_range)
        intervals.clicks = self._get_clicks_statistics(interactions_range, range_width)
        intervals.keys = self._get_keyboard_statistics(interactions_range, range_width)
        intervals.urls = self._get_urls_statistics(interactions_range, range_width)
        intervals.event_times = self._get_event_times(interactions_range)
        intervals.idle = self._get_average_idle_time(interactions_range)

        return intervals

    def set_website_categories(self, websites: Dict[str, Website]) -> None:
        logger.info("Setting websites categories")
        for obj in self.interactions:
            obj.url_category = websites.get(obj.url, Website(None)).category

    def to_csv(self, *filename: str, mode: str = 'w'):
        dest_path = os.path.join(*filename)

        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, mode=mode, encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, self.interactions[0].to_dict().keys())
            if mode != 'a' and mode != 'ab':
                writer.writeheader()

            writer.writerows(o.to_dict() for o in self.interactions)
