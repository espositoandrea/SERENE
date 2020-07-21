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

"""The Command Line Interface of the module"""

import argparse
import gc
import logging
import os
import pathlib
from typing import List, Dict, Hashable, Any

import coloredlogs
import pandas as pd
import sklearn as sk
import yaml

import classification
import multiprocessing
from . import data_loader
from . import models

logger = logging.getLogger('classification')


def get_config(filename: str = 'config.yml') -> Dict[str, Any]:
    if not filename:
        return dict()
    if not os.path.exists(filename):
        logger.error("ERROR: Config file '%s' does not exist", filename)
        return dict()

    with open(filename, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error("ERROR: %s (%s)", str(e), type(e).__name__)
            return dict()
    return config


def setup_args(args: List[str] = None) -> argparse.Namespace:
    """Set up the CLI arguments.

    Parameters
    ----------
    args
        The given arguments (can be empty).

    Returns
    -------
    argparse.Namespace
        The parsed arguments
    """

    def range_type(x: str):
        x = float(x)
        if not 0 <= x <= 1:
            raise argparse.ArgumentTypeError(f"{x} is not in [0, 1]")
        return x

    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        prog=classification.__prog__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=classification.__doc__,
        epilog=f"Copyright (C) 2020 {classification.__author__}. "
               "Released under the GNU GPL v3 License."
    )
    parser.add_argument(
        '--config',
        metavar='CONFIG',
        help='The path to a configuration file.'
    )
    parser.add_argument(
        '--data', '-d',
        metavar='DATA',
        help='The dataset base path. Required unless --complete is specified.'
    )
    parser.add_argument(
        '--complete', '-c',
        metavar='DATA',
        help='The full dataset base path. Required unless --data is specified.'
    )
    parser.add_argument(
        '--split', '-s',
        help='The relative split size in [0, 1] of the dataset to be used. '
             'Defaults to 0.01.',
        default=0.01,
        type=range_type
    )
    parser.add_argument(
        '--jobs', '-j',
        help='The number of parallel jobs. Default is 1.',
        default=1,
        type=int
    )
    data_selection_group = parser.add_argument_group(
        'data selection',
        'Options to select the data on which the models will be trained'
    )
    data_selection_group.add_argument(
        '--half',
        help='The halves of the windows to train the model on.',
        choices=['before', 'after', 'full'],
        action='append',
        required=True,
        dest='halves'
    )
    data_selection_group.add_argument(
        '--emotion', '-e',
        help='An emotion to train the model on.',
        choices=[s.split('.')[2] for s in data_loader.KEYS_TO_PREDICT],
        action='append',
        required=True,
        dest='emotions'
    )
    data_selection_group.add_argument(
        '--window', '-w',
        help='A window width to train',
        default=None,
        type=int,
        choices=[25, 50, 100, 200, 500, 1000, 2000],
        action='append',
        dest='windows'
    )
    data_selection_group.add_argument(
        '--model', '-m',
        help='the type of models to be trained',
        choices=models.MODELS.keys(),
        required=True,
        action='append',
        dest='models'
    )
    model_tuning_group = parser.add_argument_group(
        'model tuning',
        'A group of options that changes the way the training is performed'
    )
    model_tuning_group.add_argument(
        '--random', '-r',
        help='The random seed.',
        default=None,
        type=int
    )
    parser.add_argument(
        "--version", '-v',
        help="Output version information and exit",
        action='version',
        version=classification.__disclaimer__
    )
    model_tuning_group.add_argument(
        '--cross-validate', '-k',
        dest='cv',
        type=int,
        default=None,
        metavar='K',
        help='enable stratified k-fold validation with k=K'
    )
    model_tuning_group.add_argument(
        '--discretize',
        dest='discretize',
        type=int,
        default=7,
        help='the number of steps into which the emotions will be discretized'
    )
    # parser.add_argument(
    #     '--no-all',
    #     help='Do not train the multilabel version',
    #     action='store_false',
    #     dest='do_all'
    # )

    parsed = parser.parse_args(args)
    config = get_config(parsed.config)
    for key, val in config.items():
        print(key, val)
        setattr(parsed, key, val)
    parsed = parser.parse_args(args, namespace=parsed)
    return parsed


def main(args: List[str] = None):
    """The main function for CLI usage.

    Parameters
    ----------
    args
        The given arguments (can be empty)
    """
    args = setup_args(args)
    logger.setLevel(logging.INFO)
    coloredlogs.install(
        level=logging.INFO,
        logger=logger,
        fmt="[%(levelname)s] %(asctime)s (%(name)s) %(message)s",
    )

    reports = []
    ranges_widths = args.windows or [
        # t = 100 ms is the time between two captured emotions
        25,  # 1/4 * t
        50,  # 1/2 * t
        100,  # 1 * t
        200,  # 2 * t
        500,  # 5 * t
        1000,  # 10 * t
        2000  # 20 * t
    ]
    logger.info("Windows to train: %s", str(ranges_widths))

    target_models = (models.MODELS[k] for k in args.models)
    target_emotions = [f"middle.emotions.{s}" for s in args.emotions] or data_loader.KEYS_TO_PREDICT
    target_halves = args.halves or ['before', 'after', 'full']

    for title, model, discretize in target_models:
        for width in ranges_widths:
            for location in target_halves:
                for emotion in target_emotions:
                    logger.info(
                        "Loading %s data (width: %d, location: %s)",
                        emotion.split('.')[2], width, location
                    )
                    if not args.complete:
                        full_dataset = None
                    else:
                        full_dataset = pathlib.Path(
                            args.complete) / f"{emotion.split('.')[2]}.csv"
                    x, y = data_loader.load_dataset(
                        base_path=pathlib.Path(args.data),
                        full_dataset=full_dataset,
                        width=width,
                        location=location,
                        split=args.split,
                        discrete_steps=(
                            args.discretize if discretize else None),
                        random_state=args.random
                    )
                    logger.info("Final dataset length: %d objects", x.shape[0])

                    logger.info(
                        "Splitting dataset into train and test set (70-30)")
                    x_train, x_test, y_train, y_test = \
                        sk.model_selection.train_test_split(
                            x, y, test_size=0.3, random_state=args.random
                        )

                    report = models.test_model(
                        model=model,
                        x_train=x_train,
                        y_train=y_train,
                        x_test=x_test,
                        y_test=y_test,
                        title=title,
                        emotion=emotion.split('.')[2],
                        width=width,
                        location=location,
                        out='models',
                        n_jobs=args.jobs,
                        cv=args.cv
                    )
                    reports.append(report)
                    gc.collect()
                gc.collect()

    report_table = pd.DataFrame.from_records(reports)
    report_table.to_csv('report.csv')
