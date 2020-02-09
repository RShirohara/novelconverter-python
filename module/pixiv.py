# -*- coding: utf-8 -*-
# author: RSHirohara

import copy
import re
from . import convert
from . import getData

class pixiv:
    def __init__(self):
        self.FormatName = ('chapter', 'image', 'newpage', 'ruby', 'url')
        self.Format = {
            "chapter": '[chapter:{_field1}]',
            "image": '[pixivimage:{_field1}]',
            "newpage": '[newpage]',
            "ruby": '[[rb:{_field1}>{_field2}]]',
            "url": '[jumpurl:{_field1}>{_field2}]',
        }
        self.Pattern = {
            "chapter": re.compile(r'\[chapter:(?P<_field1>.*?)$\]'),
            "image": re.compile(r'!\[pixivimage:(?P<_field1>.*?)\]'),
            "newpage": re.compile(r'^\[newpage\]$'),
            "ruby": re.compile(r'\[\[rb:(?P<_field1>.*?)>(?P<_field2>.*?)\]\]'),
            "url": re.compile(r'\[jumpurl:(?P<_field1>.*?)>(?P<_field2>.*?)\]'),
        }

    def Convert(self, _data, _pattern):
        """Convert data"""
        _meta = dict()
        _cache = list()
        _result = str()
        # Get and delete metadata
        for _line in _data:
            _meta_cache = copy.copy(_meta)
            for _key, _patt in _pattern.items():
                _meta_result = getData.meta(_line, _key, _patt)
                if _meta_result:
                    _meta[_key] = _meta_result
            if _meta == _meta_cache:
                _cache.append(_line)
        # Set convert pattern
        for _key in _pattern.keys():
            if not _key in self.FormatName:
                if not '_field1' in str(_pattern[_key]):
                    self.Format[_key] = None
                else:
                    self.Format[_key] = '{_field1}'
        # Convert
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                if _match:
                    _line = convert.Convert(_line, _match, self.Format[_key])
            if _line:
                _result += _line
        return _result
