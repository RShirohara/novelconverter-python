# -*- coding: utf-8 -*-
# author: @RShirohara

from copy import copy

from . import util


def build_renderer():
    """Build the default renderers."""
    renderer = Renderer()
    renderer.reg.add(renderer.newpage, "newline", 110)
    renderer.reg.add(renderer.header, "header", 100)
    renderer.reg.add(renderer.code_block, "code_block", 90)
    renderer.reg.add(renderer.item_list, "item_list", 80)
    renderer.reg.add(renderer.quote, "quote", 70)
    renderer.reg.add(renderer.para, "para", 60)
    renderer.reg.add(renderer.bold, "bold", 50)
    renderer.reg.add(renderer.image, "image", 40)
    renderer.reg.add(renderer.link, "link", 30)
    renderer.reg.add(renderer.ruby, "ruby", 20)
    renderer.reg.add(renderer.tcy, "tcy", 10)
    return renderer


class Renderer(util.Processor):
    """Renders the ElementTree into a formatted string."""

    def _render_block(self, source):
        _result = copy(source)
        if type(_result) == list:
            for i in range(len(_result)):
                _result[i] = "".join(self._render_block(_result[i]))
        if type(_result) == dict:
            _result["content"] = self._render_block(_result["content"])
            _result = self.reg[_result["type"]](_result)
        return _result

    def run(self, tree):
        result = copy(tree.root["block"])
        for i in range(len(tree)):
            result[i] = self._render_block(result[i])
        return result

    def para(self, _result):
        """Paragraph"""
        return "\n".join(_result["content"])

    def header(self, _result):
        """Header"""
        return _result["content"][0]

    def code_block(self, _result):
        """Code block"""
        return "\n".join(_result["content"][0])

    def item_list(self, _result):
        """Item list"""
        return "\n".join(_result["content"][0][0])

    def quote(self, _result):
        """Quote"""
        return "\n".join(_result["content"][0])

    def newpage(self, _result):
        """New page"""
        pass

    def bold(self, _result):
        """Bold text"""
        return _result["content"][0]

    def image(self, _result):
        """Image link"""
        return _result["content"][0]

    def link(self, _result):
        """Hyper link"""
        return _result["content"][0]

    def ruby(self, _result):
        """Ruby text"""
        return _result["content"][0]

    def tcy(self, _result):
        """Tate chu Yoko"""
        return _result["content"][0]
