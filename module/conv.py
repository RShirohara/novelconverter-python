# -*- coding: utf-8 -*-
# author: RShirohara

import re

def setPatt(_pattern, _format, _formatName):
    """Set convert pattern"""
    for _key, _patt in _pattern.items():
        if not _key in _formatName:
            if not "_field1" in _patt.pattern:
                _format[_key] = None
            else:
                _format[_key] = "{_field1}"
    return _format

def conv(_data, _match, _form):
    """Return converted string"""
    _cache = _data
    for _obj in _match:
        # Get old string
        _old = _obj.group(0)
        # Get new string
        _new_dict = _obj.groupdict()
        if not _form:
            _new = None
        else:
            if not "_field2" in (_obj.re.pattern or _form):
                if not "_field1" in _form:
                    _new = _form
                elif (not "_field1" in _obj.re.pattern) or ((_obj.endpos == len(_data)) and ("$" in _obj.re.pattern)):
                    _new = None
                else:
                    _new = _form.format(_field1 = _new_dict["_field1"])
            else:
                _new = _form.format(**_new_dict)
        if _new:
            _cache = _cache.replace(_old, _new)
        else:
            _cache = ""
    return _cache
