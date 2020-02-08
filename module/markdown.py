# -*- coding: utf-8 -*-
# author: RShirohara

import copy
import re
from . import Convert
from . import getData

class markdown:
    def __init__(self):
        self.FormatName = ('title', 'chapter', 'image', 'qwote', 'url')
        self.Format = {
            'title': '# {_field1}',
            'chapter': '## {_field1}',
            'image': '![{_field1}]({_field2})',
            'qwote': '>{_field1}',
            'url': '[{_field1}]({_field2})',
        }
        self.Pattern = {
            'title': re.compile(r'^# (?P<_field>.*?)$'),
            'chapter': re.compile(r'## (?P<_field1>.*?)$'),
            'image': re.compile(r'!\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)'),
            'qwote': re.compile(r'^>(?P<_field1>.*?)$'),
            'url': re.compile(r'\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)'),
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
                    _line = Convert.Convert(_line, _match, self.Format[_key])
            if _line:
                _result += _line
        return _result
