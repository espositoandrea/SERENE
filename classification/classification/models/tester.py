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

"""A tester for an AI model."""

import logging
import pathlib
import time
from typing import Dict, Union, Optional

import joblib
import matplotlib.pyplot as plt
import mlxtend as mlx
import mlxtend.plotting
import pandas as pd
import sklearn as sk
import sklearn.model_selection

from .analyzer import analyze_model

logger = logging.getLogger(__name__)


def test_model(model: sk.base.BaseEstimator, x_train: pd.DataFrame,
               y_train: pd.DataFrame, x_test: pd.DataFrame,
               y_test: pd.DataFrame, title: str, emotion: str, width: int,
               location: str, out: str = 'models', n_jobs: int = 1,
               cv: Optional[int] = None) \
        -> Dict[str, Union[str, float, int]]:

    y_train_target = y_train[f"middle.emotions.{emotion}"] if emotion != 'all' \
        else y_train
    y_test_target = y_test[f"middle.emotions.{emotion}"] if emotion != 'all' \
        else y_test

    out_path = pathlib.Path(out) \
               / f"w{width}/{location}" / f"{title.lower().replace(' ', '-')}"
    out_path.mkdir(parents=True, exist_ok=True)
    report = {}
    logger.info("Analyzing %s on %s", title, emotion)
    report['model'] = title
    report['target'] = emotion
    report['width'] = width
    report['location'] = location
    backup_model = sk.base.clone(model)

    try:
        features = analyze_model(
            model,
            x_train,
            y_train_target,
            n_jobs=n_jobs
        )
    except BaseException as e:
        import textwrap
        logger.error("There was an error of type %s", str(type(e)))
        logger.error("Error message: %s", str(e))
        with open(out_path / f"no-{emotion}.txt", 'w',
                  encoding='utf-8') as file:
            file.write("Error in generating the model.\n\n")
            file.write("Error message\n")
            file.write("-------------\n\n")
            file.write(textwrap.fill(str(e), 80))
        return report

    mlx.plotting.plot_sequential_feature_selection(
        features.get_metric_dict(),
        kind='std_dev'
    )
    logger.info("Saving feature selection diagram")
    plt.title(
        f'{title} on {emotion} (w/StdDev, width: {width}, location: {location})'
    )
    plt.grid()
    plt.savefig(out_path / f"{emotion}.svg")

    if cv is not None:
        logger.info("Cross validating model")
        scores = sk.model_selection.cross_validate(
            model,
            features.transform(x_train),
            y_train_target,
            cv=cv,
            n_jobs=n_jobs,
        )
        logger.info("Saving cross validation results to a CSV")
        pd.DataFrame(scores).to_csv(
            out_path / f'{emotion}-cv.csv',
            encoding='utf-8'
        )

    logger.info("Training final model")
    start_time = time.time()
    backup_model.fit(
        features.transform(x_train),
        y_train_target
    )
    end_time = time.time()
    report['training_time'] = end_time - start_time
    logger.info("Training completed in %.3f seconds", report['training_time'])

    try:
        logger.info("Testing final model")
        y_pred = backup_model.predict(features.transform(x_test))
        report['test_accuracy'] = sk.metrics.accuracy_score(
            y_test_target,
            y_pred
        )
        cm = sk.metrics.classification_report(
            y_test_target,
            y_pred,
            # target_names=(y_test.columns if emotion == 'all' else range(7))
        )
        with open(out_path / f"{emotion}-report.txt", 'w',
                  encoding='utf-8') as file:
            logger.info("Saving report to file")
            file.write(cm)
    except BaseException as e:
        logger.error(
            "There was a %s in the testing phase. Testing phase skipped."
            "\nError message: %s",
            str(type(e)), str(e)
        )

    logger.info("Saving final model to file...")
    joblib.dump(backup_model, out_path / f"{emotion}.joblib")

    report['n_features'] = len(features.k_feature_names_)
    report['features'] = features.k_feature_names_
    report['score'] = features.k_score_

    return report
