# -*- coding: utf-8 -*-
# author: RShirohara

import sys
import re
from . import form


__version__ = "3.0.0"
description = """
Novel Converter v{__version__}
Copyright (c) 2019-2020 Ray Shirohara
Released under MIT License.
https://github.com/RShirohara/NovelConverter
"""


def load_format(_format_name):
    """Load the format"""
    _format = {
        "ddmarkdown": form.ddmarkdown.DDMarkdown(),
        "markdown": form.markdown.Markdown(),
        "pixiv": form.pixiv.Pixiv(),
        "plain": form.plain.Plain(),
    }
    if _format_name in _format:
        _data = _format[_format_name]
        return _data
    else:
        print(f"{_format_name} is not found!")
        sys.exit()


def set_pattern(_from_format, _to_format):
    """Sets an output format name"""
    for _key, _form in _from_format:
        if _key not in _to_format.keys():
            if "_f1" in _form:
                _to_format[_key] = "{_f1}"
            else:
                _to_format[_key] = ""
    return _to_format


def check(_data, _from_format_name, _to_pattern):
    """Check the output format"""
    _result = [_name for _name in _from_format_name
               if re.match(_data, _to_pattern[_name])]
    return _result


def convert(_data, _to_format_name, _from_format_name):
    """Return the converted data"""
    _to_format = load_format(_to_format_name)
    _from_format = load_format(_from_format_name)
    _to_format.Format = set_pattern(_from_format.Format, _to_format.Format)
    _check_list = check(_data, _from_format.FormatName, _from_format.Pattern)
    _converted_data = _to_format.convert(
        _data, _check_list, _from_format.Pattern)
    return _converted_data
