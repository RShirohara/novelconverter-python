#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter.extension import pixiv


class TestBlockParser(unittest.TestCase):
    """Test class of pixiv.blockparser in extension."""

    def setUp(self):
        self.parser = pixiv.build_blockparser()

    def test_header(self):
        self.assertEqual(
            {"type": "header", "content": ["test", 2]},
            self.parser.reg["header"]("[chapter:test]")
        )

    def test_newpage(self):
        self.assertEqual(
            {"type": "newpage"},
            self.parser.reg["newpage"]("[newpage]")
        )


class TestInlineParser(unittest.TestCase):
    """Test class of pixiv.inlineparser in extension."""

    def setUp(self):
        self.parser = pixiv.build_inlineparser()

    def test_image(self):
        self.assertEqual(
            '{"type": "image", "content": ["12345678", "12345678"]}',
            self.parser.reg["image"]("[pixivimage:12345678]")
        )

    def test_link(self):
        self.assertEqual(
            '{"type": "link", "content": ["example", "http://example.com"]}',
            self.parser.reg["link"]("[jumpurl:example>http://example.com]")
        )

    def test_ruby(self):
        self.assertEqual(
            '{"type": "ruby", "content": ["私", "わたし"]}',
            self.parser.reg["ruby"]("[[rb:私>わたし]]")
        )


class TestRenderer(unittest.TestCase):
    """Test class of pixiv.renderer in extension."""

    def setUp(self):
        self.renderer = pixiv.build_renderer()

    def test_header(self):
        self.assertEqual(
            "[chapter:test]",
            self.renderer.reg["header"](
                {"type": "header", "content": ["test", 2]}
            )
        )
        self.assertEqual(
            "[chapter:test]",
            self.renderer.reg["header"](
                {"type": "header", "content": ["test", 5]}
            )
        )

    def test_image(self):
        self.assertEqual(
            "[pixivimage:12345678]",
            self.renderer.reg["image"](
                {"type": "image", "content": ["12345678", "12345678"]}
            )
        )

    def test_link(self):
        self.assertEqual(
            "[jumpurl:example.com>http://example.com]",
            self.renderer.reg["link"](
                {
                    "type": "link",
                    "content": [
                        "example.com",
                        "http://example.com"
                    ]
                }
            )
        )

    def test_newpage(self):
        self.assertEqual(
            "[newpage]",
            self.renderer.reg["newpage"]({"type": "newpage"})
        )

    def test_ruby(self):
        self.assertEqual(
            "[[rb:私>わたし]]",
            self.renderer.reg["ruby"](
                {"type": "ruby", "content": ["私", "わたし"]}
            )
        )


if __name__ == "__main__":
    unittest.main()
