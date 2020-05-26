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

import dataclasses
import urllib.parse

import requests


@dataclasses.dataclass
class Website:
    url: urllib.parse.ParseResult
    count: int = 0
    category: str = 'UNKNOWN'


def load_websites(mongodb=None):
    if mongodb:
        db_content = [w for w in mongodb['websites'].find()]
        for w in db_content:
            w['url'] = urllib.parse.urlparse(str(w['_id']))
            del w['_id']
    else:
        db_content = requests.get("https://giuseppe-desolda.ddns.net:8080/api/websites", verify=False).json()
        for w in db_content:
            w['url'] = urllib.parse.urlparse(w['url'])
    websites = {}
    for website in db_content:
        websites[website['url'].geturl()] = Website(**website)
    return websites
