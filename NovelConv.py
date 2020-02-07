#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: RShirohara

__version__ = """
Novel Converter ver 2.0-test1(202002)
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
    _group_path = _parser.add_mutually_exclusive_group()
    _group_path.add_argument('path', type = str, help = "Data path")
    _parser.add_argument('form', type = str, help = "Format name")
    _parser.add_argument('-i', '--imput_form', type = str, help = "Format type(imput data)")
    _group_path.add_argument('-s', '--read_stdin', action = 'store_true', help = "Read data from stdin")
    _args = _parser.parse_args()
    return _args

def load_format(_name):
    """Load format"""
    try:
        _form = module.call(_name)
    except ModuleNotFoundError:
        sys.exit()
    return _form

def load_data(_path):
    """Load data"""
    with open(_path, 'r') as _file:
        _data = _file.readlines()
    return _data

if __name__ == '__main__':
    args = get_args()
    # Load Format
    form_exp = load_format(args.form)
    if args.imput_form:
        form_imp = load_format(args.imput_form)
    else:
        form_imp = load_format('ddmarkdown')
    # Load data
    if args.imput_form:
        data = sys.stdin.readlines()
    else:
        data = load_data(args.path)
    # Convert
    result = form_exp.Convert(data, form_imp.Pattern)
    # Export
    print(result)
