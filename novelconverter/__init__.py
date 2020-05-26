# -*- coding: utf-8 -*-
# author: RShirohara

import re

from novelconverter import form


__version__ = "3.0.2"
description = f"""
Novel Converter v{__version__}
Copyright (c) 2019-2020 Ray Shirohara
Released under MIT License.
https://github.com/RShirohara/NovelConverter
"""


def set_pattern(_from_format, _to_format):
    """Sets an output format name"""
    _metadata = (
        "encode",
        "author",
        "title",
        "chapter"
    )
    for _key, _form in _from_format.items():
        if _key not in _to_format.keys():
            if "_f1" in _form and _key not in _metadata:
                _to_format[_key] = "{_f1}"
            else:
                _to_format[_key] = ""
    return _to_format


def check(_data, _from_format_name, _from_pattern):
    """Check the output format"""
    _result = [_name for _name in _from_format_name
               if re.search(_from_pattern[_name], _data)]
    return _result


def convert(_data, _from_format_name, _to_format_name):
    """Return the converted data"""
    _from_format = form.call(_from_format_name)
    _to_format = form.call(_to_format_name)
    _to_format.Format = set_pattern(_from_format.Format, _to_format.Format)
    _check_list = check(_data, _from_format.FormatName, _from_format.Pattern)
    _converted_data = _to_format.convert(
        _data, _check_list, _from_format.Pattern)
    return _converted_data
