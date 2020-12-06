#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter.extension import ddmarkdown


class TestInlineParser(unittest.TestCase):
    """Test class of ddmarkdown.inlineparser in extension."""

    def setUp(self):
        self.parser = ddmarkdown.build_inlineparser()

    def test_ruby(self):
        self.assertEqual(
            '{"type": "ruby", "content": ["私", "わたし"]}',
            self.parser.reg["ruby"]("{私|わたし}")
        )

    def test_tcy(self):
        self.assertEqual(
            '{"type": "tcy", "content": ["12"]}',
            self.parser.reg["tcy"]("^12^")
        )


class TestBlockParser(unittest.TestCase):
    """Test class of ddmarkdown.blockparser in extension."""

    def setUp(self):
        self.parser = ddmarkdown.build_blockparser()

    def test_newpage(self):
        self.assertEqual(
            {"type": "newpage"},
            self.parser.reg["newpage"]("========")
        )


class TestRenderer(unittest.TestCase):
    """Tests class of ddmarkdown.renderer in extension."""

    def setUp(self):
        self.renderer = ddmarkdown.build_renderer()

    def test_newpage(self):
        self.assertEqual(
            "========",
            self.renderer.reg["newpage"]({"type": "newpage"})
        )

    def test_ruby(self):
        self.assertEqual(
            "{私|わたし}",
            self.renderer.reg["ruby"](
                {"type": "ruby", "content": ["私", "わたし"]}
            )
        )

    def test_tcy(self):
        self.assertEqual(
            "^12^",
            self.renderer.reg["tcy"]({"type": "tcy", "content": ["12"]})
        )


if __name__ == "__main__":
    unittest.main()
