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
import gc
import logging
import math
import os
import shutil
import time

import coloredlogs
import pymongo
import urllib3

import analyzer
from . import utilities
from .data import *
from .process import process_user


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
        '--no-gc',
        action='store_false',
        dest="gc_enabled",
        help='Disable explicit calls to garbage collection.'
    )
    parser.add_argument(
        '--multiprocess',
        action='store_true',
        dest="multiprocessing_enabled",
        help='Enables multiprocessing (it will use all the available CPU minus two).'
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
        '--no-log',
        help="Disable the generation of the logfile",
        action='store_true',
        dest='no_log'
    )
    return parser.parse_args()


def main():
    urllib3.disable_warnings()
    gc.enable()

    args = set_up_args()

    logger = logging.getLogger('analyzer')
    logger.setLevel(logging.INFO)
    if not args.quiet:
        coloredlogs.install(
            level=logging.INFO,
            logger=logger,
            fmt="[%(levelname)s] %(asctime)s (%(name)s) %(message)s",
        )
    if not args.no_log:
        if not os.path.exists(args.out):
            os.makedirs(args.out, exist_ok=True)
        file_handler = logging.FileHandler('{}/report.log'.format(args.out), mode='w')
        file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s (%(name)s) %(message)s"))
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    if args.drop and os.path.exists(args.out) and os.listdir(args.out):
        logger.info("Emptying output directory ('%s')", os.path.abspath(args.out))
        shutil.rmtree(args.out, ignore_errors=True)

    if args.test:
        os.environ['TESTING_MODE'] = 'True'

    db = None
    if args.db:
        db = pymongo.MongoClient(args.db).get_default_database()

    users, __ = load_users(mongodb=db)

    if args.test:
        logger.warning("Users limited to the first two IDs for testing purposes.")
        users = dict(list(users.items())[0:2])

    logger.info("Saving users")
    utilities.to_csv(users, args.out, 'users.csv')

    websites, __ = load_websites(mongodb=db)
    logger.info("Saving websites")
    utilities.to_csv(websites, args.out, 'websites.csv')

    start_time = time.time()
    user_times = list()
    if args.user:
        users = [args.user]
    for i, user in enumerate(users, 1):
        __, t = process_user(user, websites, db=db, index=i, total_users=len(users), enable_gc=args.gc_enabled, enable_multiprocessing=args.multiprocessing_enabled)
        user_times.append(t)

    end_time = time.time()
    total_time = end_time - start_time
    logger.info("DONE after %.3fs", total_time)
    avg = sum(user_times) / len(user_times)
    std = math.sqrt(sum([(x - avg) ** 2 for x in user_times]) / len(user_times))
    logger.info("AVERAGE TIME PER USER: %.3fs (SD: %.3fs)", avg, std)
    if args.zip:
        logger.info("Zipping output folder")
        zip_path = os.path.join(args.out, '..', os.path.basename(args.out))
        shutil.make_archive(zip_path, 'zip', args.out)
