# -*- coding: utf-8 -*-
# author: RShirohara

import copy
import re
from . import getData
from . import conv


class Default:
    def __init__(self):
        self.FormatName = ("encode", "title", "author", "chapter", "image", "newpage", "qwote", "ruby", "tate-chu-yoko", "url")
        self.Format = {
            "encode": "# encoding: {_field1}",
            "author": "# author: {_field1}",
            "title": "# title: {_field1}",
            "chapter": "## {_field1}",
            "image": "![{_field1}]({_field2})",
            "newpage": "========",
            "qwote": ">{_field1}",
            "ruby": "{{{_field1}}}|{{{_field2}}}",
            "tate-chu-yoko": "^{_field1}^",
            "url": "[{_field1}]({_field2})",
        }
        self.Pattern = {
            "encode": re.compile(r"^# encoding: (?P<_field>.*?)$"),
            "author": re.compile(r"^# author: (?P<_field>.*?)$"),
            "title": re.compile(r"^# title: (?P<_field>.*?)$"),
            "chapter": re.compile(r"^## (?P<_field1>.*?)$"),
            "image": re.compile(r"!\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)"),
            "newpage": re.compile(r"^========"),
            "qwote": re.compile(r"^>(?P<_field1>.*?)"),
            "ruby": re.compile(r"{(?P<_field1>.*?)\|(?P<_field2>.*?)}"),
            "tate-chu-yoko": re.compile(r"\^(?P<_field1>.*?)\^"),
            "url": re.compile(r"\[(?P<_field1>.*?)]\((?P<_field2>.*?)\)"),
        }

    def convert(self, _data, _pattern):
        """Convert data"""
        _result = str()
        # Get and delete metadata
        _meta, _cache = getData.meta(_data, _pattern)
        # Set convert pattern
        self.Format = conv.setPatt(_pattern, self.Format, self.FormatName)
        # Convert
        if _meta:
            for _key in _meta.keys():
                _result += self.Format[_key].format(_field1 = _meta[_key]) + "\n"
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                _line = conv.conv(_line, _match, self.Format[_key])
            _result += _line
        return _result


class Plain:
    def __init__(self):
        self.FormatName = {}
        self.Format = {}
        self.Pattern = {}

    def convert(self, _data, _pattern):
        """Convert data"""
        _result = str()
        # delete metadata
        _meta, _cache = getData.meta(_data, _pattern)
        # Set convert pattern
        self.Format = conv.setPatt(_pattern, self.Format, self.FormatName)
        # Convert
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                _line = conv.conv(_line, _match, self.Format[_key])
            _result += _line
        return _result


class DDMarkdown:
    def __init__(self):
        self.FormatName = ("chapter", "image", "newpage", "qwote", "ruby", "tate-chu-yoko", "url")
        self.Format = {
            "chapter": "## {_field1}",
            "image": "![{_field1}]({_field2})",
            "newpage": "========",
            "qwote": ">{_field1}",
            "ruby": "{{{_field1}}}|{{{_field2}}}",
            "tate-chu-yoko": "^{_field1}^",
            "url": "[{_field1}]({_field2})",
        }
        self.Pattern = {
            "chapter": re.compile(r"^## (?P<_field1>.*?)$"),
            "image": re.compile(r"!\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)"),
            "newpage": re.compile(r"^========"),
            "qwote": re.compile(r"^>(?P<_field1>.*?)"),
            "ruby": re.compile(r"{(?P<_field1>.*?)\|(?P<_field2>.*?)}"),
            "tate-chu-yoko": re.compile(r"\^(?P<_field1>.*?)\^"),
            "url": re.compile(r"\[(?P<_field1>.*?)]\((?P<_field2>.*?)\)"),
        }

    def convert(self, _data, _pattern):
        """Convert data"""
        _result = str()
        # Get and delete metadata
        _meta, _cache = getData.meta(_data, _pattern)
        # Set convert pattern
        self.Format = conv.setPatt(_pattern, self.Format, self.FormatName)
        # Convert
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                _line = conv.conv(_line, _match, self.Format[_key])
            _result += _line
        return _result


class Markdown:
    def __init__(self):
        self.FormatName = ("title", "chapter", "image", "qwote", "url")
        self.Format = {
            "title": "# {_field1}",
            "chapter": "## {_field1}",
            "image": "![{_field1}]({_field2})",
            "qwote": ">{_field1}",
            "url": "[{_field1}]({_field2})",
        }
        self.Pattern = {
            "title": re.compile(r"^# (?P<_field>.*?)$"),
            "chapter": re.compile(r"^## (?P<_field1>.*?)$"),
            "image": re.compile(r"!\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)"),
            "qwote": re.compile(r"^>(?P<_field1>.*?)"),
            "url": re.compile(r"\[(?P<_field1>.*?)\]\((?P<_field2>.*?)\)"),
        }

    def convert(self, _data, _pattern):
        """Convert data"""
        _result = str()
        # Get and delete metadata
        _meta, _cache = getData.meta(_data, _pattern)
        # Set convert pattern
        self.Format = conv.setPatt(_pattern, self.Format, self.FormatName)
        # Convert
        if "title" in _meta.keys():
            _result = self.Format["title"].format(_field1 = _meta["title"]) + "\n"
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                _line = conv.conv(_line, _match, self.Format[_key])
            if len(_line) > 2:
                _line = _line.replace("\n", "  \n")
            _result += _line
        # Remove duplicate line breaks
        _result = re.sub(r"\n{3}", "\n\n", _result, flags = re.DOTALL)
        return _result


class Pixiv:
    def __init__(self):
        self.FormatName = ("chapter", "image", "newpage", "ruby", "url")
        self.Format = {
            "chapter": "[chapter:{_field1}]",
            "image": "[pixivimage:{_field1}]",
            "newpage": "[newpage]",
            "ruby": "[[rb:{_field1}>{_field2}]]",
            "url": "[jumpurl:{_field1}>{_field2}]",
        }
        self.Pattern = {
            "chapter": re.compile(r"^\[chapter:(?P<_field1>.*?)$\]"),
            "image": re.compile(r"!\[pixivimage:(?P<_field1>.*?)\]"),
            "newpage": re.compile(r"^\[newpage\]$"),
            "ruby": re.compile(r"\[\[rb:(?P<_field1>.*?)>(?P<_field2>.*?)\]\]"),
            "url": re.compile(r"\[jumpurl:(?P<_field1>.*?)>(?P<_field2>.*?)\]"),
        }

    def convert(self, _data, _pattern):
        """Convert data"""
        _result = str()
        # Get and delete metadata
        _meta, _cache = getData.meta(_data, _pattern)
        # Set convert pattern
        self.Format = conv.setPatt(_pattern, self.Format, self.FormatName)
        # Convert
        for _line in _cache:
            for _key, _patt in _pattern.items():
                _match = getData.match(_line, _patt)
                _line = conv.conv(_line, _match, self.Format[_key])
            _result += _line
        return _result
