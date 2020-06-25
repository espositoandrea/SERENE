#  This file is part of 'classification-models', the tool used to test various
#  AI models used in Andrea Esposito's Thesis.
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

"""The data loader.

This module loads the dataset and holds useful constants to deal with the
dataset's features.
"""

import gc
import logging
import pathlib
import time
from typing import Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

KEYS_TO_INCLUDE = {
    "middle.url",
    "middle.url.category",
    'middle.user_id'
}

KEYS_TO_IGNORE = {
    "middle.emotions.exists",  # Always True by design
    # The time of the middle object has served its purpose in the creation of
    # the interval and is now useless
    "middle.timestamp",
    # Often contains untreatable values (NaN or Inf) by design
    "middle.trajectory.slope",
}
KEYS_TO_PREDICT = {
    "middle.emotions.joy", "middle.emotions.fear", "middle.emotions.disgust",
    "middle.emotions.sadness", "middle.emotions.anger",
    "middle.emotions.valence", "middle.emotions.surprise",
    "middle.emotions.contempt", "middle.emotions.engagement"
}


def load_dataset(base_path: str = '.', width: int = None,
                 location: Optional[str] = None,
                 split: float = 1, discrete_steps: int = 7,
                 random_state: int = None, full_dataset: pathlib.Path = None) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the dataset.

    Parameters
    ----------
    base_path : str
        The path to the folder containing the dataset. This must contain the
        users' file and the websites' file and, unless `full_dataset` is
        specified, a folder for each user containing the aggregate data.
    width : int
        The interval width to be read. If None, all the intervals will be read.
    location : "before", "after", "full", None
        The location of the interval to be read. If None all the locations are
        read.
    split : float
        A number in the interval [0, 1] that indicates the size of the dataset
        to be read. If `full_dataset` is given, this is ignored.
    discrete_steps : int
        The number of steps into which the emotions will be discretized. If
        `full_dataset` is given, this is ignored.
    random_state : int, optional
        A random state.
    full_dataset : str, optional
        The path to the folder containing the sampled dataset. This is used to
        increase the loading speed of a stratified dataset.

    Returns
    -------
    x : pandas.DataFrame
        A dataframe containing all the features columns. Its shape depends on
        the size of the datasets' files.
    y : pandas.DataFrame
        A dataframe containing all the target (emotions) columns. It has the
        shape (len(x), 7).
    """
    users = pd.read_csv(
        pathlib.Path(base_path) / 'users.csv',
        index_col='id',
        dtype={
            'age': np.float32,
            'internet': np.float32,
            'gender': pd.StringDtype()
        }
    )
    users['gender'] = pd.Categorical(
        users['gender'],
        categories={'m', 'f', 'a'}
    )
    users['age'] = pd.Categorical(users['age'], categories=range(6))

    websites = pd.read_csv(
        pathlib.Path(base_path) / 'websites.csv',
        dtype={
            'count': np.float32,
            'category': pd.StringDtype()
        }
    )
    websites['category'] = pd.Categorical(websites['category'])
    websites['url'] = pd.Categorical(websites['url'])

    def can_take_column(col: str) -> bool:
        if width is None and location is None:
            return col in KEYS_TO_INCLUDE | KEYS_TO_PREDICT or \
                   col not in KEYS_TO_IGNORE
        if width is not None and location is None:
            return col in KEYS_TO_INCLUDE | KEYS_TO_PREDICT or \
                   col not in KEYS_TO_IGNORE and col.startswith(f"{width}.")
        if width is None and location is not None:
            return col in KEYS_TO_INCLUDE | KEYS_TO_PREDICT or \
                   col not in KEYS_TO_IGNORE and f".{location}." in col
        if width is not None and location is not None:
            return col in KEYS_TO_INCLUDE | KEYS_TO_PREDICT or \
                   col not in KEYS_TO_IGNORE and \
                   col.startswith(f"{width}.{location}.")

    def get_data_from_files():
        with open(pathlib.Path(base_path) / 'users.csv', 'r') as file:
            iterfile = iter(file)
            next(iterfile)
            user_ids = [line.split(',')[0] for line in iterfile]

        for i, user_id in enumerate(user_ids, 1):
            logger.info("Loading user '%s' (%d of %d)", user_id, i,
                        len(user_ids))
            path = pathlib.Path(base_path) / user_id / 'aggregate.csv'
            if not path.exists():
                yield pd.DataFrame()
            else:
                logger.debug("Loading CSV for user '%s'", user_id)
                df = pd.read_csv(
                    path,
                    usecols=can_take_column,
                    encoding='utf-8'
                )

                yield df

    if full_dataset is None:
        if split < 0 or split > 1:
            raise ValueError("The split value must be in [0, 1]")

        logger.info("Reading data from multiple CSV files")
        start_time = time.time()
        df = pd.concat(get_data_from_files())
        end_time = time.time()
        logger.info("Completed loading in %.3f seconds", end_time - start_time)
        logger.info("Full dataset length: %d objects", df.shape[0])
        if split != 1:
            df = df.sample(frac=split, random_state=random_state)
            logger.info("Sampled dataset length: %d objects", df.shape[0])
    else:
        logger.info("Loading from '%s'", str(full_dataset))
        start_time = time.time()
        df = pd.read_csv(
            full_dataset,
            engine='c',
            encoding='utf-8',
            usecols=lambda c: can_take_column(c) or c == 'middle.user_id'
        )
        end_time = time.time()
        logger.info("Completed loading in %.3f seconds", end_time - start_time)

    df['user.age'] = df['middle.user_id'].map(users['age'])
    df['user.internet'] = df['middle.user_id'].map(users['internet'])
    df['user.gender'] = df['middle.user_id'].map(users['gender'])
    # The user id is no longer needed
    df.drop(columns=['middle.user_id'], inplace=True)

    # OneHot encoder
    df['user.gender'] = df['user.gender'].map({
        'm': 'male',
        'f': 'female',
        'a': 'other'
    })
    df = pd.get_dummies(
        df,
        prefix_sep='.',
        columns=[
            'user.gender'
        ]
    )
    # Ordinal encoder
    df['middle.url'] = df['middle.url'].map(
        {u: i for i, u in enumerate(pd.Categorical(df['middle.url']))}
    )
    # Ordinal encoder
    df['middle.url.category'] = df['middle.url.category'].map(
        {c: i for i, c in
         enumerate(pd.Categorical(df['middle.url.category']))}
    )

    # Filling NaN values on target columns: by design if a value isn't there it
    # means that it was under 1 and can then be approximated to 0 (see
    # https://shorturl.at/JOTU5 and https://shorturl.at/etM09).
    x = df.drop(columns=KEYS_TO_PREDICT)
    y = df[KEYS_TO_PREDICT].fillna(0)
    if full_dataset is None and discrete_steps is not None:
        # in full_dataset, the emotions are already discretized
        y = discretize_emotions(y, steps=discrete_steps)
    gc.collect()

    return x, y


def discretize_emotions(data: pd.DataFrame, steps: int = 7) -> pd.DataFrame:
    """Discretize the emotions.
    :param data: The dataframe containing the emotions to be discretized.
    :param steps: The number of steps into which the emotions' range will be
        discretized.
    :return: The discretized dataframe.
    """

    def get_step(val, minimum=0, maximum=100):
        step_width = (maximum - minimum) / steps
        for i in range(0, steps):
            if minimum + step_width * i <= val < minimum + step_width * (
                    i + 1):
                return i
        if val == maximum:
            return steps - 1
        return None

    df = pd.DataFrame(columns=KEYS_TO_PREDICT)
    df['middle.emotions.valence'] = data['middle.emotions.valence'].apply(
        lambda x: get_step(x, minimum=-100, maximum=100)
    )
    for k in KEYS_TO_PREDICT - {'middle.emotions.valence'}:
        df[k] = data[k].apply(get_step)

    return df
