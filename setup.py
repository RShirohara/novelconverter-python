# -*- coding: utf-8 -*-
# author: RShirohara

from setuptools import setup
import novelconverter

setup(
    name="novelconverter",
    version=novelconverter.__version__,
    author="Ray Shirohara",
    author_email="rshirohara@gmail.com",
    url="https://github.com/RShirohara/NovelConverter",
    description="Convert novel on python",
    license="MIT License",
    install_requires=[
        "Markdown",
        "denden_extension",
    ],
    entry_points={
        "console_scripts": [
            "novelconv = novelconverter.cli: main",
        ]
    },
)
