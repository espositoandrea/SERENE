# This file is part of 'data-processor', the tool used to process the information
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

import argparse
import logging
from . import __version__, __author__
from .data import CollectedData, User
from .plotting import plot_mouse_on_common_websites


def main():
    """The main entry point.
    """
    parser = argparse.ArgumentParser(
        description='Process the JSON file',
        prog='data-processor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', help='The file')
    parser.add_argument(
        'users',
        help='A JSON file containing the users'
    )
    parser.add_argument(
        "--version",
        help="output version information and exit",
        action='version',
        version=f'%(prog)s (v{__version__}) Copyright (C) 2020 {__author__}\n\n'
        'License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n'
        'This program comes with ABSOLUTELY NO WARRANTY, to the extent permitted by law.\n'
        'This is free software, and you are welcome to redistribute it\n'
        'under certain conditions (see the License for more details).\n\n'
        f'Written by {__author__}'
    )
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(levelname)s - %(asctime)s - %(name)s - %(message)s')

    # add formatter to console_handler
    console_handler.setFormatter(formatter)

    # add console_handler to logger
    logger.addHandler(console_handler)

    with open(args.users, 'r') as file:
        users = set(User.from_json(file.read()))
    logger.info('Loaded %(number)d users', number=len(users))

    with open(args.file, 'r') as file:
        collection = CollectedData.from_json(users, file.read())
    logger.info('Loaded %(number)d interaction objects',
                number=len(collection))

    plot_mouse_on_common_websites(collection)
