# -*- coding: utf-8 -*-
# author: RShirohara

def match(_data, _pattern):
    """Return matched string"""
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

def meta(_data, _key, _pattern):
    """Return metadata"""
    _pattern_match = ('encode', 'title', 'author')
    if _key in _pattern_match:
        _match = _pattern.match(_data)
        if _match:
            _result = _match.group(1)
            return _result
