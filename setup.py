# -*- coding: utf-8 -*-
# author: RShirohara

import setuptools

setuptools.setup(
    name="novelconverter",
    version="3.0.2",
    author="Ray Shirohara",
    author_email="rshirohara@gmail.com",
    url="https://github.com/RShirohara/NovelConverter",
    description="Convert novel on python",
    license="MIT License",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "novelconv = novelconverter.cli:main",
        ]
    },
)
