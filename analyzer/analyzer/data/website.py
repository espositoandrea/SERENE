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
import logging
import urllib.parse
from typing import Optional, Dict, Union

import pymongo.database as db
import requests

from analyzer.data.base import BaseObject


@dataclasses.dataclass
class Website(BaseObject):
    url: Optional[urllib.parse.ParseResult]
    count: int = 0
    category: str = 'UNKNOWN'

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            'url': self.url.geturl() if self.url else None,
            'count': int(self.count),
            'category': self.category
        }


def load_websites(mongodb: db.Database = None):
    logger = logging.getLogger(__name__)

    if mongodb:
        logger.info("Loading websites from database...")
        db_content = list(mongodb['websites'].find())
        for w in db_content:
            w['url'] = urllib.parse.urlparse(str(w['_id']))
            del w['_id']
    else:
        logger.info("Loading websites from web APIs...")
        db_content = requests.get("https://giuseppe-desolda.ddns.net:8080/api/websites", verify=False).json()
        for w in db_content:
            w['url'] = urllib.parse.urlparse(w['url'])
    websites = {}
    for website in db_content:
        websites[website['url'].geturl()] = Website(**website)

    logger.info("Done. Loaded %d websites", len(websites))
    return websites
