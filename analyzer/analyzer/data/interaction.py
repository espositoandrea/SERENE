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

import gc
import logging
import math
import os
import re
from typing import List, Dict, Any

import pymongo.database as db
import requests

from .base import *
from .emotions import Emotions


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


def load_interactions(mongodb: db.Database = None, user: str = None) -> List[Interaction]:
    def convert_object(to_convert: dict) -> Interaction:
        # noinspection PyArgumentList
        return Interaction(
            id=to_convert["_id"],
            user_id=to_convert.get("ui", None),
            timestamp=to_convert.get("t", None),
            url=to_convert.get("u", None),
            mouse=MouseData(
                position=ScreenCoordinates(*to_convert.get("m", {}).get("p", [None, None])),
                clicks=MouseData.Clicks(
                    any=any(to_convert.get("m", {}).get("b", {}).values()),
                    left=to_convert.get("m", {}).get("b", {}).get('l', False),
                    right=to_convert.get("m", {}).get("b", {}).get('r'),
                    middle=to_convert.get("m", {}).get("b", {}).get('m'),
                    others=any([value for key, value in to_convert.get("m", {}).get("b", {}).items() if
                                re.match(r"^b\d+?$", key)]),
                )
            ),
            scroll=ScrollData(
                absolute=ScreenCoordinates(*to_convert.get("s", {}).get("a", [None, None])),
                relative=ScreenCoordinates(*to_convert.get("s", {}).get("r", [None, None])),
            ),
            keyboard=KeyboardData(
                any=any(to_convert.get("k", {}).values()),
                alpha=to_convert.get("k", {}).get("a", None),
                numeric=to_convert.get("k", {}).get("n", None),
                function=to_convert.get("k", {}).get("f", None),
                symbol=to_convert.get("k", {}).get("s", None),
            ),
            emotions=Emotions(
                exists=to_convert.get("e", None) is None,
                joy=to_convert.get("e", {}).get("j", None),
                fear=to_convert.get("e", {}).get("f", None),
                disgust=to_convert.get("e", {}).get("d", None),
                sadness=to_convert.get("e", {}).get("s", None),
                anger=to_convert.get("e", {}).get("a", None),
                surprise=to_convert.get("e", {}).get("su", None),
                contempt=to_convert.get("e", {}).get("c", None),
                valence=to_convert.get("e", {}).get("v", None),
                engagement=to_convert.get("e", {}).get("e", None)
            )
        )

    logger = logging.getLogger(__name__)
    is_test_mode = os.getenv('TESTING_MODE', 'False') == 'True'
    testing_limit = 20000

    if mongodb:
        logger.info("Loading interactions from database...")
        interactions = mongodb['interactions'].find() if user is None else mongodb['interactions'].find({'ui': user})
        logger.info("Got %d objects", interactions.count())
        if is_test_mode:
            interactions.limit(testing_limit)

        interactions = [convert_object(obj) for obj in interactions]
    else:
        api_url = "https://giuseppe-desolda.ddns.net:8080/api/interactions/{}-{}" if user is None else f"https://giuseppe-desolda.ddns.net:8080/api/user/{user}/interactions/{{}}-{{}}"
        current_base = 0
        skip = 10000

        number_of_objects = int(requests.get(api_url[0:-5] + 'count', verify=False).text)
        expected_iterations = math.ceil(
            number_of_objects / skip) if not is_test_mode or number_of_objects < testing_limit else math.ceil(
            testing_limit / skip)

        if number_of_objects == 0:
            logger.warning("No data to load")
            return []

        interactions = list()
        while True:
            if is_test_mode and current_base >= testing_limit:
                break

            logger.info("Loading interactions from web APIs (iteration %d of %d)...", round(current_base / skip) + 1,
                        expected_iterations)
            db_content = requests.get(api_url.format(current_base, skip), verify=False).json()

            if not db_content:
                logger.info("Loaded interactions from web APIs (iteration %d of %d): empty",
                            round(current_base / skip) + 1, expected_iterations)
                break

            interactions.extend(convert_object(obj) for obj in db_content)
            current_base += skip
            logger.info("Loaded interactions from web APIs (iteration %d of %d)", round(current_base / skip),
                        expected_iterations)
            logger.info("Running garbage collector")
            gc.collect()

    logger.info("Done. Loaded %d interactions", len(interactions))

    # Remove duplicate timestamps
    # logger.info("Removing duplicate timestamps from interactions")
    # for ids in timestamps.values():
    #     if len(ids) <= 1:
    #         continue
    #     logger.info("Removing duplicates from [%s]", ", ".join(ids))

    #     objects = [obj for obj in interactions if obj._id in ids]
    #     not_emotions = list(filter(lambda obj: not obj.emotions.exists, objects))
    #     if len(objects) == len(not_emotions):
    #         to_remove = objects[1:]
    #     else:
    #         to_remove = not_emotions

    #     interactions = list(filter(lambda obj: obj not in to_remove, interactions))
    # logger.info("Done. New number of interactions: %d", len(interactions))

    return interactions
