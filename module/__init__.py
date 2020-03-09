# -*- coding: utf-8 -*-
# author: RShirohara

from . import form

def call(_format_name):
    if _format_name == "default":
        return form.Default()
    elif _format_name == "ddmarkdown":
        return form.DDMarkdown()
    elif _format_name == "markdown":
        return form.Markdown()
    elif _format_name == "pixiv":
        return form.Pixiv()
    else:
        raise ModuleNotFoundError()
