# -*- coding: utf-8 -*-
# author: RSHirohara

import re


def form():
    """Return format data"""
    form = {
        "header": '[chapter:{_str1}]',
        "image": '[pixivimage:{_str1}]',
        "newpage": '[newpage]',
        "ruby": '[[rb:{_str1}>{_str2}]]',
        "url": '[jumpurl:{_str1}>{_str2}]',
    }
    return form

def pattern():
    """Return pattern data"""
    pattern = {
        "header": re.compile(r'\[chapter:(?P<_str1>.*?)$\]'),
        "image": re.compile(r'!\[pixivimage:(?P<_str1>.*?)\]'),
        "newpage": re.compile(r'^\[newpage\]$'),
        "ruby": re.compile(r'\[\[rb:(?P<_str1>.*?)>(?P<_str2>.*?)\]\]'),
        "url": re.compile(r'\[jumpurl:(?P<_str1>.*?)>(?P<_str2>.*?)\]'),
    }
    return pattern
