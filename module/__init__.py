# -*- coding: utf-8 -*-
# author: RShirohara

_name = ("markdown", "ddmarkdown", "pixiv")

def call(_format_name):
    if _format_name in _name:
        exec(f'from . import {_format_name} as _format')
        return exec(f'_format.{_format_name}()')
    else:
        raise ModuleNotFoundError('No format! : {_format_name}')
