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

import argparse
import datetime
import logging
import math
import os
import time

import coloredlogs
import pymongo
import urllib3

import analyzer
from analyzer.features import average_speed, clicks_statistics, keyboard_statistics, websites_statistics, \
    interactions_set_speed, interactions_set_website_categories, scrolls_per_milliseconds, \
    mouse_movements_per_milliseconds, average_idle_time, average_events_time, interactions_set_directions, \
    average_direction
from . import plotting
from .data import *
from .interval import interactions_split_intervals, interactions_from_range, flatten_range
from .report import Report


def set_up_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=analyzer.__prog__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=analyzer.__doc__,
        epilog=f"Copyright (C) 2020 {analyzer.__author__}. Released under the GNU GPL v3 License."
    )
    parser.add_argument(
        '--db',
        metavar='URI',
        help="A MongoDB connection string to be used to fetch the data."
             "If it's not available, the web API will be used."
    )
    parser.add_argument(
        "--version",
        help="output version information and exit",
        action='version',
        version=analyzer.__disclaimer__
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in testing mode: the amount of data processed is significantly smaller.'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Run the program in quiet mode (nothing will be printed to the console).'
    )
    return parser.parse_args()


def main():
    urllib3.disable_warnings()

    args = set_up_args()

    logger = logging.getLogger('analyzer')
    coloredlogs.install(
        level=logging.INFO if not args.quiet else logging.CRITICAL,
        logger=logger,
        fmt="[%(levelname)s] %(asctime)s (%(name)s) %(message)s"
    )

    if args.test:
        os.environ['TESTING_MODE'] = 'True'

    db = None
    source_description = "web APIs"
    if args.db:
        db = pymongo.MongoClient(args.db).get_default_database()
        source_description = "MongoDB"

    Report.section("Load the Users")
    start_time = time.time()
    users = load_users(mongodb=db)
    Report.text(
        f"Loaded {len(users)} users from {source_description} in {round(time.time() - start_time, 3)} seconds.")

    if args.test:
        Report.text("Users limited to the first two IDs for testing purposes.")
        logger.warning("Users limited to the first two IDs for testing purposes.")
        users = dict(list(users.items())[0:2])

    Report.table([u.to_dict() for u in users.values()], caption='Loaded users', id_col='_id')

    Report.figure(plotting.plot_to_data_uri(plotting.plot_user_basic_info(users)), caption="Users details")

    Report.section("Load the Websites")
    start_time = time.time()
    websites = load_websites(mongodb=db)
    Report.text(
        f"Loaded {len(websites)} websites from {source_description} in {round(time.time() - start_time, 3)} seconds.")
    Report.table([w.to_dict() for w in list(websites.values())[0:5]], caption="The first loaded websites", id_col='url')
    Report.figure(plotting.plot_to_data_uri(plotting.plot_websites_categories(websites)), caption="Website categories")

    start_time = time.time()
    Report.section("Process the Data")
    processing_summary = Report.text('')
    user_times = list()
    for i, user in enumerate(users, 1):
        user_start_time = time.time()
        Report.subsection(f"Processing Data by User '{user}' ({i} of {len(users)})")
        Report.text(
            f"Started processing the user at {datetime.datetime.utcfromtimestamp(user_start_time).isoformat(sep=' ', timespec='seconds')}.")
        logger.info("Processing data by user '%s' (%d of %d)", str(user), i, len(users))

        interactions = load_interactions(mongodb=db, user=user)
        if not interactions:
            user_end_time = time.time()
            user_times.append(user_end_time - user_start_time)
            logger.warning("No interactions from the user")
            Report.text(
                f"No interactions by the user. Ended processing the user at {datetime.datetime.utcfromtimestamp(user_end_time).isoformat(sep=' ', timespec='seconds')}, after {round(user_times[-1], 3)} seconds.")
            logger.info("User done in %.3fs", user_times[-1])
            continue

        end_text = Report.text()

        interactions.sort(key=lambda obj: obj.timestamp)
        interactions_set_speed(interactions)
        interactions_set_directions(interactions)
        interactions_set_website_categories(interactions, websites)

        intervals = {}
        for range_width in [600]:
            Report.subsubsection(f"Range Width: {range_width} ms")
            intervals[range_width] = [interactions_from_range(interactions, r) for r in
                                      interactions_split_intervals(interactions, range_width)]

            for interactions_range in intervals[range_width]:
                slopes = dict()
                slopes["full"] = average_direction(flatten_range(interactions_range))
                slopes["before"] = average_direction(
                    interactions_range.preceding + [interactions_range.middle])
                slopes["after"] = average_direction([interactions_range.middle] + interactions_range.following)

                mouse_movements = dict()
                mouse_movements["full"] = mouse_movements_per_milliseconds(flatten_range(interactions_range),
                                                                           range_width)
                mouse_movements["before"] = mouse_movements_per_milliseconds(
                    interactions_range.preceding + [interactions_range.middle], range_width / 2)
                mouse_movements["after"] = mouse_movements_per_milliseconds(
                    [interactions_range.middle] + interactions_range.following, range_width / 2)

                scrolls = dict()
                scrolls["full"] = scrolls_per_milliseconds(flatten_range(interactions_range), range_width)
                scrolls["before"] = scrolls_per_milliseconds(interactions_range.preceding + [interactions_range.middle],
                                                             range_width / 2)
                scrolls["after"] = scrolls_per_milliseconds([interactions_range.middle] + interactions_range.following,
                                                            range_width / 2)

                avg_speed = dict()
                avg_speed["full"] = average_speed(flatten_range(interactions_range))
                avg_speed["before"] = average_speed(interactions_range.preceding + [interactions_range.middle])
                avg_speed["after"] = average_speed([interactions_range.middle] + interactions_range.following)

                # Click statistics
                clicks = dict()
                clicks["full"] = clicks_statistics(flatten_range(interactions_range), range_width)
                clicks["before"] = clicks_statistics(interactions_range.preceding + [interactions_range.middle],
                                                     range_width / 2)
                clicks["after"] = clicks_statistics([interactions_range.middle] + interactions_range.following,
                                                    range_width / 2)

                # keyboard statistics
                keys = dict()
                keys["full"] = keyboard_statistics(flatten_range(interactions_range), range_width)
                keys["before"] = keyboard_statistics(interactions_range.preceding + [interactions_range.middle],
                                                     range_width / 2)
                keys["after"] = keyboard_statistics([interactions_range.middle] + interactions_range.following,
                                                    range_width / 2)

                urls = dict()
                urls["full"] = websites_statistics(flatten_range(interactions_range), range_width)
                urls["before"] = websites_statistics(interactions_range.preceding + [interactions_range.middle],
                                                     range_width / 2)
                urls["after"] = websites_statistics([interactions_range.middle] + interactions_range.following,
                                                    range_width / 2)

                event_times = dict()
                event_times["full"] = average_events_time(flatten_range(interactions_range))
                event_times["before"] = average_events_time(interactions_range.preceding + [interactions_range.middle])
                event_times["after"] = average_events_time([interactions_range.middle] + interactions_range.following)

                idle = dict()
                idle["full"] = average_idle_time(flatten_range(interactions_range))
                idle["before"] = average_idle_time(interactions_range.preceding + [interactions_range.middle])
                idle["after"] = average_idle_time([interactions_range.middle] + interactions_range.following)

        user_end_time = time.time()
        user_times.append(user_end_time - user_start_time)
        end_text.text = f"Ended processing the user at {datetime.datetime.utcfromtimestamp(user_end_time).isoformat(sep=' ', timespec='seconds')}, after {round(user_times[-1], 3)} seconds."
        logger.info("User done in %.3fs", user_times[-1])

    end_time = time.time()
    logger.info("DONE after %.3fs", end_time - start_time)
    avg = sum(user_times) / len(user_times)
    std = math.sqrt(sum([(x - avg) ** 2 for x in user_times]) / len(user_times))
    logger.info("AVERAGE TIME PER USER: %.3fs (SD: %.3fs)", avg, std)
    processing_summary.text = f"A total of {len(users)} users have been processed in {round(end_time - start_time, 3)} seconds, with an average of {round(avg, 3)} seconds per user (standard deviation: {round(std, 3)} seconds)."
    Report.html('report.html')
