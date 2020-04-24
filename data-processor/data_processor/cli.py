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
import re
import matplotlib.pyplot as plt
from . import __version__, __author__
from .user import User
from .data import CollectedData


def main():
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

    new_collection = {}
    for document in collection:
        if document.user not in new_collection:
            new_collection[document.user] = []
        if (len(new_collection[document.user]) == 0
                or document.url != new_collection[document.user][-1]['url']):
            new_collection[document.user].append({
                'url': document.url,
                'positions': [list(document.mouse.position)],
                'window': list(document.window)
            })
        else:
            new_collection[document.user][-1]['positions'].append(
                list(document.mouse.position))

    temp = {}
    for user in new_collection:
        if user not in temp:
            temp[user] = set()
        for element in new_collection[user]:
            temp[user].add(element['url'])
    common_urls = None
    for user in temp:
        if common_urls is None:
            common_urls = temp[user]
            continue
        common_urls = common_urls.intersection(temp[user])

    j = 1
    for url in common_urls:
        fig, axs = plt.subplots(1, 2, sharex=False, sharey=False)
        index = 0
        for user in new_collection:
            url_list = [e['url'] for e in new_collection[user]]
            element_indes = url_list.index(url)
            window_size = new_collection[user][element_indes]['window']

            axs[index].set_aspect('equal')  # window_size[1] / window_size[0]
            axs[index].set_xlim([0, window_size[0]])
            axs[index].set_ylim([window_size[1], 0])
            axs[index].set_xticklabels([])
            axs[index].set_yticklabels([])

            mouse_positions = new_collection[user][element_indes]['positions']
            x_vals = [p[0] for p in mouse_positions]
            y_vals = [p[1] for p in mouse_positions]

            axs[index].plot(x_vals, y_vals, '-r')
            axs[index].plot(x_vals, y_vals, '.b')

            url_to_print = re.match(r"https?://(.*?)/", url)[1]
            axs[index].set_title(user.user_id)

            fig.suptitle(url_to_print)

            index += 1
        plt.figure(j)
        j += 1

    plt.show()
