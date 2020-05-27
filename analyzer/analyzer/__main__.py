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

from . import __prog__, __disclaimer__
from .data import *
from .report import Report


def main():
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(
        prog=__prog__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--db',
        metavar='URI',
        help="A MongoDB connection string to be used to fetch the data. If it's not available, the web API will be used."
    )
    parser.add_argument(
        "--version",
        help="output version information and exit",
        action='version',
        version=__disclaimer__
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Set the program to run in testing mode'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Run the program in quiet mode. By default, the program generates a report.'
    )
    args = parser.parse_args()

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
    Report.paragraph(
        f"Loaded {len(users)} users from {source_description} in {round(time.time() - start_time, 3)} seconds.")

    if args.test:
        Report.paragraph("Users limited to the first two IDs for testing purposes.")
        logger.warning("Users limited to the first two IDs for testing purposes.")
        users = dict(list(users.items())[0:2])

    Report.section("Load the Websites")
    start_time = time.time()
    websites = load_websites(mongodb=db)
    Report.paragraph(
        f"Loaded {len(websites)} websites from {source_description} in {round(time.time() - start_time, 3)} seconds.")

    start_time = time.time()
    Report.section("Process the Data")
    processing_summary = Report.paragraph('')
    user_times = list()
    for i, user in enumerate(users, 1):
        user_start_time = time.time()
        Report.subsection(f"Processing Data by User '{user}' ({i} of {len(users)})")
        Report.paragraph(
            f"Started processing the user at {datetime.datetime.utcfromtimestamp(user_start_time).isoformat(sep=' ', timespec='seconds')}.")
        logger.info("Processing data by user '%s' (%d of %d)", str(user), i, len(users))

        interactions = load_interactions(mongodb=db, user=user)

        user_end_time = time.time()
        user_times.append(user_end_time - user_start_time)
        Report.paragraph(
            f"Ended processing the user at {datetime.datetime.utcfromtimestamp(user_end_time).isoformat(sep=' ', timespec='seconds')}, after {round(user_times[-1], 3)} seconds.")
        logger.info("User done in %.3fs", user_times[-1])

    end_time = time.time()
    logger.info("DONE after %.3fs", end_time - start_time)
    avg = sum(user_times) / len(user_times)
    std = math.sqrt(sum([(x - avg) ** 2 for x in user_times]) / len(user_times))
    logger.info("AVERAGE TIME PER USER: %.3fs (SD: %.3fs)", avg, std)
    processing_summary.text = f"A total of {len(users)} users have been processed in {round(end_time - start_time, 3)} seconds, with an average of {round(avg, 3)} seconds per user (standard deviation: {round(std, 3)} seconds)."
    Report.html('report.html')


if __name__ == "__main__":
    main()
