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

"""An analyzer for an AI model."""

import logging
import time

import mlxtend as mlx
import mlxtend.feature_selection
import pandas as pd
import sklearn as sk

logger = logging.getLogger(__name__)


def analyze_model(model: sk.base.BaseEstimator, x: pd.DataFrame,
                  y: pd.DataFrame, n_jobs: int = 1) \
        -> mlx.feature_selection.SequentialFeatureSelector:
    start_time = time.time()
    logger.info("Starting feature selection")

    sfs = mlx.feature_selection.SequentialFeatureSelector(
        estimator=model,
        k_features="parsimonious",
        cv=None,
        verbose=1,
        forward=True,
        n_jobs=n_jobs,
        # scoring is chosen as a default based on the type of model
    )
    sfs.fit(x, y)

    end_time = time.time()
    logger.info("Feature selection done in %.3f seconds", end_time - start_time)
    return sfs
