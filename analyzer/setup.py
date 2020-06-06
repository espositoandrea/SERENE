#!/usr/bin/env python3

# This file is part of 'analyzer', the tool used to process the information
# collected for Andrea Esposito's Thesis.
# Copyright (C) 2020  Andrea Esposito
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

import analyzer

setup(
    name=analyzer.__prog__,
    version=analyzer.__version__,
    description='Process the data collected by the extension',
    author=analyzer.__author__,
    author_email=analyzer.__email__,
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'coloredlogs',
        'pymongo',
        'requests',
        'multiprocessing-logging'
    ],
    entry_points={
        'console_scripts': [
            f'{analyzer.__prog__}=analyzer.cli:main'
        ]
    }
)
