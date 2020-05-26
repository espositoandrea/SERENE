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
import logging
import os

import pymongo
import urllib3

from .data import *
from . import __prog__, __disclaimer__

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
    help='Run the program in quiet mode'
)
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO if not args.quiet else logging.CRITICAL,
    format="[%(levelname)s] %(message)s"
)

if args.test:
    os.environ['TESTING_MODE'] = 'True'

db = None
if args.db:
    db = pymongo.MongoClient(args.db).get_default_database()
users = load_users(mongodb=db)
websites = load_websites(mongodb=db)
for i, user in enumerate(users, 1):
    logging.info('-' * 80)
    logging.info(f"Processing user '{user}' ({i} of {len(users)})".center(80))
    logging.info('-' * 80)
    interactions = load_interactions(mongodb=db, user=user)
# print(users)
# input()
# print(websites)
