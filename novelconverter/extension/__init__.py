# -*- coding: utf-8 -*-
# author: RShiohara

import sys

from . import ddmarkdown, markdown, pixiv, plain


def call(_format_name):
    """Return the format class"""
    _format = {
        "ddmarkdown": ddmarkdown.DDMarkdown(),
        "markdown": markdown.Markdown(),
        "pixiv": pixiv.Pixiv(),
        "plain": plain.Plain(),
    }
    if _format_name in _format.keys():
        return _format[_format_name]
    else:
        print(f"{_format_name} is not found!")
        sys.exit()
