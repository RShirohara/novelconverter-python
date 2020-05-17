# -*- coding: utf-8 -*-
# author: RShirohara

import copy
import re


class DDMarkdown:
    def __init__(self):
        self.FormatName = (
            "encode",
            "title",
            "author",
            "chapter",
            "image",
            "newpage",
            "qwote",
            "ruby",
            "tate-chu-yoko",
            "url",
        )
        self.Format = {
            "encode": "<!-- encoding: {_f1} -->",
            "author": "<!-- author: {_f1} -->",
            "title": "# {_f1}",
            "chapter": "## {_f1}",
            "image": "![{_f1}]({_f2})",
            "newpage": "========",
            "qwote": "> {_f1}",
            "ruby": "{{{_f1}}}|{{{_f2}}}",
            "tate-chu-yoko": "^{_f1}^",
            "url": "[{_f1}]({_f2})",
        }
        self.Pattern = {
            "encode": re.compile(
                r"^<!-- encoding: (?P<_f1>.*?) -->", re.MULTILINE),
            "author": re.compile(
                r"^<!-- author: (?P<_f1>.*?) -->", re.MULTILINE),
            "title": re.compile(r"^#{,1} (?P<_f1>.*)", re.MULTILINE),
            "chapter": re.compile(r"^#{2,5} (?P<_f1>.*)", re.MULTILINE),
            "image": re.compile(r"!\[(?P<_f1>.*?)\]\((?P<_f2>.*?)\)"),
            "newpage": re.compile(r"^========", re.MULTILINE),
            "qwote": re.compile(r"^>{1,} (?P<_f1>.*?)", re.MULTILINE),
            "ruby": re.compile(r"{(?P<_f1>.*?)\|(?P<_f2>.*?)}"),
            "tate-chu-yoko": re.compile(r"\^(?P<_f1>.*?)\^"),
            "url": re.compile(r"\[(?P<_f1>.*?)]\((?P<_f2>.*?)\)"),
        }

    def match(self, _data, _from_pattern):
        """Return the matched object"""
        _match = list()
        _pos = 0
        while True:
            _result = _from_pattern.search(_data, pos=_pos)
            if not _result:
                break
            _match.append(_result)
            _pos = _result.end(0)
        return tuple(_match)

    def convert(self, _data, _check_list, _from_pattern):
        """Return the converted data"""
        _converted_data = copy.copy(_data)
        for _key in _check_list:
            for _match in self.match(_converted_data, _from_pattern[_key]):
                _old = _match.group(0)
                _new_dict = _match.groupdict()
                if "_f2" in _match.re.pattern and self.Format[_key]:
                    _new = self.Format[_key].format(**_new_dict)
                elif "_f1" in _match.re.pattern:
                    _new = self.Format[_key].format(
                        _f1=_new_dict["_f1"])
                else:
                    _new = self.Format[_key]
                _converted_data = _converted_data.replace(_old, _new)
        while True:
            if "\n\n\n" not in _converted_data:
                break
            _converted_data = _converted_data.replace("\n\n\n", "\n\n")
        return _converted_data
