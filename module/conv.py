# -*- coding: utf-8 -*-
# author: RShirohara

import re
import string

def conv(_data, _match, _form):
    """Return converted string"""
    _cache = _data
    for _obj in _match:
        # Get old string
        _old = _obj.group(0)
        # Get new string
        _new_dict = _obj.groupdict()
        if not '_field2' in (str(_obj.re) or _form):
            if not '_field1' in str(_obj.re):
                _new = _form
            else:
                _new = _form.format(_field1 = _new_dict['_field1'])
        else:
            _new = _form.format(**_new_dict)
        if _new:
            _cache = _cache.replace(_old, _new)
    return _cache
