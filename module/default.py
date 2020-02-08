# -*- coding: utf-8 -*-
# author: RShirohara

import copy
import re
from . import Convert
from . import getData

class default:
    def __init__(self):
        self.FormatName = ('encode', 'title', 'author', 'chapter', 'image', 'newpage', 'qwote', 'ruby', 'tate-chu-yoko', 'url')
        self.Format = {
            'encode': '# encoding: {_field1}',
            'author': '# author: {_field1}',
            'title': '# title: {_field1}',
            'chapter': '## {_field1}',
            'image': '![{_field1}]({_field2})',
            'newpage': '========',
            'qwote': '>{_field1}',
            'ruby': '{{_field1}}|{{_field2}}',
            'tate-chu-yoko': '^{_field1}^',
            'url': '[{_field1}]({_field2})',
        }
        self.Pattern = {
            'encode': re.compile(r'^# encoding: (?P<_field>.*?)$'),
            'author': re.compile(r'^# author: (?P<_field>.*?)$'),
            'title': re.compile(r'^# title: (?P<_field>.*?)$'),
            'chapter': re.compile(r'## (?P<_field1>.*?)$'),
            'image': re.compile(r'!\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)'),
            'newpage': re.compile(r'^========'),
            'qwote': re.compile(r'^>(?P<_field1>.*?)$'),
            'ruby': re.compile(r'{(?P<_field1>.*?)\|(?P<_field2>.*?)}'),
            'tate-chu-yoko': re.compile(r'\^(?P<_field1>.*?)\^'),
            'url': re.compile(r'\[(?P<_field1>.*?)]\((?P<_field2>.*?)\)'),
        }

    def Convert(self, _data, _meta, _pattern):
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
