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


class Emotions(object):
    __slots__ = [
        "exists",
        "joy",
        "fear",
        "disgust",
        "sadness",
        "anger",
        "surprise",
        "contempt",
        "valence",
        "engagement"
    ]

    def __init__(self, **kwargs):
        self.exists: bool = kwargs.get("exists", False)
        self.joy: float = kwargs.get("joy", None)
        self.fear: float = kwargs.get("fear", None)
        self.disgust: float = kwargs.get("disgust", None)
        self.sadness: float = kwargs.get("sadness", None)
        self.anger: float = kwargs.get("anger", None)
        self.surprise: float = kwargs.get("surprise", None)
        self.contempt: float = kwargs.get("contempt", None)
        self.valence: float = kwargs.get("valence", None)
        self.engagement: float = kwargs.get("engagement", None)
