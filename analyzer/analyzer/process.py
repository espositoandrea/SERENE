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
import os
from typing import Dict

import pymongo.database as db
import multiprocessing

from . import utilities
from .data import *
from .decorators import timed


@timed("User done in %.3fs")
def process_user(user: str, websites: Dict[str, Website], db: db.Database, index: int = 1,
                 total_users: int = 1, out_dir: str = 'out') -> None:
    logger = logging.getLogger(__name__)
    logger.info("Running garbage collector")
    gc.collect()
    logger.info("Processing data by user '%s' (%d of %d)", str(user), index, total_users)

    interactions, __ = load_interactions(mongodb=db, user=user)
    if not interactions:
        logger.warning("No interactions from the user")
        return
    interactions.set_website_categories(websites)

    interactions.to_csv(out_dir, user, 'interactions.csv')

    logger.info("Getting intervals")
    intervals = {}
    ranges_widths = [
        # t = 100 ms is the time between two captured emotions
        25,  # 1/4 * t
        50,  # 1/2 * t
        100,  # 1 * t
        200,  # 2 * t
        500,  # 5 * t
        1000,  # 10 * t
        2000  # 20 * t
    ]
    with multiprocessing.Pool() as pool:
        for data, __ in pool.map(interactions.process_intervals, ranges_widths):
            intervals.update(data)

    logger.info("Saving aggregate data")
    utilities.to_csv(utilities.aggregate_data_to_list(intervals, interactions), out_dir, user, 'aggregate.csv')
