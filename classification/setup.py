#!/usr/bin/env python3

from setuptools import setup, find_packages

import classification

setup(
    name=classification.__prog__,
    version=classification.__version__,
    description=classification.__doc__,
    author=classification.__author__,
    author_email=classification.__email__,
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'matplotlib',
        'mlxtend',
        'progressbar2',
        'coloredlogs',
        'joblib'
    ],
    entry_points={
        'console_scripts': [
            f'{classification.__prog__}=classification.cli:main'
        ]
    }
)