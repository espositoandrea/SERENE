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

import typing
import re
import matplotlib.pyplot as plt
from .data import CollectedData


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


def plot_mouse_on_common_websites(collection: typing.List[CollectedData]) -> None:
    """Plot various graph containing the mouse movement on websites commonly used by all users.

    Parameters
    ----------
    user : set [User]
        The users.
    collection : list [CollectedData]
        The collected data.
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

    common_urls = get_common_urls(collection)

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
