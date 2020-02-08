# -*- coding: utf-8 -*-
# author: RShirohara

_format = ('default', 'markdown', 'ddmarkdown', 'pixiv')

def call(_format_name):
    if _format_name == 'default':
        from . import default
        return default.default()
    elif _format_name == 'markdown':
        from . import markdown
        return markdown.markdown()
    elif _format_name == 'ddmarkdown':
        from . import ddmarkdown
        return ddmarkdown.ddmarkdown()
    elif _format_name == 'pixiv':
        from . import pixiv
        return pixiv.pixiv()
    else:
        raise ModuleNotFoundError()
