#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter.extension import markdown


class TestInlineParser(unittest.TestCase):
    """Test class of markdown.inlineparser in extension."""

    def setUp(self):
        self.parser = markdown.build_inlineparser()

    def test_bold(self):
        self.assertEqual(
            '{"type": "bold", "content": ["test"]}',
            self.parser.reg["bold"]("**test**")
        )

    def test_code_inline(self):
        self.assertEqual(
            '{"type": "code_inline", "content": ["test"]}',
            self.parser.reg["code_inline"]("`test`")
        )

    def test_image(self):
        self.assertEqual(
            '{"type": "image", "content": ["test.", "http://example.com"]}',
            self.parser.reg["image"]("![test.](http://example.com)")
        )
        self.assertEqual(
            '{"type": "image", "content": ["example.com", "example.com"]}',
            self.parser.reg["image"]("![](example.com)")
        )

    def test_link(self):
        self.assertEqual(
            '{"type": "link", "content": ["test.", "http://example.com"]}',
            self.parser.reg["link"]("![test.](http://example.com)")
        )
        self.assertEqual(
            '{"type": "link", "content": ["example.com", "example.com"]}',
            self.parser.reg["link"]("![](example.com)")
        )


class TestBlockParser(unittest.TestCase):
    """Test class of markdown.blockparser in extension."""

    def setUp(self):
        self.parser = markdown.build_blockparser()

    def test_code_block(self):
        self.assertEqual(
            {"type": "code_block", "content": [["test1", "test2"], "test"]},
            self.parser.reg["code_block"]("```test\ntest1\ntest2\n```")
        )

    def test_header(self):
        self.assertEqual(
            {"type": "header", "content": ["test 1", 1]},
            self.parser.reg["header"]("# test 1")
        )
        self.assertEqual(
            {"type": "header", "content": ["test 2", 2]},
            self.parser.reg["header"]("## test 2")
        )
        self.assertEqual(
            {"type": "header", "content": ["test 3", 3]},
            self.parser.reg["header"]("### test 3")
        )
        self.assertEqual(
            {"type": "header", "content": ["test 4", 4]},
            self.parser.reg["header"]("#### test 4")
        )
        self.assertEqual(
            {"type": "header", "content": ["test 5", 5]},
            self.parser.reg["header"]("##### test 5")
        )

    def test_item_list(self):
        self.assertEqual(
            {
                "type": "item_list",
                "content": [
                    ["t1", "t2", "t3", "t3-1", "t3-1-1", "t4"],
                    [0, 0, 0, 2, 4, 0]
                ]
            },
            self.parser.reg["item_list"](
                "- t1\n- t2\n+ t3\n  + t3-1\n    * t3-1-1\n1. t4"
            )
        )

    def test_quote(self):
        self.assertEqual(
            {
                "type": "quote",
                "content": [
                    ["t1", "t2", "t2-1", "t2-1-1", "t3"],
                    [1, 1, 2, 3, 1]
                ]
            },
            self.parser.reg["quote"](
                "> t1\n> t2\n> > t2-1\n> > > t2-1-1\n> t3"
            )
        )


class TestRenderer(unittest.TestCase):
    """Test class of markdown.renderer in extension."""

    def setUp(self):
        self.renderer = markdown.build_renderer()

    def test_bold(self):
        self.assertEqual(
            "**test**",
            self.renderer.reg["bold"](
                {"type": "bold", "content": ["test"]}
            )
        )

    def test_code_block(self):
        self.assertEqual(
            "```test\ntest1\ntest2\n```",
            self.renderer.reg["code_block"](
                {"type": "code_block", "content": [["test1", "test2"], "test"]}
            )
        )

    def test_code_inline(self):
        self.assertEqual(
            "`test`",
            self.renderer.reg["code_inline"](
                {"type": "code_inline", "content": ["test"]}
            )
        )

    def test_header(self):
        self.assertEqual(
            "# test 1",
            self.renderer.reg["header"](
                {"type": "header", "content": ["test 1", 1]}
            )
        )

    def test_image(self):
        self.assertEqual(
            "![test.](http://example.com)",
            self.renderer.reg["image"](
                {"type": "image", "content": ["test.", "http://example.com"]}
            )
        )
        self.assertEqual(
            "![](example.com)",
            self.renderer.reg["image"](
                {"type": "image", "content": ["example.com", "example.com"]}
            )
        )

    def test_item_list(self):
        self.assertEqual(
            "- 1\n- 2\n    - 2-1\n        - 2-1-1\n- 3\n- 4",
            self.renderer.reg["item_list"](
                {
                    "type": "item_list",
                    "content": [
                        ["1", "2", "2-1", "2-1-1", "3", "4"],
                        [0, 0, 2, 4, 0, 0]
                    ]
                }
            )
        )

    def test_link(self):
        self.assertEqual(
            "[test.](http://example.com)",
            self.renderer.reg["link"](
                {"type": "link", "content": ["test.", "http://example.com"]}
            )
        )
        self.assertEqual(
            "[](example.com)",
            self.renderer.reg["link"](
                {"type": "link", "content": ["example.com", "example.com"]}
            )
        )

    def test_quote(self):
        self.assertEqual(
            "> t1\n> t2\n> > t2-1\n> > > t2-1-1\n> t3",
            self.renderer.reg["quote"](
                {
                    "type": "quote",
                    "content": [
                        ["t1", "t2", "t2-1", "t2-1-1", "t3"],
                        [1, 1, 2, 3, 1]
                    ]
                }
            )
        )


class TestPostProcessor(unittest.TestCase):
    """Test class of markdown.postprocessor in extension."""

    def setUp(self):
        self.processor = markdown.build_postprocessor()

    def test_add_space(self):
        self.assertEqual(
            "t1  \nt2  \nt3",
            self.processor.reg["add_space"]("t1\nt2\nt3")
        )


class TestPreProcessor(unittest.TestCase):
    """Test class of markdown.preprocessor in extension."""

    def setUp(self):
        self.processor = markdown.build_preprocessor()

    def test_del_space(self):
        self.assertEqual(
            "t1\nt2\nt3",
            self.processor.reg["del_space"]("t1  \nt2  \nt3")
        )


if __name__ == "__main__":
    unittest.main()
