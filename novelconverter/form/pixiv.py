# -*- coding: utf-8 -*-
# author: RShirohara

import copy
import re


class Pixiv:
    def __init__(self):
        self.FormatName = (
            "chapter",
            "image",
            "newpage",
            "ruby",
            "url"
        )
        self.Format = {
            "chapter": "[chapter:{_f1}]",
            "image": "[pixivimage:{_f1}]",
            "newpage": "[newpage]",
            "ruby": "[[rb:{_f1}>{_f2}]]",
            "url": "[jumpurl:{_f1}>{_f2}]",
        }
        self.Pattern = {
            "chapter": re.compile(r"\[chapter:(?P<_f1>.*?)\]"),
            "image": re.compile(r"!\[pixivimage:(?P<_f1>.*?)\]"),
            "newpage": re.compile(r"\[newpage\]"),
            "ruby": re.compile(r"\[\[rb:(?P<_f1>.*?)>(?P<_f2>.*?)\]\]"),
            "url": re.compile(r"\[jumpurl:(?P<_f1>.*?)>(?P<_f2>.*?)\]"),
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
        _converted_data = re.sub(r"\n{3,}", "\n\n", _converted_data)
        return _converted_data
