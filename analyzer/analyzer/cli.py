# This file is part of 'analyzer', the tool used to process the information
# collected for Andrea Esposito's Thesis.
# Copyright (C) 2020  Andrea Esposito
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This module defines the CLI of the tool.

This module contains the definition of the Command Line Interface (CLI) of the
tool and its entry point.
"""

import argparse
import logging
import typing
import time
import coloredlogs
from . import __version__, __author__, __prog__, __disclaimer__
from .data import CollectedData, User, CollectedDataSeries
from .plotting import plot_mouse_on_common_websites


def phase(msg: str, *args, **kwargs):
    def decorator(f):
        def wrapper(*fargs, **fkargs):
            start_time = time.time()
            result = f(*fargs, **fkargs)
            logging.getLogger(kwargs.get('module', 'analyzer')).info(
                msg.format(len=len(result)) + ' after %.3f seconds',
                *args,
                time.time() - start_time
            )
            return result

        return wrapper

    return decorator


@phase('Loaded {len} users')
def load_users(file_name: str):
    with open(file_name, 'r') as file:
        users = set(User.from_json(file.read()))
    return users


@phase('Loaded {len} interaction objects')
def load_data(file_name: str, users: typing.Set['User']):
    with open(file_name, 'r') as file:
        collection = CollectedDataSeries(CollectedData.from_json(users, file.read()))
    return collection


def main():
    """The main entry point.
    """
    parser = argparse.ArgumentParser(
        description='Process the JSON file',
        prog=__prog__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'interactions',
        help='A JSON file containing the interactions'
    )
    parser.add_argument(
        'users',
        help='A JSON file containing the users'
    )
    parser.add_argument(
        "--version",
        help="output version information and exit",
        action='version',
        version=__disclaimer__
    )
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    args = parser.parse_args()

    logger = logging.getLogger('analyzer')
    coloredlogs.install(
        level='DEBUG' if args.verbose else 'INFO',
        logger=logger,
        fmt="[%(levelname)s] %(asctime)s (%(name)s) %(message)s"
    )

    start_time = time.time()
    logger.info('Start of execution')

    users = load_users(args.users)
    collection = load_data(args.interactions, users)

    collection.to_csv('output.csv')

    # data = collection.to_dataframe()
    # with open('data.html', 'w') as f:
    #     data.to_html(f)
    # data.to_excel('output.xlsx')

    # plot_mouse_on_common_websites(collection)

    logger.info('End of execution after %.3f seconds', time.time() - start_time)
