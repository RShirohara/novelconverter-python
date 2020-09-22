# -*- coding: utf-8 -*-
# author: @RShirohara

import json
import re

from novelconverter import parser, renderer

_IMAGE = re.compile(r"!\[pixivimage:(?P<link>.*?)")
_LINK = re.compile(r"\[jumpurl:(?P<string>.*?)>(?P<url>.*?)\]")
_RUBY = re.compile(r"\[\[rb:(?P<text>.*?)>(?P<ruby>.*?)\]\]")
_HEADER = re.compile(r"\[chapter:(?P<name>.*?)\]")
_NEW_PAGE = re.compile(r"\[newpage\]")


def build_inlineparser():
    pass


def build_blockparser():
    pass


def build_renderer():
    pass


class InlineParser(parser.InlineParser):
    def image(self, source):
        _pos = 0
        while True:
            _match = _IMAGE.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = "{\"type\": \"image\", " + \
                f"\"content\": [\"{_dict['link']}\", \"{_dict['link']}\"]" + \
                "}"
            source = source.replace(_old, _new)
        return source

    def link(self, source):
        _pos = 0
        while True:
            _match = _LINK.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = "{\"type\": \"link\", " + \
                f"content\": [\"{_dict['string']}\", \"{_dict['url']}\"]" + \
                "}"
            source = source.replace(_old, _new)
        return source

    def ruby(self, source):
        _pos = 0
        while True:
            _match = _RUBY.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = "{\"type\": \"ruby\", " + \
                f"\"content\": [\"{_dict['text']}\", \"{_dict['ruby']}\"]" + \
                "}"
            source = source.replace(_old, _new)
        return source


class BlockParser(parser.BlockParser):
    def header(self, source):
        _match = _HEADER.match(source)
        if not _match:
            return
        _dict = _match.groupdict()
        result = "{\"type\": \"header\", " + \
            f"\"content\": [\"{_dict['name']}\", 2]" + \
            "}"
        return json.loads(result)

    def newpage(self, source):
        _match = _NEW_PAGE.match(source)
        if not _match:
            return
        return json.loads("{\"type\": \"newpage\"}")


class Renderer(renderer.Renderer):
    def image(self, source):
        return f"[pixivimage:{source['content'][0]}]"

    def link(self, source):
        return f"[jumpurl:{source['content'][0]}>{source['content'][1]}]"

    def ruby(self, source):
        return f"[[rb:{source['content'][0]}>{source['content'][1]}]]"

    def header(self, source):
        return f"[chapter:{source['content'][0]}"

    def newpage(self, source):
        return "[newpage]"
