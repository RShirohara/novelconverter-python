# -*- coding: utf-8 -*-
# author: @RShirohara

import json
import re

from novelconverter import parser, processor, renderer

_BOLD = re.compile(r"\*\*(?P<text>.*?)\*\*")
_CODE_INLINE = re.compile(r"`(?P<text>.*?)`")
_IMAGE = re.compile(r"!\[(?P<text>.*?){,1}\]\((?P<link>.*?)\)")
_LINK = re.compile(r"\[(?P<text>.*?){,1}\]\((?P<link>.*?)\)")
_HEADER = re.compile(r"^(?P<level>#{1,6}) (?P<title>.*?) {,1}#{0,}$")
_CODE_BLOCK = re.compile(
    r"^```(?P<lang>.*?){,1}\n(?P<text>.*?)\n```$", re.DOTALL
)
_ITEM_LIST = re.compile(
    r"^(?P<level>(  ){,})([-+*]|[0-9]+[.]) (?P<text>.*?)$"
)
_INDENT = re.compile(r"^(?P<level>(  ){1,})(?P<text>.*?)$")
_QUOTE = re.compile(r"^(?P<level>(> {,1}){1,})(?P<text>.*?)$")


def build_inlineparser():
    parser = InlineParser()
    parser.reg.add(parser.code_inline, "code_inline", 40)
    parser.reg.add(parser.bold, "bold", 30)
    parser.reg.add(parser.image, "image", 20)
    parser.reg.add(parser.link, "link", 10)
    return parser


def build_blockparser():
    parser = BlockParser()
    parser.reg.add(parser.code_block, "code_block", 50)
    parser.reg.add(parser.header, "header", 40)
    parser.reg.add(parser.item_list, "item_list", 30)
    parser.reg.add(parser.quote, "quote", 20)
    parser.reg.add(parser.para, "para", 10)
    return parser


def build_renderer():
    renderer = Renderer()
    renderer.reg.add(renderer.bold, "bold", 110)
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


def build_preprocessor():
    processor = PreProcessor()
    processor.reg.add(processor.del_space, "del_space", 10)
    return processor


def build_postprocessor():
    processor = PostProcessor()
    processor.reg.add(processor.add_space, "add_space", 10)
    return processor


class InlineParser(parser.InlineParser):
    def bold(self, source):
        _pos = 0
        while True:
            _match = _BOLD.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = '{"type": "bold", ' + \
                f'"content": ["{_dict["text"]}\"]' + \
                "}"
            source = source.replace(_old, _new)
        return source

    def code_inline(self, source):
        _pos = 0
        while True:
            _match = _CODE_INLINE.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = '{"type: "code_inline", ' + \
                f'"content": ["{_dict["text"]}"]' + \
                "}"
            source = source.replace(_old, _new)
        return source

    def image(self, source):
        _pos = 0
        while True:
            _match = _IMAGE.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(0)
            _dict = _match.groupdict()
            _old = _match.group(0)
            _new = '{"type": "image", "content": [' + \
                f'"{_dict["text"] if _dict["text"] else _dict["link"]}"' + \
                f', "{_dict["link"]}"]' + \
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
            _new = '{"type": "image", "content": [' + \
                f'"{_dict["text"] if _dict["text"] else _dict["link"]}"' + \
                f', "{_dict["link"]}"]' + \
                "}"
            source = source.replace(_old, _new)
        return source


class BlockParser(parser.BlockParser):
    def header(self, source):
        _match = _HEADER.match(source)
        if not _match:
            return
        _dict = _match.groupdict()
        result = {
            "type": "header",
            "content": [_dict["title"], len(_dict["level"])]
        }
        return result

    def code_block(self, source):
        _match = _CODE_BLOCK.match(source)
        if not _match:
            return
        _dict = _match.groupdict()
        result = {
            "type": "code_block",
            "content": [
                _dict["text"].splitlines(),
                _dict["lang"]
            ]
        }
        return result

    def item_list(self, source):
        text = []
        level = []
        for s in source.splitlines():
            _index = len(text) - 1
            _match = _ITEM_LIST.match(s)
            if not _match:
                _match_indent = _INDENT.match(s)
                if not _match_indent:
                    return
                if level[_index] + 2 == len(_match_indent.group(1)):
                    text[_index] += f"\n{_match_indent.group(3)}"
                continue
            _dic = _match.groupdict()
            text.append(_dic["text"])
            level.append(len(_dic["level"]))
        result = '{"type": "item_list", ' +\
            f'"content": [{text}, {level}]'.replace("'", '"') + \
            "}"
        return json.loads(result)

    def quote(self, source):
        text = []
        level = []
        for s in source.splitlines():
            _match = _QUOTE.match(s)
            if not _match:
                return
            _dict = _match.groupdict()
            text.append(_dict["text"])
            level.append(len(_dict["level"].replace(" ", "")))
        result = '{"type": "quote", ' + \
            f'"content": [{text}, {level}]'.replace("'", '"') + \
            "}"
        return json.loads(result)


class Renderer(renderer.Renderer):
    def header(self, source):
        level = "#" * source["content"][1]
        return f"{level} {source['content'][0]}"

    def code_block(self, source):
        result = self._join_nest(source["content"][0], "\n", "")
        lang = source["content"][1]
        return f"```{lang}\n{result}```"

    def item_list(self, source):
        result = [
            "  "*l+"- "+s for s, l in zip(source["content"][0],
                                          source["content"][1])
        ]
        return "\n".join(result)

    def quote(self, source):
        result = [
            "> "*l+s for s, l in zip(source["content"][0],
                                     source["content"][1])
        ]
        return "\n".join(result)

    def bold(self, source):
        return f'**{source["content"][0]}**'

    def code_inline(self, source):
        return f'`{source["content"][0]}`'

    def image(self, source):
        text = source["content"][0]
        link = source["content"][1]
        if text == link:
            text = ""
        return f"![{text}]({link})"

    def link(self, source):
        text = source["content"][0]
        link = source["content"][1]
        if text == link:
            text = ""
        return f"[{text}]({link})"


class PreProcessor(processor.PreProcessor):
    def del_space(self, source):
        """Delete a space at the end of line."""
        return source.replace("  \n", "\n")


class PostProcessor(processor.PostProcessor):
    def add_space(self, source):
        """Add a space at the end of line."""
        return source.replace("\n", "  \n")
