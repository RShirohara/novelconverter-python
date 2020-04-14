#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: RShirohara

__version__ = """
Novel Converter ver 2.2.3(202004)
Copyright (c) 2019-2020 Ray Shirohara
Released under MIT License.
https://github.com/RShirohara/NovelConverter
"""

import sys
import argparse
import module

def get_args():
    """Get argument"""
    _parser = argparse.ArgumentParser(description = __version__, formatter_class = argparse.RawDescriptionHelpFormatter)
    _parser.add_argument("-p", "--path", type = str, help = "Data path")
    _parser.add_argument("form", type = str, help = "Format type")
    _parser.add_argument("-f", "--imput_form", help = "Format type(Imput Data)")
    _args = _parser.parse_args()
    return _args

def load_format(_name):
    """Load format"""
    if not _name:
        _name = "default"
    try:
        _form = module.call(_name)
    except ModuleNotFoundError:
        print(f"{_name} is not found!")
        sys.exit()
    return _form

def load_data(_path):
    """Load data"""
    if _path:
        with open(_path, "r") as _file:
            _data = _file.readlines()
    else:
        _data = sys.stdin.readlines()
    return _data

if __name__ == "__main__":
    args = get_args()
    # Load Format
    form_exp = load_format(args.form)
    form_imp = load_format(args.imput_form)
    # Load data
    data = load_data(args.path)
    # Convert
    result = form_exp.convert(data, form_imp.Pattern)
    # Export
    print(result)
