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

from typing import Dict
import urllib.parse
import matplotlib.pyplot as plt
import io

from analyzer.data import User, Website


def plot_to_data_uri(fig: plt.Figure) -> str:
    svg = plot_to_svg(fig)
    return 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg.replace('\n', '').replace('\r', ''))


def plot_to_svg(fig: plt.Figure) -> str:
    f = io.StringIO()
    fig.savefig(f, format='svg')
    return f.getvalue()


def plot_user_basic_info(users: Dict[str, User]) -> plt.Figure:
    age_map = {
        0: '<= 18',
        1: '[18, 29]',
        2: '[30, 39]',
        3: '[40, 49]',
        4: '[50, 59]',
        5: '>= 60'
    }
    ages = [u.age for u in users.values()]
    sizes = [ages.count(i) for i in age_map]
    filtered_age_map = [v for k, v in age_map.items() if sizes[k] > 0]
    sizes = [u for u in sizes if u > 0]
    # print(sizes)
    fig1, (ax_age, ax_internet, ax_gender) = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Ages
    ax_age.pie(sizes, labels=filtered_age_map, autopct='%1.1f%%')
    ax_age.title.set_text("Age")
    ax_age.axis('equal')
    ax_age.legend(filtered_age_map)

    # Genders
    genders = {
        'm': 0,
        'f': 0,
        'a': 0
    }
    for user in users.values():
        genders[user.gender] += 1

    genders_values = [(k, v) for k, v in genders.items() if v > 0]
    ax_gender.pie([v for k, v in genders_values], labels=[k for k, v in genders_values], autopct='%1.1f%%')
    ax_gender.title.set_text("Gender")
    ax_gender.axis('equal')
    ax_gender.legend([{'m': 'Male', 'f': 'Female', 'o': 'Other'}[k] for k, v in genders_values])

    # Internet
    internet = [u.internet for u in users.values()]
    internet = [internet.count(i) for i in range(0, 25)]
    ax_internet.grid(True, axis='y', linestyle='dashed', linewidth=.5)
    ax_internet.bar(range(0, 25), internet)
    ax_internet.set_ylabel("frequency")
    ax_internet.set_xlabel("hours per day")
    ax_internet.set_xticks([i for i, v in enumerate(internet) if v > 0])
    ax_internet.title.set_text("Hours on the Internet per day")

    fig1.tight_layout()
    return fig1


def plot_websites_categories(websites: Dict[str, Website]) -> plt.Figure:
    categories = {'OTHERS': 0}
    for w in websites.values():
        cat = w.category.split('/')[0]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += w.count

    for cat in list(categories):
        if cat == 'OTHERS':
            continue
        if categories[cat] / sum(categories.values()) < 0.01:
            categories['OTHERS'] += categories[cat]
            del categories[cat]
    # print(sizes)
    fig1, ax_category = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

    # Ages
    ax_category.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    ax_category.title.set_text("Websites categories")
    ax_category.axis('equal')
    ax_category.legend(categories.keys())

    fig1.tight_layout()
    return fig1
