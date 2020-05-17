#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: RShirohara

import argparse
import sys

from novelconverter import convert, description


def get_args():
    _parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    _parser.add_argument(
        "to_format", type=str, help="Format of the output text")
    _parser.add_argument(
        "-f", "--from_format", type=str, help="Format of the original text",
        default="ddmarkdown")
    _parser.add_argument(
        "-o", "--output", type=str, help="File path of the output text")
    _parser.add_argument(
        "-i", "--input", type=str, help="File path of the original text")
    args = _parser.parse_args()
    return args


def load_text(_path):
    """Load the original text"""
    if _path:
        with open(_path, "r") as _file:
            data = _file.read()
    else:
        data = sys.stdin.read()
    return data


def export_text(_data, _path):
    """Export the converted text"""
    if _path:
        with open(_path, "w") as _file:
            _file.write(_data)
    else:
        sys.stdout.write(_data)


def main():
    args = get_args()
    original_text = load_text(args.input)
    converted_text = convert(
        original_text, args.from_format, args.to_format)
    export_text(converted_text, args.output)


if __name__ == "__main__":
    main()
