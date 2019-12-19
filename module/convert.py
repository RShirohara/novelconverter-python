# -*- coding: utf-8 -*-
# author: RShirohara

import re
import string

def getData(_dat_imp, _patt):
    """Return matched string"""
    _match = []
    _pos = 0
    while True:
        _result = _patt.search(_dat_imp, pos = _pos)
        if not _result:
            break
        else:
            _match.append(_result)
            _pos = _result.end(0)
    return _match

def Convert(_dat_imp, _match, _form):
    """Return converted string"""
    if _match and len(_match) > 0:
        # Get string
        _cache = _dat_imp
        for _obj in _match:
            # Get old string
            _str_old = _obj.group(0)
            # Ger new string
            _obj_dict = _obj.groupdict()
            if not '_str2' in (str(_obj.re) or _form):
                if not '_str1' in str(_obj.re):
                    _str_new = None
                else:
                    _str_new = _form.format(_str1 = _obj_dict['_str1'])
            else:
                _str_new = _form.format(**_obj_dict)
            if not _str_new:
                _cache = None
            else:
                _cache = _cache.replace(_str_old, _str_new)
        _dat_exp = _cache
    else:
        _dat_exp = _dat_imp
    return _dat_exp
