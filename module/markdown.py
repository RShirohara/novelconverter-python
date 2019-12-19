# -*- coding: utf-8 -*-
# author: RShirohara

import re

def form():
    """Return format data"""
    form = {
        "header": '## {_str1}',
        "image": '![{_str1}]({_str2})',
        "qwote": '>{_str1}',
        "url": '[{_str1}]({_str2})',
    }
    return form

def pattern():
    """Return pattern data"""
    pattern = {
        "header": re.compile(r'## (?P<_str1>.*?)$'),
        "image": re.compile(r'!\[(?P<_str1>.*?)\]\((?P<_str2>.*?)\)'),
        "qwote": re.compile(r'^>(?P<_str1>.*?)$'),
        "url": re.compile(r'\[(?P<_str1>.*?)\]\((?P<_str2>.*?)\)'),
    }
    return pattern
