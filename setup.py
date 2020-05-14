# -*- coding: utf-8 -*-
# author: RShirohara

from setuptools import setup
from NovelConverter import __main__ as main

setup(
    name = "NovelConverter",
    version = main.__version__,
    author = "Ray Shirohara",
    author_email = "rshirohara@gmail.com",
    url = "https://github.com/RShirohara/NovelConverter",
    description = "Convert novel on python",
    license = "MIT License",
    entry_points = {
        "console_scripts": [
            "novelconv = NovelConverter.cli:main",
        ]
    }
)