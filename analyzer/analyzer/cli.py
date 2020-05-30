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
import shutil
import time
import gc
import coloredlogs
import pymongo
import urllib3
from bson import ObjectId

import analyzer
from analyzer.features import average_speed, clicks_statistics, keyboard_statistics, websites_statistics, \
    interactions_set_speed, interactions_set_website_categories, scrolls_per_milliseconds, \
    mouse_movements_per_milliseconds, average_idle_time, average_events_time, interactions_set_directions, \
    direction_changes
from . import plotting
from . import utilities
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
        '--user',
        metavar='USER_ID',
        help="The user ID to analyze."
    )
    parser.add_argument(
        "--version", '-v',
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
    parser.add_argument(
        '--out', '-o',
        help='Set the output directory',
        default='out'
    )
    parser.add_argument(
        '--drop', '-d',
        action='store_true',
        help='Drop the output folder if it already exist.'
    )
    parser.add_argument(
        '--zip',
        help='Zip the output folder',
        action='store_true'
    )
    parser.add_argument(
        '--report',
        help="Set the output format of the report. Use 'none' to disable it",
        choices=['html', 'pdf', 'none', 'all'],
        metavar='FORMAT',
        default='html'
    )
    return parser.parse_args()


def main():
    urllib3.disable_warnings()
    gc.enable()

    args = set_up_args()

    logger = logging.getLogger('analyzer')
    coloredlogs.install(
        level=logging.INFO if not args.quiet else logging.CRITICAL,
        logger=logger,
        fmt="[%(levelname)s] %(asctime)s (%(name)s) %(message)s"
    )

    if args.drop and os.path.exists(args.out) and os.listdir(args.out):
        logger.info("Emptying output directory ('%s')", os.path.abspath(args.out))
        shutil.rmtree(args.out, ignore_errors=True)

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
    logger.info("Saving users")
    utilities.to_csv(users, args.out, 'users.csv')

    Report.figure(plotting.plot_to_data_uri(plotting.plot_user_basic_info(users)), caption="Users details")

    Report.section("Load the Websites")
    start_time = time.time()
    websites = load_websites(mongodb=db)
    Report.text(
        f"Loaded {len(websites)} websites from {source_description} in {round(time.time() - start_time, 3)} seconds.")
    Report.table([w.to_dict() for w in list(websites.values())[0:5]], caption="The first loaded websites", id_col='url')
    Report.figure(plotting.plot_to_data_uri(plotting.plot_websites_categories(websites)), caption="Website categories")
    logger.info("Saving websites")
    utilities.to_csv(websites, args.out, 'websites.csv')

    start_time = time.time()
    Report.section("Process the Data")
    processing_summary = Report.text('')
    user_times = list()
    if args.user:
        users = [args.user]
    for i, user in enumerate(users, 1):
        logger.info("Running garbage collector")
        gc.collect()
        user_start_time = time.time()
        Report.subsection(f"Processing Data by User “{user}” ({i} of {len(users)})")
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

        logger.info("Sorting by timestamps")
        interactions.sort(key=lambda obj: (obj.timestamp, ObjectId(obj._id).generation_time))
        logger.info("Setting speed")
        interactions_set_speed(interactions)
        logger.info("Setting direction")
        interactions_set_directions(interactions)
        logger.info("Setting websites categories")
        interactions_set_website_categories(interactions, websites)
        logger.info("Saving punctual data")
        utilities.to_csv(interactions, args.out, user, 'interactions.csv')

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
        report_range_list = Report.description_list()
        for range_width in ranges_widths:
            logger.info("Getting intervals of %d milliseconds", range_width)
            _, report_range_list_item = report_range_list.add_item(f"Range width: {range_width} ms.", "")
            temp_intervals = (interactions_from_range(interactions, r) for r in
                              interactions_split_intervals(interactions, range_width))
            report_range_list_item.text += f" Got the intervals using the given width ({range_width} ms)."
            interval_start_time = time.time()
            logger.info("Calculating aggregate data on intervals")
            for interactions_range in temp_intervals:
                if (interactions_range.middle._id, interactions_range.middle.timestamp) not in intervals:
                    intervals[(interactions_range.middle._id, interactions_range.middle.timestamp)] = dict()

                intervals[(interactions_range.middle._id, interactions_range.middle.timestamp)][range_width] = {
                    'slopes': {
                        'full': direction_changes(flatten_range(interactions_range), range_width),
                        'before': direction_changes(
                            interactions_range.preceding + [interactions_range.middle], range_width / 2),
                        'after': direction_changes([interactions_range.middle] + interactions_range.following,
                                                   range_width / 2)
                    },
                    'mouse_movements': {
                        'full': mouse_movements_per_milliseconds(flatten_range(interactions_range),
                                                                 range_width),
                        'before': mouse_movements_per_milliseconds(
                            interactions_range.preceding + [interactions_range.middle], range_width / 2),
                        'after': mouse_movements_per_milliseconds(
                            [interactions_range.middle] + interactions_range.following, range_width / 2)
                    },
                    'scrolls': {
                        'full': scrolls_per_milliseconds(flatten_range(interactions_range), range_width),
                        'before': scrolls_per_milliseconds(interactions_range.preceding + [interactions_range.middle],
                                                           range_width / 2),
                        'after': scrolls_per_milliseconds([interactions_range.middle] + interactions_range.following,
                                                          range_width / 2)
                    },
                    'avg_speed': {
                        'full': average_speed(flatten_range(interactions_range)),
                        'before': average_speed(interactions_range.preceding + [interactions_range.middle]),
                        'after': average_speed([interactions_range.middle] + interactions_range.following)
                    },
                    'clicks': {
                        'full': clicks_statistics(flatten_range(interactions_range), range_width),
                        'before': clicks_statistics(interactions_range.preceding + [interactions_range.middle],
                                                    range_width / 2),
                        'after': clicks_statistics([interactions_range.middle] + interactions_range.following,
                                                   range_width / 2)
                    },
                    'keys': {
                        'full': keyboard_statistics(flatten_range(interactions_range), range_width),
                        'before': keyboard_statistics(interactions_range.preceding + [interactions_range.middle],
                                                      range_width / 2),
                        'after': keyboard_statistics([interactions_range.middle] + interactions_range.following,
                                                     range_width / 2)
                    },
                    'urls': {
                        'full': websites_statistics(flatten_range(interactions_range), range_width),
                        'before': websites_statistics(interactions_range.preceding + [interactions_range.middle],
                                                      range_width / 2),
                        'after': websites_statistics([interactions_range.middle] + interactions_range.following,
                                                     range_width / 2)
                    },
                    'event_times': {
                        'full': average_events_time(flatten_range(interactions_range)),
                        'before': average_events_time(interactions_range.preceding + [interactions_range.middle]),
                        'after': average_events_time([interactions_range.middle] + interactions_range.following)
                    },
                    'idle': {
                        'full': average_idle_time(flatten_range(interactions_range)),
                        'before': average_idle_time(interactions_range.preceding + [interactions_range.middle]),
                        'after': average_idle_time([interactions_range.middle] + interactions_range.following)
                    }
                }
            logger.info("Running garbage collector")
            gc.collect()
            report_range_list_item.text += f" Interval analysis completed after {round(time.time() - interval_start_time, 3)} seconds."
            logger.info("Interval analysis completed after %.3f seconds", time.time() - interval_start_time)

        logger.info("Saving aggregate data")
        utilities.to_csv(utilities.aggregate_data_to_list(intervals), args.out, user, 'aggregate.csv')

        user_end_time = time.time()
        user_times.append(user_end_time - user_start_time)
        end_text.text = f"Ended processing the user at {datetime.datetime.utcfromtimestamp(user_end_time).isoformat(sep=' ', timespec='seconds')}, after {round(user_times[-1], 3)} seconds."
        logger.info("User done in %.3fs", user_times[-1])

    end_time = time.time()
    total_time = end_time - start_time
    logger.info("DONE after %.3fs", total_time)
    avg = sum(user_times) / len(user_times)
    std = math.sqrt(sum([(x - avg) ** 2 for x in user_times]) / len(user_times))
    logger.info("AVERAGE TIME PER USER: %.3fs (SD: %.3fs)", avg, std)
    processing_summary.text = f"A total of {len(users)} users have been processed in {round(total_time, 3)}" \
                              f"seconds, with an average of {round(avg, 3)} seconds per user (standard deviation: " \
                              f"{round(std, 3)} seconds). All the processed data have been saved to the directory “"
    Report.code(os.path.abspath(args.out), parent=processing_summary).tail = '”.'
    if args.zip:
        logger.info("Zipping output folder")
        zip_path = os.path.join(args.out, '..', os.path.basename(args.out))
        shutil.make_archive(zip_path, 'zip', args.out)

    if args.report == 'none':
        logger.info("Not writing report")
    else:
        args.report = 'html pdf' if args.report == 'all' else args.report
        if 'html' in args.report:
            logger.info("Writing report to HTML file")
            with open('report.html', mode='w', encoding='utf-8') as f:
                f.write(Report.html())
        if 'pdf' in args.report:
            logger.info("Writing report to PDF file")
            import weasyprint
            html = weasyprint.HTML(string=Report.html())
            html.write_pdf('report.pdf')
