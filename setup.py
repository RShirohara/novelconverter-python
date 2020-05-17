# -*- coding: utf-8 -*-
# author: RShirohara

from setuptools import setup
from novelconverter import __main__ as main

setup(
    name="novelconverter",
    version=main.__version__,
    author="Ray Shirohara",
    author_email="rshirohara@gmail.com",
    url="https://github.com/RShirohara/NovelConverter",
    description="Convert novel on python",
    license="MIT License",
    install_requires=[
        "python-markdown",
        "denden_extension",
    ],
    entry_points={
        "console_scripts": [
            "novelconv = novelconverter.cli:main",
        ]
    },
)
