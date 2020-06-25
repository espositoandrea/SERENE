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

"""The AI Models"""

import collections

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .analyzer import analyze_model
from .tester import test_model

Model = collections.namedtuple('Model', ['title', 'model', 'discretize'])

MODELS = {
    'tree': Model(
        'Decision Tree',
        DecisionTreeClassifier(),
        True
    ),
    'svm': Model(
        'SVM',
        SVC(),
        True
    ),
    'randforest': Model(
        'Random Forest',
        RandomForestClassifier(n_estimators=200),
        True
    ),
    'adaboost': Model(
        'AdaBoost',
        AdaBoostClassifier(n_estimators=200),
        True
    ),
    'nn': Model(
        'Multi Layer Perceptron (NN)',
        MLPClassifier(solver='adam', max_iter=1000),
        True
    )
}
