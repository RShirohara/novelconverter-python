# -*- coding: utf-8 -*-
# author: @RShirohara


import json
import re

from . import util

_PARA = re.compile(r"\n\n(.*?)\n\n", re.DOTALL)


def build_parser():
    """Build the default parsers."""
    parser = Parser()
    # parser.reg.add(item, name, priority)
    parser.reg.add(parser.para, "para", 10)
    return parser


class Parser(util.Processor):
    """Parse strings into a JSON-formatted string

    Example:
        {
            "type": "parser name"
            "content": [content]
        }

    In most cases, the 0th element in "content" will be output if the
    corresponding "Renderer" does not exist.
    """

    def run(self, source):
        """Run parser"""
        for i in self.reg:
            source = i(source)
        return source.replace("\n\n", "\n")

    def para(self, source):
        """Paragraph

        Example:
            {"type": "para", "content": ["content strings"]}
        """
        result = []
        _pos = 0
        while True:
            _match = _PARA.search(source, pos=_pos)
            if not _match:
                break
            _pos = _match.end(1)
            result.append(_match)
        for r in result:
            _content = str(r.group(1).splitlines()).replace("\'", "\"")
            _new = "{" + f"\"type\": \"para\", \"content\": {_content}" + "}"
            try:
                json.loads(r.group(1))
            except ValueError:
                source = source.replace(r.group(1), _new)
        return source

    def header(self, source):
        """Header

        Example:
            {"type": "header", "content": ["Header name", level]}
        """
        pass

    def quote(self, source):
        """Quote

        Example:
            {"type": "quote", "content": ["content strings", level]}
        """
        pass

    def item_list(self, source):
        """Item list

        Example:
            {"type": "item_list", "content": ["1", "2", ["2-1", "2-2]]}
        """
        pass

    def code_block(self, source):
        """Code block

        Example:
            {"type": "code_block", "content": ["content strings", "language"]}
        """
        pass

    def newpage(self, source):
        """New page

        Example:
            {"type": "newpage"}
        """
        pass

    def link(self, source):
        """Hyper link

        Example:
            {"type": "link", "content": ["strings", "url"]}
        """
        pass

    def bold(self, source):
        """Bold in text

        Example:
            {"type": "bold", "content": ["strings"]}
        """
        pass

    def ruby(self, source):
        """Ruby text

        Example:
            {"type": "ruby", "content": ["text", "ruby"]}
        """
        pass

    def tcy(self, source):
        """Tate chu Yoko

        Example:
            {"type": "tcy", "content": ["text"]}
        """
        pass

    def image(self, source):
        """Image

        Example:
            {"type": "image", "content", ["text", "link"]}
        """
        pass
