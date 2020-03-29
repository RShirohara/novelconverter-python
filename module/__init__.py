# -*- coding: utf-8 -*-
# author: RShirohara

from . import form

def call(_name):
    _format = {
        "default": form.Default(),
        "plain": form.Plain(),
        "ddmarkdown": form.DDMarkdown(),
        "markdown": form.Markdown(),
        "pixiv": form.Pixiv()
    }
    if _name in _format.keys():
        return _format[_name]
    else:
        raise ModuleNotFoundError()
