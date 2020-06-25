#!/usr/bin/env python3

"""A tool to sample a dataset in a stratified fashion."""

__version__: str = '0.0.1'
__author__: str = 'Andrea Esposito'
__email__: str = 'a.esposito39@studenti.uniba.it'
__prog__: str = 'dataset-sampler'
__disclaimer__: str = f'''
{__prog__} (v{__version__}) Copyright (C) 2020 {__author__}

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This program comes with ABSOLUTELY NO WARRANTY, to the extent permitted by law.
This is free software, and you are welcome to redistribute it
under certain conditions (see the License for more details).

Written by {__author__}
'''.strip()

import argparse
import gc
import logging
import math
import multiprocessing
import pathlib
from functools import partial
from typing import List

import coloredlogs
import multiprocessing_logging
import pandas as pd

from classification.data_loader import discretize_emotions, KEYS_TO_PREDICT

DISCRETE_STEPS = 7


def range_type(x: str) -> float:
    x = float(x)
    if not 0 <= x <= 1:
        raise argparse.ArgumentTypeError(f"{x} is not in [0, 1]")
    return x


def get_users_ids(base_path: str) -> List[str]:
    path = pathlib.Path(base_path) / 'users.csv'
    if not path.exists():
        raise FileNotFoundError(
            "The users' file does not exists in the base path")
    with open(path, 'r') as file:
        users_ids = [s.split(',')[0] for s in file.readlines()[1:]]
    return users_ids


def get_interactions(user_id: str, base_path: str = '.') -> pd.DataFrame:
    path = pathlib.Path(base_path) / f'{user_id}/aggregate.csv'
    if not path.exists():
        logging.warning("The user '%s''s file doesn't exists", user_id)
        return pd.DataFrame()

    logging.info("Reading user '%s''s file", user_id)
    df = pd.read_csv(path, encoding='utf-8', engine='c')
    gc.collect()
    return df


def setup_args() -> argparse.Namespace:
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Copyright (C) 2020 {__author__}. "
               "Released under the GNU GPL v3 License."
    )
    parser.add_argument(
        'data',
        metavar='DATA',
        help='the dataset base path'
    )
    parser.add_argument(
        '--split', '-s',
        help='the relative split size in [0, 1] of the dataset to be used '
             '(defaults to 0.01)',
        default=0.01,
        type=range_type
    )
    parser.add_argument(
        '--version',
        help="output version information and exit",
        action='version',
        version=__disclaimer__
    )
    parser.add_argument(
        '--jobs', '-j',
        help='the number of parallel jobs (default is 1)',
        default=1,
        type=int
    )
    parser.add_argument(
        '--random', '-r',
        help='the random seed',
        default=None,
        type=int
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '--quiet', '-q',
        help='suppress the output (except errors)',
        action='store_true'
    )
    verbosity.add_argument(
        '--verbose', '-v',
        help='increases the output verbosity to debug level',
        action='store_true'
    )
    parser.add_argument(
        '--test',
        help='loads only TESTING_SIZE users for testing purposes',
        default=None,
        type=int,
        metavar='TESTING_SIZE'
    )
    return parser.parse_args()


def get_value(interactions: pd.DataFrame, to_take: int, emotion: str, i: int,
              random_state: int = None):
    logging.debug(
        "Selecting from %s with value %d",
        emotion.split('.')[2], i
    )
    df = interactions.loc[interactions[emotion] == i]
    n = to_take if to_take < df.shape[0] else df.shape[0]
    logging.debug(
        "Taking %d objects for %s (with value %d)",
        n, emotion.split('.')[2], i
    )
    return df.sample(n=n, random_state=random_state)


if __name__ == '__main__':
    gc.enable()
    args = setup_args()
    logging_level = logging.DEBUG if args.verbose else logging.ERROR if args.quiet else logging.INFO
    coloredlogs.install(
        level=logging_level,
        fmt="[%(levelname)s] %(asctime)s %(message)s",
    )

    users_ids = get_users_ids(args.data)
    if args.test is not None:
        logging.warning("Starting in testing mode")
        logging.warning("Original users' number: %d", len(users_ids))
        users_ids = users_ids[0:args.test]
        logging.warning("Final users' number: %d", len(users_ids))

    logging.info("Getting the interactions")
    if args.jobs == 1:
        interactions = pd.concat(
            (get_interactions(id, base_path=args.data) for id in users_ids)
        )
    else:
        multiprocessing_logging.install_mp_handler()
        func = partial(get_interactions, base_path=args.data)
        logging.info("Instantiating %d parallel processes", args.jobs)
        with multiprocessing.Pool(processes=args.jobs) as pool:
            dfs = pool.map(func, users_ids)
        interactions = pd.concat(dfs)

    gc.collect()
    logging.info("Discretizing emotion values")
    keys = list(KEYS_TO_PREDICT)
    interactions[keys] = interactions[keys].fillna(0)
    interactions[keys] = discretize_emotions(
        interactions[keys],
        steps=DISCRETE_STEPS
    )

    gc.collect()

    logging.info("Sampling the dataset")
    total_objects = math.ceil(interactions.shape[0] * args.split)
    to_take = math.ceil(total_objects / DISCRETE_STEPS)
    out_path = pathlib.Path(args.data) / f'aggregate-{args.split * 100}percent'
    out_path.mkdir(parents=True, exist_ok=True)
    for emotion in keys:
        func = partial(get_value, interactions, to_take, emotion,
                       random_state=args.random)
        if args.jobs == 1:
            final = []
            for i in range(DISCRETE_STEPS):
                final.append(func(i))
        else:
            logging.info("Instantiating %d parallel processes", args.jobs)
            with multiprocessing.Pool(processes=args.jobs) as pool:
                final = pool.map(func, range(DISCRETE_STEPS))
        logging.info(
            "Merging and saving output for %s",
            emotion.split('.')[2]
        )
        df = pd.concat(final)
        df.to_csv(
            out_path / f"{emotion.split('.')[2]}.csv",
            encoding='utf-8',
            index=False
        )
        logging.info("Took %d objects for %s", df.shape[0],
                     emotion.split('.')[2])
