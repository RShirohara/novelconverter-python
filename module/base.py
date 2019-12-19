# -*- coding: utf-8 -*-
# author: RShirohara

import re


def form():
    """Return format data"""
    _form = {
        "header": '## {_str1}',
        "image": '![{_str1}]({_str2})',
        "newpage": '========',
        "qwote": '>{_str1}',
        "ruby": '{{_str1}}|{{_str2}}',
        "tate-chu-yoko": '^{_str1}^',
        "url": '[{_str1}]({_str2})',
    }
    return _form

def pattern():
    """Return pattern data"""
    _pattern = {
        "header": re.compile(r'## (?P<_str1>.*?)$'),
        "image": re.compile(r'!\[(?P<_str1>.*?)\]\((?P<_str2>.*?)\)'),
        "newpage": re.compile(r'^========'),
        "qwote": re.compile(r'^>(?P<_str1>.*?)$'),
        "ruby": re.compile(r'{(?P<_str1>.*?)\|(?P<_str2>.*?)}'),
        "tate-chu-yoko": re.compile(r'\^(?P<_str1>.*?)\^'),
        "url": re.compile(r'\[(?P<_str1>.*?)]\((?P<_str2>.*?)\)'),
    }
    return _pattern
