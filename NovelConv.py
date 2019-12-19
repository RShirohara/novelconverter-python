#!usr/bin/python3
# -*- coding: utf-8 -*-
# author: RShirohara

"""Convert novel on python3"""

__version__ = """
Novel Convertor command version 1.0(201912)
Copyrigut (c) 2019 Ray Shirohara
Released under MIT License.
https://github.com/RShirohara/NovelConvertor
"""

import re
import string
import sys
from argparse import ArgumentParser
from module import convert


def get_args():
    """Get argment"""
    _parser = ArgumentParser(description = str(__version__))
    _parser.add_argument('filepath', type = str, help = "Noveldata path")
    _parser.add_argument('formtype', type = str, help = "Format name")
    _parser.add_argument('-i', '--impform', type = str, help = "Set import format name")
    _args = _parser.parse_args()
    return _args

def load_data(_path):
    """Load noveldata"""
    with open(_path, 'r') as _file:
        _dat_exp = _file.readlines()
    return _dat_exp

def conv_data(_dat_imp):
    """Convert data"""
    pass    # debug
    _dat_exp = []
    # Set format module
    _form_exp = module_exp.form()
    _pattern_imp = module_imp.pattern()
    for _key in _pattern_imp.keys():
        if not _key in _form_exp:
            if not '_str1' in str(_pattern_imp[_key]):
                _form_exp[_key] = None
            else:
                _form_exp[_key] = '{_str1}'
    # Delete metadata
    for _num in range(len(_dat_imp)):
        _meta = re.match(r'^# .*?$', _dat_imp[_num])
        if not _meta and _dat_imp[_num] == '\n':
            del _dat_imp[:_num]
            break
    # Convert data
    for _str in _dat_imp:
        _cache = _str
        for _form in _form_exp.keys():
            _match = convert.getData(_cache, _pattern_imp[_form])
            _cache = convert.Convert(_cache, _match, _form_exp[_form])
            if not _cache:
                break
        if _cache:
            _dat_exp.append(_cache)
    return _dat_exp


if __name__ == '__main__':
    # Get argment
    args = get_args()
    # Import modules
    exec(f'from module import {args.formtype} as module_exp')
    if args.impform:
        form_imp = args.formtype
    else:
        form_imp = "base"
    exec(f'from module import {form_imp} as module_imp')
    del form_imp
    # Load data
    dat_imp = load_data(args.filepath)
    # Convert data
    dat_exp = conv_data(dat_imp)
    # Export data
    print(''.join(dat_exp))
