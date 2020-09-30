# -*- coding: utf-8 -*-
# author: @RShirohara

import re

from . import markdown

_RUBY = re.compile(r"{(?P<text>.*?)\|(?P<ruby>.*?)}")
_TCY = re.compile(r"\^(?P<text>.*?)\^")
_NEWPAGE = re.compile(r"^={3,}$")


def build_inlineparser():
    parser = InlineParser()
    parser.reg.add(parser.code_inline, "code_inline", 60)
    parser.reg.add(parser.ruby, "ruby", 50)
    parser.reg.add(parser.tcy, "tcy", 40)
    parser.reg.add(parser.bold, "bold", 30)
    parser.reg.add(parser.image, "image", 20)
    parser.reg.add(parser.link, "link", 10)
    return parser


def build_blockparser():
    parser = BlockParser()
    parser.reg.add(parser.code_block, "code_block", 60)
    parser.reg.add(parser.newpage, "newpage", 50)
    parser.reg.add(parser.header, "header", 40)
    parser.reg.add(parser.item_list, "item_list", 30)
    parser.reg.add(parser.quote, "quote", 20)
    parser.reg.add(parser.para, "para", 10)
    return parser


def build_renderer():
    renderer = Renderer()
    renderer.reg.add(renderer.bold, "bold", 120)
    renderer.reg.add(renderer.code_inline, "code_inline", 110)
    renderer.reg.add(renderer.image, "image", 100)
    renderer.reg.add(renderer.link, "link", 90)
    renderer.reg.add(renderer.ruby, "ruby", 80)
    renderer.reg.add(renderer.tcy, "tcy", 70)
    renderer.reg.add(renderer.newpage, "newpage", 60)
    renderer.reg.add(renderer.header, "header", 50)
    renderer.reg.add(renderer.code_block, "code_block", 40)
    renderer.reg.add(renderer.item_list, "item_list", 30)
    renderer.reg.add(renderer.quote, "quote", 20)
    renderer.reg.add(renderer.para, "para", 10)
    return renderer


class InlineParser(markdown.InlineParser):
    def ruby(self, source):
        _pos = 0
        while True:
            _match = _RUBY.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = '{"type": "ruby", ' + \
                f'"content": ["{_dict["text"]}", "{_dict["ruby"]}"]' + \
                "}"
            source = source.replace(_old, _new)
        return source

    def tcy(self, source):
        _pos = 0
        while True:
            _match = _TCY.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = '{"type": "tcy", ' + \
                f'"content": ["{_dict["text"]}"]' + \
                "}"
            source = source.replace(_old, _new)
        return source


class BlockParser(markdown.BlockParser):
    def newpage(self, source):
        _match = _NEWPAGE.match(source)
        if not _match:
            return
        result = {
            "type": "newpage",
        }
        return result


class Renderer(markdown.Renderer):
    def newpage(self, source):
        return "========"

    def ruby(self, source):
        text = source["content"][0]
        ruby = source["content"][1]
        return "{" + f"{text}|{ruby}" + "}"
