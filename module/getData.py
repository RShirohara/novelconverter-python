# -*- coding: utf-8 -*-
# author: RShirohara

from copy import copy
import re

def match(_data, _pattern):
    """Return matched strings"""
    _match = list()
    _pos = 0
    if _data:
        while True:
            _result = _pattern.search(_data, pos = _pos)
            if not _result:
                break
            else:
                _match.append(_result)
                _pos = _result.end(0)
    return _match

def meta(_data, _pattern):
    """Return metadata and removed strings"""
    _meta = dict()
    _cache = list()
    _pattern_match = ("encode", "title", "author")
    for _line in _data:
        _meta_cache = copy(_meta)
        for _key, _patt in _pattern.items():
            if _key in _pattern_match:
                _match = _patt.match(_line)
                if _match:
                    _meta[_key] = _match.group(1)
        if _meta == _meta_cache:
            _cache.append(_line)
    return _meta, _cache
