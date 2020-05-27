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

import requests


@dataclasses.dataclass(frozen=True)
class User:
    _id: str
    age: int
    internet: int
    gender: str


def load_users(mongodb=None):
    logger = logging.getLogger(__name__)

    if mongodb:
        logger.info("Loading users from database...")
        users = list(mongodb['users'].find())
        for user in users:
            user['_id'] = str(user['_id'])
    else:
        logger.info("Loading users from web APIs...")
        users = requests.get("https://giuseppe-desolda.ddns.net:8080/api/users", verify=False).json()
    users = {user['_id']: User(**user) for user in users}
    logger.info("Done. Loaded %d users", len(users))
    return users
