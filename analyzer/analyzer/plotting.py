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

"""A module to plot data.

This module contains various definition of various function that plot the data
on various graph types.
"""

import typing
import re
import logging
import matplotlib.pyplot as plt
from .data import CollectedData, User


logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_common_urls(collection: typing.List[CollectedData]) -> typing.Set[str]:
    """Get all the urls visited by all the users in a collection.

    Parameters
    ----------
    collection : list [CollectedData]
        A list of data.

    Returns
    -------
    set [str]
        A set of URLs visited by all the users in the ``collection``.
    """
    temp = {}
    for element in collection:
        if element.user not in temp:
            temp[element.user] = set()
        temp[element.user].add(element.url)

    common_urls = None
    for element in collection:
        if common_urls is None:
            common_urls = temp[element.user]
            continue
        common_urls = common_urls.intersection(temp[element.user])

    return common_urls


def convert_collection(collection: typing.List[CollectedData]) \
        -> typing.Dict[User, typing.List[typing.Dict[str, typing.Any]]]:
    """Convert a collection to a dictionary.

    This function converts a collection of CollectedData to a dictionary that
    has users as key and all their related data (grouped by URL and visit) as
    values.

    Returns
    -------
    dict [User, list [dict [str, any]]]
        A dictionary that, for each user, holds all the collected data grouped
        by URL an time of visit. This means that two visit in two different
        times to the same website, will result in two different objects in
        this dictionary's value.
    """
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

    return new_collection


def plot_mouse_on_common_websites(collection: typing.List[CollectedData]) \
        -> None:
    """Plot various graph containing the mouse movement on websites commonly
    used by all users.

    Parameters
    ----------
    user : set [User]
        The users.
    collection : list [CollectedData]
        The collected data.
    """

    logging.getLogger(__name__).info(
        'Plotting mouse positions in all the common websites: START...'
    )

    common_urls = get_common_urls(collection)
    new_collection = convert_collection(collection)

    j = 1
    for url in common_urls:
        fig, axs = plt.subplots(1, 2, sharex=False, sharey=False)
        index = 0
        for user, data in new_collection.items():
            element_index = [e['url'] for e in data].index(url)
            window_size = data[element_index]['window']

            axs[index].set_aspect('equal')
            axs[index].set_xlim([0, window_size[0]])
            axs[index].set_ylim([window_size[1], 0])
            axs[index].set_xticklabels([])
            axs[index].set_yticklabels([])

            mouse_positions = data[element_index]['positions']

            # The mouse positions are assumed to start from (0, 0). For this
            # reason, all the (0, 0) positions at the start of the list.
            logging.getLogger(__name__).debug(
                'Cleaning mouse position list of user %s',
                user
            )
            while len(mouse_positions) > 0 and mouse_positions[0] == [0, 0]:
                mouse_positions.pop(0)

            x_vals = [p[0] for p in mouse_positions]
            y_vals = [p[1] for p in mouse_positions]

            axs[index].plot(x_vals, y_vals, '-r')
            axs[index].plot(x_vals, y_vals, '.b')

            axs[index].set_title(user.user_id)

            fig.suptitle(re.match(r"https?://(.*?)/", url)[1])

            index += 1
        plt.figure(j)
        j += 1

    logging.getLogger(__name__).info(
        '...END: Plotted mouse positions in all the common websites'
    )
    plt.show()
