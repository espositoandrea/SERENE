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

import logging
from typing import Dict, Union

import pymongo.database as db
import requests

from analyzer.data.base import BaseObject


class User(BaseObject):
    __slots__ = ["id", "age", "internet", "gender"]

    def __init__(self, id: str, age: int, internet: int, gender: str):
        self.id: str = id
        self.age: int = age
        self.internet: int = internet
        self.gender: str = gender

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            'id': self.id,
            'age': self.age,
            'internet': self.internet,
            'gender': self.gender
        }


def load_users(mongodb: db.Database = None) -> Dict[str, User]:
    logger = logging.getLogger(__name__)

    if mongodb:
        logger.info("Loading users from database...")
        db_content = list(mongodb['users'].find())
    else:
        logger.info("Loading users from web APIs...")
        db_content = requests.get("https://giuseppe-desolda.ddns.net:8080/api/users", verify=False).json()

    users = dict()
    for user in db_content:
        user['id'] = str(user['_id'])
        del user['_id']
        users[user['id']] = User(**user)
    del db_content
    logger.info("Done. Loaded %d users", len(users))
    return users
