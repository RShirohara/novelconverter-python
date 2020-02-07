# -*- coding: utf-8 -*-
# author: RShirohara

def getData(_data, _pattern):
    """Return matched string"""
    _match = list()
    _pos = 0
    while True:
        _result = _pattern.search(_data, pos = _pos)
        if not _result:
            break
        else:
            _match.append(_result)
            _pos = _result.end(0)
    return _match
