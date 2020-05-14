#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: RShirohara

import sys
import argparse
from .__main__ import convert

description = """
Novel Converter v{main.__version__}
Copyright (c) 2019-2020 Ray Shirohara
Released under MIT License.
https://github.com/RShirohara/NovelConverter
"""

def get_args():
    _parser = argparse.ArgumentParser(description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter)
    _parser.add_argument("to_format", type=str,
    help="Format of the output text")
    _parser.add_argument("-f", "--from_format", type=str,
    help="Format of the original text")
    _parser.add_argument("-o", "--output", type=str,
    help="File path of the output text")
    _parser.add_argument("-i", "--input", type=str,
    help="File path of the original text")
    args = _parser.parse_args()
    return args

def load_text(_path):
    """Load original text"""
    if _path:
        with open(_path, "r") as _file:
            data = tuple(_file.readlines)
    else:
        data = tuple(sys.stdin.readlines())
    return data

def export_text(_data, _path):
    """Export """
    if _path:
        with open(_path, "w") as _file:
            _file.write(_data)
    else:
        sys.stdout.write(_data)

def main():
    args = get_args()
    original_text = load_text(args.input)
    converted_text = convert(original_text, args.to_format, args.from_format)
    export_text(converted_text, args.output)
