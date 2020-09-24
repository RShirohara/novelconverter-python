# -*- coding: utf-8 -*-
# author: RShirohara

import setuptools

from novelconverter import __version__ as version

setuptools.setup(
    name="novelconverter",
    version=version,
    author="Ray Shirohara",
    author_email="rshirohara@gmail.com",
    url="https://github.com/RShirohara/NovelConverter",
    description="Convert novel on python",
    license="MIT License",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "novelconv = novelconverter.cli:main",
        ]
    },
)
